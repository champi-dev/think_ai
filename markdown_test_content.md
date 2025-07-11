# Comprehensive Markdown Test Document

This document contains all standard markdown elements to test Think AI's markdown rendering capabilities.

## Headings

# Heading Level 1
## Heading Level 2
### Heading Level 3
#### Heading Level 4
##### Heading Level 5
###### Heading Level 6

## Text Formatting

This is a paragraph with **bold text**, *italic text*, and ***bold italic text***.

You can also use _underscores for italic_ and __double underscores for bold__.

~~Strikethrough text~~ (if supported)

## Lists

### Unordered List
- First item
- Second item
  - Nested item 1
  - Nested item 2
    - Deep nested item
- Third item

### Ordered List
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step

### Mixed Lists
1. First ordered item
   - Unordered sub-item
   - Another unordered sub-item
2. Second ordered item
   1. Ordered sub-item
   2. Another ordered sub-item

## Links and Images

[This is a link to OpenAI](https://openai.com)

[Link with title](https://github.com "GitHub Homepage")

![Alt text for image](https://via.placeholder.com/150 "Image Title")

## Code

### Inline Code
Use `console.log()` to print to console in JavaScript.

### Code Blocks

```javascript
// JavaScript code block
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10)); // Output: 55
```

```python
# Python code block
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([3, 6, 8, 10, 1, 2, 1]))
```

```rust
// Rust code block
fn main() {
    let mut vec = vec![1, 2, 3, 4, 5];
    vec.iter_mut().for_each(|x| *x *= 2);
    println!("{:?}", vec); // [2, 4, 6, 8, 10]
}
```

## Blockquotes

> This is a blockquote. It can contain multiple lines.
> 
> It can also contain **formatted text** and even `code`.

> Blockquotes can be nested
>> Like this
>>> And even deeper

## Horizontal Rules

---

Three or more hyphens

***

Three or more asterisks

___

Three or more underscores

## Tables

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row 1, Col 1 | Row 1, Col 2 | Row 1, Col 3 |
| Row 2, Col 1 | Row 2, Col 2 | Row 2, Col 3 |
| Row 3, Col 1 | Row 3, Col 2 | Row 3, Col 3 |

### Aligned Tables

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left | Center | Right |
| Text | Text | Text |
| More | More | More |

## Task Lists

- [x] Completed task
- [ ] Uncompleted task
- [x] Another completed task
  - [ ] Sub-task 1
  - [x] Sub-task 2

## HTML Elements (if supported)

<details>
<summary>Click to expand</summary>
This is hidden content that can be expanded.
</details>

## Escaping Characters

\*This text has escaped asterisks\*

\`This has escaped backticks\`

## Line Breaks

This is line one.  
This is line two (with two spaces before line break).

This is a new paragraph (with blank line between).

## Emoji Support

Here are some emojis: 😀 🚀 💻 🎉 ✨

## Mathematical Expressions (if supported)

Inline math: $E = mc^2$

Block math:
$$
\frac{n!}{k!(n-k)!} = \binom{n}{k}
$$

## Special Characters

Copyright © 2025
Trademark ™
Registered ®
En dash – Em dash —
Ellipsis…

## Complex Nested Example

Here's a complex example combining multiple elements:

1. **First main point**
   - Sub-point with `inline code`
   - Another sub-point with a [link](https://example.com)
   
2. **Second main point**
   > A blockquote within a list
   > with multiple lines
   
   ```python
   # Code block in a list
   def example():
       return "Hello, World!"
   ```

3. **Third main point**
   
   | Feature | Status |
   |---------|--------|
   | Markdown | ✅ |
   | Rendering | ✅ |

## Edge Cases

### Empty Code Block
```
```

### Long Inline Code
This is a very long inline code example: `const longVariableName = "This is a very long string that might cause wrapping issues in the rendered output";`

### Unicode in Code
```javascript
const greeting = "Hello, 世界! 🌍";
console.log(greeting);
```

### Deeply Nested Lists
1. Level 1
   1. Level 2
      1. Level 3
         1. Level 4
            1. Level 5
               - Mixed unordered
               - In deep nesting

## Performance Test

This section contains a large amount of text to test rendering performance:

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

---

End of comprehensive markdown test document.