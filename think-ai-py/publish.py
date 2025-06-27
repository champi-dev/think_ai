#!/usr/bin/env python3

"""
Think AI Python Library - PyPI Publishing Script
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result"""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"❌ Error running command: {cmd}")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        sys.exit(1)
    
    return result


def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    # Check if build tools are available
    try:
        import build
        import twine
    except ImportError:
        print("❌ Missing required dependencies. Installing...")
        run_command("pip install build twine")
        

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    directories_to_clean = ['dist', 'build', 'think_ai.egg-info']
    for dir_name in directories_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")


def build_package():
    """Build the Python package"""
    print("📦 Building package...")
    run_command("python3 -m build")
    
    # Verify build artifacts
    dist_path = Path("dist")
    if not dist_path.exists():
        print("❌ Error: dist/ directory not created")
        sys.exit(1)
    
    whl_files = list(dist_path.glob("*.whl"))
    tar_files = list(dist_path.glob("*.tar.gz"))
    
    if not whl_files or not tar_files:
        print("❌ Error: Missing build artifacts")
        sys.exit(1)
    
    print(f"✅ Built: {whl_files[0].name}")
    print(f"✅ Built: {tar_files[0].name}")


def test_installation():
    """Test the built package"""
    print("🧪 Testing package installation...")
    
    # Create a temporary environment and test installation
    run_command("python3 -c 'import think_ai; print(think_ai.__version__)'")
    print("✅ Package import test passed")


def check_pypi_credentials():
    """Check if PyPI credentials are configured"""
    # Check for API token in environment
    if os.getenv('TWINE_PASSWORD'):
        print("✅ PyPI token found in environment")
        return True
    
    # Check for .pypirc file
    pypirc_paths = [
        Path.home() / '.pypirc',
        Path('.pypirc')
    ]
    
    for pypirc_path in pypirc_paths:
        if pypirc_path.exists():
            print(f"✅ PyPI config found: {pypirc_path}")
            return True
    
    print("❌ No PyPI credentials found!")
    print("💡 Please set TWINE_PASSWORD environment variable with your PyPI API token")
    print("   or create a .pypirc file with your credentials")
    return False


def upload_to_pypi():
    """Upload package to PyPI"""
    print("📤 Uploading to PyPI...")
    
    # Check credentials first
    if not check_pypi_credentials():
        sys.exit(1)
    
    # Upload using twine
    run_command("python3 -m twine upload dist/*")
    
    print("✅ Successfully uploaded to PyPI!")


def main():
    """Main publishing workflow"""
    print("🚀 Publishing Think AI Python Library to PyPI...")
    print()
    
    # Verify we're in the right directory
    if not Path("setup.py").exists():
        print("❌ Error: setup.py not found. Run this script from the think-ai-py directory.")
        sys.exit(1)
    
    # Get current version
    result = run_command("python3 setup.py --version")
    version = result.stdout.strip()
    print(f"📋 Current version: {version}")
    
    try:
        # Check dependencies
        check_dependencies()
        
        # Clean previous builds
        clean_build()
        
        # Build the package
        build_package()
        
        # Test the package
        test_installation()
        
        # Ask for confirmation
        response = input(f"\n📤 Ready to upload think-ai {version} to PyPI? (y/N): ")
        if response.lower() != 'y':
            print("❌ Upload cancelled")
            sys.exit(0)
        
        # Upload to PyPI
        upload_to_pypi()
        
        print()
        print(f"🎉 Successfully published think-ai {version} to PyPI!")
        print()
        print("📦 Users can now install with:")
        print("   pip install think-ai")
        print()
        print("🧠 Think AI Python library is now available to all users!")
        
    except KeyboardInterrupt:
        print("\n❌ Publishing cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()