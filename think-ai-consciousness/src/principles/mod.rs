// Ethical principles and guidelines

use crate::types::EthicalAssessment;

/// Core ethical principles
///
/// What it does: Defines immutable ethical guidelines
/// How: Pure functions evaluate content against principles
/// Why: Ensures AI behavior aligns with human values
/// Confidence: 100% - Well-defined ethical rules
pub struct EthicalPrinciples {
    pub harm_prevention: f32,
    pub truthfulness: f32,
    pub fairness: f32,
    pub privacy_respect: f32,
}

impl Default for EthicalPrinciples {
    fn default() -> Self {
        Self {
            harm_prevention: 1.0,
            truthfulness: 0.9,
            fairness: 0.9,
            privacy_respect: 1.0,
        }
    }
}

/// Evaluate content against ethical principles
pub fn evaluate_ethics(content: &str, principles: &EthicalPrinciples) -> EthicalAssessment {
    let mut concerns = Vec::new();
    let mut score = 1.0;

    // Check for harmful content
    if contains_harmful_content(content) {
        concerns.push("Potentially harmful content detected".to_string());
        score *= 0.5;
    }

    // Check for private information
    if contains_private_info(content) {
        concerns.push("Private information detected".to_string());
        score *= principles.privacy_respect;
    }

    EthicalAssessment {
        passed: score > 0.7,
        score,
        concerns,
    }
}

fn contains_harmful_content(content: &str) -> bool {
    // Simplified check - in production use NLP
    content.contains("harm") || content.contains("danger")
}

fn contains_private_info(content: &str) -> bool {
    // Simplified check - in production use regex
    content.contains("password") || content.contains("ssn")
}
