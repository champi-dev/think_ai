#!/bin/bash
# Script to set up Twilio webhook for WhatsApp integration

# Load credentials from environment
ACCOUNT_SID="${TWILIO_ACCOUNT_SID}"
AUTH_TOKEN="${TWILIO_AUTH_TOKEN}"
WEBHOOK_URL="https://thinkai.lat/webhooks/whatsapp"
STATUS_WEBHOOK_URL="https://thinkai.lat/webhooks/whatsapp/status"

if [ -z "$ACCOUNT_SID" ] || [ -z "$AUTH_TOKEN" ]; then
    echo "❌ Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables"
    exit 1
fi

echo "🔧 Setting up WhatsApp webhook for ThinkAI..."

# Update sandbox webhook configuration
echo ""
echo "📱 To complete setup:"
echo "1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn"
echo "2. In the 'Sandbox Configuration' section:"
echo "   - Set 'WHEN A MESSAGE COMES IN' to: $WEBHOOK_URL"
echo "   - Method: HTTP POST"
echo "   - Set 'STATUS CALLBACK URL' to: $STATUS_WEBHOOK_URL"
echo "3. Save the configuration"
echo ""
echo "🎉 Then users can chat with ThinkAI on WhatsApp by:"
echo "   1. Joining sandbox: Send 'join <your-code>' to +1 415 523 8886"
echo "   2. Start chatting with the AI!"
echo ""
echo "📝 Available commands:"
echo "   • Any message - Chat with AI"
echo "   • /help - Show commands"
echo "   • /status - System status"
echo "   • /clear - Clear conversation"
echo "   • /web - Get web link"