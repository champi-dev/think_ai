#!/usr/bin/env python3
"""Pre-commit QA Environment with Browser - Manual testing interface for Think AI."""

import subprocess
import time
import webbrowser
import sys
import os
import signal
import threading
from pathlib import Path
import json
import psutil

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def kill_process_on_port(port):
    """Kill any process using the specified port."""
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                try:
                    process = psutil.Process(conn.pid)
                    process.terminate()
                    time.sleep(1)
                    if process.is_running():
                        process.kill()
                    print(f"{YELLOW}Killed process on port {port}{RESET}")
                except:
                    pass
    except:
        pass


def launch_qa_environment_browser():
    """Launch full QA testing environment with browser for manual verification."""
    print(f"{BLUE}🧪 THINK AI QA ENVIRONMENT - BROWSER MODE{RESET}")
    print("=" * 60)
    print("Starting all services for manual browser testing...\n")

    processes = []

    try:
        # Kill any existing processes on our ports
        for port in [8080, 3000, 5000, 8081]:
            kill_process_on_port(port)

        # 1. Start main API server
        print(f"{BLUE}1️⃣  Starting API server on http://localhost:8080...{RESET}")
        # Set up environment with proper Python path and Railway settings
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).parent.parent)
        env["PYTHONUNBUFFERED"] = "1"
        env["THINK_AI_USE_LIGHTWEIGHT"] = "false"
        env["THINK_AI_MINIMAL_INIT"] = "false"
        env["THINK_AI_COLOMBIAN"] = "true"

        api_proc = subprocess.Popen(
            [sys.executable, "think_ai_full.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            env=env,
            preexec_fn=os.setsid if sys.platform != "win32" else None,
        )
        processes.append(api_proc)

        # Check for errors in startup
        print(f"{YELLOW}Checking API server startup...{RESET}")
        time.sleep(3)

        # Read first few lines of output to check for errors
        try:
            import select

            if api_proc.stdout and select.select([api_proc.stdout], [], [], 0)[0]:
                output = api_proc.stdout.read(1000).decode("utf-8", errors="ignore")
                if output:
                    print(f"{YELLOW}API Server Output:{RESET}")
                    print(output[:500])  # Show first 500 chars
        except:
            pass

        time.sleep(2)

        # 2. Start webapp (if exists)
        webapp_path = Path("webapp")
        if webapp_path.exists() and (webapp_path / "package.json").exists():
            print(f"{BLUE}2️⃣  Starting webapp on http://localhost:3000...{RESET}")
            webapp_proc = subprocess.Popen(
                ["npm", "start"],
                cwd="webapp",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "BROWSER": "none"},  # Prevent auto-opening browser
                preexec_fn=os.setsid if sys.platform != "win32" else None,
            )
            processes.append(webapp_proc)
            time.sleep(8)
        else:
            print(f"{YELLOW}⚠️  No webapp found, skipping...{RESET}")

        # 3. Start test API on different port
        print(f"{BLUE}3️⃣  Starting test API on http://localhost:8081...{RESET}")
        test_api_proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                """
import asyncio
from aiohttp import web
import json

async def handle_health(request):
    return web.json_response({
        'status': 'healthy',
        'service': 'think-ai-full',
        'timestamp': str(asyncio.get_event_loop().time())
    })

async def handle_test(request):
    return web.json_response({
        'message': 'Test endpoint working!',
        'data': {'test': True}
    })

app = web.Application()
app.router.add_get('/health', handle_health)
app.router.add_get('/test', handle_test)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8081)
""",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid if sys.platform != "win32" else None,
        )
        processes.append(test_api_proc)
        time.sleep(3)

        # 4. Create QA dashboard HTML
        dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - QA Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        .card h2 {
            margin-top: 0;
            color: #4CAF50;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status.loading {
            background: #FFA500;
            animation: pulse 1s infinite;
        }
        .status.online {
            background: #4CAF50;
        }
        .status.offline {
            background: #f44336;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .endpoint {
            background: #1a1a1a;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .endpoint a {
            color: #4CAF50;
            text-decoration: none;
        }
        .endpoint a:hover {
            text-decoration: underline;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #45a049;
        }
        .checklist {
            background: #333;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .checklist h3 {
            margin-top: 0;
            color: #4CAF50;
        }
        .checklist label {
            display: block;
            margin: 8px 0;
            cursor: pointer;
        }
        .checklist input[type="checkbox"] {
            margin-right: 10px;
            transform: scale(1.2);
        }
        .approve-section {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            background: #2a2a2a;
            border-radius: 10px;
        }
        .approve-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 18px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
        }
        .reject-btn {
            background: #f44336;
        }
        .result {
            margin-top: 10px;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            background: #1a1a1a;
            max-height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Think AI - QA Dashboard</h1>
        <p class="subtitle">Manual Testing Interface</p>
        
        <div class="grid">
            <div class="card">
                <h2><span class="status loading" id="api-status"></span>API Server</h2>
                <div class="endpoint">
                    <a href="http://localhost:8080/health" target="_blank">Health Check</a>
                    <button onclick="testEndpoint('http://localhost:8080/health', 'api-health-result')">Test</button>
                </div>
                <div id="api-health-result" class="result"></div>
                
                <div class="endpoint">
                    <a href="http://localhost:8080/" target="_blank">Root Endpoint</a>
                    <button onclick="testEndpoint('http://localhost:8080/', 'api-root-result')">Test</button>
                </div>
                <div id="api-root-result" class="result"></div>
                
                <div class="endpoint">
                    <a href="http://localhost:8080/api/v1/generate" target="_blank">Generate Endpoint</a>
                    <button onclick="testGenerateEndpoint('api-generate-result')">Test</button>
                </div>
                <div id="api-generate-result" class="result"></div>
            </div>
            
            <div class="card">
                <h2><span class="status loading" id="webapp-status"></span>Web Application</h2>
                <div class="endpoint">
                    <a href="http://localhost:3000" target="_blank">Open Webapp</a>
                    <button onclick="testEndpoint('http://localhost:3000', 'webapp-result')">Test</button>
                </div>
                <div id="webapp-result" class="result"></div>
            </div>
            
            <div class="card">
                <h2><span class="status loading" id="test-status"></span>Test API</h2>
                <div class="endpoint">
                    <a href="http://localhost:8081/health" target="_blank">Health Check</a>
                    <button onclick="testEndpoint('http://localhost:8081/health', 'test-health-result')">Test</button>
                </div>
                <div id="test-health-result" class="result"></div>
                
                <div class="endpoint">
                    <a href="http://localhost:8081/test" target="_blank">Test Endpoint</a>
                    <button onclick="testEndpoint('http://localhost:8081/test', 'test-endpoint-result')">Test</button>
                </div>
                <div id="test-endpoint-result" class="result"></div>
            </div>
        </div>
        
        <div class="checklist">
            <h3>✅ QA Checklist</h3>
            <label><input type="checkbox" id="check1"> API server responds to health checks</label>
            <label><input type="checkbox" id="check2"> Generate endpoint returns valid results</label>
            <label><input type="checkbox" id="check3"> Web interface loads without errors</label>
            <label><input type="checkbox" id="check4"> All critical endpoints are accessible</label>
            <label><input type="checkbox" id="check5"> No console errors in browser</label>
            <label><input type="checkbox" id="check6"> Response times are acceptable (< 1s)</label>
            <label><input type="checkbox" id="check7"> Error handling works correctly</label>
            <label><input type="checkbox" id="check8"> UI is responsive and functional</label>
            <label><input type="checkbox" id="check9"> Data persistence works correctly</label>
            <label><input type="checkbox" id="check10"> All tests pass successfully</label>
        </div>
        
        <div class="approve-section">
            <h3>QA Decision</h3>
            <p>Once you've completed manual testing, make your decision:</p>
            <button class="approve-btn" onclick="approveQA()">✅ APPROVE - Ready to Commit</button>
            <button class="approve-btn reject-btn" onclick="rejectQA()">❌ REJECT - Issues Found</button>
        </div>
    </div>
    
    <script>
        // Check service status
        async function checkStatus(url, statusId) {
            try {
                const response = await fetch(url, { method: 'HEAD' });
                document.getElementById(statusId).className = 'status online';
            } catch (e) {
                document.getElementById(statusId).className = 'status offline';
            }
        }
        
        // Test endpoint
        async function testEndpoint(url, resultId) {
            const resultDiv = document.getElementById(resultId);
            resultDiv.textContent = 'Testing...';
            
            try {
                const start = Date.now();
                const response = await fetch(url);
                const time = Date.now() - start;
                const data = await response.text();
                
                let displayData = data;
                try {
                    const json = JSON.parse(data);
                    displayData = JSON.stringify(json, null, 2);
                } catch (e) {}
                
                resultDiv.innerHTML = `<strong>Status:</strong> ${response.status} ${response.statusText}<br>
                                      <strong>Time:</strong> ${time}ms<br>
                                      <strong>Response:</strong><pre>${displayData}</pre>`;
            } catch (e) {
                resultDiv.innerHTML = `<strong style="color: #f44336;">Error:</strong> ${e.message}`;
            }
        }
        
        // Test generate endpoint with POST
        async function testGenerateEndpoint(resultId) {
            const resultDiv = document.getElementById(resultId);
            resultDiv.textContent = 'Testing...';
            
            try {
                const start = Date.now();
                const response = await fetch('http://localhost:8080/api/v1/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        prompt: 'Hello, test the Think AI system',
                        max_length: 200,
                        temperature: 0.7,
                        colombian_mode: true
                    })
                });
                const time = Date.now() - start;
                const data = await response.text();
                
                let displayData = data;
                try {
                    const json = JSON.parse(data);
                    displayData = JSON.stringify(json, null, 2);
                } catch (e) {}
                
                resultDiv.innerHTML = `<strong>Status:</strong> ${response.status} ${response.statusText}<br>
                                      <strong>Time:</strong> ${time}ms<br>
                                      <strong>Response:</strong><pre>${displayData}</pre>`;
            } catch (e) {
                resultDiv.innerHTML = `<strong style="color: #f44336;">Error:</strong> ${e.message}`;
            }
        }
        
        // QA decisions
        function approveQA() {
            fetch('http://localhost:8082/approve', { method: 'POST' })
                .then(() => window.close())
                .catch(() => alert('Decision sent. You can close this window.'));
        }
        
        function rejectQA() {
            fetch('http://localhost:8082/reject', { method: 'POST' })
                .then(() => window.close())
                .catch(() => alert('Decision sent. You can close this window.'));
        }
        
        // Auto-check status every 2 seconds
        setInterval(() => {
            checkStatus('http://localhost:8080/health', 'api-status');
            checkStatus('http://localhost:3000', 'webapp-status');
            checkStatus('http://localhost:8081/health', 'test-status');
        }, 2000);
        
        // Initial check
        checkStatus('http://localhost:8080/health', 'api-status');
        checkStatus('http://localhost:3000', 'webapp-status');
        checkStatus('http://localhost:8081/health', 'test-status');
    </script>
