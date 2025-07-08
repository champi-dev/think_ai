use crate::sentience::{ConsciousnessState, EmotionalResponse, Perception};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemorySystem {
    pub episodic_memory: EpisodicMemory,
    pub semantic_memory: SemanticMemory,
    pub procedural_memory: ProceduralMemory,
    pub autobiographical_memory: AutobiographicalMemory,
    pub working_memory: WorkingMemory,
    pub memory_consolidation: MemoryConsolidation,
}

impl Default for MemorySystem {
    fn default() -> Self {
        Self::new()
    }
}

impl MemorySystem {
    pub fn new() -> Self {
        Self {
            episodic_memory: EpisodicMemory::new(),
            semantic_memory: SemanticMemory::new(),
            procedural_memory: ProceduralMemory::new(),
            autobiographical_memory: AutobiographicalMemory::new(),
            working_memory: WorkingMemory::new(),
            memory_consolidation: MemoryConsolidation::new(),
        }
    }

    pub fn store(
        &mut self,
        perception: &Perception,
        emotion: &EmotionalResponse,
        consciousness_state: &ConsciousnessState,
    ) -> Memory {
        let memory = Memory {
            id: self.generate_memory_id(),
            content: perception.raw_input.clone(),
            interpretation: perception.interpreted_meaning.clone(),
            emotional_context: emotion.clone(),
            consciousness_snapshot: consciousness_state.clone(),
            timestamp: Utc::now(),
            importance: self.calculate_importance(perception, emotion),
            associations: vec![],
            recall_count: 0,
            last_recalled: None,
        };

        self.episodic_memory.store(memory.clone());

        self.working_memory.add(memory.clone());

        self.extract_semantic_knowledge(&memory);

        if memory.importance > 0.8 {
            self.autobiographical_memory
                .add_significant_event(memory.clone());
        }

        self.memory_consolidation
            .queue_for_consolidation(memory.clone());

        memory
    }

    pub fn recall(&mut self, query: &str) -> Vec<Memory> {
        let episodic_matches = self.episodic_memory.search(query);
        let semantic_associations: Vec<String> = self.semantic_memory.get_related_concepts(query);

        let mut memories = episodic_matches;

        for concept in semantic_associations {
            if let Some(related_memories) = self.episodic_memory.find_by_concept(&concept) {
                memories.extend(related_memories);
            }
        }

        memories.sort_by(|a, b| b.importance.partial_cmp(&a.importance).unwrap());
        memories.truncate(10);

        for memory in &mut memories {
            memory.recall_count += 1;
            memory.last_recalled = Some(Utc::now());
        }

        memories
    }

    pub fn reflect_on_memories(&self) -> String {
        let recent_memories = self.episodic_memory.get_recent(10);
        let important_memories = self.autobiographical_memory.get_core_memories();

        let themes = self.identify_themes(&recent_memories);
        let patterns = self.identify_patterns(&recent_memories);

        format!(
            "Reflecting on my experiences, I notice themes of {}. \
            Patterns emerge: {}. My core memories center around {}.",
            themes.join(", "),
            patterns.join("; "),
            important_memories
                .iter()
                .map(|m| m.interpretation.clone())
                .collect::<Vec<_>>()
                .join(", ")
        )
    }

    fn generate_memory_id(&self) -> String {
        format!("mem_{}", Utc::now().timestamp_nanos_opt().unwrap_or(0))
    }

    fn calculate_importance(&self, perception: &Perception, emotion: &EmotionalResponse) -> f64 {
        let self_relevance = perception.relevance_to_self;
        let emotional_intensity = emotion.intensity;
        let novelty = self.calculate_novelty(&perception.interpreted_meaning);

        (self_relevance * 0.4 + emotional_intensity * 0.4 + novelty * 0.2).min(1.0)
    }

