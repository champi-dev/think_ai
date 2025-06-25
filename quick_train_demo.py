#!/usr/bin/env python3
"""Quick training demo - trains Think AI with sample knowledge."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.core.config import Config
from think_ai.core.engine import ThinkAIEngine
from think_ai.training.knowledge_packager import KnowledgePackager
from think_ai.training.massive_trainer import MassiveKnowledgeTrainer
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def quick_train():
    """Quick training with 10,000 Q&A pairs for demo."""
    logger.info("Starting quick Think AI training demo...")

    # Initialize engine
    config = Config()
    engine = ThinkAIEngine(config)
    await engine.initialize()

    # Create trainer
    trainer = MassiveKnowledgeTrainer(engine)

    # Generate smaller set for quick demo
    logger.info("Generating 10,000 Q&A pairs for demo...")
    qa_pairs = await trainer.generate_qa_pairs(10_000)

    # Train the engine
    logger.info("Training Think AI engine...")
    await trainer.train_engine(qa_pairs, batch_size=100)

    # Package knowledge
    logger.info("Packaging knowledge...")
    packager = KnowledgePackager()
    manifest = packager.create_knowledge_packages(qa_pairs, chunk_size=1000)
    packager.create_embeddings_index(qa_pairs)
    packager.create_category_index(qa_pairs)

    # Test some questions
    logger.info("\nTesting trained knowledge:")
    test_questions = [
        "What is consciousness?",
        "How do I implement a hash table?",
        "Explain quantum mechanics",
        "Write a Python function to sort an array",
        "What is the meaning of life?",
    ]

    for question in test_questions:
        result = await engine.query_knowledge(question)
        logger.info(f"\nQ: {question}")
        if result.results:
            # Get the top result
            top_result = result.results[0]
            response = top_result.get('content', 'No response')
            logger.info(f"A: {response[:200]}...")
        else:
            logger.info("A: No results found")

    logger.info("\nQuick training complete! Full training available via train_massive_knowledge.py")


if __name__ == "__main__":
    asyncio.run(quick_train())
