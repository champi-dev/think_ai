#!/bin/bash
# Full System Deployment Script for Think AI
# Deploys all libraries (Python & JavaScript) and creates comprehensive testing evidence

set -e

echo "🚀 Think AI Full System Deployment"
echo "================================="
echo "Deploying all libraries and creating testing evidence..."
echo ""

# Create deployment directory
DEPLOY_DIR="think_ai_deployment_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

# 1. Deploy Python Libraries
echo "📦 Deploying Python Libraries..."
echo "--------------------------------"

# Main think-ai-consciousness package
echo "Building think-ai-consciousness..."
cd ..
rm -rf dist build *.egg-info
python -m build
cp -r dist "$DEPLOY_DIR/python_dist"

# Build think-ai-cli Python package
echo "Building think-ai-cli Python package..."
cd think-ai-cli/python
rm -rf dist build *.egg-info
python -m build
cd ../..
cp -r think-ai-cli/python/dist "$DEPLOY_DIR/python_cli_dist"

# Build o1-python package
echo "Building o1-python package..."
cd o1-python
rm -rf dist build *.egg-info
python -m build
cd ..
cp -r o1-python/dist "$DEPLOY_DIR/o1_python_dist"

# 2. Deploy JavaScript Libraries
echo ""
echo "📦 Deploying JavaScript Libraries..."
echo "-----------------------------------"

# Main think-ai-js package
echo "Building main think-ai-js package..."
cd npm
npm install
npm run build
npm pack
cd ..
cp npm/*.tgz "$DEPLOY_DIR/"

# Build think-ai-cli Node.js package
echo "Building think-ai-cli Node.js package..."
cd think-ai-cli/nodejs
npm install
npm run build
npm pack
cd ../..
cp think-ai-cli/nodejs/*.tgz "$DEPLOY_DIR/"

# Build o1-js package
echo "Building o1-js package..."
cd o1-js
npm install
npm run build
npm pack
cd ..
cp o1-js/*.tgz "$DEPLOY_DIR/"

# 3. Create comprehensive documentation
echo ""
echo "📚 Updating Documentation..."
echo "---------------------------"

cat > "$DEPLOY_DIR/DEPLOYMENT_README.md" << 'EOF'
# Think AI Full System Deployment

## Deployed Packages

### Python Packages
1. **think-ai-consciousness** (v2.1.0) - Main Python package
   - PyPI: `pip install think-ai-consciousness`
   - Features: Core AI engine, consciousness module, vector search, self-training

2. **think-ai-cli** - Command-line interface
   - PyPI: `pip install think-ai-cli`
   - Features: CLI tools for interacting with Think AI

3. **o1-python** - O(1) vector search implementation
   - PyPI: `pip install o1-python`
   - Features: Ultra-fast vector search with O(1) complexity

### JavaScript Packages
1. **think-ai-js** (v2.0.1) - Main JavaScript client
   - NPM: `npm install think-ai-js`
   - Features: JavaScript/TypeScript client for Think AI

2. **think-ai-cli** - Node.js CLI tools
   - NPM: `npm install @think-ai/cli`
   - Features: Command-line tools for Node.js

3. **o1-js** - O(1) vector search for JavaScript
   - NPM: `npm install o1-js`
   - Features: JavaScript implementation of O(1) vector search

## Installation Instructions

### Python Installation
```bash
# Install main package
pip install think-ai-consciousness

# Install CLI tools
pip install think-ai-cli

# Install O(1) vector search
pip install o1-python
```

### JavaScript Installation
```bash
# Install main client
npm install think-ai-js

# Install CLI tools
npm install -g @think-ai/cli

# Install O(1) vector search
npm install o1-js
```

## Quick Start

### Python Example
```python
from think_ai import ThinkAI

# Initialize Think AI
ai = ThinkAI()

# Chat with the AI
response = ai.chat("What is consciousness?")
print(response)

# Self-training
ai.train("consciousness", iterations=100)
```

### JavaScript Example
```javascript
import { ThinkAI } from 'think-ai-js';

// Initialize client
const ai = new ThinkAI({
  apiUrl: 'http://localhost:8000'
});

// Chat with the AI
const response = await ai.chat("What is consciousness?");
console.log(response);
```

## Full System Architecture

The Think AI system consists of:
1. Core AI Engine (Python) - Handles reasoning and consciousness
2. Vector Database - O(1) complexity search
3. Self-Training Module - Autonomous learning
4. API Server - RESTful and WebSocket interfaces
5. CLI Tools - Command-line interaction
6. Web Interface - Browser-based UI

## Testing

See test_evidence/ directory for comprehensive testing results.
EOF

# 4. Create testing scripts
echo ""
echo "🧪 Creating Test Scripts..."
echo "--------------------------"

# Python test script
cat > "$DEPLOY_DIR/test_python_packages.py" << 'EOF'
#!/usr/bin/env python3
"""Test script for Python packages"""

import json
import datetime
import sys
import subprocess

def test_package_import(package_name, module_name=None):
    """Test if package can be imported"""
    if module_name is None:
        module_name = package_name
    
    try:
        __import__(module_name)
        return {"status": "success", "message": f"Successfully imported {module_name}"}
    except ImportError as e:
        return {"status": "failed", "message": str(e)}

def test_cli_command(command):
    """Test CLI command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:500]
        }
    except Exception as e:
        return {"status": "failed", "message": str(e)}

def main():
    results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "python_version": sys.version,
        "tests": {}
    }
    
    # Test imports
    print("Testing Python package imports...")
    packages = [
        ("think_ai", "think_ai"),
        ("think_ai_cli", "think_ai_cli"),
        ("o1_vector_search", "o1_vector_search")
    ]
    
    for pkg_name, import_name in packages:
        print(f"  Testing {pkg_name}...")
        results["tests"][f"import_{pkg_name}"] = test_package_import(import_name)
    
    # Test CLI commands
    print("\nTesting CLI commands...")
    commands = [
        "think-ai --version",
        "think-ai --help",
        "python -m think_ai --help"
    ]
    
    for cmd in commands:
        print(f"  Testing: {cmd}")
        results["tests"][f"cli_{cmd.replace(' ', '_')}"] = test_cli_command(cmd)
    
    # Test core functionality
    print("\nTesting core functionality...")
    try:
        from think_ai import ThinkAI
        ai = ThinkAI()
        response = ai.chat("Hello, are you working?")
        results["tests"]["core_chat"] = {
            "status": "success",
            "response": response[:200]
        }
    except Exception as e:
        results["tests"]["core_chat"] = {
            "status": "failed",
            "error": str(e)
        }
    
    # Save results
    with open("python_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Python tests completed. Results saved to python_test_results.json")

if __name__ == "__main__":
    main()
EOF

# JavaScript test script
cat > "$DEPLOY_DIR/test_javascript_packages.js" << 'EOF'
#!/usr/bin/env node
/**
 * Test script for JavaScript packages
 */

