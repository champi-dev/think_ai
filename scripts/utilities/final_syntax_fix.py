#! / usr / bin / env python3
"""Final aggressive syntax fix for remaining issues"""

import os
import re
from pathlib import Path


def fix_triple_quotes(content):
"""Fix unterminated triple quote issues"""
# Count triple quotes
    single_triple = content.count('"""')
    double_triple = content.count("'''")

# If odd number, we have unterminated
    if single_triple % 2 ! = 0:
# Find all positions
        positions = []
        for i in range(len(content) - 2):
            if content[i:i + 3] == '"""':
                positions.append(i)

# Check if last one looks like it should be closed
                if positions:
                    last_pos = positions[ - 1]
# Look for next newline after last triple quote
                    next_newline = content.find("\n", last_pos)
                    if next_newline > last_pos + 3:
# Insert closing quote before newline
                        content = content[:next_newline] + '"""' + content[next_newline:]

# Similar for single triple quotes
                        if double_triple % 2 ! = 0:
                            positions = []
                            for i in range(len(content) - 2):
                                if content[i:i + 3] == "'''":
                                    positions.append(i)

                                    if positions:
                                        last_pos = positions[ - 1]
                                        next_newline = content.find("\n", last_pos)
                                        if next_newline > last_pos + 3:
                                            content = content[:next_newline] + "'''" + content[next_newline:]

# Fix quadruple quotes (common typo)
                                            content = re.sub(r'"""', '"""', content)
                                            content = re.sub(r"'''", "'''", content)

                                            return content

                                        def fix_indentation_aggressively(lines):
"""Aggressively fix indentation issues"""
                                            fixed_lines = []
                                            expected_indent = 0

                                            for i, line in enumerate(lines):
                                                stripped = line.strip()

# Skip empty lines
                                                if not stripped:
                                                    fixed_lines.append("")
                                                    continue

# Handle dedent keywords
                                                if stripped.startswith(("return", "break", "continue", "pass", "raise")):
                                                    if expected_indent > 0:
                                                        fixed_lines.append(" " * expected_indent + stripped)
                                                    else:
                                                        fixed_lines.append(stripped)
                                                        continue

# Handle block starts
                                                    if stripped.endswith(":"):
                                                        fixed_lines.append(" " * expected_indent + stripped)
                                                        expected_indent + = 4
                                                        continue

# Handle dedent markers
                                                    if stripped in ("else:", "elif:", "except:", "finally:"):
                                                        expected_indent = max(0, expected_indent - 4)
                                                        fixed_lines.append(" " * expected_indent + stripped)
                                                        expected_indent + = 4
                                                        continue

# Normal line
                                                    fixed_lines.append(" " * expected_indent + stripped)

# Check if we should dedent for next line
                                                    if stripped.startswith("return ") or stripped = = "return":
                                                        expected_indent = max(0, expected_indent - 4)

                                                        return fixed_lines

                                                    def fix_specific_file_issues(filepath, content):
"""Fix known issues in specific files"""
                                                        filename = os.path.basename(filepath)

                                                        if filename = = "test_full_system_fixed.py":
# Fix the specific triple quote issue
                                                            content = content.replace('"""', '"""')
# Fix the line with only import
                                                            content = re.sub(r"\n\s * import traceback\n", "\nimport traceback\n", content)

                                                        elif filename = = "run_all_tests_parallel.py":
# Fix the f - string with triple quotes
                                                            content = re.sub(r'f"""', 'f"""', content)

                                                        elif filename = = "integrate_superintelligence.py":
# Fix the syntax error with comma placement
                                                            content = re.sub(r""\s * , \s * \n\s * , ", "", ", content)
# Fix multi - line string issues
                                                            lines = content.split("\n")
                                                            fixed_lines = []
                                                            in_string = False
                                                            for line in lines:
                                                                if ""understanding":" in line and not in_string:
# Start of multi - line string
                                                                    if not line.rstrip().endswith(", "):
                                                                        line = line.rstrip() + " \\"
                                                                        in_string = True
                                                                    elif in_string and "", \n" in line:
                                                                        in_string = False
                                                                        fixed_lines.append(line)
                                                                        content = "\n".join(fixed_lines)

                                                                        return content

                                                                    def aggressive_fix_file(filepath):
