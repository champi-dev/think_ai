#!/bin/bash
set -e

echo "Removing excessive closing braces..."

# Remove lines that only contain a closing brace at the end of files
remove_trailing_braces() {
    local file=$1
    # Count consecutive lines with only '}' at the end
    local last_line=$(tail -1 "$file")
    if [ "$last_line" = "}" ]; then
        # Remove trailing lines that only contain '}'
        sed -i ':a; /^}$/{ $d; N; ba; }' "$file"
        # Keep at least one closing brace if needed
        echo "}" >> "$file"
    fi
}

# Process all Rust files
find think-ai-consciousness think-ai-core think-ai-vector think-ai-image-gen -name "*.rs" -type f | while read file; do
    echo "Cleaning $file"
    # Remove consecutive closing braces at end of file
    awk 'NR==FNR{lines++; next} FNR==1{found=0} /^}$/{if(FNR>lines-20 && !found){found=1; print; next}} found && /^}$/{next} {print}' "$file" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done

echo "Removed excessive braces"