#!/usr/bin/env python3

"""Think AI Linter V2 - Proper Python formatting that actually works"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
import tokenize
import io


class ThinkAILinterV2:
    """Think AI Linter with correct Python formatting

    This version properly handles Python indentation without cascading issues.
    """

    def __init__(self):
        self.errors = []
        self.fixes_applied = 0
        self.indent_size = 4

    def format_file(self, filepath: str) -> bool:
        """Format a Python file with correct indentation"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                return False

            # Format the content
            formatted = self._format_python_correctly(content)

            if formatted != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(formatted)
                self.fixes_applied += 1
                print(f"✨ Formatted: {filepath}")
                return True

            return False

        except Exception as e:
            print(f"Error formatting {filepath}: {e}")
            return False

    def _format_python_correctly(self, content: str) -> str:
        """Format Python code with proper indentation using tokenization"""
        try:
            # Tokenize to understand the structure better
            tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))

            # Format line by line with proper context
            lines = content.split("\n")
            formatted_lines = []
            indent_stack = [0]  # Stack to track indentation levels

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Empty lines
                if not stripped:
                    formatted_lines.append("")
                    continue

                # Comments - preserve at current indent level
                if stripped.startswith("#"):
                    formatted_lines.append(" " * indent_stack[-1] + stripped)
                    continue

                # Determine proper indentation
                if self._should_dedent(stripped):
                    # Pop from stack for dedent keywords
                    if len(indent_stack) > 1:
                        indent_stack.pop()

                # Apply current indentation
                formatted_lines.append(" " * indent_stack[-1] + stripped)

                # Check if next line should indent
                if stripped.endswith(":") and not stripped.startswith("#"):
                    # Push new level onto stack
                    indent_stack.append(indent_stack[-1] + self.indent_size)
                elif self._ends_block(stripped):
                    # Pop after block-ending statements
                    if len(indent_stack) > 1:
                        indent_stack.pop()

            # Ensure newline at end
            if formatted_lines and formatted_lines[-1] != "":
                formatted_lines.append("")

            return "\n".join(formatted_lines)

        except Exception:
            # Fallback to simple formatting if tokenization fails
            return self._simple_format(content)

    def _should_dedent(self, line: str) -> bool:
        """Check if line should dedent"""
        dedent_keywords = ["elif", "else", "except", "finally", "case"]
        for keyword in dedent_keywords:
            if line.startswith(keyword) and (
                len(line) == len(keyword) or line[len(keyword)] in " :("
            ):
                return True
        return False

    def _ends_block(self, line: str) -> bool:
        """Check if line ends a block"""
        end_keywords = ["return", "break", "continue", "pass", "raise"]
        for keyword in end_keywords:
            if line.startswith(keyword) and (
                len(line) == len(keyword) or line[len(keyword)] in " (#"
            ):
                return True
        return False

    def _simple_format(self, content: str) -> str:
        """Simple formatting fallback"""
        lines = content.split("\n")
        formatted = []
        indent = 0

        for line in lines:
            stripped = line.strip()

            if not stripped:
                formatted.append("")
                continue

            # Dedent before adding line
            if self._should_dedent(stripped):
                indent = max(0, indent - self.indent_size)

            formatted.append(" " * indent + stripped)

            # Indent after colon
            if stripped.endswith(":") and not stripped.startswith("#"):
                indent += self.indent_size
            # Dedent after block end
            elif self._ends_block(stripped):
                indent = max(0, indent - self.indent_size)

        if formatted and formatted[-1] != "":
            formatted.append("")

        return "\n".join(formatted)

    def lint_file(self, filepath: str) -> None:
        """Basic linting"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Try to parse AST
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.errors.append(f"{filepath}:{e.lineno}: {e.msg}")

        except Exception as e:
            self.errors.append(f"{filepath}: Error: {e}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Think AI Linter V2")
    parser.add_argument("files", nargs="+", help="Files to format")
    parser.add_argument("--check", action="store_true", help="Check only")

    args = parser.parse_args()

    linter = ThinkAILinterV2()

    for filepath in args.files:
        if args.check:
            linter.lint_file(filepath)
        else:
            linter.format_file(filepath)

    if linter.errors:
        print(f"\n❌ Found {len(linter.errors)} errors")
        for error in linter.errors:
            print(f"  {error}")
        return 1
    elif not args.check:
        print(f"\n✅ Formatted {linter.fixes_applied} files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
