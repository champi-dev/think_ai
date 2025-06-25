#!/bin/bash

cd "$(dirname "$0")"

echo "Think AI O(1) Chat"
echo "Type 'exit' to quit"
echo ""

python3 -c "
import sys
sys.path.append('.')
from core.o1_chat import O1Chat
import time

chat = O1Chat()
total_time = 0
count = 0

while True:
    try:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit', 'bye']:
            break
        
        response, elapsed_ms = chat.get_response(user_input)
        total_time += elapsed_ms
        count += 1
        
        print(f'Think AI: {response}')
        print(f'[{elapsed_ms:.2f}ms]')
        print()
        
    except (KeyboardInterrupt, EOFError):
        break

if count > 0:
    print(f'\nAvg response time: {total_time/count:.2f}ms')
"