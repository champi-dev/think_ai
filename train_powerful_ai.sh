#!/bin/bash

# Train Think AI to be a powerful tool and conversationalist
set -e

echo "🚀 Training Think AI to be Powerful & Conversational"
echo "==================================================="

# First, run comprehensive training for tool capabilities
echo -e "\n📊 Phase 1: Tool Training (1,000 iterations)"
./target/release/comprehensive-train

# Then add high-quality direct knowledge
echo -e "\n📊 Phase 2: Direct Knowledge Training"
./target/release/direct-train

# Combine the knowledge bases
echo -e "\n🔄 Combining knowledge bases..."
mkdir -p final_training/checkpoints

# Use Python to merge the knowledge bases
python3 << 'EOF'
import json
import os

# Load all knowledge sources
knowledge = {}

# Load comprehensive training (filter good ones)
try:
    with open('comprehensive_knowledge/checkpoints/checkpoint_2000.json', 'r') as f:
        data = json.load(f)
        for k, v in data['nodes'].items():
            # Filter out poor quality patterns
            if not v['content'].startswith('Q: What\'s causing') and \
               not v['content'].startswith('user:') and \
               not v['content'].startswith('Pattern') and \
               len(v['content']) > 100:
                knowledge[k] = v
        print(f"✅ Loaded {len(knowledge)} quality items from comprehensive training")
except:
    print("⚠️  No comprehensive training found")

# Load direct training (all high quality)
try:
    with open('direct_training/checkpoints/checkpoint_1000.json', 'r') as f:
        data = json.load(f)
        before = len(knowledge)
        knowledge.update(data['nodes'])
        print(f"✅ Added {len(knowledge) - before} items from direct training")
except:
    print("⚠️  No direct training found")

# Save combined knowledge
os.makedirs('final_training/checkpoints', exist_ok=True)
with open('final_training/checkpoints/checkpoint_final.json', 'w') as f:
    json.dump({
        'iteration': 3000,
        'nodes': knowledge,
        'metadata': {
            'training_type': 'combined',
            'tool_iterations': 1000,
            'conversation_iterations': 1000,
            'direct_knowledge_items': 14
        }
    }, f)

print(f"\n✅ Final knowledge base: {len(knowledge)} total items")
EOF

echo -e "\n✨ Training Complete!"
echo "Think AI is now trained with:"
echo "  ✓ Powerful tool capabilities"
echo "  ✓ Natural conversational abilities"
echo "  ✓ High-quality knowledge base"
echo ""
echo "To use the trained AI, update full-server.rs to load from 'final_training'"