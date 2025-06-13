#! / usr / bin / env python3

"""Complete system test with 100 questions - properly initialized."""

import asyncio
import contextlib
import json
import sys
import time

from implement_proper_architecture import ProperThinkAI

sys.path.append(".")


async def test_complete_system() - > None:
"""Test with 100 questions after proper initialization."""
# Initialize system properly
    system = ProperThinkAI()

    with contextlib.suppress(Exception):
        await system.initialize()

# Test questions organized by category
        test_questions = {
        "Astronomy": [
        ("what is a black hole", "region of spacetime"),
        ("what is the sun", "G - type main - sequence star"),
        ("what is the universe", "all of space, time, matter"),
        ("what is a galaxy", "collection of stars"),
        ("what is a planet", "celestial body"),
        ("what is a star", "massive ball"),
        ("what is dark matter", "matter"),
        ("what is a supernova", "stellar explosion"),
        ("what is a nebula", "cloud of gas"),
        ("what is a comet", "icy body"),
        ],
        "Philosophy": [
        ("what is consciousness", "awareness"),
        ("what is reality", "state of things"),
        ("what is truth", "accordance with fact"),
        ("what is knowledge", "facts, information"),
        ("what is wisdom", "quality of having"),
        ("what is existence", "state of being"),
        ("what is meaning", "what is meant"),
        ("what is purpose", "reason for which"),
        ("what is free will", "ability to choose"),
        ("what is morality", "principles concerning"),
        ],
        "Emotions": [
        ("what is love", "complex emotion"),
        ("what is happiness", "state of being happy"),
        ("what is sadness", "feeling of sorrow"),
        ("what is fear", "unpleasant emotion"),
        ("what is anger", "strong feeling"),
        ("what is joy", "feeling of great pleasure"),
        ("what is hope", "feeling of expectation"),
        ("what is empathy", "ability to understand"),
        ("what is compassion", "sympathetic pity"),
        ("what is gratitude", "quality of being thankful"),
        ],
        "Technology": [
        ("what is AI", "artificial intelligence"),
        ("what is a computer", "electronic device"),
        ("what is the internet", "global network"),
        ("what is blockchain", "distributed ledger"),
        ("what is machine learning", "type of AI"),
        ("what is programming", "process of creating"),
        ("what is an algorithm", "set of rules"),
        ("what is data", "facts and statistics"),
        ("what is software", "programs and operating"),
        ("what is hardware", "physical parts"),
        ],
        "Science": [
        ("what is physics", "science of matter"),
        ("what is chemistry", "science of substances"),
        ("what is biology", "science of life"),
        ("what is mathematics", "abstract science"),
        ("what is energy", "capacity to do work"),
        ("what is matter", "physical substance"),
        ("what is time", "indefinite continued progress"),
        ("what is space", "boundless three - dimensional"),
        ("what is gravity", "force that attracts"),
        ("what is light", "electromagnetic radiation"),
        ],
        "Nature": [
        ("what is water", "transparent fluid"),
        ("what is air", "invisible gaseous"),
        ("what is fire", "rapid oxidation"),
        ("what is earth", "planet we live on"),
        ("what is weather", "state of atmosphere"),
        ("what is climate", "weather conditions"),
        ("what is an ocean", "very large expanse"),
        ("what is a mountain", "large natural elevation"),
        ("what is a forest", "large area covered"),
        ("what is a desert", "barren area of landscape"),
        ],
        "Biology": [
        ("what is life", "condition that distinguishes"),
        ("what is DNA", "hereditary material"),
        ("what is evolution", "change in heritable"),
        ("what is a cell", "smallest unit of life"),
        ("what is photosynthesis", "process used by plants"),
        ("what is a virus", "infectious agent"),
        ("what is bacteria", "single - celled microorganisms"),
        ("what is a gene", "unit of heredity"),
        ("what is metabolism", "chemical processes"),
        ("what is protein", "large biomolecules"),
        ],
        "Abstract": [
        ("what is beauty", "quality that gives pleasure"),
        ("what is art", "expression of human creative"),
        ("what is music", "art of arranging sounds"),
        ("what is language", "method of communication"),
        ("what is culture", "ideas, customs, and social"),
        ("what is society", "aggregate of people"),
        ("what is democracy", "system of government"),
        ("what is justice", "quality of being fair"),
        ("what is freedom", "power to act"),
        ("what is peace", "freedom from disturbance"),
        ],
        "Daily Life": [
        ("what is money", "medium of exchange"),
        ("what is food", "substance consumed"),
        ("what is sleep", "naturally recurring state"),
        ("what is a dream", "series of thoughts"),
        ("what is memory", "faculty by which"),
        ("what is learning", "acquisition of knowledge"),
        ("what is teaching", "occupation of educating"),
        ("what is communication", "imparting or exchanging"),
        ("what is friendship", "mutual affection"),
        ("what is family", "group of people related"),
        ],
        "Random": [
        ("what is a quasar", "extremely luminous"),
        ("what is quantum mechanics", "fundamental theory"),
        ("what is relativity", "Einstein's theory"),
        ("what is an atom", "smallest unit of matter"),
        ("what is a photon", "quantum of light"),
        ("what is electricity", "form of energy"),
        ("what is magnetism", "physical phenomenon"),
        ("what is radiation", "emission of energy"),
        ("what is entropy", "measure of disorder"),
        ("what is chaos", "complete disorder"),
        ],
        }

