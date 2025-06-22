package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
)

type HealthResponse struct {
    Status string `json:"status"`
    Mode   string `json:"mode"`
}

type ChatRequest struct {
    Message string `json:"message"`
}

type ChatResponse struct {
    Response string `json:"response"`
    Mode     string `json:"mode"`
    Note     string `json:"note"`
}

const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <title>Think AI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        .chat-box { border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 20px 0; min-height: 300px; background: #fafafa; }
        .input-group { display: flex; gap: 10px; }
        input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .ai { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Think AI - Ultra Fast Mode</h1>
        <div id="chat-box" class="chat-box">
            <div class="message ai">Welcome to Think AI! Running from a 5MB binary!</div>
        </div>
        <div class="input-group">
            <input type="text" id="message-input" placeholder="Type your message..." onkeypress="if(event.key==='Enter')sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    <script>
        async function sendMessage() {
            const input = document.getElementById('message-input');
            const chatBox = document.getElementById('chat-box');
            const message = input.value.trim();
            if (!message) return;
            
            chatBox.innerHTML += '<div class="message user">' + message + '</div>';
            input.value = '';
            
            try {
                const response = await fetch('/api/v1/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                chatBox.innerHTML += '<div class="message ai">' + data.response + '</div>';
            } catch (error) {
                chatBox.innerHTML += '<div class="message ai">Error: ' + error.message + '</div>';
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>`

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    http.HandleFunc("/", handleRoot)
    http.HandleFunc("/health", handleHealth)
    http.HandleFunc("/api/v1/chat", handleChat)

    fmt.Printf("🚀 Think AI Go server starting on port %s\n", port)
    log.Fatal(http.ListenAndServe(":"+port, nil))
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html")
    w.Write([]byte(htmlContent))
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(HealthResponse{
        Status: "healthy",
        Mode:   "go-binary",
    })
}

func handleChat(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req ChatRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(ChatResponse{
        Response: fmt.Sprintf("Echo: %s", req.Message),
        Mode:     "go-binary",
        Note:     "Running from a tiny static binary!",
    })
}