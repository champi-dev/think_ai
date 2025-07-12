#!/bin/bash

# Script to add marked.js to webapp_temp.html

echo "🔧 Adding marked.js to webapp_temp.html"
echo "======================================"

# Backup original
cp webapp_temp.html webapp_temp_backup_$(date +%Y%m%d_%H%M%S).html

# Create a new version with marked.js
cat > webapp_temp_marked.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Think AI</title>
    
    <!-- Add marked.js for proper markdown parsing -->
    <script src="https://cdn.jsdelivr.net/npm/marked@4.3.0/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js"></script>
    
EOF

# Extract the styles from original and append
sed -n '/<style>/,/<\/style>/p' webapp_temp.html >> webapp_temp_marked.html

# Add the closing head and opening body
echo '</head>' >> webapp_temp_marked.html
echo '<body>' >> webapp_temp_marked.html

# Extract body content (excluding script)
sed -n '/<body>/,/<script>/p' webapp_temp.html | grep -v '<body>' | grep -v '<script>' >> webapp_temp_marked.html

# Add the updated script section
cat >> webapp_temp_marked.html << 'EOF'
    <script>
        // Configure marked.js
        marked.setOptions({
            breaks: true,
            gfm: true,
            tables: true,
            pedantic: false,
            sanitize: false,
            smartLists: true,
            smartypants: false
        });
EOF

# Extract the original script content but replace parseMarkdown function
sed -n '/<script>/,/<\/script>/p' webapp_temp.html | \
    sed '/<script>/d' | \
    sed '/<\/script>/d' | \
    sed '/function parseMarkdown/,/^        }/c\
        function parseMarkdown(text) {\
            // Use marked.js for proper markdown parsing\
            try {\
                const rawHtml = marked.parse(text);\
                // Sanitize with DOMPurify for security\
                const cleanHtml = DOMPurify.sanitize(rawHtml, {\
                    ALLOWED_TAGS: ["h1", "h2", "h3", "h4", "h5", "h6", "p", "br", "hr",\
                                  "strong", "b", "em", "i", "del", "code", "pre", "blockquote",\
                                  "ul", "ol", "li", "a", "table", "thead", "tbody", "tr", "th", "td"],\
                    ALLOWED_ATTR: ["href", "target", "class", "id", "style"],\
                    ALLOW_DATA_ATTR: false\
                });\
                return cleanHtml;\
            } catch (e) {\
                console.error("Markdown parsing error:", e);\
                // Fallback to simple text with line breaks\
                return text.replace(/\\n/g, "<br>");\
            }\
        }' >> webapp_temp_marked.html

# Close the script and body tags
echo '    </script>' >> webapp_temp_marked.html
echo '</body>' >> webapp_temp_marked.html
echo '</html>' >> webapp_temp_marked.html

echo "✅ Created webapp_temp_marked.html with marked.js"
echo ""
echo "To use it:"
echo "1. Stop the current server (Ctrl+C)"
echo "2. Replace webapp_temp.html with webapp_temp_marked.html:"
echo "   mv webapp_temp_marked.html webapp_temp.html"
echo "3. Restart the server:"
echo "   python3 serve_webapp_7777_final.py"
echo ""
echo "Or test it directly:"
echo "   python3 -m http.server 8888"
echo "   Then open: http://localhost:8888/webapp_temp_marked.html"