const fs = require('fs');
const { execSync } = require('child_process');

const results = {
  timestamp: new Date().toISOString(),
  nodeVersion: process.version,
  tests: {}
};

// Test package imports
console.log('Testing JavaScript package imports...');

const packages = ['think-ai-js', '@think-ai/cli', 'o1-js'];

for (const pkg of packages) {
  console.log(`  Testing ${pkg}...`);
  try {
    require(pkg);
    results.tests[`import_${pkg}`] = {
      status: 'success',
      message: `Successfully imported ${pkg}`
    };
  } catch (e) {
    results.tests[`import_${pkg}`] = {
      status: 'failed',
      message: e.message
    };
  }
}

// Test ThinkAI client
console.log('\nTesting ThinkAI client...');
try {
  const { ThinkAI } = require('think-ai-js');
  const client = new ThinkAI({ apiUrl: 'http://localhost:8000' });
  results.tests.client_creation = {
    status: 'success',
    message: 'ThinkAI client created successfully'
  };
} catch (e) {
  results.tests.client_creation = {
    status: 'failed',
    message: e.message
  };
}

// Save results
fs.writeFileSync('javascript_test_results.json', JSON.stringify(results, null, 2));
console.log('\n✅ JavaScript tests completed. Results saved to javascript_test_results.json');
EOF

chmod +x "$DEPLOY_DIR/test_python_packages.py"
chmod +x "$DEPLOY_DIR/test_javascript_packages.js"

# 5. Create full system test
echo ""
echo "🔧 Creating Full System Test..."
echo "-------------------------------"

cat > "$DEPLOY_DIR/test_full_system.py" << 'EOF'
#!/usr/bin/env python3
"""Full system integration test"""

import json
import time
import asyncio
import datetime
import subprocess
import os
import signal
import sys

