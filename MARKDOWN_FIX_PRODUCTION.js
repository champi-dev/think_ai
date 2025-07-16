// PRODUCTION FIX for parseMarkdown function
// This fixes:
// 1. Single line breaks not rendering (they should become <br> tags)
// 2. Double line breaks not creating proper paragraphs
// 3. Weird spacing in messages
// 4. Proper handling of mixed content

function parseMarkdown(text) {
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // IMPORTANT: Don't over-clean the text - preserve original formatting
    let result = text;
    
    // Step 1: Handle code blocks FIRST (to protect their content)
    const codeBlocks = [];
    result = result.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
        const placeholder = `__CODE_BLOCK_${codeBlocks.length}__`;
        codeBlocks.push(`<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`);
        return placeholder;
    });
    
    // Step 2: Handle inline code
    const inlineCodes = [];
    result = result.replace(/`([^`]+)`/g, (match, code) => {
        const placeholder = `__INLINE_CODE_${inlineCodes.length}__`;
        inlineCodes.push(`<code>${escapeHtml(code)}</code>`);
        return placeholder;
    });
    
    // Step 3: Headers (must be on their own line)
    result = result.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    result = result.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    result = result.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Step 4: Lists
    // Ordered lists
    result = result.replace(/^\d+\.\s+(.+)$/gm, '<li class="numbered">$1</li>');
    result = result.replace(/(<li class="numbered">.*<\/li>\s*)+/gs, (match) => {
        return '<ol style="margin: 10px 0; padding-left: 30px;">' + match + '</ol>';
    });
    
    // Unordered lists  
    result = result.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
    result = result.replace(/(<li>(?!class).*<\/li>\s*)+/gs, (match) => {
        return '<ul style="margin: 10px 0; padding-left: 30px;">' + match + '</ul>';
    });
    
    // Step 5: Bold and italic
    result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    result = result.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Step 6: Links
    result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // Step 7: Blockquotes
    result = result.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
    
    // Step 8: Horizontal rules
    result = result.replace(/^---+$/gm, '<hr>');
    
    // Step 9: Paragraphs and line breaks - FIXED VERSION
    // First, normalize line endings
    result = result.replace(/\r\n/g, '\n');
    
    // Split by double newlines to identify paragraphs
    const paragraphs = result.split(/\n\n+/);
    
    result = paragraphs.map(para => {
        // Skip if already wrapped in HTML tags
        if (para.trim().match(/^<[^>]+>/)) {
            return para;
        }
        
        // Handle single newlines within paragraphs
        if (para.includes('\n')) {
            // Split by newlines and filter empty lines
            const lines = para.split('\n').map(line => line.trim()).filter(line => line);
            if (lines.length > 0) {
                // Join with <br> for line breaks within paragraph
                return '<p>' + lines.join('<br>') + '</p>';
            }
        } else if (para.trim()) {
            // Single line paragraph
            return '<p>' + para.trim() + '</p>';
        }
        return '';
    }).filter(p => p).join('\n');
    
    // Step 10: Restore code blocks and inline code
    codeBlocks.forEach((code, i) => {
        result = result.replace(`__CODE_BLOCK_${i}__`, code);
    });
    
    inlineCodes.forEach((code, i) => {
        result = result.replace(`__INLINE_CODE_${i}__`, code);
    });
    
    return result;
}

// Additional CSS that should be added to improve rendering:
const additionalCSS = `
/* Improved message styling */
.message-content p {
    margin: 10px 0;
    line-height: 1.6;
}

.message-content p:first-child {
    margin-top: 0;
}

.message-content p:last-child {
    margin-bottom: 0;
}

.message-content br {
    display: block;
    content: "";
    margin-top: 0.5em;
}

.message-content h1,
.message-content h2,
.message-content h3 {
    margin: 15px 0 10px 0;
    font-weight: 600;
}

.message-content ul,
.message-content ol {
    margin: 10px 0;
    padding-left: 30px;
}

.message-content li {
    margin: 5px 0;
}

.message-content blockquote {
    border-left: 4px solid #6366f1;
    padding-left: 15px;
    margin: 10px 0;
    color: #666;
}

.message-content pre {
    background: #f4f4f4;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    margin: 10px 0;
}

.message-content code {
    background: #f4f4f4;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
}

.message-content hr {
    border: none;
    border-top: 1px solid #e9ecef;
    margin: 20px 0;
}
`;

// Test the fix
console.log("=== MARKDOWN FIX TEST ===");
console.log("Test 1 - Line breaks:");
console.log(parseMarkdown("Line 1\nLine 2\nLine 3"));
console.log("\nTest 2 - Paragraphs:");
console.log(parseMarkdown("Para 1\n\nPara 2\n\nPara 3"));
console.log("\nTest 3 - Mixed:");
console.log(parseMarkdown("# Title\n\nParagraph with\nmultiple lines.\n\n- List item 1\n- List item 2"));