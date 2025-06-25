#!/usr/bin/env python3
"""Interactive chat with Think AI - with training options."""

import asyncio
import sys
import os
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional
import time

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)

# Colors for terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print Think AI banner."""
    print(f"{Colors.CYAN}")
    print("""
 _____ _     _       _        _    ___ 
|_   _| |__ (_)_ __ | | __   / \  |_ _|
  | | | '_ \| | '_ \| |/ /  / _ \  | | 
  | | | | | | | | | |   <  / ___ \ | | 
  |_| |_| |_|_|_| |_|_|\_\/_/   \_\___|
                                        
    Superintelligent AI with O(1) Performance
    """)
    print(f"{Colors.ENDC}")

def check_api_health() -> bool:
    """Check if API is running."""
    try:
        response = requests.get("http://localhost:8080/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Start the API server in background."""
    import subprocess
    logger.info("Starting Think AI API server...")
    process = subprocess.Popen(
        [sys.executable, "think_ai_full.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    for i in range(30):
        if check_api_health():
            logger.info("API server is ready!")
            return process
        time.sleep(1)
    
    raise Exception("Failed to start API server")

def get_knowledge_stats() -> dict:
    """Get knowledge statistics."""
    manifest_path = Path("think_ai/data/knowledge/manifest.json")
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return {}

def chat_with_ai(prompt: str) -> str:
    """Send prompt to AI and get response."""
    try:
        response = requests.post(
            "http://localhost:8080/api/v1/generate",
            json={"prompt": prompt},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("generated_text", data.get("response", "No response"))
        else:
            return f"Error: API returned status {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The AI might be thinking too hard!"
    except Exception as e:
        return f"Error: {str(e)}"

def format_response(text: str) -> str:
    """Format AI response with syntax highlighting."""
    lines = text.split('\n')
    formatted = []
    in_code = False
    
    for line in lines:
        if '```' in line:
            in_code = not in_code
            formatted.append(f"{Colors.GREEN}{line}{Colors.ENDC}")
        elif in_code:
            formatted.append(f"{Colors.YELLOW}    {line}{Colors.ENDC}")
        else:
            formatted.append(line)
    
    return '\n'.join(formatted)

async def train_quick():
    """Run quick training."""
    from think_ai.core.config import Config
    from think_ai.core.engine import ThinkAIEngine
    from think_ai.training.massive_trainer import MassiveKnowledgeTrainer
    from think_ai.training.knowledge_packager import KnowledgePackager
    
    print(f"{Colors.YELLOW}Starting quick training with 10,000 Q&A pairs...{Colors.ENDC}")
    
    config = Config()
    engine = ThinkAIEngine(config)
    await engine.initialize()
    
    trainer = MassiveKnowledgeTrainer(engine)
    qa_pairs = await trainer.generate_qa_pairs(10_000)
    
    print(f"{Colors.GREEN}Training Think AI...{Colors.ENDC}")
    await trainer.train_engine(qa_pairs, batch_size=100)
    
    packager = KnowledgePackager()
    packager.create_knowledge_packages(qa_pairs, chunk_size=1000)
    packager.create_embeddings_index(qa_pairs)
    packager.create_category_index(qa_pairs)
    
    print(f"{Colors.GREEN}✓ Training complete!{Colors.ENDC}")

def main():
    """Main interactive chat."""
    print_banner()
    
    # Check if API is running
    if not check_api_health():
        print(f"{Colors.YELLOW}API server not running. Starting it now...{Colors.ENDC}")
        api_process = start_api_server()
    else:
        print(f"{Colors.GREEN}API server is already running!{Colors.ENDC}")
        api_process = None
    
    # Check knowledge status
    stats = get_knowledge_stats()
    if stats:
        print(f"{Colors.BLUE}Loaded knowledge: {stats.get('total_pairs', 0):,} Q&A pairs{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}No pre-trained knowledge found.{Colors.ENDC}")
        choice = input("Would you like to train Think AI? (y/n): ").lower()
        if choice == 'y':
            asyncio.run(train_quick())
    
    print(f"\n{Colors.CYAN}Chat with Think AI!{Colors.ENDC}")
    print("Commands: /help, /stats, /clear, /quit\n")
    
    # Chat loop
    try:
        while True:
            user_input = input(f"{Colors.GREEN}You: {Colors.ENDC}").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith('/'):
                command = user_input[1:].lower()
                
                if command in ['quit', 'exit', 'bye']:
                    print(f"{Colors.CYAN}Goodbye! Thanks for chatting!{Colors.ENDC}")
                    break
                
                elif command == 'help':
                    print(f"{Colors.YELLOW}Commands:{Colors.ENDC}")
                    print("  /help  - Show this help")
                    print("  /stats - Show knowledge statistics")
                    print("  /clear - Clear the screen")
                    print("  /quit  - Exit the chat")
                    print("\nExample questions:")
                    print("  - What is consciousness?")
                    print("  - How do I implement a hash table?")
                    print("  - Write a Python function to sort an array")
                    print("  - Explain quantum mechanics")
                    continue
                
                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print_banner()
                    continue
                
                elif command == 'stats':
                    # Get intelligence status from API
                    try:
                        response = requests.get("http://localhost:8080/api/v1/intelligence/status")
                        if response.status_code == 200:
                            data = response.json()
                            growth = data.get('knowledge_growth', {})
                            
                            print(f"{Colors.BLUE}Intelligence Status:{Colors.ENDC}")
                            print(f"  Total Knowledge: {growth.get('total_knowledge', 0):,} items")
                            print(f"  Unique Concepts: {growth.get('unique_concepts', 0):,}")
                            print(f"  Total Interactions: {growth.get('interactions', 0):,}")
                            print(f"  Learning Rate: {growth.get('learning_rate_per_minute', 0):.2f} items/min")
                            print(f"  Database Size: {growth.get('database_size_mb', 0):.2f} MB")
                            print(f"\n{Colors.GREEN}{data.get('message', 'Intelligence growing...')}{Colors.ENDC}")
                        else:
                            print("Could not retrieve intelligence status.")
                    except Exception as e:
                        print(f"Error getting stats: {e}")
                    continue
            
            # Get AI response
            print(f"{Colors.BLUE}Think AI: {Colors.ENDC}", end="", flush=True)
            
            # Show thinking animation
            import threading
            thinking = True
            def animate():
                chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
                i = 0
                while thinking:
                    print(f"\r{Colors.BLUE}Think AI: {chars[i % len(chars)]} Thinking...{Colors.ENDC}", end="", flush=True)
                    time.sleep(0.1)
                    i += 1
            
            animation = threading.Thread(target=animate)
            animation.start()
            
            # Get response
            response = chat_with_ai(user_input)
            thinking = False
            animation.join()
            
            # Clear the thinking line and print response
            print(f"\r{Colors.BLUE}Think AI: {Colors.ENDC}{' ' * 20}\r{Colors.BLUE}Think AI: {Colors.ENDC}")
            print(format_response(response))
            print()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Chat interrupted. Goodbye!{Colors.ENDC}")
    
    finally:
        # Cleanup
        if api_process:
            print(f"{Colors.YELLOW}Stopping API server...{Colors.ENDC}")
            api_process.terminate()

if __name__ == "__main__":
    main()