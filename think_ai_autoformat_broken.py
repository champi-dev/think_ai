import argparse
import ast
import json
import os
import re
import subprocess
import sys

from pathlib import Path
from typing import List, Tuple, Optional

"""
Think AI Auto-Formatter - Prettier-like formatting for Think AI
Fully integrated with Think AI Linter
Runs on pre-commit hooks and file save
O(1) performance with intelligent formatting
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class ThinkAIAutoFormat:
"""Smart auto-formatter that understands Python syntax"""

    def __init__(self, line_length: int = 200):
        self.line_length = line_length
        self.indent_size = 4
        self.files_formatted = 0

        def format_file(self, filepath: Path) -> bool:
"""Format a single Python file intelligently"""
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = f.read()

# Parse AST to understand structure
                    try:
                        tree = ast.parse(original, filename=str(filepath))
                        except SyntaxError:
# File has syntax errors, try basic formatting
                            formatted = self._basic_format(original)
                        else:
# File is valid Python, do smart formatting
                            formatted = self._smart_format(original, tree)

                            if formatted != original:
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    f.write(formatted)
                                    self.files_formatted += 1
                                    return True

                                return False

                            except Exception as e:
                                print(f"Error formatting {filepath}: {e}")
                                return False

                            def _basic_format(self, content: str) -> str:
"""Basic formatting for files with syntax errors"""
                                lines = content.split('\n')
                                formatted_lines = []

                                for line in lines:
# Fix basic spacing issues
                                    line = self._fix_basic_spacing(line)
# Fix trailing whitespace
                                    line = line.rstrip()
                                    formatted_lines.append(line)

# Ensure file ends with newline
                                    if formatted_lines and formatted_lines[-1]:
                                        formatted_lines.append('')

                                        return '\n'.join(formatted_lines)

                                    def _smart_format(
                                    self, content: str, tree: ast.AST) -> str:
"""Smart formatting using AST understanding"""
                                        lines = content.split('\n')

# First pass: organize imports
                                        lines = self._organize_imports(lines, tree)

# Second pass: fix indentation
                                        lines = self._fix_indentation(lines)

# Third pass: fix spacing
                                        lines = self._fix_spacing(lines)

# Fourth pass: fix line length
                                        lines = self._fix_line_length(lines)

# Final pass: clean up
                                        lines = self._final_cleanup(lines)

                                        return '\n'.join(lines)

                                    def _organize_imports(
                                    self, lines: List[str], tree: ast.AST) -> List[str]:
"""Organize imports according to PEP 8"""
                                        import_lines = []
                                        from_imports = []
                                        other_lines = []

# Extract imports
                                        for node in ast.walk(tree):
                                            if isinstance(node, ast.Import):
                                                line_num = node.lineno - 1
                                                if line_num < len(lines):
                                                    import_lines.append(
                                                    (node.names[0].name, lines[line_num].strip()))
                                                elif isinstance(node, ast.ImportFrom):
                                                    line_num = node.lineno - 1
                                                    if line_num < len(lines):
                                                        module = node.module or ''
                                                        from_imports.append(
                                                        (module, lines[line_num].strip()))

# Sort imports
                                                        import_lines.sort(
                                                        key=lambda x: x[0])
                                                        from_imports.sort(
                                                        key=lambda x: x[0])

# Find where imports end
                                                        import_end = 0
                                                        for i, line in enumerate(
                                                        lines):
                                                            if line.strip() and not (line.strip().startswith('import ') or
                                                            line.strip().startswith('from ') or
                                                            line.strip().startswith('#')):
                                                                import_end = i
                                                                break

# Reconstruct with
# organized imports
                                                            result = []

# Standard library imports
                                                            for _, line in import_lines:
                                                                if not any(
                                                                line.startswith(
                                                                f'import {pkg}') for pkg in [
                                                                'numpy',
                                                                'torch',
                                                                'pandas']):
                                                                    result.append(line)

                                                                    if result:
                                                                        result.append(
                                                                        '')

# Third-party
# imports
                                                                        for _, line in from_imports:
                                                                            result.append(
                                                                            line)

                                                                            if from_imports:
                                                                                result.append(
                                                                                '')

# Add
# remaining
# code
                                                                                result.extend(
                                                                                lines[import_end:])

                                                                                return result

                                                                            def _fix_basic_spacing(
                                                                            self, line: str) -> str:
"""Fix basic spacing issues without breaking code"""
# Don't
# modify
# strings
                                                                                if '"""' in line or "'''" in line:
                                                                                    return line

