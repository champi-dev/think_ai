#!/bin/bash

# Script to fix markdown rendering in webapp_temp.html

echo "🔧 Fixing Markdown Rendering in webapp_temp.html"
echo "=============================================="

# Backup the original
cp webapp_temp.html webapp_temp.html.backup

# Create the improved parseMarkdown function
cat > /tmp/improved_markdown.js << 'EOF'
        function parseMarkdownImproved(text) {
            let result = text;
            
            // Normalize line endings
            result = result.replace(/\r\n/g, '\n');
            
            // Step 1: Protect code blocks
            const codeBlocks = [];
            result = result.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
                const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
                codeBlocks.push(`<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`);
                return placeholder;
            });
            
            // Step 2: Protect inline code  
            const inlineCodes = [];
            result = result.replace(/`([^`\n]+)`/g, (match, code) => {
                const placeholder = `__INLINE_CODE_${inlineCodes.length}__`;
                inlineCodes.push(`<code>${escapeHtml(code)}</code>`);
                return placeholder;
            });
            
            // Step 3: Headers (must be on their own line)
            result = result.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
            result = result.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
            result = result.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');
            
            // Step 4: Handle lists more carefully
            const lines = result.split('\n');
            let inUL = false;
            let inOL = false;
            let processedLines = [];
            
            for (let i = 0; i < lines.length; i++) {
                let line = lines[i];
                const trimmed = line.trim();
                
                // Check for unordered list
                if (/^[-*]\s+/.test(trimmed)) {
                    if (!inUL) {
                        if (inOL) {
                            processedLines.push('</ol>');
                            inOL = false;
                        }
                        processedLines.push('<ul>');
                        inUL = true;
                    }
                    line = trimmed.replace(/^[-*]\s+(.+)$/, '<li>$1</li>');
                }
                // Check for ordered list
                else if (/^\d+\.\s+/.test(trimmed)) {
                    if (!inOL) {
                        if (inUL) {
                            processedLines.push('</ul>');
                            inUL = false;
                        }
                        processedLines.push('<ol>');
                        inOL = true;
                    }
                    line = trimmed.replace(/^\d+\.\s+(.+)$/, '<li>$1</li>');
                }
                // Empty line or non-list item
                else if (trimmed === '' || !trimmed.startsWith('<li>')) {
                    // Close any open lists
                    if (inUL) {
                        processedLines.push('</ul>');
                        inUL = false;
                    }
                    if (inOL) {
                        processedLines.push('</ol>');
                        inOL = false;
                    }
                }
                
                processedLines.push(line);
            }
            
            // Close any remaining lists
            if (inUL) processedLines.push('</ul>');
            if (inOL) processedLines.push('</ol>');
            
            result = processedLines.join('\n');
            
            // Step 5: Text formatting (after lists to avoid conflicts)
            // Bold
            result = result.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
            // Italic - both * and _
            result = result.replace(/(?<![\*\w])\*([^\*\n]+)\*(?![\*\w])/g, '<em>$1</em>');
            result = result.replace(/(?<![\w])_([^_\n]+)_(?![\w])/g, '<em>$1</em>');
            // Strikethrough
            result = result.replace(/~~([^~]+)~~/g, '<del>$1</del>');
            
            // Step 6: Links
            result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
            
            // Step 7: Horizontal rules
            result = result.replace(/^---+$/gm, '<hr>');
            
            // Step 8: Blockquotes
            result = result.replace(/^>\s+(.+)$/gm, '<blockquote>$1</blockquote>');
            
            // Step 9: Paragraphs and line breaks
            const blocks = result.split(/\n\n+/);
            result = blocks.map(block => {
                // Skip if already HTML
                if (block.match(/^<(h[1-6]|ul|ol|blockquote|pre|hr)/m)) {
                    return block;
                }
                
                // For plain text blocks
                const lines = block.split('\n').filter(line => line.trim());
                if (lines.length > 0) {
                    // Don't wrap single lines that are already list items
                    if (lines.length === 1 && lines[0].includes('<li>')) {
                        return lines[0];
                    }
                    return '<p>' + lines.join('<br>') + '</p>';
                }
                return '';
            }).filter(b => b).join('\n\n');
            
            // Step 10: Restore code
            codeBlocks.forEach((code, i) => {
                result = result.replace(`__CODE_BLOCK_${i}__`, code);
            });
            
            inlineCodes.forEach((code, i) => {
                result = result.replace(`__INLINE_CODE_${i}__`, code);
            });
            
            return result;
        }
EOF

echo "✅ Created improved markdown parser"

# Add enhanced CSS styles
cat > /tmp/markdown_styles.css << 'EOF'
        /* Enhanced markdown rendering styles */
        .message-content h1 {
            font-size: 1.8em !important;
            margin: 0.8em 0 0.5em 0 !important;
            color: #8b5cf6 !important;
            font-weight: 600 !important;
            line-height: 1.3 !important;
        }
        
        .message-content h2 {
            font-size: 1.4em !important;
            margin: 0.7em 0 0.4em 0 !important;
            color: #c4b5fd !important;
            font-weight: 600 !important;
        }
        
        .message-content h3 {
            font-size: 1.2em !important;
            margin: 0.6em 0 0.3em 0 !important;
            color: #ddd6fe !important;
            font-weight: 500 !important;
        }
        
        .message-content ul, .message-content ol {
            margin: 0.5em 0 1em 0 !important;
            padding-left: 1.8em !important;
            list-style-position: outside !important;
        }
        
        .message-content ul li {
            list-style-type: disc !important;
            margin: 0.3em 0 !important;
            padding-left: 0.2em !important;
        }
        
        .message-content ol li {
            list-style-type: decimal !important;
            margin: 0.3em 0 !important;
            padding-left: 0.2em !important;
        }
        
        .message-content ul ul {
            margin-top: 0.2em !important;
            margin-bottom: 0.2em !important;
        }
        
        .message-content del {
            text-decoration: line-through;
            opacity: 0.7;
        }
        
        .message-content blockquote {
            border-left: 4px solid #6366f1 !important;
            padding: 0.5em 0 0.5em 1em !important;
            margin: 0.5em 0 !important;
            background: rgba(99, 102, 241, 0.05) !important;
            border-radius: 0 4px 4px 0 !important;
        }
EOF

echo "✅ Created enhanced CSS styles"
echo ""
echo "📝 Instructions to apply the fix:"
echo "1. Open webapp_temp.html in your editor"
echo "2. Find the 'function parseMarkdown' (around line 1110)"
echo "3. Replace it with the contents of /tmp/improved_markdown.js"
echo "4. Add the CSS from /tmp/markdown_styles.css to the <style> section"
echo "5. Save and reload http://localhost:7777"
echo ""
echo "🧪 Test with this markdown:"
cat << 'TEST'
# Main Heading

This is **bold** and *italic* and ~~strikethrough~~.

## Lists

Unordered:
- First item
- Second item
  - Nested item

Ordered:
1. Step one
2. Step two

### Code

Inline: `console.log('hello')`

Block:
```python
def hello():
    print("O(1) performance!")
```

> This is a quote

---

[Link to docs](https://example.com)
TEST