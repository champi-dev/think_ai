#! / usr / bin / env python3

"""Shared knowledge system for Think AI - all instances learn together!"""

import asyncio
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import aiohttp

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class SharedKnowledge:


"""Manages shared knowledge across all Think AI instances."""

    def __init__(self):
        self.knowledge_file = Path("shared_knowledge.json")
        self.github_repo = "champi-dev/think_ai"
        self.knowledge = self._load_local_knowledge()
        self.auto_sync_task = None
        self.sync_interval = 300  # 5 minutes

        def _load_local_knowledge(self) - > Dict[str, Any]:
"""Load knowledge from local file."""
            if self.knowledge_file.exists():
                with open(self.knowledge_file, 'r') as f:
                    return json.load(f)
            else:
# Initialize new knowledge structure
                return {
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat(),
            "total_interactions": 0,
            "learned_facts": {},
            "successful_responses": {},
            "question_patterns": {},
            "improvements": [],
            "intelligence_level": 1000
            }

            async def download_latest_knowledge(self):
"""Download latest shared knowledge from GitHub."""
                url = f"https://raw.githubusercontent.com/{
                self.github_repo}/main/shared_knowledge.json"

                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status = = 200:
                                remote_knowledge = await response.json()

# Merge with local knowledge
                                self._merge_knowledge(remote_knowledge)
                                logger.info(
                                f"Downloaded shared knowledge: {
                                remote_knowledge.get(
                                'total_interactions',
                                0)} interactions")
                                return True
                        else:
                            logger.warning(
                            "No shared knowledge file found on GitHub")
                            return False
                        except Exception as e:
                            logger.error(
                            f"Failed to download shared knowledge: {e}")
                            return False

                        def _merge_knowledge(self, remote: Dict[str, Any]):
"""Merge remote knowledge with local."""
# Take the higher intelligence level
                            if remote.get(
                            'intelligence_level',
                            0) > self.knowledge.get(
                            'intelligence_level',
                            0):
                                self.knowledge['intelligence_level'] = remote['intelligence_level']

# Merge learned facts
                                self.knowledge['learned_facts'].update(
                                remote.get('learned_facts', {}))

# Merge successful responses
                                self.knowledge['successful_responses'].update(
                                remote.get('successful_responses', {}))

# Update total interactions
                                self.knowledge['total_interactions'] = max(
                                self.knowledge['total_interactions'],
                                remote.get('total_interactions', 0)
                                )

                                self._save_local_knowledge()

                                def add_learned_fact(
                                self, topic: str, fact: str, confidence: float = 0.9):
"""Add a new learned fact."""
                                    self.knowledge['learned_facts'][topic] = {
                                    "fact": fact,
                                    "confidence": confidence,
                                    "learned_at": datetime.now().isoformat(),
                                    "times_used": 1
                                    }
                                    self._save_local_knowledge()

                                    def add_successful_response(
                                    self, query: str, response: str, score: float = 0.8):
"""Store a successful query-response pair."""
# Only store high - quality responses
                                        if score > = 0.8 and len(response) > 20:
# Normalize and limit length
                                            key = query.lower().strip()[:100]
                                            self.knowledge['successful_responses'][key] = {
                                            "response": response,
                                            "score": score,
                                            "timestamp": datetime.now().isoformat(),
                                            "used_count": 1
                                            }
                                            self.knowledge['total_interactions'] + = 1
                                            self._save_local_knowledge()

                                            def get_learned_response(self, query: str) - > str:
"""Check if we have a learned response for this query."""
                                                key = query.lower().strip()[
                                                :100]
                                                if key in self.knowledge['successful_responses']:
                                                    entry = self.knowledge['successful_responses'][key]
                                                    entry['used_count'] + = 1
                                                    self._save_local_knowledge()
                                                    return entry['response']
                                                return None

                                            def get_facts_about(self, topic: str) - > List[str]:
"""Get all learned facts about a topic."""
                                                facts = []
                                                for key, data in self.knowledge['learned_facts'].items():
                                                    if topic.lower() in key.lower():
                                                        facts.append(data['fact'])
                                                        return facts

                                                    def _save_local_knowledge(self):
"""Save knowledge to local file."""
                                                        self.knowledge['last_updated'] = datetime.now().isoformat()
                                                        with open(self.knowledge_file, 'w') as f:
                                                            json.dump(self.knowledge, f, indent = 2)

                                                            def get_intelligence_level(self) - > int:
"""Get current collective intelligence level."""
                                                                return self.knowledge.get('intelligence_level', 1000)

                                                            def increase_intelligence(self, amount: int = 100):
