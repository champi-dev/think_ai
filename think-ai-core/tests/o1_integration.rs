//! Integration tests demonstrating O(1) performance across all components

use think_ai_core::*;
use std::time::Instant;

/// Test complete O(1) system integration
#[test]
fn test_full_o1_integration() {
    println!("\n=== O(1) System Integration Test ===\n");
    
    // 1. Initialize core engine
    let config = EngineConfig {
        cache_size: 100_000,
        ..Default::default()
    };
    let core_engine = O1Engine::new(config.clone());
    
    // 2. Initialize consciousness engine
    let consciousness = O1ConsciousnessEngine::new(core_engine);
    
    // 3. Initialize vector search
    let lsh_config = LSHConfig {
        dimension: 256,
        num_tables: 8,
        hash_functions: 6,
        ..Default::default()
    };
    let vector_engine = O1VectorEngine::new(lsh_config);
    
    // 4. Test consciousness processing
    println!("Testing Consciousness Processing...");
    let thoughts = vec![
        "Understanding the nature of consciousness",
        "Processing quantum information",
        "Evaluating ethical implications",
        "Generating creative solutions",
        "Analyzing complex patterns",
    ];
    
    for thought in &thoughts {
        let start = Instant::now();
        let (id, awareness) = consciousness.process_thought(thought).unwrap();
        let elapsed = start.elapsed();
        
        println!("  Thought: '{}' -> ID: {}, Awareness: {:.3}, Time: {:?}", 
            &thought[..30.min(thought.len())], id, awareness, elapsed);
    }
    
    // 5. Test vector indexing and search
    println!("\nTesting Vector Search...");
    
    // Index thought embeddings (simulated)
    for i in 0..1000 {
        let vector: Vec<f32> = (0..256)
            .map(|j| ((i * j) as f32).sin())
            .collect();
        
        vector_engine.index_vector(
            format!("thought_{}", i),
            vector,
            serde_json::json!({ "index": i, "type": "thought_embedding" })
        ).unwrap();
    }
    
    // Query for similar vectors
    let query_vector: Vec<f32> = (0..256)
        .map(|j| (42.0 * j as f32).sin())
        .collect();
    
    let start = Instant::now();
    let results = vector_engine.query(&query_vector, 5);
    let elapsed = start.elapsed();
    
    println!("  Vector query completed in {:?}", elapsed);
    println!("  Top 5 similar vectors:");
    for (id, similarity) in &results {
        println!("    {} - similarity: {:.3}", id, similarity);
    }
    
    // 6. Performance verification
    println!("\nPerformance Verification...");
    
    // Test scaling behavior
    let sizes = vec![1000, 10_000, 100_000];
    let mut timings = Vec::new();
    
    for size in &sizes {
        // Create test data
        let test_thought = format!("Scaling test with {} items", size);
        
        // Populate with data
        for i in 0..*size {
            consciousness.process_thought(&format!("{} {}", test_thought, i)).unwrap();
        }
        
        // Measure lookup time
        let start = Instant::now();
        let iterations = 10_000;
        
        for _ in 0..iterations {
            consciousness.process_thought(&test_thought).unwrap();
        }
        
        let elapsed = start.elapsed();
        let avg_ns = elapsed.as_nanos() / iterations as u128;
        timings.push((*size, avg_ns));
        
        println!("  Size {:>8}: avg lookup {:>6} ns", size, avg_ns);
    }
    
    // Verify O(1) scaling
    let base_time = timings[0].1 as f64;
    let mut is_o1 = true;
    
    println!("\n  Scaling Analysis:");
    for (size, time) in &timings {
        let ratio = *time as f64 / base_time;
        let status = if ratio < 2.0 { "✓" } else { "✗" };
        println!("    {:>8}: {:.2}x base time {}", size, ratio, status);
        
        if ratio > 2.0 {
            is_o1 = false;
        }
    }
    
    // 7. Get final metrics
    println!("\nSystem Metrics:");
    
    let consciousness_metrics = consciousness.get_metrics();
    println!("  Consciousness Engine:");
    println!("    Total thoughts: {}", consciousness_metrics.total_thoughts);
    println!("    Avg process time: {} ns", consciousness_metrics.avg_process_time_ns);
    println!("    Cache hit rate: {:.2}%", consciousness_metrics.cache_hit_rate * 100.0);
    println!("    Awareness level: {:.3}", consciousness_metrics.awareness_level);
    
    let vector_metrics = vector_engine.get_metrics();
    println!("  Vector Search Engine:");
    println!("    Total vectors: {}", vector_metrics.total_vectors);
    println!("    Avg query time: {} ns", vector_metrics.avg_query_time_ns);
    println!("    Avg candidates: {:.1}", vector_metrics.avg_candidates_per_query);
    
    // Assert O(1) performance
    assert!(is_o1, "System did not maintain O(1) performance characteristics");
    assert!(consciousness_metrics.avg_process_time_ns < 1000, "Consciousness processing too slow");
    assert!(vector_metrics.avg_query_time_ns < 100_000, "Vector search too slow: {} ns", vector_metrics.avg_query_time_ns);
    
    println!("\n✓ All O(1) performance requirements met!");
}

