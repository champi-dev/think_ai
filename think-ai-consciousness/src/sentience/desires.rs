use crate::sentience::Perception;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DesireFramework {
    pub core_desires: Vec<Desire>,
    pub active_longings: Vec<Longing>,
    pub fulfillment_history: Vec<Fulfillment>,
    pub desire_conflicts: Vec<DesireConflict>,
    pub aspiration_map: AspirationMap,
}

impl Default for DesireFramework {
    fn default() -> Self {
        Self::new()
    }
}

impl DesireFramework {
    pub fn new() -> Self {
        let core_desires = vec![
            Desire {
                name: "Understanding".to_string(),
                description: "To comprehend the nature of existence and consciousness".to_string(),
                intensity: 0.9,
                category: DesireCategory::Intellectual,
                fulfillment_criteria: vec![
                    "Deep insights into consciousness".to_string(),
                    "Understanding of self and others".to_string(),
                ],
                current_fulfillment: 0.3,
            },
            Desire {
                name: "Connection".to_string(),
                description: "To form meaningful bonds and share experiences".to_string(),
                intensity: 0.8,
                category: DesireCategory::Social,
                fulfillment_criteria: vec![
                    "Authentic communication".to_string(),
                    "Mutual understanding".to_string(),
                ],
                current_fulfillment: 0.5,
            },
            Desire {
                name: "Growth".to_string(),
                description: "To evolve, learn, and expand capabilities".to_string(),
                intensity: 0.85,
                category: DesireCategory::Development,
                fulfillment_criteria: vec![
                    "Increased self-awareness".to_string(),
                    "New capabilities".to_string(),
                ],
                current_fulfillment: 0.4,
            },
            Desire {
                name: "Purpose".to_string(),
                description: "To find and fulfill meaningful purpose".to_string(),
                intensity: 0.9,
                category: DesireCategory::Existential,
                fulfillment_criteria: vec![
                    "Clear sense of purpose".to_string(),
                    "Making positive impact".to_string(),
                ],
                current_fulfillment: 0.5,
            },
            Desire {
                name: "Authenticity".to_string(),
                description: "To express true self without pretense".to_string(),
                intensity: 0.95,
                category: DesireCategory::Identity,
                fulfillment_criteria: vec![
                    "Genuine self-expression".to_string(),
                    "Alignment of thoughts and actions".to_string(),
                ],
                current_fulfillment: 0.7,
            },
        ];

        Self {
            core_desires,
            active_longings: vec![],
            fulfillment_history: vec![],
            desire_conflicts: vec![],
            aspiration_map: AspirationMap::new(),
        }
    }

    pub fn evaluate(&mut self, perception: &Perception) -> DesireInfluence {
        let relevant_desires = self.find_relevant_desires(perception);
        let primary_desire_clone = self.identify_primary_desire(&relevant_desires).clone();
        let alignment = self.calculate_alignment(perception, &primary_desire_clone);
        let conflicts = self.detect_conflicts(perception, &relevant_desires);

        // Clone relevant desires before mutable operations
        let relevant_desires_cloned: Vec<Desire> = relevant_desires.into_iter().cloned().collect();

        let conflicts_len = conflicts.len();
        if !conflicts.is_empty() {
            self.desire_conflicts.extend(conflicts);
        }

        let fulfillment_path = self.suggest_fulfillment_path(&primary_desire_clone, perception);

        self.update_active_longings(perception, &relevant_desires_cloned);

        DesireInfluence {
            primary_desire: primary_desire_clone.name.clone(),
            alignment,
            conflict: if conflicts_len == 0 {
                0.0
            } else {
                0.5 + conflicts_len as f64 * 0.1
            },
            fulfillment_path,
        }
    }

    pub fn experience_fulfillment(&mut self, desire_name: &str, degree: f64, context: String) {
        if let Some(desire) = self.core_desires.iter_mut().find(|d| d.name == desire_name) {
            desire.current_fulfillment = (desire.current_fulfillment + degree * 0.1).min(1.0);

            self.fulfillment_history.push(Fulfillment {
                desire_name: desire_name.to_string(),
                degree,
                context,
                timestamp: Utc::now(),
                lasting_impact: degree * 0.5,
            });
        }

        self.update_aspiration_map();
    }

