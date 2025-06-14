"""Knowledge graph implementation using Neo4j."""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import asyncio
from neo4j import AsyncGraphDatabase, AsyncDriver
import json

from ..core.config import Config
from ..utils.logging import get_logger


logger = get_logger(__name__)


@dataclass
class Node:
    """Knowledge graph node."""
    id: str
    labels: List[str]
    properties: Dict[str, Any]


@dataclass
class Relationship:
    """Knowledge graph relationship."""
    id: str
    type: str
    start_node: str
    end_node: str
    properties: Dict[str, Any]


@dataclass
class GraphQuery:
    """Query for knowledge graph."""
    cypher: str
    parameters: Dict[str, Any]
    description: str


class KnowledgeGraph:
    """Neo4j-based knowledge graph for semantic relationships."""
    
    def __init__(self, uri: str, username: str, password: str):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver: Optional[AsyncDriver] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize Neo4j connection."""
        if self._initialized:
            return
        
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            
            # Test connection
            async with self.driver.session() as session:
                await session.run("RETURN 1")
            
            # Create indexes
            await self._create_indexes()
            
            self._initialized = True
            logger.info("Knowledge graph initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge graph: {e}")
            raise
    
    async def close(self) -> None:
        """Close Neo4j connection."""
        if self.driver:
            await self.driver.close()
            self._initialized = False
    
    async def _create_indexes(self) -> None:
        """Create necessary indexes for performance."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS FOR (n:Knowledge) ON (n.key)",
            "CREATE INDEX IF NOT EXISTS FOR (n:Knowledge) ON (n.created_at)",
            "CREATE INDEX IF NOT EXISTS FOR (n:Concept) ON (n.name)",
            "CREATE INDEX IF NOT EXISTS FOR (n:Category) ON (n.name)",
            "CREATE INDEX IF NOT EXISTS FOR (n:User) ON (n.id)",
            "CREATE FULLTEXT INDEX knowledge_text IF NOT EXISTS FOR (n:Knowledge) ON EACH [n.content]",
        ]
        
        async with self.driver.session() as session:
            for index in indexes:
                try:
                    await session.run(index)
                except Exception as e:
                    logger.warning(f"Index creation warning: {e}")
    
    async def create_knowledge_node(
        self,
        key: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> Node:
        """Create a knowledge node."""
        query = """
        CREATE (k:Knowledge {
            key: $key,
            content: $content,
            metadata: $metadata,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN k
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                key=key,
                content=content,
                metadata=json.dumps(metadata)
            )
            
            record = await result.single()
            node_data = record["k"]
            
            return Node(
                id=node_data.element_id,
                labels=list(node_data.labels),
                properties=dict(node_data)
            )
    
    async def create_concept_node(self, name: str, description: str = "") -> Node:
        """Create a concept node."""
        query = """
        MERGE (c:Concept {name: $name})
        ON CREATE SET c.description = $description, c.created_at = datetime()
        ON MATCH SET c.accessed_at = datetime()
        RETURN c
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                name=name,
                description=description
            )
            
            record = await result.single()
            node_data = record["c"]
            
            return Node(
                id=node_data.element_id,
                labels=list(node_data.labels),
                properties=dict(node_data)
            )
    
    async def link_knowledge_to_concept(
        self,
        knowledge_key: str,
        concept_name: str,
        relationship_type: str = "RELATES_TO",
        properties: Dict[str, Any] = None
    ) -> Relationship:
        """Create relationship between knowledge and concept."""
        query = """
        MATCH (k:Knowledge {key: $knowledge_key})
        MATCH (c:Concept {name: $concept_name})
        CREATE (k)-[r:""" + relationship_type + """ $properties]->(c)
        RETURN r, id(r) as rel_id
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                knowledge_key=knowledge_key,
                concept_name=concept_name,
                properties=properties or {}
            )
            
            record = await result.single()
            rel_data = record["r"]
            
            return Relationship(
                id=record["rel_id"],
                type=relationship_type,
                start_node=knowledge_key,
                end_node=concept_name,
                properties=dict(rel_data)
            )
    
    async def find_related_knowledge(
        self,
        knowledge_key: str,
        max_depth: int = 2,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find knowledge related through shared concepts."""
        query = """
        MATCH (k1:Knowledge {key: $key})-[:RELATES_TO]->(:Concept)<-[:RELATES_TO]-(k2:Knowledge)
        WHERE k1 <> k2
        WITH k2, count(*) as shared_concepts
        ORDER BY shared_concepts DESC
        LIMIT $limit
        RETURN k2.key as key, k2.content as content, shared_concepts
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                key=knowledge_key,
                limit=limit
            )
            
            related = []
            async for record in result:
                related.append({
                    "key": record["key"],
                    "content": record["content"],
                    "shared_concepts": record["shared_concepts"]
                })
            
            return related
    
    async def find_concept_path(
        self,
        start_concept: str,
        end_concept: str,
        max_length: int = 5
    ) -> Optional[List[str]]:
        """Find shortest path between two concepts."""
        query = """
        MATCH path = shortestPath(
            (c1:Concept {name: $start})-[*..""" + str(max_length) + """]-
            (c2:Concept {name: $end})
        )
        RETURN [n in nodes(path) | n.name] as path
        """
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                start=start_concept,
                end=end_concept
            )
            
            record = await result.single()
            if record:
                return record["path"]
            return None
    
    async def get_knowledge_context(
        self,
        knowledge_key: str
    ) -> Dict[str, Any]:
        """Get full context of a knowledge item including relationships."""
        query = """
        MATCH (k:Knowledge {key: $key})
        OPTIONAL MATCH (k)-[r]->(c:Concept)
        OPTIONAL MATCH (k)<-[r2]-(other)
        RETURN k,
               collect(DISTINCT {concept: c.name, relationship: type(r)}) as concepts,
               collect(DISTINCT {node: labels(other)[0], relationship: type(r2)}) as incoming
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, key=knowledge_key)
            record = await result.single()
            
            if not record:
                return None
            
            return {
                "knowledge": dict(record["k"]),
                "concepts": [c for c in record["concepts"] if c["concept"]],
                "incoming_relationships": [r for r in record["incoming"] if r["node"]]
            }
    
    async def search_by_concept_similarity(
        self,
        concepts: List[str],
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search knowledge by concept similarity."""
        query = """
        UNWIND $concepts as concept
        MATCH (c:Concept {name: concept})<-[:RELATES_TO]-(k:Knowledge)
        WITH k, count(DISTINCT c) as matching_concepts, collect(c.name) as matched
        WHERE matching_concepts >= $min_matches
        RETURN k.key as key, k.content as content, 
               matching_concepts, matched
        ORDER BY matching_concepts DESC
        LIMIT $limit
        """
        
        min_matches = max(1, len(concepts) // 2)  # At least half the concepts
        
        async with self.driver.session() as session:
            result = await session.run(
                query,
                concepts=concepts,
                min_matches=min_matches,
                limit=limit
            )
            
            results = []
            async for record in result:
                results.append({
                    "key": record["key"],
                    "content": record["content"],
                    "matching_concepts": record["matching_concepts"],
                    "matched_concepts": record["matched"]
                })
            
            return results
    
    async def create_category_hierarchy(
        self,
        parent_category: str,
        child_category: str
    ) -> None:
        """Create hierarchical relationship between categories."""
        query = """
        MERGE (p:Category {name: $parent})
        MERGE (c:Category {name: $child})
        MERGE (p)-[:HAS_SUBCATEGORY]->(c)
        """
        
        async with self.driver.session() as session:
            await session.run(
                query,
                parent=parent_category,
                child=child_category
            )
    
    async def get_category_tree(self, root_category: str) -> Dict[str, Any]:
        """Get category hierarchy tree."""
        query = """
        MATCH path = (root:Category {name: $root})-[:HAS_SUBCATEGORY*0..]->(cat)
        WITH cat, length(path) as depth
        ORDER BY depth
        RETURN collect({
            name: cat.name,
            depth: depth
        }) as tree
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, root=root_category)
            record = await result.single()
            
            if record:
                return self._build_tree_structure(record["tree"])
            return {"name": root_category, "children": []}
    
    def _build_tree_structure(self, flat_tree: List[Dict]) -> Dict[str, Any]:
        """Convert flat tree to nested structure."""
        if not flat_tree:
            return {}
        
        tree = {"name": flat_tree[0]["name"], "children": []}
        
        # Group by depth
        by_depth = {}
        for node in flat_tree:
            depth = node["depth"]
            if depth not in by_depth:
                by_depth[depth] = []
            by_depth[depth].append(node["name"])
        
        # Build nested structure (simplified)
        return tree
    
    async def analyze_knowledge_clusters(self) -> List[Dict[str, Any]]:
        """Analyze knowledge clusters based on concept connections."""
        query = """
        MATCH (k:Knowledge)-[:RELATES_TO]->(c:Concept)
        WITH c, collect(k) as knowledge_items
        WHERE size(knowledge_items) >= 2
        RETURN c.name as concept,
               size(knowledge_items) as item_count,
               [k in knowledge_items | k.key][0..5] as sample_keys
        ORDER BY item_count DESC
        LIMIT 20
        """
        
        async with self.driver.session() as session:
            result = await session.run(query)
            
            clusters = []
            async for record in result:
                clusters.append({
                    "concept": record["concept"],
                    "item_count": record["item_count"],
                    "sample_keys": record["sample_keys"]
                })
            
            return clusters
    
    async def suggest_relationships(
        self,
        knowledge_key: str
    ) -> List[Dict[str, Any]]:
        """Suggest potential relationships for a knowledge item."""
        # Get content of the knowledge
        query = """
        MATCH (k:Knowledge {key: $key})
        RETURN k.content as content
        """
        
        async with self.driver.session() as session:
            result = await session.run(query, key=knowledge_key)
            record = await result.single()
            
            if not record:
                return []
            
            # Find similar knowledge items (simplified - in production would use NLP)
            similarity_query = """
            MATCH (other:Knowledge)
            WHERE other.key <> $key
            WITH other, 
                 size(filter(word in split(toLower(other.content), ' ') 
                       WHERE word in split(toLower($content), ' '))) as common_words
            WHERE common_words > 3
            RETURN other.key as suggested_key,
                   other.content as content,
                   common_words
            ORDER BY common_words DESC
            LIMIT 5
            """
            
            suggestions_result = await session.run(
                similarity_query,
                key=knowledge_key,
                content=record["content"]
            )
            
            suggestions = []
            async for sug_record in suggestions_result:
                suggestions.append({
                    "suggested_key": sug_record["suggested_key"],
                    "content": sug_record["content"],
                    "common_words": sug_record["common_words"],
                    "relationship_type": "SIMILAR_TO"
                })
            
            return suggestions
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Neo4j knowledge graph statistics."""
        if not self.driver:
            return {"status": "disconnected", "nodes": 0, "relationships": 0, "total_nodes": 0, "total_relationships": 0}
        
        try:
            async with self.driver.session() as session:
                # Count nodes
                node_result = await session.run("MATCH (n) RETURN count(n) as node_count")
                node_record = await node_result.single()
                node_count = node_record["node_count"] if node_record else 0
                
                # Count relationships
                rel_result = await session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
                rel_record = await rel_result.single()
                rel_count = rel_record["rel_count"] if rel_record else 0
                
                # Get node types
                type_result = await session.run("""
                    MATCH (n) 
                    RETURN labels(n) as labels, count(*) as count 
                    ORDER BY count DESC 
                    LIMIT 5
                """)
                
                node_types = []
                async for record in type_result:
                    labels = record["labels"]
                    count = record["count"]
                    if labels:
                        node_types.append({"type": labels[0], "count": count})
                
                return {
                    "status": "connected",
                    "nodes": node_count,
                    "relationships": rel_count,
                    "total_nodes": node_count,
                    "total_relationships": rel_count,
                    "node_types": node_types,
                    "database": "neo4j"
                }
                
        except Exception as e:
            logger.error(f"Failed to get Neo4j stats: {e}")
            return {
                "status": "error", 
                "error": str(e),
                "nodes": 0,
                "relationships": 0,
                "total_nodes": 0,
                "total_relationships": 0
            }


class GraphEnhancedEngine:
    """Engine enhancement with knowledge graph capabilities."""
    
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
    
    async def store_with_concepts(
        self,
        key: str,
        content: str,
        metadata: Dict[str, Any],
        concepts: List[str]
    ) -> None:
        """Store knowledge and automatically create concept relationships."""
        # Create knowledge node
        knowledge_node = await self.graph.create_knowledge_node(key, content, metadata)
        
        # Create and link concepts
        for concept_name in concepts:
            concept_node = await self.graph.create_concept_node(concept_name)
            await self.graph.link_knowledge_to_concept(
                key,
                concept_name,
                "RELATES_TO",
                {"strength": 1.0}
            )
        
        logger.info(f"Stored knowledge '{key}' with {len(concepts)} concepts")
    
    async def query_with_graph_context(
        self,
        query: str,
        use_graph: bool = True
    ) -> Dict[str, Any]:
        """Query knowledge with graph context enhancement."""
        results = {
            "direct_results": [],
            "graph_enhanced": [],
            "concept_clusters": [],
            "suggested_paths": []
        }
        
        if use_graph:
            # Extract concepts from query (simplified)
            query_concepts = [word for word in query.lower().split() if len(word) > 4]
            
            # Search by concept similarity
            if query_concepts:
                concept_results = await self.graph.search_by_concept_similarity(
                    query_concepts,
                    limit=5
                )
                results["graph_enhanced"] = concept_results
            
            # Get concept clusters
            clusters = await self.graph.analyze_knowledge_clusters()
            results["concept_clusters"] = clusters[:5]
        
        return results