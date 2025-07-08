#!/bin/bash

echo "🎯 AUTO-LINT ON SAVE DEMO"
echo "========================"
echo ""
echo "You now have several options for auto-linting:"
echo ""
echo "1️⃣ Start the file watcher (recommended):"
echo "   ./watch-and-fix.sh"
echo ""
echo "2️⃣ Or use the interactive starter:"
echo "   ./start-auto-lint.sh"
echo ""
echo "Let's test it! Starting the watcher in background..."
echo ""

# Start the watcher in background
nohup ./watch-and-fix.sh > auto-lint.log 2>&1 &
WATCHER_PID=$!
echo "✅ Auto-lint watcher started (PID: $WATCHER_PID)"
echo ""

# Create a test file with formatting issues
echo "Creating a test file with formatting issues..."
cat > test-auto-lint.rs << 'EOF'
// Test file with formatting issues
fn main() {
let x = 5;     // Bad indentation
let y=10;  // No spaces around =
    println!("Hello, world!")  ;  // Trailing whitespace   
}

fn unused_function() {
// This function is unused and should trigger a warning
let unused_variable = 42;
}
EOF

echo "📝 Created test-auto-lint.rs with formatting issues"
echo ""
echo "The watcher will automatically fix it when cargo-watch detects the change!"
echo ""
echo "To stop the watcher: kill $WATCHER_PID"
echo "To see watcher output: tail -f auto-lint.log"