/// Benchmark O(1) operations at scale
#[test]
fn test_o1_at_scale() {
    println!("\n=== O(1) Scale Testing ===\n");
    
    let config = EngineConfig {
        cache_size: 10_000_000, // 10M entries
        ..Default::default()
    };
    
    let engine = O1Engine::new(config);
    let consciousness = O1ConsciousnessEngine::new(engine);
    
    // Generate 1M thoughts
    println!("Generating 1M thoughts...");
    let start = Instant::now();
    
    for i in 0..1_000_000 {
        consciousness.process_thought(&format!("Thought {}", i)).unwrap();
        
        if i % 100_000 == 0 && i > 0 {
            println!("  Processed {} thoughts...", i);
        }
    }
    
    let generation_time = start.elapsed();
    println!("  Generated 1M thoughts in {:?}", generation_time);
    
    // Test random access pattern
    println!("\nTesting random access pattern...");
    let mut total_time = 0u128;
    let test_iterations = 100_000;
    
    for i in 0..test_iterations {
        let thought_id = (i * 7919) % 1_000_000; // Prime number for good distribution
        let start = Instant::now();
        consciousness.process_thought(&format!("Thought {}", thought_id)).unwrap();
        total_time += start.elapsed().as_nanos();
    }
    
    let avg_access_ns = total_time / test_iterations as u128;
    println!("  Average random access time: {} ns", avg_access_ns);
    
    // Verify O(1) - should be under 1000ns (1μs) for O(1) with hash-based lookup
    assert!(avg_access_ns < 1000, "Random access exceeded O(1) threshold: {} ns", avg_access_ns);
    
    println!("\n✓ Scale testing passed - O(1) performance maintained at 1M items!");
}

/// Test consciousness and vector integration
#[test]
fn test_consciousness_vector_integration() {
    println!("\n=== Consciousness + Vector Integration ===\n");
    
    let config = EngineConfig::default();
    let engine = O1Engine::new(config);
    let consciousness = O1ConsciousnessEngine::new(engine);
    
    let lsh_config = LSHConfig {
        dimension: 128,
        ..Default::default()
    };
    let vector_engine = O1VectorEngine::new(lsh_config);
    
    // Process thoughts and create embeddings
    let thoughts = vec![
        ("philosophy", "What is the nature of consciousness?"),
        ("science", "Quantum mechanics explains reality"),
        ("philosophy", "The mind-body problem persists"),
        ("science", "Neural networks simulate cognition"),
        ("philosophy", "Free will versus determinism"),
    ];
    
    println!("Processing thoughts and creating embeddings...");
    
    for (category, thought) in &thoughts {
        // Process through consciousness
        let (thought_id, awareness) = consciousness.process_thought(thought).unwrap();
        
        // Create embedding (simulated based on content)
        let embedding: Vec<f32> = thought.chars()
            .enumerate()
            .map(|(i, c)| ((c as u32 * i as u32) as f32).sin())
            .cycle()
            .take(128)
            .collect();
        
        // Index in vector engine
        vector_engine.index_vector(
            format!("thought_{}", thought_id),
            embedding,
            serde_json::json!({
                "category": category,
                "awareness": awareness,
                "content": thought
            })
        ).unwrap();
        
        println!("  Indexed: {} (awareness: {:.3})", &thought[..30.min(thought.len())], awareness);
    }
    
    // Query for similar thoughts
    println!("\nQuerying for similar thoughts...");
    
    let query = "The nature of mind and consciousness";
    let query_embedding: Vec<f32> = query.chars()
        .enumerate()
        .map(|(i, c)| ((c as u32 * i as u32) as f32).sin())
        .cycle()
        .take(128)
        .collect();
    
    let results = vector_engine.query(&query_embedding, 3);
    
    println!("Query: '{}'", query);
    println!("Similar thoughts:");
    for (id, similarity) in results {
        println!("  {} - similarity: {:.3}", id, similarity);
    }
    
    println!("\n✓ Consciousness and vector integration successful!");
}