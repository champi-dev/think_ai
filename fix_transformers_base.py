#!/usr/bin/env python3
"""Permanently fix transformers in the base image."""

import os
import sys

# Find the transformers installation
site_packages = None
for path in sys.path:
    if "site-packages" in path and os.path.exists(path):
        config_path = os.path.join(path, "transformers", "models", "auto", "configuration_auto.py")
        if os.path.exists(config_path):
            site_packages = path
            break

if not site_packages:
    print("❌ Could not find transformers installation")
    sys.exit(1)

config_file = os.path.join(site_packages, "transformers", "models", "auto", "configuration_auto.py")
print(f"📝 Patching {config_file}")

# Read the file
with open(config_file, "r") as f:
    content = f.read()

# Replace the problematic decorator
if "@replace_list_option_in_docstrings()" in content:
    content = content.replace(
        "@replace_list_option_in_docstrings()",
        "# @replace_list_option_in_docstrings()  # Patched by fix_transformers_base.py",
    )

    # Write back
    with open(config_file, "w") as f:
        f.write(content)

    print("✅ Transformers patched successfully!")
else:
    print("⚠️  Decorator not found or already patched")

# Also create a startup patch
startup_patch = os.path.join(site_packages, "transformers_patch.py")
with open(startup_patch, "w") as f:
    f.write(
        """# Auto-patch for transformers
def patch():
    try:
        import transformers.models.auto.configuration_auto as config_auto
        config_auto.replace_list_option_in_docstrings = lambda *args, **kwargs: lambda fn: fn
    except:
        pass

patch()
"""
    )

print("✅ Created startup patch")
