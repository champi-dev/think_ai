use std::sync::Arc;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use think_ai_knowledge::KnowledgeEngine;

#[test]
fn test_no_llm_initialization_errors() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test queries that previously might have triggered LLM calls
    let test_cases = vec![
        // Scientific queries
        ("explain relativity", "should get relativity explanation"),
        (
            "what is quantum mechanics",
            "should get quantum explanation",
        ),
        (
            "tell me about evolution",
            "should get evolution explanation",
        ),
        // Technical queries
        ("how do computers work", "should get computer explanation"),
        ("explain programming", "should get programming explanation"),
        ("what is an algorithm", "should get algorithm explanation"),
        // Philosophical queries
        (
            "what is the meaning of life",
            "should get philosophical response",
        ),
        ("what is consciousness", "should get consciousness response"),
        ("explain reality", "should get reality explanation"),
        // Analogy queries
        ("what is love like", "should get analogy response"),
        // Unknown queries
        ("xyzabc random gibberish", "should get helpful fallback"),
    ];

    for (query, description) in test_cases {
        println!("Testing: {} - {}", query, description);
        let response = generator.generate_response(query);

        // The fix ensures we never see this error
        assert!(
            !response.contains("Knowledge engine LLM not initialized"),
            "Query '{}' returned LLM initialization error: {}",
            query,
            response
        );

        // Response should be meaningful
        assert!(
            !response.is_empty(),
            "Query '{}' returned empty response",
            query
        );
    }
}

#[test]
fn test_response_quality_after_fix() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test that we get appropriate responses for each component type

    // Scientific component should handle science queries
    let response = generator.generate_response("explain relativity");
    assert!(
        response.contains("Einstein")
            || response.contains("spacetime")
            || response.contains("relativity")
    );

    // Technical component should handle tech queries
    let response = generator.generate_response("how do computers work");
    assert!(response.contains("CPU") || response.contains("processing"));

    // Philosophical component should handle philosophy
    let response = generator.generate_response("what is the meaning of life");
    assert!(response.contains("meaning") || response.contains("purpose"));

    // Unknown queries should get helpful responses
    let response = generator.generate_response("xyzabc123 gibberish");
    assert!(
        response.contains("don't have specific information")
            || response.contains("rephrase")
            || response.contains("not sure"),
        "Unknown query should get helpful response, got: {}",
        response
    );
}

#[test]
fn test_conversation_context_handling() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test with conversation context prepended (as done in chat handler)
    let context_query =
        "Previous conversation:\nuser: hello\nassistant: Hi there!\n\nCurrent query: what is AI";
    let response = generator.generate_response(context_query);

    // Should not trigger LLM error despite complex context
    assert!(
        !response.contains("Knowledge engine LLM not initialized"),
        "Context query returned LLM error: {}",
        response
    );
}

#[test]
fn test_model_selection() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test with explicit model selection
    let response =
        generator.generate_response_with_model("write hello world in rust", Some("codellama"));
    assert!(!response.contains("Knowledge engine LLM not initialized"));

    let response = generator.generate_response_with_model("what is consciousness", Some("qwen"));
    assert!(!response.contains("Knowledge engine LLM not initialized"));
}
