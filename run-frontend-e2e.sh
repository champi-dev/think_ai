#!/bin/bash

echo "🚀 Frontend E2E Test Runner for Think AI Eternal Context"
echo "======================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if node and npm are installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Installing...${NC}"
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Install puppeteer if not already installed
if [ ! -d "node_modules/puppeteer" ]; then
    echo -e "${YELLOW}📦 Installing Puppeteer...${NC}"
    npm install puppeteer
fi

# Determine test environment
ENV=${1:-local}
if [ "$ENV" = "prod" ]; then
    URL="https://thinkai.lat"
    echo -e "${YELLOW}🌐 Testing PRODUCTION: $URL${NC}"
else
    URL="http://localhost:7878"
    echo -e "${GREEN}🏠 Testing LOCAL: $URL${NC}"
    
    # Check if local server is running
    if ! curl -s http://localhost:7878/health > /dev/null; then
        echo -e "${RED}❌ Local server not running on port 7878${NC}"
        echo "Starting eternal context server..."
        ./target/release/eternal-context-server > eternal-server.log 2>&1 &
        SERVER_PID=$!
        echo "Waiting for server to start..."
        sleep 5
        
        if ! curl -s http://localhost:7878/health > /dev/null; then
            echo -e "${RED}❌ Failed to start server${NC}"
            exit 1
        fi
    fi
fi

# Create results directory
mkdir -p e2e-results

# Run the frontend tests
echo -e "\n${GREEN}🧪 Running Frontend E2E Tests...${NC}"
node e2e-frontend-test.js $ENV

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ All frontend tests passed!${NC}"
    
    # Generate HTML report with screenshots
    cat > e2e-results/frontend-report.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Frontend E2E Test Report - Think AI</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #f1f5f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #6366f1;
            text-align: center;
            margin-bottom: 40px;
        }
        .test-section {
            background: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .screenshot {
            width: 100%;
            max-width: 800px;
            margin: 20px auto;
            display: block;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .test-title {
            color: #06b6d4;
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .timestamp {
            color: #94a3b8;
            font-size: 0.9em;
        }
        .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.9em;
            font-weight: 600;
        }
        .status.pass {
            background: #10b981;
            color: white;
        }
        .status.fail {
            background: #ef4444;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Frontend E2E Test Report - Think AI Eternal Context</h1>
        <div class="timestamp">Generated: $(date)</div>
        <div class="timestamp">Environment: $ENV ($URL)</div>
EOF

    # Add screenshots to report
    for screenshot in e2e-screenshots/${ENV}-*.png; do
        if [ -f "$screenshot" ]; then
            filename=$(basename "$screenshot")
            testname=$(echo "$filename" | sed 's/^[^-]*-//' | sed 's/.png$//' | sed 's/-/ /g')
            
            echo "<div class='test-section'>" >> e2e-results/frontend-report.html
            echo "<h2 class='test-title'>$testname</h2>" >> e2e-results/frontend-report.html
            echo "<span class='status pass'>CAPTURED</span>" >> e2e-results/frontend-report.html
            echo "<img class='screenshot' src='../e2e-screenshots/$filename' alt='$testname'>" >> e2e-results/frontend-report.html
            echo "</div>" >> e2e-results/frontend-report.html
        fi
    done

    echo "</div></body></html>" >> e2e-results/frontend-report.html
    
    echo -e "${GREEN}📊 HTML report generated: e2e-results/frontend-report.html${NC}"
    echo -e "${GREEN}📸 Screenshots saved in: e2e-screenshots/${NC}"
    
    # Open report in browser if available
    if command -v xdg-open &> /dev/null; then
        xdg-open e2e-results/frontend-report.html
    elif command -v open &> /dev/null; then
        open e2e-results/frontend-report.html
    fi
else
    echo -e "\n${RED}❌ Some frontend tests failed!${NC}"
    echo -e "${YELLOW}Check screenshots in e2e-screenshots/ for details${NC}"
fi

# Cleanup if we started the server
if [ ! -z "$SERVER_PID" ]; then
    echo -e "\n${YELLOW}Stopping test server...${NC}"
    kill $SERVER_PID 2>/dev/null
fi

echo -e "\n${GREEN}Test run complete!${NC}"