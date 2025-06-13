#! / usr / bin / env python3

"""Test Think AI with 100 questions - simpler version without cache."""

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from implement_proper_architecture import ProperThinkAI
from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


class QuestionGenerator:
"""Generate questions with increasing difficulty."""

    def generate_question(self, iteration: int) - > Dict[str, Any]:
"""Generate a question based on iteration."""
        categories = ["math", "science", "programming", "philosophy", "general"]
        category = categories[iteration % len(categories)]

# Simple difficulty scaling
        difficulty = min(iteration / / 10 + 1, 10)

        if category = = "math":
            if difficulty < = 3:
                question = f"What is {iteration} + {iteration + 1}?"
            elif difficulty < = 6:
                question = f"Calculate {iteration} * {iteration + 1} / 2"
            else:
                question = f"Find the {iteration}th prime number"

            elif category = = "science":
                topics = [
                "atom",
                "molecule",
                "energy",
                "gravity",
                "light",
                "heat",
                "evolution",
                "DNA",
                "quantum",
                "relativity"]
                topic = topics[iteration % len(topics)]
                question = f"What is {topic}?"

            elif category = = "programming":
                concepts = [
                "variable",
                "function",
                "class",
                "loop",
                "array",
                "recursion",
                "algorithm",
                "API",
                "database",
                "AI"]
                concept = concepts[iteration % len(concepts)]
                question = f"Explain {concept} in programming"

            elif category = = "philosophy":
                topics = [
                "truth",
                "reality",
                "knowledge",
                "ethics",
                "free will",
                "consciousness",
                "meaning",
                "existence",
                "time",
                "identity"]
                topic = topics[iteration % len(topics)]
                question = f"What is {topic}?"

            else:  # general
            question = f"Question {iteration}: Tell me something interesting"

            return {
        "iteration": iteration,
        "category": category,
        "difficulty": difficulty,
        "question": question,
        }


        async def run_test() - > None:
"""Run 100 iteration test."""
# Initialize WITHOUT cache to ensure fresh state
            think_ai = ProperThinkAI(enable_cache=False)
            generator = QuestionGenerator()

            start_init = time.time()
            await think_ai.initialize()
            init_time = time.time() - start_init

# Test results
            results = []
            success_count = 0

            for i in range(100):
# Generate question
                question_data = generator.generate_question(i)
                question = question_data["question"]

# Query
                start_time = time.time()
                try:
                    response_data = await think_ai.process_with_proper_architecture(question)
                    response = response_data.get("response", "No response")
                    query_time = time.time() - start_time

# Check if we got a real response
                    if response and len(response) > 10:
                        success_count + = 1
                        success = True
                    else:
                        success = False

                        except Exception as e:
                            response = f"Error: {e ! s}"
                            query_time = time.time() - start_time
                            success = False
                            logger.exception(f"Query {i} failed: {e}")

                            results.append({
                            "iteration": i,
                            "question": question,
                            "response": response[:200] + "..." if len(response) > 200 else response,
                            "time": query_time,
                            "success": success,
                            })

# Update progress
                            if i % 5 = = 0:
                                int((i + 1) / 100 * 50)
                                success_rate = (success_count / (i + 1)) * 100 if i > 0 else 0

# Small delay
                                await asyncio.sleep(0.5)

# Calculate statistics
                                total_time = sum(r["time"] for r in results)
                                avg_time = total_time / len(results)
                                success_rate = (success_count / len(results)) * 100

# Show sample responses
                                for i in [0, 25, 50, 75, 99]:
                                    if i < len(results):
                                        results[i]

# Save results
                                        filename = f"test_results_100_{
                                        datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
                                        with open(filename, "w") as f:
                                            json.dump({
                                            "test_time": datetime.now().isoformat(),
                                            "init_time": init_time,
                                            "total_time": total_time,
                                            "success_rate": success_rate,
                                            "avg_response_time": avg_time,
                                            "results": results,
                                            }, f, indent=2)

                                            await think_ai.shutdown()

                                            if __name__ = = "__main__":
                                                asyncio.run(run_test())