</body>
</html>
        """

        dashboard_path = Path("/tmp/think_ai_qa_dashboard.html")
        dashboard_path.write_text(dashboard_html)

        # 5. Start decision server
        print(f"{BLUE}4️⃣  Starting QA decision server...{RESET}")
        decision_result = {"approved": None}

        def run_decision_server():
            from http.server import HTTPServer, BaseHTTPRequestHandler

            class DecisionHandler(BaseHTTPRequestHandler):
                def do_POST(self):
                    if self.path == "/approve":
                        decision_result["approved"] = True
                    elif self.path == "/reject":
                        decision_result["approved"] = False

                    self.send_response(200)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b"OK")

                def log_message(self, format, *args):
                    pass  # Suppress logs

            server = HTTPServer(("localhost", 8082), DecisionHandler)
            while decision_result["approved"] is None:
                server.handle_request()

        decision_thread = threading.Thread(target=run_decision_server)
        decision_thread.daemon = True
        decision_thread.start()

        # 6. Open browser
        print(f"\n{GREEN}✅ All services started!{RESET}")
        print(f"\n{BLUE}Opening QA Dashboard in your browser...{RESET}")
        time.sleep(2)

        # Open the dashboard
        webbrowser.open(f"file://{dashboard_path}")

        print(f"\n{YELLOW}📋 Manual Testing Checklist:{RESET}")
        print("   1. ✓ Check API health endpoint")
        print("   2. ✓ Test query functionality")
        print("   3. ✓ Verify web interface loads")
        print("   4. ✓ Test all critical features")
        print("   5. ✓ Check browser console for errors")
        print("   6. ✓ Verify response times")
        print("   7. ✓ Test error handling")
        print("   8. ✓ Check UI responsiveness")
        print("   9. ✓ Verify data persistence")
        print("  10. ✓ Ensure all tests pass")

        print(f"\n{YELLOW}⏳ Waiting for your QA decision...{RESET}")
        print("   Click APPROVE or REJECT in the browser when done.\n")

        # Wait for decision
        while decision_result["approved"] is None:
            time.sleep(0.5)

        # Show result
        if decision_result["approved"]:
            print(f"\n{GREEN}✅ QA APPROVED! Proceeding with commit...{RESET}")
            return True
        else:
            print(f"\n{RED}❌ QA REJECTED! Please fix issues before committing.{RESET}")
            return False

    except Exception as e:
        print(f"\n{RED}❌ Error launching QA environment: {e}{RESET}")
        return False

    finally:
        # Cleanup
        print(f"\n{BLUE}Shutting down services...{RESET}")
        for proc in processes:
            try:
                if sys.platform != "win32":
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
            except:
                pass

        # Give processes time to shut down
        time.sleep(2)


if __name__ == "__main__":
    if launch_qa_environment_browser():
        sys.exit(0)
    else:
        sys.exit(1)
