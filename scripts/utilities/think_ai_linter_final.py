#!/usr/bin/env python3

"""Think AI Linter - Final version with correct Python formatting"""

import ast
import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional
from textwrap import dedent


class PythonFormatter:
    """Properly format Python code without breaking indentation"""

    def __init__(self):
        self.indent_size = 4
        self.errors = []
        self.fixes_applied = 0

    def format_file(self, filepath: str) -> bool:
        """Format a Python file"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                original = f.read()

            # Try AST-based formatting first
            try:
                tree = ast.parse(original)
                formatted = self._format_with_ast(original, tree)
            except SyntaxError:
                # Fallback to line-by-line if syntax is broken
                formatted = self._format_line_by_line(original)

            if formatted != original:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(formatted)
                self.fixes_applied += 1
                print(f"✨ Formatted: {filepath}")
                return True

            return False

        except Exception as e:
            print(f"Error formatting {filepath}: {e}")
            return False

    def _format_with_ast(self, code: str, tree: ast.AST) -> str:
        """Format code using AST information"""
        lines = code.split("\n")

        # Build a map of which lines belong to which AST nodes
        node_lines = {}
        for node in ast.walk(tree):
            if hasattr(node, "lineno"):
                node_lines[node.lineno - 1] = node

        # Format with proper indentation
        formatted = []
        current_indent = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Empty lines
            if not stripped:
                formatted.append("")
                continue

            # Get indentation from original if it's valid Python
            original_indent = len(line) - len(line.lstrip())

            # For lines that are part of AST nodes, trust the original indent
            # but ensure it's a multiple of indent_size
            if i in node_lines:
                # Round to nearest indent level
                indent_level = (
                    round(original_indent / self.indent_size) * self.indent_size
                )
                formatted.append(" " * indent_level + stripped)
            else:
                # For non-AST lines (like comments between code), preserve original
                formatted.append(line)

        # Ensure trailing newline
        if formatted and formatted[-1] != "":
            formatted.append("")

        return "\n".join(formatted)

    def _format_line_by_line(self, code: str) -> str:
        """Format broken code line by line"""
        lines = code.split("\n")
        formatted = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            if not stripped:
                formatted.append("")
                continue

            # Handle dedent keywords
            if self._is_dedent_keyword(stripped):
                if indent_level > 0:
                    indent_level -= 1

            # Add the line
            formatted.append(" " * (indent_level * self.indent_size) + stripped)

            # Handle indent
            if stripped.endswith(":") and not stripped.startswith("#"):
                indent_level += 1
            elif self._is_block_end(stripped):
                if indent_level > 0:
                    indent_level -= 1

        if formatted and formatted[-1] != "":
            formatted.append("")

        return "\n".join(formatted)

    def _is_dedent_keyword(self, line: str) -> bool:
        """Check if line starts with dedent keyword"""
        keywords = ["elif", "else", "except", "finally", "case"]
        for kw in keywords:
            if line.startswith(kw) and (
                len(line) == len(kw) or line[len(kw) :].lstrip().startswith(":")
            ):
                return True
        return False

    def _is_block_end(self, line: str) -> bool:
        """Check if line ends a block"""
        keywords = ["return", "break", "continue", "pass", "raise"]
        for kw in keywords:
            if line == kw or line.startswith(kw + " ") or line.startswith(kw + "#"):
                return True
        return False

    def lint_file(self, filepath: str) -> List[str]:
        """Lint a file and return errors"""
        errors = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check syntax
            try:
                ast.parse(content)
            except SyntaxError as e:
                errors.append(f"{filepath}:{e.lineno}: {e.msg}")

            # Basic style checks
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                # Trailing whitespace
                if line.endswith(" ") or line.endswith("\t"):
                    errors.append(f"{filepath}:{i}: Trailing whitespace")

                # Tabs
                if "\t" in line:
                    errors.append(f"{filepath}:{i}: Tab character (use spaces)")

                # Line length
                if len(line) > 120:
                    errors.append(f"{filepath}:{i}: Line too long ({len(line)} > 120)")

        except Exception as e:
            errors.append(f"{filepath}: Error reading file: {e}")

        return errors

    def format_code(self, code: str) -> str:
        """Format code string and return formatted version"""
        try:
            tree = ast.parse(code)
            return self._format_with_ast(code, tree)
        except SyntaxError:
            return self._format_line_by_line(code)


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Think AI Python Formatter - Correct Python formatting"
    )
    parser.add_argument(
        "paths", nargs="*", default=["."], help="Files or directories to process"
    )
    parser.add_argument(
        "--check", action="store_true", help="Check only, don't modify files"
    )
    parser.add_argument("--fix", action="store_true", help="Fix issues (format files)")

    args = parser.parse_args()

    formatter = PythonFormatter()
    all_errors = []

    # Collect all Python files
    py_files = []
    for path in args.paths:
        path_obj = Path(path)
        if path_obj.is_file() and path_obj.suffix == ".py":
            py_files.append(path_obj)
        elif path_obj.is_dir():
            py_files.extend(path_obj.rglob("*.py"))

    # Process files
    for filepath in py_files:
        filepath_str = str(filepath)

        # Skip virtual environments and caches
        if any(
            part in filepath_str for part in [".venv", "venv", "__pycache__", ".git"]
        ):
            continue

        if args.check:
            errors = formatter.lint_file(filepath_str)
            all_errors.extend(errors)
        else:
            formatter.format_file(filepath_str)

    # Report results
    if args.check:
        if all_errors:
            print(f"\n❌ Found {len(all_errors)} issues:")
            for error in all_errors[:50]:  # Limit output
                print(f"  {error}")
            return 1
        else:
            print("✅ All files pass linting!")
            return 0
    else:
        print(f"\n✨ Formatted {formatter.fixes_applied} files")
        return 0


if __name__ == "__main__":
    sys.exit(main())
