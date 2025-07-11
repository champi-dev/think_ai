use std::collections::HashMap;

/// Token counter for managing conversation context size
/// Uses a simple heuristic: ~4 characters = 1 token (approximation for English text)
/// For production, you'd use tiktoken or similar
pub struct TokenCounter {
    char_to_token_ratio: f32,
}

impl TokenCounter {
    pub fn new() -> Self {
        Self {
            // Conservative estimate: ~4 characters per token
            // This is approximate but works well for English text
            char_to_token_ratio: 4.0,
        }
    }
    
    /// Count tokens in a text string
    pub fn count(&self, text: &str) -> usize {
        (text.len() as f32 / self.char_to_token_ratio).ceil() as usize
    }
    
    /// Count tokens in a conversation (role + content for each message)
    pub fn count_conversation(&self, messages: &[(String, String)]) -> usize {
        messages.iter()
            .map(|(role, content)| self.count(&format!("{}: {}", role, content)))
            .sum()
    }
    
    /// Estimate tokens for a full context (system prompt + conversation + query)
    pub fn estimate_context_tokens(
        &self,
        system_prompt: Option<&str>,
        conversation: &[(String, String)],
        query: &str,
    ) -> usize {
        let mut total = 0;
        
        if let Some(prompt) = system_prompt {
            total += self.count(prompt);
        }
        
        total += self.count_conversation(conversation);
        total += self.count(query);
        
        total
    }
}

/// Conversation compactor for managing token limits
pub struct ConversationCompactor {
    token_counter: TokenCounter,
    max_tokens: usize,
}

impl ConversationCompactor {
    pub fn new(max_tokens: usize) -> Self {
        Self {
            token_counter: TokenCounter::new(),
            max_tokens,
        }
    }
    
    /// Compact a conversation to fit within token limit
    /// Strategy: Keep most recent messages and summarize older ones
    pub fn compact(
        &self,
        messages: &[(String, String)],
        reserved_tokens: usize, // Reserved for system prompt + new query
    ) -> Vec<(String, String)> {
        let available_tokens = self.max_tokens.saturating_sub(reserved_tokens);
        
        if messages.is_empty() {
            return Vec::new();
        }
        
        // First, check if all messages fit
        let total_tokens = self.token_counter.count_conversation(messages);
        if total_tokens <= available_tokens {
            return messages.to_vec();
        }
        
        // Strategy: Keep recent messages, summarize older ones
        let mut result = Vec::new();
        let mut used_tokens = 0;
        
        // Always try to keep the most recent messages
        for (role, content) in messages.iter().rev() {
            let msg_tokens = self.token_counter.count(&format!("{}: {}", role, content));
            
            if used_tokens + msg_tokens <= available_tokens {
                result.push((role.clone(), content.clone()));
                used_tokens += msg_tokens;
            } else if result.is_empty() {
                // If even the most recent message is too long, truncate it
                let available_chars = (available_tokens as f32 * 4.0) as usize;
                let truncated = Self::truncate_text(content, available_chars.saturating_sub(role.len() + 2));
                result.push((role.clone(), format!("{}... [truncated]", truncated)));
                break;
            } else {
                // Add a summary message for older context
                if used_tokens + 50 <= available_tokens {
                    let remaining_count = messages.len() - result.len();
                    result.push((
                        "system".to_string(),
                        format!("[{} earlier messages omitted for brevity]", remaining_count)
                    ));
                }
                break;
            }
        }
        
        // Reverse to maintain chronological order
        result.reverse();
        result
    }
    
    /// Intelligently summarize messages (simplified version)
    pub fn summarize_messages(&self, messages: &[(String, String)]) -> String {
        if messages.is_empty() {
            return String::new();
        }
        
        // Count key facts mentioned
        let mut key_facts = Vec::new();
        
        for (role, content) in messages {
            if role == "user" {
                // Extract potential key facts (simple heuristic)
                if content.to_lowercase().contains("my name is") {
                    if let Some(name) = Self::extract_after(content, "my name is") {
                        key_facts.push(format!("User's name: {}", name));
                    }
                }
                if content.to_lowercase().contains("i am a") || content.to_lowercase().contains("i'm a") {
                    if let Some(profession) = Self::extract_after(content, "i am a")
                        .or_else(|| Self::extract_after(content, "i'm a")) {
                        key_facts.push(format!("Profession: {}", profession));
                    }
                }
                if content.to_lowercase().contains("i love") || content.to_lowercase().contains("i like") {
                    if let Some(interest) = Self::extract_after(content, "i love")
                        .or_else(|| Self::extract_after(content, "i like")) {
                        key_facts.push(format!("Interest: {}", interest));
                    }
                }
            }
        }
        
        if key_facts.is_empty() {
            format!("Previous conversation with {} messages", messages.len())
        } else {
            format!("Previous context: {}", key_facts.join(", "))
        }
    }
    
    fn truncate_text(text: &str, max_chars: usize) -> &str {
        if text.len() <= max_chars {
            text
        } else {
            // Try to break at word boundary
            let truncated = &text[..max_chars];
            if let Some(last_space) = truncated.rfind(' ') {
                &text[..last_space]
            } else {
                truncated
            }
        }
    }
    
    fn extract_after(text: &str, prefix: &str) -> Option<String> {
        let lower_text = text.to_lowercase();
        let lower_prefix = prefix.to_lowercase();
        
        if let Some(pos) = lower_text.find(&lower_prefix) {
            let start = pos + lower_prefix.len();
            let remaining = &text[start..].trim();
            
            // Take until punctuation or newline
            let end = remaining.find(|c: char| c == '.' || c == ',' || c == '!' || c == '?' || c == '\n')
                .unwrap_or(remaining.len());
            
            Some(remaining[..end].trim().to_string())
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_token_counting() {
        let counter = TokenCounter::new();
        
        assert_eq!(counter.count("Hello"), 2); // 5 chars / 4 = 1.25, ceil = 2
        assert_eq!(counter.count("Hello, world!"), 4); // 13 chars / 4 = 3.25, ceil = 4
        assert_eq!(counter.count(""), 0);
    }
    
    #[test]
    fn test_conversation_compaction() {
        let compactor = ConversationCompactor::new(100);
        
        let messages = vec![
            ("user".to_string(), "Hello, my name is Alice".to_string()),
            ("assistant".to_string(), "Nice to meet you, Alice!".to_string()),
            ("user".to_string(), "I'm a software engineer".to_string()),
            ("assistant".to_string(), "That's great!".to_string()),
            ("user".to_string(), "I love coding in Rust".to_string()),
        ];
        
        // Should keep all messages if they fit
        let compacted = compactor.compact(&messages, 20);
        assert_eq!(compacted.len(), messages.len());
        
        // Should truncate if limit is very small
        let compacted = compactor.compact(&messages, 80);
        assert!(compacted.len() < messages.len());
    }
}

/// Simple function to count tokens in text
/// Uses ~4 characters = 1 token approximation
pub fn count_tokens(text: &str) -> usize {
    (text.len() as f32 / 4.0).ceil() as usize
}