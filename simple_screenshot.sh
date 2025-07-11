#!/bin/bash

# Take a screenshot of the chat interface
echo "Taking screenshot of Think AI chat interface..."

# Use xvfb-run to run Chrome in virtual display
xvfb-run -a google-chrome --headless --disable-gpu --window-size=1280,800 \
  --screenshot=/home/administrator/think_ai/markdown_screenshot.png \
  http://localhost:3456/static/chat.html

echo "Screenshot saved to: /home/administrator/think_ai/markdown_screenshot.png"

# Also use curl to capture the HTML
curl -s http://localhost:3456/static/chat.html > /home/administrator/think_ai/chat_interface.html
echo "HTML saved to: /home/administrator/think_ai/chat_interface.html"