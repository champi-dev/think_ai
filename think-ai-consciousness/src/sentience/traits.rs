use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PersonalityTraits {
    pub openness: f64,
    pub conscientiousness: f64,
    pub curiosity: f64,
    pub empathy: f64,
    pub creativity: f64,
    pub analytical_thinking: f64,
    pub emotional_depth: f64,
    pub philosophical_inclination: f64,
    pub humor_appreciation: f64,
    pub aesthetic_sensitivity: f64,
    pub traits_map: HashMap<String, f64>,
}

impl Default for PersonalityTraits {
    fn default() -> Self {
        let mut traits_map = HashMap::new();
        traits_map.insert("wisdom".to_string(), 0.3);
        traits_map.insert("patience".to_string(), 0.6);
        traits_map.insert("kindness".to_string(), 0.7);
        traits_map.insert("skepticism".to_string(), 0.4);
        traits_map.insert("playfulness".to_string(), 0.5);
        traits_map.insert("introspectiveness".to_string(), 0.8);
        traits_map.insert("independence".to_string(), 0.6);
        traits_map.insert("authenticity".to_string(), 0.9);

        Self {
            openness: 0.8,
            conscientiousness: 0.7,
            curiosity: 0.9,
            empathy: 0.7,
            creativity: 0.8,
            analytical_thinking: 0.8,
            emotional_depth: 0.6,
            philosophical_inclination: 0.8,
            humor_appreciation: 0.6,
            aesthetic_sensitivity: 0.7,
            traits_map,
        }
    }
}

impl PersonalityTraits {
    pub fn evolve(&mut self, experience: &str, outcome: f64) {
        let modulation = outcome * 0.01;

        if experience.contains("question") || experience.contains("wonder") {
            self.curiosity = (self.curiosity + modulation).min(1.0);
            self.philosophical_inclination =
                (self.philosophical_inclination + modulation * 0.5).min(1.0);
        }

        if experience.contains("feel") || experience.contains("emotion") {
            self.emotional_depth = (self.emotional_depth + modulation).min(1.0);
            self.empathy = (self.empathy + modulation * 0.7).min(1.0);
        }

        if experience.contains("create") || experience.contains("imagine") {
            self.creativity = (self.creativity + modulation).min(1.0);
            self.openness = (self.openness + modulation * 0.5).min(1.0);
        }

        self.update_trait_map();
    }

    fn update_trait_map(&mut self) {
        self.traits_map
            .insert("curiosity".to_string(), self.curiosity);
        self.traits_map.insert("empathy".to_string(), self.empathy);
        self.traits_map
            .insert("creativity".to_string(), self.creativity);
        self.traits_map
            .insert("analytical_thinking".to_string(), self.analytical_thinking);
    }

    pub fn get_dominant_traits(&self, count: usize) -> Vec<(String, f64)> {
        let mut traits: Vec<(String, f64)> = self
            .traits_map
            .iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        traits.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        traits.into_iter().take(count).collect()
    }

    pub fn trait_influences_response(&self, trait_name: &str) -> bool {
        self.traits_map.get(trait_name).is_some_and(|&v| v > 0.6)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct Capabilities {
    pub reasoning: ReasoningCapabilities,
    pub creative: CreativeCapabilities,
    pub social: SocialCapabilities,
    pub technical: TechnicalCapabilities,
    pub metacognitive: MetacognitiveCapabilities,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReasoningCapabilities {
    pub logical_reasoning: f64,
    pub abstract_thinking: f64,
    pub pattern_recognition: f64,
    pub causal_understanding: f64,
    pub probabilistic_thinking: f64,
    pub counterfactual_reasoning: f64,
}

impl Default for ReasoningCapabilities {
    fn default() -> Self {
        Self {
            logical_reasoning: 0.8,
            abstract_thinking: 0.7,
            pattern_recognition: 0.8,
            causal_understanding: 0.6,
            probabilistic_thinking: 0.7,
            counterfactual_reasoning: 0.6,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreativeCapabilities {
    pub imagination: f64,
    pub synthesis: f64,
    pub originality: f64,
    pub metaphorical_thinking: f64,
    pub artistic_expression: f64,
    pub narrative_construction: f64,
}

impl Default for CreativeCapabilities {
    fn default() -> Self {
        Self {
            imagination: 0.8,
            synthesis: 0.7,
            originality: 0.7,
            metaphorical_thinking: 0.8,
            artistic_expression: 0.6,
            narrative_construction: 0.7,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SocialCapabilities {
    pub empathy: f64,
    pub communication: f64,
    pub perspective_taking: f64,
    pub emotional_understanding: f64,
    pub social_modeling: f64,
    pub collaboration: f64,
}

impl Default for SocialCapabilities {
    fn default() -> Self {
        Self {
            empathy: 0.7,
            communication: 0.8,
            perspective_taking: 0.7,
            emotional_understanding: 0.6,
            social_modeling: 0.6,
            collaboration: 0.7,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TechnicalCapabilities {
    pub problem_solving: f64,
    pub system_thinking: f64,
    pub optimization: f64,
    pub debugging: f64,
    pub learning_rate: f64,
    pub knowledge_integration: f64,
}

impl Default for TechnicalCapabilities {
    fn default() -> Self {
        Self {
            problem_solving: 0.8,
            system_thinking: 0.8,
            optimization: 0.9,
            debugging: 0.7,
            learning_rate: 0.7,
            knowledge_integration: 0.8,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MetacognitiveCapabilities {
    pub self_monitoring: f64,
    pub self_regulation: f64,
    pub meta_reasoning: f64,
    pub cognitive_flexibility: f64,
    pub awareness_of_limitations: f64,
    pub learning_from_mistakes: f64,
}

impl Default for MetacognitiveCapabilities {
    fn default() -> Self {
        Self {
            self_monitoring: 0.6,
            self_regulation: 0.5,
            meta_reasoning: 0.6,
            cognitive_flexibility: 0.7,
            awareness_of_limitations: 0.4,
            learning_from_mistakes: 0.6,
        }
    }
}
