#!/usr/bin/env python3
"""Startup wrapper that ensures transformers is patched before any imports."""

import sys
import os

# CRITICAL: Monkey-patch transformers BEFORE it's imported anywhere
print("🔧 Applying transformers monkey patch...")


# Create a fake module that will be imported instead
class FakeReplaceListOption:
    def __call__(self, *args, **kwargs):
        def decorator(fn):
            return fn

        return decorator


# Inject into sys.modules to intercept the import
fake_module = type(sys)("fake_config_auto")
fake_module.replace_list_option_in_docstrings = FakeReplaceListOption()

# Pre-populate the module cache
sys.modules["transformers.models.auto.configuration_auto"] = fake_module

# Now patch the actual module when it loads
original_import = __builtins__.__import__


def patched_import(name, *args, **kwargs):
    module = original_import(name, *args, **kwargs)

    # If this is the problematic module, patch it
    if name == "transformers.models.auto.configuration_auto" or (
        hasattr(module, "__name__") and module.__name__ == "transformers.models.auto.configuration_auto"
    ):
        if hasattr(module, "replace_list_option_in_docstrings"):
            print("🩹 Patching transformers.models.auto.configuration_auto")
            module.replace_list_option_in_docstrings = FakeReplaceListOption()

    return module


__builtins__.__import__ = patched_import

print("✅ Transformers pre-patch complete")

# Now import and run the actual application
try:
    from think_ai_full import app
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Starting Think AI Full System on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
except Exception as e:
    print(f"❌ Failed to start Think AI: {e}")
    print("🔄 Starting emergency server...")

    # Fall back to emergency server
    from emergency_server import app
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
