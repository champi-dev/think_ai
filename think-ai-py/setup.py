#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thinkai-quantum",
    version="1.0.5",
    author="champi-dev",
    author_email="danielsarcor@gmail.com",
    description="Think AI - Quantum Consciousness AI Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/champi-dev/think_ai",
    project_urls={
        "Homepage": "https://thinkai.lat",
        "Bug Tracker": "https://github.com/champi-dev/think_ai/issues",
        "Documentation": "https://github.com/champi-dev/think_ai/blob/main/README.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "websocket-client>=1.0.0",
        "click>=8.0.0",
        "rich>=10.0.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0",
        "asyncio-throttle>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=1.0.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "think-ai=think_ai.cli:main",
        ],
    },
    keywords="ai consciousness quantum machine-learning nlp chat intelligence think-ai",
    include_package_data=True,
    zip_safe=False,
)
