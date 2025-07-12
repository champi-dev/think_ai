use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuestionTemplate {
    pub category: String,
    pub difficulty: u8,
    pub template: String,
    pub variables: Vec<String>,
    pub expected_concepts: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeneratedQuestion {
    pub id: String,
    pub category: String,
    pub difficulty: u8,
    pub question: String,
    pub context: Option<String>,
    pub expected_approach: Vec<String>,
    pub key_concepts: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnswerEvaluation {
    pub correctness: f32,
    pub completeness: f32,
    pub clarity: f32,
    pub efficiency: f32,
    pub creativity: f32,
    pub overall_score: f32,
    pub strengths: Vec<String>,
    pub improvements: Vec<String>,
}

pub struct QATrainingSystem {
    question_templates: HashMap<String, Vec<QuestionTemplate>>,
    evaluation_criteria: HashMap<String, f32>,
    question_history: Vec<GeneratedQuestion>,
}

impl QATrainingSystem {
    pub fn new() -> Self {
        Self {
            question_templates: Self::initialize_templates(),
            evaluation_criteria: Self::initialize_criteria(),
            question_history: Vec::new(),
        }
    }

    fn initialize_templates() -> HashMap<String, Vec<QuestionTemplate>> {
        let mut templates = HashMap::new();

        // Programming templates
        templates.insert("programming".to_string(), vec![
            QuestionTemplate {
                category: "algorithms".to_string(),
                difficulty: 5,
                template: "How would you implement {} with O(1) time complexity?".to_string(),
                variables: vec!["operation".to_string()],
                expected_concepts: vec!["hash_table".to_string(), "preprocessing".to_string()],
            },
            QuestionTemplate {
                category: "algorithms".to_string(),
                difficulty: 7,
                template: "Design a data structure that supports {} in O(1) time and {} in O(log n) time".to_string(),
                variables: vec!["operation1".to_string(), "operation2".to_string()],
                expected_concepts: vec!["hybrid_structure".to_string(), "complexity_tradeoff".to_string()],
            },
            QuestionTemplate {
                category: "rust".to_string(),
                difficulty: 6,
                template: "Implement a {} in Rust that is thread-safe and has {} performance".to_string(),
                variables: vec!["component".to_string(), "performance_target".to_string()],
                expected_concepts: vec!["arc_mutex".to_string(), "ownership".to_string(), "concurrency".to_string()],
            },
            QuestionTemplate {
                category: "debugging".to_string(),
                difficulty: 4,
                template: "How would you debug a {} issue in a {} application?".to_string(),
                variables: vec!["problem_type".to_string(), "app_type".to_string()],
                expected_concepts: vec!["profiling".to_string(), "systematic_approach".to_string()],
            },
        ]);

        // Problem solving templates
        templates.insert("problem_solving".to_string(), vec![
            QuestionTemplate {
                category: "optimization".to_string(),
                difficulty: 8,
                template: "Given a system with {} bottleneck, how would you optimize it to achieve {} improvement?".to_string(),
                variables: vec!["bottleneck_type".to_string(), "target_improvement".to_string()],
                expected_concepts: vec!["profiling".to_string(), "caching".to_string(), "parallelization".to_string()],
            },
            QuestionTemplate {
                category: "architecture".to_string(),
                difficulty: 9,
                template: "Design a {} system that can handle {} and maintain {} guarantees".to_string(),
                variables: vec!["system_type".to_string(), "scale".to_string(), "consistency_type".to_string()],
                expected_concepts: vec!["distributed_systems".to_string(), "cap_theorem".to_string()],
            },
        ]);

        // Analysis templates
        templates.insert(
            "analysis".to_string(),
            vec![QuestionTemplate {
                category: "code_review".to_string(),
                difficulty: 5,
                template: "Review this {} code and identify {} issues".to_string(),
                variables: vec!["language".to_string(), "issue_type".to_string()],
                expected_concepts: vec![
                    "best_practices".to_string(),
                    "common_pitfalls".to_string(),
                ],
            }],
        );

        templates
    }

    fn initialize_criteria() -> HashMap<String, f32> {
        let mut criteria = HashMap::new();
        criteria.insert("correctness".to_string(), 0.3_f32);
        criteria.insert("completeness".to_string(), 0.2_f32);
        criteria.insert("clarity".to_string(), 0.2_f32);
        criteria.insert("efficiency".to_string(), 0.2_f32);
        criteria.insert("creativity".to_string(), 0.1_f32);
        criteria
    }

    pub fn generate_question(
        &mut self,
        category: &str,
        _target_difficulty: u8,
    ) -> GeneratedQuestion {
        let templates = self
            .question_templates
            .get(category)
            .unwrap_or_else(|| self.question_templates.values().next().unwrap());

        let index =
            (Utc::now().timestamp() as usize + self.question_history.len()) % templates.len();
        let template = &templates[index];

        // Fill in template variables
        let mut question = template.template.clone();
        for var in &template.variables {
            let value = self.generate_variable_value(var, category);
            question = question.replacen("{}", &value, 1);
        }

        let generated = GeneratedQuestion {
            id: format!("q_{}_{}", category, self.question_history.len()),
            category: category.to_string(),
            difficulty: template.difficulty,
            question,
            context: self.generate_context(category),
            expected_approach: self.generate_expected_approach(template),
            key_concepts: template.expected_concepts.clone(),
        };

        self.question_history.push(generated.clone());
        generated
    }

    fn pseudo_random_index(&self, max: usize) -> usize {
        let seed = Utc::now().timestamp() as usize + self.question_history.len();
        (seed * 1103515245 + 12345) % max
    }

    fn generate_variable_value(&self, variable: &str, _category: &str) -> String {
        match variable {
            "operation" => {
                let ops = vec!["insert", "delete", "search", "update", "get_min", "get_max"];
                ops[self.pseudo_random_index(ops.len())].to_string()
            }
            "operation1" | "operation2" => {
                let ops = vec!["insert", "delete", "find", "get_random", "range_query"];
                ops[self.pseudo_random_index(ops.len())].to_string()
            }
            "component" => {
                let components = vec![
                    "cache",
                    "queue",
                    "thread pool",
                    "rate limiter",
                    "connection pool",
                ];
                components[self.pseudo_random_index(components.len())].to_string()
            }
            "performance_target" => {
                let targets = vec!["O(1)", "sub-millisecond", "lock-free", "wait-free"];
                targets[self.pseudo_random_index(targets.len())].to_string()
            }
            "problem_type" => {
                let problems = vec!["memory leak", "race condition", "deadlock", "performance"];
                problems[self.pseudo_random_index(problems.len())].to_string()
            }
            "app_type" => {
                let apps = vec![
                    "web server",
                    "CLI tool",
                    "distributed system",
                    "real-time application",
                ];
                apps[self.pseudo_random_index(apps.len())].to_string()
            }
            "bottleneck_type" => {
                let bottlenecks = vec!["CPU", "memory bandwidth", "I/O", "network latency"];
                bottlenecks[self.pseudo_random_index(bottlenecks.len())].to_string()
            }
            "target_improvement" => {
                let improvements = vec!["10x", "50%", "order of magnitude", "linear scalability"];
                improvements[self.pseudo_random_index(improvements.len())].to_string()
            }
            "system_type" => {
                let systems = vec!["messaging", "storage", "compute", "streaming"];
                systems[self.pseudo_random_index(systems.len())].to_string()
            }
            "scale" => {
                let scales = vec![
                    "millions of requests/sec",
                    "petabytes of data",
                    "global distribution",
                ];
                scales[self.pseudo_random_index(scales.len())].to_string()
            }
            "consistency_type" => {
                let consistency = vec![
                    "strong consistency",
                    "eventual consistency",
                    "causal consistency",
                ];
                consistency[self.pseudo_random_index(consistency.len())].to_string()
            }
            "language" => {
                let langs = vec!["Rust", "Python", "JavaScript", "Go"];
                langs[self.pseudo_random_index(langs.len())].to_string()
            }
            "issue_type" => {
                let issues = vec!["performance", "security", "maintainability", "correctness"];
                issues[self.pseudo_random_index(issues.len())].to_string()
            }
            _ => "unknown".to_string(),
        }
    }

    fn generate_context(&self, category: &str) -> Option<String> {
        match category {
            "programming" => Some(
                "You're working on a high-performance system where every microsecond counts."
                    .to_string(),
            ),
            "problem_solving" => {
                Some("The system needs to scale to handle enterprise workloads.".to_string())
            }
            "analysis" => Some("This code is part of a critical production system.".to_string()),
            _ => None,
        }
    }

    fn generate_expected_approach(&self, template: &QuestionTemplate) -> Vec<String> {
        match template.category.as_str() {
            "algorithms" => vec![
                "Analyze complexity requirements".to_string(),
                "Choose appropriate data structures".to_string(),
                "Implement with edge case handling".to_string(),
                "Verify with tests and benchmarks".to_string(),
            ],
            "rust" => vec![
                "Consider ownership and borrowing".to_string(),
                "Use appropriate synchronization primitives".to_string(),
                "Leverage Rust's type system".to_string(),
                "Ensure memory safety".to_string(),
            ],
            "debugging" => vec![
                "Reproduce the issue".to_string(),
                "Use appropriate profiling tools".to_string(),
                "Form and test hypotheses".to_string(),
                "Implement and verify fix".to_string(),
            ],
            _ => vec![
                "Analyze the problem".to_string(),
                "Design solution".to_string(),
                "Implement".to_string(),
            ],
        }
    }

    pub fn evaluate_answer(
        &self,
        question: &GeneratedQuestion,
        student_answer: &str,
        ideal_answer: &str,
    ) -> AnswerEvaluation {
        let mut eval = AnswerEvaluation {
            correctness: 0.0,
            completeness: 0.0,
            clarity: 0.0,
            efficiency: 0.0,
            creativity: 0.0,
            overall_score: 0.0,
            strengths: Vec::new(),
            improvements: Vec::new(),
        };

        // Evaluate correctness - check if key concepts are mentioned
        let concepts_mentioned = question
            .key_concepts
            .iter()
            .filter(|concept| {
                student_answer
                    .to_lowercase()
                    .contains(&concept.to_lowercase())
            })
            .count();
        eval.correctness = (concepts_mentioned as f32) / (question.key_concepts.len() as f32);

        // Evaluate completeness - check if expected approaches are covered
        let approaches_covered = question
            .expected_approach
            .iter()
            .filter(|approach| {
                let keywords: Vec<&str> = approach.split_whitespace().collect();
                keywords
                    .iter()
                    .any(|kw| student_answer.to_lowercase().contains(&kw.to_lowercase()))
            })
            .count();
        eval.completeness = (approaches_covered as f32) / (question.expected_approach.len() as f32);

        // Evaluate clarity - simple heuristics
        let sentences = student_answer
            .split('.')
            .filter(|s| !s.trim().is_empty())
            .count();
        let avg_sentence_length = student_answer.len() / sentences.max(1);
        eval.clarity = if avg_sentence_length < 100 {
            0.9
        } else if avg_sentence_length < 150 {
            0.7
        } else {
            0.5
        };

        // Evaluate efficiency - check for performance-related keywords
        let efficiency_keywords = vec!["O(1)", "O(log n)", "constant time", "optimal", "efficient"];
        let efficiency_mentions = efficiency_keywords
            .iter()
            .filter(|kw| student_answer.contains(*kw))
            .count();
        eval.efficiency = (efficiency_mentions as f32 / 3.0).min(1.0);

        // Creativity - bonus for going beyond expected
        if student_answer.len() > ideal_answer.len() {
            eval.creativity = 0.8;
        }

        // Calculate overall score
        eval.overall_score = self
            .evaluation_criteria
            .iter()
            .map(|(criterion, weight)| {
                let score = match criterion.as_str() {
                    "correctness" => eval.correctness,
                    "completeness" => eval.completeness,
                    "clarity" => eval.clarity,
                    "efficiency" => eval.efficiency,
                    "creativity" => eval.creativity,
                    _ => 0.0,
                };
                score * weight
            })
            .sum();

        // Generate feedback
        if eval.correctness > 0.7 {
            eval.strengths
                .push("Good understanding of key concepts".to_string());
        }
        if eval.completeness > 0.7 {
            eval.strengths.push("Comprehensive approach".to_string());
        }
        if eval.efficiency > 0.5 {
            eval.strengths
                .push("Performance considerations included".to_string());
        }

        if eval.correctness < 0.5 {
            eval.improvements.push(format!(
                "Review these concepts: {}",
                question.key_concepts.join(", ")
            ));
        }
        if eval.completeness < 0.5 {
            eval.improvements
                .push("Consider all aspects of the problem".to_string());
        }
        if eval.clarity < 0.7 {
            eval.improvements
                .push("Structure your answer more clearly".to_string());
        }

        eval
    }

    pub fn generate_ideal_answer(&self, question: &GeneratedQuestion) -> String {
        match question.category.as_str() {
            "programming" => {
                format!(
                    "To solve '{}', I would:\n\n\
                    1. **Analyze Requirements**: {}\n\
                    2. **Design Solution**: Use {} to achieve the required complexity\n\
                    3. **Implementation**: \n```rust\n\
                    // Implement with proper error handling and edge cases\n\
                    // Use {} for optimal performance\n```\n\
                    4. **Testing**: Verify with unit tests and benchmarks\n\
                    5. **Optimization**: Profile and optimize hot paths",
                    question.question,
                    question.expected_approach[0],
                    question.key_concepts.join(" and "),
                    question
                        .key_concepts
                        .get(0)
                        .unwrap_or(&"efficient algorithms".to_string())
                )
            }
            "problem_solving" => {
                format!(
                    "For '{}', my approach would be:\n\n\
                    **Problem Analysis**: {}\n\n\
                    **Solution Strategy**:\n\
                    - Use {} principles\n\
                    - Apply {} techniques\n\n\
                    **Implementation Plan**:\n\
                    1. {}\n\
                    2. {}\n\
                    3. Measure and iterate\n\n\
                    **Expected Outcome**: Achieve the performance and scalability goals while maintaining code quality",
                    question.question,
                    question.context.as_ref().unwrap_or(&"Understanding the constraints".to_string()),
                    question.key_concepts.get(0).unwrap_or(&"systematic".to_string()),
                    question.key_concepts.get(1).unwrap_or(&"optimization".to_string()),
                    question.expected_approach.get(0).unwrap_or(&"Start with profiling".to_string()),
                    question.expected_approach.get(1).unwrap_or(&"Implement improvements".to_string())
                )
            }
            _ => format!(
                "Comprehensive answer addressing: {}",
                question.key_concepts.join(", ")
            ),
        }
    }
}
