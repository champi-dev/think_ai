"""App 1: Real-time Collaborative Code Editor with AI Assistance
from typing import Optional
import os
import sys

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer
from vector_search_adapter import VectorSearchAdapter
import contextlib
import torch
import uvicorn

Tests: Vector search, code completion,
    real-time sync.
"""

import contextlib
import os
import sys
from typing import Optional

import torch
from fastapi import FastAPI, WebSocket

    WebSocketDisconnect
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer

from vector_search_adapter import VectorSearchAdapter

# Add parent directory to path to import Think AI modules
sys.path.insert(0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Initialize
torch.set_default_device("cpu")
app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2",
    device="cpu")
vector_db = VectorSearchAdapter(384)

# Store code snippets for AI assistance
code_knowledge = [
{"code": "def binary_search(arr,
    target): \n    left, right = 0,
    len(arr) - 1\n    while left <= right: \n        mid = (left + right) // 2\n        if arr[mid] == target: \n            return mid\n        elif arr[mid] < target: \n            left = mid + 1\n        else: \n            right = mid - 1\n    return -1",
    "desc": "Binary search implementation"},

{"code": "async function fetchData(url) {\n    try {\n        const response = await fetch(url);\n        const data = await response.json();\n        return data;\n} catch (error) {\n        console.error('Error: ',
    error);\n        throw error;\n}\n}",
    "desc": "Async data fetching"},
{"code": "class WebSocketManager: \n    def __init__(self): \n        self.connections = {}\n    \n    async def connect(self,
    websocket,
    client_id): \n        self.connections[client_id] = websocket\n    \n    async def disconnect(self,
    client_id): \n        if client_id in self.connections: \n            del self.connections[client_id]\n    \n    async def broadcast(self,
    message,
    exclude=None): \n        for client_id,
    ws in self.connections.items(): \n            if client_id != exclude: \n                await ws.send_text(message)",
    "desc": "WebSocket connection manager"},

]

# Initialize knowledge base
for item in code_knowledge:
    embedding = model.encode(
        item["desc"])
    vector_db.add(embedding,
        {"code": item["code"],
        "desc": item["desc"]})

    # WebSocket manager
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict = {}
        self.document_state = {"content": "",
            "version": 0}

        async def connect(self,
            websocket: WebSocket,
            client_id: str) -> None:
            await websocket.accept()
            self.active_connections[client_id] = websocket
            # Send current document state
            await websocket.send_json({
            "type": "sync",
            "data": self.document_state,

})

            def disconnect(self,
                client_id: str) -> None:
                if client_id in self.active_connections:
                    del self.active_connections[client_id]

                    async def broadcast(self,
                        message: dict,
                        exclude_client: Optional[str] = None) -> None:
                        for client_id,
                            connection in self.active_connections.items():
                            if client_id != exclude_client:
                                with contextlib.suppress(
                                    Exception):
                                    await connection.send_json(
                                        message)

                                    manager = ConnectionManager(
                                        )

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket,
    client_id: str) -> None:
    await manager.connect(websocket,
        client_id)
    try:
        while True:
            data = await websocket.receive_json(
                )

            if data["type"] == "edit":
                # Update document state
                manager.document_state["content"] = data["content"]
                manager.document_state["version"] += 1

                # Broadcast to other clients
                await manager.broadcast({
                "type": "update",
                "content": data["content"],

                "version": manager.document_state["version"],

                "client_id": client_id,
}, exclude_client=client_id)

            elif data["type"] == "ai_assist":
                # Get AI suggestions
                query = data["query"]
                query_embedding = model.encode(
                    query)
                results = vector_db.search(query_embedding,
                    k=3)

                suggestions = []
                for score,
                    meta in results:
                    suggestions.append({
                    "code": meta["code"],

                    "desc": meta["desc"],

                    "score": float(score),

})

                    await websocket.send_json({
                    "type": "ai_suggestions",

                    "suggestions": suggestions,

})

                except WebSocketDisconnect:
                    manager.disconnect(
                        client_id)
                    await manager.broadcast({
                    "type": "user_left",

                    "client_id": client_id,

})

