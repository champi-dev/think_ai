use std::sync::Arc;
use think_ai_knowledge::{ComponentResponseGenerator, KnowledgeEngine};

#[test]
fn test_response_generator_prioritizes_components_correctly() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test mathematical queries get handled by mathematical component
    let response = generator.generate_response("what is 2+2");
    assert_eq!(response, "2 + 2 = 4");

    let response = generator.generate_response("calculate 2 + 2");
    assert_eq!(response, "2 + 2 = 4");

    // Test greeting queries get handled by conversational component
    let response = generator.generate_response("hello");
    assert!(response.contains("Hi") || response.contains("Hello") || response.contains("Hey"));
    assert!(!response.contains("quantum field"));

    // Test identity queries
    let response = generator.generate_response("what is your name");
    assert!(response.contains("Think AI"));
    assert!(!response.contains("quantum field"));

    // Test philosophical queries get quantum responses
    let response = generator.generate_response("what is consciousness");
    assert!(response.contains("quantum") || response.contains("Quantum"));
    assert!(response.contains("consciousness") || response.contains("Consciousness"));
}

#[test]
fn test_no_quantum_hijacking_of_technical_queries() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Technical queries should not get quantum responses
    let technical_queries = vec![
        "how to install rust",
        "debug python code",
        "git commit message",
        "npm install error",
        "fix typescript bug",
        "create react component",
        "database query optimization",
        "api endpoint design",
    ];

    for query in technical_queries {
        let response = generator.generate_response(query);
        assert!(
            !response.contains("Your query resonates through the quantum field"),
            "Query '{}' should not get quantum field response, but got: {}",
            query,
            response
        );
    }
}

#[test]
fn test_fallback_for_truly_unknown_queries() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Completely unhandled queries should get fallback
    let response = generator.generate_response("xyzabc123 gibberish query");
    assert!(
        response.contains("not sure how to respond")
            || response.contains("rephrase")
            || response.contains("Knowledge engine LLM not initialized"),
        "Unknown query should get fallback response, but got: {}",
        response
    );
}

#[test]
fn test_math_component_priority() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Math component should have highest priority for arithmetic
    assert_eq!(generator.generate_response("2+2"), "2 + 2 = 4");
    assert_eq!(generator.generate_response("what is 2+2?"), "2 + 2 = 4");
    assert_eq!(generator.generate_response("What's 2 + 2"), "2 + 2 = 4");
    assert_eq!(generator.generate_response("calculate 1 + 1"), "1 + 1 = 2");
}

#[test]
fn test_humor_component_priority() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    let response = generator.generate_response("tell me a joke");
    assert!(response.contains("joke"));
    assert!(!response.contains("quantum field"));
}

#[test]
fn test_component_ordering_and_fallthrough() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);

    // Test that components are tried in order of score
    // Identity should win for "who are you" over quantum consciousness
    let response = generator.generate_response("who are you");
    assert!(response.contains("Think AI"));
    assert!(response.contains("AI assistant"));

    // But quantum consciousness should handle philosophical identity questions
    let response = generator.generate_response("what is the nature of your consciousness");
    assert!(response.contains("quantum") || response.contains("Quantum"));
}
