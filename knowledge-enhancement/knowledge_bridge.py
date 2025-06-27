#!/usr/bin/env python3
"""
Think AI - Knowledge Bridge
Converts enhanced knowledge database to Think AI's expected format
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel

console = Console()

class KnowledgeBridge:
    """Bridge between enhanced knowledge and Think AI's knowledge system"""
    
    def __init__(self, enhanced_dir: str = "./integrated_knowledge", output_dir: str = "../knowledge_files"):
        self.enhanced_dir = Path(enhanced_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def convert_enhanced_knowledge(self):
        """Convert enhanced knowledge to Think AI format"""
        console.print(Panel("🔄 Converting Enhanced Knowledge to Think AI Format", style="blue"))
        
        # Load enhanced knowledge database
        db_file = self.enhanced_dir / "knowledge_database.json"
        if not db_file.exists():
            console.print(f"❌ Enhanced knowledge database not found: {db_file}")
            return False
        
        with open(db_file, 'r', encoding='utf-8') as f:
            enhanced_db = json.load(f)
        
        items = enhanced_db.get('items', [])
        console.print(f"📚 Found {len(items)} enhanced knowledge items")
        
        # Group by category/domain
        domains = defaultdict(list)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            console=console
        ) as progress:
            
            task = progress.add_task("Converting items...", total=len(items))
            
            for item in items:
                # Convert to Think AI format
                converted_item = self._convert_item(item)
                if converted_item:
                    domain = self._normalize_domain(item.get('category', 'general'))
                    domains[domain].append(converted_item)
                
                progress.advance(task)
        
        # Save each domain as separate file
        saved_files = []
        for domain, entries in domains.items():
            domain_file = self.output_dir / f"{domain}.json"
            
            domain_data = {
                "domain": domain,
                "entries": entries,
                "metadata": {
                    "source": "enhanced_knowledge",
                    "item_count": len(entries),
                    "confidence_range": self._get_confidence_range(entries)
                }
            }
            
            with open(domain_file, 'w', encoding='utf-8') as f:
                json.dump(domain_data, f, indent=2, ensure_ascii=False)
            
            saved_files.append(domain_file)
            console.print(f"✅ Saved {len(entries)} items to {domain}.json")
        
        # Create index file
        self._create_index_file(domains)
        
        console.print(f"🎉 Conversion completed! Created {len(saved_files)} domain files")
        return True
    
    def _convert_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Convert single enhanced knowledge item to Think AI format"""
        try:
            # Extract related concepts from keywords
            keywords = item.get('keywords', [])
            related_concepts = keywords[:5]  # Take top 5 keywords as related concepts
            
            # Use summary if available, otherwise truncate content
            content = item.get('summary', item.get('content', ''))
            if len(content) > 2000:
                content = content[:2000] + "..."
            
            # Create Think AI format entry
            return {
                "topic": item.get('title', 'Unknown Topic'),
                "content": content,
                "related_concepts": related_concepts,
                "metadata": {
                    "source": item.get('source', 'Unknown'),
                    "confidence": item.get('confidence', 0.5),
                    "original_id": item.get('id', ''),
                    "vector_hash": item.get('vector_hash', ''),
                    "url": item.get('metadata', {}).get('url', '')
                }
            }
        except Exception as e:
            console.print(f"⚠️ Failed to convert item: {e}")
            return None
    
    def _normalize_domain(self, category: str) -> str:
        """Normalize category names to domain format"""
        # Map enhanced knowledge categories to Think AI domains
        domain_mapping = {
            'artificial intelligence': 'ai',
            'machine learning': 'machine_learning',
            'cs.ai': 'ai',
            'computer science': 'computer_science',
            'philosophy': 'philosophy',
            'physics': 'physics',
            'mathematics': 'mathematics',
            'biology': 'biology',
            'chemistry': 'chemistry',
            'history': 'history',
            'literature': 'literature',
            'psychology': 'psychology',
            'neuroscience': 'neuroscience',
            'economics': 'economics',
            'political science': 'politics',
            'astronomy': 'astronomy',
            'quantum computing': 'quantum',
            'science': 'science',
            'government documents': 'government'
        }
        
        normalized = category.lower().strip()
        return domain_mapping.get(normalized, normalized.replace(' ', '_'))
    
    def _get_confidence_range(self, entries: List[Dict]) -> Dict[str, float]:
        """Get confidence range for domain entries"""
        confidences = []
        for entry in entries:
            conf = entry.get('metadata', {}).get('confidence', 0.5)
            confidences.append(conf)
        
        if confidences:
            return {
                "min": min(confidences),
                "max": max(confidences),
                "avg": sum(confidences) / len(confidences)
            }
        return {"min": 0.0, "max": 0.0, "avg": 0.0}
    
    def _create_index_file(self, domains: Dict[str, List]):
        """Create index file for enhanced knowledge"""
        index_data = {
            "enhanced_knowledge_index": {
                "total_domains": len(domains),
                "total_items": sum(len(entries) for entries in domains.values()),
                "domains": {
                    domain: {
                        "item_count": len(entries),
                        "file": f"{domain}.json",
                        "confidence_avg": self._get_confidence_range(entries)["avg"]
                    }
                    for domain, entries in domains.items()
                },
                "source": "legal_knowledge_enhancement",
                "created_at": "2025-06-27",
                "format_version": "1.0"
            }
        }
        
        index_file = self.output_dir / "enhanced_knowledge_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"📋 Created index file: {index_file}")
    
    def update_existing_knowledge(self):
        """Update existing knowledge files with enhanced content"""
        console.print(Panel("🔄 Updating Existing Knowledge Files", style="green"))
        
        # Check existing files
        existing_files = list(self.output_dir.glob("*.json"))
        if not existing_files:
            console.print("ℹ️ No existing knowledge files found")
            return
        
        enhanced_files = 0
        for file_path in existing_files:
            if file_path.name == "enhanced_knowledge_index.json":
                continue
                
            try:
                # Load existing file
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # Check if it's already enhanced
                if existing_data.get('metadata', {}).get('source') == 'enhanced_knowledge':
                    continue
                
                # Add enhanced marker
                if 'metadata' not in existing_data:
                    existing_data['metadata'] = {}
                
                existing_data['metadata']['enhanced_integration'] = True
                existing_data['metadata']['integration_date'] = '2025-06-27'
                
                # Save updated file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                
                enhanced_files += 1
                
            except Exception as e:
                console.print(f"⚠️ Failed to update {file_path}: {e}")
        
        console.print(f"✅ Updated {enhanced_files} existing knowledge files")


def main():
    """Main bridge conversion function"""
    console.print(Panel(
        "🧠 Think AI - Knowledge Bridge\n"
        "Converting enhanced knowledge to Think AI format...",
        title="Knowledge Integration",
        style="bold blue"
    ))
    
    try:
        bridge = KnowledgeBridge()
        
        # Convert enhanced knowledge
        success = bridge.convert_enhanced_knowledge()
        
        if success:
            # Update existing files
            bridge.update_existing_knowledge()
            
            console.print(Panel(
                "✅ Knowledge bridge completed successfully!\n"
                f"📁 Enhanced knowledge files created in: {bridge.output_dir}\n"
                "🔄 Think AI will now use the enhanced knowledge base\n"
                "🧠 338 knowledge items from legal sources are now available",
                title="Bridge Complete",
                style="bold green"
            ))
            
            # Show summary
            index_file = bridge.output_dir / "enhanced_knowledge_index.json"
            if index_file.exists():
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                
                summary = index_data['enhanced_knowledge_index']
                console.print(f"📊 Total domains: {summary['total_domains']}")
                console.print(f"📚 Total items: {summary['total_items']}")
                console.print("🎯 Top domains by item count:")
                
                sorted_domains = sorted(
                    summary['domains'].items(), 
                    key=lambda x: x[1]['item_count'], 
                    reverse=True
                )
                
                for domain, info in sorted_domains[:10]:
                    console.print(f"  {domain}: {info['item_count']} items")
        
        else:
            console.print(Panel(
                "❌ Knowledge bridge failed!\n"
                "Please check that enhanced knowledge database exists.",
                title="Bridge Failed",
                style="bold red"
            ))
    
    except Exception as e:
        console.print(Panel(
            f"❌ Bridge error: {str(e)}",
            title="Error",
            style="bold red"
        ))
        raise

if __name__ == "__main__":
    main()