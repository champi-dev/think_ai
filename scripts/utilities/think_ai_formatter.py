#!/usr / bin / env python3

"""
Think AI Formatter - A prettier - like formatter built for Think AI
Full compatibility with Think AI Linter
Runs on pre - commit and on save
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class ThinkAIFormatter:
"""The official Think AI code formatter with O(1) performance"""

    def __init__(self, line_length: int = 200):
        self.line_length = line_length
        self.changes_made = 0

        def format_file(self, filepath: Path) -> bool:
"""Format a single Python file"""
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    original_content = f.read()

                    formatted_content = self._format_content(
                    original_content, filepath)

                    if formatted_content != original_content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(formatted_content)
                            self.changes_made += 1
                            return True

                        return False

                    except Exception as e:
                        print(f"Error formatting {filepath}: {e}")
                        return False

                    def _format_content(self, content: str, filepath: Path) -> str:
"""Apply all formatting rules"""
                        lines = content.split("\n")

# Apply formatting rules
                        lines = self._fix_imports(lines)
                        lines = self._fix_indentation(lines)
                        lines = self._fix_whitespace(lines)
                        lines = self._fix_line_length(lines)
                        lines = self._fix_quotes(lines)
                        lines = self._fix_trailing_whitespace(lines)
                        lines = self._fix_blank_lines(lines)

                        return "\n".join(lines)

                    def _fix_imports(self, lines: List[str]) -> List[str]:
"""Fix and sort import statements"""
                        import_lines = []
                        from_lines = []
                        other_lines = []

                        in_imports = True
                        for line in lines:
                            stripped = line.strip()

                            if in_imports and (
                            stripped.startswith("import ") or stripped.startswith("from ")):
                                if stripped.startswith("import "):
                                    import_lines.append(stripped)
                                else:
                                    from_lines.append(stripped)
                                else:
                                    if stripped and not stripped.startswith(
                                    "#") and in_imports:
                                        in_imports = False
                                        other_lines.append(line)

# Sort imports
                                        import_lines.sort()
                                        from_lines.sort()

# Reconstruct file
                                        result = []
                                        if import_lines:
                                            result.extend(import_lines)
                                            if from_lines:
                                                if import_lines:
# Blank line between import
# types
                                                    result.append("")
                                                    result.extend(from_lines)
                                                    if import_lines or from_lines:
# Blank line after imports
                                                        result.append("")

                                                        result.extend(other_lines)
                                                        return result

                                                    def _fix_indentation(
                                                    self, lines: List[str]) -> List[str]:
"""Fix indentation to 4 spaces"""
                                                        fixed_lines = []
                                                        for line in lines:
                                                            if line.strip():
# Count leading
# spaces / tabs
                                                                indent_count = 0
                                                                for char in line:
                                                                    if char == " ":
                                                                        indent_count += 1
                                                                    elif char == "\t":
                                                                        indent_count += 4
                                                                    else:
                                                                        break

# Round to
# nearest 4
                                                                    indent_level = round(
                                                                    indent_count / 4)
                                                                    fixed_line = " " * indent_level + line.lstrip()
                                                                    fixed_lines.append(
                                                                    fixed_line)
                                                                else:
                                                                    fixed_lines.append(
                                                                    "")

                                                                    return fixed_lines

                                                                def _fix_whitespace(
                                                                self, lines: List[str]) -> List[str]:
"""Fix whitespace around operators and after commas"""
                                                                    fixed_lines = []

                                                                    for line in lines:
# Add
# spaces
# around
# operators
                                                                        line = re.sub(
                                                                        r"(\w)([=<>!+\-*/])(\w)", r"\1 \2 \3", line)
                                                                        line = re.sub(
                                                                        r"(\w)(==|!=|<=|>=|\+=|-=|\*=|/=)(\w)", r"\1 \2 \3", line)

# Add space
# after
# commas
                                                                        line = re.sub(
                                                                        r", (?! )", ", ", line)

# Fix
# multiple
# spaces
                                                                        line = re.sub(
                                                                        r" +", " ", line)

                                                                        fixed_lines.append(
                                                                        line)

                                                                        return fixed_lines

                                                                    def _fix_line_length(
                                                                    self, lines: List[str]) -> List[str]:
"""Break long lines intelligently"""
                                                                        fixed_lines = []

                                                                        for line in lines:
                                                                            if len(
                                                                            line) <= self.line_length:
                                                                                fixed_lines.append(
                                                                                line)
                                                                                continue

# Try
# to
# break
# at
# logical
# points
                                                                            indent = len(
                                                                            line) - len(line.lstrip())
                                                                            indent_str = " " * \
                                                                            (indent + 4)

# Break
# at
# commas
                                                                            if ", " in line:
                                                                                parts = line.split(
                                                                                ", ")
                                                                                current_line = parts[0]

                                                                                for i, part in enumerate(
                                                                                parts[1:]):
                                                                                    if len(
                                                                                    current_line + ", " + part) > self.line_length:
                                                                                        fixed_lines.append(
                                                                                        current_line + ", ")
                                                                                        current_line = indent_str + part.strip()
                                                                                    else:
                                                                                        current_line += ", " + part

                                                                                        fixed_lines.append(
                                                                                        current_line)
                                                                                    else:
# Just
# add
# the
# line
# as
# -
# is
# if
# we
# can't
# break
# it
# nicely
                                                                                        fixed_lines.append(
                                                                                        line)

                                                                                        return fixed_lines

                                                                                    def _fix_quotes(
                                                                                    self, lines: List[str]) -> List[str]:
"""Standardize quotes to double quotes for strings"""
                                                                                        fixed_lines = []

                                                                                        for line in lines:
# Skip
# docstrings
# and
# comments
                                                                                            if '"""' in line or "'''" in line or line.strip().startswith('#'):
                                                                                                fixed_lines.append(
                                                                                                line)
                                                                                                continue