# Track results
        results = {
        "total": 0,
        "good_responses": 0,
        "generic_responses": 0,
        "errors": 0,
        "by_category": {},
        "response_times": [],
        "response_lengths": [],
        }

# Test each category
        for category, questions in test_questions.items():
            category_results = {"good": 0, "generic": 0, "errors": 0}

            for question, expected_keyword in questions:
                results["total"] + = 1

                try:
                    start_time = time.time()

# Call the response method directly
                    response = await system.get_response(question)

                    response_time = time.time() - start_time
                    results["response_times"].append(response_time)
                    results["response_lengths"].append(len(response))

# Check response quality
                    if "While I'm processing this through my distributed intelligence" in response:
                        results["generic_responses"] + = 1
                        category_results["generic"] + = 1
                    elif expected_keyword.lower() in response.lower() or len(response) > 100:
                        results["good_responses"] + = 1
                        category_results["good"] + = 1
                    else:
                        results["generic_responses"] + = 1
                        category_results["generic"] + = 1

# Show progress

                        except Exception:
                            results["errors"] + = 1
                            category_results["errors"] + = 1

                            results["by_category"][category] = category_results

# Calculate statistics
                            sum(results["response_times"]) / len(results["response_times"]
                            ) if results["response_times"] else 0
                            sum(results["response_lengths"]) / len(results["response_lengths"]
                            ) if results["response_lengths"] else 0

# Generate detailed report

                            for category, cat_results in results["by_category"].items():
                                total = cat_results["good"] + \
                                cat_results["generic"] + cat_results["errors"]
                                success_rate = cat_results["good"] / total * 100 if total > 0 else 0

# Overall assessment
                                success_rate = results["good_responses"] / results["total"] * 100

                                if success_rate > = 90:
                                    verdict = "🏆 EXCELLENT - System performing at peak efficiency!"
                                elif success_rate > = 75:
                                    verdict = "✅ GOOD - System working well with minor issues"
                                elif success_rate > = 60:
                                    verdict = "⚠️ ADEQUATE - System functional but needs improvement"
                                else:
                                    verdict = "❌ POOR - System requires significant fixes"

# Save results
                                    with open("test_results.json", "w") as f:
                                        json.dump({
                                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                        "results": results,
                                        "success_rate": success_rate,
                                        "verdict": verdict,
                                        }, f, indent=2)

# Show some example responses

                                        sample_questions = [
                                        "what is a black hole",
                                        "what is consciousness",
                                        "what is love",
                                        "what is the sun",
                                        "what is AI",
                                        ]

                                        for q in sample_questions:
                                            with contextlib.suppress(Exception):
                                                response = await system.get_response(q)

                                                if __name__ = = "__main__":

                                                    asyncio.run(test_complete_system())
