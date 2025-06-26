# Dynamic Knowledge System Documentation

## Overview

Think AI now features a fully dynamic knowledge loading system with component-based response generation and enhanced TinyLlama integration. This eliminates all hardcoded responses and enables runtime extensibility.

## Key Components

### 1. Dynamic Knowledge Loader (`dynamic_loader.rs`)

Loads knowledge from external files at runtime:

- **Supported Formats**: JSON and YAML
- **Location**: `./knowledge_files/` directory
- **Hot Reload**: Can watch for file changes (planned)
- **Export**: Can export current knowledge to files

#### File Format

**JSON Example:**
```json
{
  "domain": "computer_science",
  "entries": [
    {
      "topic": "Machine Learning",
      "content": "Machine learning is a subset of AI that enables systems to learn from data...",
      "related_concepts": ["AI", "neural networks", "data science"],
      "metadata": {
        "author": "Think AI",
        "version": "1.0"
      }
    }
  ]
}
```

**YAML Example:**
```yaml
domain: physics
entries:
  - topic: "Quantum Entanglement"
    content: "Quantum entanglement is a phenomenon where particles become correlated..."
    related_concepts: ["quantum mechanics", "superposition", "Bell's theorem"]
```

### 2. Component-Based Response Generator (`response_generator.rs`)

Modular response generation system with specialized components:

- **KnowledgeBaseComponent**: Direct knowledge retrieval
- **ScientificExplanationComponent**: Science-focused responses
- **TechnicalComponent**: Programming and technology
- **PhilosophicalComponent**: Deep thinking and ethics
- **CompositionComponent**: "What is X made of?" queries
- **ComparisonComponent**: Comparing concepts
- **HistoricalComponent**: Historical context
- **PracticalApplicationComponent**: Real-world uses
- **FutureSpeculationComponent**: Future predictions
- **AnalogyComponent**: Metaphors and comparisons

#### Creating Custom Components

```rust
use think_ai_knowledge::response_generator::{ResponseComponent, ResponseContext};

pub struct MyCustomComponent;

impl ResponseComponent for MyCustomComponent {
    fn name(&self) -> &'static str {
        "MyCustom"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        // Return 0.0-1.0 based on relevance
        if query.contains("my topic") { 0.9 } else { 0.0 }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Generate response or return None
        Some("My custom response".to_string())
    }
}
```

### 3. Enhanced TinyLlama (`enhanced.rs`)

Dynamic response generation without hardcoding:

- **Token-based Generation**: Builds responses from vocabulary
- **Pattern Matching**: Uses response patterns for different query types
- **Context-Aware**: Incorporates provided context into responses
- **Temperature Control**: Adjustable randomness for variety
- **Query Type Detection**: Identifies definition, explanation, comparison, process queries

## Usage

### Loading Knowledge Files

1. Create a `knowledge_files` directory in your project root
2. Add JSON or YAML files with knowledge entries
3. The system automatically loads them on startup

```bash
mkdir knowledge_files
# Add your knowledge files
./target/release/think-ai chat
```

### Extending with Custom Components

```rust
let engine = Arc::new(KnowledgeEngine::new());
let mut generator = ComponentResponseGenerator::new(engine);

// Add custom component
generator.add_component(Box::new(MyCustomComponent));

// Generate response
let response = generator.generate_response("my query");
```

### Using Enhanced TinyLlama

```rust
let llama = EnhancedTinyLlama::new();

// Generate without context
let response = llama.generate("What is consciousness?", None).await?;

// Generate with context
let context = "In neuroscience, consciousness is...";
let response = llama.generate("What is consciousness?", Some(context)).await?;
```

## Performance Characteristics

- **Knowledge Lookup**: O(1) hash-based retrieval
- **Component Scoring**: O(n) where n = number of components
- **Response Generation**: O(m) where m = response length
- **File Loading**: O(k) where k = number of knowledge entries

## Best Practices

1. **Knowledge Files**: Keep files focused on specific domains
2. **Component Design**: Make components specific and score accurately
3. **Context Usage**: Provide relevant context for better responses
4. **Performance**: Use hash-based lookups for O(1) access

## Future Enhancements

- [ ] Hot reload of knowledge files
- [ ] Plugin system for components
- [ ] Machine learning-based component selection
- [ ] Distributed knowledge loading
- [ ] Knowledge versioning and rollback