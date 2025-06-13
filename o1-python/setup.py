from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    setup(
    name="o1-vector-search",
    version="1.0.0",
    author="Think AI Lab",
    author_email="hello@thinkai.dev",
    description="O(1) Vector Search - Instant similarity search with LSH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/champi-dev/o1-vector-search",
    packages=find_packages(),
    classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
    "numpy>=1.19.0",
    ],
    extras_require={
    "dev": [
    "pytest>=6.0",
# Think AI Linter handles all code quality
    ],
    },
    keywords="vector-search o1 lsh similarity-search machine-learning ai",
    project_urls={
    "Bug Reports": "https://github.com/champi-dev/o1-vector-search/issues",
    "Source": "https://github.com/champi-dev/o1-vector-search",
    },
    )
