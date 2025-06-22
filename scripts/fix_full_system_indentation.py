#!/usr/bin/env python3
"""Fix indentation issues in think_ai/engine/full_system.py"""


def fix_full_system_indentation():
    """Fix the severe indentation issues in full_system.py"""

    # Read the original file
    with open("think_ai/engine/full_system.py", "r") as f:
        lines = f.readlines()

    # Fix the indentation
    fixed_lines = []
    for i, line in enumerate(lines):
        # Skip the first 52 lines (they're mostly OK)
        if i < 52:
            fixed_lines.append(line)
            continue

        # Fix specific issues
        if i == 53:  # Line 54 in 1-based numbering
            fixed_lines.append('        logger.info("🚀 Initializing Think AI Full Distributed System")\n')
        elif i == 55:  # Line 56
            fixed_lines.append("        # Check system mode\n")
        elif i == 56:  # Line 57
            fixed_lines.append("        if self.config.get('system_mode') != 'full_distributed':\n")
        elif i == 57:  # Line 58
            fixed_lines.append("            logger.warning(\n")
        elif i == 58:  # Line 59
            fixed_lines.append(
                '                "System not in full_distributed mode. Some features may be limited.")\n'
            )
        elif i == 60:  # Line 61
            fixed_lines.append("        # Initialize ScyllaDB\n")
        elif i == 72:  # Line 73 - fix except indentation
            fixed_lines.append("            except Exception as e:\n")
        elif i == 73:  # Line 74
            fixed_lines.append('                logger.error(f"❌ ScyllaDB initialization failed: {e}")\n')
        elif i == 75:  # Line 76
            fixed_lines.append("        # Initialize Redis\n")
        elif i == 76:  # Line 77
            fixed_lines.append("        if self.config.get('redis', {}).get('enabled', False):\n")
        elif i == 77:  # Line 78
            fixed_lines.append("            try:\n")
        elif i == 78:  # Line 79
            fixed_lines.append("                redis_config = RedisConfig(\n")
        elif i == 79:  # Line 80
            fixed_lines.append("                    host=self.config['redis'].get('host', 'localhost'),\n")
        elif i == 80:  # Line 81
            fixed_lines.append("                    port=self.config['redis'].get('port', 6379),\n")
        elif i == 81:  # Line 82
            fixed_lines.append("                    password=self.config['redis'].get('password', None)\n")
        elif i == 82:  # Line 83
            fixed_lines.append("                )\n")
        elif i == 83:  # Line 84
            fixed_lines.append("                redis = RedisCache(redis_config)\n")
        elif i == 87:  # Line 88
            fixed_lines.append("            except Exception as e:\n")
        elif i == 88:  # Line 89
            fixed_lines.append('                logger.error(f"❌ Redis initialization failed: {e}")\n')
        elif i == 90:  # Line 91
            fixed_lines.append("        # Initialize Milvus\n")
        else:
            # Keep the line but try to fix obvious indentation issues
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                # This line should probably be indented
                if "def " in line or "class " in line or line.strip().startswith("@"):
                    fixed_lines.append(line)  # Keep as is
                else:
                    fixed_lines.append("        " + line)  # Add base indentation
            else:
                fixed_lines.append(line)

    # Write the fixed file
    with open("think_ai/engine/full_system.py", "w") as f:
        f.writelines(fixed_lines)

    print("✅ Fixed full_system.py indentation")


if __name__ == "__main__":
    fix_full_system_indentation()
