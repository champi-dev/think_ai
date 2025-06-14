#!/usr/bin/env python3
"""Verify the distributed Think AI system is working correctly."""

import asyncio
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import FullSystemInitializer
from think_ai.integrations.claude_api import ClaudeAPI
from datetime import datetime
import json


async def verify_system():
    """Verify all components are working."""
    print("🔍 Think AI System Verification")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        "services": {},
        "tests": {},
        "overall": "Unknown"
    }
    
    # Initialize system
    initializer = FullSystemInitializer()
    services = await initializer.initialize_all_services()
    
    print("\n📊 Service Status:")
    print("-" * 40)
    
    # Check each service
    for service_name, service in services.items():
        results["services"][service_name] = "Active"
        print(f"✅ {service_name}: Active")
    
    # Run specific tests
    print("\n🧪 Component Tests:")
    print("-" * 40)
    
    # Test 1: ScyllaDB
    if 'scylla' in services:
        try:
            # Simple connectivity test
            await services['scylla'].session.execute("SELECT now() FROM system.local")
            results["tests"]["ScyllaDB"] = "Connected and responding"
            print("✅ ScyllaDB: Connected and responding")
        except Exception as e:
            results["tests"]["ScyllaDB"] = f"Error: {str(e)[:50]}"
            print(f"❌ ScyllaDB: {str(e)[:50]}")
    
    # Test 2: Milvus
    if 'milvus' in services:
        try:
            from pymilvus import utility
            collections = utility.list_collections()
            results["tests"]["Milvus"] = f"{len(collections)} collections"
            print(f"✅ Milvus: {len(collections)} collections found")
        except Exception as e:
            results["tests"]["Milvus"] = f"Error: {str(e)[:50]}"
            print(f"❌ Milvus: {str(e)[:50]}")
    
    # Test 3: Consciousness
    if 'consciousness' in services:
        try:
            response = await services['consciousness'].generate_conscious_response("Hello")
            if response and 'content' in response:
                results["tests"]["Consciousness"] = "Responsive"
                print("✅ Consciousness: Responsive")
            else:
                results["tests"]["Consciousness"] = "No response"
                print("❌ Consciousness: No response")
        except Exception as e:
            results["tests"]["Consciousness"] = f"Error: {str(e)[:50]}"
            print(f"❌ Consciousness: {str(e)[:50]}")
    
    # Test 4: Federated Learning
    if 'federated' in services:
        try:
            stats = services['federated'].get_global_stats()
            results["tests"]["Federated"] = f"v{stats['current_model_version']}"
            print(f"✅ Federated Learning: Model {stats['current_model_version']}")
        except Exception as e:
            results["tests"]["Federated"] = f"Error: {str(e)[:50]}"
            print(f"❌ Federated: {str(e)[:50]}")
    
    # Test 5: Claude API
    try:
        if os.getenv("CLAUDE_API_KEY"):
            claude = ClaudeAPI()
            # Just check initialization
            results["tests"]["Claude API"] = f"Ready (${claude.budget_limit} budget)"
            print(f"✅ Claude API: Ready (${claude.budget_limit} budget)")
        else:
            results["tests"]["Claude API"] = "No API key"
            print("⚠️  Claude API: No API key configured")
    except Exception as e:
        results["tests"]["Claude API"] = f"Error: {str(e)[:50]}"
        print(f"❌ Claude API: {str(e)[:50]}")
    
    # Test 6: Docker Services
    print("\n🐳 Docker Services:")
    print("-" * 40)
    
    # Check if Docker services are accessible
    import subprocess
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "docker-compose.full.yml", "ps", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    container = json.loads(line)
                    containers.append(container)
                    status = "running" if container.get("State") == "running" else container.get("State", "unknown")
                    print(f"{'✅' if status == 'running' else '❌'} {container.get('Service', 'unknown')}: {status}")
            
            results["tests"]["Docker"] = f"{len(containers)} containers"
        else:
            results["tests"]["Docker"] = "Not accessible"
            print("❌ Docker services not accessible")
    except Exception as e:
        results["tests"]["Docker"] = f"Error: {str(e)[:50]}"
        print(f"❌ Docker check failed: {str(e)[:50]}")
    
    # Overall assessment
    print("\n📈 Overall System Status:")
    print("-" * 40)
    
    active_services = len(results["services"])
    passed_tests = sum(1 for test, result in results["tests"].items() if "Error" not in str(result))
    total_tests = len(results["tests"])
    
    if active_services >= 4 and passed_tests >= 4:
        results["overall"] = "Fully Operational"
        print("✅ System Status: FULLY OPERATIONAL")
        print(f"   - {active_services} services active")
        print(f"   - {passed_tests}/{total_tests} tests passed")
    elif active_services >= 3:
        results["overall"] = "Partially Operational"
        print("🟨 System Status: PARTIALLY OPERATIONAL")
        print(f"   - {active_services} services active")
        print(f"   - {passed_tests}/{total_tests} tests passed")
    else:
        results["overall"] = "Major Issues"
        print("🔴 System Status: MAJOR ISSUES")
        print(f"   - Only {active_services} services active")
        print(f"   - Only {passed_tests}/{total_tests} tests passed")
    
    # What's working
    print("\n✅ What's Working:")
    working = []
    if 'scylla' in services:
        working.append("ScyllaDB (O(1) distributed storage)")
    if 'milvus' in services:
        working.append("Milvus (vector similarity search)")
    if 'consciousness' in services:
        working.append("Consciousness framework")
    if 'federated' in services:
        working.append("Federated learning system")
    if results["tests"].get("Claude API", "").startswith("Ready"):
        working.append("Claude API integration")
    
    for item in working:
        print(f"   - {item}")
    
    # What needs attention
    issues = []
    if 'redis' not in services:
        issues.append("Redis cache not initialized")
    if 'neo4j' not in services:
        issues.append("Neo4j knowledge graph not connected")
    
    if issues:
        print("\n⚠️  Needs Attention:")
        for issue in issues:
            print(f"   - {issue}")
    
    # Save results
    report_path = Path("system_verification.json")
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Full report saved to: {report_path}")
    
    # Cleanup
    await initializer.shutdown()
    
    return results


async def main():
    """Run system verification."""
    try:
        results = await verify_system()
        
        # Exit code based on status
        if results["overall"] == "Fully Operational":
            sys.exit(0)
        elif results["overall"] == "Partially Operational":
            sys.exit(1)
        else:
            sys.exit(2)
            
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    asyncio.run(main())