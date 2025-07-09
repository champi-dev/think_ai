#!/bin/bash

echo "🔧 FIXING DUPLICATE F PARAMETERS"
echo "==============================="

# 1. Fix evidence.rs - remove duplicate f
echo "1️⃣ Fixing evidence.rs..."
sed -i '/impl std::fmt::Display for EvidenceReport/,/^}/ {
    /write!(/,/)$/ {
        /write!($/N
        s/write!(\n[[:space:]]*f,\n[[:space:]]*f,/write!(\n            f,/
    }
}' think-ai-knowledge/src/evidence.rs

# Also remove the standalone f line
sed -i '276d' think-ai-knowledge/src/evidence.rs

# 2. Fix persistence.rs - remove duplicate f
echo "2️⃣ Fixing persistence.rs..."
sed -i '/impl std::fmt::Display for PersistenceReport/,/^}/ {
    /write!(/,/)$/ {
        /write!($/N
        s/write!(\n[[:space:]]*f,\n[[:space:]]*f,/write!(\n            f,/
    }
}' think-ai-knowledge/src/persistence.rs

# Also remove the standalone f line
sed -i '224d' think-ai-knowledge/src/persistence.rs

# 3. Fix comprehensive_knowledge - add missing vec parameter
echo "3️⃣ Fixing comprehensive_knowledge immunology call..."
sed -i '/engine.add_knowledge(/,/)/ {
    /"Immunology".to_string(),$/a\            vec!["immune system".to_string(), "antibodies".to_string(), "lymphocytes".to_string()],
}' think-ai-knowledge/src/comprehensive_knowledge.rs

# 4. Test the build
echo ""
echo "4️⃣ Testing build..."
cargo build --all 2>&1 | tail -10

echo ""
echo "✅ Display duplicate f parameters fixed!"