#!/bin/bash

echo "🔧 FIXING SYNTAX ERRORS IN KNOWLEDGE MODULE"
echo "========================================="

# Fix the malformed function signatures in comprehensive_knowledge.rs
echo "1️⃣ Fixing comprehensive_knowledge.rs syntax errors..."
sed -i 's/__engine: engine: &Arc<KnowledgeEngine>Arc<KnowledgeEngine>/_engine: \&Arc<KnowledgeEngine>/g' think-ai-knowledge/src/comprehensive_knowledge.rs
sed -i 's/_engine: engine: &Arc<KnowledgeEngine>Arc<KnowledgeEngine>/_engine: \&Arc<KnowledgeEngine>/g' think-ai-knowledge/src/comprehensive_knowledge.rs

echo "✅ Syntax fixes applied!"