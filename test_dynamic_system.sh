#!/bin/bash

# Test script for dynamic knowledge loading and enhanced response generation

echo "🧪 Testing Dynamic Knowledge System"
echo "=================================="

# Create knowledge files directory
echo "📁 Creating knowledge files directory..."
mkdir -p knowledge_files

# Create a custom knowledge file
echo "📝 Creating custom knowledge file..."
cat > knowledge_files/custom_knowledge.json << 'EOF'
{
  "domain": "computer_science",
  "entries": [
    {
      "topic": "Dynamic Knowledge Loading",
      "content": "Dynamic knowledge loading allows Think AI to read and integrate new knowledge from external files at runtime. This system supports JSON and YAML formats, enabling users to extend the knowledge base without recompiling. Files are loaded from the knowledge_files directory and can include custom domains, topics, and relationships.",
      "related_concepts": ["file system", "runtime configuration", "knowledge management", "extensibility"]
    },
    {
      "topic": "Component-Based Response Generation",
      "content": "The component-based response generator uses a modular architecture where different components handle specific types of queries. Each component has a scoring function to determine relevance and generates targeted responses. Components include KnowledgeBase, Scientific, Technical, Philosophical, Composition, Comparison, Historical, Practical, Future, and Analogy generators.",
      "related_concepts": ["modular design", "response synthesis", "query analysis", "component architecture"]
    },
    {
      "topic": "Enhanced TinyLlama",
      "content": "Enhanced TinyLlama is an improved language model that generates responses using vocabulary, embeddings, and pattern matching. Unlike the original hardcoded responses, it builds sentences dynamically based on query type (definition, explanation, comparison, process) and context. It uses temperature-controlled randomness for varied but coherent outputs.",
      "related_concepts": ["language model", "dynamic generation", "pattern matching", "embeddings"]
    }
  ]
}
EOF

# Create a YAML knowledge file
echo "📝 Creating YAML knowledge file..."
cat > knowledge_files/astronomy_extended.yaml << 'EOF'
domain: astronomy
entries:
  - topic: "Neutron Star"
    content: "A neutron star is the collapsed core of a massive star that has undergone a supernova explosion. With a radius of only 10-15 km but a mass 1.4-2 times the Sun's, neutron stars are incredibly dense - a teaspoon would weigh billions of tons. They spin rapidly, with some rotating hundreds of times per second, creating pulsars that emit regular radio pulses."
    related_concepts: ["supernova", "pulsar", "degenerate matter", "gravitational collapse"]
  
  - topic: "Exoplanet"
    content: "An exoplanet is a planet that orbits a star outside our solar system. Over 5,000 exoplanets have been confirmed using methods like transit photometry and radial velocity. They range from hot Jupiters (gas giants orbiting close to their stars) to potentially habitable rocky worlds in the goldilocks zone. The search for exoplanets helps us understand planetary formation and the potential for life elsewhere."
    related_concepts: ["transit method", "habitable zone", "Kepler mission", "biosignatures"]
EOF

# Build the project
echo "🔨 Building Think AI..."
cd /home/champi/Development/think_ai
cargo build --release --bin think-ai 2>&1 | grep -E "(Compiling|Finished|error)"

# Test the enhanced system
echo -e "\n🚀 Testing enhanced knowledge chat...\n"

# Create test queries
cat > test_queries.txt << 'EOF'
What is Dynamic Knowledge Loading?
How does Component-Based Response Generation work?
Tell me about Enhanced TinyLlama
What is a Neutron Star?
Explain exoplanets
What is the composition of a neutron star?
How big is a typical exoplanet?
Compare neutron stars and black holes
exit
EOF

# Run the chat with test queries
echo "📊 Running test queries..."
./target/release/think-ai chat < test_queries.txt

echo -e "\n✅ Test complete!"
echo "📌 Check the knowledge_files directory for the created files"
echo "🔍 The system should now respond with information from both:"
echo "   - Dynamically loaded knowledge files"
echo "   - Component-based response generation"
echo "   - Enhanced TinyLlama for unknown queries"