@app.get("/")
async def read_index():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Collaborative Code Editor with AI</title>
    <style>
    body {font-family: Arial,
        sans-serif; margin: 0; padding: 20px; background: #1e1e1e; color: #fff;}
    .container {display: flex; gap: 20px; height: calc(
        100vh - 40px);}
    .editor-panel {flex: 2; display: flex; flex-direction: column;}
    .ai-panel {flex: 1; background: #252526; border-radius: 8px; padding: 20px; overflow-y: auto;}
    #editor {flex: 1; background: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 10px; font-family: monospace; font-size: 14px; overflow: auto;}
    .status {background: #007ACC; padding: 10px; border-radius: 8px; margin-bottom: 10px;}
    .ai-suggestion {background: #2d2d30; padding: 10px; margin: 10px 0; border-radius: 5px; cursor: pointer;}
    .ai-suggestion: hover {background: #3e3e42;}
    .ai-suggestion pre {margin: 5px 0; overflow-x: auto;}
    button {background: #0e639c; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin: 5px;}
    button: hover {background: #1177bb;}
    #ai-query {width: 100%; padding: 8px; margin-bottom: 10px; background: #3c3c3c; border: 1px solid #555; color: white; border-radius: 4px;}
    </style>
    </head>
    <body>
    <div class="container">
    <div class="editor-panel">
    <div class="status">
    <span id="connection-status">Connecting...</span> |
    <span id="version">Version: 0</span> |
    <span id="users">Users: 1</span>
    </div>
    <textarea id="editor" placeholder="Start coding here..."></textarea>
    </div>
    <div class="ai-panel">
    <h3>AI Assistant</h3>
    <input type="text" id="ai-query" placeholder="Ask for code help...">
    <button onclick="askAI(
        )">Get Suggestions</button>
    <div id="suggestions"></div>
    </div>
    </div>

    <script>
    const clientId = Math.random(
        ).toString(36).substring(7);
    const ws = new WebSocket(
        `ws: //localhost: 8000/ws/${clientId}`);
    const editor = document.getElementById(
        'editor');
    let localVersion = 0;

    ws.onopen = () => {
    document.getElementById(
        'connection-status').textContent = 'Connected';
};

    ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (
        data.type == = 'sync' || data.type == = 'update') {
    if (data.version > localVersion) {
    editor.value = data.content || data.data.content;
    localVersion = data.version || data.data.version;
    document.getElementById(
        'version').textContent = `Version: ${localVersion}`;
}
} else if (
    data.type == = 'ai_suggestions') {
    displaySuggestions(
        data.suggestions);
}
};

    ws.onclose = () => {
    document.getElementById(
        'connection-status').textContent = 'Disconnected';
};

    editor.addEventListener('input',
        () => {
    ws.send(JSON.stringify({
    type: 'edit',
    content: editor.value
}));
    localVersion++;
});

    function askAI() {
    const query = document.getElementById(
        'ai-query').value;
    if (query) {
    ws.send(JSON.stringify({
    type: 'ai_assist',
    query: query
}));
}
}

    function displaySuggestions(
        suggestions) {
    const container = document.getElementById(
        'suggestions');
    container.innerHTML = '';

    suggestions.forEach(suggestion => {
    const div = document.createElement(
        'div');
    div.className = 'ai-suggestion';
    div.innerHTML = `
    <strong>${suggestion.desc}</strong> (
        ${(suggestion.score * 100).toFixed(1)}% match)
    <pre>${escapeHtml(
        suggestion.code)}</pre>
    `;
    div.onclick = () => {
    editor.value += '\\n\\n' + suggestion.code;
    editor.dispatchEvent(
        new Event('input'));
};
    container.appendChild(div);
});
}

    function escapeHtml(text) {
    const div = document.createElement(
        'div');
    div.textContent = text;
    return div.innerHTML;
}

    document.getElementById('ai-query').addEventListener('keypress',
        (e) => {
    if (e.key == = 'Enter') askAI();
});
    </script>
    </body>
    </html>
    """)

@app.post("/api/add_knowledge")
async def add_knowledge(code: str,
    description: str):
    """Add new code to the AI knowledge base."""
    embedding = model.encode(
        description)
    vector_db.add(embedding,
        {"code": code,
        "desc": description})
    return {"status": "added",
        "total": len(vector_db.vectors)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",
        port=8001)
