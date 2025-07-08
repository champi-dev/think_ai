# Think AI Image Generation Examples

## Quick Start

1. First, run the setup script to configure your API key:
```bash
./setup-image-gen.sh
```

2. Test the image generation:
```bash
./test-image-generation.sh
```

## Example Commands

### Basic Generation
```bash
./target/release/think-ai-image generate "a peaceful zen garden" -o zen.png
```

### High-Quality Portrait
```bash
./target/release/think-ai-image generate "portrait of a wise AI teacher, digital painting" \
  --width 768 \
  --height 1024 \
  --negative "cartoon, anime, low quality" \
  --output teacher.png
```

### Landscape Scene
```bash
./target/release/think-ai-image generate "vast alien landscape with two moons, sci-fi art" \
  --width 1920 \
  --height 1080 \
  --output alien_world.png
```

### Abstract Art
```bash
./target/release/think-ai-image generate "abstract representation of consciousness, vibrant colors" \
  --width 1024 \
  --height 1024 \
  --output consciousness.png
```

## Advanced Usage

### Batch Generation Script
```bash
#!/bin/bash
# batch-generate.sh

prompts=(
  "sunrise over mountains, photorealistic"
  "underwater coral reef, vivid colors"
  "ancient library, mystical atmosphere"
  "futuristic transportation hub"
  "quantum computer visualization"
)

for i in "${!prompts[@]}"; do
  echo "Generating image $((i+1))/${#prompts[@]}: ${prompts[$i]}"
  ./target/release/think-ai-image generate "${prompts[$i]}" -o "batch_$i.png"
done

# Show cache statistics
./target/release/think-ai-image stats
```

### Interactive Image Generator
```bash
#!/bin/bash
# interactive-image-gen.sh

while true; do
  echo ""
  echo "🎨 Think AI Image Generator"
  echo "=========================="
  echo "Enter a prompt (or 'quit' to exit):"
  read -r prompt
  
  if [ "$prompt" = "quit" ]; then
    break
  fi
  
  echo "Output filename (default: output.png):"
  read -r filename
  filename=${filename:-output.png}
  
  echo "Width (default: 512):"
  read -r width
  width=${width:-512}
  
  echo "Height (default: 512):"
  read -r height
  height=${height:-512}
  
  echo ""
  echo "Generating image..."
  ./target/release/think-ai-image generate "$prompt" \
    --width "$width" \
    --height "$height" \
    --output "$filename"
done
```

## Performance Tips

1. **Leverage O(1) Cache**: Reuse similar prompts to get instant results
2. **Batch Similar Requests**: Group similar styles together for learning
3. **Monitor Cache Size**: Use `stats` command to track cache usage
4. **Optimize Prompts**: The system learns from successful generations

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $LEONARDO_API_KEY

# Reload environment
source .env
```

### Cache Issues
```bash
# View cache statistics
./target/release/think-ai-image stats

# Clear cache if needed
./target/release/think-ai-image clear

# Check cache directory
ls -la ./image_cache/
```

### Debug Mode
```bash
# Run with debug logging
RUST_LOG=debug ./target/release/think-ai-image generate "test prompt" -o test.png
```