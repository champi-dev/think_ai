#! / usr / bin / env python3

"""
Aggressive dependency compression for serverless deployment
"""

import gzip
import os
import shutil
import sys
import zipfile
from pathlib import Path


class DependencyCompressor:

    def __init__(self, venv_path="venv"):
        self.venv_path = Path(venv_path)
        self.site_packages = self.venv_path / "lib" / \
        f"python{sys.version_info.major}.{sys.version_info.minor}" / "site - packages"

        def compress_wheels(self):
"""Compress all wheel files"""
            print("🗜️ Compressing wheel files...")
            wheels = list(Path(".").glob("*.whl"))

            for wheel in wheels:
                print(f" Compressing {wheel.name}...")
# Re - compress wheel with maximum compression
                with zipfile.ZipFile(wheel, "r") as zin:
                    with zipfile.ZipFile(f"{wheel}.new", "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
                        for item in zin.infolist():
                            data = zin.read(item.filename)
                            zout.writestr(item, data)

                            os.rename(f"{wheel}.new", wheel)

                            def strip_package(self, package_path):
"""Strip unnecessary files from a package"""
                                removals = [
                                "tests", "test", "__pycache__", "*.pyc",
                                "examples", "docs", "benchmarks", "*.md",
                                "LICENSE*", "NOTICE*", "*.txt", "*.rst"
                                ]

                                removed_size = 0
                                for pattern in removals:
                                    for path in Path(package_path).rglob(pattern):
                                        if path.is_file():
                                            size = path.stat().st_size
                                            path.unlink()
                                            removed_size + = size
                                        elif path.is_dir():
                                            shutil.rmtree(path, ignore_errors=True)

                                            return removed_size

                                        def compress_transformers_cache(self):
"""Compress transformers model cache"""
                                            print("🗜️ Compressing model cache...")
                                            cache_dir = Path.home() / ".cache" / "huggingface"

                                            if not cache_dir.exists():
                                                return

# Remove git directories
                                            for git_dir in cache_dir.rglob(".git"):
                                                shutil.rmtree(git_dir)

# Compress large model files
                                                for model_file in cache_dir.rglob("*.bin"):
                                                    if model_file.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                                                    print(f" Compressing {model_file.name}...")
                                                    with open(model_file, "rb") as f_in:
                                                        with gzip.open(f"{model_file}.gz", "wb", compresslevel=9) as f_out:
                                                            shutil.copyfileobj(f_in, f_out)

# Replace with compressed version
                                                            os.remove(model_file)
                                                            os.rename(f"{model_file}.gz", model_file)

                                                            def optimize_site_packages(self):
"""Aggressively optimize site - packages"""
                                                                print("🗜️ Optimizing site - packages...")

                                                                if not self.site_packages.exists():
                                                                    print(" Site - packages not found")
                                                                    return

                                                                total_removed = 0

# Priority packages to keep minimal

                                                                for package_dir in self.site_packages.iterdir():
                                                                    if package_dir.is_dir():
                                                                        package_name = package_dir.name.split("-")[0]

# Skip essential packages
                                                                        if package_name in ["pip", "setuptools", "wheel"]:
                                                                            continue

# Remove test directories
                                                                        removed = self.strip_package(package_dir)
                                                                        total_removed + = removed

# Strip .dist - info directories
                                                                        if package_dir.name.endswith(".dist - info"):
                                                                            for file in package_dir.iterdir():
                                                                                if file.name not in ["METADATA", "WHEEL", "top_level.txt"]:
                                                                                    file.unlink()

                                                                                    print(
                                                                                    f" Removed {
                                                                                    total_removed /
                                                                                    1024 /
                                                                                    1024:.2f} MB of unnecessary files")

                                                                                    def create_lambda_layer(self):
"""Create AWS Lambda layer with compressed dependencies"""
                                                                                        print("🗜️ Creating Lambda layer...")

                                                                                        layer_dir = Path("lambda - layer")
                                                                                        python_dir = layer_dir / "python"
                                                                                        python_dir.mkdir(parents=True, exist_ok=True)

# Copy only essential packages
                                                                                        essential_packages = [
                                                                                        "annoy", "sentence_transformers", "transformers",
                                                                                        "torch", "numpy", "requests", "click"
                                                                                        ]

                                                                                        for package in essential_packages:
                                                                                            for item in self.site_packages.glob(f"{package}*"):
                                                                                                if item.is_dir():
                                                                                                    shutil.copytree(item, python_dir / item.name)

# Create layer zip
                                                                                                    shutil.make_archive("think - ai - layer", "zip", layer_dir)
                                                                                                    shutil.rmtree(layer_dir)

                                                                                                    print(" Created think - ai - layer.zip")

                                                                                                    def create_requirements_minimal(self):
"""Create minimal requirements file"""
                                                                                                        print("📝 Creating minimal requirements...")

                                                                                                        minimal_reqs = """# Minimal requirements for Think AI (no compilation needed)
# Use these for serverless / Vercel deployment

# Core ML (no FAISS)
                                                                                                        annoy > = 1.17.0
                                                                                                        sentence - transformers > = 2.0.0
                                                                                                        torch > = 2.0.0
                                                                                                        transformers > = 4.30.0

# Database clients (optional)
                                                                                                        neo4j > = 5.0.0
# pymilvus > = 2.3.0 # Uncomment if needed

# API (optional)
# fastapi > = 0.100.0 # Uncomment if needed
# uvicorn > = 0.20.0 # Uncomment if needed

# CLI
                                                                                                        click > = 8.0.0
                                                                                                        rich > = 13.0.0
"""

                                                                                                        with open("requirements - minimal.txt", "w") as f:
                                                                                                            f.write(minimal_reqs)

                                                                                                            def optimize_docker_image(self):
"""Create optimized Docker build script"""
                                                                                                                print("🐳 Creating optimized Docker build...")

                                                                                                                docker_script = """#!/bin / bash
# Optimized Docker build script

                                                                                                                echo "Building compressed Docker image..."

# Build with BuildKit for better caching
                                                                                                                DOCKER_BUILDKIT = 1 docker build \
                                                                                                                - f Dockerfile.compressed \
                                                                                                                - - build - arg BUILDKIT_INLINE_CACHE = 1 \
                                                                                                                - - target runtime \
                                                                                                                - t think - ai:compressed .

# Compress the image further
                                                                                                                docker save think - ai:compressed | gzip - 9 > think - ai - compressed.tar.gz

                                                                                                                echo "Compressed image saved to think - ai - compressed.tar.gz"
                                                                                                                echo "Size: $(du -h think - ai - compressed.tar.gz | cut -f1)"

# Create squashed version (even smaller)
                                                                                                                docker export $(docker create think - ai:compressed) | \
                                                                                                                docker import - - change "CMD ["python", " - O", "vector_db_api.py"]" \
                                                                                                                - think - ai:squashed

                                                                                                                echo "Created squashed image think - ai:squashed"
"""

                                                                                                                with open("build - compressed.sh", "w") as f:
                                                                                                                    f.write(docker_script)

                                                                                                                    os.chmod("build - compressed.sh", 0o755)


                                                                                                                    def main():
                                                                                                                        print("🚀 Aggressive Dependency Compression Tool")
                                                                                                                        print("=" * 50)

                                                                                                                        compressor = DependencyCompressor()

# Run all optimizations
                                                                                                                        compressor.create_requirements_minimal()
                                                                                                                        compressor.optimize_site_packages()
                                                                                                                        compressor.compress_transformers_cache()
                                                                                                                        compressor.create_lambda_layer()
                                                                                                                        compressor.optimize_docker_image()

                                                                                                                        print("\n✅ Compression complete!")
                                                                                                                        print("\n📊 Results:")
                                                                                                                        print(" • requirements - minimal.txt - Minimal deps list")
                                                                                                                        print(" • think - ai - layer.zip - AWS Lambda layer")
                                                                                                                        print(" • build - compressed.sh - Docker build script")
                                                                                                                        print(" • Site - packages optimized")
                                                                                                                        print(" • Model cache compressed")

                                                                                                                        print("\n💡 Tips for maximum compression:")
                                                                                                                        print(" 1. Use requirements - minimal.txt for Vercel")
                                                                                                                        print(" 2. Run build - compressed.sh for tiny Docker images")
                                                                                                                        print(" 3. Use think - ai - layer.zip for AWS Lambda")
                                                                                                                        print(" 4. Enable PYTHONOPTIMIZE = 2 in production")


                                                                                                                        if __name__ = = "__main__":
                                                                                                                            main()
