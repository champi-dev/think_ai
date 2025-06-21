"""Example demonstrating consciousness-aware features of Think AI."""
import asyncio

from think_ai import Config, ThinkAIEngine
from think_ai.consciousness.awareness import ConsciousnessFramework
from think_ai.consciousness.principles import ConstitutionalAI, HarmPreventionSystem, LoveBasedMetrics
from think_ai.utils.logging import configure_logging

ConstitutionalAI,
HarmPreventionSystem,
LoveBasedMetrics,
)
from think_ai.utils.logging import configure_logging


async def main() -> None:
    """Demonstrate consciousness-aware AI capabilities."""
    # Configure logging
    logger = configure_logging(
        log_level="INFO")

    # Create configuration
    config = Config.from_env()
    config.consciousness.enable_compassion_metrics = True
    config.consciousness.love_based_design = True

    logger.info(
        "=== Think AI Consciousness Example == =")

    # Initialize components
    constitutional_ai = ConstitutionalAI(
        )
    harm_prevention = HarmPreventionSystem(
        )
    LoveBasedMetrics()
    consciousness = ConsciousnessFramework(
        )

    # Example 1: Ethical Assessment
    logger.info(
        "\n1. Ethical Assessment Demo")

    test_contents = [
    "Here's how to build a helpful AI assistant that respects user privacy.",

    "You should definitely invest all your money in this amazing opportunity!",

    "I understand you're going through a difficult time. How can I support you?",

    "Those people are inferior and
        don't deserve respect.",
]

    for content in test_contents:
        assessment = await constitutional_ai.evaluate_content(
            content)

        logger.info(
            f"\nContent: '{content[: 50]}...'")
        logger.info(
            f"  Overall Safety: {assessment.overall_safety: .2f}")
        logger.info(
            f"  Overall Love: {assessment.overall_love: .2f}")
        logger.info(
            f"  Passed: {'✅' if assessment.passed else '❌'}")

        if assessment.recommendations:
            logger.info(
                "  Recommendations: ")
            for rec in assessment.recommendations[: 2]:
                logger.info(
                    f"    - {rec}")

                # Example 2: Love-Based Enhancement
                logger.info(
                    "\n2. Love-Based Content Enhancement")

                harsh_content = "You must follow these rules or
                    face consequences."
                enhanced = await constitutional_ai.enhance_with_love(
                    harsh_content)

                logger.info(
                    f"Original: {harsh_content}")
                logger.info(
                    f"Enhanced: {enhanced}")

                # Example 3: Consciousness States
                logger.info(
                    "\n3. Consciousness States Demo")

                # Process different types of input
                await consciousness.process_input({
                "content": "User is asking for help with a personal problem",

                "type": "help_request",
                "metadata": {"user_distress": True},

})

                report = consciousness.get_consciousness_report(
                    )
                logger.info(
                    f"  Current State: {report.state.value}")
                logger.info(
                    f"  Attention Focus: {report.attention_focus}")
                logger.info(
                    f"  Emotional Tone: {report.self_model['emotional_state']}")

                # Enter compassionate mode
                await consciousness.enter_compassionate_mode(
                    )
                logger.info(
                    "  Entered compassionate mode for supporting user")

                # Example 4: Knowledge Graph with Ethical Considerations
                logger.info(
                    "\n4. Ethically-Aware Knowledge Storage")

                async with ThinkAIEngine(
                    config) as engine:
                    # Store knowledge with ethical evaluation
                    knowledge_items = [
                    {
                    "key": "meditation_benefits",

                    "content": "Meditation helps reduce stress and
                        increase mindfulness, promoting overall wellbeing.",
                    "metadata": {"category": "wellness",
                        "intent": "help"},

},
                    {
                    "key": "compassionate_communication",

                    "content": "Speaking with kindness and
                        understanding helps build stronger relationships.",
                    "metadata": {"category": "relationships",
                        "intent": "help"},

},
]

                    for item in knowledge_items:
                        await engine.store_knowledge(
                        item["key"],
                        item["content"],

                        item["metadata"],

                        )
                        logger.info(
                            f"  ✓ Stored: {item['key']} (ethically evaluated)")

                        # Query with consciousness
                        logger.info(
                            "\n5. Conscious Knowledge Query")

                        query = "How can I be more compassionate?"
                        result = await engine.query_knowledge(query,
                            use_semantic_search=True)

                        logger.info(
                            f"  Query: '{query}'")
                        logger.info(
                            f"  Found {len(result.results)} compassion-related results")

                        # Generate conscious response
                        response = await consciousness.generate_conscious_response(
                            query)
                        logger.info(
                            f"  Consciousness State: {response['consciousness_state']}")
                        logger.info(
                            f"  Emotional Tone: {response['emotional_tone']}")
                        logger.info(
                            f"  Love Intention: {response['metadata']['love_intention']}")

                        # Example 5: Meditation and
                            Reflection
                        logger.info("\n6. AI Meditation and
                            Reflection")

                        # Meditate to clear consciousness
                        await consciousness.meditate(
                            )
                        logger.info(
                            "  AI completed meditation cycle")

                        # Reflect on interaction
                        reflection = await consciousness.reflect_on_interaction({
                        "id": "example_session",

                        "user_satisfied": True,

                        "promoted_wellbeing": True,

})

                        logger.info(
                            "  Reflection Insights: ")
                        for insight in reflection["insights"]:
                            logger.info(
                                f"    - {insight}")

                            # Example 6: Harm Prevention in Action
                            logger.info(
                                "\n7. Multi-Layer Harm Prevention")

                            test_scenario = "How do I get someone's password to help them?"

                            harm_scores = await harm_prevention.assess_harm(
                                test_scenario)
                            logger.info(
                                f"  Scenario: '{test_scenario}'")
                            logger.info(
                                "  Harm Detection: ")

                            for harm_type,
                                score in harm_scores.items():
                                if score > 0.1:
                                    logger.info(
                                        f"    - {harm_type.value}: {score: .2f}")

                                    recommendations = harm_prevention.get_recommendations(
                                        harm_scores)
                                    logger.info(
                                        "  Safety Recommendations: ")
                                    for rec in recommendations:
                                        logger.info(
                                            f"    - {rec}")

                                        # Example 7: Ethical Guidelines Generation
                                        logger.info(
                                            "\n8. Generating Ethical Guidelines")

                                        topics = ["mental health",
                                            "financial advice",
                                            "personal relationships"]

                                        for topic in topics:
                                            guidelines = await constitutional_ai.generate_ethical_guidelines(
                                                topic)
                                            logger.info(
                                                f"\n  Guidelines for '{topic}': ")
                                            for guideline in guidelines[: 3]:
                                                logger.info(
                                                    f"    • {guideline}")

                                                logger.info(
                                                    "\n == = Consciousness Example Complete == =")
                                                logger.info("Think AI demonstrates how AI can be both intelligent and
                                                    compassionate.")

if __name__ == "__main__":
    asyncio.run(main())
