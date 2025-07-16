import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { test, describe, expect, beforeEach, afterEach, vi } from 'vitest';

// Mock server for integration tests
import { setupServer } from 'msw/node';
import { rest } from 'msw';

// Create mock server
const server = setupServer(
  rest.post('/api/chat', async (req, res, ctx) => {
    const { message, session_id, mode, use_web_search, fact_check } = await req.json();
    
    // Simulate different responses based on input
    let response = 'Default response';
    let consciousness_level = 'aware';
    let confidence = 0.95;
    
    if (message.toLowerCase().includes('hello')) {
      response = 'Hello! How can I help you today?';
    } else if (message.toLowerCase().includes('code')) {
      response = 'Here\'s a Python function:\n```python\ndef greet(name):\n    return f"Hello, {name}!"\n```';
      consciousness_level = 'focused';
    } else if (message.toLowerCase().includes('search')) {
      response = 'Based on my web search, here are the latest findings...';
      confidence = 0.85;
    } else if (message.toLowerCase().includes('fact')) {
      response = 'Let me fact-check that for you. The statement appears to be accurate.';
      consciousness_level = 'analytical';
    } else if (message.toLowerCase().includes('error')) {
      return res(ctx.status(500), ctx.json({ error: 'Internal server error' }));
    }
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 100));
    
    return res(
      ctx.json({
        response,
        session_id: session_id || `session-${Date.now()}`,
        confidence,
        response_time_ms: 100 + Math.random() * 50,
        consciousness_level,
        tokens_used: Math.floor(50 + Math.random() * 100),
        context_tokens: Math.floor(20 + Math.random() * 30),
        compacted: false
      })
    );
  }),
  
  rest.get('/api/health', (req, res, ctx) => {
    return res(
      ctx.json({
        status: 'healthy',
        service: 'think-ai-full',
        version: '1.0.0'
      })
    );
  })
);

// Setup and teardown
beforeEach(() => {
  server.listen({ onUnhandledRequest: 'error' });
  localStorage.clear();
  sessionStorage.clear();
});

afterEach(() => {
  server.resetHandlers();
  vi.clearAllMocks();
});

afterEach(() => {
  server.close();
});

