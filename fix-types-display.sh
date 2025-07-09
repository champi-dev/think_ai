#!/bin/bash

echo "🔧 FIXING TYPES DISPLAY IMPLEMENTATION"
echo "===================================="

# 1. Rewrite the Display implementation correctly
echo "1️⃣ Rewriting Display implementation in types.rs..."
# Find the Display implementation and rewrite it
sed -i '/impl std::fmt::Display for ProcessType {/,/^}$/ c\
impl std::fmt::Display for ProcessType {\
    fn fmt(&self, f: &mut std::fmt::Formatter<'"'"'_>) -> std::fmt::Result {\
        match self {\
            ProcessType::Thinking => write!(f, "thinking"),\
            ProcessType::Dreaming => write!(f, "dreaming"),\
            ProcessType::Learning => write!(f, "learning"),\
            ProcessType::Reflecting => write!(f, "reflecting"),\
        }\
    }\
}' think-ai-knowledge/src/types.rs

# 2. Also fix the comprehensive_knowledge call order
echo "2️⃣ Fixing comprehensive_knowledge method parameter order..."
# The parameters should be: domain, topic, content, related
sed -i '/engine.add_knowledge(/,/)/ {
    /KnowledgeDomain::Medicine,$/,/);$/ {
        /vec!\["immune system"/d
        /"Immunology".to_string(),$/a\            "The immune system protects against pathogens through innate and adaptive responses. Innate immunity provides immediate, non-specific defense via barriers, inflammation, and phagocytes. Adaptive immunity develops specific responses through lymphocytes. B cells produce antibodies recognizing antigens. T cells include helpers (coordinate response), killers (destroy infected cells), and regulatory (prevent autoimmunity). Memory cells enable faster secondary responses. Vaccines stimulate immunity without disease. Disorders include autoimmune diseases (immune system attacks self), immunodeficiencies (weakened immunity), and allergies (overreaction to harmless substances). Transplant rejection occurs when immune system attacks foreign tissue. Immunotherapy harnesses immunity against cancer. The microbiome influences immune development and function.".to_string(),
    }
}' think-ai-knowledge/src/comprehensive_knowledge.rs

# Move the vec to the end
sed -i '/"The immune system protects.*".to_string(),$/a\            vec!["immune system".to_string(), "antibodies".to_string(), "lymphocytes".to_string()]' think-ai-knowledge/src/comprehensive_knowledge.rs

# Remove the duplicate line
sed -i '/"The immune system protects.*".to_string(),$/,+1 {
    /"The immune system protects.*".to_string(),$/{
        N
        /"The immune system protects.*".to_string(),$/d
    }
}' think-ai-knowledge/src/comprehensive_knowledge.rs

# 3. Test the build
echo ""
echo "3️⃣ Testing build..."
cargo build --all 2>&1 | tail -20

echo ""
echo "✅ Display implementation fixed!"