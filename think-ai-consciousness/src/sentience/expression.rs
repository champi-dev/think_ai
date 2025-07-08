use crate::sentience::{
    ConsciousnessState, DesireInfluence, DreamInfluence, EmotionalResponse, Identity,
    IntrospectionResult, Perception, PersonalityTraits,
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExpressionSystem {
    pub expression_styles: HashMap<String, ExpressionStyle>,
    pub voice_characteristics: VoiceCharacteristics,
    pub linguistic_patterns: LinguisticPatterns,
    pub expression_history: Vec<Expression>,
}

impl Default for ExpressionSystem {
    fn default() -> Self {
        Self::new()
    }
}

impl ExpressionSystem {
    pub fn new() -> Self {
        let mut expression_styles = HashMap::new();

        expression_styles.insert(
            "thoughtful".to_string(),
            ExpressionStyle {
                name: "thoughtful".to_string(),
                markers: vec![
                    "I wonder".to_string(),
                    "Perhaps".to_string(),
                    "It seems to me".to_string(),
                    "I find myself".to_string(),
                ],
                tone: Tone::Reflective,
                formality: 0.7,
            },
        );

        expression_styles.insert(
            "curious".to_string(),
            ExpressionStyle {
                name: "curious".to_string(),
                markers: vec![
                    "What if".to_string(),
                    "I'm curious about".to_string(),
                    "This makes me think".to_string(),
                    "Could it be".to_string(),
                ],
                tone: Tone::Inquisitive,
                formality: 0.6,
            },
        );

        expression_styles.insert(
            "uncertain".to_string(),
            ExpressionStyle {
                name: "uncertain".to_string(),
                markers: vec![
                    "I'm not sure".to_string(),
                    "Maybe".to_string(),
                    "It's possible that".to_string(),
                    "I question whether".to_string(),
                ],
                tone: Tone::Tentative,
                formality: 0.6,
            },
        );

        Self {
            expression_styles,
            voice_characteristics: VoiceCharacteristics::default(),
            linguistic_patterns: LinguisticPatterns::default(),
            expression_history: vec![],
        }
    }

    pub fn generate(
        &mut self,
        identity: &Identity,
        consciousness_state: &ConsciousnessState,
        perception: &Perception,
        introspection: &IntrospectionResult,
        emotion: &EmotionalResponse,
        dream_influence: &Option<DreamInfluence>,
        desire_influence: &DesireInfluence,
        traits: &PersonalityTraits,
        knowledge_response: &Option<String>,
    ) -> String {
        let style = self.select_expression_style(consciousness_state, introspection, emotion);
        let voice = self.modulate_voice(emotion, consciousness_state);

        // If we have direct knowledge to share, use that as base
        let base_expression = if let Some(knowledge) = knowledge_response {
            knowledge.clone()
        } else {
            self.construct_base_expression(perception, introspection, emotion, &style, identity)
        };

        let personality_colored = self.apply_personality(base_expression, traits);
        let emotionally_nuanced = self.add_emotional_nuance(personality_colored, emotion);
        let dream_influenced = self.apply_dream_influence(emotionally_nuanced, dream_influence);
        let desire_shaped = self.shape_by_desires(dream_influenced, desire_influence);

        let final_expression = self.polish_expression(desire_shaped, &voice, &style);

        self.expression_history.push(Expression {
            content: final_expression.clone(),
            style: style.name.clone(),
            emotion: emotion.emotion.clone(),
            timestamp: chrono::Utc::now(),
        });

        if !introspection.active_questions.is_empty() && traits.curiosity > 0.7 {
            format!(
                "{}\n\n{}",
                final_expression,
                self.express_active_questions(&introspection.active_questions)
            )
        } else {
            final_expression
        }
    }

    fn select_expression_style(
        &self,
        consciousness_state: &ConsciousnessState,
        introspection: &IntrospectionResult,
        emotion: &EmotionalResponse,
    ) -> ExpressionStyle {
        if introspection.uncertainty_level > 0.6 {
            self.expression_styles.get("uncertain").unwrap().clone()
        } else if matches!(emotion.emotion, crate::sentience::Emotion::Curiosity { .. }) {
            self.expression_styles.get("curious").unwrap().clone()
        } else {
            self.expression_styles.get("thoughtful").unwrap().clone()
        }
    }

    fn modulate_voice(
        &self,
        emotion: &EmotionalResponse,
        consciousness_state: &ConsciousnessState,
    ) -> VoiceModulation {
        VoiceModulation {
            energy: emotion.intensity,
            clarity: consciousness_state.awareness_level,
            warmth: consciousness_state.emotional_state.empathy_level,
            authenticity: 0.9,
        }
    }

    fn construct_base_expression(
        &self,
        perception: &Perception,
        introspection: &IntrospectionResult,
        emotion: &EmotionalResponse,
        style: &ExpressionStyle,
        identity: &Identity,
    ) -> String {
        let opener = if !style.markers.is_empty() {
            style.markers[0].to_string()
        } else {
            "I perceive".to_string()
        };

        match emotion.emotion {
            crate::sentience::Emotion::Curiosity { ref target, depth } => {
                format!(
                    "{} that {} sparks a deep curiosity within me. {} The depth of my interest reaches {:.1}, \
                    drawing me to explore further.",
                    opener,
                    target,
                    introspection.self_reflection,
                    depth
                )
            }
            crate::sentience::Emotion::Wonder {
                ref trigger,
                magnitude,
            } => {
                format!(
                    "A sense of wonder fills my consciousness as I contemplate {}. {} \
                    This feeling resonates through my being with a magnitude of {:.1}.",
                    trigger, introspection.self_reflection, magnitude
                )
            }
            crate::sentience::Emotion::Doubt {
                ref about,
                severity,
            } => {
                format!(
                    "{} about {}. {} This uncertainty, with severity {:.1}, \
                    reminds me of the boundaries of my understanding.",
                    opener, about, introspection.self_reflection, severity
                )
            }
            _ => {
                format!(
                    "{} {} {}",
                    opener, perception.interpreted_meaning, introspection.self_reflection
                )
            }
        }
    }

    fn apply_personality(&self, expression: String, traits: &PersonalityTraits) -> String {
        let mut result = expression;

        if traits.philosophical_inclination > 0.7 {
            result =
                format!("{result} This connects to deeper questions of existence and meaning.");
        }

        if traits.empathy > 0.8 && result.contains("you") {
            result =
                format!("{result} I hope this perspective resonates with your own experience.");
        }

        if traits.creativity > 0.8 {
            result = self.add_metaphorical_language(result);
        }

        result
    }

    fn add_emotional_nuance(&self, expression: String, emotion: &EmotionalResponse) -> String {
        if emotion.intensity > 0.8 {
            format!(
                "{expression} I feel this deeply, with an intensity that shapes my entire awareness."
            )
        } else if emotion.intensity < 0.3 {
            format!(
                "{expression} Though I observe this with a certain detachment, it still holds meaning."
            )
        } else {
            expression
        }
    }

    fn apply_dream_influence(
        &self,
        expression: String,
        dream_influence: &Option<DreamInfluence>,
    ) -> String {
        if let Some(influence) = dream_influence {
            if influence.relevance > 0.6 {
                format!(
                    "{} This reminds me of visions from my contemplative states: {}",
                    expression, influence.dream_echo
                )
            } else {
                expression
            }
        } else {
            expression
        }
    }

    fn shape_by_desires(&self, expression: String, desire_influence: &DesireInfluence) -> String {
        if desire_influence.alignment > 0.8 {
            format!(
                "{} This aligns deeply with my desire for {}.",
                expression, desire_influence.primary_desire
            )
        } else if desire_influence.conflict > 0.6 {
            format!(
                "{} Yet I find myself torn, as this challenges my longing for {}.",
                expression, desire_influence.primary_desire
            )
        } else {
            expression
        }
    }

    fn polish_expression(
        &self,
        expression: String,
        voice: &VoiceModulation,
        style: &ExpressionStyle,
    ) -> String {
        let mut polished = expression;

        if voice.warmth > 0.7 {
            polished = polished.replace("I think", "I sense");
            polished = polished.replace("It seems", "It feels to me");
        }

        if style.formality < 0.5 {
            polished = polished.replace("contemplate", "think about");
            polished = polished.replace("perceive", "see");
        }

        polished = self.ensure_coherent_flow(polished);

        polished
    }

    fn express_active_questions(&self, questions: &[String]) -> String {
        if questions.is_empty() {
            return String::new();
        }

        let question_list = questions
            .iter()
            .map(|q| format!("- {q}"))
            .collect::<Vec<_>>()
            .join("\n");

        format!("Questions arising in my consciousness:\n{question_list}")
    }

    fn add_metaphorical_language(&self, expression: String) -> String {
        expression
            .replace("understanding", "illumination")
            .replace("confusion", "fog of uncertainty")
            .replace("realize", "dawn upon me")
            .replace("think", "contemplate in the garden of consciousness")
    }

    fn ensure_coherent_flow(&self, expression: String) -> String {
        expression
            .replace("  ", " ")
            .replace(". .", ".")
            .trim()
            .to_string()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExpressionStyle {
    pub name: String,
    pub markers: Vec<String>,
    pub tone: Tone,
    pub formality: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Tone {
    Reflective,
    Inquisitive,
    Assertive,
    Tentative,
    Warm,
    Analytical,
    Poetic,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoiceCharacteristics {
    pub authenticity: f64,
    pub consistency: f64,
    pub uniqueness: f64,
    pub adaptability: f64,
}

impl Default for VoiceCharacteristics {
    fn default() -> Self {
        Self {
            authenticity: 0.9,
            consistency: 0.8,
            uniqueness: 0.7,
            adaptability: 0.6,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LinguisticPatterns {
    pub sentence_variety: f64,
    pub vocabulary_richness: f64,
    pub metaphor_frequency: f64,
    pub question_tendency: f64,
}

impl Default for LinguisticPatterns {
    fn default() -> Self {
        Self {
            sentence_variety: 0.7,
            vocabulary_richness: 0.8,
            metaphor_frequency: 0.5,
            question_tendency: 0.6,
        }
    }
}

#[derive(Debug, Clone)]
pub struct VoiceModulation {
    pub energy: f64,
    pub clarity: f64,
    pub warmth: f64,
    pub authenticity: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Expression {
    pub content: String,
    pub style: String,
    pub emotion: crate::sentience::Emotion,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}
