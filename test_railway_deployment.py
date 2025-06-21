#!/usr/bin/env python3
"""Test Railway deployment configuration locally with elite standards."""

import os
import subprocess
import sys
import time
from typing import Optional, Tuple

import requests


class DeploymentTester:
    """O(1) deployment verification system."""

    def __init__(self):
        self.container_name = "think-ai-railway-test"
        self.image_name = "think-ai-railway:test"
        self.test_results = {}

    def build_docker_image(self) -> bool:
        """Build Docker image with optimal caching."""
        print("🔨 Building Docker image...")
        try:
            result = subprocess.run(
                ["docker", "build", "-f", "Dockerfile.railway", "-t", self.image_name, "."],
                capture_output=True,
                text=True,
                check=True,
            )
            print("✅ Docker image built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker build failed: {e.stderr}")
            return False

    def run_container(self) -> bool:
        """Run container with proper configuration."""
        print("🚀 Starting container...")

        # Stop existing container if running
        subprocess.run(["docker", "stop", self.container_name], capture_output=True)
        subprocess.run(["docker", "rm", self.container_name], capture_output=True)

        try:
            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "-d",
                    "--name",
                    self.container_name,
                    "-p",
                    "8080:8080",
                    "-e",
                    "PORT=8080",
                    self.image_name,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            print("✅ Container started successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Container start failed: {e.stderr}")
            return False

    def wait_for_services(self, timeout: int = 60) -> bool:
        """Wait for all services to be ready with O(1) health checks."""
        print("⏳ Waiting for services to start...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Check health endpoint
                response = requests.get("http://localhost:8080/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Services are ready!")
                    return True
            except requests.exceptions.RequestException:
                pass

            time.sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()

        print("\n❌ Services failed to start within timeout")
        return False

    def test_api_endpoint(self) -> Tuple[bool, Optional[str]]:
        """Test API backend endpoint."""
        print("\n🧪 Testing API endpoint...")
        try:
            response = requests.get("http://localhost:8080/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ API endpoint working")
                return True, response.text
            else:
                print(f"❌ API returned status {response.status_code}")
                return False, None
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False, None

    def test_webapp_endpoint(self) -> Tuple[bool, Optional[str]]:
        """Test webapp frontend."""
        print("\n🧪 Testing webapp endpoint...")
        try:
            response = requests.get("http://localhost:8080/", timeout=5)
            if response.status_code == 200 and "Think AI" in response.text:
                print("✅ Webapp endpoint working")
                return True, "Homepage loaded"
            else:
                print(f"❌ Webapp returned status {response.status_code}")
                return False, None
        except Exception as e:
            print(f"❌ Webapp test failed: {e}")
            return False, None

    def test_websocket_support(self) -> bool:
        """Test WebSocket connectivity."""
        print("\n🧪 Testing WebSocket support...")
        try:
            # Test WebSocket upgrade headers
            response = requests.get(
                "http://localhost:8080/ws", headers={"Upgrade": "websocket", "Connection": "Upgrade"}, timeout=2
            )
            # WebSocket should return 426 Upgrade Required or similar
            if response.status_code in [426, 400, 101]:
                print("✅ WebSocket endpoint accessible")
                return True
            else:
                print(f"❌ Unexpected WebSocket response: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ WebSocket test failed: {e}")
            return False

    def check_container_logs(self):
        """Display container logs for debugging."""
        print("\n📋 Container logs:")
        subprocess.run(["docker", "logs", "--tail", "50", self.container_name])

    def cleanup(self):
        """Clean up test resources."""
        print("\n🧹 Cleaning up...")
        subprocess.run(["docker", "stop", self.container_name], capture_output=True)
        subprocess.run(["docker", "rm", self.container_name], capture_output=True)
        print("✅ Cleanup complete")

    def run_all_tests(self) -> bool:
        """Execute all deployment tests with elite standards."""
        print("🎯 Think AI Railway Deployment Test Suite\n")

        all_passed = True

        # Build image
        if not self.build_docker_image():
            return False

        # Run container
        if not self.run_container():
            return False

        # Wait for services
        if not self.wait_for_services():
            self.check_container_logs()
            self.cleanup()
            return False

        # Run tests
        api_passed, _ = self.test_api_endpoint()
        webapp_passed, _ = self.test_webapp_endpoint()
        ws_passed = self.test_websocket_support()

        all_passed = api_passed and webapp_passed and ws_passed

        # Show results
        print("\n" + "=" * 50)
        print("📊 Test Results:")
        print(f"  API Backend: {'✅ PASS' if api_passed else '❌ FAIL'}")
        print(f"  Webapp Frontend: {'✅ PASS' if webapp_passed else '❌ FAIL'}")
        print(f"  WebSocket Support: {'✅ PASS' if ws_passed else '❌ FAIL'}")
        print("=" * 50)

        if not all_passed:
            self.check_container_logs()

        self.cleanup()

        return all_passed


def main():
    """Run deployment tests."""
    tester = DeploymentTester()
    success = tester.run_all_tests()

    if success:
        print("\n✅ All deployment tests passed! Ready for Railway deployment.")
        print("\n📝 Next steps:")
        print("1. Commit these files to your repository")
        print("2. Push to GitHub")
        print("3. Deploy on Railway using this repository")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
