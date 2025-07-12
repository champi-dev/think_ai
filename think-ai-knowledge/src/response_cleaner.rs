//\! Response text cleaning utilities to fix formatting issues

/// Cleans response text by removing excessive spaces between characters
pub fn clean_response_text(text: &str) -> String {
    let mut result = String::with_capacity(text.len());
    let mut prev_char = '\0';
    let mut in_word = false;
    
    for ch in text.chars() {
        match ch {
            ' ' => {
                // Only add space if previous wasn't a space and we're between words
                if prev_char \!= ' ' && prev_char \!= '\0' {
                    // Check if this space is breaking up a word
                    if in_word && text.chars().nth(
                        result.len() + 1
                    ).map_or(false, |c| c.is_alphabetic()) {
                        // Skip this space - it's inside a word
                        continue;
                    }
                    result.push(ch);
                    in_word = false;
                }
            }
            c if c.is_alphabetic() => {
                result.push(ch);
                in_word = true;
            }
            _ => {
                result.push(ch);
                in_word = false;
            }
        }
        prev_char = ch;
    }
    
    // Final cleanup
    result
        .replace("  ", " ")
        .trim()
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_clean_broken_spacing() {
        assert_eq\!(
            clean_response_text("P h y s i c s   i s   f u n"),
            "Physics is fun"
        );
        assert_eq\!(
            clean_response_text("Love is a complex emotion"),
            "Love is a complex emotion"
        );
    }
}