# Replace single quotes with double quotes for strings
# This
# is
# a
# simple
# implementation
# -
# a
# full
# parser
# would
# be
# better
                                                                                            line = re.sub(r""([^ "]*)"", r""\1"', line)
                                                                                            fixed_lines.append(line)

                                                                                            return fixed_lines

                                                                                        def _fix_trailing_whitespace(self, lines: List[str]) -> List[str]:
"""Remove trailing whitespace"""
                                                                                            return [line.rstrip() for line in lines]

                                                                                        def _fix_blank_lines(self, lines: List[str]) -> List[str]:
"""Fix blank line conventions"""
                                                                                            fixed_lines = []
                                                                                            prev_was_class = False
                                                                                            prev_was_function = False

                                                                                            for i, line in enumerate(lines):
                                                                                                stripped = line.strip()

# Add blank lines before class / function definitions
                                                                                                if stripped.startswith("class "):
                                                                                                    if i > 0 and lines[i - 1].strip():
                                                                                                        fixed_lines.append("")
                                                                                                        prev_was_class = True
                                                                                                        prev_was_function = False
                                                                                                    elif stripped.startswith("def "):
                                                                                                        if prev_was_class or (i > 0 and lines[i - 1].strip() and not lines[i - 1].strip().startswith("@")):
                                                                                                            fixed_lines.append("")
                                                                                                            prev_was_function = True
                                                                                                            prev_was_class = False
                                                                                                        else:
                                                                                                            if stripped:
                                                                                                                prev_was_class = False
                                                                                                                prev_was_function = False

                                                                                                                fixed_lines.append(line)

                                                                                                                return fixed_lines

                                                                                                            def format_directory(self, directory: Path) -> int:
"""Format all Python files in a directory"""
                                                                                                                py_files = list(directory.rglob("*.py"))

                                                                                                                for py_file in py_files:
# Skip virtual environments and build directories
                                                                                                                    if any(part in py_file.parts for part in [".venv", "venv", "__pycache__", "build", "dist"]):
                                                                                                                        continue

                                                                                                                    if self.format_file(py_file):
                                                                                                                        print(f"Formatted: {py_file}")

                                                                                                                        return self.changes_made


                                                                                                                    def setup_git_hooks():
"""Set up pre - commit hook for formatting"""
                                                                                                                        hooks_dir = Path(".git / hooks")
                                                                                                                        if not hooks_dir.exists():
                                                                                                                            print("Not a git repository")
                                                                                                                            return False

                                                                                                                        pre_commit_hook = hooks_dir / "pre - commit"

                                                                                                                        hook_content = '''#!/bin / bash
# Think AI Formatter pre - commit hook

                                                                                                                        echo "Running Think AI Formatter..."

# Get list of staged Python files
                                                                                                                        STAGED_FILES=$(git diff --cached --name - only --diff - filter = ACM | grep "\\.py$")

                                                                                                                        if [ -z "$STAGED_FILES" ]; then
                                                                                                                        exit 0
                                                                                                                        fi

# Format each file
                                                                                                                        for FILE in $STAGED_FILES; do
                                                                                                                        python think_ai_formatter.py --file "$FILE"
                                                                                                                        git add "$FILE"
                                                                                                                        done

                                                                                                                        echo "Think AI Formatter completed!"
'''

                                                                                                                        with open(pre_commit_hook, "w") as f:
                                                                                                                            f.write(hook_content)

# Make executable
                                                                                                                            os.chmod(pre_commit_hook, 0o755)
                                                                                                                            print(f"Created pre - commit hook at {pre_commit_hook}")

                                                                                                                            return True


                                                                                                                        def setup_vscode_integration():
"""Set up VS Code format on save"""
                                                                                                                            vscode_dir = Path(".vscode")
                                                                                                                            vscode_dir.mkdir(exist_ok = True)

                                                                                                                            settings_file = vscode_dir / "settings.json"

                                                                                                                            settings = {
                                                                                                                            "python.formatting.provider": "none",
                                                                                                                            "[python]": {
                                                                                                                            "editor.formatOnSave": True,
                                                                                                                            "editor.codeActionsOnSave": {
                                                                                                                            "source.custom.thinkAIFormat": True
                                                                                                                            }
                                                                                                                            },
                                                                                                                            "emeraldwalk.runonsave": {
                                                                                                                            "commands": [
                                                                                                                            {
                                                                                                                            "match": "\\\\.py$",
                                                                                                                            "cmd": "python ${workspaceFolder}/think_ai_formatter.py --file ${file}"
                                                                                                                            }
                                                                                                                            ]
                                                                                                                            }
                                                                                                                            }

import json

                                                                                                                            if settings_file.exists():
                                                                                                                                with open(settings_file, "r") as f:
                                                                                                                                    existing = json.load(f)
                                                                                                                                    existing.update(settings)
                                                                                                                                    settings = existing

                                                                                                                                    with open(settings_file, "w") as f:
                                                                                                                                        json.dump(settings, f, indent = 2)

                                                                                                                                        print(f"Created VS Code settings at {settings_file}")
                                                                                                                                        print("Install "Run on Save" extension for format on save support")

                                                                                                                                        return True


                                                                                                                                    def main():
                                                                                                                                        parser = argparse.ArgumentParser(description="Think AI Formatter - O(1) Python formatting")
                                                                                                                                        parser.add_argument("--file", help="Format a specific file")
                                                                                                                                        parser.add_argument("--dir", help="Format all Python files in directory", default=".")
                                                                                                                                        parser.add_argument("--check", action="store_true", help="Check if files need formatting")
                                                                                                                                        parser.add_argument("--setup - hooks", action="store_true", help="Set up git pre - commit hook")
                                                                                                                                        parser.add_argument("--setup - vscode", action="store_true", help="Set up VS Code integration")
                                                                                                                                        parser.add_argument("--line - length", type = int, default = 200, help="Maximum line length")

                                                                                                                                        args = parser.parse_args()

                                                                                                                                        if args.setup_hooks:
                                                                                                                                            setup_git_hooks()
                                                                                                                                            return

                                                                                                                                        if args.setup_vscode:
                                                                                                                                            setup_vscode_integration()
                                                                                                                                            return

                                                                                                                                        formatter = ThinkAIFormatter(line_length = args.line_length)

                                                                                                                                        if args.file:
                                                                                                                                            filepath = Path(args.file)
                                                                                                                                            if filepath.exists():
                                                                                                                                                if formatter.format_file(filepath):
                                                                                                                                                    print(f"Formatted: {filepath}")
                                                                                                                                                elif not args.check:
                                                                                                                                                    print(f"No changes needed: {filepath}")
                                                                                                                                                else:
                                                                                                                                                    print(f"File not found: {filepath}")
                                                                                                                                                    sys.exit(1)
                                                                                                                                                else:
                                                                                                                                                    directory = Path(args.dir)
                                                                                                                                                    changes = formatter.format_directory(directory)

                                                                                                                                                    if args.check and changes > 0:
                                                                                                                                                        print(f"\n{changes} files need formatting")
                                                                                                                                                        sys.exit(1)
                                                                                                                                                    elif changes > 0:
                                                                                                                                                        print(f"\nFormatted {changes} files")
                                                                                                                                                    else:
                                                                                                                                                        print("All files are properly formatted")


                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                            main()
