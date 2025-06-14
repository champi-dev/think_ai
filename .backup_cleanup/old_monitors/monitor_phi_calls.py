#!/usr/bin/env python3
"""Monitor Phi-3.5 calls in real-time."""

import subprocess
import time
from datetime import datetime


def monitor_ollama():
    """Monitor Ollama/Phi-3.5 calls."""
    print("🔍 Monitoring Phi-3.5 Mini calls...")
    print("Press Ctrl+C to stop\n")
    
    last_log_line = None
    
    try:
        while True:
            # Check Ollama logs
            try:
                # Get last few lines of training output
                result = subprocess.run(
                    ['tail', '-20', 'training_output.log'],
                    capture_output=True,
                    text=True
                )
                
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if 'Phi-3.5 Mini' in line and line != last_log_line:
                            timestamp = datetime.now().strftime('%H:%M:%S')
                            print(f"[{timestamp}] 🤖 {line.strip()}")
                            last_log_line = line
                
                # Also check if Ollama is running
                ps_result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True
                )
                
                if 'ollama' in ps_result.stdout:
                    # Check Ollama API status
                    api_check = subprocess.run(
                        ['curl', '-s', 'http://localhost:11434/api/tags'],
                        capture_output=True,
                        text=True
                    )
                    
                    if 'phi3' in api_check.stdout:
                        status = "✅ Phi-3.5 Mini available"
                    else:
                        status = "❌ Phi-3.5 Mini not loaded"
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {status}")
                        print("To load: ollama run phi3:mini")
            
            except Exception as e:
                pass
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped.")


if __name__ == "__main__":
    monitor_ollama()