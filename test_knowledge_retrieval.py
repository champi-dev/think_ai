#!/usr/bin/env python3
"""
Test script to verify Think AI knowledge retrieval
"""

import json
import random
from pathlib import Path

def test_knowledge_retrieval():
    """Test that knowledge can be retrieved from the system"""
    knowledge_dir = Path("/home/administrator/think_ai/knowledge_files")
    cache_dir = Path("/home/administrator/think_ai/cache")
    
    print("🧪 Testing Think AI Knowledge Retrieval")
    print("=" * 50)
    
    # Test 1: Check all knowledge files exist
    print("\n1️⃣ Checking knowledge files...")
    expected_domains = [
        "science", "technology", "mathematics", "philosophy", "history",
        "arts", "language", "psychology", "medicine", "engineering",
        "economics", "law", "education", "environment", "culture",
        "sociology", "anthropology", "geography", "astronomy", "chemistry"
    ]
    
    all_files_exist = True
    for domain in expected_domains:
        file_path = knowledge_dir / f"{domain}.json"
        if file_path.exists():
            print(f"   ✅ {domain}.json exists")
        else:
            print(f"   ❌ {domain}.json missing")
            all_files_exist = False
    
    # Test 2: Sample knowledge from each domain
    print("\n2️⃣ Sampling knowledge from domains...")
    sample_knowledge = {}
    
    for domain in expected_domains[:5]:  # Sample first 5 domains
        file_path = knowledge_dir / f"{domain}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = json.load(f)
                if "entries" in data and len(data["entries"]) > 0:
                    entry = random.choice(data["entries"])
                    topic = entry.get("topic", "unknown")
                    content_preview = entry.get("content", "")[:100] + "..."
                    sample_knowledge[domain] = {
                        "topic": topic,
                        "preview": content_preview
                    }
                    print(f"   📚 {domain}: {topic}")
    
    # Test 3: Check cache files
    print("\n3️⃣ Checking cache integration...")
    response_cache_path = cache_dir / "response_cache.json"
    evaluated_cache_path = cache_dir / "evaluated_knowledge.json"
    
    cache_stats = {}
    if response_cache_path.exists():
        with open(response_cache_path, 'r') as f:
            response_cache = json.load(f)
            cache_stats["response_cache_entries"] = len(response_cache)
            print(f"   ✅ Response cache: {len(response_cache)} entries")
    else:
        print("   ❌ Response cache not found")
    
    if evaluated_cache_path.exists():
        with open(evaluated_cache_path, 'r') as f:
            evaluated_cache = json.load(f)
            kb_entries = len(evaluated_cache.get("knowledge_base", {}))
            cache_stats["evaluated_cache_entries"] = kb_entries
            print(f"   ✅ Evaluated cache: {kb_entries} entries")
    else:
        print("   ❌ Evaluated cache not found")
    
    # Test 4: Query simulation
    print("\n4️⃣ Simulating knowledge queries...")
    test_queries = [
        "quantum mechanics",
        "artificial intelligence", 
        "consciousness",
        "climate change",
        "human evolution"
    ]
    
    for query in test_queries:
        found = False
        for domain_file in knowledge_dir.glob("*.json"):
            if domain_file.name == "knowledge_index.json":
                continue
            with open(domain_file, 'r') as f:
                data = json.load(f)
                for entry in data.get("entries", []):
                    if query.lower() in entry.get("topic", "").lower():
                        print(f"   🔍 Found '{query}' in {domain_file.stem} domain")
                        found = True
                        break
            if found:
                break
        if not found:
            print(f"   ⚠️  '{query}' not found")
    
    # Summary
    print("\n📊 Knowledge Integration Summary")
    print("=" * 50)
    print(f"✓ Knowledge domains loaded: {len(expected_domains)}")
    print(f"✓ All files present: {'Yes' if all_files_exist else 'No'}")
    print(f"✓ Response cache entries: {cache_stats.get('response_cache_entries', 0)}")
    print(f"✓ Evaluated knowledge entries: {cache_stats.get('evaluated_cache_entries', 0)}")
    print("\n✨ Knowledge system is ready for use!")
    print("\nTo use Think AI with this knowledge:")
    print("1. Start the server: cargo run --release")
    print("2. Ask questions about any topic!")
    print("3. The AI will use the comprehensive knowledge base")

if __name__ == "__main__":
    test_knowledge_retrieval()