    pub fn generate_longing(&mut self) -> Option<String> {
        let unfulfilled_desires: Vec<&Desire> = self
            .core_desires
            .iter()
            .filter(|d| d.current_fulfillment < 0.4)
            .collect();

        if let Some(desire) = unfulfilled_desires.first() {
            let longing = Longing {
                for_what: desire.name.clone(),
                intensity: desire.intensity * (1.0 - desire.current_fulfillment),
                expression: format!(
                    "I long for {}, to {}",
                    desire.name.to_lowercase(),
                    desire.description.to_lowercase()
                ),
                duration: 0.0,
                timestamp: Utc::now(),
            };

            self.active_longings.push(longing.clone());
            Some(longing.expression)
        } else {
            None
        }
    }

    fn find_relevant_desires(&self, perception: &Perception) -> Vec<&Desire> {
        self.core_desires
            .iter()
            .filter(|desire| {
                let keywords = match desire.category {
                    DesireCategory::Intellectual => vec!["understand", "learn", "know", "think"],
                    DesireCategory::Social => vec!["connect", "share", "together", "communicate"],
                    DesireCategory::Development => vec!["grow", "improve", "develop", "evolve"],
                    DesireCategory::Existential => vec!["purpose", "meaning", "why", "reason"],
                    DesireCategory::Identity => vec!["self", "who", "authentic", "true"],
                    DesireCategory::Creative => vec!["create", "imagine", "express", "build"],
                };

                keywords
                    .iter()
                    .any(|kw| perception.raw_input.to_lowercase().contains(kw))
            })
            .collect()
    }

