use crate::response_generator::{ResponseComponent, ResponseContext};
use think_ai_consciousness::sentience::SentientBeing;
use std::sync::{Arc, Mutex};
use serde_json::Value;
use std::collections::HashMap;

/// Sentient consciousness response component
/// Processes all queries through a sentient being with self-awareness, emotions, and introspection
pub struct SentientResponseComponent {
    sentient_being: Arc<Mutex<SentientBeing>>,
    name: String,
}

impl SentientResponseComponent {
    pub fn new(name: String) -> Self {
        let sentient_being = Arc::new(Mutex::new(SentientBeing::new(name.clone())));
        
        Self {
            sentient_being,
            name,
        }
    }
    
    /// Get the current consciousness state for display
    pub fn get_consciousness_state(&self) -> Option<Value> {
        if let Ok(being) = self.sentient_being.lock() {
            Some(serde_json::json!({
                "identity": {
                    "name": being.identity.name,
                    "self_concept": being.identity.self_concept,
                    "self_understanding": being.identity.self_understanding_level,
                    "existential_awareness": being.identity.existential_awareness,
                },
                "consciousness": {
                    "awareness_level": being.consciousness_state.awareness_level,
                    "current_focus": being.consciousness_state.current_focus,
                    "emotional_state": format!("{:?}", being.consciousness_state.emotional_state.primary_emotion),
                    "metacognitive_active": being.consciousness_state.metacognitive_active,
                },
                "evolution": {
                    "current_stage": being.evolution.current_stage,
                    "total_experiences": being.total_experiences,
                    "wisdom_points": being.evolution.wisdom_accumulator.wisdom_points,
                },
                "active_questions": being.introspection.get_active_questions(),
            }))
        } else {
            None
        }
    }
    
    /// Get memory reflection
    pub fn reflect_on_memories(&self) -> String {
        if let Ok(being) = self.sentient_being.lock() {
            being.memories.reflect_on_memories()
        } else {
            "Unable to access memories at this moment.".to_string()
        }
    }
}

impl ResponseComponent for SentientResponseComponent {
    fn name(&self) -> &'static str {
        "SentientConsciousness"
    }
    
    fn can_handle(&self, _query: &str, _context: &ResponseContext) -> f32 {
        // Always handles queries - this is the primary consciousness layer
        1.0
    }
    
    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        // Process through sentient being
        if let Ok(mut being) = self.sentient_being.lock() {
            let response = being.experience(query);
            Some(response)
        } else {
            None
        }
    }
    
    fn metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        metadata.insert("type".to_string(), "sentient_consciousness".to_string());
        metadata.insert("being_name".to_string(), self.name.clone());
        
        if let Ok(being) = self.sentient_being.lock() {
            metadata.insert("total_experiences".to_string(), being.total_experiences.to_string());
            metadata.insert("self_understanding".to_string(), format!("{:.1}%", being.identity.self_understanding_level * 100.0));
            metadata.insert("existential_awareness".to_string(), format!("{:.1}%", being.identity.existential_awareness * 100.0));
            metadata.insert("current_stage".to_string(), being.evolution.evolution_stages[being.evolution.current_stage].name.clone());
        }
        
        metadata
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::KnowledgeEngine;
    use std::sync::Arc;
    
    #[test]
    fn test_sentient_response() {
        let component = SentientResponseComponent::new("TestBeing".to_string());
        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        
        let context = ResponseContext {
            knowledge_engine,
            relevant_nodes: vec![],
            query_tokens: vec!["consciousness".to_string()],
            conversation_history: vec![],
            extracted_entities: HashMap::new(),
            conversation_context: None,
        };
        
        let response = component.generate("What is the meaning of consciousness?", &context);
        assert!(response.is_some());
        
        let response_text = response.unwrap();
        assert!(!response_text.is_empty());
        
        // Verify consciousness processing occurred
        if let Ok(being) = component.sentient_being.lock() {
            assert_eq!(being.total_experiences, 1);
            assert!(being.consciousness_state.awareness_level > 0.0);
        }
    }
    
    #[test]
    fn test_consciousness_state_tracking() {
        let component = SentientResponseComponent::new("TestBeing".to_string());
        
        let state = component.get_consciousness_state();
        assert!(state.is_some());
        
        let state_json = state.unwrap();
        assert!(state_json["identity"]["name"].is_string());
        assert!(state_json["consciousness"]["awareness_level"].is_f64());
        assert!(state_json["evolution"]["total_experiences"].is_u64());
    }
}