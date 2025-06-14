#!/usr/bin/env python3
"""Monitor the exponential intelligence training progress."""

import time
import json
import re
from pathlib import Path

def monitor_training():
    """Monitor training progress from log file."""
    log_file = Path("training.log")
    
    if not log_file.exists():
        print("❌ Training log not found. Is training running?")
        return
    
    print("📊 MONITORING EXPONENTIAL INTELLIGENCE TRAINING")
    print("=" * 50)
    
    last_position = 0
    iteration_count = 0
    last_metrics = {}
    
    while True:
        try:
            with open(log_file, 'r') as f:
                f.seek(last_position)
                new_content = f.read()
                last_position = f.tell()
            
            # Find iterations
            iterations = re.findall(r'DIRECTIVE #(\d+):', new_content)
            if iterations:
                iteration_count = max(int(i) for i in iterations)
            
            # Find intelligence scores
            scores = re.findall(r'Intelligence Score: ([\d.]+)', new_content)
            
            # Find metrics
            metrics_matches = re.findall(r'Metrics: ({[^}]+})', new_content, re.DOTALL)
            if metrics_matches:
                try:
                    # Clean up the metrics string
                    metrics_str = metrics_matches[-1].replace('\n', '').replace('  ', ' ')
                    last_metrics = eval(metrics_str)
                except:
                    pass
            
            # Find cost
            costs = re.findall(r'Cost: \$([\d.]+)/\$([\d.]+)', new_content)
            
            # Display current status
            print(f"\r🧠 Iteration: {iteration_count}/10000", end="")
            
            if scores:
                print(f" | Intelligence: {scores[-1]}", end="")
            
            if costs:
                spent, budget = costs[-1]
                print(f" | Cost: ${spent}/${budget}", end="")
            
            if last_metrics:
                # Calculate average metric
                avg_metric = sum(float(v) for v in last_metrics.values()) / len(last_metrics)
                print(f" | Avg Metric: {avg_metric:.2f}", end="")
            
            print("     ", end="", flush=True)
            
            # Check for completion messages
            if "EXPONENTIAL INTELLIGENCE ACHIEVED" in new_content:
                print("\n\n🎉 EXPONENTIAL INTELLIGENCE ACHIEVED! 🎉")
                break
            
            if "TRAINING COMPLETE" in new_content:
                print("\n\n✅ Training completed!")
                break
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_training()