#!/bin/bash
set -e

echo "Fixing consciousness_engine.rs test module..."

# Create a temporary file with the fixed test module
cat > /tmp/consciousness_engine_tests.rs << 'EOF'
#[cfg(test)]
mod tests {
    use super::*;
    use crate::EngineConfig;
    
    #[test]
    fn test_o1_consciousness() {
        let config = EngineConfig::default();
        let core = O1Engine::new(config);
        let consciousness = O1ConsciousnessEngine::new(core);
        
        // Test thought processing
        let (id1, awareness1) = consciousness.process_thought("Hello world").unwrap();
        assert!(id1 > 0);
        assert!(awareness1 > 0.0 && awareness1 <= 1.0);
        
        // Test cache hit (should be faster)
        let (id2, awareness2) = consciousness.process_thought("Hello world").unwrap();
        assert_eq!(id1, id2); // Same thought should return same ID
        assert_eq!(awareness1, awareness2);
        
        // Test metrics
        let metrics = consciousness.get_metrics();
        assert_eq!(metrics.total_thoughts, 2);
        assert_eq!(metrics.cache_hit_rate, 0.5); // 1 hit, 1 miss
    }
    
    #[test]
    fn test_o1_performance_guarantee() {
        let config = EngineConfig {
            cache_size: 1_000_000,
            ..Default::default()
        };
        let core = O1Engine::new(config);
        let consciousness = O1ConsciousnessEngine::new(core);
        
        // Generate many thoughts
        for i in 0..10000 {
            consciousness
                .process_thought(&format!("Thought {}", i))
                .unwrap();
        }
        
        // Measure lookup time for existing thought
        let start = std::time::Instant::now();
        for _ in 0..1000 {
            consciousness.process_thought("Thought 42").unwrap();
        }
        let elapsed = start.elapsed();
        let avg_ns = elapsed.as_nanos() / 1000;
        println!("Average consciousness lookup: {} ns", avg_ns);
        
        // Should be under 100ns for O(1) guarantee
        assert!(
            avg_ns < 100,
            "Lookup time {} ns exceeds O(1) threshold",
            avg_ns
        );
    }
}
EOF

# Replace the test module in the file
# First, find where the test module starts
LINE_NUM=$(grep -n "^#\[cfg(test)\]" think-ai-core/src/consciousness_engine.rs | cut -d: -f1)

# Delete from that line to the end of the file
sed -i "${LINE_NUM},\$ d" think-ai-core/src/consciousness_engine.rs

# Append the fixed test module
cat /tmp/consciousness_engine_tests.rs >> think-ai-core/src/consciousness_engine.rs

echo "Fixed consciousness_engine.rs test module"