#!/bin/bash
set -e

echo "📚 Generating documentation..."

# Generate Rust docs
echo "🦀 Generating Rust documentation..."
cargo doc --no-deps --document-private-items

# Create docs directory
mkdir -p docs

# Copy Rust docs
cp -r target/doc/* docs/

# Generate index.html
cat > docs/index.html << 'HTML_EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .section { margin: 20px 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Think AI Documentation</h1>
    
    <div class="section">
        <h2>Rust API Documentation</h2>
        <ul>
            <li><a href="think_ai_core/index.html">think-ai-core</a> - Core O(1) engine</li>
            <li><a href="think_ai_vector/index.html">think-ai-vector</a> - Vector search with LSH</li>
            <li><a href="think_ai_cache/index.html">think-ai-cache</a> - Caching system</li>
            <li><a href="think_ai_webapp/index.html">think-ai-webapp</a> - Web interface</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Quick Links</h2>
        <ul>
            <li><a href="https://github.com/champi-dev/think_ai">GitHub Repository</a></li>
            <li><a href="https://thinkai-production.up.railway.app">Live Demo</a></li>
            <li><a href="https://www.npmjs.com/package/thinkai-quantum">npm Package</a></li>
            <li><a href="https://pypi.org/project/thinkai-quantum/">PyPI Package</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>Author</h2>
        <p>Created by <a href="mailto:danielsarcor@gmail.com">champi-dev</a></p>
    </div>
</body>
</html>
HTML_EOF

echo "✅ Documentation generated in docs/"
