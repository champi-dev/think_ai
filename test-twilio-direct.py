#!/usr/bin/env python3
import requests
from base64 import b64encode

# Your Twilio credentials
account_sid = "<your_account_sid>"
auth_token = "<your_auth_token>"

print("🔍 Checking your Twilio account setup...\n")

# 1. Check account status
url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json"
response = requests.get(url, auth=(account_sid, auth_token))

if response.status_code == 200:
    account = response.json()
    print(f"✅ Account Active: {account.get('friendly_name', 'Your Account')}")
    print(f"   Status: {account.get('status')}")
    print(f"   Type: {account.get('type')}")
else:
    print(f"❌ Account check failed: {response.status_code}")

# 2. Check for phone numbers
print("\n📱 Checking phone numbers...")
url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/IncomingPhoneNumbers.json"
response = requests.get(url, auth=(account_sid, auth_token))

if response.status_code == 200:
    data = response.json()
    numbers = data.get('incoming_phone_numbers', [])
    if numbers:
        print(f"✅ Found {len(numbers)} phone number(s):")
        for num in numbers:
            print(f"   - {num.get('phone_number')} ({num.get('friendly_name')})")
    else:
        print("❌ No phone numbers found. You need to buy a Twilio number first.")
        print("\n💡 To buy a number:")
        print("   1. Go to: https://console.twilio.com/us1/develop/phone-numbers/manage/search")
        print("   2. Search for a number (costs ~$1/month)")
        print("   3. Buy the number")
        print("   4. Then SMS will work!")

# 3. Check WhatsApp setup
print("\n💬 Checking WhatsApp Sandbox...")
print("\nTo use WhatsApp (FREE):")
print("1. Open WhatsApp on your phone")
print("2. Send a message to: +1 415 523 8886")
print("3. Get your join code from:")
print("   https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
print("4. Send: join <your-code>")
print("5. You'll get a confirmation")
print("\nThen I can send WhatsApp messages to +573026132990!")

# 4. Try sending a test message via Twilio Sandbox
print("\n📤 Attempting to send test message...")
print("   (This will only work after you join the sandbox)")

# For WhatsApp (after joining sandbox)
whatsapp_data = {
    'From': 'whatsapp:+14155238886',  # Twilio Sandbox number
    'To': 'whatsapp:<your_phone_number>',
    'Body': '🤖 ThinkAI Test Alert\n\nYour testing suite is ready!\n\n✅ 100% test coverage target\n✅ E2E tests implemented\n✅ WhatsApp notifications active\n\nProduction: https://thinkai.lat'
}

url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
response = requests.post(url, data=whatsapp_data, auth=(account_sid, auth_token))

if response.status_code in [200, 201]:
    print("✅ WhatsApp message sent! Check your phone.")
else:
    error = response.json()
    if error.get('code') == 63007:
        print("❌ You need to join the WhatsApp sandbox first (see instructions above)")
    else:
        print(f"❌ Error: {error.get('message', 'Unknown error')}")