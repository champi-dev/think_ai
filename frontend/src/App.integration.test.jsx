
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { test, describe, expect, beforeEach, afterEach, vi } from 'vitest';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.post('/api/chat', async ({request}) => {
    const { message } = await request.json();
    
    let response = 'Default response';
    if (message.toLowerCase().includes('hello')) {
      response = 'Hello! How can I help you today?';
    }
    
    await new Promise(resolve => setTimeout(resolve, 100));
    
    return HttpResponse.json({ response });
  }),
);

describe('App Integration Tests', () => {
    beforeEach(() => {
        server.listen({ onUnhandledRequest: 'error' });
        global.innerWidth = 1920;
        global.innerHeight = 1080;
        global.dispatchEvent(new Event('resize'));
      });
      
      afterEach(() => {
        server.resetHandlers();
        vi.clearAllMocks();
      });
      
      afterEach(() => {
        server.close();
      });

  test('complete user journey - basic conversation', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Verify initial state
    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    
    // Start conversation
    const input = screen.getByRole('textbox');
    await user.type(input, 'Hello AI');
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('Hello AI')).toBeInTheDocument();
      expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
    });
  });
});

describe('Smartwatch UI', () => {
    beforeEach(() => {
        server.listen({ onUnhandledRequest: 'error' });
        global.innerWidth = 1920;
        global.innerHeight = 1080;
        global.dispatchEvent(new Event('resize'));
      });
      
      afterEach(() => {
        server.resetHandlers();
        vi.clearAllMocks();
      });
      
      afterEach(() => {
        server.close();
      });

    test('renders SmartwatchView on small screens', () => {
      // Mock window dimensions for a smartwatch
      global.innerWidth = 360;
      global.innerHeight = 360;
      global.dispatchEvent(new Event('resize'));
  
      render(<App />);
  
      expect(screen.getByText('Tap to Speak')).toBeInTheDocument();
      expect(screen.queryByRole('banner')).not.toBeInTheDocument();
    });
  
    test('renders standard view on large screens', () => {
      // Mock window dimensions for a desktop
      global.innerWidth = 1920;
      global.innerHeight = 1080;
      global.dispatchEvent(new Event('resize'));
  
      render(<App />);
  
      expect(screen.getByRole('banner')).toBeInTheDocument();
      expect(screen.queryByText('Tap to Speak')).not.toBeInTheDocument();
    });
});
