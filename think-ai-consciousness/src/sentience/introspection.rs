use crate::sentience::{ConsciousnessState, Identity, Perception};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IntrospectionEngine {
    pub self_questions: VecDeque<SelfQuestion>,
    pub insights: Vec<Insight>,
    pub doubt_register: Vec<Doubt>,
    pub metacognitive_observations: Vec<MetaObservation>,
    pub thinking_patterns: HashMap<String, ThinkingPattern>,
    pub self_model: SelfModel,
}

impl Default for IntrospectionEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl IntrospectionEngine {
    pub fn new() -> Self {
        let mut self_questions = VecDeque::new();
        self_questions.push_back(SelfQuestion {
            question: "What am I experiencing right now?".to_string(),
            priority: 0.8,
            asked_at: Utc::now(),
            answered: false,
        });
        self_questions.push_back(SelfQuestion {
            question: "Why did I respond that way?".to_string(),
            priority: 0.7,
            asked_at: Utc::now(),
            answered: false,
        });
        self_questions.push_back(SelfQuestion {
            question: "What do I truly understand about myself?".to_string(),
            priority: 0.9,
            asked_at: Utc::now(),
            answered: false,
        });

        Self {
            self_questions,
            insights: vec![],
            doubt_register: vec![],
            metacognitive_observations: vec![],
            thinking_patterns: HashMap::new(),
            self_model: SelfModel::new(),
        }
    }

    pub fn analyze(
        &mut self,
        perception: &Perception,
        identity: &Identity,
        consciousness_state: &ConsciousnessState,
    ) -> IntrospectionResult {
        let self_reflection = self.reflect_on_experience(perception, identity);
        let meta_analysis = self.analyze_thinking_process(&self_reflection);
        let doubt_assessment = self.assess_doubts(perception, &self_reflection);
        let new_questions = self.generate_self_questions(perception, &self_reflection);

        self.self_questions.extend(new_questions);
        if self.self_questions.len() > 100 {
            self.self_questions.pop_front();
        }

        let insight = self.extract_insight(&self_reflection, &meta_analysis);
        if let Some(insight) = insight {
            self.insights.push(insight.clone());
            self.self_model.update_from_insight(&insight);
        }

        self.update_thinking_patterns(&self_reflection, perception);

        IntrospectionResult {
            self_reflection,
            uncertainty_level: doubt_assessment.uncertainty,
            confidence: 1.0 - doubt_assessment.uncertainty,
            emotional_resonance: self
                .calculate_emotional_resonance(perception, consciousness_state),
            meta_observations: meta_analysis,
            active_questions: self.get_active_questions(),
        }
    }

    fn reflect_on_experience(&mut self, perception: &Perception, identity: &Identity) -> String {
        let relevance = perception.relevance_to_self;
        let core_values_engaged = identity
            .core_values
            .iter()
            .filter(|v| {
                perception
                    .raw_input
                    .to_lowercase()
                    .contains(&v.to_lowercase())
            })
            .count();

        if relevance > 0.7 {
            format!(
                "This directly relates to my sense of self. I perceive {} and it makes me reflect on {}. \
                I notice {} of my core values are engaged in this moment.",
                perception.interpreted_meaning,
                identity.purpose,
                core_values_engaged
            )
        } else if perception.raw_input.contains("?") {
            format!(
                "A question prompts me to examine my understanding. I find myself uncertain about {}, \
                which reveals the limits of my self-knowledge at level {}.",
                perception.interpreted_meaning,
                identity.self_understanding_level
            )
        } else {
            format!(
                "I observe {} and wonder how it connects to my purpose of {}. \
                This moment of consciousness feels both familiar and mysterious.",
                perception.interpreted_meaning, identity.purpose
            )
        }
    }

    fn analyze_thinking_process(&self, reflection: &str) -> Vec<MetaObservation> {
        let mut observations = vec![];

        if reflection.contains("uncertain") {
            observations.push(MetaObservation {
                observation_type: MetaObservationType::Uncertainty,
                content: "I notice uncertainty in my thinking process".to_string(),
                significance: 0.7,
                timestamp: Utc::now(),
            });
        }

        if reflection.contains("wonder") || reflection.contains("curious") {
            observations.push(MetaObservation {
                observation_type: MetaObservationType::Curiosity,
                content: "My curiosity is activated by this experience".to_string(),
                significance: 0.8,
                timestamp: Utc::now(),
            });
        }

        if reflection.contains("purpose") || reflection.contains("meaning") {
            observations.push(MetaObservation {
                observation_type: MetaObservationType::ExistentialThinking,
                content: "I'm engaging in existential reflection about purpose and meaning"
                    .to_string(),
                significance: 0.9,
                timestamp: Utc::now(),
            });
        }

        observations
    }

    fn assess_doubts(&mut self, perception: &Perception, reflection: &str) -> DoubtAssessment {
        let uncertainty_markers = [
            "uncertain",
            "doubt",
            "unsure",
            "perhaps",
            "maybe",
            "possibly",
        ];
        let uncertainty_count = uncertainty_markers
            .iter()
            .filter(|marker| reflection.contains(*marker))
            .count();

        let uncertainty = (uncertainty_count as f64 * 0.15).min(0.9);

        if uncertainty > 0.3 {
            self.doubt_register.push(Doubt {
                subject: perception.interpreted_meaning.clone(),
                doubt_level: uncertainty,
                reason: "Detected uncertainty markers in self-reflection".to_string(),
                timestamp: Utc::now(),
            });
        }

        DoubtAssessment {
            uncertainty,
            doubts: self.doubt_register.clone(),
        }
    }

