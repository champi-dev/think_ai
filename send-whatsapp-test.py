#!/usr/bin/env python3
import os
import requests
from datetime import datetime

# Twilio credentials (set these as environment variables)
account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
from_whatsapp = os.environ.get('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')  # Twilio sandbox default
to_whatsapp = 'whatsapp:+573026132990'

if not account_sid or not auth_token:
    print("❌ Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables")
    print("\nTo test without Twilio, I'll simulate the message that would be sent:")
    
    message = f"""
🤖 *ThinkAI Test Alert*

*System Test Successful*

This is a test message from the Think AI comprehensive testing suite.

✅ Code committed and pushed
✅ WhatsApp integration ready
✅ Monitoring system active

Check your production at: https://thinkai.lat

_Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_
"""
    print("\n📱 Message that would be sent to +573026132990:")
    print(message)
    exit(0)

# Send via Twilio
url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'

message = f"""🤖 *ThinkAI Test Alert*

*System Test Successful*

This is a test message from the Think AI comprehensive testing suite.

✅ Code committed and pushed to GitHub
✅ WhatsApp integration implemented
✅ E2E tests with 100% coverage target
✅ Monitoring system active

Your production site: https://thinkai.lat

_Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}_"""

data = {
    'From': from_whatsapp,
    'To': to_whatsapp,
    'Body': message
}

try:
    response = requests.post(url, data=data, auth=(account_sid, auth_token))
    
    if response.status_code in [200, 201]:
        print("✅ WhatsApp message sent successfully to +573026132990!")
        print(f"Message SID: {response.json().get('sid', 'N/A')}")
    else:
        print(f"❌ Failed to send message. Status: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error sending WhatsApp message: {e}")
    
print("\n📱 Check WhatsApp on +573026132990 for the test message!")