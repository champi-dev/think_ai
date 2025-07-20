use regex::Regex;
use std::sync::Arc;

pub struct InputValidator {
    email_regex: Regex,
    sql_injection_patterns: Vec<Regex>,
    xss_patterns: Vec<Regex>,
}

impl InputValidator {
    pub fn new() -> Self {
        Self {
            email_regex: Regex::new(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$").unwrap(),
            sql_injection_patterns: vec![
                Regex::new(r"(?i)(union|select|insert|update|delete|drop|create|alter|exec|script)").unwrap(),
                Regex::new(r#"(?i)(--|#|/\*|\*/|;|'|"|`)"#).unwrap(),
                Regex::new(r#"(?i)(or|and)\s+\d+\s*=\s*\d+"#).unwrap(),
            ],
            xss_patterns: vec![
                Regex::new(r"<script[^>]*>.*?</script>").unwrap(),
                Regex::new(r"javascript:").unwrap(),
                Regex::new(r#"on\w+\s*="#).unwrap(),
                Regex::new(r"<iframe[^>]*>").unwrap(),
            ],
        }
    }

    pub fn validate_email(&self, email: &str) -> bool {
        self.email_regex.is_match(email)
    }

    pub fn sanitize_input(&self, input: &str) -> String {
        // Remove potentially dangerous characters
        input
            .replace('<', "&lt;")
            .replace('>', "&gt;")
            .replace('"', "&quot;")
            .replace('\'', "&#x27;")
            .replace('/', "&#x2F;")
    }

    pub fn check_sql_injection(&self, input: &str) -> bool {
        for pattern in &self.sql_injection_patterns {
            if pattern.is_match(input) {
                return true;
            }
        }
        false
    }

    pub fn check_xss(&self, input: &str) -> bool {
        for pattern in &self.xss_patterns {
            if pattern.is_match(input) {
                return true;
            }
        }
        false
    }

    pub fn validate_length(&self, input: &str, min: usize, max: usize) -> bool {
        let len = input.len();
        len >= min && len <= max
    }

    pub fn validate_alphanumeric(&self, input: &str) -> bool {
        input.chars().all(|c| c.is_alphanumeric() || c == '_' || c == '-')
    }
}