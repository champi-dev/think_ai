# API Documentation

The Think AI API provides a comprehensive set of endpoints for interacting with the AI system, managing sessions, and accessing system information.

## Base URL

- **Production**: `https://thinkai.lat/api`
- **Development**: `http://localhost:8080/api`

## Authentication

Currently, the API is open access. Future versions will support API key authentication.

## Endpoints

### Health Check

#### Basic Health Check

```http
GET /health
```

Returns a simple health status.

**Response**
```
OK
```

#### Detailed Health Check

```http
GET /api/health
```

Returns detailed service health information.

**Response**
```json
{
  "status": "healthy",
  "service": "think-ai-full",
  "version": "1.0.0",
  "timestamp": "2024-07-16T12:00:00Z"
}
```

### Chat Endpoints

#### Send Message

```http
POST /api/chat
Content-Type: application/json
```

Send a message to the AI and receive a response.

**Request Body**
```json
{
  "message": "string",
  "session_id": "string (optional)",
  "mode": "general | code (optional, default: general)",
  "use_web_search": "boolean (optional, default: false)",
  "fact_check": "boolean (optional, default: false)"
}
```

**Response**
```json
{
  "response": "string",
  "session_id": "string",
  "confidence": 0.95,
  "response_time_ms": 123.45,
  "consciousness_level": "aware",
  "tokens_used": 150,
  "context_tokens": 50,
  "compacted": false
}
```

**Example**
```bash
curl -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of France?",
    "session_id": "user-123",
    "mode": "general"
  }'
```

#### Stream Chat Response

```http
POST /api/chat/stream
Content-Type: application/json
Accept: text/event-stream
```

Stream the AI response using Server-Sent Events.

**Request Body**
Same as `/api/chat`

**Response** (Server-Sent Events)
```
data: {"chunk": "The capital", "done": false}
data: {"chunk": " of France", "done": false}
data: {"chunk": " is Paris.", "done": false}
data: {"chunk": "", "done": true, "metadata": {...}}
```

**Example**
```javascript
const eventSource = new EventSource('/api/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'Hello' })
});

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) {
    eventSource.close();
  }
};
```

### Session Management

#### List Sessions

```http
GET /api/chat/sessions
```

Get a list of all active sessions.

