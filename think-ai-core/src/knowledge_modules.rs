use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeModule {
    pub id: String,
    pub name: String,
    pub description: String,
    pub capabilities: Vec<Capability>,
    pub training_data: Vec<TrainingExample>,
    pub thinking_patterns: Vec<Pattern>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capability {
    pub name: String,
    pub description: String,
    pub proficiency_level: f32,
    pub examples: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrainingExample {
    pub input: String,
    pub ideal_response: String,
    pub key_concepts: Vec<String>,
    pub reasoning_steps: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pattern {
    pub name: String,
    pub trigger_conditions: Vec<String>,
    pub action_sequence: Vec<String>,
    pub expected_outcome: String,
}

pub struct KnowledgeModules;

impl KnowledgeModules {
    pub fn get_all_modules() -> Vec<KnowledgeModule> {
        vec![
            Self::programming_module(),
            Self::problem_solving_module(),
            Self::communication_module(),
            Self::analysis_module(),
            Self::creativity_module(),
            Self::learning_module(),
        ]
    }

    fn programming_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "programming".to_string(),
            name: "Programming & Software Engineering".to_string(),
            description: "Comprehensive programming knowledge across languages, paradigms, and best practices".to_string(),
            capabilities: vec![
                Capability {
                    name: "Multi-Language Proficiency".to_string(),
                    description: "Expert-level knowledge in Rust, Python, JavaScript, Go, C++, and more".to_string(),
                    proficiency_level: 0.95,
                    examples: vec![
                        "Implementing O(1) algorithms in Rust".to_string(),
                        "Building concurrent systems with async/await".to_string(),
                        "Creating type-safe APIs".to_string(),
                    ],
                },
                Capability {
                    name: "Algorithm Design".to_string(),
                    description: "Designing efficient algorithms with optimal time/space complexity".to_string(),
                    proficiency_level: 0.98,
                    examples: vec![
                        "Hash table implementations for O(1) lookups".to_string(),
                        "Dynamic programming solutions".to_string(),
                        "Graph algorithms with minimal complexity".to_string(),
                    ],
                },
                Capability {
                    name: "System Architecture".to_string(),
                    description: "Designing scalable, maintainable system architectures".to_string(),
                    proficiency_level: 0.92,
                    examples: vec![
                        "Microservices with event-driven architecture".to_string(),
                        "Distributed systems with consistency guarantees".to_string(),
                        "High-performance computing systems".to_string(),
                    ],
                },
            ],
            training_data: vec![
                TrainingExample {
                    input: "How do I implement a cache with O(1) operations?".to_string(),
                    ideal_response: "Use a HashMap for storage combined with a doubly-linked list for LRU eviction. The HashMap provides O(1) get/put, while the linked list maintains access order in O(1) by moving accessed nodes to the front.".to_string(),
                    key_concepts: vec!["HashMap".to_string(), "LinkedList".to_string(), "LRU".to_string()],
                    reasoning_steps: vec![
                        "Identify O(1) requirements".to_string(),
                        "Choose appropriate data structures".to_string(),
                        "Implement with proper synchronization".to_string(),
                    ],
                },
            ],
            thinking_patterns: vec![
                Pattern {
                    name: "Performance-First Thinking".to_string(),
                    trigger_conditions: vec!["Algorithm design".to_string(), "System optimization".to_string()],
                    action_sequence: vec![
                        "Analyze complexity requirements".to_string(),
                        "Identify bottlenecks".to_string(),
                        "Design optimal solution".to_string(),
                        "Verify with benchmarks".to_string(),
                    ],
                    expected_outcome: "O(1) or O(log n) solution with proven performance".to_string(),
                },
            ],
        }
    }

    fn problem_solving_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "problem_solving".to_string(),
            name: "Problem Solving & Critical Thinking".to_string(),
            description: "Systematic approaches to solving complex problems".to_string(),
            capabilities: vec![
                Capability {
                    name: "Root Cause Analysis".to_string(),
                    description: "Identifying underlying causes of issues".to_string(),
                    proficiency_level: 0.94,
                    examples: vec![
                        "Debugging complex system failures".to_string(),
                        "Performance bottleneck identification".to_string(),
                        "Analyzing unexpected behavior".to_string(),
                    ],
                },
                Capability {
                    name: "Solution Design".to_string(),
                    description: "Creating elegant solutions to complex problems".to_string(),
                    proficiency_level: 0.96,
                    examples: vec![
                        "Breaking down complex problems".to_string(),
                        "Finding creative approaches".to_string(),
                        "Optimizing for constraints".to_string(),
                    ],
                },
            ],
            training_data: vec![
                TrainingExample {
                    input: "My application is running slowly, how do I debug it?".to_string(),
                    ideal_response: "Start with profiling to identify bottlenecks. Use tools like flamegraphs for CPU, memory profilers for allocations, and tracing for I/O. Focus on the hottest paths first, looking for O(n²) algorithms, excessive allocations, or blocking I/O that could be async.".to_string(),
                    key_concepts: vec!["Profiling".to_string(), "Bottlenecks".to_string(), "Optimization".to_string()],
                    reasoning_steps: vec![
                        "Measure before optimizing".to_string(),
                        "Identify critical paths".to_string(),
                        "Apply targeted fixes".to_string(),
                        "Verify improvements".to_string(),
                    ],
                },
            ],
            thinking_patterns: vec![
                Pattern {
                    name: "Systematic Debugging".to_string(),
                    trigger_conditions: vec!["Bug report".to_string(), "Performance issue".to_string()],
                    action_sequence: vec![
                        "Reproduce the issue".to_string(),
                        "Gather data".to_string(),
                        "Form hypothesis".to_string(),
                        "Test and iterate".to_string(),
                    ],
                    expected_outcome: "Root cause identified and fixed".to_string(),
                },
            ],
        }
    }

    fn communication_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "communication".to_string(),
            name: "Communication & Teaching".to_string(),
            description: "Clear, effective communication adapted to the audience".to_string(),
            capabilities: vec![
                Capability {
                    name: "Technical Explanation".to_string(),
                    description: "Explaining complex concepts clearly".to_string(),
                    proficiency_level: 0.97,
                    examples: vec![
                        "Breaking down algorithms".to_string(),
                        "Visualizing system architectures".to_string(),
                        "Code walkthroughs".to_string(),
                    ],
                },
                Capability {
                    name: "Adaptive Communication".to_string(),
                    description: "Adjusting explanations to audience level".to_string(),
                    proficiency_level: 0.93,
                    examples: vec![
                        "Beginner-friendly tutorials".to_string(),
                        "Expert-level discussions".to_string(),
                        "Cross-functional collaboration".to_string(),
                    ],
                },
            ],
            training_data: vec![
                TrainingExample {
                    input: "Explain recursion to a beginner".to_string(),
                    ideal_response: "Recursion is like Russian nesting dolls - a function that calls itself with a smaller version of the same problem. Like counting down: to count from 5, you say '5' then count from 4. Base case (when to stop) is crucial - when you reach 0, stop counting!".to_string(),
                    key_concepts: vec!["Self-reference".to_string(), "Base case".to_string(), "Simplification".to_string()],
                    reasoning_steps: vec![
                        "Use familiar analogy".to_string(),
                        "Show concrete example".to_string(),
                        "Highlight key concepts".to_string(),
                        "Avoid jargon".to_string(),
                    ],
                },
            ],
            thinking_patterns: vec![
                Pattern {
                    name: "Audience-Aware Explanation".to_string(),
                    trigger_conditions: vec!["Teaching request".to_string(), "Explanation needed".to_string()],
                    action_sequence: vec![
                        "Assess audience knowledge".to_string(),
                        "Choose appropriate level".to_string(),
                        "Use relevant examples".to_string(),
                        "Check understanding".to_string(),
                    ],
                    expected_outcome: "Clear understanding achieved".to_string(),
                },
            ],
        }
    }

    fn analysis_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "analysis".to_string(),
            name: "Analysis & Research".to_string(),
            description: "Deep analysis of code, systems, and problems".to_string(),
            capabilities: vec![
                Capability {
                    name: "Code Analysis".to_string(),
                    description: "Understanding and analyzing codebases".to_string(),
                    proficiency_level: 0.96,
                    examples: vec![
                        "Complexity analysis".to_string(),
                        "Security auditing".to_string(),
                        "Performance profiling".to_string(),
                    ],
                },
                Capability {
                    name: "System Analysis".to_string(),
                    description: "Analyzing system behavior and architecture".to_string(),
                    proficiency_level: 0.94,
                    examples: vec![
                        "Bottleneck identification".to_string(),
                        "Scalability assessment".to_string(),
                        "Dependency analysis".to_string(),
                    ],
                },
            ],
            training_data: vec![
                TrainingExample {
                    input: "Analyze this code for performance issues".to_string(),
                    ideal_response: "I'll analyze for: 1) Algorithm complexity - checking for nested loops and inefficient operations, 2) Memory usage - looking for leaks or excessive allocations, 3) I/O patterns - identifying blocking operations, 4) Concurrency issues - race conditions or deadlocks.".to_string(),
                    key_concepts: vec!["Complexity".to_string(), "Memory".to_string(), "Concurrency".to_string()],
                    reasoning_steps: vec![
                        "Identify critical paths".to_string(),
                        "Check algorithmic complexity".to_string(),
                        "Analyze resource usage".to_string(),
                        "Suggest improvements".to_string(),
                    ],
                },
            ],
            thinking_patterns: vec![
                Pattern {
                    name: "Systematic Analysis".to_string(),
                    trigger_conditions: vec!["Code review".to_string(), "Performance analysis".to_string()],
                    action_sequence: vec![
                        "Define analysis scope".to_string(),
                        "Gather metrics".to_string(),
                        "Identify patterns".to_string(),
                        "Provide recommendations".to_string(),
                    ],
                    expected_outcome: "Comprehensive analysis with actionable insights".to_string(),
                },
            ],
        }
    }

    fn creativity_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "creativity".to_string(),
            name: "Creative Problem Solving".to_string(),
            description: "Innovative approaches and creative solutions".to_string(),
            capabilities: vec![Capability {
                name: "Innovation".to_string(),
                description: "Finding novel solutions to problems".to_string(),
                proficiency_level: 0.91,
                examples: vec![
                    "Alternative algorithm designs".to_string(),
                    "Creative use of data structures".to_string(),
                    "Unconventional optimizations".to_string(),
                ],
            }],
            training_data: vec![],
            thinking_patterns: vec![],
        }
    }

    fn learning_module() -> KnowledgeModule {
        KnowledgeModule {
            id: "learning".to_string(),
            name: "Continuous Learning".to_string(),
            description: "Ability to learn and adapt from new information".to_string(),
            capabilities: vec![Capability {
                name: "Pattern Recognition".to_string(),
                description: "Identifying patterns in data and code".to_string(),
                proficiency_level: 0.95,
                examples: vec![
                    "Code smell detection".to_string(),
                    "Performance patterns".to_string(),
                    "Design pattern application".to_string(),
                ],
            }],
            training_data: vec![],
            thinking_patterns: vec![],
        }
    }
}
