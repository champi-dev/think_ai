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
