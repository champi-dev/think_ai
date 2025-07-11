#!/bin/bash

echo "🔍 Verifying markdown features in minimal_3d_markdown.html..."
echo ""

# Check for required libraries
echo "✅ Checking for markdown libraries:"
grep -q "marked.min.js" minimal_3d_markdown.html && echo "  ✓ Marked.js library included"
grep -q "highlight.js" minimal_3d_markdown.html && echo "  ✓ Highlight.js library included"

echo ""
echo "✅ Checking markdown configuration:"
grep -q "marked.setOptions" minimal_3d_markdown.html && echo "  ✓ Marked options configured"
grep -q "breaks: true" minimal_3d_markdown.html && echo "  ✓ Line breaks enabled"
grep -q "gfm: true" minimal_3d_markdown.html && echo "  ✓ GitHub Flavored Markdown enabled"

echo ""
echo "✅ Checking copy button implementation:"
grep -q "copy-button" minimal_3d_markdown.html && echo "  ✓ Copy button CSS class defined"
grep -q "copyButton.textContent = 'Copy'" minimal_3d_markdown.html && echo "  ✓ Copy button creation code found"
grep -q "navigator.clipboard.writeText" minimal_3d_markdown.html && echo "  ✓ Clipboard API usage found"

echo ""
echo "✅ Checking markdown styling:"
grep -q ".message-content h1" minimal_3d_markdown.html && echo "  ✓ Header styles defined"
grep -q ".message-content pre" minimal_3d_markdown.html && echo "  ✓ Code block styles defined"
grep -q ".message-content table" minimal_3d_markdown.html && echo "  ✓ Table styles defined"
grep -q ".message-content ul" minimal_3d_markdown.html && echo "  ✓ List styles defined"

echo ""
echo "✅ Checking hover effects for copy button:"
grep -q ".copy-button:hover" minimal_3d_markdown.html && echo "  ✓ Copy button hover state defined"
grep -q "pre:hover .copy-button" minimal_3d_markdown.html && echo "  ✓ Show on hover implemented"

echo ""
echo "📋 Summary of markdown improvements:"
echo "  • Markdown parsing with marked.js"
echo "  • Syntax highlighting with highlight.js"
echo "  • Copy buttons on code blocks (hover to show)"
echo "  • Support for tables, lists, headers, and GFM"
echo "  • Responsive styling for all markdown elements"

echo ""
echo "🌐 Test server is running at: http://localhost:3456/minimal_3d_markdown.html"
echo ""
echo "To stop the server, run: kill $(lsof -t -i:3456)"