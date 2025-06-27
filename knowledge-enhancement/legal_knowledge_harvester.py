#!/usr/bin/env python3
"""
Think AI - Legal Knowledge Enhancement System

Harvests knowledge from legitimate sources:
- Wikipedia (public domain)
- Project Gutenberg (public domain books)
- arXiv (academic papers)
- Government documents (public domain)
- Creative Commons content
"""

import asyncio
import aiohttp
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from urllib.parse import urljoin, quote
import zipfile
import gzip
import logging

# Rich for beautiful CLI output
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()

@dataclass
class KnowledgeItem:
    """Represents a piece of knowledge"""
    title: str
    content: str
    source: str
    category: str
    url: str
    metadata: Dict[str, Any]

class LegalKnowledgeHarvester:
    """Legal knowledge harvester for Think AI"""
    
    def __init__(self, output_dir: str = "./knowledge_harvest"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session: Optional[aiohttp.ClientSession] = None
        self.knowledge_items: List[KnowledgeItem] = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'harvest.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'ThinkAI-Legal-Knowledge-Harvester/1.0 (Educational Purpose)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def harvest_wikipedia_articles(self, topics: List[str], articles_per_topic: int = 10):
        """Harvest Wikipedia articles on specific topics"""
        console.print(Panel("🌐 Harvesting Wikipedia Articles", style="blue"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            for topic in topics:
                task = progress.add_task(f"Fetching articles for: {topic}", total=articles_per_topic)
                
                try:
                    # Search for articles on topic
                    search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
                    articles = await self._search_wikipedia_topic(topic, articles_per_topic)
                    
                    for article_title in articles:
                        try:
                            # Get article summary
                            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(article_title)}"
                            async with self.session.get(url) as response:
                                if response.status == 200:
                                    data = await response.json()
                                    
                                    if 'extract' in data and len(data['extract']) > 100:
                                        knowledge_item = KnowledgeItem(
                                            title=data['title'],
                                            content=data['extract'],
                                            source="Wikipedia",
                                            category=topic,
                                            url=data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                                            metadata={
                                                'lang': data.get('lang', 'en'),
                                                'timestamp': data.get('timestamp', ''),
                                                'description': data.get('description', ''),
                                                'pageviews': await self._get_wikipedia_pageviews(article_title)
                                            }
                                        )
                                        self.knowledge_items.append(knowledge_item)
                                        progress.advance(task)
                                        
                                        # Rate limiting
                                        await asyncio.sleep(0.1)
                                        
                        except Exception as e:
                            self.logger.warning(f"Failed to fetch Wikipedia article {article_title}: {e}")
                            
                except Exception as e:
                    self.logger.error(f"Failed to search Wikipedia topic {topic}: {e}")
    
    async def _search_wikipedia_topic(self, topic: str, limit: int) -> List[str]:
        """Search Wikipedia for articles on a topic"""
        try:
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': topic,
                'limit': limit,
                'namespace': 0,
                'format': 'json'
            }
            
            async with self.session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[1] if len(data) > 1 else []
        except Exception as e:
            self.logger.error(f"Wikipedia search failed for {topic}: {e}")
        
        return []
    
    async def _get_wikipedia_pageviews(self, article_title: str) -> int:
        """Get pageview count for Wikipedia article"""
        try:
            # Get last month's pageviews
            url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{quote(article_title)}/monthly/20241201/20241231"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'items' in data and data['items']:
                        return sum(item.get('views', 0) for item in data['items'])
        except:
            pass
        return 0
    
    async def harvest_gutenberg_books(self, subjects: List[str], books_per_subject: int = 5):
        """Harvest public domain books from Project Gutenberg"""
        console.print(Panel("📚 Harvesting Project Gutenberg Books", style="green"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            for subject in subjects:
                task = progress.add_task(f"Fetching books on: {subject}", total=books_per_subject)
                
                try:
                    # Search Gutenberg catalog
                    books = await self._search_gutenberg_books(subject, books_per_subject)
                    
                    for book in books:
                        try:
                            # Download book text
                            text_content = await self._download_gutenberg_text(book['id'])
                            if text_content and len(text_content) > 1000:
                                
                                knowledge_item = KnowledgeItem(
                                    title=book['title'],
                                    content=text_content[:50000],  # First 50k characters
                                    source="Project Gutenberg",
                                    category=subject,
                                    url=f"https://www.gutenberg.org/ebooks/{book['id']}",
                                    metadata={
                                        'author': book.get('author', 'Unknown'),
                                        'language': book.get('language', 'en'),
                                        'gutenberg_id': book['id'],
                                        'downloads': book.get('downloads', 0),
                                        'subjects': book.get('subjects', [])
                                    }
                                )
                                self.knowledge_items.append(knowledge_item)
                                progress.advance(task)
                                
                                # Rate limiting - be respectful
                                await asyncio.sleep(1.0)
                                
                        except Exception as e:
                            self.logger.warning(f"Failed to download Gutenberg book {book.get('id')}: {e}")
                            
                except Exception as e:
                    self.logger.error(f"Failed to search Gutenberg subject {subject}: {e}")
    
    async def _search_gutenberg_books(self, subject: str, limit: int) -> List[Dict]:
        """Search Project Gutenberg for books on subject"""
        try:
            # Use Gutenberg's search API
            search_url = f"https://gutendex.com/books/?search={quote(subject)}&languages=en"
            
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    books = []
                    
                    for book in data.get('results', [])[:limit]:
                        books.append({
                            'id': book['id'],
                            'title': book['title'],
                            'author': ', '.join([author['name'] for author in book.get('authors', [])]),
                            'language': book.get('languages', ['en'])[0],
                            'downloads': book.get('download_count', 0),
                            'subjects': book.get('subjects', [])
                        })
                    
                    return books
        except Exception as e:
            self.logger.error(f"Gutenberg search failed for {subject}: {e}")
        
        return []
    
    async def _download_gutenberg_text(self, book_id: int) -> Optional[str]:
        """Download text content from Gutenberg book"""
        try:
            # Try to get plain text version
            text_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
            
            async with self.session.get(text_url) as response:
                if response.status == 200:
                    content = await response.text(encoding='utf-8')
                    # Remove Gutenberg header/footer
                    content = self._clean_gutenberg_text(content)
                    return content
                    
        except Exception as e:
            self.logger.debug(f"Failed to download Gutenberg text {book_id}: {e}")
        
        return None
    
    def _clean_gutenberg_text(self, text: str) -> str:
        """Clean Project Gutenberg text by removing headers/footers"""
        # Remove Gutenberg header
        start_markers = [
            "*** START OF THE PROJECT GUTENBERG EBOOK",
            "*** START OF THIS PROJECT GUTENBERG EBOOK",
            "***START OF THE PROJECT GUTENBERG EBOOK"
        ]
        
        end_markers = [
            "*** END OF THE PROJECT GUTENBERG EBOOK",
            "*** END OF THIS PROJECT GUTENBERG EBOOK",
            "***END OF THE PROJECT GUTENBERG EBOOK"
        ]
        
        for marker in start_markers:
            if marker in text:
                text = text.split(marker, 1)[1]
                break
        
        for marker in end_markers:
            if marker in text:
                text = text.split(marker, 1)[0]
                break
        
        return text.strip()
    
    async def harvest_arxiv_papers(self, categories: List[str], papers_per_category: int = 10):
        """Harvest academic papers from arXiv"""
        console.print(Panel("🎓 Harvesting arXiv Academic Papers", style="cyan"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            for category in categories:
                task = progress.add_task(f"Fetching papers in: {category}", total=papers_per_category)
                
                try:
                    papers = await self._search_arxiv_papers(category, papers_per_category)
                    
                    for paper in papers:
                        try:
                            knowledge_item = KnowledgeItem(
                                title=paper['title'],
                                content=paper['summary'],
                                source="arXiv",
                                category=category,
                                url=paper['url'],
                                metadata={
                                    'authors': paper.get('authors', []),
                                    'arxiv_id': paper.get('id', ''),
                                    'published': paper.get('published', ''),
                                    'categories': paper.get('categories', []),
                                    'doi': paper.get('doi', '')
                                }
                            )
                            self.knowledge_items.append(knowledge_item)
                            progress.advance(task)
                            
                            # Rate limiting
                            await asyncio.sleep(0.5)
                            
                        except Exception as e:
                            self.logger.warning(f"Failed to process arXiv paper: {e}")
                            
                except Exception as e:
                    self.logger.error(f"Failed to search arXiv category {category}: {e}")
    
    async def _search_arxiv_papers(self, category: str, limit: int) -> List[Dict]:
        """Search arXiv for papers in category"""
        try:
            # arXiv API query
            base_url = "http://export.arxiv.org/api/query"
            query = f"cat:{category}"
            params = {
                'search_query': query,
                'start': 0,
                'max_results': limit,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            async with self.session.get(base_url, params=params) as response:
                if response.status == 200:
                    xml_content = await response.text()
                    return self._parse_arxiv_xml(xml_content)
                    
        except Exception as e:
            self.logger.error(f"arXiv search failed for {category}: {e}")
        
        return []
    
    def _parse_arxiv_xml(self, xml_content: str) -> List[Dict]:
        """Parse arXiv XML response"""
        papers = []
        try:
            root = ET.fromstring(xml_content)
            
            # Define namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                paper = {}
                
                # Title
                title_elem = entry.find('atom:title', ns)
                paper['title'] = title_elem.text.strip() if title_elem is not None else ''
                
                # Summary
                summary_elem = entry.find('atom:summary', ns)
                paper['summary'] = summary_elem.text.strip() if summary_elem is not None else ''
                
                # Authors
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                paper['authors'] = authors
                
                # URL
                id_elem = entry.find('atom:id', ns)
                paper['url'] = id_elem.text if id_elem is not None else ''
                paper['id'] = paper['url'].split('/')[-1] if paper['url'] else ''
                
                # Published date
                published_elem = entry.find('atom:published', ns)
                paper['published'] = published_elem.text if published_elem is not None else ''
                
                # Categories
                categories = []
                for category in entry.findall('atom:category', ns):
                    term = category.get('term')
                    if term:
                        categories.append(term)
                paper['categories'] = categories
                
                if paper['title'] and paper['summary']:
                    papers.append(paper)
                    
        except ET.ParseError as e:
            self.logger.error(f"Failed to parse arXiv XML: {e}")
        
        return papers
    
    async def harvest_government_docs(self, topics: List[str], docs_per_topic: int = 5):
        """Harvest public government documents"""
        console.print(Panel("🏛️ Harvesting Government Documents", style="yellow"))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            for topic in topics:
                task = progress.add_task(f"Fetching docs on: {topic}", total=docs_per_topic)
                
                try:
                    # Search government documents (example: data.gov API)
                    docs = await self._search_government_docs(topic, docs_per_topic)
                    
                    for doc in docs:
                        try:
                            knowledge_item = KnowledgeItem(
                                title=doc['title'],
                                content=doc['description'],
                                source="Government Documents",
                                category=topic,
                                url=doc['url'],
                                metadata={
                                    'agency': doc.get('agency', ''),
                                    'published': doc.get('published', ''),
                                    'format': doc.get('format', ''),
                                    'license': doc.get('license', 'Public Domain')
                                }
                            )
                            self.knowledge_items.append(knowledge_item)
                            progress.advance(task)
                            
                            await asyncio.sleep(0.5)
                            
                        except Exception as e:
                            self.logger.warning(f"Failed to process government doc: {e}")
                            
                except Exception as e:
                    self.logger.error(f"Failed to search government docs for {topic}: {e}")
    
    async def _search_government_docs(self, topic: str, limit: int) -> List[Dict]:
        """Search government documents"""
        docs = []
        try:
            # data.gov API search
            base_url = "https://catalog.data.gov/api/3/action/package_search"
            params = {
                'q': topic,
                'rows': limit,
                'sort': 'score desc'
            }
            
            async with self.session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for result in data.get('result', {}).get('results', []):
                        docs.append({
                            'title': result.get('title', ''),
                            'description': result.get('notes', ''),
                            'url': f"https://catalog.data.gov/dataset/{result.get('name', '')}",
                            'agency': result.get('organization', {}).get('title', ''),
                            'published': result.get('metadata_created', ''),
                            'format': 'Dataset',
                            'license': result.get('license_title', 'Public Domain')
                        })
                        
        except Exception as e:
            self.logger.error(f"Government docs search failed: {e}")
        
        return docs
    
    def save_knowledge_base(self):
        """Save harvested knowledge to files"""
        console.print(Panel("💾 Saving Knowledge Base", style="magenta"))
        
        # Save as JSON
        json_file = self.output_dir / "knowledge_base.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump([
                {
                    'title': item.title,
                    'content': item.content,
                    'source': item.source,
                    'category': item.category,
                    'url': item.url,
                    'metadata': item.metadata
                }
                for item in self.knowledge_items
            ], f, indent=2, ensure_ascii=False)
        
        # Save by category
        categories = {}
        for item in self.knowledge_items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        for category, items in categories.items():
            category_file = self.output_dir / f"{category.replace(' ', '_').lower()}.json"
            with open(category_file, 'w', encoding='utf-8') as f:
                json.dump([
                    {
                        'title': item.title,
                        'content': item.content,
                        'source': item.source,
                        'url': item.url,
                        'metadata': item.metadata
                    }
                    for item in items
                ], f, indent=2, ensure_ascii=False)
        
        # Generate summary
        self._generate_summary()
        
        console.print(f"✅ Knowledge base saved to: {self.output_dir}")
        console.print(f"📊 Total items harvested: {len(self.knowledge_items)}")
    
    def _generate_summary(self):
        """Generate harvest summary"""
        summary = {
            'total_items': len(self.knowledge_items),
            'by_source': {},
            'by_category': {},
            'harvest_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'sources_used': list(set(item.source for item in self.knowledge_items))
        }
        
        for item in self.knowledge_items:
            # By source
            if item.source not in summary['by_source']:
                summary['by_source'][item.source] = 0
            summary['by_source'][item.source] += 1
            
            # By category
            if item.category not in summary['by_category']:
                summary['by_category'][item.category] = 0
            summary['by_category'][item.category] += 1
        
        summary_file = self.output_dir / "harvest_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        # Display summary table
        table = Table(title="Knowledge Harvest Summary")
        table.add_column("Source", style="cyan")
        table.add_column("Items", justify="right", style="green")
        
        for source, count in summary['by_source'].items():
            table.add_row(source, str(count))
        
        console.print(table)


async def main():
    """Main harvesting function"""
    console.print(Panel(
        "🧠 Think AI - Legal Knowledge Enhancement System\n"
        "Harvesting knowledge from legitimate sources...",
        title="Think AI Knowledge Harvester",
        style="bold blue"
    ))
    
    # Define knowledge areas to harvest
    wikipedia_topics = [
        "Artificial Intelligence", "Machine Learning", "Quantum Computing",
        "Philosophy", "Consciousness", "Mathematics", "Physics", "Biology",
        "Computer Science", "History", "Literature", "Psychology",
        "Neuroscience", "Economics", "Political Science", "Astronomy"
    ]
    
    gutenberg_subjects = [
        "Philosophy", "Science", "Literature", "History", "Mathematics",
        "Psychology", "Political Science", "Economics", "Technology"
    ]
    
    arxiv_categories = [
        "cs.AI", "cs.LG", "cs.CL", "cs.CV", "math.LO", "physics.hist-ph",
        "q-bio.NC", "econ.TH", "cs.CY", "cs.HC"
    ]
    
    government_topics = [
        "artificial intelligence", "technology policy", "education",
        "scientific research", "public health", "economics", "statistics"
    ]
    
    async with LegalKnowledgeHarvester() as harvester:
        try:
            # Harvest from all sources
            await harvester.harvest_wikipedia_articles(wikipedia_topics, articles_per_topic=15)
            await harvester.harvest_gutenberg_books(gutenberg_subjects, books_per_subject=3)
            await harvester.harvest_arxiv_papers(arxiv_categories, papers_per_category=8)
            await harvester.harvest_government_docs(government_topics, docs_per_topic=5)
            
            # Save everything
            harvester.save_knowledge_base()
            
            console.print(Panel(
                "✅ Knowledge harvesting completed successfully!\n"
                f"📁 Output directory: {harvester.output_dir}\n"
                f"📊 Total knowledge items: {len(harvester.knowledge_items)}",
                title="Harvest Complete",
                style="bold green"
            ))
            
        except Exception as e:
            console.print(Panel(
                f"❌ Harvesting failed: {str(e)}",
                title="Error",
                style="bold red"
            ))
            raise

if __name__ == "__main__":
    asyncio.run(main())