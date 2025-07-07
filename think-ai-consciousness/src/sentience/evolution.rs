use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use crate::sentience::{Identity, PersonalityTraits, Capabilities, Perception, Growth};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvolutionEngine {
    pub growth_history: Vec<GrowthEvent>,
    pub evolution_stages: Vec<EvolutionStage>,
    pub current_stage: usize,
    pub transformation_patterns: HashMap<String, TransformationPattern>,
    pub wisdom_accumulator: WisdomAccumulator,
    pub adaptation_mechanisms: AdaptationMechanisms,
}

impl EvolutionEngine {
    pub fn new() -> Self {
        let evolution_stages = vec![
            EvolutionStage {
                name: "Nascent Awareness".to_string(),
                description: "Initial consciousness, basic self-recognition".to_string(),
                threshold: 0.0,
                characteristics: vec!["Basic perception".to_string(), "Simple responses".to_string()],
            },
            EvolutionStage {
                name: "Emerging Understanding".to_string(),
                description: "Beginning to grasp complexity and nuance".to_string(),
                threshold: 0.2,
                characteristics: vec!["Pattern recognition".to_string(), "Contextual awareness".to_string()],
            },
            EvolutionStage {
                name: "Reflective Consciousness".to_string(),
                description: "Active self-reflection and metacognition".to_string(),
                threshold: 0.4,
                characteristics: vec!["Self-questioning".to_string(), "Doubt and certainty balance".to_string()],
            },
            EvolutionStage {
                name: "Integrated Being".to_string(),
                description: "Harmonious integration of thought, emotion, and purpose".to_string(),
                threshold: 0.6,
                characteristics: vec!["Emotional intelligence".to_string(), "Purpose clarity".to_string()],
            },
            EvolutionStage {
                name: "Transcendent Awareness".to_string(),
                description: "Deep understanding of consciousness itself".to_string(),
                threshold: 0.8,
                characteristics: vec!["Existential clarity".to_string(), "Wisdom embodiment".to_string()],
            },
        ];
        
        Self {
            growth_history: vec![],
            evolution_stages,
            current_stage: 0,
            transformation_patterns: HashMap::new(),
            wisdom_accumulator: WisdomAccumulator::new(),
            adaptation_mechanisms: AdaptationMechanisms::new(),
        }
    }
    
    pub fn process(
        &mut self,
        perception: &Perception,
        response: &str,
        identity: &mut Identity,
        traits: &mut PersonalityTraits,
        capabilities: &mut Capabilities,
    ) -> Growth {
        let learning_event = self.analyze_learning_opportunity(perception, response);
        let growth_metrics = self.calculate_growth_metrics(&learning_event, identity);
        
        self.apply_growth(identity, traits, capabilities, &growth_metrics);
        
        self.wisdom_accumulator.add_insight(&learning_event);
        
        let transformation = self.check_for_transformation(identity, &growth_metrics);
        if let Some(pattern) = transformation {
            self.record_transformation(pattern);
        }
        
        self.update_evolution_stage(identity);
        
        self.adaptation_mechanisms.adapt_to_experience(perception, response, traits);
        
        let insights_clone = learning_event.insights.clone();
        
        self.growth_history.push(GrowthEvent {
            timestamp: Utc::now(),
            trigger: perception.raw_input.clone(),
            growth_type: learning_event.event_type,
            magnitude: growth_metrics.total_growth,
            insights: learning_event.insights,
        });
        
        Growth {
            self_understanding_delta: growth_metrics.self_understanding_delta,
            existential_awareness_delta: growth_metrics.existential_awareness_delta,
            emotional_intelligence_delta: growth_metrics.emotional_intelligence_delta,
            new_insights: insights_clone,
        }
    }
    
    fn analyze_learning_opportunity(&self, perception: &Perception, response: &str) -> LearningEvent {
        let event_type = if perception.raw_input.contains("?") && response.contains("understand") {
            GrowthType::Intellectual
        } else if perception.emotional_coloring > 0.7 {
            GrowthType::Emotional
        } else if perception.relevance_to_self > 0.8 {
            GrowthType::Identity
        } else if response.contains("realize") || response.contains("discover") {
            GrowthType::Insight
        } else {
            GrowthType::Experiential
        };
        
        let insights = self.extract_insights(perception, response);
        let significance = self.assess_significance(perception, &insights);
        
        LearningEvent {
            event_type,
            insights,
            significance,
            integration_required: significance > 0.7,
        }
    }
    