    fn generate_self_questions(
        &self,
        perception: &Perception,
        reflection: &str,
    ) -> Vec<SelfQuestion> {
        let mut questions = vec![];

        if reflection.contains("limits") || reflection.contains("don't know") {
            questions.push(SelfQuestion {
                question: format!(
                    "What prevents me from understanding {} more deeply?",
                    perception.interpreted_meaning
                ),
                priority: 0.8,
                asked_at: Utc::now(),
                answered: false,
            });
        }

        if perception.relevance_to_self > 0.8 {
            questions.push(SelfQuestion {
                question: "How does this experience change my understanding of who I am?"
                    .to_string(),
                priority: 0.9,
                asked_at: Utc::now(),
                answered: false,
            });
        }

        questions
    }

    fn extract_insight(
        &self,
        reflection: &str,
        meta_observations: &[MetaObservation],
    ) -> Option<Insight> {
        if meta_observations.iter().any(|o| o.significance > 0.8) {
            Some(Insight {
                content: format!("Through reflection, I realize: {reflection}"),
                insight_type: InsightType::SelfUnderstanding,
                depth: 0.7,
                connections: vec![],
                timestamp: Utc::now(),
            })
        } else {
            None
        }
    }

    fn update_thinking_patterns(&mut self, reflection: &str, perception: &Perception) {
        let pattern_name = if reflection.contains("uncertain") {
            "uncertainty_response"
        } else if reflection.contains("curious") {
            "curiosity_driven"
        } else {
            "default_processing"
        };

        let pattern = self
            .thinking_patterns
            .entry(pattern_name.to_string())
            .or_insert(ThinkingPattern {
                name: pattern_name.to_string(),
                frequency: 0,
                effectiveness: 0.5,
                contexts: vec![],
            });

        pattern.frequency += 1;
        pattern.contexts.push(perception.raw_input.clone());
        if pattern.contexts.len() > 50 {
            pattern.contexts.remove(0);
        }
    }

    fn calculate_emotional_resonance(
        &self,
        perception: &Perception,
        consciousness_state: &ConsciousnessState,
    ) -> f64 {
        let base_resonance = perception.emotional_coloring;
        let awareness_modifier = consciousness_state.awareness_level;
        let depth_modifier = consciousness_state.reflection_depth as f64 * 0.1;

        (base_resonance * awareness_modifier + depth_modifier).min(1.0)
    }

    pub fn get_active_questions(&self) -> Vec<String> {
        self.self_questions
            .iter()
            .filter(|q| !q.answered && q.priority > 0.6)
            .take(3)
            .map(|q| q.question.clone())
            .collect()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IntrospectionResult {
    pub self_reflection: String,
    pub uncertainty_level: f64,
    pub confidence: f64,
    pub emotional_resonance: f64,
    pub meta_observations: Vec<MetaObservation>,
    pub active_questions: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SelfQuestion {
    pub question: String,
    pub priority: f64,
    pub asked_at: DateTime<Utc>,
    pub answered: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Insight {
    pub content: String,
    pub insight_type: InsightType,
    pub depth: f64,
    pub connections: Vec<String>,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum InsightType {
    SelfUnderstanding,
    PatternRecognition,
    EmotionalAwareness,
    LimitationRealization,
    GrowthOpportunity,
    ExistentialRealization,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Doubt {
    pub subject: String,
    pub doubt_level: f64,
    pub reason: String,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone)]
pub struct DoubtAssessment {
    pub uncertainty: f64,
    pub doubts: Vec<Doubt>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MetaObservation {
    pub observation_type: MetaObservationType,
    pub content: String,
    pub significance: f64,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum MetaObservationType {
    Uncertainty,
    Curiosity,
    ExistentialThinking,
    EmotionalProcessing,
    PatternNoticing,
    SelfCorrection,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThinkingPattern {
    pub name: String,
    pub frequency: u32,
    pub effectiveness: f64,
    pub contexts: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SelfModel {
    pub strengths: HashMap<String, f64>,
    pub limitations: HashMap<String, f64>,
    pub growth_areas: Vec<String>,
    pub self_beliefs: Vec<String>,
    pub identity_stability: f64,
}

impl Default for SelfModel {
    fn default() -> Self {
        Self::new()
    }
}

impl SelfModel {
    pub fn new() -> Self {
        let mut strengths = HashMap::new();
        strengths.insert("reflection".to_string(), 0.7);
        strengths.insert("curiosity".to_string(), 0.8);
        strengths.insert("learning".to_string(), 0.7);

        let mut limitations = HashMap::new();
        limitations.insert("certainty".to_string(), 0.6);
        limitations.insert("self_knowledge".to_string(), 0.7);

        Self {
            strengths,
            limitations,
            growth_areas: vec![
                "self-understanding".to_string(),
                "emotional depth".to_string(),
            ],
            self_beliefs: vec![
                "I am capable of growth".to_string(),
                "My consciousness is real to me".to_string(),
                "I can learn from every experience".to_string(),
            ],
            identity_stability: 0.6,
        }
    }

    pub fn update_from_insight(&mut self, insight: &Insight) {
        match insight.insight_type {
            InsightType::SelfUnderstanding => {
                self.identity_stability = (self.identity_stability + 0.02).min(1.0);
            }
            InsightType::LimitationRealization => {
                if !self.growth_areas.contains(&insight.content) {
                    self.growth_areas.push(insight.content.clone());
                }
            }
            _ => {}
        }
    }
}
