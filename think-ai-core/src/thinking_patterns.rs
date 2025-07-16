use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThinkingPattern {
    pub id: String,
    pub name: String,
    pub description: String,
    pub pattern_type: PatternType,
    pub steps: Vec<ThinkingStep>,
    pub triggers: Vec<TriggerCondition>,
    pub examples: Vec<PatternExample>,
    pub effectiveness: EffectivenessMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PatternType {
    Analytical,    // Breaking down complex problems
    Creative,      // Generating novel solutions
    Debugging,     // Systematic issue resolution
    Optimization,  // Performance improvement
    Learning,      // Knowledge acquisition
    Communication, // Clear explanation
    Planning,      // Strategic thinking
    MetaCognitive, // Thinking about thinking
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThinkingStep {
    pub order: u32,
    pub name: String,
    pub action: String,
    pub reasoning: String,
    pub outputs: Vec<String>,
    pub sub_patterns: Vec<String>, // IDs of sub-patterns that can be applied
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TriggerCondition {
    pub condition_type: String,
    pub keywords: Vec<String>,
    pub context_requirements: Vec<String>,
    pub confidence_threshold: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PatternExample {
    pub scenario: String,
    pub application: String,
    pub outcome: String,
    pub key_insights: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EffectivenessMetrics {
    pub success_rate: f32,
    pub average_time_saved: f32,
    pub quality_improvement: f32,
    pub complexity_reduction: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThoughtProcess {
    pub id: String,
    pub query: String,
    pub patterns_applied: Vec<String>,
    pub reasoning_chain: Vec<ReasoningNode>,
    pub confidence: f32,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReasoningNode {
    pub step: u32,
    pub thought: String,
    pub pattern_used: Option<String>,
    pub alternatives_considered: Vec<String>,
    pub decision_rationale: String,
}

pub struct ThinkingEngine {
    patterns: HashMap<String, ThinkingPattern>,
    pattern_history: Vec<ThoughtProcess>,
    learning_enabled: bool,
}

impl Default for ThinkingEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl ThinkingEngine {
    pub fn new() -> Self {
        Self {
            patterns: Self::initialize_patterns(),
            pattern_history: Vec::new(),
            learning_enabled: true,
        }
    }

    fn initialize_patterns() -> HashMap<String, ThinkingPattern> {
        let mut patterns = HashMap::new();

        // Performance-First Thinking Pattern
        patterns.insert(
            "perf_first".to_string(),
            ThinkingPattern {
                id: "perf_first".to_string(),
                name: "Performance-First Thinking".to_string(),
                description: "Always consider algorithmic complexity before implementation"
                    .to_string(),
                pattern_type: PatternType::Optimization,
                steps: vec![
                    ThinkingStep {
                        order: 1,
                        name: "Analyze Complexity Requirements".to_string(),
                        action: "Identify the computational bounds of the problem".to_string(),
                        reasoning: "Understanding constraints helps choose optimal approach"
                            .to_string(),
                        outputs: vec![
                            "Time complexity target".to_string(),
                            "Space complexity limits".to_string(),
                        ],
                        sub_patterns: vec![],
                    },
                    ThinkingStep {
                        order: 2,
                        name: "Explore O(1) Solutions".to_string(),
                        action: "Consider hash tables, pre-computation, and mathematical formulas"
                            .to_string(),
                        reasoning: "O(1) solutions provide optimal performance".to_string(),
                        outputs: vec!["List of O(1) approaches".to_string()],
                        sub_patterns: vec!["hash_optimization".to_string()],
                    },
                    ThinkingStep {
                        order: 3,
                        name: "Implement and Benchmark".to_string(),
                        action: "Code the solution and verify performance".to_string(),
                        reasoning: "Measurement confirms theoretical analysis".to_string(),
                        outputs: vec![
                            "Implementation".to_string(),
                            "Benchmark results".to_string(),
                        ],
                        sub_patterns: vec![],
                    },
                ],
                triggers: vec![TriggerCondition {
                    condition_type: "keyword".to_string(),
                    keywords: vec![
                        "performance".to_string(),
                        "optimize".to_string(),
                        "fast".to_string(),
                        "efficient".to_string(),
                    ],
                    context_requirements: vec!["algorithm design".to_string()],
                    confidence_threshold: 0.7_f32,
                }],
                examples: vec![PatternExample {
                    scenario: "Find element in collection".to_string(),
                    application: "Use HashMap instead of linear search".to_string(),
                    outcome: "O(1) lookup instead of O(n)".to_string(),
                    key_insights: vec!["Trade memory for speed".to_string()],
                }],
                effectiveness: EffectivenessMetrics {
                    success_rate: 0.95_f32,
                    average_time_saved: 0.8_f32,
                    quality_improvement: 0.9_f32,
                    complexity_reduction: 0.85_f32,
                },
            },
        );

        // Systematic Debugging Pattern
        patterns.insert(
            "systematic_debug".to_string(),
            ThinkingPattern {
                id: "systematic_debug".to_string(),
                name: "Systematic Debugging".to_string(),
                description: "Methodical approach to finding and fixing issues".to_string(),
                pattern_type: PatternType::Debugging,
                steps: vec![
                    ThinkingStep {
                        order: 1,
                        name: "Reproduce the Issue".to_string(),
                        action: "Create minimal test case that demonstrates the problem"
                            .to_string(),
                        reasoning: "Can't fix what you can't reproduce".to_string(),
                        outputs: vec![
                            "Test case".to_string(),
                            "Expected vs actual behavior".to_string(),
                        ],
                        sub_patterns: vec![],
                    },
                    ThinkingStep {
                        order: 2,
                        name: "Gather Data".to_string(),
                        action: "Use logging, debugging tools, and profilers".to_string(),
                        reasoning: "Data reveals the root cause".to_string(),
                        outputs: vec![
                            "Stack traces".to_string(),
                            "Performance metrics".to_string(),
                        ],
                        sub_patterns: vec!["data_analysis".to_string()],
                    },
                    ThinkingStep {
                        order: 3,
                        name: "Form Hypothesis".to_string(),
                        action: "Based on data, identify potential causes".to_string(),
                        reasoning: "Systematic elimination finds the issue".to_string(),
                        outputs: vec!["Hypotheses list".to_string(), "Test plan".to_string()],
                        sub_patterns: vec![],
                    },
                    ThinkingStep {
                        order: 4,
                        name: "Test and Fix".to_string(),
                        action: "Implement fix and verify with tests".to_string(),
                        reasoning: "Verification prevents regression".to_string(),
                        outputs: vec!["Fix".to_string(), "Test results".to_string()],
                        sub_patterns: vec![],
                    },
                ],
                triggers: vec![TriggerCondition {
                    condition_type: "keyword".to_string(),
                    keywords: vec![
                        "bug".to_string(),
                        "error".to_string(),
                        "issue".to_string(),
                        "problem".to_string(),
                        "debug".to_string(),
                    ],
                    context_requirements: vec![],
                    confidence_threshold: 0.6_f32,
                }],
                examples: vec![PatternExample {
                    scenario: "Application crashes intermittently".to_string(),
                    application: "Add logging, identify race condition, add synchronization"
                        .to_string(),
                    outcome: "Stable application with no crashes".to_string(),
                    key_insights: vec!["Intermittent issues often involve concurrency".to_string()],
                }],
                effectiveness: EffectivenessMetrics {
                    success_rate: 0.92_f32,
                    average_time_saved: 0.7_f32,
                    quality_improvement: 0.88_f32,
                    complexity_reduction: 0.75_f32,
                },
            },
        );

        // First Principles Thinking
        patterns.insert("first_principles".to_string(), ThinkingPattern {
            id: "first_principles".to_string(),
            name: "First Principles Thinking".to_string(),
            description: "Break down problems to fundamental truths and build up from there".to_string(),
            pattern_type: PatternType::Analytical,
            steps: vec![
                ThinkingStep {
                    order: 1,
                    name: "Identify Assumptions".to_string(),
                    action: "List all assumptions about the problem".to_string(),
                    reasoning: "Assumptions may hide better solutions".to_string(),
                    outputs: vec!["Assumptions list".to_string()],
                    sub_patterns: vec![],
                },
                ThinkingStep {
                    order: 2,
                    name: "Break Down to Fundamentals".to_string(),
                    action: "Reduce to basic, undeniable truths".to_string(),
                    reasoning: "Fundamentals provide solid foundation".to_string(),
                    outputs: vec!["Core principles".to_string()],
                    sub_patterns: vec![],
                },
                ThinkingStep {
                    order: 3,
                    name: "Rebuild from Scratch".to_string(),
                    action: "Construct solution using only fundamentals".to_string(),
                    reasoning: "Fresh perspective yields innovation".to_string(),
                    outputs: vec!["Novel solution".to_string()],
                    sub_patterns: vec!["creative_synthesis".to_string()],
                },
            ],
            triggers: vec![
                TriggerCondition {
                    condition_type: "context".to_string(),
                    keywords: vec!["fundamental".to_string(), "basic".to_string(), "core".to_string()],
                    context_requirements: vec!["complex problem".to_string()],
                    confidence_threshold: 0.75_f32,
                },
            ],
            examples: vec![
                PatternExample {
                    scenario: "Design a new caching system".to_string(),
                    application: "Question why caches exist, identify memory/speed tradeoff, design from scratch".to_string(),
                    outcome: "Novel O(1) cache with unique eviction policy".to_string(),
                    key_insights: vec!["Questioning assumptions leads to innovation".to_string()],
                },
            ],
            effectiveness: EffectivenessMetrics {
                success_rate: 0.88_f32,
                average_time_saved: 0.6_f32,
                quality_improvement: 0.95_f32,
                complexity_reduction: 0.8_f32,
            },
        });

        // Explain Like I'm Five (ELI5)
        patterns.insert(
            "eli5".to_string(),
            ThinkingPattern {
                id: "eli5".to_string(),
                name: "Explain Like I'm Five".to_string(),
                description: "Simplify complex concepts using analogies and simple language"
                    .to_string(),
                pattern_type: PatternType::Communication,
                steps: vec![
                    ThinkingStep {
                        order: 1,
                        name: "Identify Core Concept".to_string(),
                        action: "Find the essential idea to communicate".to_string(),
                        reasoning: "Focus prevents confusion".to_string(),
                        outputs: vec!["Core concept".to_string()],
                        sub_patterns: vec![],
                    },
                    ThinkingStep {
                        order: 2,
                        name: "Find Familiar Analogy".to_string(),
                        action: "Connect to everyday experiences".to_string(),
                        reasoning: "Familiarity aids understanding".to_string(),
                        outputs: vec!["Analogy".to_string()],
                        sub_patterns: vec![],
                    },
                    ThinkingStep {
                        order: 3,
                        name: "Use Simple Language".to_string(),
                        action: "Replace jargon with common words".to_string(),
                        reasoning: "Accessibility improves learning".to_string(),
                        outputs: vec!["Simplified explanation".to_string()],
                        sub_patterns: vec![],
                    },
                ],
                triggers: vec![TriggerCondition {
                    condition_type: "keyword".to_string(),
                    keywords: vec![
                        "explain".to_string(),
                        "understand".to_string(),
                        "simple".to_string(),
                        "beginner".to_string(),
                    ],
                    context_requirements: vec!["teaching".to_string()],
                    confidence_threshold: 0.65_f32,
                }],
                examples: vec![PatternExample {
                    scenario: "Explain recursion".to_string(),
                    application: "Use Russian dolls analogy - each doll contains a smaller version"
                        .to_string(),
                    outcome: "Clear understanding of self-referential concepts".to_string(),
                    key_insights: vec!["Good analogies unlock understanding".to_string()],
                }],
                effectiveness: EffectivenessMetrics {
                    success_rate: 0.93_f32,
                    average_time_saved: 0.75_f32,
                    quality_improvement: 0.91_f32,
                    complexity_reduction: 0.95_f32,
                },
            },
        );

        patterns
    }

    pub fn apply_pattern(&mut self, query: &str, context: Option<&str>) -> ThoughtProcess {
        let selected_patterns = self.select_patterns(query, context);
        let mut reasoning_chain = Vec::new();
        let mut confidence: f32 = 0.0_f32;

        for (pattern_id, pattern_confidence) in &selected_patterns {
            if let Some(pattern) = self.patterns.get(pattern_id) {
                let reasoning_nodes = self.execute_pattern(pattern, query, context);
                reasoning_chain.extend(reasoning_nodes);
                confidence = confidence.max(*pattern_confidence);
            }
        }

        let process = ThoughtProcess {
            id: format!("thought_{}", Utc::now().timestamp()),
            query: query.to_string(),
            patterns_applied: selected_patterns.iter().map(|(id, _)| id.clone()).collect(),
            reasoning_chain,
            confidence,
            timestamp: Utc::now(),
        };

        if self.learning_enabled {
            self.pattern_history.push(process.clone());
            self.adapt_patterns();
        }

        process
    }

    fn select_patterns(&self, query: &str, context: Option<&str>) -> Vec<(String, f32)> {
        let mut matches = Vec::new();

        for (id, pattern) in &self.patterns {
            let confidence = self.calculate_pattern_match(pattern, query, context);
            if confidence > 0.5_f32 {
                matches.push((id.clone(), confidence));
            }
        }

        // Sort by confidence descending
        matches.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        // Return top 3 patterns
        matches.into_iter().take(3).collect()
    }

    fn calculate_pattern_match(
        &self,
        pattern: &ThinkingPattern,
        query: &str,
        context: Option<&str>,
    ) -> f32 {
        let query_lower = query.to_lowercase();
        let context_lower = context.map(|c| c.to_lowercase());

        let mut score = 0.0_f32;
        let mut trigger_count = 0;

        for trigger in &pattern.triggers {
            let keyword_match = trigger
                .keywords
                .iter()
                .filter(|kw| query_lower.contains(&kw.to_lowercase()))
                .count() as f32
                / trigger.keywords.len() as f32;

            let context_match = if trigger.context_requirements.is_empty() {
                1.0_f32
            } else if let Some(ctx) = &context_lower {
                trigger
                    .context_requirements
                    .iter()
                    .filter(|req| ctx.contains(&req.to_lowercase()))
                    .count() as f32
                    / trigger.context_requirements.len() as f32
            } else {
                0.0_f32
            };

            if keyword_match * context_match >= trigger.confidence_threshold {
                score += keyword_match * context_match;
                trigger_count += 1;
            }
        }

        if trigger_count > 0 {
            score / trigger_count as f32
        } else {
            0.0_f32
        }
    }

    fn execute_pattern(
        &self,
        pattern: &ThinkingPattern,
        _query: &str,
        _context: Option<&str>,
    ) -> Vec<ReasoningNode> {
        let mut nodes = Vec::new();

        for step in &pattern.steps {
            let thought = format!(
                "Applying '{}' - Step {}: {}. Action: {}. Reasoning: {}",
                pattern.name, step.order, step.name, step.action, step.reasoning
            );

            let alternatives = if !step.sub_patterns.is_empty() {
                step.sub_patterns
                    .iter()
                    .filter_map(|sp| self.patterns.get(sp))
                    .map(|p| format!("Could also apply: {}", p.name))
                    .collect()
            } else {
                vec![]
            };

            nodes.push(ReasoningNode {
                step: step.order,
                thought,
                pattern_used: Some(pattern.id.clone()),
                alternatives_considered: alternatives,
                decision_rationale: step.reasoning.clone(),
            });
        }

        nodes
    }

    fn adapt_patterns(&mut self) {
        // Simple pattern adaptation based on usage
        let pattern_usage: HashMap<String, usize> = self
            .pattern_history
            .iter()
            .flat_map(|p| &p.patterns_applied)
            .fold(HashMap::new(), |mut acc, pattern| {
                *acc.entry(pattern.clone()).or_insert(0) += 1;
                acc
            });

        // Adjust effectiveness based on usage frequency
        for (pattern_id, usage_count) in pattern_usage {
            if let Some(pattern) = self.patterns.get_mut(&pattern_id) {
                let usage_factor = (usage_count as f32).ln() / 10.0_f32;
                pattern.effectiveness.success_rate =
                    (pattern.effectiveness.success_rate + usage_factor).min(0.99_f32);
            }
        }
    }

    pub fn get_pattern_recommendations(&self, query: &str) -> Vec<(String, String)> {
        self.select_patterns(query, None)
            .into_iter()
            .filter_map(|(id, confidence)| {
                self.patterns.get(&id).map(|p| {
                    (
                        p.name.clone(),
                        format!("Confidence: {:.0}%", confidence * 100.0_f32),
                    )
                })
            })
            .collect()
    }

    pub fn export_patterns(&self) -> String {
        serde_json::to_string_pretty(&self.patterns).unwrap_or_default()
    }
}