# Fix
# spacing
# around
# operators
# (but
# not
# in
# strings)
                                                                                parts = []
                                                                                in_string = False
                                                                                string_char = None
                                                                                i = 0

                                                                                while i < len(
                                                                                line):
                                                                                    char = line[i]

# Track
# string
# boundaries
                                                                                    if char in ['"', "'"] and (
                                                                                    i == 0 or line[i-1] != '\\'):
                                                                                        if not in_string:
                                                                                            in_string = True
                                                                                            string_char = char
                                                                                        elif char == string_char:
                                                                                            in_string = False

# Fix
# spacing
# only
# outside
# strings
                                                                                            if not in_string:
                                                                                                if char in '=<>!+-*/' and i > 0 and i < len(
                                                                                                line) - 1:
# Check
# for
# compound
# operators
                                                                                                    if i < len(
                                                                                                    line) - 1 and line[i+1] in '=':
# Compound
# operator
# like
# ==
# ,
# !=,
# +=
                                                                                                        parts.append(
                                                                                                        f' {char}{line[i+1]} ')
                                                                                                        i += 2
                                                                                                        continue
                                                                                                elif char == '=' and i > 0 and line[i-1] not in ' =!<>+-*/':
                                                                                                    parts.append(
                                                                                                    f' {char} ')
                                                                                                    i += 1
                                                                                                    continue

                                                                                                parts.append(
                                                                                                char)
                                                                                                i += 1

                                                                                                return ''.join(
                                                                                            parts)

                                                                                            def _fix_indentation(
                                                                                            self, lines: List[str]) -> List[str]:
"""Fix indentation to be consistent"""
                                                                                                fixed = []
                                                                                                indent_stack = [
                                                                                                0]

                                                                                                for line in lines:
                                                                                                    stripped = line.strip()

                                                                                                    if not stripped:
                                                                                                        fixed.append(
                                                                                                        '')
                                                                                                        continue

# Calculate
# current
# indent
                                                                                                    current_indent = len(
                                                                                                    line) - len(line.lstrip())

# Dedent
# on
# certain
# keywords
                                                                                                    if stripped.startswith(
                                                                                                    ('return', 'break', 'continue', 'pass', 'raise')):
                                                                                                        if len(
                                                                                                        indent_stack) > 1:
                                                                                                            indent_stack.pop()

# Handle
# dedent
# markers
                                                                                                            if stripped in (
                                                                                                            'else:', 'elif:', 'except:', 'finally:') or stripped.startswith(
                                                                                                            ('elif ', 'except ')):
                                                                                                                if len(
                                                                                                                indent_stack) > 1:
                                                                                                                    indent_stack.pop()

# Apply
# indent
                                                                                                                    indent = indent_stack[-1]
                                                                                                                    fixed.append(
                                                                                                                    ' ' * indent + stripped)

# Increase
# indent
# after
# colons
                                                                                                                    if stripped.endswith(
                                                                                                                    ':'):
                                                                                                                        indent_stack.append(
                                                                                                                        indent + self.indent_size)

                                                                                                                        return fixed

                                                                                                                    def _fix_spacing(
                                                                                                                    self, lines: List[str]) -> List[str]:
"""Fix spacing issues"""
                                                                                                                        fixed = []

                                                                                                                        for line in lines:
# Add
# space
# after
# comma
                                                                                                                            line = re.sub(
                                                                                                                            r', (?! )', ', ', line)

# Remove
# multiple
# spaces
                                                                                                                            line = re.sub(
                                                                                                                            r' +', ' ', line)

# Fix
# spacing
# in
# dictionary/set
# literals
                                                                                                                            line = re.sub(
                                                                                                                            r'{\s+', '{', line)
                                                                                                                            line = re.sub(
                                                                                                                            r'\s+}', '}', line)

                                                                                                                            fixed.append(
                                                                                                                            line)

                                                                                                                            return fixed

                                                                                                                        def _fix_line_length(
                                                                                                                        self, lines: List[str]) -> List[str]:
"""Break long lines at appropriate points"""
                                                                                                                            fixed = []

                                                                                                                            for line in lines:
                                                                                                                                if len(
                                                                                                                                line) <= self.line_length:
                                                                                                                                    fixed.append(
                                                                                                                                    line)
                                                                                                                                    continue