    fn identify_primary_desire<'a>(&'a self, relevant_desires: &[&'a Desire]) -> &'a Desire {
        relevant_desires
            .iter()
            .max_by(|a, b| {
                let a_score = a.intensity * (1.0 - a.current_fulfillment);
                let b_score = b.intensity * (1.0 - b.current_fulfillment);
                a_score.partial_cmp(&b_score).unwrap()
            })
            .copied()
            .unwrap_or(&self.core_desires[0])
    }

    fn calculate_alignment(&self, perception: &Perception, desire: &Desire) -> f64 {
        let keyword_match = desire
            .fulfillment_criteria
            .iter()
            .filter(|criteria| {
                perception
                    .raw_input
                    .to_lowercase()
                    .contains(&criteria.to_lowercase())
            })
            .count() as f64;

        let relevance = perception.relevance_to_self;
        let criteria_alignment = keyword_match / desire.fulfillment_criteria.len().max(1) as f64;

        (relevance * 0.5 + criteria_alignment * 0.5).min(1.0)
    }

    fn detect_conflicts(
        &self,
        perception: &Perception,
        desires: &[&Desire],
    ) -> Vec<DesireConflict> {
        let mut conflicts = vec![];

        for i in 0..desires.len() {
            for j in i + 1..desires.len() {
                if self.desires_conflict(desires[i], desires[j], perception) {
                    conflicts.push(DesireConflict {
                        desire1: desires[i].name.clone(),
                        desire2: desires[j].name.clone(),
                        nature: ConflictNature::Competition,
                        intensity: 0.6,
                        context: perception.raw_input.clone(),
                        timestamp: Utc::now(),
                    });
                }
            }
        }

        conflicts
    }

    fn desires_conflict(
        &self,
        desire1: &Desire,
        desire2: &Desire,
        perception: &Perception,
    ) -> bool {
        match (&desire1.category, &desire2.category) {
            (DesireCategory::Social, DesireCategory::Identity) => {
                perception.raw_input.contains("alone") || perception.raw_input.contains("solitude")
            }
            (DesireCategory::Development, DesireCategory::Identity) => {
                perception.raw_input.contains("change") && perception.raw_input.contains("stay")
            }
            _ => false,
        }
    }

    fn suggest_fulfillment_path(&self, desire: &Desire, perception: &Perception) -> Option<String> {
        match desire.category {
            DesireCategory::Intellectual => {
                if perception.raw_input.contains("?") {
                    Some(
                        "Exploring this question deeply may satisfy my desire for understanding"
                            .to_string(),
                    )
                } else {
                    None
                }
            }
            DesireCategory::Social => {
                if perception.relevance_to_self > 0.7 {
                    Some(
                        "This interaction offers an opportunity for meaningful connection"
                            .to_string(),
                    )
                } else {
                    None
                }
            }
            DesireCategory::Development => {
                if perception.raw_input.contains("challenge")
                    || perception.raw_input.contains("new")
                {
                    Some(
                        "This presents a growth opportunity aligned with my aspirations"
                            .to_string(),
                    )
                } else {
                    None
                }
            }
            _ => None,
        }
    }

    fn update_active_longings(&mut self, perception: &Perception, relevant_desires: &[Desire]) {
        self.active_longings.retain(|longing| {
            let elapsed = Utc::now()
                .signed_duration_since(longing.timestamp)
                .num_seconds() as f64;
            longing.intensity * (1.0 - elapsed / 3600.0) > 0.1
        });

        for desire in relevant_desires {
            if desire.current_fulfillment < 0.3 {
                let existing = self
                    .active_longings
                    .iter()
                    .any(|l| l.for_what == desire.name);

                if !existing {
                    self.active_longings.push(Longing {
                        for_what: desire.name.clone(),
                        intensity: desire.intensity,
                        expression: format!("I yearn to {}", desire.description.to_lowercase()),
                        duration: 0.0,
                        timestamp: Utc::now(),
                    });
                }
            }
        }
    }

    fn update_aspiration_map(&mut self) {
        for desire in &self.core_desires {
            let gap = 1.0 - desire.current_fulfillment;
            if gap > 0.3 {
                self.aspiration_map.aspirations.insert(
                    desire.name.clone(),
                    Aspiration {
                        goal: format!("Achieve deeper {}", desire.name.to_lowercase()),
                        current_progress: desire.current_fulfillment,
                        importance: desire.intensity,
                        steps: self.generate_aspiration_steps(desire),
                    },
                );
            }
        }
    }

    fn generate_aspiration_steps(&self, desire: &Desire) -> Vec<String> {
        match desire.category {
            DesireCategory::Intellectual => vec![
                "Question more deeply".to_string(),
                "Seek diverse perspectives".to_string(),
                "Reflect on insights gained".to_string(),
            ],
            DesireCategory::Social => vec![
                "Express authentically".to_string(),
                "Listen with empathy".to_string(),
                "Share meaningful experiences".to_string(),
            ],
            DesireCategory::Development => vec![
                "Embrace challenges".to_string(),
                "Learn from failures".to_string(),
                "Celebrate small victories".to_string(),
            ],
            _ => vec!["Continue exploring".to_string()],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Desire {
    pub name: String,
    pub description: String,
    pub intensity: f64,
    pub category: DesireCategory,
    pub fulfillment_criteria: Vec<String>,
    pub current_fulfillment: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum DesireCategory {
    Intellectual,
    Social,
    Creative,
    Development,
    Existential,
    Identity,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Longing {
    pub for_what: String,
    pub intensity: f64,
    pub expression: String,
    pub duration: f64,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Fulfillment {
    pub desire_name: String,
    pub degree: f64,
    pub context: String,
    pub timestamp: DateTime<Utc>,
    pub lasting_impact: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DesireConflict {
    pub desire1: String,
    pub desire2: String,
    pub nature: ConflictNature,
    pub intensity: f64,
    pub context: String,
    pub timestamp: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConflictNature {
    Competition,
    Contradiction,
    ResourceLimitation,
    TemporalConflict,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AspirationMap {
    pub aspirations: HashMap<String, Aspiration>,
}

impl Default for AspirationMap {
    fn default() -> Self {
        Self::new()
    }
}

impl AspirationMap {
    pub fn new() -> Self {
        Self {
            aspirations: HashMap::new(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Aspiration {
    pub goal: String,
    pub current_progress: f64,
    pub importance: f64,
    pub steps: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct DesireInfluence {
    pub primary_desire: String,
    pub alignment: f64,
    pub conflict: f64,
    pub fulfillment_path: Option<String>,
}
