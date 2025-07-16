// Fixed parseMarkdown function that properly handles line breaks and spacing

function parseMarkdown(text) {
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Don't over-clean the text - preserve original formatting
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
        return '<ol>' + match + '</ol>';
    });
    
    // Unordered lists
    result = result.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
    result = result.replace(/(<li>(?!class).*<\/li>\s*)+/gs, (match) => {
        return '<ul>' + match + '</ul>';
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
    
    // Step 9: CRITICAL FIX - Proper paragraph and line break handling
    // First, normalize line endings
    result = result.replace(/\r\n/g, '\n');
    
    // Split into blocks by double newlines (paragraphs)
    const blocks = result.split(/\n\n+/);
    
    result = blocks.map(block => {
        // Skip if already wrapped in HTML tags
        if (block.trim().match(/^<[^>]+>/)) {
            return block;
        }
        
        // Handle single newlines within blocks
        // Check if block has newlines
        if (block.includes('\n')) {
            // Replace single newlines with <br> tags
            const lines = block.split('\n').map(line => line.trim()).filter(line => line);
            if (lines.length > 0) {
                return '<p>' + lines.join('<br>') + '</p>';
            }
        } else if (block.trim()) {
            // Single line paragraph
            return '<p>' + block.trim() + '</p>';
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

// Test cases
const testCases = [
    {
        name: "Single line breaks",
        input: "Line 1\nLine 2\nLine 3",
        expected: "<p>Line 1<br>Line 2<br>Line 3</p>"
    },
    {
        name: "Paragraphs with double newlines",
        input: "Paragraph 1\n\nParagraph 2\n\nParagraph 3",
        expected: "<p>Paragraph 1</p>\n<p>Paragraph 2</p>\n<p>Paragraph 3</p>"
    },
    {
        name: "Mixed content",
        input: "# Title\n\nFirst paragraph with **bold**.\n\nSecond paragraph with:\n- Item 1\n- Item 2",
        expected: "Should have h1, two paragraphs, and a list"
    },
    {
        name: "Code with line breaks",
        input: "Here's code:\n```python\ndef test():\n    return True\n```\nAfter code",
        expected: "Should preserve code formatting"
    }
];

// Run tests
console.log("Testing parseMarkdown fixes:\n");
testCases.forEach(test => {
    console.log(`Test: ${test.name}`);
    console.log(`Input: ${JSON.stringify(test.input)}`);
    const result = parseMarkdown(test.input);
    console.log(`Output: ${result}`);
    console.log(`---\n`);
});