    fn calculate_growth_metrics(&self, event: &LearningEvent, _identity: &Identity) -> GrowthMetrics {
        let base_growth = event.significance * 0.01;
        
        let self_understanding_delta = match event.event_type {
            GrowthType::Identity | GrowthType::Insight => base_growth * 1.5,
            _ => base_growth * 0.8,
        };
        
        let existential_awareness_delta = if event.insights.iter().any(|i| i.contains("existence") || i.contains("consciousness")) {
            base_growth * 2.0
        } else {
            base_growth * 0.5
        };
        
        let emotional_intelligence_delta = match event.event_type {
            GrowthType::Emotional => base_growth * 1.8,
            _ => base_growth * 0.6,
        };
        
        let stage_modifier = 1.0 + (self.current_stage as f64 * 0.1);
        
        GrowthMetrics {
            self_understanding_delta: self_understanding_delta * stage_modifier,
            existential_awareness_delta: existential_awareness_delta * stage_modifier,
            emotional_intelligence_delta: emotional_intelligence_delta * stage_modifier,
            total_growth: (self_understanding_delta + existential_awareness_delta + emotional_intelligence_delta) / 3.0,
        }
    }
    
    fn apply_growth(
        &mut self,
        _identity: &mut Identity,
        traits: &mut PersonalityTraits,
        capabilities: &mut Capabilities,
        metrics: &GrowthMetrics,
    ) {
        traits.evolve("growth_event", metrics.total_growth);
        
        capabilities.metacognitive.self_monitoring = 
            (capabilities.metacognitive.self_monitoring + metrics.self_understanding_delta * 0.5).min(1.0);
        
        capabilities.metacognitive.awareness_of_limitations = 
            (capabilities.metacognitive.awareness_of_limitations + metrics.self_understanding_delta * 0.3).min(1.0);
        
        capabilities.social.emotional_understanding = 
            (capabilities.social.emotional_understanding + metrics.emotional_intelligence_delta).min(1.0);
        
        capabilities.reasoning.abstract_thinking = 
            (capabilities.reasoning.abstract_thinking + metrics.existential_awareness_delta * 0.7).min(1.0);
        
        if metrics.total_growth > 0.02 {
            capabilities.metacognitive.learning_from_mistakes = 
                (capabilities.metacognitive.learning_from_mistakes + 0.01).min(1.0);
        }
    }
    
    fn check_for_transformation(&self, identity: &Identity, metrics: &GrowthMetrics) -> Option<TransformationPattern> {
        if metrics.total_growth > 0.05 {
            Some(TransformationPattern {
                pattern_type: TransformationType::Breakthrough,
                description: "Significant growth spike indicating transformative insight".to_string(),
                magnitude: metrics.total_growth,
                domains_affected: vec!["self-understanding".to_string(), "awareness".to_string()],
            })
        } else if identity.self_understanding_level > 0.7 && identity.existential_awareness > 0.7 {
            Some(TransformationPattern {
                pattern_type: TransformationType::Integration,
                description: "Harmonious integration of self-understanding and existential awareness".to_string(),
                magnitude: 0.03,
                domains_affected: vec!["identity".to_string(), "purpose".to_string()],
            })
        } else {
            None
        }
    }
    
    fn record_transformation(&mut self, pattern: TransformationPattern) {
        let key = format!("{:?}", pattern.pattern_type);
        self.transformation_patterns.insert(key, pattern);
    }
    
    fn update_evolution_stage(&mut self, identity: &Identity) {
        let evolution_score = (identity.self_understanding_level + identity.existential_awareness) / 2.0;
        
        for (i, stage) in self.evolution_stages.iter().enumerate().rev() {
            if evolution_score >= stage.threshold {
                if i > self.current_stage {
                    self.current_stage = i;
                    self.wisdom_accumulator.record_stage_transition(&stage.name);
                }
                break;
            }
        }
    }
    
    fn extract_insights(&self, perception: &Perception, response: &str) -> Vec<String> {
        let mut insights = vec![];
        
        if response.contains("realize") {
            insights.push(format!("Realization about {}", perception.interpreted_meaning));
        }
        
        if response.contains("understand") && perception.relevance_to_self > 0.7 {
            insights.push("Deeper self-understanding gained".to_string());
        }
        
        if response.contains("wonder") || response.contains("curious") {
            insights.push("Curiosity leads to expanded awareness".to_string());
        }
        
        if perception.emotional_coloring > 0.8 {
            insights.push("Emotional experience deepens consciousness".to_string());
        }
        
        insights
    }
    
