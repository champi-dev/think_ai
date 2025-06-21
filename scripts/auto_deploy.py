#!/usr/bin/env python3
"""
Auto-deployment script for Think AI
Deploys to Vercel, PyPI, Docker Hub when CI passes
"""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("auto_deploy")

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # Manual .env loading
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value


class AutoDeployer:
    """Handles automatic deployment after successful CI."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.version = self._get_version()
        self.deploy_config = self._load_deploy_config()

    def _get_version(self) -> str:
        """Get current version from setup.py or pyproject.toml."""
        setup_py = self.project_root / "setup.py"
        if setup_py.exists():
            with open(setup_py) as f:
                for line in f:
                    if "version=" in line:
                        return line.split('"')[1]
        return "0.1.0"

    def _load_deploy_config(self) -> Dict:
        """Load deployment configuration."""
        config_file = self.project_root / ".deploy.json"
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)

        # Default config
        return {
            "vercel": {
                "enabled": False,
                "project": "think-ai",
                "domain": "think-ai.vercel.app",
            },
            "pypi": {"enabled": True, "repository": "https://upload.pypi.org/legacy/"},
            "docker": {
                "enabled": True,
                "registry": "docker.io",
                "image": "thinkaicolumbia/think-ai",
            },
            "npm": {"enabled": False, "registry": "https://registry.npmjs.org"},
        }

    def check_credentials(self) -> Dict[str, bool]:
        """Check if deployment credentials are available."""
        creds = {}

        # Vercel
        creds["vercel"] = bool(os.getenv("VERCEL_TOKEN"))

        # PyPI
        creds["pypi"] = bool(os.getenv("PYPI_TOKEN") or os.getenv("TWINE_PASSWORD"))

        # Docker Hub
        creds["docker"] = bool(os.getenv("DOCKER_TOKEN") or os.getenv("DOCKER_PASSWORD"))

        # NPM
        creds["npm"] = bool(os.getenv("NPM_TOKEN"))

        return creds

    def deploy_vercel(self) -> bool:
        """Deploy to Vercel."""
        if not self.deploy_config["vercel"]["enabled"]:
            logger.info("Vercel deployment disabled")
            return True

        logger.info("🚀 Deploying to Vercel...")

        try:
            # Install Vercel CLI if needed
            subprocess.run(["npm", "install", "-g", "vercel"], check=True, capture_output=True)

            # Deploy
            env = os.environ.copy()
            env["VERCEL_TOKEN"] = os.getenv("VERCEL_TOKEN", "")

            result = subprocess.run(
                ["vercel", "--prod", "--yes", "--token", env["VERCEL_TOKEN"]],
                cwd=self.project_root,
                env=env,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info(f"✅ Deployed to Vercel: {self.deploy_config['vercel']['domain']}")
                return True
            else:
                logger.error(f"❌ Vercel deployment failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Vercel deployment error: {e}")
            return False

    def deploy_pypi(self) -> bool:
        """Deploy to PyPI."""
        if not self.deploy_config["pypi"]["enabled"]:
            logger.info("PyPI deployment disabled")
            return True

        logger.info("📦 Deploying to PyPI...")

        try:
            # Build distribution
            logger.info("🔨 Building distribution packages...")
            build_process = subprocess.Popen(
                ["python", "-m", "build"],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Show build progress
            while True:
                output = build_process.stdout.readline()
                if output == "" and build_process.poll() is not None:
                    break
                if output:
                    logger.info(f"  Build: {output.strip()}")

            if build_process.returncode != 0:
                stderr = build_process.stderr.read()
                logger.error(f"❌ Build failed: {stderr}")
                return False

            logger.info("✅ Build completed successfully")

            # Upload to PyPI
            env = os.environ.copy()
            if os.getenv("PYPI_TOKEN"):
                env["TWINE_USERNAME"] = "__token__"
                env["TWINE_PASSWORD"] = os.getenv("PYPI_TOKEN")

            logger.info("📤 Uploading to PyPI...")
            upload_process = subprocess.Popen(
                ["twine", "upload", "dist/*", "--skip-existing", "--verbose"],
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            # Show upload progress
            while True:
                output = upload_process.stdout.readline()
                if output == "" and upload_process.poll() is not None:
                    break
                if output:
                    logger.info(f"  Upload: {output.strip()}")

            if upload_process.returncode == 0:
                logger.info(f"✅ Published to PyPI: think-ai=={self.version}")
                return True
            else:
                logger.error(f"❌ PyPI deployment failed with return code: {upload_process.returncode}")
                return False

        except Exception as e:
            logger.error(f"❌ PyPI deployment error: {e}")
            return False

    def deploy_docker(self) -> bool:
        """Deploy to Docker Hub."""
        if not self.deploy_config["docker"]["enabled"]:
            logger.info("Docker deployment disabled")
            return True

        logger.info("🐳 Building and pushing Docker image...")

        try:
            image_name = f"{self.deploy_config['docker']['image']}:{self.version}"
            image_latest = f"{self.deploy_config['docker']['image']}:latest"

            # Build image
            subprocess.run(
                ["docker", "build", "-t", image_name, "-t", image_latest, "."],
                cwd=self.project_root,
                check=True,
            )

            # Login to Docker Hub
            if os.getenv("DOCKER_TOKEN"):
                subprocess.run(
                    [
                        "docker",
                        "login",
                        "-u",
                        os.getenv("DOCKER_USERNAME", "thinkaicolumbia"),
                        "--password-stdin",
                    ],
                    input=os.getenv("DOCKER_TOKEN").encode(),
                    check=True,
                )

            # Push images
            subprocess.run(["docker", "push", image_name], check=True)
            subprocess.run(["docker", "push", image_latest], check=True)

            logger.info(f"✅ Pushed to Docker Hub: {image_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Docker deployment error: {e}")
            return False

    def deploy_npm(self) -> bool:
        """Deploy JavaScript SDK to NPM."""
        if not self.deploy_config["npm"]["enabled"]:
            logger.info("NPM deployment disabled")
            return True

        sdk_path = self.project_root / "sdk" / "js"
        if not sdk_path.exists():
            logger.info("No JavaScript SDK found")
            return True

        logger.info("📦 Publishing to NPM...")

        try:
            # Set NPM token
            if os.getenv("NPM_TOKEN"):
                subprocess.run(
                    [
                        "npm",
                        "config",
                        "set",
                        f"//registry.npmjs.org/:_authToken={os.getenv('NPM_TOKEN')}",
                    ],
                    check=True,
                )

            # Publish
            result = subprocess.run(
                ["npm", "publish", "--access", "public"],
                cwd=sdk_path,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                logger.info("✅ Published to NPM: @thinkaicolumbia/think-ai")
                return True
            else:
                logger.error(f"❌ NPM deployment failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ NPM deployment error: {e}")
            return False

    def run_deployments(self, targets: List[str] = None) -> bool:
        """Run all enabled deployments."""
        if targets is None:
            targets = ["vercel", "pypi", "docker", "npm"]

        # Check credentials
        creds = self.check_credentials()
        logger.info("📋 Deployment credentials check:")
        for service, available in creds.items():
            status = "✅" if available else "❌"
            logger.info(f"  {service}: {status}")

        # Run deployments
        results = {}

        if "vercel" in targets and creds.get("vercel"):
            results["vercel"] = self.deploy_vercel()

        if "pypi" in targets and creds.get("pypi"):
            results["pypi"] = self.deploy_pypi()

        if "docker" in targets and creds.get("docker"):
            results["docker"] = self.deploy_docker()

        if "npm" in targets and creds.get("npm"):
            results["npm"] = self.deploy_npm()

        # Summary
        logger.info("\n📊 Deployment Summary")
        logger.info("=" * 40)

        all_success = True
        for service, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            logger.info(f"{service}: {status}")
            if not success:
                all_success = False

        return all_success


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Think AI Auto Deployment")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=["vercel", "pypi", "docker", "npm"],
        help="Deployment targets (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without deploying",
    )

    args = parser.parse_args()

    deployer = AutoDeployer()

    if args.dry_run:
        logger.info("🔍 Dry run mode - no actual deployments")
        creds = deployer.check_credentials()
        logger.info(f"Version to deploy: {deployer.version}")
        logger.info(f"Available credentials: {creds}")
        return

    # Run deployments
    success = deployer.run_deployments(args.targets)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
