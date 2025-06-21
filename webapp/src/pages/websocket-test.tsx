import { useEffect, useState } from 'react';

export default function WebSocketTest() {
  const [wsStatus, setWsStatus] = useState('Disconnected');
  const [messages, setMessages] = useState<string[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const connectWebSocket = () => {
    if (typeof window === 'undefined') return;

    console.log('Connecting to WebSocket...');
    setMessages((prev) => [
      ...prev,
      `[${new Date().toISOString()}] Connecting...`,
    ]);

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;

    const websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('WebSocket connected!');
      setWsStatus('Connected');
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] ✅ Connected to ${wsUrl}`,
      ]);

      // Send a test message
      const testMsg = JSON.stringify({
        type: 'test',
        message: 'Hello from browser!',
        timestamp: Date.now(),
      });
      websocket.send(testMsg);
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] → Sent: ${testMsg}`,
      ]);
    };

    websocket.onmessage = (event) => {
      console.log('Received:', event.data);
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] ← Received: ${event.data}`,
      ]);
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsStatus('Error');
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] ❌ Error occurred`,
      ]);
    };

    websocket.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      setWsStatus('Disconnected');
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] Disconnected (code: ${event.code})`,
      ]);
    };

    setWs(websocket);
  };

  const disconnect = () => {
    if (ws) {
      ws.close();
      setWs(null);
    }
  };

  const sendMessage = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      const msg = JSON.stringify({ type: 'ping', timestamp: Date.now() });
      ws.send(msg);
      setMessages((prev) => [
        ...prev,
        `[${new Date().toISOString()}] → Sent: ${msg}`,
      ]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-8">WebSocket Test Page</h1>

      <div className="mb-8">
        <p className="text-xl mb-4">
          Status:{' '}
          <span
            className={
              wsStatus === 'Connected'
                ? 'text-green-500'
                : wsStatus === 'Error'
                  ? 'text-red-500'
                  : 'text-yellow-500'
            }
          >
            {wsStatus}
          </span>
        </p>

        <div className="space-x-4">
          <button
            onClick={connectWebSocket}
            disabled={wsStatus === 'Connected'}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded"
          >
            Connect
          </button>

          <button
            onClick={disconnect}
            disabled={wsStatus !== 'Connected'}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 rounded"
          >
            Disconnect
          </button>

          <button
            onClick={sendMessage}
            disabled={wsStatus !== 'Connected'}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded"
          >
            Send Ping
          </button>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4">Message Log:</h2>
        <div className="bg-black p-4 rounded-lg h-96 overflow-y-auto font-mono text-sm">
          {messages.length === 0 ? (
            <p className="text-gray-500">No messages yet...</p>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className="mb-1">
                {msg}
              </div>
            ))
          )}
        </div>
      </div>

      <div className="mt-8 text-gray-400">
        <p>
          This page tests the WebSocket connection at: ws://
          {typeof window !== 'undefined' ? window.location.host : 'localhost'}
          /ws
        </p>
        <p>
          The WebSocket proxy forwards messages to:
          ws://localhost:8080/api/v1/ws
        </p>
      </div>
    </div>
  );
}
