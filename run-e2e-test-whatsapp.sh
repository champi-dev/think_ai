#!/bin/bash
# Quick E2E test with WhatsApp notification to +573026132990

set -e

echo "🚀 Starting E2E test with WhatsApp notifications..."

# Set your WhatsApp number
export WHATSAPP_TO_NUMBER="+573026132990"

# Set up Twilio credentials if available
if [ -f ~/.twilio_env ]; then
    source ~/.twilio_env
fi

# Start the service
echo "Starting ThinkAI service..."
cd /home/champi/Dev/think_ai/full-system
PORT=7777 cargo run --release --bin think-ai-full > test.log 2>&1 &
SERVICE_PID=$!

# Wait for service to start
sleep 10

# Check if service is running
if ! curl -s http://localhost:7777/health > /dev/null; then
    echo "❌ Service failed to start!"
    kill $SERVICE_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Service started successfully"

# Run the WhatsApp notification test
echo "Running WhatsApp notification test..."
cd /home/champi/Dev/think_ai/full-system

# Create a test that triggers an error and sends WhatsApp
cat > test_whatsapp.rs << 'EOF'
use reqwest::Client;
use serde_json::json;

#[tokio::main]
async fn main() {
    let client = Client::new();
    
    println!("Triggering error to test WhatsApp notification...");
    
    // This should trigger validation error and send WhatsApp
    let response = client
        .post("http://localhost:7777/api/chat")
        .json(&json!({
            "message": "<script>alert('XSS test')</script>",
            "session_id": "whatsapp-test"
        }))
        .send()
        .await
        .unwrap();
    
    println!("Response status: {}", response.status());
    
    if response.status() == 400 {
        println!("✅ Error correctly detected!");
        println!("📱 WhatsApp notification should be sent to +573026132990");
    }
}
EOF

# Run the test
cargo run --bin test_whatsapp

# Clean up
rm test_whatsapp.rs
kill $SERVICE_PID 2>/dev/null || true

echo "
✅ E2E Test completed!
📱 Check WhatsApp (+573026132990) for notification
"