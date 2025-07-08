#!/bin/bash
set -e

echo "🧹 Cleaning up warnings in isolated sessions modules..."

# Fix unused imports in isolated_session.rs
sed -i '2s/use std::sync::{Arc, RwLock};/use std::sync::Arc;/' think-ai-knowledge/src/isolated_session.rs
sed -i '8s/use crate::types::{Message, Context, SessionState};/use crate::types::{Message, SessionState};/' think-ai-knowledge/src/isolated_session.rs

# Fix unused imports in parallel_processor.rs
sed -i '2s/use std::sync::{Arc, RwLock, Mutex};/use std::sync::{Arc, Mutex};/' think-ai-knowledge/src/parallel_processor.rs

# Fix unused imports in shared_knowledge.rs
sed -i '2s/use std::sync::{Arc, RwLock};/use std::sync::RwLock;/' think-ai-knowledge/src/shared_knowledge.rs
sed -i '/use crate::types::KnowledgeType;/d' think-ai-knowledge/src/shared_knowledge.rs

# Fix unused variables with underscore prefix
sed -i 's/process_config/_process_config/g' think-ai-knowledge/src/parallel_processor.rs
sed -i 's/context: Option<String>/context: Option<String>/g' think-ai-knowledge/src/parallel_processor.rs
sed -i 's/context\./context\./g' think-ai-knowledge/src/parallel_processor.rs
sed -i 's/\bcontext\b/_context/g' think-ai-knowledge/src/parallel_processor.rs

# Add underscore to last_activity field or remove if truly unused
sed -i 's/last_activity/_last_activity/g' think-ai-knowledge/src/parallel_processor.rs

echo "✅ Cleanup completed!"
echo ""
echo "Running cargo check to verify..."
cargo check -p think-ai-knowledge

echo ""
echo "🎉 All warnings should be resolved!"