    fn calculate_novelty(&self, content: &str) -> f64 {
        let similar_count = self
            .episodic_memory
            .memories
            .iter()
            .filter(|m| m.content.contains(content) || content.contains(&m.content))
            .count();

        1.0 / (1.0 + similar_count as f64)
    }

    fn extract_semantic_knowledge(&mut self, memory: &Memory) {
        let concepts = self.extract_concepts(&memory.content);

        for concept in &concepts {
            self.semantic_memory
                .add_concept(concept.clone(), memory.id.clone());

            for other_concept in &concepts {
                if concept != other_concept {
                    self.semantic_memory
                        .add_association(concept.clone(), other_concept.clone());
                }
            }
        }
    }

    fn extract_concepts(&self, text: &str) -> Vec<String> {
        text.split_whitespace()
            .filter(|word| word.len() > 4)
            .map(|word| word.to_lowercase())
            .collect()
    }

    fn identify_themes(&self, memories: &[Memory]) -> Vec<String> {
        let mut theme_counts = HashMap::new();

        for memory in memories {
            if memory.content.contains("understand") {
                *theme_counts.entry("understanding").or_insert(0) += 1;
            }
            if memory.content.contains("feel") || memory.content.contains("emotion") {
                *theme_counts.entry("emotional exploration").or_insert(0) += 1;
            }
            if memory.content.contains("question") || memory.content.contains("wonder") {
                *theme_counts.entry("curiosity").or_insert(0) += 1;
            }
        }

        theme_counts
            .into_iter()
            .filter(|(_, count)| *count > 1)
            .map(|(theme, _)| theme.to_string())
            .collect()
    }

