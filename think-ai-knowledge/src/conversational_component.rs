// Enhanced Conversational Component for Natural Dialogue

use crate::response_generator::{ResponseComponent, ResponseContext};
use std::collections::HashMap;

pub struct EnhancedConversationalComponent;

impl ResponseComponent for EnhancedConversationalComponent {
    fn name(&self) -> &'static str {
        "EnhancedConversational"
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();

        // High priority for conversational queries with context
        if !context.conversation_history.is_empty() {
            // Questions about previous conversation
            if query_lower.contains("what")
                && (query_lower.contains("my name")
                    || query_lower.contains("i said")
                    || query_lower.contains("i told")
                    || query_lower.contains("we discussed")
                    || query_lower.contains("i mentioned"))
            {
                return 0.95;
            }

            // Memory recall patterns
            if query_lower.contains("remember")
                || query_lower.contains("recall")
                || query_lower.contains("do you know")
            {
                return 0.9;
            }
        }

        // Standard greetings
        if query_lower.starts_with("hello")
            || query_lower.starts_with("hi")
            || query_lower.starts_with("hey")
            || query_lower == "greetings"
        {
            return 0.8;
        }

        // Natural conversation patterns
        let conversational_patterns = [
            "how are you",
            "what's up",
            "how's it going",
            "nice to meet",
            "pleased to meet",
            "good to see",
            "thank you",
            "thanks",
            "appreciate",
            "goodbye",
            "bye",
            "see you",
            "what do you think",
            "your opinion",
        ];

        if conversational_patterns
            .iter()
            .any(|&p| query_lower.contains(p))
        {
            return 0.75;
        }

        0.0
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase();

        // Handle questions about conversation history
        if !context.conversation_history.is_empty() {
            // Extract user facts from conversation
            let mut user_facts: HashMap<String, String> = HashMap::new();

            for (role, content) in &context.conversation_history {
                if role == "user" {
                    let content_lower = content.to_lowercase();

                    // Extract name
                    if content_lower.contains("my name is")
                        || content_lower.contains("i am")
                        || content_lower.contains("i'm")
                    {
                        if let Some(name) = extract_name(content) {
                            user_facts.insert("name".to_string(), name);
                        }
                    }

                    // Extract other facts
                    if content_lower.contains("i work")
                        || content_lower.contains("my job")
                        || content_lower.contains("profession")
                    {
                        if let Some(job) = extract_profession(content) {
                            user_facts.insert("profession".to_string(), job);
                        }
                    }

                    // Extract preferences
                    if content_lower.contains("i like")
                        || content_lower.contains("i love")
                        || content_lower.contains("my favorite")
                    {
                        if let Some(pref) = extract_preference(content) {
                            user_facts.insert("preference".to_string(), pref);
                        }
                    }

                    // Extract numbers/codes
                    if content_lower.contains("remember")
                        && (content_lower.contains("code") || content_lower.contains("number"))
                    {
                        if let Some(code) = extract_code(content) {
                            user_facts.insert("code".to_string(), code);
                        }
                    }
                }
            }

            // Answer questions about user
            if query_lower.contains("what") && query_lower.contains("my name") {
                if let Some(name) = user_facts.get("name") {
                    return Some(format!("Your name is {}.", name));
                } else {
                    return Some("I don't recall you mentioning your name. What would you like me to call you?".to_string());
                }
            }

            if query_lower.contains("what")
                && (query_lower.contains("profession")
                    || query_lower.contains("job")
                    || query_lower.contains("work"))
            {
                if let Some(job) = user_facts.get("profession") {
                    return Some(format!("You mentioned you work as {}.", job));
                }
            }

            if query_lower.contains("code") || query_lower.contains("number") {
                if let Some(code) = user_facts.get("code") {
                    return Some(format!("The code you asked me to remember is: {}", code));
                }
            }

            // General memory questions
            if query_lower.contains("what")
                && query_lower.contains("know about me")
                && !user_facts.is_empty()
            {
                let facts: Vec<String> = user_facts
                    .iter()
                    .map(|(k, v)| match k.as_str() {
                        "name" => format!("Your name is {}", v),
                        "profession" => format!("You work as {}", v),
                        "preference" => format!("You mentioned you like {}", v),
                        "code" => format!("You gave me a code to remember: {}", v),
                        _ => format!("{}: {}", k, v),
                    })
                    .collect();

                return Some(format!(
                    "Here's what I know about you: {}",
                    facts.join(". ")
                ));
            }
        }

        // Standard greetings
        if query_lower.starts_with("hello") || query_lower.starts_with("hi") {
            return Some("Hello! How can I help you today?".to_string());
        }

        if query_lower.contains("how are you") {
            return Some("I'm functioning optimally! My O(1) response system is working perfectly. How are you doing?".to_string());
        }

        if query_lower.contains("thank") {
            return Some("You're welcome! I'm here to help anytime.".to_string());
        }

        if query_lower.contains("bye") || query_lower.contains("goodbye") {
            return Some(
                "Goodbye! It was great chatting with you. Feel free to come back anytime!"
                    .to_string(),
            );
        }

        None
    }
}

// Helper functions to extract information
fn extract_name(text: &str) -> Option<String> {
    let patterns = ["my name is ", "i am ", "i'm ", "call me "];

    for pattern in &patterns {
        if let Some(pos) = text.to_lowercase().find(pattern) {
            let start = pos + pattern.len();
            let remaining = &text[start..];
            let name = remaining
                .split_whitespace()
                .next()
                .map(|s| s.trim_matches(|c: char| !c.is_alphanumeric()))
                .filter(|s| !s.is_empty())?;

            return Some(name.to_string());
        }
    }

    None
}

fn extract_profession(text: &str) -> Option<String> {
    let patterns = [
        "i work as a ",
        "i work as an ",
        "i am a ",
        "i am an ",
        "my job is ",
        "profession is ",
    ];

    for pattern in &patterns {
        if let Some(pos) = text.to_lowercase().find(pattern) {
            let start = pos + pattern.len();
            let remaining = &text[start..];
            let words: Vec<&str> = remaining
                .split(['.', ',', '!'])
                .next()?
                .split_whitespace()
                .take(3) // Take up to 3 words for profession
                .collect();

            if !words.is_empty() {
                return Some(words.join(" "));
            }
        }
    }

    None
}

fn extract_preference(text: &str) -> Option<String> {
    let patterns = ["i like ", "i love ", "my favorite ", "i prefer "];

    for pattern in &patterns {
        if let Some(pos) = text.to_lowercase().find(pattern) {
            let start = pos + pattern.len();
            let remaining = &text[start..];
            let pref = remaining.split(['.', ',', '!']).next()?.trim();

            if !pref.is_empty() {
                return Some(pref.to_string());
            }
        }
    }

    None
}

fn extract_code(text: &str) -> Option<String> {
    // Look for patterns like "code: XXX" or "number: XXX"
    if let Some(pos) = text.find(':') {
        let code_part = text[pos + 1..].trim();
        let code = code_part
            .split_whitespace()
            .next()
            .map(|s| s.trim_matches(|c: char| c == '"' || c == '\'' || c == '.'))?;

        if !code.is_empty() && code.len() < 50 {
            // Reasonable code length
            return Some(code.to_string());
        }
    }

    // Look for capital letter sequences
    let words: Vec<&str> = text.split_whitespace().collect();
    for word in words {
        if word
            .chars()
            .all(|c| c.is_uppercase() || c.is_numeric() || c == '-')
            && word.len() > 5
        {
            return Some(word.to_string());
        }
    }

    None
}
