from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="think-ai-cli",
    version="0.1.0",
    author="Think AI",
    description="AI-powered coding assistant with vector search capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/champi-dev/think_ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "sentence-transformers>=2.0.0",
        "requests>=2.25.0",
        "pyyaml>=6.0",
        "pygments>=2.10.0",
    ],
    entry_points={
        "console_scripts": [
            "think=think_ai_cli.cli:main",
        ],
    },
)
