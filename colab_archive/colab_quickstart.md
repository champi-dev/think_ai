# Google Colab Quick Start Guide

## 🚀 One-Click Setup

Copy and paste this into a Google Colab cell:

```python
# Clone the repository
!git clone https://github.com/yourusername/Think_AI.git
%cd Think_AI

# Run the setup script
!python colab_setup.py

# Optional: Run a simple test
!python chat_simple.py
```

## 📋 What the Setup Script Does

1. **Fixes NVIDIA Package Corruption**: Removes the corrupted `~vidia-nccl-cu12` packages
2. **Resolves Dependency Conflicts**: Ensures fastapi/starlette versions are compatible with Gradio
3. **Fixes Marshmallow**: Installs the correct version for Milvus compatibility
4. **Creates Configuration**: Sets up a `.env` file with Colab-specific settings
5. **Enables Mock Services**: Since Colab can't run external databases, it uses mock services

## 🔧 Manual Fix (if needed)

If you still see the NVIDIA warning, run this:

```python
import os
import shutil

# Remove corrupted packages
dist_dir = "/usr/local/lib/python3.11/dist-packages"
for item in os.listdir(dist_dir):
    if item.startswith("~vidia"):
        path = os.path.join(dist_dir, item)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        print(f"Removed: {item}")

# Clear pip cache
!pip cache purge
```

## 🎯 Running Think AI in Colab

After setup, you can run:

1. **Simple Chat Mode** (recommended for Colab):
   ```python
   !python chat_simple.py
   ```

2. **Full Architecture** (will use mock services):
   ```python
   !python full_architecture_chat.py
   ```

## ⚠️ Colab Limitations

- External databases (ScyllaDB, Redis, Milvus, Neo4j) won't work
- The system will use mock services instead
- GPU acceleration works if you enable it in Colab
- Session data is temporary and will be lost when the runtime disconnects

## 💡 Tips

- Use GPU runtime for better performance: Runtime → Change runtime type → GPU
- Save important outputs to Google Drive
- The setup script creates `/content/think_ai_data` for local storage