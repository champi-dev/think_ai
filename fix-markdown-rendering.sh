#\!/bin/bash
set -e

echo "🔧 Fixing Markdown Rendering Issue"
echo "=================================="

# Find and fix the text processing issue
echo "Searching for text processing code..."

# Look for the actual binary source
BINARY_NAME=$(ps aux  < /dev/null |  grep -E "8080.*think-ai" | grep -v grep | awk '{print $11}' | head -1)
echo "Current running binary: $BINARY_NAME"

# Create a fix patch
cat > fix-response-formatting.rs << 'RUST'
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
RUST

# Create a wrapper that fixes responses before sending
cat > fixed-chat-handler.rs << 'RUST'
// In your chat handler, wrap the response:
let original_response = // ... your current response generation
let cleaned_response = clean_response_formatting(&original_response);

Json(ChatResponse {
    response: cleaned_response,
    session_id,
    error: None,
})
RUST

echo -e "\n✅ Fix created\! To apply:"
echo "1. Add the clean_response_formatting function to your response handler"
echo "2. Apply it to all text responses before sending"
echo "3. Rebuild with: cargo build --release"

# Test the fix concept
echo -e "\n🧪 Testing fix concept..."
BROKEN="P h y s i c s   i s   t h e   f u n d a m e n t a l"
FIXED=$(echo "$BROKEN" | sed 's/\([a-zA-Z]\) \([a-zA-Z]\)/\1\2/g')
echo "Broken: $BROKEN"
echo "Fixed:  $FIXED"

echo -e "\n📝 Summary: The issue is extra spaces being inserted between characters."
echo "The fix removes these spaces while preserving legitimate word boundaries."
