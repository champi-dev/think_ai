"""App 2: API Documentation Generator with Semantic Search
import ast
import os
import sys

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer
from vector_search_adapter import VectorSearchAdapter
import torch
import uvicorn

Tests: Code analysis, semantic search,
documentation generation.
"""

import ast
import os
import sys

import torch
from fastapi import FastAPI,
HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer

from vector_search_adapter import VectorSearchAdapter

sys.path.insert(0,
os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

torch.set_default_device("cpu")
app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2",
device="cpu")
vector_db = VectorSearchAdapter(384)

# Store API documentation
api_docs = {}


def extract_python_api(code: str):
"""Extract API information from Python code."""
    tree = ast.parse(code)
    apis = []

    for node in ast.walk(tree):
        if isinstance(node,
        ast.FunctionDef):
            api = {
            "name": node.name,
            "type": "function",
            "args": [arg.arg for arg in node.args.args],

            "docstring": ast.get_docstring(node) or
            "No documentation",
            "decorators": [d.id if hasattr(d,
            "id") else str(d) for d in node.decorator_list],

            }
            apis.append(api)
        elif isinstance(node,
        ast.ClassDef):
            api = {
            "name": node.name,
            "type": "class",
            "methods": [],
            "docstring": ast.get_docstring(node) or
            "No documentation",
            }
            for item in node.body:
                if isinstance(item,
                ast.FunctionDef):
                    api["methods"].append({
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],

                    "docstring": ast.get_docstring(item) or
                    "No documentation",
                    })
                    apis.append(api)

                    return apis


                @app.post("/api/analyze")
                async def analyze_code(
                file: UploadFile):
"""Analyze code file and
                    extract API documentation."""
                    content = await file.read()
                    code = content.decode("utf-8")

                    try:
                        apis = extract_python_api(code)

# Add to vector database for semantic search
                        for api in apis:
                            doc_text = f"{api['name']} - {api['type']}: {api['docstring']}"
                            embedding = model.encode(
                            doc_text)
                            vector_db.add(embedding,
                            api)

# Store in docs
                            api_id = f"{api['type']}_{api['name']}"
                            api_docs[api_id] = api

                            return {
                        "status": "success",
                        "apis_found": len(apis),
                        "apis": apis,
                        }
                        except Exception as e:
                            raise HTTPException(status_code=400,
                        detail=str(e))


                        @app.get("/api/search")
                        async def search_docs(query: str):
"""Semantic search through API documentation."""
                            query_embedding = model.encode(
                            query)
                            results = vector_db.search(query_embedding,
                            k=5)

                            return {
                        "query": query,
                        "results": [
                        {
                        "api": meta,
                        "score": float(score),
                        }
                        for score, meta in results
                        ],
                        }


                        @app.get("/api/generate_docs")
                        async def generate_documentation():
"""Generate markdown documentation for all APIs."""
                            markdown = "# API Documentation\n\n"

