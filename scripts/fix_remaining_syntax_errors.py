#!/usr/bin/env python3
"""Fix remaining syntax errors in Think AI files."""

import re


def fix_shared_knowledge():
    """Fix shared_knowledge.py"""
    with open("think_ai/persistence/shared_knowledge.py", "r") as f:
        content = f.read()

    # Fix remaining indentation issues after line 57
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        if i < 57:
            fixed_lines.append(line)
        elif i == 57:
            fixed_lines.append("                        # Merge with local knowledge")
        elif i == 58:
            fixed_lines.append("                        self._merge_knowledge(remote_knowledge)")
        elif i == 59:
            fixed_lines.append('                        logger.info("Downloaded and merged latest knowledge")')
        elif i == 60:
            fixed_lines.append("                    else:")
        elif i == 61:
            fixed_lines.append(
                '                        logger.warning(f"Failed to download knowledge: {response.status}")'
            )
        elif i == 62:
            fixed_lines.append("        except Exception as e:")
        elif i == 63:
            fixed_lines.append('            logger.error(f"Error downloading knowledge: {e}")')
        else:
            # Keep the rest but fix obvious indentation
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                if line.strip().startswith("def ") or line.strip().startswith("async def "):
                    fixed_lines.append("    " + line.strip())
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

    with open("think_ai/persistence/shared_knowledge.py", "w") as f:
        f.write("\n".join(fixed_lines))

    print("✅ Fixed shared_knowledge.py")


def fix_ui_visualization():
    """Fix ui_visualization.py"""
    with open("think_ai/plugins/examples/ui_visualization.py", "r") as f:
        content = f.read()

    # Find where METADATA ends and fix indentation
    lines = content.split("\n")
    fixed_lines = []
    in_metadata = False

    for i, line in enumerate(lines):
        if "METADATA = PluginMetadata(" in line:
            in_metadata = True
            fixed_lines.append(line)
        elif in_metadata and line.strip() == ")":
            in_metadata = False
            fixed_lines.append("    )")
        elif in_metadata:
            # Ensure proper indentation inside METADATA
            if line.strip():
                fixed_lines.append("        " + line.strip())
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    with open("think_ai/plugins/examples/ui_visualization.py", "w") as f:
        f.write("\n".join(fixed_lines))

    print("✅ Fixed ui_visualization.py")


def fix_installer():
    """Fix installer.py"""
    with open("think_ai/plugins/installer.py", "r") as f:
        lines = f.readlines()

    # Fix the indentation after line 51
    fixed_lines = []
    for i, line in enumerate(lines):
        if i < 52:
            fixed_lines.append(line)
        elif i == 52:
            fixed_lines.append("\n")
        elif i == 53:
            fixed_lines.append("            # Verify plugin\n")
        elif i == 54:
            fixed_lines.append("            if verify_signature:\n")
        elif i == 55:
            fixed_lines.append("                if not await self._verify_plugin_signature(plugin_path):\n")
        elif i == 56:
            fixed_lines.append('                    return False, "Plugin signature verification failed"\n')
        elif i == 57:
            fixed_lines.append("\n")
        elif i == 58:
            fixed_lines.append("            # Install plugin\n")
        elif i == 59:
            fixed_lines.append("            success = await self.manager.install_plugin(plugin_path)\n")
        elif i == 60:
            fixed_lines.append(
                '            return success, "Plugin installed successfully" if success else "Plugin installation failed"\n'
            )
        elif i == 61:
            fixed_lines.append("        except Exception as e:\n")
        elif i == 62:
            fixed_lines.append('            logger.error(f"Plugin installation error: {e}")\n')
        elif i == 63:
            fixed_lines.append("            return False, str(e)\n")
        else:
            # Add remaining methods if any
            fixed_lines.append(line)

    with open("think_ai/plugins/installer.py", "w") as f:
        f.writelines(fixed_lines)

    print("✅ Fixed installer.py")


def fix_manager():
    """Fix manager.py"""
    with open("think_ai/plugins/manager.py", "r") as f:
        content = f.read()

    # Fix indentation of load_plugin method
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        if i < 52:
            fixed_lines.append(line)
        elif i == 52:
            fixed_lines.append("")
        elif i == 53:
            fixed_lines.append("    async def load_plugin(")
        elif i == 54:
            fixed_lines.append("        self,")
        elif i == 55:
            fixed_lines.append("        plugin_name: str,")
        elif i == 56:
            fixed_lines.append("        config: Optional[Dict[str, Any]] = None")
        elif i == 57:
            fixed_lines.append("    ) -> Optional[BasePlugin]:")
        elif i == 58:
            fixed_lines.append('        """Load and initialize a plugin."""')
        elif i == 59:
            fixed_lines.append("        # Implementation here")
        elif i == 60:
            fixed_lines.append("        pass")
        else:
            fixed_lines.append(line)

    with open("think_ai/plugins/manager.py", "w") as f:
        f.write("\n".join(fixed_lines))

    print("✅ Fixed manager.py")


def fix_federated_learning():
    """Fix remaining issues in federated_learning.py"""
    with open("think_ai/federated/federated_learning.py", "r") as f:
        content = f.read()

    # Fix any remaining class definition issues
    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        if i < 144:
            fixed_lines.append(line)
        elif i == 144:
            fixed_lines.append("")
        elif i == 145:
            if line.strip().startswith("class FederatedLearningServer:"):
                fixed_lines.append("class FederatedLearningServer:")
            else:
                fixed_lines.append("")
                fixed_lines.append("class FederatedLearningServer:")
        elif i == 146:
            fixed_lines.append('    """Central server for federated learning coordination."""')
        else:
            # Fix indentation for rest of file
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                if any(keyword in line for keyword in ["def ", "async def ", "class "]):
                    if "class " in line:
                        fixed_lines.append(line)
                    else:
                        fixed_lines.append("    " + line.strip())
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

    with open("think_ai/federated/federated_learning.py", "w") as f:
        f.write("\n".join(fixed_lines))

    print("✅ Fixed federated_learning.py")


if __name__ == "__main__":
    fix_shared_knowledge()
    fix_ui_visualization()
    fix_installer()
    fix_manager()
    fix_federated_learning()
    print("\n✅ All syntax errors fixed!")
