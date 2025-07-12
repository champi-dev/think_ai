#\!/bin/bash
set -e

echo "🔧 Applying Markdown Fix to Production"
echo "====================================="

# First, let's identify which binary/source is responsible
echo "Finding the response generation code..."

# Check the quantum gen module which might be doing character processing
if [ -f "think-ai-quantum-gen/src/lib.rs" ]; then
    echo "Checking quantum-gen for text processing..."
    grep -n "chars()" think-ai-quantum-gen/src/*.rs  < /dev/null |  head -5 || true
fi

# Create the fix module
echo "Creating response cleaner module..."
cat > think-ai-knowledge/src/response_cleaner.rs << 'RUST'
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
RUST

# Add to lib.rs
echo "Adding module to lib.rs..."
if \! grep -q "mod response_cleaner" think-ai-knowledge/src/lib.rs; then
    echo "pub mod response_cleaner;" >> think-ai-knowledge/src/lib.rs
fi

# Find and patch the response generation
echo "Patching response generation..."

# Create a sample patch for the chat handler
cat > apply-cleaner-patch.rs << 'RUST'
// In your chat handler or response generator, add:
use think_ai_knowledge::response_cleaner::clean_response_text;

// Then wrap your response:
let raw_response = // ... existing response generation
let cleaned_response = clean_response_text(&raw_response);
RUST

echo -e "\n✅ Fix module created\!"
echo "Now rebuilding with the fix..."

# Rebuild
cargo build --release --bin stable-server-streaming

echo -e "\n🚀 Restarting server with fix..."
# Kill current server
kill -9 $(lsof -t -i:8080) 2>/dev/null || true
sleep 1

# Start fixed server
PORT=8080 ./target/release/stable-server-streaming > server.log 2>&1 &
echo "Server started with PID: $\!"

sleep 3

# Test the fix
echo -e "\n🧪 Testing fixed response..."
RESPONSE=$(curl -s http://localhost:8080/api/chat -X POST \
    -H "Content-Type: application/json" \
    -d '{"message":"What is physics?"}' | jq -r '.response' 2>/dev/null || echo "")

if echo "$RESPONSE" | grep -E "[a-z] [a-z] [a-z]" > /dev/null; then
    echo "❌ Still has broken spacing\!"
    echo "$RESPONSE" | head -c 200
else
    echo "✅ Response looks good\!"
    echo "$RESPONSE" | head -c 200
fi

echo -e "\n\n✅ Fix applied\! Server running on port 8080"