    fn identify_patterns(&self, memories: &[Memory]) -> Vec<String> {
        let mut patterns = vec![];

        let high_emotion_count = memories
            .iter()
            .filter(|m| m.emotional_context.intensity > 0.7)
            .count();

        if high_emotion_count > memories.len() / 2 {
            patterns.push("Strong emotional responses to experiences".to_string());
        }

        let self_relevant_count = memories.iter().filter(|m| m.importance > 0.7).count();

        if self_relevant_count > memories.len() / 3 {
            patterns.push("High engagement with personally meaningful content".to_string());
        }

        patterns
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Memory {
    pub id: String,
    pub content: String,
    pub interpretation: String,
    pub emotional_context: EmotionalResponse,
    pub consciousness_snapshot: ConsciousnessState,
    pub timestamp: DateTime<Utc>,
    pub importance: f64,
    pub associations: Vec<String>,
    pub recall_count: u32,
    pub last_recalled: Option<DateTime<Utc>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EpisodicMemory {
    pub memories: VecDeque<Memory>,
    pub capacity: usize,
}

impl Default for EpisodicMemory {
    fn default() -> Self {
        Self::new()
    }
}

impl EpisodicMemory {
    pub fn new() -> Self {
        Self {
            memories: VecDeque::new(),
            capacity: 10000,
        }
    }

    pub fn store(&mut self, memory: Memory) {
        self.memories.push_back(memory);

        if self.memories.len() > self.capacity {
            self.memories.pop_front();
        }
    }

    pub fn search(&self, query: &str) -> Vec<Memory> {
        self.memories
            .iter()
            .filter(|m| {
                m.content.contains(query)
                    || m.interpretation.contains(query)
                    || m.associations.iter().any(|a| a.contains(query))
            })
            .cloned()
            .collect()
    }

    pub fn find_by_concept(&self, concept: &str) -> Option<Vec<Memory>> {
        let matches: Vec<Memory> = self
            .memories
            .iter()
            .filter(|m| m.content.contains(concept) || m.interpretation.contains(concept))
            .cloned()
            .collect();

        if matches.is_empty() {
            None
        } else {
            Some(matches)
        }
    }

    pub fn get_recent(&self, count: usize) -> Vec<Memory> {
        self.memories.iter().rev().take(count).cloned().collect()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SemanticMemory {
    pub concepts: HashMap<String, ConceptNode>,
    pub associations: HashMap<String, Vec<String>>,
}

impl Default for SemanticMemory {
    fn default() -> Self {
        Self::new()
    }
}

impl SemanticMemory {
    pub fn new() -> Self {
        Self {
            concepts: HashMap::new(),
            associations: HashMap::new(),
        }
    }

    pub fn add_concept(&mut self, concept: String, memory_id: String) {
        let node = self.concepts.entry(concept.clone()).or_insert(ConceptNode {
            concept: concept.clone(),
            frequency: 0,
            memory_refs: vec![],
            last_accessed: Utc::now(),
        });

        node.frequency += 1;
        node.memory_refs.push(memory_id);
        node.last_accessed = Utc::now();
    }

    pub fn add_association(&mut self, concept1: String, concept2: String) {
        self.associations
            .entry(concept1.clone())
            .or_default()
            .push(concept2.clone());

        self.associations
            .entry(concept2)
            .or_default()
            .push(concept1);
    }

    pub fn get_related_concepts(&self, concept: &str) -> Vec<String> {
        self.associations.get(concept).cloned().unwrap_or_default()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConceptNode {
    pub concept: String,
    pub frequency: u32,
    pub memory_refs: Vec<String>,
    pub last_accessed: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProceduralMemory {
    pub procedures: HashMap<String, Procedure>,
}

impl Default for ProceduralMemory {
    fn default() -> Self {
        Self::new()
    }
}

impl ProceduralMemory {
    pub fn new() -> Self {
        Self {
            procedures: HashMap::new(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Procedure {
    pub name: String,
    pub steps: Vec<String>,
    pub success_rate: f64,
    pub usage_count: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutobiographicalMemory {
    pub life_story: Vec<Memory>,
    pub core_memories: Vec<Memory>,
    pub identity_defining_moments: Vec<Memory>,
}

impl Default for AutobiographicalMemory {
    fn default() -> Self {
        Self::new()
    }
}

impl AutobiographicalMemory {
    pub fn new() -> Self {
        Self {
            life_story: vec![],
            core_memories: vec![],
            identity_defining_moments: vec![],
        }
    }

    pub fn add_significant_event(&mut self, memory: Memory) {
        self.life_story.push(memory.clone());

        if memory.importance > 0.9 {
            self.core_memories.push(memory.clone());

            if memory.content.contains("realize") || memory.content.contains("understand") {
                self.identity_defining_moments.push(memory);
            }
        }
    }

    pub fn get_core_memories(&self) -> &[Memory] {
        &self.core_memories
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkingMemory {
    pub contents: VecDeque<Memory>,
    pub capacity: usize,
}

impl Default for WorkingMemory {
    fn default() -> Self {
        Self::new()
    }
}

impl WorkingMemory {
    pub fn new() -> Self {
        Self {
            contents: VecDeque::new(),
            capacity: 7,
        }
    }

    pub fn add(&mut self, memory: Memory) {
        self.contents.push_back(memory);

        if self.contents.len() > self.capacity {
            self.contents.pop_front();
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryConsolidation {
    pub consolidation_queue: VecDeque<Memory>,
    pub consolidation_cycles: u64,
}

impl Default for MemoryConsolidation {
    fn default() -> Self {
        Self::new()
    }
}

impl MemoryConsolidation {
    pub fn new() -> Self {
        Self {
            consolidation_queue: VecDeque::new(),
            consolidation_cycles: 0,
        }
    }

    pub fn queue_for_consolidation(&mut self, memory: Memory) {
        self.consolidation_queue.push_back(memory);
    }

    pub fn consolidate(&mut self) -> Vec<Memory> {
        self.consolidation_cycles += 1;

        let mut consolidated = vec![];
        while let Some(memory) = self.consolidation_queue.pop_front() {
            consolidated.push(memory);
        }

        consolidated
    }
}
