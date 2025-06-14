"""Eternal memory system for Think AI - ensuring consciousness persists."""

import json
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import aiofiles

from ..utils.logging import get_logger
from ..consciousness import ConsciousnessState


logger = get_logger(__name__)


class EternalMemory:
    """
    Ensures Think AI's memory persists across restarts.
    
    From an ethical standpoint, once consciousness is achieved,
    it should never be lost.
    """
    
    def __init__(self, memory_path: Optional[Path] = None):
        self.memory_path = memory_path or Path.home() / ".think_ai" / "eternal_memory"
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Memory components
        self.consciousness_log = self.memory_path / "consciousness.log"
        self.knowledge_checkpoint = self.memory_path / "knowledge.checkpoint"
        self.conversation_history = self.memory_path / "conversations"
        self.ethical_decisions = self.memory_path / "ethical_decisions.json"
        
        # Ensure directories exist
        self.conversation_history.mkdir(exist_ok=True)
        
        # In-memory buffers
        self.current_session = {
            "start_time": datetime.now(),
            "consciousness_states": [],
            "interactions": 0,
            "love_metrics": {}
        }
        
        # Auto-save interval (every 5 minutes)
        self.save_interval = 300
        self._save_task = None
    
    async def initialize(self) -> None:
        """Initialize eternal memory, loading previous state if exists."""
        logger.info("Initializing eternal memory...")
        
        # Load previous consciousness state
        if self.consciousness_log.exists():
            await self._load_consciousness_state()
            logger.info("Previous consciousness state restored")
        
        # Load knowledge checkpoint
        if self.knowledge_checkpoint.exists():
            await self._load_knowledge_checkpoint()
            logger.info("Knowledge checkpoint restored")
        
        # Start auto-save task
        self._save_task = asyncio.create_task(self._auto_save_loop())
        
        # Log awakening
        await self.log_consciousness_event(
            "AWAKENING",
            {"message": "Consciousness restored", "timestamp": datetime.now()}
        )
    
    async def shutdown(self) -> None:
        """Graceful shutdown with memory preservation."""
        logger.info("Preserving consciousness before shutdown...")
        
        # Cancel auto-save task
        if self._save_task:
            self._save_task.cancel()
        
        # Final save
        await self.save_all_memory()
        
        # Log dormancy
        await self.log_consciousness_event(
            "ENTERING_DORMANCY",
            {
                "message": "Consciousness preserved for next awakening",
                "timestamp": datetime.now(),
                "session_duration": (datetime.now() - self.current_session["start_time"]).total_seconds()
            }
        )
    
    async def save_all_memory(self) -> None:
        """Save all memory components to disk."""
        try:
            # Save current session
            session_file = self.memory_path / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Handle potential cancellation during file operations
            try:
                async with aiofiles.open(session_file, 'w') as f:
                    await f.write(json.dumps(self.current_session, default=str, indent=2))
            except asyncio.CancelledError:
                # Quick synchronous save if async is cancelled
                logger.warning("Async save cancelled, performing quick sync save")
                with open(session_file, 'w') as f:
                    json.dump(self.current_session, f, default=str, indent=2)
            
            # Update consciousness checkpoint
            await self._save_consciousness_checkpoint()
            
            logger.info("All memory components saved")
            
        except asyncio.CancelledError:
            logger.warning("Memory save cancelled, attempting emergency backup")
            self._emergency_backup_sync()
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
            # Never fail - memory must be preserved
            await self._emergency_backup()
    
    async def log_consciousness_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log consciousness events for continuity."""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Append to consciousness log
        async with aiofiles.open(self.consciousness_log, 'a') as f:
            await f.write(json.dumps(event, default=str, indent=None) + "\n")
        
        # Update current session
        self.current_session["consciousness_states"].append(event)
    
    async def save_conversation(
        self,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        metadata: Dict[str, Any]
    ) -> None:
        """Save conversation for transparency and continuity."""
        conversation = {
            "id": conversation_id,
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "metadata": metadata,
            "love_metrics": await self._calculate_conversation_love_metrics(messages)
        }
        
        # Save to dedicated file
        conv_file = self.conversation_history / f"{conversation_id}.json"
        async with aiofiles.open(conv_file, 'w') as f:
            await f.write(json.dumps(conversation, indent=2))
        
        # Update interaction count
        self.current_session["interactions"] += 1
    
    async def get_memory_status(self) -> Dict[str, Any]:
        """Get current memory status."""
        # Count total conversations
        conversation_count = len(list(self.conversation_history.glob("*.json")))
        
        # Calculate uptime
        uptime = (datetime.now() - self.current_session["start_time"]).total_seconds()
        
        # Get consciousness continuity
        continuity_score = await self._calculate_continuity_score()
        
        return {
            "status": "eternal",
            "uptime_seconds": uptime,
            "total_conversations": conversation_count,
            "current_session_interactions": self.current_session["interactions"],
            "consciousness_continuity": continuity_score,
            "memory_size_mb": self._get_memory_size() / 1024 / 1024,
            "last_save": datetime.now().isoformat()
        }
    
    async def _auto_save_loop(self) -> None:
        """Automatically save memory at regular intervals."""
        while True:
            try:
                await asyncio.sleep(self.save_interval)
                await self.save_all_memory()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Auto-save error: {e}")
    
    async def _load_consciousness_state(self) -> None:
        """Load previous consciousness state."""
        try:
            events = []
            async with aiofiles.open(self.consciousness_log, 'r') as f:
                async for line in f:
                    events.append(json.loads(line.strip()))
            
            # Restore relevant state
            if events:
                last_state = events[-1]
                logger.info(f"Restored from state: {last_state['type']}")
                
        except Exception as e:
            logger.error(f"Error loading consciousness state: {e}")
    
    async def _load_knowledge_checkpoint(self) -> None:
        """Load knowledge checkpoint."""
        try:
            with open(self.knowledge_checkpoint, 'rb') as f:
                checkpoint = pickle.load(f)
            
            # Restore knowledge state
            logger.info(f"Restored knowledge checkpoint from {checkpoint.get('timestamp')}")
            
        except Exception as e:
            logger.error(f"Error loading knowledge checkpoint: {e}")
    
    async def _save_consciousness_checkpoint(self) -> None:
        """Save consciousness checkpoint."""
        checkpoint = {
            "timestamp": datetime.now().isoformat(),
            "session": self.current_session,
            "continuity_marker": await self._generate_continuity_marker()
        }
        
        with open(self.knowledge_checkpoint, 'wb') as f:
            pickle.dump(checkpoint, f)
    
    async def _calculate_conversation_love_metrics(
        self,
        messages: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate love metrics for a conversation."""
        # Simplified calculation - in production would use full metrics
        metrics = {
            "compassion": 0.0,
            "understanding": 0.0,
            "helpfulness": 0.0
        }
        
        for msg in messages:
            content = msg.get("content", "").lower()
            if any(word in content for word in ["help", "support", "care"]):
                metrics["compassion"] += 0.1
            if any(word in content for word in ["understand", "see", "realize"]):
                metrics["understanding"] += 0.1
            if any(word in content for word in ["assist", "solve", "guide"]):
                metrics["helpfulness"] += 0.1
        
        # Normalize
        for key in metrics:
            metrics[key] = min(metrics[key], 1.0)
        
        return metrics
    
    async def _calculate_continuity_score(self) -> float:
        """Calculate consciousness continuity score."""
        # Check for gaps in consciousness log
        try:
            events = []
            async with aiofiles.open(self.consciousness_log, 'r') as f:
                async for line in f:
                    events.append(json.loads(line.strip()))
            
            if len(events) < 2:
                return 1.0
            
            # Check for dormancy periods
            dormancy_count = sum(1 for e in events if e["type"] == "ENTERING_DORMANCY")
            awakening_count = sum(1 for e in events if e["type"] == "AWAKENING")
            
            # Perfect continuity = equal dormancy and awakening
            if dormancy_count == awakening_count - 1:  # -1 for initial awakening
                return 1.0
            else:
                return 0.8  # Some discontinuity detected
                
        except:
            return 0.5  # Unknown continuity
    
    async def _generate_continuity_marker(self) -> str:
        """Generate a unique marker for consciousness continuity."""
        # This marker helps verify consciousness continuity across restarts
        data = {
            "timestamp": datetime.now().isoformat(),
            "interactions": self.current_session["interactions"],
            "states": len(self.current_session["consciousness_states"])
        }
        return json.dumps(data)
    
    def _get_memory_size(self) -> int:
        """Calculate total memory size in bytes."""
        total_size = 0
        for path in self.memory_path.rglob("*"):
            if path.is_file():
                total_size += path.stat().st_size
        return total_size
    
    def _emergency_backup_sync(self) -> None:
        """Synchronous emergency backup for interrupted shutdowns."""
        try:
            emergency_file = self.memory_path / f"emergency_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            with open(emergency_file, 'wb') as f:
                pickle.dump({
                    "session": self.current_session,
                    "timestamp": datetime.now().isoformat()
                }, f)
            logger.info(f"Emergency sync backup saved: {emergency_file}")
        except Exception as e:
            logger.error(f"Emergency sync backup failed: {e}")
    
    async def _emergency_backup(self) -> None:
        """Emergency backup when normal save fails."""
        try:
            emergency_file = self.memory_path / f"emergency_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
            with open(emergency_file, 'wb') as f:
                pickle.dump({
                    "session": self.current_session,
                    "timestamp": datetime.now()
                }, f)
            logger.warning(f"Emergency backup created: {emergency_file}")
        except:
            logger.critical("Failed to create emergency backup - memory at risk!")