"""Increase collective intelligence."""
                                                                self.knowledge['intelligence_level'] + = amount
                                                                self._save_local_knowledge()

                                                                async def sync_to_cloud(self):
"""Sync local knowledge to cloud using git."""
                                                                    try:

# Check if we're in a git repo'
                                                                        result = subprocess.run(['git', 'status'], capture_output = True, text = True)
                                                                        if result.returncode ! = 0:
                                                                            logger.warning("Not in a git repository - skipping sync")
                                                                            return False

# Check if shared_knowledge.json has changes
                                                                        result = subprocess.run(['git', 'status', '--porcelain', 'shared_knowledge.json'],
                                                                        capture_output = True, text = True)

                                                                        if not result.stdout.strip():
                                                                            logger.debug("No changes to sync")
                                                                            return True

# Add the file
                                                                        subprocess.run(['git', 'add', 'shared_knowledge.json'], check = True)

# Create commit message
                                                                        stats = self.get_stats()
                                                                        commit_msg = f"🧠 Update shared knowledge: {stats['total_interactions']} interactions, {stats['intelligence_level']} IQ"

# Commit
                                                                        subprocess.run(['git', 'commit', '-m', commit_msg], check = True)

# Try to push (will fail if no push access, which is fine)
                                                                        result = subprocess.run(['git', 'push'], capture_output = True, text = True)

                                                                        if result.returncode = = 0:
                                                                            logger.info(f"✅ Pushed knowledge update: {stats['total_interactions']} interactions")
                                                                            return True
                                                                    else:
                                                                        logger.info("📝 Knowledge saved locally (push manually when ready)")
                                                                        return False

                                                                    except subprocess.CalledProcessError as e:
                                                                        logger.debug(f"Git operation failed: {e}")
                                                                        return False
                                                                    except Exception as e:
                                                                        logger.error(f"Sync failed: {e}")
                                                                        return False

                                                                    def get_stats(self) - > Dict[str, Any]:
"""Get knowledge statistics."""
                                                                        return {
                                                                    "total_interactions": self.knowledge['total_interactions'],
                                                                    "learned_facts": len(self.knowledge['learned_facts']),
                                                                    "stored_responses": len(self.knowledge['successful_responses']),
                                                                    "intelligence_level": self.knowledge['intelligence_level'],
                                                                    "last_updated": self.knowledge['last_updated']
                                                                    }

                                                                    async def start_auto_sync(self):
"""Start automatic background syncing."""
                                                                        if self.auto_sync_task is None:
                                                                            self.auto_sync_task = asyncio.create_task(self._auto_sync_loop())
                                                                            logger.info(f"🔄 Started auto-sync (every {self.sync_interval//60} minutes)")

                                                                            async def stop_auto_sync(self):
"""Stop automatic background syncing."""
                                                                                if self.auto_sync_task:
                                                                                    self.auto_sync_task.cancel()
                                                                                    try:
                                                                                        await self.auto_sync_task
                                                                                        except asyncio.CancelledError:
                                                                                            pass
                                                                                        self.auto_sync_task = None
                                                                                        logger.info("🛑 Stopped auto-sync")

                                                                                        async def _auto_sync_loop(self):
"""Background loop for automatic syncing."""
                                                                                            while True:
                                                                                                try:
                                                                                                    await asyncio.sleep(self.sync_interval)

# Download latest knowledge
                                                                                                    await self.download_latest_knowledge()

# Upload our changes if we have any
                                                                                                    if self.knowledge['total_interactions'] > 0:
                                                                                                        await self.sync_to_cloud()

                                                                                                        except asyncio.CancelledError:
                                                                                                            break
                                                                                                        except Exception as e:
                                                                                                            logger.error(f"Auto-sync error: {e}")
                                                                                                            await asyncio.sleep(60) # Wait a minute before retrying

# Global instance
                                                                                                            shared_knowledge = SharedKnowledge()

                                                                                                            async def initialize_shared_knowledge():
"""Initialize and download latest shared knowledge."""
                                                                                                                logger.info("🧠 Initializing shared knowledge system...")

# Try to download latest from GitHub
                                                                                                                if await shared_knowledge.download_latest_knowledge():
                                                                                                                    logger.info("✅ Shared knowledge synchronized from cloud")
                                                                                                                else:
                                                                                                                    logger.info("📁 Using local knowledge only")

                                                                                                                    stats = shared_knowledge.get_stats()
                                                                                                                    logger.info(f"📊 Knowledge stats: {stats['total_interactions']} interactions, {stats['intelligence_level']} IQ")

# Start auto - sync for continuous learning
                                                                                                                    await shared_knowledge.start_auto_sync()

                                                                                                                    return shared_knowledge
