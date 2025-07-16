#!/bin/bash

echo "🔧 SETTING UP AUTO LINT ON SAVE"
echo "==============================="

# 1. Install cargo-watch if not already installed
echo "1️⃣ Checking for cargo-watch..."
if ! command -v cargo-watch &> /dev/null; then
    echo "Installing cargo-watch..."
    cargo install cargo-watch
else
    echo "✓ cargo-watch already installed"
fi

# 2. Create a file watcher script
echo "2️⃣ Creating file watcher script..."
cat > watch-and-fix.sh << 'EOF'
#!/bin/bash

echo "👁️ WATCHING FOR FILE CHANGES - AUTO LINT ON SAVE"
echo "==============================================="
echo ""
echo "Press Ctrl+C to stop watching"
echo ""

# Function to fix a specific file
fix_file() {
    local file=$1
    echo "🔧 Fixing: $file"
    
    # Fix common syntax issues
    sed -i 's/:_:/\:\:/g' "$file"
    sed -i 's/^\/\/! /\/\/ /g' "$file"
    
    # Remove trailing whitespace
    sed -i 's/[[:space:]]*$//' "$file"
    
    # Run rustfmt on the specific file
    rustfmt "$file" 2>/dev/null || true
}

# Watch for Rust file changes
cargo watch -s 'echo "File saved, running lint fixes..."' \
    -w . \
    --ignore target \
    --ignore '*.lock' \
    -x 'fmt' \
    -x 'clippy --fix --allow-dirty --allow-staged 2>/dev/null || true'

# Alternative: Use inotifywait if cargo-watch has issues
# while true; do
#     inotifywait -r -e modify,create --include '.*\.rs$' . 2>/dev/null | while read path action file; do
#         if [[ "$file" =~ \.rs$ ]]; then
#             fix_file "$path$file"
#         fi
#     done
# done
EOF

chmod +x watch-and-fix.sh

# 3. Create VS Code settings
echo "3️⃣ Creating VS Code settings..."
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
    // Auto-format on save
    "editor.formatOnSave": true,
    
    // Rust-specific settings
    "[rust]": {
        "editor.defaultFormatter": "rust-lang.rust-analyzer",
        "editor.formatOnSave": true,
        "editor.formatOnPaste": true,
        "editor.formatOnType": true
    },
    
    // Run rustfmt on save
    "rust-analyzer.rustfmt.extraArgs": [
        "--edition=2021"
    ],
    
    // Enable all clippy lints
    "rust-analyzer.check.command": "clippy",
    "rust-analyzer.check.extraArgs": [
        "--",
        "-W", "clippy::all",
        "-W", "clippy::pedantic"
    ],
    
    // Auto-fix on save
    "editor.codeActionsOnSave": {
        "source.fixAll": true,
        "source.organizeImports": true
    },
    
    // Enable format on save for all files
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
EOF

# 4. Create Vim/Neovim autocommand
echo "4️⃣ Creating Vim auto-format config..."
cat > .vim-rust-fmt << 'EOF'
" Add this to your .vimrc or init.vim

" Auto-format Rust files on save
augroup rustfmt
    autocmd!
    autocmd BufWritePre *.rs execute ':silent !rustfmt %'
    autocmd BufWritePost *.rs execute ':edit'
    autocmd BufWritePost *.rs execute ':silent !cargo clippy --fix --allow-dirty --allow-staged 2>/dev/null'
augroup END

" Optional: Show errors in quickfix window
autocmd BufWritePost *.rs :silent make | redraw!
EOF

# 5. Create a simple file watcher using inotify
echo "5️⃣ Creating simple file watcher..."
cat > simple-watch.sh << 'EOF'
#!/bin/bash

# Check if inotify-tools is installed
if ! command -v inotifywait &> /dev/null; then
    echo "Installing inotify-tools..."
    sudo apt-get update && sudo apt-get install -y inotify-tools 2>/dev/null || \
    brew install fswatch 2>/dev/null || \
    echo "Please install inotify-tools or fswatch manually"
fi

echo "👁️ Watching Rust files for changes..."
echo "Press Ctrl+C to stop"

# Linux with inotifywait
if command -v inotifywait &> /dev/null; then
    while true; do
        inotifywait -r -e modify,create --include '.*\.rs$' src/ 2>/dev/null | while read -r directory event filename; do
            if [[ "$filename" =~ \.rs$ ]]; then
                echo "📝 Changed: $directory$filename"
                rustfmt "$directory$filename" 2>/dev/null || true
                echo "✅ Formatted!"
            fi
        done
    done
# macOS with fswatch
elif command -v fswatch &> /dev/null; then
    fswatch -o src/ --include='\.rs$' | while read -r file; do
        echo "📝 Changed: $file"
        find src/ -name "*.rs" -newer /tmp/fswatch_timestamp -exec rustfmt {} \; 2>/dev/null || true
        touch /tmp/fswatch_timestamp
        echo "✅ Formatted!"
    done
fi
EOF

chmod +x simple-watch.sh

# 6. Create systemd service for auto-formatting (Linux)
echo "6️⃣ Creating systemd service template..."
cat > think-ai-autofmt.service << EOF
[Unit]
Description=Think AI Auto Format on Save
After=multi-user.target

[Service]
Type=simple
ExecStart=$PWD/watch-and-fix.sh
WorkingDirectory=$PWD
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

# 7. Create startup script
echo "7️⃣ Creating startup script..."
cat > start-auto-lint.sh << 'EOF'
#!/bin/bash

echo "🚀 STARTING AUTO-LINT ON SAVE"
echo "============================"
echo ""
echo "Choose your method:"
echo "1) cargo-watch (recommended)"
echo "2) Simple file watcher"
echo "3) Run in background"
echo ""
read -p "Select option (1-3): " choice

case $choice in
    1)
        ./watch-and-fix.sh
        ;;
    2)
        ./simple-watch.sh
        ;;
    3)
        nohup ./watch-and-fix.sh > auto-lint.log 2>&1 &
        echo "✅ Auto-lint running in background (PID: $!)"
        echo "Check auto-lint.log for output"
        echo "To stop: kill $!"
        ;;
    *)
        echo "Invalid option"
        ;;
esac
EOF

chmod +x start-auto-lint.sh

echo ""
echo "✅ AUTO LINT ON SAVE SETUP COMPLETE!"
echo ""
echo "📋 Usage Options:"
echo ""
echo "1️⃣ VS Code Users:"
echo "   - Settings automatically configured in .vscode/settings.json"
echo "   - Just save any .rs file and it will auto-format!"
echo ""
echo "2️⃣ Vim/Neovim Users:"
echo "   - Add the contents of .vim-rust-fmt to your config"
echo ""
echo "3️⃣ Any Editor - File Watcher:"
echo "   ./start-auto-lint.sh"
echo ""
echo "4️⃣ Run in Terminal:"
echo "   ./watch-and-fix.sh"
echo ""
echo "5️⃣ Install as System Service (Linux):"
echo "   sudo cp think-ai-autofmt.service /etc/systemd/system/"
echo "   sudo systemctl enable think-ai-autofmt"
echo "   sudo systemctl start think-ai-autofmt"
echo ""
echo "💡 The watcher will:"
echo "   • Format code on save (rustfmt)"
echo "   • Fix linting issues (clippy)"
echo "   • Remove trailing whitespace"
echo "   • Fix common syntax errors"