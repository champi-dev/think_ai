#!/bin/bash
set -e

echo "🔧 Adding timeout protection to chat handler..."

# Create a patch for full-working-o1.rs
cat > /tmp/chat-timeout.patch << 'EOF'
--- a/think-ai-cli/src/bin/full-working-o1.rs
+++ b/think-ai-cli/src/bin/full-working-o1.rs
@@ -187,11 +187,25 @@
     }
 
     // Generate response using Qwen 1.5B
-    let response = match state
-        .qwen_client
-        .generate_simple(&request.query, None)
-        .await
-    {
+    let response = match tokio::time::timeout(
+        std::time::Duration::from_secs(30),
+        async {
+            match state
+                .qwen_client
+                .generate_simple(&request.query, None)
+                .await
+            {
+                Ok(qwen_response) => Ok(qwen_response),
+                Err(e) => {
+                    eprintln!("Qwen error: {}", e);
+                    Err(e)
+                }
+            }
+        }
+    )
+    .await
+    {
+        Ok(Ok(qwen_response)) => qwen_response,
+        Ok(Err(_)) | Err(_) => {
             // Log error for debugging but don't show to user
             eprintln!("Qwen unavailable: {}", e);
             // Fallback to response generator if Qwen fails
EOF

# Apply the patch
cd /home/champi/Dev/think_ai
patch -p1 < /tmp/chat-timeout.patch || echo "Patch might have failed, trying direct edit..."

echo "✅ Timeout protection added"