#!/bin/bash
set -e

echo "🔧 Fixing raw string issues in think-ai-coding.rs..."

# Create a Python script to properly fix the raw strings
cat > /tmp/fix_raw_strings.py << 'EOF'
import re
import sys

def fix_raw_strings(content):
    # Pattern to find malformed raw strings
    lines = content.split('\n')
    fixed_lines = []
    in_raw_string = False
    raw_string_delimiter = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if line starts a raw string
        if re.search(r'r#+"', line) and not in_raw_string:
            # Extract the delimiter (number of #s)
            match = re.search(r'r(#+)"', line)
            if match:
                raw_string_delimiter = match.group(1)
                in_raw_string = True
                fixed_lines.append(line)
                
                # Look ahead to find where this raw string should end
                j = i + 1
                raw_content = []
                while j < len(lines):
                    next_line = lines[j]
                    # Check if this line contains the end delimiter
                    if f'"{raw_string_delimiter}' in next_line:
                        # Found the end
                        raw_content.append(next_line)
                        fixed_lines.extend(raw_content)
                        in_raw_string = False
                        i = j
                        break
                    elif (j < len(lines) - 1 and 
                          lines[j+1].strip().startswith('description:') or 
                          lines[j+1].strip().startswith('complexity:') or
                          lines[j+1].strip().startswith('pattern:') or
                          lines[j+1].strip().startswith('language:')):
                        # This is the last line of the raw string
                        raw_content.append(next_line + f'"{raw_string_delimiter},')
                        fixed_lines.extend(raw_content)
                        in_raw_string = False
                        i = j
                        break
                    else:
                        raw_content.append(next_line)
                    j += 1
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

# Read the file
with open('think-ai-cli/src/bin/think-ai-coding.rs', 'r') as f:
    content = f.read()

# Fix the content
fixed_content = fix_raw_strings(content)

# Additional fixes for specific patterns
fixed_content = re.sub(r'(\w+)"#\s*description:', r'\1"#,\n                description:', fixed_content)
fixed_content = re.sub(r'(\w+)"#\s*complexity:', r'\1"#,\n                complexity:', fixed_content)
fixed_content = re.sub(r'(\w+)"#\s*pattern:', r'\1"#,\n                pattern:', fixed_content)

# Fix prefix errors
fixed_content = re.sub(r'(\w+)"\.to_string', r'\1 ".to_string', fixed_content)

# Fix Python f-strings and quotes
fixed_content = fixed_content.replace("f\"", "f \\\"")
fixed_content = fixed_content.replace("'", "\\'")

# Write the fixed content
with open('think-ai-cli/src/bin/think-ai-coding.rs', 'w') as f:
    f.write(fixed_content)

print("Fixed raw strings in think-ai-coding.rs")
EOF

# Run the Python fix script
cd /home/champi/Dev/think_ai
python3 /tmp/fix_raw_strings.py

# Fix think-ai-coding-v2.rs
echo "Fixing think-ai-coding-v2.rs..."
# Add closing braces if needed
OPEN_COUNT=$(grep -o '{' think-ai-cli/src/bin/think-ai-coding-v2.rs | wc -l)
CLOSE_COUNT=$(grep -o '}' think-ai-cli/src/bin/think-ai-coding-v2.rs | wc -l)

if [ $OPEN_COUNT -gt $CLOSE_COUNT ]; then
    DIFF=$((OPEN_COUNT - CLOSE_COUNT))
    echo "Adding $DIFF closing braces to think-ai-coding-v2.rs..."
    for ((i=0; i<$DIFF; i++)); do
        echo "}" >> think-ai-cli/src/bin/think-ai-coding-v2.rs
    done
fi

echo "✅ Raw string fixes applied!"