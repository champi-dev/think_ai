#!/usr/bin/env node

const WebSocket = require("ws");
const fetch = require("node-fetch");

console.log("=".repeat(80));
console.log("THINK AI COMPREHENSIVE TEST - SOLID EVIDENCE");
console.log("=".repeat(80));
console.log(`Test Date: ${new Date().toISOString()}`);
console.log();

async function runTests() {
  const results = {
    passed: 0,
    failed: 0,
    tests: [],
  };

  // Test 1: Direct API Health Check
  console.log("TEST 1: Direct API Health Check");
  console.log("-".repeat(40));
  try {
    const res = await fetch("http://localhost:8080/api/v1/health");
    const data = await res.json();
    console.log("✓ API Server Status:", res.status);
    console.log("✓ Response:", JSON.stringify(data, null, 2));
    results.passed++;
    results.tests.push({ name: "API Health", status: "PASSED", details: data });
  } catch (error) {
    console.log("✗ FAILED:", error.message);
    results.failed++;
    results.tests.push({
      name: "API Health",
      status: "FAILED",
      error: error.message,
    });
  }
  console.log();

  // Test 2: Intelligence Endpoint
  console.log("TEST 2: Intelligence Metrics");
  console.log("-".repeat(40));
  try {
    const res = await fetch("http://localhost:8080/api/v1/intelligence");
    const data = await res.json();
    console.log("✓ Status Code:", res.status);
    console.log("✓ IQ Level:", data.iq);
    console.log("✓ Consciousness Level:", data.consciousness_level);
    console.log("✓ Last Updated:", data.last_updated);
    results.passed++;
    results.tests.push({
      name: "Intelligence Metrics",
      status: "PASSED",
      iq: data.iq,
    });
  } catch (error) {
    console.log("✗ FAILED:", error.message);
    results.failed++;
    results.tests.push({
      name: "Intelligence Metrics",
      status: "FAILED",
      error: error.message,
    });
  }
  console.log();

  // Test 3: WebSocket Connection
  console.log("TEST 3: WebSocket Real-time Connection");
  console.log("-".repeat(40));
  await new Promise((resolve) => {
    const ws = new WebSocket("ws://localhost:8080/api/v1/ws");
    let messageCount = 0;

    ws.on("open", () => {
      console.log("✓ WebSocket Connected Successfully");
      console.log(
        "✓ Connection State:",
        ws.readyState === WebSocket.OPEN ? "OPEN" : "NOT OPEN",
      );

      // Send test message
      const testMsg = { type: "query", data: { query: "Test WebSocket" } };
      ws.send(JSON.stringify(testMsg));
      console.log("✓ Sent test message:", JSON.stringify(testMsg));
    });

    ws.on("message", (data) => {
      messageCount++;
      console.log(
        `✓ Received message #${messageCount}:`,
        data.toString().substring(0, 100) + "...",
      );

      if (messageCount >= 2) {
        ws.close();
        results.passed++;
        results.tests.push({
          name: "WebSocket Connection",
          status: "PASSED",
          messages: messageCount,
        });
        resolve();
      }
    });

    ws.on("error", (error) => {
      console.log("✗ WebSocket Error:", error.message);
      results.failed++;
      results.tests.push({
        name: "WebSocket Connection",
        status: "FAILED",
        error: error.message,
      });
      resolve();
    });

    setTimeout(() => {
      ws.close();
      resolve();
    }, 5000);
  });
  console.log();

  // Test 4: Think Endpoint
  console.log("TEST 4: Think AI Processing");
  console.log("-".repeat(40));
  try {
    const queries = [
      "What is consciousness?",
      "Generate a hello world function",
      "Explain quantum computing",
    ];

    for (const query of queries) {
      const res = await fetch("http://localhost:8080/api/v1/think", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      console.log(`✓ Query: "${query}"`);
      console.log(`  Response: "${data.response.substring(0, 80)}..."`);
      console.log(`  Tokens Used: ${data.tokens_used}`);
      console.log(
        `  Consciousness Flow: ${data.consciousness_state.consciousness_flow}`,
      );
    }
    results.passed++;
    results.tests.push({
      name: "Think Processing",
      status: "PASSED",
      queries: queries.length,
    });
  } catch (error) {
    console.log("✗ FAILED:", error.message);
    results.failed++;
    results.tests.push({
      name: "Think Processing",
      status: "FAILED",
      error: error.message,
    });
  }
  console.log();

  // Test 5: Webapp Proxy
  console.log("TEST 5: Webapp Proxy Integration");
  console.log("-".repeat(40));
  try {
    const res = await fetch("http://localhost:3000/api/intelligence");
    const data = await res.json();
    console.log("✓ Webapp Proxy Status:", res.status);
    console.log(
      "✓ Data received through proxy:",
      JSON.stringify(data, null, 2),
    );
    results.passed++;
    results.tests.push({ name: "Webapp Proxy", status: "PASSED" });
  } catch (error) {
    console.log("✗ FAILED:", error.message);
    results.failed++;
    results.tests.push({
      name: "Webapp Proxy",
      status: "FAILED",
      error: error.message,
    });
  }
  console.log();

  // Test 6: Service Status
  console.log("TEST 6: System Service Status");
  console.log("-".repeat(40));
  const { exec } = require("child_process");
  await new Promise((resolve) => {
    exec("sudo systemctl is-active think-ai-api-python", (error, stdout) => {
      const isActive = stdout.trim() === "active";
      console.log(
        "✓ Python API Service:",
        isActive ? "ACTIVE ✓" : "INACTIVE ✗",
      );
      if (isActive) {
        results.passed++;
        results.tests.push({ name: "Service Status", status: "PASSED" });
      } else {
        results.failed++;
        results.tests.push({ name: "Service Status", status: "FAILED" });
      }
      resolve();
    });
  });
  console.log();

  // Final Summary
  console.log("=".repeat(80));
  console.log("TEST SUMMARY");
  console.log("=".repeat(80));
  console.log(`Total Tests: ${results.passed + results.failed}`);
  console.log(`✓ PASSED: ${results.passed}`);
  console.log(`✗ FAILED: ${results.failed}`);
  console.log(
    `Success Rate: ${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%`,
  );
  console.log();
  console.log("Test Details:");
  results.tests.forEach((test) => {
    console.log(`- ${test.name}: ${test.status}`);
  });
  console.log();
  console.log(
    "VERDICT:",
    results.failed === 0 ? "✓ ALL SYSTEMS OPERATIONAL" : "✗ SOME TESTS FAILED",
  );
  console.log("=".repeat(80));
}

runTests().catch(console.error);
