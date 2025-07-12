// Test markdown rendering in browser console
console.log("Testing markdown parser...");

const testCases = [
    {
        name: "Headers",
        input: "# H1\\n## H2\\n### H3",
        expected: ["<h1>", "<h2>", "<h3>"]
    },
    {
        name: "Bold/Italic", 
        input: "**bold** and *italic*",
        expected: ["<strong>", "<em>"]
    },
    {
        name: "Lists",
        input: "- Item 1\\n- Item 2\\n\\n1. First\\n2. Second",
        expected: ["<ul>", "<ol>", "<li>"]
    },
    {
        name: "Code",
        input: "Inline `code` and\\n```python\\nprint('hello')\\n```",
        expected: ["<code>", "<pre>"]
    }
];

// Run tests
testCases.forEach(test => {
    console.log(`\\nTesting: ${test.name}`);
    console.log(`Input: ${test.input}`);
    
    // Call the parseMarkdown function from the webapp
    if (typeof parseMarkdown === 'function') {
        const result = parseMarkdown(test.input);
        console.log(`Output HTML: ${result}`);
        
        const passed = test.expected.every(tag => result.includes(tag));
        console.log(`Result: ${passed ? '✅ PASS' : '❌ FAIL'}`);
    } else {
        console.log("❌ parseMarkdown function not found\!");
    }
});