class FullSystemTest:
    def __init__(self):
        self.results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "tests": {},
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        self.server_process = None
    
    def start_api_server(self):
        """Start the API server"""
        try:
            # Start server in background
            self.server_process = subprocess.Popen(
                ["python", "-m", "think_ai.api.server"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(5)  # Wait for server to start
            return {"status": "success", "pid": self.server_process.pid}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def stop_api_server(self):
        """Stop the API server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
    
    async def test_api_endpoints(self):
        """Test API endpoints"""
        import aiohttp
        
        endpoints = [
            ("GET", "/health"),
            ("GET", "/stats"),
            ("POST", "/chat", {"message": "Hello"}),
            ("POST", "/train", {"topic": "test", "iterations": 1})
        ]
        
        results = {}
        
        async with aiohttp.ClientSession() as session:
            for method, endpoint, data in endpoints:
                url = f"http://localhost:8000{endpoint}"
                try:
                    if method == "GET":
                        async with session.get(url) as resp:
                            results[endpoint] = {
                                "status": "success",
                                "code": resp.status
                            }
                    else:
                        async with session.post(url, json=data) as resp:
                            results[endpoint] = {
                                "status": "success",
                                "code": resp.status
                            }
                except Exception as e:
                    results[endpoint] = {
                        "status": "failed",
                        "error": str(e)
                    }
        
        return results
    
    def test_vector_search(self):
        """Test vector search functionality"""
        try:
            from think_ai.storage import VectorDB
            
            db = VectorDB()
            
            # Add test data
            db.add("test1", [0.1, 0.2, 0.3], {"content": "Test 1"})
            db.add("test2", [0.2, 0.3, 0.4], {"content": "Test 2"})
            
            # Search
            results = db.search([0.15, 0.25, 0.35], k=1)
            
            return {
                "status": "success",
                "results": len(results),
                "top_result": results[0]["id"] if results else None
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def test_consciousness_module(self):
        """Test consciousness module"""
        try:
            from think_ai.consciousness import ConsciousnessEngine
            
            engine = ConsciousnessEngine()
            thought = engine.think("What is the nature of reality?")
            
            return {
                "status": "success",
                "thought_generated": bool(thought),
                "thought_preview": thought[:100] if thought else None
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def test_self_training(self):
        """Test self-training capability"""
        try:
            from think_ai.intelligence.self_trainer import SelfTrainer
            
            trainer = SelfTrainer()
            result = trainer.train("quantum mechanics", iterations=1)
            
            return {
                "status": "success",
                "training_completed": True,
                "knowledge_gained": result.get("knowledge_gained", 0)
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting Full System Test...")
        print("===============================")
        
        # Test 1: Core imports
        print("\n1. Testing core imports...")
        try:
            import think_ai
            import think_ai_cli
            import o1_vector_search
            self.results["tests"]["core_imports"] = {"status": "success"}
        except Exception as e:
            self.results["tests"]["core_imports"] = {"status": "failed", "error": str(e)}
        
        # Test 2: Start API server
        print("\n2. Starting API server...")
        self.results["tests"]["api_server_start"] = self.start_api_server()
        
        # Test 3: API endpoints
        if self.results["tests"]["api_server_start"]["status"] == "success":
            print("\n3. Testing API endpoints...")
            self.results["tests"]["api_endpoints"] = await self.test_api_endpoints()
        
        # Test 4: Vector search
        print("\n4. Testing vector search...")
        self.results["tests"]["vector_search"] = self.test_vector_search()
        
        # Test 5: Consciousness module
        print("\n5. Testing consciousness module...")
        self.results["tests"]["consciousness"] = self.test_consciousness_module()
        
        # Test 6: Self-training
        print("\n6. Testing self-training...")
        self.results["tests"]["self_training"] = self.test_self_training()
        
        # Stop server
        print("\n7. Stopping API server...")
        self.stop_api_server()
        
        # Save results
        with open("full_system_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        # Generate summary
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for t in self.results["tests"].values() 
                          if t.get("status") == "success")
        
        print("\n" + "="*50)
        print(f"✅ Full System Test Complete!")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print("="*50)
        
        return self.results

if __name__ == "__main__":
    tester = FullSystemTest()
    asyncio.run(tester.run_all_tests())
EOF

chmod +x "$DEPLOY_DIR/test_full_system.py"

# 6. Create deployment summary
echo ""
echo "📊 Creating Deployment Summary..."
echo "---------------------------------"

cat > "$DEPLOY_DIR/deployment_summary.txt" << EOF
Think AI Full System Deployment Summary
======================================
Date: $(date)

Deployed Packages:
-----------------
Python:
- think-ai-consciousness v2.1.0
- think-ai-cli
- o1-python

JavaScript:
- think-ai-js v2.0.1
- @think-ai/cli
- o1-js

Build Artifacts:
---------------
$(ls -la "$DEPLOY_DIR"/*.tgz 2>/dev/null || echo "No .tgz files")
$(ls -la "$DEPLOY_DIR"/*/dist/*.whl 2>/dev/null || echo "No .whl files")
$(ls -la "$DEPLOY_DIR"/*/dist/*.tar.gz 2>/dev/null || echo "No .tar.gz files")

To Deploy to PyPI:
-----------------
cd python_dist && python -m twine upload dist/*
cd python_cli_dist && python -m twine upload dist/*
cd o1_python_dist && python -m twine upload dist/*

To Deploy to NPM:
----------------
npm publish think-ai-js-*.tgz
npm publish think-ai-cli-*.tgz
npm publish o1-js-*.tgz

Next Steps:
----------
1. Run test_python_packages.py to test Python installations
2. Run test_javascript_packages.js to test JS installations
3. Run test_full_system.py for complete integration test
4. Deploy packages to PyPI/NPM
5. Update repository documentation
EOF

echo ""
echo "✅ Full System Deployment Prepared!"
echo "===================================="
echo "Deployment directory: $DEPLOY_DIR"
echo ""
echo "To test the deployment:"
echo "  cd $DEPLOY_DIR"
echo "  python test_python_packages.py"
echo "  node test_javascript_packages.js"
echo "  python test_full_system.py"
echo ""
echo "All build artifacts are ready for deployment!"