describe('App Integration Tests', () => {
  test('complete user journey - basic conversation', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Verify initial state
    expect(screen.getByText('🧠 Think AI')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    
    // Start conversation
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Hello AI');
    await user.click(screen.getByText('Send'));
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('Hello AI')).toBeInTheDocument();
      expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
    });
    
    // Continue conversation
    await user.type(input, 'Can you write some code?');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Can you write some code?')).toBeInTheDocument();
      expect(screen.getByText(/Here's a Python function/)).toBeInTheDocument();
    });
    
    // Verify session persistence
    expect(localStorage.getItem('think-ai-session')).toBeTruthy();
  });

  test('complete user journey - using AI features', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Toggle to code mode
    const modeToggle = screen.getByRole('checkbox');
    await user.click(modeToggle);
    expect(screen.getByText('💻 Code')).toBeInTheDocument();
    
    // Enable web search
    const searchToggle = screen.getByText('🔍');
    await user.click(searchToggle);
    expect(searchToggle.parentElement).toHaveClass('active');
    
    // Enable fact check
    const factCheckToggle = screen.getByText('✅');
    await user.click(factCheckToggle);
    expect(factCheckToggle.parentElement).toHaveClass('active');
    
    // Send message with features enabled
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Search for latest AI trends and fact check them');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText(/Based on my web search/)).toBeInTheDocument();
    });
  });

  test('error handling and recovery flow', async () => {
    const user = userEvent.setup();
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    render(<App />);
    
    // Trigger an error
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Trigger error');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Sorry, I encountered an error. Please try again.')).toBeInTheDocument();
    });
    
    // Verify app still works after error
    await user.clear(input);
    await user.type(input, 'Hello after error');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
    });
    
    consoleSpy.mockRestore();
  });

  test('session continuity across page reloads', async () => {
    const user = userEvent.setup();
    const { unmount } = render(<App />);
    
    // Create initial conversation
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Remember me');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Remember me')).toBeInTheDocument();
    });
    
    const sessionId = localStorage.getItem('think-ai-session');
    expect(sessionId).toBeTruthy();
    
    // Unmount and remount to simulate page reload
    unmount();
    render(<App />);
    
    // Verify session is restored
    expect(localStorage.getItem('think-ai-session')).toBe(sessionId);
  });

  test('concurrent message handling', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    // Send multiple messages rapidly
    await user.type(input, 'First message');
    await user.click(screen.getByText('Send'));
    
    await user.type(input, 'Second message');
    await user.click(screen.getByText('Send'));
    
    await user.type(input, 'Third message');
    await user.click(screen.getByText('Send'));
    
    // All messages should be displayed
    await waitFor(() => {
      expect(screen.getByText('First message')).toBeInTheDocument();
      expect(screen.getByText('Second message')).toBeInTheDocument();
      expect(screen.getByText('Third message')).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  test('copy functionality integration', async () => {
    const user = userEvent.setup();
    
    // Mock clipboard
    const mockClipboard = {
      writeText: vi.fn().mockResolvedValue(undefined)
    };
    Object.assign(navigator, { clipboard: mockClipboard });
    
    render(<App />);
    
    // Send message
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Hello');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
    });
    
    // Copy response
    const copyButton = screen.getByText('Copy');
    await user.click(copyButton);
    
    expect(mockClipboard.writeText).toHaveBeenCalledWith('Hello! How can I help you today?');
    expect(screen.getByText('Copied!')).toBeInTheDocument();
  });

  test('responsive UI behavior', async () => {
    const user = userEvent.setup();
    
    // Mock mobile viewport
    window.matchMedia = vi.fn().mockImplementation(query => ({
      matches: query === '(max-width: 768px)',
      media: query,
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));
    
    render(<App />);
    
    // UI should adapt to mobile
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Mobile test');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Mobile test')).toBeInTheDocument();
    });
  });

  test('performance - handles large conversation history', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    // Send many messages
    for (let i = 0; i < 20; i++) {
      await user.clear(input);
      await user.type(input, `Message ${i}`);
      await user.click(screen.getByText('Send'));
      
      // Wait for each response
      await waitFor(() => {
        expect(screen.getByText(`Message ${i}`)).toBeInTheDocument();
      });
    }
    
    // App should still be responsive
    await user.clear(input);
    await user.type(input, 'Final message');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Final message')).toBeInTheDocument();
    });
  });

  test('accessibility - keyboard navigation', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Tab navigation
    await user.tab();
    expect(screen.getByRole('checkbox')).toHaveFocus();
    
    await user.tab();
    expect(screen.getByPlaceholderText('Type your message here...')).toHaveFocus();
    
    // Enter to send
    await user.type(screen.getByPlaceholderText('Type your message here...'), 'Keyboard test{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('Keyboard test')).toBeInTheDocument();
    });
  });

  test('theme and visual consistency', async () => {
    render(<App />);
    
    // Check key visual elements
    expect(screen.getByText('🧠 Think AI')).toBeInTheDocument();
    expect(screen.getByText('API Docs')).toHaveAttribute('href', 'https://api.thinkai.lat/docs');
    expect(screen.getByText('GitHub')).toHaveAttribute('href', 'https://github.com/alienworkspace/think_ai');
    
    // Verify animations are present (canvas)
    const canvas = document.querySelector('canvas');
    expect(canvas).toBeInTheDocument();
  });
});

describe('App Integration Tests - Advanced Scenarios', () => {
  test('handles network interruption gracefully', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Simulate network failure
    server.use(
      rest.post('/api/chat', (req, res, ctx) => {
        return res.networkError('Failed to connect');
      })
    );
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Network test');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText('Sorry, I encountered an error. Please try again.')).toBeInTheDocument();
    });
  });

  test('handles slow network conditions', async () => {
    const user = userEvent.setup();
    
    // Mock slow response
    server.use(
      rest.post('/api/chat', async (req, res, ctx) => {
        await new Promise(resolve => setTimeout(resolve, 2000));
        return res(
          ctx.json({
            response: 'Slow response',
            session_id: 'slow-session',
            confidence: 0.95,
            response_time_ms: 2000,
            consciousness_level: 'aware',
            tokens_used: 50,
            context_tokens: 20,
            compacted: false
          })
        );
      })
    );
    
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Slow test');
    await user.click(screen.getByText('Send'));
    
    // Should show loading state
    expect(screen.getByText('AI is thinking...')).toBeInTheDocument();
    
    // Eventually show response
    await waitFor(() => {
      expect(screen.getByText('Slow response')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  test('memory management with large responses', async () => {
    const user = userEvent.setup();
    
    // Mock large response
    const largeResponse = 'Lorem ipsum '.repeat(1000);
    server.use(
      rest.post('/api/chat', async (req, res, ctx) => {
        return res(
          ctx.json({
            response: largeResponse,
            session_id: 'large-session',
            confidence: 0.95,
            response_time_ms: 100,
            consciousness_level: 'aware',
            tokens_used: 5000,
            context_tokens: 1000,
            compacted: false
          })
        );
      })
    );
    
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Large response test');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(screen.getByText(/Lorem ipsum/)).toBeInTheDocument();
    });
  });
});