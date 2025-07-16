# Think AI Image Generation

O(1) performance image generation with intelligent caching and learning.

## Features

- **O(1) Cache Lookups**: SHA256-based hash keys for instant cache retrieval
- **Intelligent Prompt Optimization**: Learns from successful generations
- **Automatic Style Enhancement**: Adds appropriate modifiers to improve quality
- **LRU Cache Management**: Automatically manages disk space with eviction
- **Learning System**: Improves over time by analyzing generation patterns
- **Secure API Key Management**: Uses environment variables, never hardcoded

## Setup

1. Run the setup script:
```bash
./setup-image-gen.sh
```

2. Enter your Leonardo AI API key when prompted

3. The script will:
   - Create a `.env` file with your configuration
   - Create the image cache directory
   - Build the image generation binary

## Usage

### Generate an Image
```bash
./target/release/think-ai-image generate "a cyberpunk city at night" -o city.png
```

### With Options
```bash
./target/release/think-ai-image generate "portrait of a robot" \
  --width 768 \
  --height 1024 \
  --negative "blurry, low quality" \
  --output robot.png
```

### View Statistics
```bash
./target/release/think-ai-image stats
```

### Clear Cache
```bash
./target/release/think-ai-image clear
```

## Architecture

### O(1) Performance

The system achieves O(1) image retrieval through:

1. **Hash-based Cache Keys**: Each unique request generates a SHA256 hash
2. **DashMap Index**: Concurrent hashmap for thread-safe O(1) lookups
3. **Direct File Access**: Images stored with hash-based filenames

### Learning System

The image learner tracks:
- Successful prompt patterns
- Effective style modifiers
- Generation time metrics
- Dimension preferences

This data improves future generations by:
- Suggesting better prompt enhancements
- Predicting optimal parameters
- Reducing generation time

### Cache Management

- **LRU Eviction**: Removes least recently used images when cache is full
- **Persistent Index**: Cache survives restarts
- **Atomic Operations**: Thread-safe concurrent access

## Example Code

```rust
use think_ai_image_gen::{ImageGenerator, ImageGenConfig, ImageGenerationRequest};

#[tokio::main]
async fn main() -> Result<()> {
    // Load config from environment
    let config = ImageGenConfig::from_env()?;
    
    // Create generator
    let generator = ImageGenerator::new(config).await?;
    
    // Generate image
    let request = ImageGenerationRequest {
        prompt: "a serene mountain landscape".to_string(),
        negative_prompt: Some("people, buildings".to_string()),
        width: Some(1024),
        height: Some(768),
        num_images: Some(1),
        guidance_scale: Some(7.5),
        model_id: None,
    };
    
    let result = generator.generate(request).await?;
    
    if result.cache_hit {
        println!("Retrieved from cache!");
    } else {
        println!("Generated in {}ms", result.metadata.generation_time_ms);
    }
    
    Ok(())
}
```

## Security

- API keys are stored in `.env` files (gitignored)
- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly

## Performance Metrics

- **Cache Hit Rate**: Typically 60-80% after initial usage
- **Retrieval Time**: <1ms for cached images
- **Generation Time**: 5-30s for new images (API dependent)
- **Storage Efficiency**: Automatic compression and eviction

## Future Enhancements

1. **Local Model Integration**: Support for Stable Diffusion
2. **Distributed Cache**: Redis-based shared cache
3. **Advanced Learning**: Neural network for prompt optimization
4. **Batch Generation**: Parallel API calls for multiple images
5. **Style Transfer**: Learn artistic styles from generated images
## Author

- **champi-dev** - [danielsarcor@gmail.com](mailto:danielsarcor@gmail.com)
- GitHub: [https://github.com/champi-dev/think_ai](https://github.com/champi-dev/think_ai)
