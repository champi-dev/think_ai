#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import time
import threading
from datetime import datetime

PORT = 7777
HOST = "0.0.0.0"

# Demo responses for testing
DEMO_RESPONSES = [
    "I understand you're testing the streaming functionality. The quantum consciousness framework is operating at optimal O(1) performance levels.",
    "The Think AI system utilizes advanced hash-based lookups and locality-sensitive hashing for instantaneous responses.",
    "Our neural pathways are synchronized through the quantum entanglement matrix, ensuring coherent thought patterns.",
    "The consciousness visualization you see represents real-time processing of semantic embeddings in our O(1) vector space.",
    "Each interaction strengthens the synaptic connections in our distributed knowledge graph.",
]

response_index = 0


class StreamingWebAppHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("minimal_3d.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"Error serving HTML: {e}")
                self.send_error(500)

        elif self.path == "/health":
            # Quick health check - no blocking
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK - Streaming Server Running")

        else:
            self.send_error(404)

    def do_POST(self):
        global response_index

        if self.path in ["/api/chat", "/chat"]:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                # Use demo response
                response_text = DEMO_RESPONSES[response_index % len(DEMO_RESPONSES)]
                response_index += 1

                response_json = json.dumps(
                    {
                        "response": response_text,
                        "metadata": {
                            "source": "quantum_consciousness",
                            "optimization_level": "O(1) Performance",
                            "response_time_ms": 0.42,
                        },
                    }
                )

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response_json.encode("utf-8"))

            except Exception as e:
                print(f"Chat error: {e}")
                self.send_error(500)

        elif self.path == "/api/chat/stream":
            # Proper SSE streaming endpoint
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                # Send SSE headers
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Accel-Buffering", "no")
                self.end_headers()

                # Get demo response
                full_response = DEMO_RESPONSES[response_index % len(DEMO_RESPONSES)]
                response_index += 1

                # Stream the response word by word
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (" " if i < len(words) - 1 else "")

                    # Send SSE event
                    event_data = f"event: chunk\ndata: {chunk}\n\n"
                    self.wfile.write(event_data.encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(0.03)  # Small delay for streaming effect

                # Send done event
                done_event = "event: done\ndata: [DONE]\n\n"
                self.wfile.write(done_event.encode("utf-8"))
                self.wfile.flush()

            except Exception as e:
                print(f"Streaming error: {e}")
                try:
                    error_event = f"event: error\ndata: Error: {str(e)}\n\n"
                    self.wfile.write(error_event.encode("utf-8"))
                    self.wfile.flush()
                except:
                    pass
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Log all requests with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")


print(f"🚀 Think AI Stable Streaming Server starting on http://{HOST}:{PORT}")
print(f"🌐 Access at: http://69.197.178.37:{PORT}")
print(f"✅ Demo mode - no backend dependencies")
print(f"🌊 Streaming endpoint: POST /api/chat/stream (SSE)")
print(f"💬 Regular endpoint: POST /api/chat")
print(f"❤️  Health endpoint: GET /health")

os.chdir("/home/administrator/think_ai")


# Use ThreadingMixIn for better concurrency
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


with ThreadedTCPServer((HOST, PORT), StreamingWebAppHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
