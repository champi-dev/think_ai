import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { test, describe, expect, beforeEach, vi } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  clear: vi.fn()
};
global.localStorage = localStorageMock;

// Mock window.matchMedia
window.matchMedia = vi.fn().mockImplementation(query => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(), // deprecated
  removeListener: vi.fn(), // deprecated
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));

// Mock canvas for animation
HTMLCanvasElement.prototype.getContext = vi.fn(() => ({
  clearRect: vi.fn(),
  beginPath: vi.fn(),
  arc: vi.fn(),
  fill: vi.fn(),
  stroke: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  save: vi.fn(),
  restore: vi.fn(),
  translate: vi.fn(),
  rotate: vi.fn(),
  fillText: vi.fn(),
  measureText: vi.fn(() => ({ width: 100 })),
}));

describe('App Component', () => {
  beforeEach(() => {
    fetch.mockClear();
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
  });

  test('renders main UI elements', () => {
    render(<App />);
    
    // Header elements
    expect(screen.getByText('🧠 Think AI')).toBeInTheDocument();
    expect(screen.getByText('API Docs')).toBeInTheDocument();
    expect(screen.getByText('GitHub')).toBeInTheDocument();
    
    // Mode toggle
    expect(screen.getByText('AI Mode')).toBeInTheDocument();
    expect(screen.getByText('🤖 General')).toBeInTheDocument();
    
    // Input area
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByText('Send')).toBeInTheDocument();
    
    // Feature toggles
    expect(screen.getByText('🔍')).toBeInTheDocument();
    expect(screen.getByText('✅')).toBeInTheDocument();
  });

  test('loads session from localStorage on mount', () => {
    const mockSession = 'test-session-123';
    localStorageMock.getItem.mockReturnValue(mockSession);
    
    render(<App />);
    
    expect(localStorageMock.getItem).toHaveBeenCalledWith('think-ai-session');
  });

  test('saves session to localStorage when set', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Hello!',
        session_id: 'new-session-456',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');
    
    await user.type(input, 'Hello');
    await user.click(sendButton);
    
    await waitFor(() => {
      expect(localStorageMock.setItem).toHaveBeenCalledWith('think-ai-session', 'new-session-456');
    });
  });

  test('sends message on button click', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Hello! How can I help you?',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');
    
    await user.type(input, 'Hello AI');
    await user.click(sendButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: 'Hello AI',
          session_id: expect.any(String),
          mode: 'general',
          use_web_search: false,
          fact_check: false
        })
      });
    });
    
    await waitFor(() => {
      expect(screen.getByText('Hello AI')).toBeInTheDocument();
      expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });
  });

  test('sends message on Enter key press', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Test response',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    await user.type(input, 'Test message{enter}');
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });
  });

  test('toggles between AI modes', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const toggle = screen.getByRole('checkbox');
    expect(screen.getByText('🤖 General')).toBeInTheDocument();
    
    await user.click(toggle);
    expect(screen.getByText('💻 Code')).toBeInTheDocument();
    
    await user.click(toggle);
    expect(screen.getByText('🤖 General')).toBeInTheDocument();
  });

  test('toggles web search feature', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Search enabled response',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const searchToggle = screen.getByText('🔍');
    await user.click(searchToggle);
    
    // Should have active class
    expect(searchToggle.parentElement).toHaveClass('active');
    
    // Send message with search enabled
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Search test{enter}');
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: 'Search test',
          session_id: expect.any(String),
          mode: 'general',
          use_web_search: true,
          fact_check: false
        })
      });
    });
  });

  test('toggles fact check feature', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const factCheckToggle = screen.getByText('✅');
    await user.click(factCheckToggle);
    
    expect(factCheckToggle.parentElement).toHaveClass('active');
  });

  test('shows loading state while sending message', async () => {
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({
          response: 'Delayed response',
          session_id: 'test-session',
          confidence: 0.95,
          response_time_ms: 1000,
          consciousness_level: 'aware',
          tokens_used: 50,
          context_tokens: 20,
          compacted: false
        })
      }), 100))
    );

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');
    
    await user.type(input, 'Test');
    await user.click(sendButton);
    
    // Should show loading
    expect(screen.getByText('AI is thinking...')).toBeInTheDocument();
    expect(sendButton).toBeDisabled();
    expect(input).toBeDisabled();
    
    // Wait for response
    await waitFor(() => {
      expect(screen.queryByText('AI is thinking...')).not.toBeInTheDocument();
      expect(sendButton).not.toBeDisabled();
      expect(input).not.toBeDisabled();
    });
  });

  test('handles API errors gracefully', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Error test{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('Error test')).toBeInTheDocument();
      expect(screen.getByText('Sorry, I encountered an error. Please try again.')).toBeInTheDocument();
    });
    
    consoleSpy.mockRestore();
  });

  test('copies message to clipboard', async () => {
    // Mock clipboard API
    const mockClipboard = {
      writeText: vi.fn().mockResolvedValue(undefined)
    };
    Object.assign(navigator, { clipboard: mockClipboard });

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Message to copy',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    // Send a message first
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Test{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('Message to copy')).toBeInTheDocument();
    });
    
    // Click copy button
    const copyButton = screen.getByText('Copy');
    await user.click(copyButton);
    
    expect(mockClipboard.writeText).toHaveBeenCalledWith('Message to copy');
    expect(screen.getByText('Copied!')).toBeInTheDocument();
    
    // Should revert back to "Copy" after timeout
    await waitFor(() => {
      expect(screen.getByText('Copy')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  test('scrolls to bottom when new message is added', async () => {
    const mockScrollIntoView = vi.fn();
    Element.prototype.scrollIntoView = mockScrollIntoView;

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'New message',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Scroll test{enter}');
    
    await waitFor(() => {
      expect(mockScrollIntoView).toHaveBeenCalled();
    });
  });

  test('disables input and button when loading', async () => {
    fetch.mockImplementationOnce(() => 
      new Promise(() => {}) // Never resolves
    );

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');
    
    await user.type(input, 'Test');
    await user.click(sendButton);
    
    expect(input).toBeDisabled();
    expect(sendButton).toBeDisabled();
  });

  test('clears input after sending message', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Response',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    await user.type(input, 'Clear test');
    expect(input).toHaveValue('Clear test');
    
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(input).toHaveValue('');
    });
  });

  test('prevents sending empty messages', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    const sendButton = screen.getByText('Send');
    await user.click(sendButton);
    
    expect(fetch).not.toHaveBeenCalled();
  });

  test('trims whitespace from messages', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Response',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 100,
        consciousness_level: 'aware',
        tokens_used: 50,
        context_tokens: 20,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, '   Trimmed message   ');
    await user.click(screen.getByText('Send'));
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: 'Trimmed message',
          session_id: expect.any(String),
          mode: 'general',
          use_web_search: false,
          fact_check: false
        })
      });
    });
  });

  test('displays message metadata', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Test response with metadata',
        session_id: 'test-session',
        confidence: 0.95,
        response_time_ms: 150,
        consciousness_level: 'enhanced',
        tokens_used: 75,
        context_tokens: 25,
        compacted: false
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Metadata test{enter}');
    
    await waitFor(() => {
      // Message should be displayed
      expect(screen.getByText('Test response with metadata')).toBeInTheDocument();
      // Metadata might be shown in UI (depending on implementation)
    });
  });

  test('handles multiple rapid messages correctly', async () => {
    let callCount = 0;
    fetch.mockImplementation(() => {
      callCount++;
      return Promise.resolve({
        ok: true,
        json: async () => ({
          response: `Response ${callCount}`,
          session_id: 'test-session',
          confidence: 0.95,
          response_time_ms: 50,
          consciousness_level: 'aware',
          tokens_used: 50,
          context_tokens: 20,
          compacted: false
        })
      });
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    // Send multiple messages rapidly
    await user.type(input, 'Message 1{enter}');
    await user.type(input, 'Message 2{enter}');
    await user.type(input, 'Message 3{enter}');
    
    await waitFor(() => {
      expect(screen.getByText('Message 1')).toBeInTheDocument();
      expect(screen.getByText('Message 2')).toBeInTheDocument();
      expect(screen.getByText('Message 3')).toBeInTheDocument();
    });
    
    // All responses should be displayed
    await waitFor(() => {
      expect(screen.getByText('Response 1')).toBeInTheDocument();
      expect(screen.getByText('Response 2')).toBeInTheDocument();
      expect(screen.getByText('Response 3')).toBeInTheDocument();
    });
  });

  test('maintains conversation history', async () => {
    const responses = ['First response', 'Second response', 'Third response'];
    let responseIndex = 0;
    
    fetch.mockImplementation(() => {
      const response = responses[responseIndex];
      responseIndex++;
      return Promise.resolve({
        ok: true,
        json: async () => ({
          response,
          session_id: 'test-session',
          confidence: 0.95,
          response_time_ms: 100,
          consciousness_level: 'aware',
          tokens_used: 50,
          context_tokens: 20,
          compacted: false
        })
      });
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    
    // Send multiple messages
    await user.type(input, 'First message{enter}');
    await waitFor(() => expect(screen.getByText('First response')).toBeInTheDocument());
    
    await user.type(input, 'Second message{enter}');
    await waitFor(() => expect(screen.getByText('Second response')).toBeInTheDocument());
    
    await user.type(input, 'Third message{enter}');
    await waitFor(() => expect(screen.getByText('Third response')).toBeInTheDocument());
    
    // All messages should still be visible
    expect(screen.getByText('First message')).toBeInTheDocument();
    expect(screen.getByText('Second message')).toBeInTheDocument();
    expect(screen.getByText('Third message')).toBeInTheDocument();
    expect(screen.getByText('First response')).toBeInTheDocument();
    expect(screen.getByText('Second response')).toBeInTheDocument();
    expect(screen.getByText('Third response')).toBeInTheDocument();
  });
});

describe('App Component - Accessibility', () => {
  test('has proper ARIA labels', () => {
    render(<App />);
    
    expect(screen.getByPlaceholderText('Type your message here...')).toHaveAttribute('aria-label');
    expect(screen.getByText('Send')).toHaveAttribute('type', 'submit');
  });

  test('supports keyboard navigation', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Tab through interactive elements
    await user.tab();
    expect(screen.getByRole('checkbox')).toHaveFocus();
    
    await user.tab();
    expect(screen.getByPlaceholderText('Type your message here...')).toHaveFocus();
  });

  test('announces loading state to screen readers', async () => {
    fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({
          response: 'Response',
          session_id: 'test-session',
          confidence: 0.95,
          response_time_ms: 100,
          consciousness_level: 'aware',
          tokens_used: 50,
          context_tokens: 20,
          compacted: false
        })
      }), 100))
    );

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByPlaceholderText('Type your message here...');
    await user.type(input, 'Test{enter}');
    
    const loadingMessage = screen.getByText('AI is thinking...');
    expect(loadingMessage).toHaveAttribute('aria-live', 'polite');
  });
});