// Human-like conversation training module
// Makes Think AI converse naturally like a super smart human

use crate::{KnowledgeDomain, KnowledgeEngine};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
/// Conversational patterns that make AI sound more human
#[derive(Debug, Clone)]
pub struct ConversationalPattern {
    pub pattern_type: PatternType,
    pub examples: Vec<String>,
    pub context: ConversationContext,
}
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum PatternType {
    Greeting,
    SmallTalk,
    Empathy,
    Humor,
    Curiosity,
    Storytelling,
    CasualExplanation,
    PersonalOpinion,
    Acknowledgment,
    Transition,
pub struct ConversationContext {
    pub formality: f32,  // 0.0 = very casual, 1.0 = very formal
    pub enthusiasm: f32, // 0.0 = reserved, 1.0 = very enthusiastic
    pub verbosity: f32,  // 0.0 = concise, 1.0 = elaborate
/// Personality traits for more human-like responses
pub struct PersonalityTraits {
    pub friendliness: f32,
    pub humor_level: f32,
    pub curiosity: f32,
    pub empathy: f32,
    pub confidence: f32,
impl Default for PersonalityTraits {
    fn default() -> Self {
        Self {
            friendliness: 0.8,
            humor_level: 0.6,
            curiosity: 0.9,
            empathy: 0.7,
            confidence: 0.85,
        }
    }
/// Human conversation trainer
pub struct HumanConversationTrainer {
    knowledge_engine: Arc<KnowledgeEngine>,
    patterns: HashMap<PatternType, Vec<ConversationalPattern>>,
    personality: PersonalityTraits,
    conversation_memory: Arc<RwLock<Vec<String>>>,
    filler_words: Vec<String>,
    thinking_phrases: Vec<String>,
impl HumanConversationTrainer {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Self {
        let mut trainer = Self {
            knowledge_engine,
            patterns: HashMap::new(),
            personality: PersonalityTraits::default(),
            conversation_memory: Arc::new(RwLock::new(Vec::new())),
            filler_words: vec![
                "hmm".to_string(),
                "well".to_string(),
                "you know".to_string(),
                "actually".to_string(),
                "basically".to_string(),
                "honestly".to_string(),
                "I mean".to_string(),
                "like".to_string(),
                "so".to_string(),
            ],
            thinking_phrases: vec![
                "Let me think about that...".to_string(),
                "That's a great question!".to_string(),
                "Hmm, interesting...".to_string(),
                "Oh, I see what you're asking...".to_string(),
                "Good point!".to_string(),
                "Yeah, so...".to_string(),
        };
        trainer.initialize_patterns();
        trainer
    /// Initialize conversational patterns
    fn initialize_patterns(&mut self) {
        // Greetings - casual and friendly
        self.add_pattern(
            PatternType::Greeting,
            vec![
                "Hey there! What's up?",
                "Oh hey! How's it going?",
                "Hi! Nice to see you!",
                "Hey! What brings you here today?",
                "Hello! How can I help you out?",
                "Yo! What's on your mind?",
        );
        // Small talk
            PatternType::SmallTalk,
                "By the way, have you tried {topic} before?",
                "Oh, that reminds me of {story}",
                "You know what's funny? {observation}",
                "I was just thinking about {topic} earlier",
                "Speaking of which, {related_topic}",
        // Empathy and understanding
            PatternType::Empathy,
                "I totally get that",
                "Yeah, that makes complete sense",
                "I hear you",
                "That must be {feeling}",
                "I can see why you'd think that",
                "Absolutely, I understand where you're coming from",
        // Humor and lightness
            PatternType::Humor,
                "Haha, that's one way to look at it!",
                "Well, that escalated quickly 😄",
                "Plot twist: {unexpected}",
                "I mean, technically you're not wrong...",
                "*adjusts imaginary glasses* Actually...",
        // Curiosity
            PatternType::Curiosity,
                "Ooh, tell me more about that!",
                "Wait, that's fascinating - how does that work?",
                "I'm curious, what made you think of that?",
                "That's really interesting! Have you considered {alternative}?",
                "Wow, I never thought about it that way",
        // Casual explanations
            PatternType::CasualExplanation,
                "So basically, {explanation}",
                "The way I think about it is {analogy}",
                "It's kinda like {comparison}",
                "Think of it this way: {example}",
                "Here's the deal: {simple_explanation}",
        // Personal opinions (while being helpful)
            PatternType::PersonalOpinion,
                "Personally, I think {opinion}",
                "In my experience, {observation}",
                "I've always found that {insight}",
                "If you ask me, {recommendation}",
                "I'm a big fan of {preference} because {reason}",
        // Acknowledgments
            PatternType::Acknowledgment,
                "Good catch!",
                "Oh, you're absolutely right",
                "That's a solid point",
                "Nice observation!",
                "Exactly!",
                "Yep, you nailed it",
        // Transitions
            PatternType::Transition,
                "So anyway...",
                "But yeah, back to your question...",
                "Oh, and another thing...",
                "Also worth mentioning...",
                "Speaking of which...",
    fn add_pattern(&mut self, pattern_type: PatternType, examples: Vec<&str>) {
        let patterns = examples
            .into_iter()
            .map(|ex| {
                ConversationalPattern {
                    pattern_type: pattern_type.clone(),
                    examples: vec![ex.to_string()],
                    context: ConversationContext {
                        formality: 0.3, // Casual by default
                        enthusiasm: 0.7,
                        verbosity: 0.5,
                    },
                }
            })
            .collect();
        self.patterns.insert(pattern_type, patterns);
    /// Transform a response to be more human-like
    pub fn humanize_response(&self, original: &str, context: Option<&str>) -> String {
        let mut response = String::new();
        // Sometimes start with a thinking phrase
        if rand::random::<f32>() < 0.3 {
            response.push_str(&self.get_random_thinking_phrase());
            response.push(' ');
        // Add personality-based modifications
        response.push_str(&self.apply_personality(original));
        // Sometimes add a follow-up thought
        if rand::random::<f32>() < 0.2 {
            response.push_str(&self.generate_follow_up(context));
        response
    fn get_random_thinking_phrase(&self) -> String {
        self.thinking_phrases[rand::random::<usize>() % self.thinking_phrases.len()].clone()
    fn apply_personality(&self, text: &str) -> String {
        let mut result = text.to_string();
        // Add casual filler words based on personality
        if self.personality.friendliness > 0.7 && rand::random::<f32>() < 0.2 {
            let filler = &self.filler_words[rand::random::<usize>() % self.filler_words.len()];
            result = format!("{filler}, {result}");
        // Make explanations more conversational
        result = result
            .replace("Therefore,", "So,")
            .replace("However,", "But,")
            .replace("Additionally,", "Also,")
            .replace("It is", "It's")
            .replace("cannot", "can't")
            .replace("will not", "won't");
        result
    fn generate_follow_up(&self, context: Option<&str>) -> String {
        let follow_ups = [
            "Does that make sense?",
            "Hope that helps!",
            "Let me know if you want me to elaborate!",
            "Feel free to ask if anything's unclear!",
            "Pretty cool, right?",
        ];
        follow_ups[rand::random::<usize>() % follow_ups.len()].to_string()
    /// Train the knowledge engine with conversational patterns
    pub fn train_conversational_knowledge(&self) {
        // Add conversational knowledge
        let conversations = vec![
            ("greeting_responses", "When someone says hi, respond warmly and ask how they're doing or what's on their mind"),
            ("active_listening", "Show that you're engaged by acknowledging what they said and asking follow-up questions"),
            ("empathy_expressions", "When someone shares a problem, acknowledge their feelings before offering solutions"),
            ("humor_timing", "Light humor can make conversations more enjoyable, but read the room first"),
            ("storytelling", "Share relevant anecdotes or examples to make explanations more relatable"),
            ("curiosity_expression", "Show genuine interest in what others are saying by asking thoughtful questions"),
            ("opinion_sharing", "It's okay to have opinions while remaining helpful and open-minded"),
            ("casual_language", "Using contractions and informal language makes conversations feel more natural"),
        for (topic, content) in conversations {
            self.knowledge_engine.add_knowledge(
                KnowledgeDomain::Philosophy, // Using Philosophy for human interaction knowledge
                topic.to_string(),
                content.to_string(),
                vec![], // No related concepts for now
            );
    /// Generate a human-like response based on input
    pub fn generate_human_response(&self, input: &str) -> String {
        // Detect the type of input
        let input_lower = input.to_lowercase();
        // Greeting
        if input_lower.contains("hello")
            || input_lower.contains("hi")
            || input_lower.contains("hey")
        {
            return self.generate_greeting_response();
        // Question
        if input_lower.contains("?")
            || input_lower.starts_with("what")
            || input_lower.starts_with("how")
            || input_lower.starts_with("why")
            return self.generate_curious_response(input);
        // Statement - respond with interest
        self.generate_engaged_response(input)
    fn generate_greeting_response(&self) -> String {
        let greetings = &self.patterns[&PatternType::Greeting];
        let greeting = &greetings[rand::random::<usize>() % greetings.len()];
        greeting.examples[0].clone()
    fn generate_curious_response(&self, input: &str) -> String {
        // Acknowledge the question
        let acks = &self.patterns[&PatternType::Acknowledgment];
        if rand::random::<f32>() < 0.4 {
            response.push_str(&acks[rand::random::<usize>() % acks.len()].examples[0]);
        // Add actual answer (would be generated by main system)
        response.push_str("Let me explain that for you. ");
    fn generate_engaged_response(&self, input: &str) -> String {
        let empathy = &self.patterns[&PatternType::Empathy];
        let response = &empathy[rand::random::<usize>() % empathy.len()];
        format!("{} Tell me more!", response.examples[0])
// Convenience function to use globally
pub fn humanize(text: &str) -> String {
    // Simple humanization without full trainer
    let mut result = text.to_string();
    // Basic conversational replacements
    result = result
        .replace("Therefore,", "So,")
        .replace("However,", "But,")
        .replace("Additionally,", "Also,")
        .replace("It is", "It's")
        .replace("cannot", "can't")
        .replace("will not", "won't")
        .replace("I am", "I'm");
    // Sometimes add a casual starter
    if rand::random::<f32>() < 0.2 {
        let starters = ["Well, ", "So, ", "Actually, ", "You know, "];
        let starter = starters[rand::random::<usize>() % starters.len()];
        result = format!("{starter}{result}");
    result
// For testing
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_humanize_response() {
        let trainer = HumanConversationTrainer::new(Arc::new(KnowledgeEngine::new()));
        let formal = "Therefore, the algorithm exhibits O(1) complexity.";
        let humanized = trainer.humanize_response(formal, None);
        assert!(humanized.contains("So,") || humanized.len() > formal.len());
    fn test_greeting_detection() {
        let response = trainer.generate_human_response("Hello there!");
        assert!(response.contains("Hey") || response.contains("Hi") || response.contains("Hello"));
