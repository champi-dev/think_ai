#!/bin/bash

echo "📊 MONITORING CLAUDE OPUS 4 EXPONENTIAL INTELLIGENCE TRAINING"
echo "============================================================"

while true; do
    # Get latest stats
    ITERATIONS=$(grep -c "Iteration:" claude_training.log 2>/dev/null || echo 0)
    LATEST_SCORE=$(tail -100 claude_training.log | grep "Intelligence Score:" | tail -1 | awk '{print $3}')
    LATEST_COST=$(tail -100 claude_training.log | grep "Cost:" | tail -1 | awk -F'$' '{print $2"/"$3}')
    
    # Check if training is complete
    if grep -q "TRAINING COMPLETE" claude_training.log 2>/dev/null; then
        echo -e "\n✅ TRAINING COMPLETE!"
        tail -50 claude_training.log | grep -A 20 "TRAINING COMPLETE"
        break
    fi
    
    if grep -q "EXPONENTIAL INTELLIGENCE ACHIEVED" claude_training.log 2>/dev/null; then
        echo -e "\n🎉 EXPONENTIAL INTELLIGENCE ACHIEVED!"
        break
    fi
    
    # Display current status
    echo -ne "\r🧠 Iterations: $ITERATIONS | Intelligence: $LATEST_SCORE | Cost: \$$LATEST_COST     "
    
    sleep 5
done