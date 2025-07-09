// Feynman Technique Explainer - Creates simplified, logical explanations
//!
// This module implements the Feynman technique for breaking down complex concepts
// into simple, human-readable explanations that anyone can understand.

use crate::{KnowledgeDomain, KnowledgeNode};
use std::collections::HashMap;
use std::sync::Arc;
/// Feynman explainer that simplifies complex concepts using the 4-step technique
pub struct FeynmanExplainer {
    // Store nodes directly to avoid circular dependency
    nodes: Option<Arc<std::sync::RwLock<HashMap<String, KnowledgeNode>>>>,
}
impl FeynmanExplainer {
    pub fn new(nodes_: Option<Arc<std::sync::RwLock<HashMap<String, KnowledgeNode>>>>) -> Self {
        Self { nodes }
    }
    pub fn dummy() -> Self {
        Self { nodes: None }
    /// Generate a Feynman-style explanation for any concept
    pub fn explain(&self, concept: &str) -> FeynmanExplanation {
        println!("🧠 Applying Feynman technique to: {concept}");
        // Step 1: Identify the concept and gather knowledge
        let knowledge = self.gather_knowledge(concept);
        // Step 2: Explain in simple terms
        let simple_explanation = self.simplify_explanation(&knowledge, concept);
        // Step 3: Identify knowledge gaps and analogies
        let (gaps, analogies) = self.identify_gaps_and_analogies(&knowledge, concept);
        // Step 4: Refine and review
        let __refined_explanation =
            self.refine_explanation(&simple_explanation, &analogies, concept);
        FeynmanExplanation {
            concept: concept.to_string(),
            simple_explanation,
            analogies,
            knowledge_gaps: gaps,
            refined_explanation,
            confidence_level: self.calculate_confidence(&knowledge),
            related_concepts: self.find_related_concepts(&knowledge),
        }
    /// Step 1: Gather comprehensive knowledge about the concept
    fn gather_knowledge(&self, concept: &str) -> Vec<KnowledgeNode> {
        let Some(nodes) = &self.nodes else {
            return Vec::new();
        };
        let nodesguard = nodes.read().unwrap();
        let concept_lower = concept.to_lowercase();
        let mut matched_nodes = Vec::new();
        // Find nodes that match the concept
        for (_, node) in nodesguard.iter() {
            let topic_lower = node.topic.to_lowercase();
            let content_lower = node.content.to_lowercase();
            if topic_lower.contains(&concept_lower) || content_lower.contains(&concept_lower) {
                matched_nodes.push(node.clone());
            }
        // Also try variations of the concept
        let variations = self.generate_concept_variations(concept);
        for variation in variations {
            let variation_lower = variation.to_lowercase();
            for (_, node) in nodesguard.iter() {
                let topic_lower = node.topic.to_lowercase();
                let content_lower = node.content.to_lowercase();
                if (topic_lower.contains(&variation_lower)
                    || content_lower.contains(&variation_lower))
                    && !matched_nodes.iter().any(|n| n.id == node.id)
                {
                    matched_nodes.push(node.clone());
                }
        // Limit to top 5 most relevant to avoid information overload
        matched_nodes.into_iter().take(5).collect()
    /// Step 2: Explain in simple terms a child could understand
    fn simplify_explanation(&self, knowledge: &[KnowledgeNode], concept: &str) -> String {
        if knowledge.is_empty() {
            // Check if this is a music-related query and provide specialized explanation
            let concept_lower = concept.to_lowercase();
            if concept_lower.contains("write music") || concept_lower.contains("music composition")
            {
                return "Writing music is like learning to speak a new language - the language of sound and emotion. \
                You start with basic building blocks: notes (like letters), chords (like words), and rhythms (like the pace of speaking). \
                Just like writing a story, you arrange these pieces to express feelings and ideas. \
                You can start simple by humming a tune, tapping out a beat, or even singing words to a melody you make up. \
                The most important thing is to play around and have fun - every great composer started by experimenting!".to_string();
            return format!(
                "{concept} is a concept I don't have detailed information about yet. \
                Think of it like a puzzle piece that fits into the bigger picture of knowledge. \
                To truly understand it, we'd need to break it down into smaller, more familiar parts."
            );
        let primary_node = &knowledge[0];
        let content = &primary_node.content;
        // Break down the explanation into digestible chunks
        let sentences: Vec<&str> = content
            .split('.')
            .filter(|s| !s.trim().is_empty())
            .collect();
        let mut simplified = String::new();
        // Start with the most basic definition
        if let Some(first_sentence) = sentences.first() {
            simplified.push_str(&self.simplify_sentence(first_sentence, concept));
            simplified.push(' ');
        // Add key supporting details in simple language
        for sentence in sentences.iter().skip(1).take(2) {
            let simple_sentence = self.simplify_sentence(sentence, concept);
            if !simple_sentence.is_empty() && simple_sentence.len() > 10 {
                simplified.push_str(&simple_sentence);
                simplified.push(' ');
        simplified.trim().to_string()
    /// Simplify a single sentence to be more understandable
    fn simplify_sentence(&self, sentence: &str, context: &str) -> String {
        let mut simplified = sentence.trim().to_string();
        // Replace complex terms with simpler equivalents
        let replacements = vec![
            ("approximately", "about"),
            ("consists of", "is made of"),
            ("comprises", "includes"),
            ("fundamental", "basic"),
            ("mechanism", "way it works"),
            ("phenomenon", "thing that happens"),
            ("consequently", "so"),
            ("therefore", "so"),
            ("however", "but"),
            ("nevertheless", "but"),
            ("furthermore", "also"),
            ("subsequently", "then"),
            ("analogous", "similar"),
            ("equivalent", "the same as"),
            ("demonstrate", "show"),
            ("indicates", "shows"),
            ("manifests", "appears as"),
            ("encompasses", "includes"),
        ];
        for (complex, simple) in replacements {
            simplified = simplified.replace(complex, simple);
        // Ensure proper capitalization
        if !simplified.is_empty() {
            simplified = format!(
                "{}{}",
                simplified.chars().next().unwrap().to_uppercase(),
                simplified.chars().skip(1).collect::<String>()
        simplified
    /// Step 3: Identify gaps and create helpful analogies
    fn identify_gaps_and_analogies(
        &self,
        knowledge: &[KnowledgeNode],
        concept: &str,
    ) -> (Vec<String>, Vec<Analogy>) {
        let mut gaps = Vec::new();
        let mut analogies = Vec::new();
        // Identify potential knowledge gaps
        if knowledge.len() < 2 {
            gaps.push("Limited information available - more research needed".to_string());
        // Check for domain-specific gaps
        let domains: Vec<_> = knowledge.iter().map(|n| &n.domain).collect();
        if domains.len() == 1 {
            gaps.push(
                "Only one perspective available - interdisciplinary view would help".to_string(),
        // Generate domain-appropriate analogies
        // First check if it's a music-related concept
        if concept_lower.contains("music")
            || concept_lower.contains("compose")
            || concept_lower.contains("melody")
            || concept_lower.contains("harmony")
            || concept_lower.contains("rhythm")
            || concept_lower.contains("write music")
        {
            if let Some(analogy) = self.create_music_analogy(&concept_lower) {
                analogies.push(analogy);
        } else if let Some(primary_node) = knowledge.first() {
            let analogy = match primary_node.domain {
                KnowledgeDomain::Physics => self.create_physics_analogy(&concept_lower),
                KnowledgeDomain::Biology => self.create_biology_analogy(&concept_lower),
                KnowledgeDomain::ComputerScience => self.create_tech_analogy(&concept_lower),
                KnowledgeDomain::Philosophy => self.create_philosophy_analogy(&concept_lower),
                KnowledgeDomain::Astronomy => self.create_astronomy_analogy(&concept_lower),
                KnowledgeDomain::Music => self.create_music_analogy(&concept_lower),
                _ => self.create_general_analogy(&concept_lower),
            };
            if let Some(analogy) = analogy {
        (gaps, analogies)
    /// Step 4: Refine the explanation with analogies and clearer language
    fn refine_explanation(
        simple_explanation: &str,
        analogies: &[Analogy],
    ) -> String {
        let mut refined = simple_explanation.to_string();
        // Add the best analogy if available
        if let Some(analogy) = analogies.first() {
            refined.push_str(&format!(" Think of it like this: {}", analogy.explanation));
        // Ensure the explanation flows logically
        refined = self.improve_logical_flow(&refined);
        // Add a practical context if possible
        refined.push_str(&format!(
            " Understanding {concept} helps us make sense of how things work in the world around us."
        ));
        refined
    /// Improve the logical flow of the explanation
    fn improve_logical_flow(&self, text: &str) -> String {
        let sentences: Vec<&str> = text.split('.').filter(|s| !s.trim().is_empty()).collect();
        if sentences.len() <= 1 {
            return text.to_string();
        let mut improved = Vec::new();
        for (i, sentence) in sentences.iter().enumerate() {
            let trimmed = sentence.trim();
            if trimmed.is_empty() {
                continue;
            if i == 0 {
                // First sentence - just add it
                improved.push(trimmed.to_string());
            } else {
                // Add logical connectors
                let connector = match i {
                    1 => "This means that",
                    2 => "In other words,",
                    _ => "Also,",
                };
                // Only add connector if sentence doesn't already start with one
                if !trimmed.starts_with("Think of") && !trimmed.starts_with("This") {
                    improved.push(format!("{} {}", connector, trimmed.to_lowercase()));
                } else {
                    improved.push(trimmed.to_string());
        improved.join(". ") + "."
    /// Generate concept variations for better knowledge gathering
    fn generate_concept_variations(&self, concept: &str) -> Vec<String> {
        let mut variations = Vec::new();
        // Add plural/singular forms
        if concept_lower.ends_with('s') && concept_lower.len() > 2 {
            variations.push(concept_lower[..concept_lower.len() - 1].to_string());
        } else {
            variations.push(format!("{concept_lower}s"));
        // Add common question patterns
        variations.push(format!("what is {concept_lower}"));
        variations.push(format!("how does {concept_lower} work"));
        variations.push(format!("{concept_lower} definition"));
        // Add domain-specific variations
        if concept_lower.contains("quantum") {
            variations.push("quantum mechanics".to_string());
            variations.push("quantum physics".to_string());
        if concept_lower.contains("consciousness") {
            variations.push("awareness".to_string());
            variations.push("self-awareness".to_string());
        variations
    /// Create physics-related analogies
    fn create_physics_analogy(&self, concept: &str) -> Option<Analogy> {
        match concept {
            s if s.contains("quantum") => Some(Analogy {
                source: "everyday object".to_string(),
                target: concept.to_string(),
                explanation: "a coin that spins in the air - while it's spinning, it's both heads and tails at the same time, but when it lands (when we measure it), it becomes definitely one or the other.".to_string(),
            }),
            s if s.contains("energy") => Some(Analogy {
                source: "money in a bank".to_string(),
                explanation: "money in a bank account - it can be stored, transferred, and converted into different forms, but the total amount stays the same.".to_string(),
            s if s.contains("wave") => Some(Analogy {
                source: "ocean wave".to_string(),
                explanation: "waves on the ocean - they carry energy from one place to another without the water itself traveling that whole distance.".to_string(),
            _ => None,
    /// Create biology-related analogies
    fn create_biology_analogy(&self, concept: &str) -> Option<Analogy> {
            s if s.contains("cell") => Some(Analogy {
                source: "factory".to_string(),
                explanation: "a busy factory with different departments - the nucleus is like the office that makes decisions, mitochondria are like power plants, and the cell membrane is like security that controls what goes in and out.".to_string(),
            s if s.contains("dna") => Some(Analogy {
                source: "recipe book".to_string(),
                explanation: "a recipe book that contains all the instructions for making a living thing - each recipe (gene) tells the cell how to make a specific protein.".to_string(),
    /// Create technology-related analogies
    fn create_tech_analogy(&self, concept: &str) -> Option<Analogy> {
            s if s.contains("algorithm") => Some(Analogy {
                source: "cooking recipe".to_string(),
                explanation: "a step-by-step cooking recipe - it tells you exactly what to do, in what order, to get the result you want.".to_string(),
            s if s.contains("data") => Some(Analogy {
                source: "library books".to_string(),
                explanation: "books in a library - they contain information that can be organized, searched, and used to learn new things.".to_string(),
    /// Create philosophy-related analogies
    fn create_philosophy_analogy(&self, concept: &str) -> Option<Analogy> {
            s if s.contains("consciousness") => Some(Analogy {
                source: "flashlight in a dark room".to_string(),
                explanation: "a flashlight in a dark room - it illuminates whatever you point it at, making you aware of things that were always there but hidden in darkness.".to_string(),
            s if s.contains("free will") => Some(Analogy {
                source: "river choosing its path".to_string(),
                explanation: "a river choosing its path down a mountain - it seems to make choices about which way to flow, but it's also constrained by the landscape around it.".to_string(),
    /// Create astronomy-related analogies
    fn create_astronomy_analogy(&self, concept: &str) -> Option<Analogy> {
            s if s.contains("solar system") => Some(Analogy {
                source: "classroom with students".to_string(),
                explanation: "a classroom where the teacher (sun) is at the center and students (planets) sit in circles around them at different distances.".to_string(),
            s if s.contains("universe") => Some(Analogy {
                source: "expanding balloon".to_string(),
                explanation: "a balloon being inflated - as it expands, every point on its surface moves away from every other point, just like galaxies moving apart.".to_string(),
    /// Create music-related analogies
    fn create_music_analogy(&self, concept: &str) -> Option<Analogy> {
            s if s.contains("write music") || s.contains("music composition") || s.contains("compose") => Some(Analogy {
                source: "building with LEGO blocks".to_string(),
                explanation: "building with LEGO blocks - you start with basic pieces (notes, chords, rhythms) and combine them in creative ways to build something beautiful. Just like LEGO, you can follow instructions (music theory) or create your own unique designs.".to_string(),
            s if s.contains("melody") => Some(Analogy {
                source: "telling a story".to_string(),
                explanation: "telling a story with your voice - it goes up and down, has exciting parts and quiet parts, and takes the listener on a journey from beginning to end.".to_string(),
            s if s.contains("harmony") => Some(Analogy {
                source: "colors mixing on a painting".to_string(),
                explanation: "different colors on a painting that blend together beautifully - when you play multiple notes at the same time, they can create rich, colorful sounds just like mixing blue and yellow makes green.".to_string(),
            s if s.contains("rhythm") => Some(Analogy {
                source: "heartbeat or walking".to_string(),
                explanation: "your heartbeat or the steady rhythm of walking - it's the regular beat that keeps everything moving together, like a drummer keeping the whole band in time.".to_string(),
    /// Create general analogies for any concept
    fn create_general_analogy(&self, concept: &str) -> Option<Analogy> {
        Some(Analogy {
            source: "building blocks".to_string(),
            target: concept.to_string(),
            explanation: format!("building blocks that fit together in specific ways to create something larger and more complex - understanding {concept} means understanding how these pieces connect."),
        })
    /// Calculate confidence level based on available knowledge
    fn calculate_confidence(&self, knowledge: &[KnowledgeNode]) -> ConfidenceLevel {
        match knowledge.len() {
            0 => ConfidenceLevel::Low,
            1 => ConfidenceLevel::Medium,
            2..=3 => ConfidenceLevel::High,
            _ => ConfidenceLevel::VeryHigh,
    /// Find related concepts that might help understanding
    fn find_related_concepts(&self, knowledge: &[KnowledgeNode]) -> Vec<String> {
        let mut related = Vec::new();
        for node in knowledge {
            related.extend(node.related_concepts.clone());
        // Remove duplicates and limit to 5
        related.sort();
        related.dedup();
        related.into_iter().take(5).collect()
/// Represents an analogy used to explain a concept
#[derive(Debug, Clone)]
pub struct Analogy {
    pub source: String,      // The familiar thing we're comparing to
    pub target: String,      // The concept being explained
    pub explanation: String, // How they're similar
/// Complete Feynman explanation of a concept
pub struct FeynmanExplanation {
    pub concept: String,
    pub simple_explanation: String,
    pub analogies: Vec<Analogy>,
    pub knowledge_gaps: Vec<String>,
    pub refined_explanation: String,
    pub confidence_level: ConfidenceLevel,
    pub related_concepts: Vec<String>,
/// Confidence level in the explanation
#[derive(Debug, Clone, PartialEq)]
pub enum ConfidenceLevel {
    Low,
    Medium,
    High,
    VeryHigh,
impl FeynmanExplanation {
    /// Format the explanation for human consumption
    pub fn format_for_human(&self) -> String {
        let mut output = String::new();
        // Main explanation
        output.push_str(&self.refined_explanation);
        output.push_str("\n\n");
        // Add confidence indicator
        match self.confidence_level {
            ConfidenceLevel::Low => {
                output.push_str("🔍 [Low confidence - limited information available]")
            ConfidenceLevel::Medium => {
                output.push_str("📚 [Medium confidence - some supporting information]")
            ConfidenceLevel::High => {
                output.push_str("✅ [High confidence - well-supported explanation]")
            ConfidenceLevel::VeryHigh => {
                output.push_str("🎯 [Very high confidence - comprehensive information]")
        // Add related concepts if any
        if !self.related_concepts.is_empty() {
            output.push_str("\n\n🔗 Related concepts: ");
            output.push_str(&self.related_concepts.join(", "));
        output
#[cfg(test)]
mod tests {
    use super::*;
    use crate::KnowledgeEngine;
    #[test]
    fn test_feynman_explainer_creation() {
        let explainer = FeynmanExplainer::new(None);
        let explanation = explainer.explain("quantum mechanics");
        assert!(!explanation.refined_explanation.is_empty());
        assert_eq!(explanation.concept, "quantum mechanics");
    fn test_explanation_formatting() {
        let explanation = explainer.explain("test concept");
        let formatted = explanation.format_for_human();
        assert!(formatted.contains("confidence"));
        assert!(!formatted.is_empty());
