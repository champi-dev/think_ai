#! / usr / bin / env python3

"""Test conversation context, relevance, and coherence fixes."""

import asyncio
import json
import time

from implement_proper_architecture import ProperThinkAI

# Test conversation flows to verify fixes
TEST_CONVERSATIONS = [
{
"name": "Universe Creation Context",
"questions": [
"what is a universe",
"who created it",  # Should understand "it" refers to universe
"how old is it",  # Should understand "it" refers to universe
],
},
{
"name": "Black Hole Properties",
"questions": [
"what is a black hole",
"how does it form",  # Should understand "it" refers to black hole
"can anything escape from it",  # Context should be maintained
],
},
{
"name": "Sun Information",
"questions": [
"what is the sun",
"how hot is it",  # Should refer to the sun
"what is it made of",  # Should still be about the sun
],
},
{
"name": "AI Consciousness",
"questions": [
"what is consciousness",
"can AI have it",  # Should understand "it" refers to consciousness
"how would we know if it exists",  # Context about AI consciousness
],
},
]


async def test_conversation_context() - > None:
"""Test that AI maintains context between questions."""
    think_ai = ProperThinkAI()
    await think_ai.initialize()

    results = {
    "total_tests": 0,
    "coherent_responses": 0,
    "relevant_responses": 0,
    "complete_responses": 0,
    "conversations": [],
    }

    for conversation in TEST_CONVERSATIONS:

        conv_results = {
        "name": conversation["name"],
        "exchanges": [],
        }

# Reset conversation history for each test
        think_ai.conversation_history = []

        for i, question in enumerate(conversation["questions"]):
            results["total_tests"] + = 1

            start_time = time.time()
            result = await think_ai.process_with_proper_architecture(question)
            process_time = time.time() - start_time

            response = result["response"]

# Check coherence (complete sentences)
            is_complete = (
            response.strip().endswith((".", "!", "?", """)) and
            len(response) > 50 # Not too short
            )

# Check relevance (for follow - up questions)
            is_relevant = True
            if i > 0: # For follow - up questions
# Check if response acknowledges context
            if "it" in question.lower():
# Response should relate to previous topic
                prev_topic = conversation["questions"][0].split()[ - 1] # Last word of first question
                is_relevant = (
                prev_topic in response.lower() or
                ("universe" in response.lower() and "universe" in conversation["questions"][0]) or
                ("black hole" in response.lower() and "black hole" in conversation["questions"][0]) or
                ("sun" in response.lower() and "sun" in conversation["questions"][0]) or
                ("consciousness" in response.lower() and "consciousness" in conversation["questions"][0])
                )

                if is_complete:
                    results["complete_responses"] + = 1
                else:
                    pass

                if is_relevant:
                    results["relevant_responses"] + = 1
                else:
                    pass

# Overall coherence check
                is_coherent = is_complete and is_relevant and len(response) > 100
                if is_coherent:
                    results["coherent_responses"] + = 1

                    conv_results["exchanges"].append({
                    "question": question,
                    "response": response,
                    "is_complete": is_complete,
                    "is_relevant": is_relevant,
                    "is_coherent": is_coherent,
                    "process_time": process_time,
                    })

                    results["conversations"].append(conv_results)

# Summary

# Detailed analysis
                    for conv in results["conversations"]:
                        for i, exchange in enumerate(conv["exchanges"]):
                            "✅" if exchange["is_coherent"] else "❌"

# Save results
                            with open("conversation_test_results.json", "w") as f:
                                json.dump(results, f, indent = 2)

# Success criteria
                                success_rate = results["coherent_responses"] / results["total_tests"]
                                if success_rate > = 0.8:
                                    pass
                            else:
                                pass

                            await think_ai.shutdown()

                            if __name__ = = "__main__":
                                asyncio.run(test_conversation_context())