# Group by type
                            functions = [api for api in api_docs.values(
                            ) if api["type"] == "function"]
                            classes = [api for api in api_docs.values(
                            ) if api["type"] == "class"]

                            if functions:
                                markdown += "## Functions\n\n"
                                for func in functions:
                                    markdown += f"### `{func['name']}({',
                                    '.join(func['args'])})`\n\n"
                                    markdown += f"{func['docstring']}\n\n"
                                    if func.get("decorators"):
                                        markdown += f"**Decorators: ** {',
                                        '.join(func['decorators'])}\n\n"

                                        if classes:
                                            markdown += "## Classes\n\n"
                                            for cls in classes:
                                                markdown += f"### class `{cls['name']}`\n\n"
                                                markdown += f"{cls['docstring']}\n\n"

                                                if cls.get(
                                                "methods"):
                                                    markdown += "#### Methods: \n\n"
                                                    for method in cls["methods"]:
                                                        markdown += f"- **`{method['name']}({',
                                                        '.join(method['args'])})`**: {method['docstring']}\n"
                                                        markdown += "\n"

                                                        return {"markdown": markdown}

                                                    @app.get("/")
                                                    async def read_index():
                                                        return HTMLResponse("""
                                                    <!DOCTYPE html>
                                                    <html>
                                                    <head>
                                                    <title>API Documentation Generator</title>
                                                    <style>
                                                    body {font-family: -apple-system,
                                                    sans-serif; margin: 0; padding: 20px; background: #f5f5f5;}
                                                    .container {max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 2fr; gap: 20px;}
                                                    .upload-panel {background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,
                                                    0, 0, 0.1);}
                                                    .docs-panel {background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,
                                                    0, 0, 0.1);}
                                                    h1, h2, h3 {color: #333;}
                                                    button {background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px 0;}
                                                    button: hover {background: #0056b3;}
                                                    input[type="file"] {margin: 10px 0;}
                                                    input[type="text"] {width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;}
                                                    .api-item {background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff;}
                                                    .method {margin-left: 20px; padding: 10px; background: #e9ecef; border-radius: 3px; margin-top: 5px;}
                                                    pre {background: #282c34; color: #abb2bf; padding: 15px; border-radius: 5px; overflow-x: auto;}
                                                    .search-result {background: #e8f4f8; padding: 10px; margin: 5px 0; border-radius: 5px; cursor: pointer;}
                                                    .search-result: hover {background: #d1e7f0;}
                                                    .score {float: right; color: #28a745; font-weight: bold;}
                                                    </style>
                                                    </head>
                                                    <body>
                                                    <h1>🔍 API Documentation Generator</h1>

                                                    <div class="container">
                                                    <div class="upload-panel">
                                                    <h2>Upload Code</h2>
                                                    <input type="file" id="fileInput" accept=".py,
                                                    .js, .ts">
                                                    <button onclick="analyzeFile(
                                                    )">Analyze Code</button>

                                                    <h3>Search Documentation</h3>
                                                    <input type="text" id="searchInput" placeholder="Search for APIs...">
                                                    <button onclick="searchDocs(
                                                    )">Search</button>
                                                    <div id="searchResults"></div>

                                                    <h3>Actions</h3>
                                                    <button onclick="generateDocs(
                                                    )">Generate Markdown</button>
                                                    <button onclick="clearAll(
                                                    )">Clear All</button>
                                                    </div>

                                                    <div class="docs-panel">
                                                    <h2>Documentation</h2>
                                                    <div id="documentation"></div>
                                                    <pre id="markdown" style="display: none;"></pre>
                                                    </div>
                                                    </div>

                                                    <script>
                                                    async function analyzeFile() {
                                                    const fileInput = document.getElementById(
                                                    'fileInput');
                                                    const file = fileInput.files[0];
                                                    if (!file) return;

                                                    const formData = new FormData();
                                                    formData.append('file', file);

                                                    const response = await fetch('/api/analyze',
                                                    {
                                                    method: 'POST',
                                                    body: formData
                                                    });

                                                    const result = await response.json(
                                                    );
                                                    if (result.status == = 'success') {
                                                    displayAPIs(result.apis);
                                                    }
                                                    }

                                                    function displayAPIs(apis) {
                                                    const container = document.getElementById(
                                                    'documentation');
                                                    container.innerHTML = '';

                                                    apis.forEach(api => {
                                                    const div = document.createElement(
                                                    'div');
                                                    div.className = 'api-item';

                                                    if (api.type == = 'function') {
                                                    div.innerHTML = `
                                                    <h3>Function: ${api.name}(${api.args.join(',
                                                    ')})</h3>
                                                    <p>${api.docstring}</p>
                                                    ${api.decorators && api.decorators.length ? `<p><strong>Decorators: </strong> @${api.decorators.join(',
                                                    @')}</p>`: ''}
                                                    `;
                                                    } else if (api.type == = 'class') {
                                                    let html = `
                                                    <h3>Class: ${api.name}</h3>
                                                    <p>${api.docstring}</p>
                                                    `;

                                                    if (
                                                    api.methods && api.methods.length) {
                                                    html += '<h4>Methods: </h4>';
                                                    api.methods.forEach(method => {
                                                    html += `
                                                    <div class="method">
                                                    <strong>${method.name}(${method.args.join(',
                                                    ')})</strong>
                                                    <p>${method.docstring}</p>
                                                    </div>
                                                    `;
                                                    });
                                                    }

                                                    div.innerHTML = html;
                                                    }

                                                    container.appendChild(div);
                                                    });
                                                    }

                                                    async function searchDocs() {
                                                    const query = document.getElementById(
                                                    'searchInput').value;
                                                    if (!query) return;

                                                    const response = await fetch(
                                                    `/api/search?query=${encodeURIComponent(query)}`);
                                                    const result = await response.json(
                                                    );

                                                    const container = document.getElementById(
                                                    'searchResults');
                                                    container.innerHTML = '';

                                                    result.results.forEach(item => {
                                                    const div = document.createElement(
                                                    'div');
                                                    div.className = 'search-result';
                                                    div.innerHTML = `
                                                    <strong>${item.api.name}</strong> (
                                                    ${item.api.type})
                                                    <span class="score">${(
                                                    item.score * 100).toFixed(1)}%</span>
                                                    <br><small>${item.api.docstring.substring(0,
                                                    100)}...</small>
                                                    `;
                                                    div.onclick = () => {
                                                    document.getElementById(
                                                    'documentation').scrollIntoView();
                                                    };
                                                    container.appendChild(div);
                                                    });
                                                    }

                                                    async function generateDocs() {
                                                    const response = await fetch(
                                                    '/api/generate_docs');
                                                    const result = await response.json(
                                                    );

                                                    const pre = document.getElementById(
                                                    'markdown');
                                                    pre.textContent = result.markdown;
                                                    pre.style.display = 'block';
                                                    }

                                                    function clearAll() {
                                                    document.getElementById(
                                                    'documentation').innerHTML = '';
                                                    document.getElementById(
                                                    'searchResults').innerHTML = '';
                                                    document.getElementById(
                                                    'markdown').style.display = 'none';
                                                    }

                                                    document.getElementById('searchInput').addEventListener('keypress',
                                                    (e) => {
                                                    if (
                                                    e.key == = 'Enter') searchDocs();
                                                    });
                                                    </script>
                                                    </body>
                                                    </html>
""")

                                                    if __name__ == "__main__":
import uvicorn
                                                        uvicorn.run(app, host="0.0.0.0",
                                                        port=8002)
