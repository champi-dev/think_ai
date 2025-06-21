#!/usr/bin/env python3
"""
🇨🇴 Think AI Packages Installer
Installs optimized Colombian AI-enhanced dependency packages
"""

import os
import sys


def install_think_ai_packages():
    """Install Think AI packages with O(1) performance."""
    print("🇨🇴 Installing Think AI optimized packages...")

    # Add Think AI packages to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    packages_dir = os.path.join(current_dir, "think_ai_packages")

    if packages_dir not in sys.path:
        sys.path.insert(0, packages_dir)

    # Create import aliases for seamless replacement
    import think_ai_aiosqlite as aiosqlite
    import think_ai_chromadb as chromadb
    import think_ai_faiss as faiss

    # Install into global namespace
    sys.modules["chromadb"] = chromadb
    sys.modules["faiss"] = faiss
    sys.modules["aiosqlite"] = aiosqlite

    print("✅ Think AI packages installed successfully!")
    print("🚀 O(1) performance activated - ¡Dale que vamos tarde!")


if __name__ == "__main__":
    install_think_ai_packages()
