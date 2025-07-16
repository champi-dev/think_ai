# Frontend Documentation

The Think AI frontend is a modern React application built with Vite, offering a responsive and intuitive interface for interacting with the AI system.

## Overview

The frontend provides:
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Communication**: WebSocket and SSE support for streaming responses
- **PWA Capabilities**: Installable as a native app with offline support
- **Modern UI/UX**: Clean, accessible interface with smooth animations

## Technology Stack

- **React 19**: Latest React with concurrent features
- **Vite**: Lightning-fast build tool with HMR
- **CSS Modules**: Scoped styling with modern CSS features
- **Vitest**: Fast unit testing framework
- **Playwright**: E2E testing across browsers

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── App.test.jsx         # Unit tests
│   ├── App.integration.jsx  # Integration tests
│   ├── index.css           # Global styles
│   ├── main.jsx           # Application entry point
│   └── test-setup.js      # Test configuration
├── public/
│   ├── favicon.svg        # Brain emoji favicon
│   ├── manifest.json      # PWA manifest
│   └── icons/            # PWA icons
├── dist/                 # Production build output
├── vite.config.js       # Vite configuration
└── package.json        # Dependencies and scripts
```

## Key Features

### 1. Responsive Chat Interface

The main chat interface adapts to different screen sizes:

```jsx
// Mobile-first responsive design
<div className="app-container">
  <header className="header">
    {/* Responsive header with mobile menu */}
  </header>
  
  <main className="chat-container">
    <div className="messages-container">
      {/* Auto-scrolling message list */}
    </div>
  </main>
  
  <footer className="input-area">
    {/* Adaptive input controls */}
  </footer>
</div>
```

### 2. Real-time Streaming

Support for streaming AI responses:

```jsx
// Server-Sent Events for streaming
const eventSource = new EventSource('/api/chat/stream');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateMessage(data.chunk);
};

// WebSocket for bi-directional communication
const ws = new WebSocket('ws://localhost:8080/ws/chat');
ws.onmessage = (event) => {
  handleWebSocketMessage(JSON.parse(event.data));
};
```

### 3. Session Management

Persistent conversations across page reloads:

```jsx
// Session persistence with localStorage
useEffect(() => {
  const savedSession = localStorage.getItem('think-ai-session');
  if (savedSession) {
    setSessionId(savedSession);
    loadSessionHistory(savedSession);
  }
}, []);
```

### 4. Feature Toggles

Interactive feature controls:

```jsx
// AI Mode toggle (General/Code)
<label className="toggle-switch">
  <input
    type="checkbox"
    checked={isCodeMode}
    onChange={(e) => setIsCodeMode(e.target.checked)}
  />
  <span className="slider"></span>
</label>

// Web Search and Fact Check toggles
<div className="feature-toggles">
  <button 
    className={`feature-toggle ${useWebSearch ? 'active' : ''}`}
    onClick={() => setUseWebSearch(!useWebSearch)}
  >
    🔍
  </button>
</div>
```

### 5. PWA Support

Progressive Web App capabilities:

```json
// manifest.json
{
  "name": "Think AI",
  "short_name": "Think AI",
  "description": "Advanced AI Assistant",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#ffffff",
  "background_color": "#f0f0f0",
  "icons": [
    {
      "src": "data:image/svg+xml,<svg>🧠</svg>",
      "sizes": "192x192",
      "type": "image/svg+xml"
    }
  ]
}
```

## Styling

The application uses modern CSS with custom properties:

```css
/* CSS Variables for theming */
:root {
  --primary-color: #4a90e2;
  --text-color: #333;
  --bg-color: #ffffff;
  --border-radius: 8px;
  --transition: all 0.3s ease;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --text-color: #ffffff;
    --bg-color: #1a1a1a;
  }
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .chat-container {
    padding: 10px;
  }
}
```

## Component Architecture

### App Component

Main application component with state management:

```jsx
function App() {
  // State management
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  
  // Feature states
  const [isCodeMode, setIsCodeMode] = useState(false);
  const [useWebSearch, setUseWebSearch] = useState(false);
  const [useFactCheck, setUseFactCheck] = useState(false);
  
  // Message handling
  const handleSendMessage = async (message) => {
    // Send to API
    // Handle response
    // Update UI
  };
  
  return (
    // JSX structure
  );
}
```

## API Integration

### Chat Endpoint

```javascript
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userMessage,
    session_id: sessionId,
    mode: isCodeMode ? 'code' : 'general',
    use_web_search: useWebSearch,
    fact_check: useFactCheck
  })
});
```

### Response Handling

```javascript
const data = await response.json();
// Response structure:
{
  response: string,
  session_id: string,
  confidence: number,
  response_time_ms: number,
  consciousness_level: string,
  tokens_used: number,
  context_tokens: number,
  compacted: boolean
}
```

## Development

### Setup

```bash
cd frontend
npm install
npm run dev
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm test` - Run unit tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Generate coverage report
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript checks

### Environment Variables

```bash
# .env.local
VITE_API_URL=http://localhost:8080
VITE_WS_URL=ws://localhost:8080
VITE_ENABLE_PWA=true
```

## Testing

### Unit Tests

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

test('sends message on button click', async () => {
  const user = userEvent.setup();
  render(<App />);
  
  const input = screen.getByPlaceholderText('Type your message here...');
  const button = screen.getByText('Send');
  
  await user.type(input, 'Hello AI');
  await user.click(button);
  
  expect(screen.getByText('Hello AI')).toBeInTheDocument();
});
```

### E2E Tests

```javascript
import { test, expect } from '@playwright/test';

test('complete chat flow', async ({ page }) => {
  await page.goto('/');
  await page.fill('input[placeholder="Type your message here..."]', 'Hello');
  await page.click('button:has-text("Send")');
  
  await expect(page.locator('.message.assistant')).toBeVisible();
});
```

## Performance Optimization

1. **Code Splitting**: Dynamic imports for large components
2. **Memoization**: React.memo for expensive components
3. **Virtualization**: Virtual scrolling for long message lists
4. **Lazy Loading**: Images and assets loaded on demand
5. **Service Worker**: Caching for offline support

## Accessibility

- **ARIA Labels**: Proper labeling for screen readers
- **Keyboard Navigation**: Full keyboard support
- **Focus Management**: Logical focus flow
- **Color Contrast**: WCAG AA compliant
- **Responsive Text**: Scalable font sizes

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari iOS 14+
- Chrome Android 90+

## Deployment

### Production Build

```bash
npm run build
# Output in dist/ directory
```

### Serving Static Files

The production build can be served by the Rust backend or any static file server:

```nginx
location / {
  root /var/www/think-ai/dist;
  try_files $uri $uri/ /index.html;
}
```

## Future Enhancements

1. **Theme System**: User-selectable themes
2. **Markdown Rendering**: Rich text formatting
3. **File Uploads**: Support for image/document analysis
4. **Voice Input**: Speech-to-text integration
5. **Collaborative Sessions**: Multi-user conversations
6. **Plugin System**: Extensible UI components