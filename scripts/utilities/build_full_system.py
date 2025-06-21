#!/usr/bin/env python3
"""
Full Build System for Think AI
Generates C binaries, JS/Python packages, and Render deployment
"""

import os
import sys
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional

class ThinkAIBuilder:
    def __init__(self):
        self.root_dir = Path.cwd()
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        
        # Create directories
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        
        print("🚀 Think AI Full Build System")
        print("=" * 40)
    
    def build_c_binaries(self):
        """Compile Think AI core to C using Cython"""
        print("\n📦 Building C binaries...")
        
        # Create C extension setup
        setup_content = '''
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "think_ai_core",
        ["think_ai/*.py"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3", "-march=native", "-ffast-math"],
        extra_link_args=["-O3"]
    )
]

setup(
    name="think_ai_binary",
    ext_modules=cythonize(extensions, compiler_directives={
        'language_level': 3,
        'boundscheck': False,
        'wraparound': False,
        'cdivision': True,
        'initializedcheck': False
    }),
    zip_safe=False
)
'''
        
        setup_file = self.build_dir / "setup_c.py"
        setup_file.write_text(setup_content)
        
        # Build C extensions
        try:
            subprocess.run([
                sys.executable, str(setup_file), 
                "build_ext", "--inplace",
                f"--build-lib={self.dist_dir}/lib"
            ], check=True, cwd=self.build_dir)
            print("✅ C binaries built successfully")
        except:
            print("⚠️  Cython not available, using pure Python")
            # Fallback to bundling Python files
            self._bundle_python_fallback()
    
    def _bundle_python_fallback(self):
        """Bundle Python files if C compilation fails"""
        lib_dir = self.dist_dir / "lib"
        lib_dir.mkdir(exist_ok=True)
        
        # Copy core Think AI modules
        if (self.root_dir / "think_ai").exists():
            shutil.copytree(
                self.root_dir / "think_ai",
                lib_dir / "think_ai",
                dirs_exist_ok=True
            )
    
    def build_webapp(self):
        """Build web application with API"""
        print("\n🌐 Building webapp...")
        
        webapp_dir = self.dist_dir / "webapp"
        webapp_dir.mkdir(exist_ok=True)
        
        # Create optimized API server
        api_content = '''
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import Think AI core
try:
    from think_ai_core import ThinkAI  # C binary
except ImportError:
    from think_ai import ThinkAI  # Python fallback

app = FastAPI(title="Think AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize Think AI
think_ai = ThinkAI()

class Query(BaseModel):
    question: str
    context: Optional[str] = None

class Response(BaseModel):
    answer: str
    confidence: float
    reasoning: Optional[str] = None

@app.get("/")
async def root():
    return {"status": "Think AI API Running", "version": "2.0"}

@app.post("/think", response_model=Response)
async def think(query: Query):
    try:
        result = think_ai.process(query.question, query.context)
        return Response(
            answer=result["answer"],
            confidence=result.get("confidence", 1.0),
            reasoning=result.get("reasoning")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model": "loaded"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
'''
        
        (webapp_dir / "app.py").write_text(api_content)
        
        # Create static frontend
        frontend_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Think AI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        input { width: 70%; }
        button { background: #007AFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        #response { margin-top: 20px; padding: 15px; background: white; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Think AI</h1>
    <div class="container">
        <input id="question" placeholder="Ask me anything..." />
        <button onclick="think()">Think</button>
        <div id="response"></div>
    </div>
    <script>
        async function think() {
            const question = document.getElementById('question').value;
            const response = await fetch('/think', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question})
            });
            const data = await response.json();
            document.getElementById('response').innerHTML = 
                `<strong>Answer:</strong> ${data.answer}<br>
                 <strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%`;
        }
    </script>
</body>
</html>
'''
        
        static_dir = webapp_dir / "static"
        static_dir.mkdir(exist_ok=True)
        (static_dir / "index.html").write_text(frontend_content)
        
        print("✅ Webapp built successfully")
    
    def update_packages(self):
        """Update JS and Python packages"""
        print("\n📚 Updating packages...")
        
        # Update Python package
        py_pkg_dir = self.dist_dir / "python-package"
        py_pkg_dir.mkdir(exist_ok=True)
        
        setup_py = '''
from setuptools import setup, find_packages

