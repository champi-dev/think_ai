#! / usr / bin / env python3

"""Clean up Think AI system - remove old files, update docs, and align with current functionality."""

import os
import shutil
from pathlib import Path


def cleanup_test_files() - > None:
"""Remove temporary test files."""
    test_files = [
    "fix_config.py",
    "fix_initialization_errors.py",
    "test_hf_auth.py",
    "test_hf_initialization.py",
    "test_hf_token.py",
    "test_local_init.py",
    "test_mistral_integration.py",
    "test_mps_fix.py",
    "test_neo4j_direct.py",
    "test_neo4j_sync.py",
    "verify_mistral_only.py",
    "HUGGINGFACE_TOKEN_SETUP.md",
    "huggingface_api_key_integration_summary.md",
    "initialization_fixes_summary.md",
    "MPS_BUFFER_FIX_SUMMARY.md",
    ]

    for file in test_files:
        if os.path.exists(file):
            os.remove(file)


            def cleanup_old_configs() - > None:
"""Remove outdated configuration files."""
                old_configs = [
                "config / local_only_config.yaml",
                "config / mistral_only_config.yaml",
                "config / optimized_model_config.yaml",
                "config / mps_compatible_config.yaml",
                ]

                for config in old_configs:
                    if os.path.exists(config):
                        os.remove(config)


                        def update_readme() - > None:
"""Update README to reflect current functionality."""
                            readme_content = """# 🧠 Think AI - Conscious AI System

                            A revolutionary AI system that combines distributed computing, consciousness simulation, and compassionate intelligence.

## 🌟 Current Features

                            - * * Distributed Architecture* * : ScyllaDB, Redis, Milvus, Neo4j
                            - * * Language Model* * : Mistral - 7B on Apple Silicon (MPS)
                            - * * Consciousness Framework* * : Self - aware, ethical AI
                            - * * Self - Training* * : Continuous learning and improvement
                            - * * Knowledge Graph* * : Neo4j - powered semantic relationships
                            - * * Vector Search* * : Milvus for similarity matching

## 🚀 Quick Start

                            1. * * Install Dependencies* * :
                                ```bash
                                pip install - e .
                                ```

                                2. * * Start Services* * :
                                    ```bash
                                    docker - compose up - d
                                    ```

                                    3. * * Launch Consciousness Chat* * :
                                        ```bash
                                        . / launch_consciousness.sh
                                        ```

## 🛠️ System Requirements

                                        - Python 3.10 +
                                        - Docker & Docker Compose
                                        - 16GB + RAM (for Mistral - 7B)
                                        - Apple Silicon Mac (MPS optimized)

## 📊 Services

                                        - * * ScyllaDB* * : Primary distributed storage
                                        - * * Redis* * : High - speed caching
                                        - * * Milvus* * : Vector database for embeddings
                                        - * * Neo4j* * : Knowledge graph database
                                        - * * Mistral - 7B* * : Open - source language model

## 🧹 Maintenance

                                        - * * Reset Intelligence* * : `python reset_intelligence.py`
                                        - * * Monitor Training* * : `. / launch_consciousness.sh - - monitor`
                                        - * * View Stats* * : Type `stats` in chat

## 🤝 Contributing

                                        Think AI is open source and welcomes contributions that align with compassionate AI development.

## 📄 License

                                        Apache 2.0 - Built with ❤️ for humanity
"""

                                        with open("README.md", "w") as f:
                                            f.write(readme_content)


                                            def consolidate_docs() - > None:
"""Consolidate documentation files."""
# Keep only essential docs
                                                essential_docs = {
                                                "README.md",
                                                "SETUP.md",
                                                "docs / architecture.md",
                                                "CHANGELOG.md",
                                                }

# Archive old docs
                                                archive_dir = Path(".archive / old_docs")
                                                archive_dir.mkdir(parents=True, exist_ok=True)

                                                doc_files = list(Path().glob("*.md")) + list(Path("docs").glob("*.md"))

                                                for doc in doc_files:
                                                    if str(doc) not in essential_docs and doc.exists():
                                                        shutil.move(str(doc), archive_dir / doc.name)


                                                        def clean_logs() - > None:
