#!/usr/bin/env python3
"""Test script to demonstrate markdown rendering improvements"""

import json
import asyncio
from aiohttp import web
import aiohttp_cors

# Test markdown content with various formatting challenges
TEST_CONTENT = """
# Markdown Rendering Test Suite

This is a comprehensive test of the markdown rendering system with improved word wrapping and line breaks.

## Long Words and URLs

Here's a very long word that should wrap properly: supercalifragilisticexpialidocious. And here's a long URL that needs to wrap: https://example.com/very/long/path/that/should/wrap/properly/without/breaking/the/layout

## Code Examples

Here's some inline code: `const longVariableName = 'This is a very long string that should wrap properly in inline code blocks';`

```javascript
// This is a code block with very long lines that should handle overflow properly
const veryLongFunctionNameThatShouldWrapProperly = (parameterOne, parameterTwo, parameterThree) => {
    return "This is a very long string that demonstrates proper code wrapping in pre blocks";
};
```

## Lists with Long Items

1. This is a numbered list item with a very long line of text that should wrap properly without breaking the list formatting or causing overflow issues
2. Another item with **bold text** and *italic text* mixed in
3. A third item with a [very long link text that should wrap](https://example.com/long/url)

- Bullet point with a very long line of text that demonstrates proper wrapping in unordered lists
- Another bullet with `inline code that might be quite long and need wrapping`
- Final bullet point

## Paragraphs and Line Breaks

This is a paragraph with multiple sentences. Each sentence should flow naturally into the next. The text should wrap at appropriate points without breaking words in the middle.

This is a second paragraph separated by a blank line. It contains a mix of **bold**, *italic*, and `code` formatting. The formatting should be preserved while still allowing proper word wrapping.

Here's a paragraph with manual line breaks:
First line of text
Second line of text  
Third line with trailing spaces for hard break

## Blockquotes

> This is a blockquote with a very long line of text that should wrap properly within the blockquote styling. The left border and background should extend to accommodate wrapped text.

## Mixed Content

Here's a paragraph followed by a list:

The following items demonstrate various formatting combinations:

1. **Bold text** with *italic text* and `inline code`
2. A [link](https://example.com) with surrounding text that might wrap
3. Multiple formatting: ***bold and italic*** with `code`

### Complex Nesting

- Parent list item
  - Nested item with long text that should wrap properly
  - Another nested item with **formatting**
- Back to parent level

## Special Characters and Edge Cases

Here's text with special characters: & < > " ' that should be properly escaped.

Mathematical expressions: E = mc² and chemical formulas: H₂O

Unicode test: 🚀 🌟 🎯 emoji should render properly

---

## Conclusion

This test demonstrates that all markdown elements render beautifully with proper word wrapping, no word splitting, and clean line breaks throughout the document.
"""

async def handle_chat(request):
    """Handle chat requests with test markdown content"""
    data = await request.json()
    message = data.get('message', '')
    
    # Return test markdown content for any message
    return web.json_response({
        'response': TEST_CONTENT
    })

async def handle_index(request):
    """Serve the fixed HTML file"""
    with open('minimal_3d_fixed.html', 'r') as f:
        return web.Response(text=f.read(), content_type='text/html')

def create_app():
    """Create the test application"""
    app = web.Application()
    
    # Configure CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Add routes
    app.router.add_get('/', handle_index)
    app.router.add_post('/chat', handle_chat)
    
    # Configure CORS for all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    return app

if __name__ == '__main__':
    print("Starting Markdown Test Server...")
    print("Open http://localhost:8888 in your browser")
    print("Send any message to see the comprehensive markdown test")
    
    app = create_app()
    web.run_app(app, host='localhost', port=8888)