"""Apply all fixes aggressively"""
                                                                        try:
                                                                            with open(filepath, "r", encoding = "utf-8") as f:
                                                                                content = f.read()

                                                                                original = content

# Fix specific file issues first
                                                                                content = fix_specific_file_issues(filepath, content)

# Fix triple quotes
                                                                                content = fix_triple_quotes(content)

# Fix indentation line by line
                                                                                lines = content.split("\n")

# Remove lines with only "import" statements that are improperly indented
                                                                                fixed_lines = []
                                                                                for line in lines:
                                                                                    if line.strip() = = "import" or re.match(r"^\s + import\s*$", line):
                                                                                        continue
# Fix lines with multiple imports on wrong indentation
                                                                                    if re.match(r"^\s + import\s+\w+", line) and not line.startswith(" "):
                                                                                        line = line.strip()
# Fix lines with from imports on wrong indentation
                                                                                        if re.match(r"^\s + from\s+\w+", line) and not line.startswith(" "):
                                                                                            line = line.strip()
                                                                                            fixed_lines.append(line)

# Apply aggressive indentation fix
                                                                                            fixed_lines = fix_indentation_aggressively(fixed_lines)

                                                                                            content = "\n".join(fixed_lines)

                                                                                            if content ! = original:
                                                                                                with open(filepath, "w", encoding = "utf-8") as f:
                                                                                                    f.write(content)
                                                                                                    print(f"✅ Fixed: {filepath}")
                                                                                                    return True

                                                                                                except Exception as e:
                                                                                                    print(f"❌ Error fixing {filepath}: {e}")
                                                                                                    return False

                                                                                                def main():
"""Fix all remaining syntax errors"""
                                                                                                    print("🔧 Final syntax fix pass...")
                                                                                                    print("=" * 60)

# Critical files from linter output
                                                                                                    critical_files = [
                                                                                                    "colab_archive / colab_full_system.py",
                                                                                                    "fix_model_generation.py",
                                                                                                    "full_architecture_chat.py",
                                                                                                    "generate_tests.py",
                                                                                                    "implement_proper_architecture.py",
                                                                                                    "integrate_superintelligence.py",
                                                                                                    "launch_with_background_training.py",
                                                                                                    "plugins / example_analytics.py",
                                                                                                    "plugins / example_storage.py",
                                                                                                    "run_all_tests_parallel.py",
                                                                                                    "test - apps / run_all_tests.py",
                                                                                                    "test_cached_model.py",
                                                                                                    "test_deployed_libs.py",
                                                                                                    "test_full_system_fixed.py",
                                                                                                    "test_full_system_working.py",
                                                                                                    "test_generation_speed.py",
                                                                                                    "test_meta_tensor_fix.py",
                                                                                                    "test_model_evidence.py",
                                                                                                    "test_mps_simple.py",
                                                                                                    "test_qwen_working.py",
                                                                                                    "test_sun_question.py",
                                                                                                    "test_vector_databases.py"
                                                                                                    ]

                                                                                                    fixed_count = 0

                                                                                                    for filename in critical_files:
                                                                                                        filepath = Path(filename)
                                                                                                        if filepath.exists():
                                                                                                            if aggressive_fix_file(filepath):
                                                                                                                fixed_count + = 1

# Also scan all Python files
                                                                                                                print("\n🔍 Scanning all Python files...")
                                                                                                                for py_file in Path(".").rglob("*.py"):
                                                                                                                    if str(py_file) not in critical_files:
                                                                                                                        try:
                                                                                                                            with open(py_file, "r") as f:
                                                                                                                                content = f.read()
# Quick check for triple quote issues
                                                                                                                                if '"""' in content or "'''" in content or content.count('"""') % 2 != 0:"""
                                                                                                                                if aggressive_fix_file(py_file):
                                                                                                                                    fixed_count + = 1
                                                                                                                                except:
                                                                                                                                    pass

                                                                                                                                print(f"\n✨ Fixed {fixed_count} files!")
                                                                                                                                print("🚀 Final syntax fixes applied")

                                                                                                                                if __name__ = = "__main__":
                                                                                                                                    main()
