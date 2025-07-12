// Add this function to clean response text
pub fn clean_response_formatting(text: &str) -> String {
    // Remove excessive spaces between characters
    let mut result = String::with_capacity(text.len());
    let mut chars = text.chars().peekable();
    
    while let Some(ch) = chars.next() {
        result.push(ch);
        
        // Skip extra spaces after characters
        if ch \!= ' ' && chars.peek() == Some(&' ') {
            // Check if next char after space is also a letter
            let mut temp_chars = chars.clone();
            temp_chars.next(); // skip the space
            if let Some(next_ch) = temp_chars.peek() {
                if next_ch.is_alphabetic() && result.chars().last().unwrap_or(' ').is_alphabetic() {
                    // Skip this space - it's breaking up a word
                    chars.next(); // consume the bad space
                }
            }
        }
    }
    
    // Clean up any remaining formatting issues
    result
        .replace("  ", " ")
        .replace(" ,", ",")
        .replace(" .", ".")
        .replace(" :", ":")
        .replace(" ;", ";")
}
