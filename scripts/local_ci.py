#!/usr/bin/env python3
"""
Local CI/CD runner for Think AI
Detects GPU and runs appropriate tests locally
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from think_ai.utils.logging import get_logger

logger = get_logger("local_ci")


def detect_gpu():
    """Detect if GPU is available."""
    gpu_info = {
        "cuda_available": False,
        "cuda_version": None,
        "gpu_count": 0,
        "gpu_names": [],
        "driver_version": None,
    }

    # Check for NVIDIA GPU
    try:
        # Check if nvidia-smi exists
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
        )

        lines = result.stdout.strip().split("\n")
        for line in lines:
            if line:
                name, driver = line.split(", ")
                gpu_info["gpu_names"].append(name)
                gpu_info["driver_version"] = driver

        gpu_info["gpu_count"] = len(gpu_info["gpu_names"])
        gpu_info["cuda_available"] = gpu_info["gpu_count"] > 0

        # Get CUDA version
        try:
            result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True, check=True)
            # Extract version from output
            for line in result.stdout.split("\n"):
                if "release" in line:
                    gpu_info["cuda_version"] = line.split("release")[-1].strip().split(",")[0]
                    break
        except:
            pass

    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.info("No NVIDIA GPU detected")

    # Check for AMD GPU (ROCm)
    try:
        result = subprocess.run(["rocm-smi", "--showproductname"], capture_output=True, text=True, check=True)
        if "GPU" in result.stdout:
            gpu_info["gpu_names"].append("AMD GPU (ROCm)")
            gpu_info["gpu_count"] += 1
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Check for Apple Silicon GPU
    if platform.system() == "Darwin" and platform.processor() == "arm":
        gpu_info["gpu_names"].append("Apple Silicon GPU")
        gpu_info["gpu_count"] += 1
        gpu_info["cuda_available"] = False  # MPS instead

    return gpu_info


def run_local_ci(gpu_info):
    """Run local CI/CD pipeline."""
    logger.info("🚀 Starting Think AI Local CI/CD Pipeline")

    # Display GPU info
    if gpu_info["gpu_count"] > 0:
        logger.info(f"✅ GPU detected: {', '.join(gpu_info['gpu_names'])}")
        if gpu_info["cuda_version"]:
            logger.info(f"   CUDA version: {gpu_info['cuda_version']}")
        if gpu_info["driver_version"]:
            logger.info(f"   Driver version: {gpu_info['driver_version']}")
    else:
        logger.warning("⚠️  No GPU detected - running in CPU mode")

    # Set environment variables
    env = os.environ.copy()
    env["CI"] = "false"  # Don't use mocks locally
    env["LOCAL_CI"] = "true"
    env["PYTHONPATH"] = str(project_root)

    if gpu_info["cuda_available"]:
        env["CUDA_VISIBLE_DEVICES"] = "0"  # Use first GPU
        env["THINK_AI_USE_GPU"] = "true"

    # Test stages
    stages = [
        {
            "name": "🔍 Linting",
            "command": ["python", "think_ai_linter.py", "--check"],
            "critical": True,
        },
        {
            "name": "🧪 Unit Tests",
            "command": ["pytest", "tests/unit", "-v", "--tb=short"],
            "critical": True,
        },
        {
            "name": "🔗 Integration Tests",
            "command": ["pytest", "tests/integration", "-v", "--tb=short"],
            "critical": False,
        },
        {
            "name": "🚀 Performance Tests",
            "command": ["pytest", "tests/performance", "-v", "--tb=short", "-k", "not slow"],
            "critical": False,
        },
    ]

    # Add GPU-specific tests if available
    if gpu_info["gpu_count"] > 0:
        stages.append(
            {
                "name": "🎮 GPU Tests",
                "command": ["pytest", "tests/gpu", "-v", "--tb=short"],
                "critical": False,
            }
        )

        # Run full model tests with GPU
        stages.append(
            {
                "name": "🤖 Model Tests (GPU)",
                "command": ["pytest", "tests/models", "-v", "--tb=short", "-k", "not cpu_only"],
                "critical": False,
            }
        )

    # Run stages
    failed_stages = []
    for stage in stages:
        logger.info(f"\n{stage['name']}")
        logger.info("=" * 50)

        try:
            result = subprocess.run(
                stage["command"],
                env=env,
                cwd=project_root,
                check=True,
                capture_output=False,  # Show output in real-time
            )
            logger.info(f"✅ {stage['name']} passed")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {stage['name']} failed with exit code {e.returncode}")
            failed_stages.append(stage["name"])

            if stage["critical"]:
                logger.error("Critical stage failed - stopping pipeline")
                return False

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Local CI/CD Summary")
    logger.info("=" * 50)

    if failed_stages:
        logger.error(f"Failed stages: {', '.join(failed_stages)}")
        return False
    else:
        logger.info("✅ All stages passed!")
        return True


def setup_local_services():
    """Setup local services for testing."""
    logger.info("🔧 Setting up local services...")

    services = []

    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)

        # Start local services
        logger.info("Starting Docker services...")

        # ScyllaDB
        subprocess.run(
            ["docker", "run", "-d", "--name", "think-ai-scylla", "-p", "9042:9042", "scylladb/scylla:5.2"],
            capture_output=True,
        )
        services.append("think-ai-scylla")

        # Redis
        subprocess.run(
            ["docker", "run", "-d", "--name", "think-ai-redis", "-p", "6379:6379", "redis:7-alpine"],
            capture_output=True,
        )
        services.append("think-ai-redis")

        # Neo4j
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                "think-ai-neo4j",
                "-p",
                "7687:7687",
                "-p",
                "7474:7474",
                "-e",
                "NEO4J_AUTH=neo4j/testpassword",
                "neo4j:5-community",
            ],
            capture_output=True,
        )
        services.append("think-ai-neo4j")

        logger.info("✅ Docker services started")

    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("⚠️  Docker not available - skipping service setup")
        logger.info("   Install Docker or run services manually")

    return services


def cleanup_services(services):
    """Stop and remove Docker services."""
    if services:
        logger.info("🧹 Cleaning up services...")
        for service in services:
            subprocess.run(["docker", "stop", service], capture_output=True)
            subprocess.run(["docker", "rm", service], capture_output=True)
        logger.info("✅ Services cleaned up")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Think AI Local CI/CD Runner")
    parser.add_argument("--no-services", action="store_true", help="Skip Docker service setup")
    parser.add_argument("--gpu-only", action="store_true", help="Only run if GPU is detected")
    parser.add_argument("--keep-services", action="store_true", help="Don't cleanup services after run")
    args = parser.parse_args()

    # Detect GPU
    gpu_info = detect_gpu()

    # Check GPU requirement
    if args.gpu_only and gpu_info["gpu_count"] == 0:
        logger.error("❌ No GPU detected and --gpu-only flag was set")
        sys.exit(1)

    # Setup services
    services = []
    if not args.no_services:
        services = setup_local_services()

    try:
        # Run CI pipeline
        success = run_local_ci(gpu_info)

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    finally:
        # Cleanup
        if services and not args.keep_services:
            cleanup_services(services)


if __name__ == "__main__":
    main()
