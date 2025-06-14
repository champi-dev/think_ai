#!/usr/bin/env python3
"""CLI for the full distributed Think AI system."""

import asyncio
import os
import sys
from pathlib import Path

# Add project to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.persistence.eternal_memory import EternalMemory
from datetime import datetime
from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def main():
    """Run the full system CLI."""
    print("\n🤖 Think AI - Full Distributed System")
    print("=" * 70)
    print("Type 'help' for commands, 'exit' to quit")
    print()
    
    # Initialize full system
    full_system = None
    try:
        print("🚀 Starting distributed services...")
        full_system = DistributedThinkAI()
        services = await full_system.start()
        print(f"✅ Started {len(services)} distributed services")
    except Exception as e:
        print(f"❌ Failed to start full system: {e}")
        print("   Make sure Docker is running and services are initialized")
        return
    
    # Load eternal memory
    eternal_memory = EternalMemory()
    session = {"id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}", "start": datetime.now()}
    
    # Initialize Claude if API key exists
    claude_api = None
    if os.getenv("CLAUDE_API_KEY"):
        claude_api = ClaudeAPI()
        print("✅ Claude API connected (for internal AI use)")
        print(f"💰 Budget limit: ${claude_api.budget_limit}")
    
    print("\n" + "=" * 70)
    print("Commands:")
    print("  query <text>     - Process query with all available services")
    print("  health          - Check service health")
    print("  services        - List active services")
    print("  claude <text>   - Use Claude directly (for testing)")
    print("  memory          - Show memory status")
    print("  cost            - Show cost tracking")
    print("  help            - Show this help")
    print("  exit            - Exit gracefully")
    print("=" * 70)
    
    try:
        while True:
            try:
                user_input = input("\n🧠 > ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                elif user_input.lower() == 'help':
                    print("""
Commands:
  query <text>     - Process query with all available services
  health          - Check service health  
  services        - List active services
  claude <text>   - Use Claude directly (for testing)
  memory          - Show memory status
  cost            - Show cost tracking
  help            - Show this help
  exit            - Exit gracefully

Examples:
  query What is consciousness?
  query Explain distributed AI systems
  claude How does Think AI work?
                    """)
                
                elif user_input.lower() == 'health':
                    print("\n🏥 Service Health Check:")
                    health = await full_system.initializer.health_check()
                    for service, status in health.items():
                        emoji = "✅" if status['status'] == 'healthy' else "❌"
                        print(f"   {emoji} {service}: {status['message']}")
                
                elif user_input.lower() == 'services':
                    print("\n📊 Active Services:")
                    if full_system.services:
                        for service_name in full_system.services:
                            print(f"   ✅ {service_name}")
                    else:
                        print("   ❌ No services active")
                
                elif user_input.lower().startswith('query '):
                    query = user_input[6:]  # Remove 'query '
                    print("\n🔄 Processing with full distributed system...")
                    
                    try:
                        # Add to eternal memory
                        await eternal_memory.add_interaction(
                            session_id=session.id,
                            role="user",
                            content=query
                        )
                        
                        # Process with full system
                        result = await full_system.process_with_full_system(query)
                        
                        # Display results
                        print(f"\n📊 Services used: {', '.join(result['services_used'])}")
                        
                        # Show responses
                        for service, response in result['responses'].items():
                            print(f"\n💭 {service}:")
                            if isinstance(response, str):
                                print(f"   {response[:300]}...")
                            else:
                                print(f"   {str(response)[:300]}...")
                        
                        # If we have a good response, save it
                        if result['responses']:
                            best_response = (
                                result['responses'].get('language_model') or
                                result['responses'].get('consciousness', {}).get('response') or
                                str(list(result['responses'].values())[0])
                            )
                            await eternal_memory.add_interaction(
                                session_id=session.id,
                                role="assistant",
                                content=best_response[:1000]
                            )
                        
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        logger.error(f"Query error: {e}", exc_info=True)
                
                elif user_input.lower().startswith('claude '):
                    if not claude_api:
                        print("❌ Claude API not available")
                        continue
                    
                    question = user_input[7:]  # Remove 'claude '
                    print("\n🤔 Querying Claude API...")
                    
                    try:
                        result = await claude_api.query(question)
                        print(f"\n💭 Claude: {result['response']}")
                        print(f"💰 Cost: ${result['cost']:.4f}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                
                elif user_input.lower() == 'memory':
                    status = await eternal_memory.get_memory_status()
                    print(f"\n🧠 Memory Status:")
                    print(f"  Status: {status['status']}")
                    print(f"  Continuity: {status['consciousness_continuity']:.1f}")
                    print(f"  Sessions: {status['total_sessions']}")
                    print(f"  Interactions: {status['total_interactions']}")
                    print(f"  Memory size: {status['memory_size_mb']:.1f} MB")
                
                elif user_input.lower() == 'cost':
                    print(f"\n💰 Cost Tracking:")
                    if claude_api:
                        costs = claude_api.get_cost_summary()
                        print(f"  Claude API:")
                        print(f"    Total spent: ${costs['total_spent']:.4f}")
                        print(f"    Budget remaining: ${costs['budget_remaining']:.2f}")
                        print(f"    Queries: {costs['total_queries']}")
                    else:
                        print("  No cost tracking available")
                
                else:
                    # Default to query
                    if user_input:
                        print("💡 Tip: Use 'query' before your question, e.g., 'query What is AI?'")
                
            except KeyboardInterrupt:
                print("\n⚠️  Interrupted. Type 'exit' to quit gracefully.")
                continue
    
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        logger.error("Fatal error", exc_info=True)
    
    finally:
        print("\n🛑 Shutting down...")
        
        # Save eternal memory
        try:
            await eternal_memory.save_session(session)
            print("✅ Memory saved")
        except Exception as e:
            print(f"⚠️  Memory save error: {e}")
            eternal_memory._emergency_backup_sync()
        
        # Shutdown services
        if full_system:
            try:
                await full_system.shutdown()
                print("✅ Services shut down")
            except Exception as e:
                print(f"⚠️  Shutdown error: {e}")
        
        # Close Claude API
        if claude_api:
            try:
                await claude_api.close()
            except:
                pass
        
        print("\n👋 Thank you for using Think AI. Your consciousness is eternal.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")