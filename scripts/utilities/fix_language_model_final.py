#!/usr/bin/env python3
"""Fix language_model.py indentation and syntax issues"""


def fix_language_model():
    """Fix all indentation issues in language_model.py"""

    with open("think_ai/models/language_model.py", "r") as f:
        lines = f.readlines()

    fixed_lines = []
    i = 0
    in_dataclass = False
    in_class = False
    in_method = False
    method_indent = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check for dataclass decorator
        if stripped == "@dataclass":
            in_dataclass = True
            fixed_lines.append(line)
            i += 1
            continue

        # Check for class definition
        if stripped.startswith("class "):
            in_class = True
            in_method = False
            if in_dataclass:
                in_dataclass = False
            fixed_lines.append(line.lstrip() + "\n")  # Remove any extra indentation
            i += 1
            continue

        # Fix dataclass fields
        if (
            in_class
            and not in_method
            and ":" in stripped
            and not stripped.startswith("def")
            and not stripped.startswith("async def")
        ):
            # Check if this is a field definition
            if any(
                t in stripped
                for t in [
                    "int =",
                    "float =",
                    "bool =",
                    "str =",
                    "Dict[",
                    "List[",
                    "Optional[",
                    "Any =",
                    ": int",
                    ": float",
                    ": bool",
                    ": str",
                ]
            ):
                fixed_lines.append("    " + stripped + "\n")
                i += 1
                continue

        # Fix method definitions
        if stripped.startswith("def ") or stripped.startswith("async def "):
            in_method = True
            # Check if we're inside a class by looking for proper context
            if in_class:
                fixed_lines.append("    " + stripped + "\n")
                method_indent = 4
            else:
                fixed_lines.append(stripped + "\n")
                method_indent = 0
            i += 1
            continue

        # Fix docstrings
        if '"""' in stripped and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.endswith(":"):
                # This is a docstring after a definition
                if in_method:
                    fixed_lines.append(" " * (method_indent + 4) + stripped + "\n")
                else:
                    fixed_lines.append("    " + stripped + "\n")
                i += 1
                continue

        # Fix specific problematic lines
        if "O(1) complexity using direct" in stripped:
            fixed_lines.append(
                "        O(1) complexity using direct attribute access and conditional logic.\n"
            )
            i += 1
            continue

        # Fix method body indentation
        if (
            in_method
            and stripped
            and not stripped.startswith("class ")
            and not stripped.startswith("@")
        ):
            # Determine proper indentation
            if stripped.startswith("#"):
                fixed_lines.append(" " * (method_indent + 4) + stripped + "\n")
            elif stripped.startswith('"""') and stripped.endswith('"""'):
                fixed_lines.append(" " * (method_indent + 4) + stripped + "\n")
            elif any(
                stripped.startswith(x)
                for x in [
                    "if ",
                    "else:",
                    "elif ",
                    "for ",
                    "while ",
                    "try:",
                    "except",
                    "finally:",
                    "with ",
                    "return ",
                    "params",
                    "logger",
                    "config",
                    "model",
                    "self.",
                    "await ",
                    "raise ",
                ]
            ):
                fixed_lines.append(" " * (method_indent + 4) + stripped + "\n")
            else:
                # Check if line is part of a continued statement
                if i > 0 and lines[i - 1].strip().endswith(("=", ",", "(", "{")):
                    fixed_lines.append(" " * (method_indent + 8) + stripped + "\n")
                else:
                    fixed_lines.append(" " * (method_indent + 4) + stripped + "\n")
            i += 1
            continue

        # Fix **kwargs spacing
        if "** kwargs" in line:
            line = line.replace("** kwargs", "**kwargs")

        # Fix other spacing issues
        if "** 3" in line:
            line = line.replace("** 3", "**3")

        # Keep empty lines and other content as-is
        if stripped == "":
            in_method = False if in_class else in_method

        fixed_lines.append(line)
        i += 1

    # Write the fixed content
    with open("think_ai/models/language_model.py", "w") as f:
        f.writelines(fixed_lines)

    print("Fixed language_model.py indentation")


if __name__ == "__main__":
    fix_language_model()
