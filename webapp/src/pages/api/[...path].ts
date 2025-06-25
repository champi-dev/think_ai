import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  const { path } = req.query;
  const apiPath = Array.isArray(path) ? path.join("/") : path;

  // Use environment variable with fallback to localhost
  const apiUrl =
    process.env.API_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8080";
  const targetUrl = `${apiUrl}/api/v1/${apiPath}`;

  console.log(`Proxying ${req.method} request to: ${targetUrl}`);

  try {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    // Forward relevant headers but remove host-specific ones
    const forwardHeaders = ["authorization", "x-api-key"];
    forwardHeaders.forEach((header) => {
      if (req.headers[header]) {
        headers[header] = req.headers[header] as string;
      }
    });

    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body:
        req.method !== "GET" && req.method !== "HEAD"
          ? JSON.stringify(req.body)
          : undefined,
    });

    // Handle non-JSON responses
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
      const data = await response.json();
      res.status(response.status).json(data);
    } else {
      const text = await response.text();
      res.status(response.status).send(text);
    }
  } catch (error) {
    console.error("API proxy error:", error);
    res.status(500).json({
      error: "Failed to proxy request",
      message: error instanceof Error ? error.message : "Unknown error",
      path: apiPath,
    });
  }
}