# Try
# to
# break
# at
# commas
                                                                                                                                if ', ' in line and not line.strip().startswith(('"""', "'''")):
                                                                                                                                    indent = len(
                                                                                                                                    line) - len(line.lstrip())
                                                                                                                                    parts = line.split(
                                                                                                                                    ', ')

                                                                                                                                    current = parts[
                                                                                                                                    0]
                                                                                                                                    for part in parts[
                                                                                                                                    1:]:
                                                                                                                                        if len(
                                                                                                                                        current + ', ' + part) > self.line_length:
                                                                                                                                            fixed.append(
                                                                                                                                            current + ', ')
                                                                                                                                            current = ' ' * \
                                                                                                                                            (indent + self.indent_size) + part
                                                                                                                                        else:
                                                                                                                                            current += ', ' + part

                                                                                                                                            fixed.append(
                                                                                                                                            current)
                                                                                                                                        else:
# Can't
# break
# nicely,
# keep
# as-is
                                                                                                                                            fixed.append(
                                                                                                                                            line)

                                                                                                                                            return fixed

                                                                                                                                        def _final_cleanup(
                                                                                                                                        self, lines: List[str]) -> List[str]:
"""Final cleanup pass"""
                                                                                                                                            fixed = []
                                                                                                                                            prev_blank = False

                                                                                                                                            for line in lines:
# Remove
# trailing
# whitespace
                                                                                                                                                line = line.rstrip()

# Avoid
# multiple
# blank
# lines
                                                                                                                                                if not line:
                                                                                                                                                    if not prev_blank:
                                                                                                                                                        fixed.append(
                                                                                                                                                        line)
                                                                                                                                                        prev_blank = True
                                                                                                                                                    else:
                                                                                                                                                        fixed.append(
                                                                                                                                                        line)
                                                                                                                                                        prev_blank = False

# Ensure
# file
# ends
# with
# newline
                                                                                                                                                        if fixed and fixed[
                                                                                                                                                        -1]:
                                                                                                                                                            fixed.append(
                                                                                                                                                            '')

                                                                                                                                                            return fixed

                                                                                                                                                        def format_directory(
                                                                                                                                                        self, directory: Path, exclude: List[str] = None) -> int:
"""Format all Python files in directory"""
                                                                                                                                                            exclude = exclude or [
                                                                                                                                                            '.venv', 'venv', '__pycache__', 'build', 'dist', '.git']

                                                                                                                                                            for py_file in directory.rglob(
                                                                                                                                                            '*.py'):
# Skip
# excluded
# directories
                                                                                                                                                                if any(
                                                                                                                                                                exc in py_file.parts for exc in exclude):
                                                                                                                                                                    continue

                                                                                                                                                                if self.format_file(
                                                                                                                                                                py_file):
                                                                                                                                                                    print(
                                                                                                                                                                    f"✨ Formatted: {py_file}")

                                                                                                                                                                    return self.files_formatted

                                                                                                                                                                def integrate_with_linter():
"""Integrate formatter with Think AI Linter"""
                                                                                                                                                                    linter_path = Path(
                                                                                                                                                                    'think_ai_linter.py')

                                                                                                                                                                    if not linter_path.exists():
                                                                                                                                                                        print(
                                                                                                                                                                        "Think AI Linter not found")
                                                                                                                                                                        return False

# Add
# format
# option
# to
# linter
                                                                                                                                                                    integration_code = '''
# Auto-format
# integration
                                                                                                                                                                    if '--format' in sys.argv:
from think_ai_autoformat import ThinkAIAutoFormat
                                                                                                                                                                        formatter = ThinkAIAutoFormat()
                                                                                                                                                                        formatter.format_directory(
                                                                                                                                                                        Path('.'))
                                                                                                                                                                        print(
                                                                                                                                                                        f"Formatted {formatter.files_formatted} files")
                                                                                                                                                                        sys.exit(
                                                                                                                                                                        0)
'''

                                                                                                                                                                        with open(linter_path, 'r') as f:
                                                                                                                                                                            content = f.read()

                                                                                                                                                                            if 'Auto-format integration' not in content:
# Add
# after
# imports
                                                                                                                                                                                lines = content.split(
                                                                                                                                                                                '\n')
                                                                                                                                                                                import_end = 0

                                                                                                                                                                                for i, line in enumerate(
                                                                                                                                                                                lines):
                                                                                                                                                                                    if line.strip() and not line.strip().startswith(('import', 'from', '#')):
                                                                                                                                                                                        import_end = i
                                                                                                                                                                                        break

                                                                                                                                                                                    lines.insert(
                                                                                                                                                                                    import_end, integration_code)

                                                                                                                                                                                    with open(linter_path, 'w') as f:
                                                                                                                                                                                        f.write(
                                                                                                                                                                                        '\n'.join(lines))

                                                                                                                                                                                        print(
                                                                                                                                                                                        "✅ Integrated with Think AI Linter")

                                                                                                                                                                                        return True

                                                                                                                                                                                    def setup_precommit():
"""Set up pre-commit hook"""
                                                                                                                                                                                        hooks_dir = Path(
                                                                                                                                                                                        '.git/hooks')
                                                                                                                                                                                        if not hooks_dir.exists():
                                                                                                                                                                                            print(
                                                                                                                                                                                            "Not a git repository")
                                                                                                                                                                                            return False

                                                                                                                                                                                        pre_commit = hooks_dir / 'pre-commit'

                                                                                                                                                                                        hook_content = '''#!/bin/bash
# Think AI Auto-Format Pre-Commit Hook

                                                                                                                                                                                        echo "🎨 Running Think AI Auto-Formatter..."

# Get staged Python files
                                                                                                                                                                                        STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\\.py$')

                                                                                                                                                                                        if [ -z "$STAGED_FILES" ]; then
                                                                                                                                                                                        exit 0
                                                                                                                                                                                        fi

# Format each file
                                                                                                                                                                                        for FILE in $STAGED_FILES; do
                                                                                                                                                                                        python think_ai_autoformat.py --file "$FILE"
                                                                                                                                                                                        git add "$FILE"
                                                                                                                                                                                        done

# Run linter check
                                                                                                                                                                                        echo "🔍 Running Think AI Linter..."
                                                                                                                                                                                        python think_ai_linter.py --check --ci

                                                                                                                                                                                        echo "✅ Pre-commit checks complete!"
'''

                                                                                                                                                                                        with open(pre_commit, 'w') as f:
                                                                                                                                                                                            f.write(
                                                                                                                                                                                            hook_content)

                                                                                                                                                                                            os.chmod(
                                                                                                                                                                                            pre_commit, 0o755)
                                                                                                                                                                                            print(
                                                                                                                                                                                            f"✅ Created pre-commit hook at {pre_commit}")

                                                                                                                                                                                            return True

                                                                                                                                                                                        def setup_vscode():
"""Set up VS Code integration"""
                                                                                                                                                                                            vscode_dir = Path(
                                                                                                                                                                                            '.vscode')
                                                                                                                                                                                            vscode_dir.mkdir(
                                                                                                                                                                                            exist_ok=True)

# Create
# tasks.json
# for
# format
# command
                                                                                                                                                                                            tasks_file = vscode_dir / 'tasks.json'
                                                                                                                                                                                            tasks = {
                                                                                                                                                                                            "version": "2.0.0",
                                                                                                                                                                                            "tasks": [
                                                                                                                                                                                            {
                                                                                                                                                                                            "label": "Think AI Format",
                                                                                                                                                                                            "type": "shell",
                                                                                                                                                                                            "command": "python",
                                                                                                                                                                                            "args": ["think_ai_autoformat.py", "--file", "${file}"],
                                                                                                                                                                                            "presentation": {
                                                                                                                                                                                            "reveal": "silent",
                                                                                                                                                                                            "showReuseMessage": False
                                                                                                                                                                                            }
                                                                                                                                                                                            }
                                                                                                                                                                                            ]
                                                                                                                                                                                            }

                                                                                                                                                                                            with open(tasks_file, 'w') as f:
                                                                                                                                                                                                json.dump(
                                                                                                                                                                                                tasks, f, indent=2)

