# Markdown Test Examples

Test these examples in the Think AI chat interface to verify rendering:

## 1. Headers Test
```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header
```

## 2. Code Block with Copy Button
```python
def calculate_o1_performance():
    """Calculate O(1) performance metrics"""
    lookup_table = {"query1": "instant", "query2": "fast"}
    return lookup_table.get("query1", "default")

# Test the copy button by hovering over this code block
print(calculate_o1_performance())
```

## 3. Table Test
```markdown
| Feature | Performance | Status |
|---------|------------|--------|
| Hash Lookup | O(1) | ✅ Ready |
| Vector Search | O(1) | ✅ Ready |
| Response Time | <10ms | ✅ Ready |
| Copy Button | Instant | ✅ Added |
```

## 4. List Test
```markdown
- Unordered list item 1
  - Nested item 1.1
  - Nested item 1.2
- Unordered list item 2

1. Ordered list item 1
   1. Nested ordered 1.1
   2. Nested ordered 1.2
2. Ordered list item 2
```

## 5. Mixed Formatting Test
```markdown
This is **bold text** and this is *italic text* and this is ***bold italic***.

Here's a `inline code` example and a [link to Think AI](https://github.com/champi-dev/think_ai).

> This is a blockquote
> with multiple lines
> showing proper formatting

---

Task list example:
- [x] Add copy button to code blocks
- [x] Fix markdown rendering
- [ ] Deploy to production
```

## 6. Complex Code Example
```javascript
// O(1) Hash-based Response System
class ThinkAI {
    constructor() {
        this.responseCache = new Map();
        this.setupO1Lookup();
    }
    
    async respond(query) {
        // O(1) lookup - copy this code to test!
        const cached = this.responseCache.get(query);
        if (cached) return cached;
        
        const response = await this.generateResponse(query);
        this.responseCache.set(query, response);
        return response;
    }
}
```

## 7. Syntax Highlighting Test
```rust
// Rust O(1) implementation
use std::collections::HashMap;

fn main() {
    let mut cache: HashMap<String, String> = HashMap::new();
    cache.insert("test".to_string(), "O(1) response".to_string());
    
    // Test copy button here
    match cache.get("test") {
        Some(response) => println!("{}", response),
        None => println!("Not found"),
    }
}
```