setup(
    name="think-ai",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "torch>=2.0.0",
        "transformers>=4.30.0"
    ],
    python_requires=">=3.8",
    author="Think AI Team",
    description="Think AI - Advanced AI System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/think-ai/think-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
'''
        
        (py_pkg_dir / "setup.py").write_text(setup_py)
        shutil.copy(self.root_dir / "README.md", py_pkg_dir / "README.md")
        
        # Copy library files
        if (self.dist_dir / "lib" / "think_ai").exists():
            shutil.copytree(
                self.dist_dir / "lib" / "think_ai",
                py_pkg_dir / "think_ai",
                dirs_exist_ok=True
            )
        
        # Update JS package
        js_pkg_dir = self.dist_dir / "js-package"
        js_pkg_dir.mkdir(exist_ok=True)
        
        package_json = {
            "name": "@think-ai/core",
            "version": "2.0.0",
            "description": "Think AI JavaScript SDK",
            "main": "index.js",
            "types": "index.d.ts",
            "scripts": {
                "build": "tsc",
                "test": "jest"
            },
            "keywords": ["ai", "think-ai", "machine-learning"],
            "author": "Think AI Team",
            "license": "MIT",
            "dependencies": {
                "axios": "^1.4.0"
            },
            "devDependencies": {
                "@types/node": "^20.0.0",
                "typescript": "^5.0.0"
            }
        }
        
        (js_pkg_dir / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # Create JS SDK
        js_sdk = '''
class ThinkAI {
    constructor(apiUrl = '/') {
        this.apiUrl = apiUrl.replace(/\/$/, '');
    }
    
    async think(question, context = null) {
        const response = await fetch(`${this.apiUrl}/think`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({question, context})
        });
        return response.json();
    }
    
    async health() {
        const response = await fetch(`${this.apiUrl}/health`);
        return response.json();
    }
}

module.exports = ThinkAI;
'''
        
        (js_pkg_dir / "index.js").write_text(js_sdk)
        
        # TypeScript definitions
        ts_defs = '''
export interface ThinkResponse {
    answer: string;
    confidence: number;
    reasoning?: string;
}

export class ThinkAI {
    constructor(apiUrl?: string);
    think(question: string, context?: string): Promise<ThinkResponse>;
    health(): Promise<{status: string, model: string}>;
}
'''
        
        (js_pkg_dir / "index.d.ts").write_text(ts_defs)
        
        print("✅ Packages updated successfully")
    
    def create_render_config(self):
        """Create Render deployment configuration"""
        print("\n🚢 Creating Render configuration...")
        
        render_dir = self.dist_dir / "render-deploy"
        render_dir.mkdir(exist_ok=True)
        
        # Dockerfile for Render
        dockerfile = '''
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled libraries and webapp
COPY lib /app/lib
COPY webapp /app/webapp

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi uvicorn \
    numpy torch transformers \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "/app/webapp/app.py"]
'''
        
        (render_dir / "Dockerfile").write_text(dockerfile)
        
        # Copy dist contents
        shutil.copytree(self.dist_dir / "lib", render_dir / "lib", dirs_exist_ok=True)
        shutil.copytree(self.dist_dir / "webapp", render_dir / "webapp", dirs_exist_ok=True)
        
        # render.yaml
        render_yaml = '''
services:
  - type: web
    name: think-ai
    runtime: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: PYTHON_UNBUFFERED
        value: "1"
    autoDeploy: false
'''
        
        (render_dir / "render.yaml").write_text(render_yaml)
        
        print("✅ Render configuration created")
        print(f"\n📁 Deployment ready at: {render_dir}")
    
    def build_all(self):
        """Build everything"""
        start_time = time.time()
        
        self.build_c_binaries()
        self.build_webapp()
        self.update_packages()
        self.create_render_config()
        
        elapsed = time.time() - start_time
        print(f"\n✨ Build completed in {elapsed:.2f}s")
        print(f"📦 Distribution ready in: {self.dist_dir}")
        
        # List contents
        print("\n📋 Build artifacts:")
        for item in sorted(self.dist_dir.rglob("*")):
            if item.is_file():
                size = item.stat().st_size
                print(f"  {item.relative_to(self.dist_dir)} ({size:,} bytes)")


if __name__ == "__main__":
    builder = ThinkAIBuilder()
    builder.build_all()