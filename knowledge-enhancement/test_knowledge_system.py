#!/usr/bin/env python3
"""
Think AI - Knowledge Enhancement System Test

Quick test to verify the knowledge enhancement system works correctly.
"""

import asyncio
import json
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

async def test_quick_harvest():
    """Test knowledge harvesting with minimal data"""
    console.print(Panel("🧪 Testing Knowledge Enhancement System", style="bold blue"))
    
    # Import the harvester
    try:
        from legal_knowledge_harvester import LegalKnowledgeHarvester
        from knowledge_integrator import ThinkAIKnowledgeIntegrator
    except ImportError as e:
        console.print(f"❌ Import failed: {e}")
        console.print("Installing missing dependencies...")
        import subprocess
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        from legal_knowledge_harvester import LegalKnowledgeHarvester
        from knowledge_integrator import ThinkAIKnowledgeIntegrator
    
    # Test harvesting
    console.print("🌐 Testing knowledge harvesting...")
    
    async with LegalKnowledgeHarvester("./test_harvest") as harvester:
        # Small test harvest
        test_topics = ["Artificial Intelligence", "Machine Learning"]
        test_subjects = ["Philosophy", "Science"]
        test_categories = ["cs.AI"]
        test_gov_topics = ["artificial intelligence"]
        
        await harvester.harvest_wikipedia_articles(test_topics, articles_per_topic=3)
        await harvester.harvest_gutenberg_books(test_subjects, books_per_subject=1)
        await harvester.harvest_arxiv_papers(test_categories, papers_per_category=2)
        await harvester.harvest_government_docs(test_gov_topics, docs_per_topic=1)
        
        harvester.save_knowledge_base()
        
        console.print(f"✅ Harvested {len(harvester.knowledge_items)} knowledge items")
    
    # Test integration
    console.print("🔄 Testing knowledge integration...")
    
    integrator = ThinkAIKnowledgeIntegrator("./test_harvest", "./test_integrated")
    
    raw_items = integrator.load_harvested_knowledge()
    integrator.process_knowledge_items(raw_items)
    integrator.build_knowledge_structures()
    integrator.generate_integration_report()
    
    # Verify outputs
    console.print("✅ Testing output validation...")
    
    test_files = [
        "./test_integrated/knowledge_database.json",
        "./test_integrated/knowledge_indexes.json",
        "./test_integrated/quick_lookup.json",
        "./test_integrated/integration_report.json"
    ]
    
    all_valid = True
    for file_path in test_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    json.load(f)
                console.print(f"  ✅ {file_path}")
            except json.JSONDecodeError:
                console.print(f"  ❌ {file_path} - Invalid JSON")
                all_valid = False
        else:
            console.print(f"  ❌ {file_path} - Missing")
            all_valid = False
    
    if all_valid:
        console.print(Panel(
            "🎉 ALL TESTS PASSED!\n"
            "Knowledge enhancement system is working correctly.\n"
            "Ready for full harvest with ./run_knowledge_enhancement.sh",
            title="Test Results",
            style="bold green"
        ))
    else:
        console.print(Panel(
            "❌ Some tests failed!\n"
            "Please check the error messages above.",
            title="Test Results", 
            style="bold red"
        ))
    
    # Show stats
    if Path("./test_integrated/integration_report.json").exists():
        with open("./test_integrated/integration_report.json", 'r') as f:
            report = json.load(f)
            
        table = Table(title="Test Harvest Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        summary = report['integration_summary']
        table.add_row("Items Processed", str(summary['total_items']))
        table.add_row("Categories", str(summary['categories']))
        table.add_row("Sources", str(summary['sources']))
        table.add_row("Avg Confidence", f"{summary['average_confidence']:.3f}")
        
        console.print(table)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(test_quick_harvest())
    elapsed = time.time() - start_time
    console.print(f"⏱️ Test completed in {elapsed:.2f} seconds")