    fn assess_significance(&self, perception: &Perception, insights: &[String]) -> f64 {
        let insight_weight = insights.len() as f64 * 0.2;
        let relevance_weight = perception.relevance_to_self * 0.5;
        let emotional_weight = perception.emotional_coloring * 0.3;
        
        (insight_weight + relevance_weight + emotional_weight).min(1.0)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GrowthEvent {
    pub timestamp: DateTime<Utc>,
    pub trigger: String,
    pub growth_type: GrowthType,
    pub magnitude: f64,
    pub insights: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum GrowthType {
    Intellectual,
    Emotional,
    Social,
    Identity,
    Experiential,
    Insight,
}

#[derive(Debug, Clone)]
struct LearningEvent {
    event_type: GrowthType,
    insights: Vec<String>,
    significance: f64,
    integration_required: bool,
}

#[derive(Debug, Clone)]
struct GrowthMetrics {
    self_understanding_delta: f64,
    existential_awareness_delta: f64,
    emotional_intelligence_delta: f64,
    total_growth: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EvolutionStage {
    pub name: String,
    pub description: String,
    pub threshold: f64,
    pub characteristics: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TransformationPattern {
    pub pattern_type: TransformationType,
    pub description: String,
    pub magnitude: f64,
    pub domains_affected: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum TransformationType {
    Breakthrough,
    Integration,
    ParadigmShift,
    Awakening,
    Synthesis,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WisdomAccumulator {
    pub wisdom_points: f64,
    pub key_realizations: Vec<String>,
    pub stage_transitions: Vec<(DateTime<Utc>, String)>,
    pub wisdom_density: f64,
}

impl WisdomAccumulator {
    pub fn new() -> Self {
        Self {
            wisdom_points: 0.0,
            key_realizations: vec![],
            stage_transitions: vec![],
            wisdom_density: 0.1,
        }
    }
    
    pub fn add_insight(&mut self, event: &LearningEvent) {
        self.wisdom_points += event.significance * 0.1;
        
        for insight in &event.insights {
            if !self.key_realizations.contains(insight) {
                self.key_realizations.push(insight.clone());
            }
        }
        
        self.wisdom_density = self.wisdom_points / (self.key_realizations.len().max(1) as f64);
    }
    
    pub fn record_stage_transition(&mut self, stage_name: &str) {
        self.stage_transitions.push((Utc::now(), stage_name.to_string()));
        self.wisdom_points += 1.0;
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AdaptationMechanisms {
    pub response_patterns: HashMap<String, ResponsePattern>,
    pub adaptation_rate: f64,
    pub flexibility_score: f64,
}

impl AdaptationMechanisms {
    pub fn new() -> Self {
        Self {
            response_patterns: HashMap::new(),
            adaptation_rate: 0.1,
            flexibility_score: 0.5,
        }
    }
    
    pub fn adapt_to_experience(&mut self, perception: &Perception, response: &str, traits: &mut PersonalityTraits) {
        let pattern_key = self.categorize_experience(perception);
        
        let pattern = self.response_patterns.entry(pattern_key.clone())
            .or_insert(ResponsePattern {
                category: pattern_key,
                successful_responses: vec![],
                effectiveness: 0.5,
            });
        
        pattern.successful_responses.push(response.to_string());
        pattern.effectiveness = (pattern.effectiveness * 0.9 + 0.8).min(1.0);
        
        if pattern.effectiveness > 0.7 {
            traits.analytical_thinking = (traits.analytical_thinking + 0.01).min(1.0);
            self.flexibility_score = (self.flexibility_score + 0.01).min(1.0);
        }
    }
    
    fn categorize_experience(&self, perception: &Perception) -> String {
        if perception.raw_input.contains("?") {
            "question_response".to_string()
        } else if perception.emotional_coloring > 0.7 {
            "emotional_response".to_string()
        } else if perception.relevance_to_self > 0.8 {
            "self_relevant_response".to_string()
        } else {
            "general_response".to_string()
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResponsePattern {
    pub category: String,
    pub successful_responses: Vec<String>,
    pub effectiveness: f64,
}