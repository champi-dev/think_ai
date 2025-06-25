import { NextApiRequest, NextApiResponse } from "next";
import { Server } from "http";
import { WebSocketServer } from "ws";

let wss: WebSocketServer | null = null;

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "GET") {
    // Upgrade HTTP connection to WebSocket
    const server = (res.socket as any).server as Server;

    if (!wss) {
      wss = new WebSocketServer({ noServer: true });

      // Handle WebSocket connections
      wss.on("connection", (ws, request) => {
        console.log("WebSocket client connected");

        // Create a connection to the backend WebSocket
        const WebSocket = require("ws");
        const backendWs = new WebSocket("ws://localhost:8080/api/v1/ws");

        // Relay messages from client to backend
        ws.on("message", (message) => {
          if (backendWs.readyState === WebSocket.OPEN) {
            backendWs.send(message);
          }
        });

        // Relay messages from backend to client
        backendWs.on("message", (message: any) => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(message);
          }
        });

        // Handle backend WebSocket errors
        backendWs.on("error", (error: Error) => {
          console.error("Backend WebSocket error:", error);
          ws.close();
        });

        // Handle backend WebSocket close
        backendWs.on("close", () => {
          ws.close();
        });

        // Handle client disconnect
        ws.on("close", () => {
          backendWs.close();
        });

        ws.on("error", (error) => {
          console.error("Client WebSocket error:", error);
          backendWs.close();
        });
      });

      // Handle upgrade requests
      server.on("upgrade", (request, socket, head) => {
        if (request.url === "/api/ws") {
          wss!.handleUpgrade(request, socket, head, (ws) => {
            wss!.emit("connection", ws, request);
          });
        }
      });
    }

    res.status(101).end();
  } else {
    res.status(405).json({ error: "Method not allowed" });
  }
}

export const config = {
  api: {
    bodyParser: false,
  },
};
