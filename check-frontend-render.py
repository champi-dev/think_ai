#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

# Fetch the page
response = requests.get("https://thinkai.lat/")
print(f"Status Code: {response.status_code}")

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Check for styles
styles = soup.find_all("link", rel="stylesheet")
print(f"\nStylesheets found: {len(styles)}")
for style in styles:
    print(f"  - {style.get('href')}")

# Check for scripts
scripts = soup.find_all("script")
print(f"\nScripts found: {len(scripts)}")
for script in scripts:
    if script.get("src"):
        print(f"  - {script.get('src')}")

# Check root element
root = soup.find(id="root")
if root:
    print(f"\nRoot element found")
    print(f"Root content: {root.get_text().strip() or '(empty)'}")
else:
    print("\nRoot element NOT found")

# Check for any visible text
body = soup.find("body")
if body:
    text = body.get_text().strip()
    print(f"\nBody text content: {text[:100] if text else '(empty)'}")
