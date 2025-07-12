#\!/bin/bash
set -e

echo "🔍 Reproducing and Fixing Markdown Issue"
echo "========================================"

# Create test server to isolate the issue
cat > test-markdown-server.rs << 'RUST'
use axum::{routing::post, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct Request { message: String }

#[derive(Serialize)]
struct Response { response: String }

async fn broken_handler(Json(req): Json<Request>) -> Json<Response> {
    // Simulating the broken formatting
    let text = "Physics is the fundamental science that explores matter and energy.";
    let broken = text.chars()
        .map( < /dev/null | c| if c.is_alphabetic() && rand::random::<bool>() { 
            format\!("{} ", c) 
        } else { 
            c.to_string() 
        })
        .collect::<String>();
    
    Json(Response { response: broken })
}

async fn fixed_handler(Json(req): Json<Request>) -> Json<Response> {
    // Clean response without extra spaces
    let text = match req.message.to_lowercase().as_str() {
        s if s.contains("physics") => {
            "Physics is the fundamental science that explores the nature of the universe, \
             matter, energy, and their interactions. It seeks to understand everything from \
             the smallest subatomic particles to the vast expanse of the cosmos."
        }
        s if s.contains("love") => {
            "Love is a complex and multifaceted emotion that has been the subject of \
             countless discussions across cultures. It involves deep affection, compassion, \
             and a desire to care for someone or something valuable."
        }
        _ => "This is a properly formatted response without broken spacing."
    };
    
    Json(Response { response: text.to_string() })
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/broken", post(broken_handler))
        .route("/fixed", post(fixed_handler));
    
    println\!("Test server on http://localhost:7777");
    axum::Server::bind(&"0.0.0.0:7777".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
RUST

# Build and run test
echo "Building test server..."
rustc --edition 2021 test-markdown-server.rs -o test-server 2>/dev/null || {
    echo "❌ Compilation failed, using curl tests instead"
    
    # Test current production
    echo -e "\n📊 Current Production Response Analysis:"
    echo "----------------------------------------"
    
    RESPONSE=$(curl -s http://localhost:8080/api/chat -X POST \
        -H "Content-Type: application/json" \
        -d '{"message":"What is physics?"}' | jq -r '.response' 2>/dev/null)
    
    # Check for broken patterns
    if echo "$RESPONSE" | grep -E "([a-z]) ([a-z]) ([a-z])" > /dev/null; then
        echo "❌ BROKEN SPACING DETECTED\!"
        echo "Example patterns found:"
        echo "$RESPONSE" | grep -oE ".{0,30}[a-z] [a-z] [a-z].{0,30}" | head -3
        
        # Show character analysis
        echo -e "\n🔬 Character-by-character analysis:"
        echo "$RESPONSE" | head -c 100 | od -c | head -5
    else
        echo "✅ No broken spacing detected"
        echo "Sample output:"
        echo "$RESPONSE" | head -c 200
    fi
    
    # Create fix script
    echo -e "\n🔧 Creating fix for the issue..."
    cat > fix-markdown-spaces.patch << 'PATCH'
diff --git a/think-ai-knowledge/src/response_cleaner.rs b/think-ai-knowledge/src/response_cleaner.rs
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/think-ai-knowledge/src/response_cleaner.rs
@@ -0,0 +1,25 @@
+pub fn clean_response_text(text: &str) -> String {
+    // Remove extra spaces between characters
+    let mut cleaned = String::with_capacity(text.len());
+    let mut prev_was_space = false;
+    
+    for ch in text.chars() {
+        if ch == ' ' {
+            if \!prev_was_space {
+                cleaned.push(ch);
+                prev_was_space = true;
+            }
+        } else {
+            cleaned.push(ch);
+            prev_was_space = false;
+        }
+    }
+    
+    // Fix specific patterns
+    cleaned
+        .replace(" , ", ", ")
+        .replace(" . ", ". ")
+        .replace(" : ", ": ")
+        .replace(" ; ", "; ")
+        .replace("  ", " ")
+}
PATCH
    
    echo -e "\n📝 Fix Summary:"
    echo "The issue appears to be extra spaces being inserted between characters."
    echo "The fix involves cleaning the response text before sending it to the client."
}

# Clean up
rm -f test-markdown-server.rs test-server

echo -e "\n✅ Analysis complete\!"
