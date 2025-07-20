# Setting up Twilio WhatsApp

The error indicates you need to set up WhatsApp with your Twilio account first.

## Steps to Enable WhatsApp:

1. **Join Twilio Sandbox** (for testing):
   - Send a WhatsApp message to: **+1 415 523 8886**
   - With text: **join <your-sandbox-keyword>**
   - You'll receive a confirmation message

2. **Get your sandbox number**:
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - You'll see your sandbox join code

3. **For production** (optional):
   - Request WhatsApp Business API access
   - Get approved WhatsApp Business number
   - Update TWILIO_WHATSAPP_FROM with your number

## Update your environment:

```bash
export TWILIO_ACCOUNT_SID="<your_account_sid>"
export TWILIO_AUTH_TOKEN="<your_auth_token>"
export TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
export WHATSAPP_TO_NUMBER="<your_phone_number>"
```

## Test with SMS instead (works immediately):

```bash
# This will send SMS instead of WhatsApp
curl -X POST https://api.twilio.com/2010-04-01/Accounts/<your_account_sid>/Messages.json \
--data-urlencode "From=+1234567890" \
--data-urlencode "To=<your_phone_number>" \
--data-urlencode "Body=ThinkAI Test: System monitoring active 🤖" \
-u <your_account_sid>:<your_auth_token>
```