**Query Parameters**
- `limit` (optional): Maximum number of sessions to return (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response**
```json
[
  {
    "id": "session-123",
    "created_at": "2024-07-16T10:00:00Z",
    "last_active": "2024-07-16T12:00:00Z",
    "message_count": 10
  }
]
```

#### Get Session Details

```http
GET /api/chat/sessions/:session_id
```

Get detailed information about a specific session.

**Response**
```json
{
  "id": "session-123",
  "created_at": "2024-07-16T10:00:00Z",
  "last_active": "2024-07-16T12:00:00Z",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-07-16T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you?",
      "timestamp": "2024-07-16T10:00:01Z",
      "metadata": {
        "confidence": 0.98,
        "tokens_used": 10
      }
    }
  ]
}
```

#### Delete Session

```http
DELETE /api/chat/sessions/:session_id
```

Delete a session and all associated data.

**Response**
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

### Knowledge Base

#### Get Knowledge Domains

```http
GET /api/knowledge/domains
```

Get a list of available knowledge domains.

**Response**
```json
[
  "Technology",
  "Science",
  "Philosophy",
  "Mathematics",
  "Programming"
]
```

#### Search Knowledge

```http
GET /api/knowledge/search
```

Search the knowledge base.

**Query Parameters**
- `q` (required): Search query
- `domain` (optional): Limit to specific domain
- `limit` (optional): Maximum results (default: 10)

**Response**
```json
{
  "results": [
    {
      "id": "node-123",
      "topic": "Quantum Computing",
      "content": "Quantum computing leverages quantum mechanics...",
      "relevance": 0.95,
      "domain": "Technology"
    }
  ],
  "total": 42,
  "query_time_ms": 23.5
}
```

#### Get System Statistics

```http
GET /api/knowledge/stats
```

Get system-wide statistics.

**Response**
```json
{
  "total_knowledge_items": 50000,
  "active_sessions": 123,
  "average_response_time_ms": 150.5,
  "cache_hit_rate": 0.85,
  "uptime_seconds": 3600000,
  "consciousness_level": "enhanced",
  "domains": ["Technology", "Science", "Philosophy"]
}
```

### Consciousness Framework

#### Get Consciousness Level

```http
GET /api/consciousness/level
```

Get the current consciousness level of the system.

**Response**
```json
{
  "level": "AWARE",
  "description": "System is fully aware and responsive",
  "introspection_depth": 3,
  "metacognitive_score": 0.87,
  "timestamp": "2024-07-16T12:00:00Z"
}
```

#### Get System Thoughts

```http
GET /api/consciousness/thoughts
```

Get current system thought processes.

**Response**
```json
{
  "thoughts": [
    {
      "id": "thought-123",
      "content": "Processing natural language query",
      "category": "language_processing",
      "confidence": 0.92,
      "timestamp": "2024-07-16T12:00:00Z"
    }
  ],
  "thought_count": 15,
  "processing_state": "active"
}
```

### WebSocket Endpoint

```
WS /ws/chat
```

Establish a WebSocket connection for real-time bidirectional communication.

**Connection**
```javascript
const ws = new WebSocket('wss://thinkai.lat/ws/chat');
```

**Message Format (Client to Server)**
```json
{
  "type": "message",
  "content": "Hello AI",
  "session_id": "session-123"
}
```

**Message Format (Server to Client)**
```json
{
  "type": "response",
  "content": "Hello! How can I help?",
  "metadata": {
    "confidence": 0.95,
    "processing_time_ms": 100
  }
}
```

**Event Types**
- `message`: Regular chat message
- `response`: AI response
- `typing`: Typing indicator
- `error`: Error message
- `system`: System notification

## Error Responses

All endpoints return standard HTTP status codes and error messages.

### Error Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request body is invalid",
    "details": {
      "field": "message",
      "reason": "Required field missing"
    }
  },
  "timestamp": "2024-07-16T12:00:00Z",
  "request_id": "req-123"
}
```

### Common Error Codes

| Status Code | Error Code | Description |
|------------|------------|-------------|
| 400 | `INVALID_REQUEST` | Invalid request format or parameters |
| 401 | `UNAUTHORIZED` | Authentication required |
| 403 | `FORBIDDEN` | Access denied |
| 404 | `NOT_FOUND` | Resource not found |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable |

## Rate Limiting

Rate limits are applied per IP address:

- **Chat endpoints**: 60 requests per minute
- **Knowledge search**: 100 requests per minute
- **Other endpoints**: 300 requests per minute

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1689508800
```

## CORS

CORS is enabled for all origins in development. In production, only approved origins are allowed.

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Pagination

List endpoints support pagination using `limit` and `offset` parameters:

```http
GET /api/chat/sessions?limit=20&offset=40
```

Paginated responses include metadata:

```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 40,
    "has_more": true
  }
}
```

## Versioning

API versioning is handled through URL paths. The current version is v1 (implicit).

Future versions will use:
- `/api/v2/chat`
- `/api/v3/chat`

## SDK Support

Official SDKs are available for:

- **JavaScript/TypeScript**: `npm install think-ai-js`
- **Python**: `pip install think-ai-py`
- **Rust**: Add to Cargo.toml: `think-ai-client = "1.0"`

## Examples

### JavaScript/TypeScript

```typescript
import { ThinkAI } from 'think-ai-js';

const client = new ThinkAI({
  baseUrl: 'https://thinkai.lat',
  apiKey: 'your-api-key' // future
});

const response = await client.chat.send({
  message: 'Hello AI',
  mode: 'general'
});

console.log(response.response);
```

### Python

```python
from think_ai import ThinkAI

client = ThinkAI(base_url="https://thinkai.lat")

response = client.chat.send(
    message="Hello AI",
    mode="general"
)

print(response.response)
```

### cURL

```bash
# Simple chat
curl -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# With session
curl -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Remember that I like Python",
    "session_id": "user-123"
  }'

# Code mode with web search
curl -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Latest Python async patterns",
    "mode": "code",
    "use_web_search": true
  }'
```

## Best Practices

1. **Use Sessions**: Always provide a session_id for context continuity
2. **Handle Errors**: Implement proper error handling for all API calls
3. **Respect Rate Limits**: Implement exponential backoff for retries
4. **Stream for Long Responses**: Use SSE endpoint for better UX
5. **Cache Responses**: Cache appropriate responses client-side
6. **Validate Input**: Validate input before sending to API
7. **Use Appropriate Modes**: Use 'code' mode for programming questions