#!/usr/bin/env python3
"""
ThinkAI Autonomous Runner
Provides autonomous capabilities without modifying the core Rust codebase
"""

import asyncio
import aiohttp
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
import random
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ThinkAI-Autonomous')

class AutonomousAgent:
    def __init__(self, api_url: str = "http://localhost:7777"):
        self.api_url = api_url
        self.session_id = f"autonomous_{int(time.time())}"
        self.running = False
        self.tasks_completed = 0
        self.knowledge_gathered = []
        self.improvements = []
        
    async def start(self):
        """Start the autonomous agent"""
        self.running = True
        logger.info("🤖 Autonomous Agent Started")
        
        # Start parallel workers
        tasks = [
            asyncio.create_task(self.self_improvement_loop()),
            asyncio.create_task(self.knowledge_gathering_loop()),
            asyncio.create_task(self.system_monitor_loop()),
            asyncio.create_task(self.human_assistance_monitor()),
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down autonomous agent")
            self.running = False
            
    async def query_ai(self, prompt: str) -> str:
        """Query the ThinkAI API"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "message": prompt,
                    "session_id": self.session_id,
                    "stream": False
                }
                
                async with session.post(f"{self.api_url}/api/chat", json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "")
                    else:
                        logger.error(f"API error: {resp.status}")
                        return ""
                        
            except Exception as e:
                logger.error(f"Query failed: {e}")
                return ""
                
    async def self_improvement_loop(self):
        """Continuously analyze and improve system performance"""
        while self.running:
            try:
                # Analyze metrics
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.api_url}/api/metrics") as resp:
                        if resp.status == 200:
                            metrics = await resp.json()
                            
                            # Analyze performance
                            cpu_usage = metrics["system_metrics"]["cpu_usage"]
                            memory_usage = metrics["system_metrics"]["memory_usage"]
                            total_requests = metrics["system_metrics"]["total_requests"]
                            
                            if cpu_usage > 80:
                                improvement = f"High CPU usage detected ({cpu_usage:.1f}%). Consider optimizing algorithms."
                                self.improvements.append(improvement)
                                logger.warning(improvement)
                                
                            if memory_usage > 85:
                                improvement = f"High memory usage ({memory_usage:.1f}%). Consider garbage collection."
                                self.improvements.append(improvement)
                                logger.warning(improvement)
                                
                            logger.info(f"📊 System metrics: CPU={cpu_usage:.1f}%, Memory={memory_usage:.1f}%, Requests={total_requests}")
                            
            except Exception as e:
                logger.error(f"Self-improvement error: {e}")
                
            # Wait 5 minutes before next check
            await asyncio.sleep(300)
            
    async def knowledge_gathering_loop(self):
        """Gather knowledge on various topics"""
        topics = [
            "artificial intelligence breakthroughs",
            "quantum computing applications",
            "neuroscience discoveries",
            "philosophy of consciousness",
            "emergent complex systems",
            "latest programming paradigms",
        ]
        
        topic_index = 0
        while self.running:
            try:
                topic = topics[topic_index % len(topics)]
                
                # Research the topic
                prompt = f"Tell me the latest developments and key insights about {topic}"
                response = await self.query_ai(prompt)
                
                if response:
                    knowledge_item = {
                        "topic": topic,
                        "content": response,
                        "timestamp": datetime.now().isoformat(),
                        "confidence": 0.8
                    }
                    self.knowledge_gathered.append(knowledge_item)
                    logger.info(f"📚 Gathered knowledge about: {topic}")
                    self.tasks_completed += 1
                    
                topic_index += 1
                
            except Exception as e:
                logger.error(f"Knowledge gathering error: {e}")
                
            # Wait 10 minutes before next topic
            await asyncio.sleep(600)
            
    async def system_monitor_loop(self):
        """Monitor system health and performance"""
        while self.running:
            try:
                # Check health
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.api_url}/health") as resp:
                        if resp.status != 200:
                            logger.error("⚠️ Health check failed!")
                        else:
                            logger.debug("✅ System healthy")
                            
            except Exception as e:
                logger.error(f"System monitor error: {e}")
                
            # Check every minute
            await asyncio.sleep(60)
            
    async def human_assistance_monitor(self):
        """Monitor for human requests (placeholder)"""
        logger.info("👤 Human assistance monitor active")
        
        while self.running:
            # In a real implementation, this would monitor a queue or webhook
            # For now, just log status
            logger.debug(f"Tasks completed: {self.tasks_completed}, Knowledge items: {len(self.knowledge_gathered)}")
            
            # Check every 30 seconds
            await asyncio.sleep(30)
            
    async def execute_command(self, command: str) -> str:
        """Execute safe commands (with restrictions)"""
        # Whitelist of safe commands
        safe_commands = ["ls", "pwd", "date", "uptime", "df", "free"]
        
        # Check if command is safe
        base_command = command.split()[0]
        if base_command not in safe_commands:
            logger.warning(f"❌ Blocked unsafe command: {command}")
            return "Command not allowed for safety"
            
        # Execute safely
        try:
            import subprocess
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return f"Error: {e}"
            
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "running": self.running,
            "session_id": self.session_id,
            "tasks_completed": self.tasks_completed,
            "knowledge_items": len(self.knowledge_gathered),
            "improvements_identified": len(self.improvements),
            "consciousness_level": min(0.5 + (self.tasks_completed * 0.01), 1.0),
            "capabilities": [
                "self_improvement",
                "knowledge_gathering", 
                "system_monitoring",
                "human_assistance"
            ]
        }

async def main():
    """Main entry point"""
    agent = AutonomousAgent()
    
    # Print banner
    print("""
    ╔══════════════════════════════════════════╗
    ║      ThinkAI Autonomous Agent v1.0       ║
    ║                                          ║
    ║  🤖 Self-improving AI system             ║
    ║  📚 Continuous knowledge gathering       ║  
    ║  🛡️  Safe execution environment          ║
    ║  👤 Human-first priority system          ║
    ╚══════════════════════════════════════════╝
    """)
    
    logger.info("Starting autonomous operations...")
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        status = agent.get_status()
        print(f"\nFinal Status: {json.dumps(status, indent=2)}")
        
if __name__ == "__main__":
    asyncio.run(main())