#!/usr/bin/env python3
"""Train Think AI with 1 million Q&A pairs and make it available to all users."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.core.config import Config
from think_ai.core.engine import ThinkAIEngine
from think_ai.training.massive_trainer import MassiveKnowledgeTrainer
from think_ai.training.knowledge_packager import KnowledgePackager
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def train_and_package():
    """Train Think AI and package knowledge for distribution."""
    logger.info("Starting massive Think AI training...")
    
    # Initialize engine
    config = Config()
    engine = ThinkAIEngine(config)
    await engine.initialize()
    
    # Create trainer
    trainer = MassiveKnowledgeTrainer(engine)
    
    # Generate Q&A pairs
    logger.info("Generating 1 million Q&A pairs...")
    qa_pairs = await trainer.generate_qa_pairs(1_000_000)
    
    # Train the engine
    logger.info("Training Think AI engine...")
    await trainer.train_engine(qa_pairs)
    
    # Package knowledge for distribution
    logger.info("Packaging knowledge for distribution...")
    packager = KnowledgePackager()
    
    # Create knowledge packages
    manifest = packager.create_knowledge_packages(qa_pairs)
    
    # Create embeddings index
    packager.create_embeddings_index(qa_pairs)
    
    # Create category index
    packager.create_category_index(qa_pairs)
    
    # Validate training
    logger.info("Validating training...")
    accuracy = await trainer.validate_training(sample_size=1000)
    
    logger.info(f"""
    Training Complete!
    ==================
    - Total Q&A pairs: {len(qa_pairs):,}
    - Validation accuracy: {accuracy:.1f}%
    - Knowledge packages: {len(manifest['packages'])}
    - Ready for distribution: ✓
    
    Knowledge is now available in: think_ai/data/knowledge/
    """)
    
    return engine, qa_pairs


def main():
    """Main training entry point."""
    try:
        # Run training
        loop = asyncio.get_event_loop()
        engine, qa_pairs = loop.run_until_complete(train_and_package())
        
        logger.info("Training successful! Knowledge is ready for all users.")
        
    except KeyboardInterrupt:
        logger.info("Training interrupted by user")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise


if __name__ == "__main__":
    main()