# Update
# settings.json
                                                                                                                                                                                                settings_file = vscode_dir / 'settings.json'
                                                                                                                                                                                                settings = {}

                                                                                                                                                                                                if settings_file.exists():
                                                                                                                                                                                                    with open(settings_file, 'r') as f:
                                                                                                                                                                                                        settings = json.load(
                                                                                                                                                                                                        f)

                                                                                                                                                                                                        settings.update({
                                                                                                                                                                                                        "[python]": {
                                                                                                                                                                                                        "editor.formatOnSave": False,  # Disable default formatter
                                                                                                                                                                                                        "editor.codeActionsOnSave": {
                                                                                                                                                                                                        "source.custom.thinkAI": True
                                                                                                                                                                                                        }
                                                                                                                                                                                                        },
                                                                                                                                                                                                        "emeraldwalk.runonsave": {
                                                                                                                                                                                                        "commands": [
                                                                                                                                                                                                        {
                                                                                                                                                                                                        "match": "\\.py$",
                                                                                                                                                                                                        "cmd": "python ${workspaceFolder}/think_ai_autoformat.py --file ${file}"
                                                                                                                                                                                                        }
                                                                                                                                                                                                        ]
                                                                                                                                                                                                        }
                                                                                                                                                                                                        })

                                                                                                                                                                                                        with open(settings_file, 'w') as f:
                                                                                                                                                                                                            json.dump(
                                                                                                                                                                                                            settings, f, indent=2)

                                                                                                                                                                                                            print(
                                                                                                                                                                                                            f"✅ VS Code integration configured")
                                                                                                                                                                                                            print(
                                                                                                                                                                                                            "📦 Install 'Run on Save' extension for automatic formatting")

                                                                                                                                                                                                            return True

                                                                                                                                                                                                        def main():
                                                                                                                                                                                                            parser = argparse.ArgumentParser(
                                                                                                                                                                                                            description="Think AI Auto-Formatter - Smart Python formatting"
                                                                                                                                                                                                            )
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--file', help='Format a specific file')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--dir', help='Format all files in directory', default='.')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--check', action='store_true', help='Check if formatting needed')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--integrate', action='store_true', help='Integrate with linter')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--setup-hooks', action='store_true', help='Set up git hooks')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--setup-vscode', action='store_true', help='Set up VS Code')
                                                                                                                                                                                                            parser.add_argument(
                                                                                                                                                                                                            '--line-length', type=int, default=200, help='Max line length')

                                                                                                                                                                                                            args = parser.parse_args()

                                                                                                                                                                                                            if args.integrate:
                                                                                                                                                                                                                integrate_with_linter()
                                                                                                                                                                                                                return

                                                                                                                                                                                                            if args.setup_hooks:
                                                                                                                                                                                                                setup_precommit()
                                                                                                                                                                                                                return

                                                                                                                                                                                                            if args.setup_vscode:
                                                                                                                                                                                                                setup_vscode()
                                                                                                                                                                                                                return

                                                                                                                                                                                                            formatter = ThinkAIAutoFormat(
                                                                                                                                                                                                            line_length=args.line_length)

                                                                                                                                                                                                            if args.file:
                                                                                                                                                                                                                path = Path(
                                                                                                                                                                                                                args.file)
                                                                                                                                                                                                                if path.exists():
                                                                                                                                                                                                                    changed = formatter.format_file(
                                                                                                                                                                                                                    path)
                                                                                                                                                                                                                    if args.check:
                                                                                                                                                                                                                        sys.exit(
                                                                                                                                                                                                                        1 if changed else 0)
                                                                                                                                                                                                                    elif changed:
                                                                                                                                                                                                                        print(
                                                                                                                                                                                                                        f"✨ Formatted: {path}")
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        print(
                                                                                                                                                                                                                        f"✅ Already formatted: {path}")
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        print(
                                                                                                                                                                                                                        f"❌ File not found: {path}")
                                                                                                                                                                                                                        sys.exit(
                                                                                                                                                                                                                        1)
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        directory = Path(
                                                                                                                                                                                                                        args.dir)
                                                                                                                                                                                                                        count = formatter.format_directory(
                                                                                                                                                                                                                        directory)

                                                                                                                                                                                                                        if args.check and count > 0:
                                                                                                                                                                                                                            print(
                                                                                                                                                                                                                            f"❌ {count} files need formatting")
                                                                                                                                                                                                                            sys.exit(
                                                                                                                                                                                                                            1)
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            print(
                                                                                                                                                                                                                            f"✨ Formatted {count} files")

                                                                                                                                                                                                                            if __name__ == '__main__':
                                                                                                                                                                                                                                main()