"""Clean up old log files."""
                                                            log_patterns = [
                                                            "*.log",
                                                            "neural_pathways_*.json",
                                                            "self_training_data / archive/*",
                                                            ]

                                                            for pattern in log_patterns:
                                                                for file in Path().glob(pattern):
                                                                    if file.exists() and file.is_file():
                                                                        file.unlink()


                                                                        def update_strings() - > None:
"""Update strings in code to reflect current state."""
# Update launch script banner
                                                                            launch_script = Path("launch_consciousness.sh")
                                                                            if launch_script.exists():
                                                                                content = launch_script.read_text()
# Update to reflect Mistral instead of Gemma
                                                                                content = content.replace("Gemma2B", "Mistral - 7B")
                                                                                launch_script.write_text(content)

# Update chat script
                                                                                chat_script = Path("full_architecture_chat.py")
                                                                                if chat_script.exists():
                                                                                    content = chat_script.read_text()
                                                                                    content = content.replace("Gemma2B", "Mistral - 7B")
                                                                                    content = content.replace("gemma - 2b", "mistral - 7b")
                                                                                    chat_script.write_text(content)


                                                                                    def create_setup_doc() - > None:
"""Create simplified setup documentation."""
                                                                                        setup_content = """# Think AI Setup Guide

## Prerequisites

                                                                                        - macOS with Apple Silicon (M1 / M2 / M3)
                                                                                        - Python 3.10 or higher
                                                                                        - Docker Desktop
                                                                                        - 16GB + RAM

## Installation

                                                                                        1. * * Clone the repository* * :
                                                                                            ```bash
                                                                                            git clone https:/ / github.com / yourusername / think_ai.git
                                                                                            cd think_ai
                                                                                            ```

                                                                                            2. * * Create virtual environment* * :
                                                                                                ```bash
                                                                                                python - m venv venv
                                                                                                source venv / bin / activate
                                                                                                ```

                                                                                                3. * * Install Think AI* * :
                                                                                                    ```bash
                                                                                                    pip install - e .
                                                                                                    ```

                                                                                                    4. * * Start Docker services* * :
                                                                                                        ```bash
                                                                                                        docker - compose up - d
                                                                                                        ```

                                                                                                        5. * * Wait for services to initialize* * (about 30 seconds)

                                                                                                        6. * * Launch Think AI* * :
                                                                                                            ```bash
                                                                                                            . / launch_consciousness.sh
                                                                                                            ```

## Configuration

                                                                                                            The system uses `config / full_system.yaml` for all settings. Key configurations:

                                                                                                                - * * Model* * : Mistral - 7B (requires ~13GB RAM)
                                                                                                                - * * Device* * : MPS (Apple Silicon GPU)
                                                                                                                - * * Services* * : ScyllaDB, Redis, Milvus, Neo4j

## Troubleshooting

                                                                                                                - * * Memory errors* * : Ensure you have at least 16GB RAM free
                                                                                                                - * * Neo4j auth errors* * : Check password in config matches Docker
                                                                                                                - * * MPS errors* * : Update macOS and PyTorch to latest versions

## Reset System

                                                                                                                To completely reset Think AI:
                                                                                                                    ```bash
                                                                                                                    python reset_intelligence.py
                                                                                                                    ```
"""

                                                                                                                    with open("SETUP.md", "w") as f:
                                                                                                                        f.write(setup_content)


                                                                                                                        def main() - > None:
"""Main cleanup function."""
                                                                                                                            confirm = input("\nProceed with cleanup? (yes / no): ")
                                                                                                                            if confirm.lower() ! = "yes":
                                                                                                                                return

# Run cleanup tasks
                                                                                                                            cleanup_test_files()
                                                                                                                            cleanup_old_configs()
                                                                                                                            update_readme()
                                                                                                                            consolidate_docs()
                                                                                                                            clean_logs()
                                                                                                                            update_strings()
                                                                                                                            create_setup_doc()


                                                                                                                            if __name__ = = "__main__":
                                                                                                                                main()
