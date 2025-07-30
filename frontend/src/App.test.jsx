
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { test, describe, expect, beforeEach, vi } from 'vitest';

describe('App Component', () => {
  beforeEach(() => {
    vi.spyOn(navigator.clipboard, 'writeText').mockResolvedValue(undefined);
    if (!navigator.mediaDevices) {
        Object.defineProperty(navigator, 'mediaDevices', {
            value: {
                getUserMedia: vi.fn().mockResolvedValue({
                    getTracks: () => [{ stop: vi.fn() }],
                }),
            },
            writable: true,
            configurable: true,
        });
    }
  });

  test('renders main UI elements', () => {
    render(<App />);
    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  test('sends message on button click', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Hello! How can I help you?',
      })
    });

    const user = userEvent.setup();
    render(<App />);
    
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    
    await user.type(input, 'Hello AI');
    await user.click(sendButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/chat', expect.any(Object));
    });
    
    await waitFor(() => {
      expect(screen.getByText('Hello AI')).toBeInTheDocument();
      expect(screen.getByText('Hello! How can I help you?')).toBeInTheDocument();
    });
  });

  test('toggles code mode', async () => {
    const user = userEvent.setup();
    render(<App />);
    const modeToggle = screen.getByText(/AI Mode/i);
    await user.click(modeToggle);
    expect(screen.getByText(/Code/i)).toBeInTheDocument();
  });

  test('toggles web search', async () => {
    const user = userEvent.setup();
    render(<App />);
    const webSearchToggle = screen.getByText('🔍');
    await user.click(webSearchToggle);
    expect(webSearchToggle.parentElement).toHaveClass('active');
  });

  test('toggles fact check', async () => {
    const user = userEvent.setup();
    render(<App />);
    const factCheckToggle = screen.getByText('✅');
    await user.click(factCheckToggle);
    expect(factCheckToggle.parentElement).toHaveClass('active');
  });

  test('handles copy message', async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          response: 'This is a response',
        })
      });
    const user = userEvent.setup();
    render(<App />);
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    await user.type(input, 'test');
    await user.click(sendButton);

    await waitFor(() => {
        expect(screen.getByText('This is a response')).toBeInTheDocument();
    });

    const copyButton = screen.getByRole('button', {name: /copy/i});
    await user.click(copyButton);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('This is a response');
  });

  test('handles audio playback', async () => {
    global.fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          response: 'This is a response',
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        blob: async () => new Blob(),
    });

    const user = userEvent.setup();
    render(<App />);
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    await user.type(input, 'test');
    await user.click(sendButton);

    await waitFor(() => {
        expect(screen.getByText('This is a response')).toBeInTheDocument();
    });

    const playButton = screen.getByRole('button', {name: /play/i});
    await user.click(playButton);
    expect(HTMLMediaElement.prototype.play).toHaveBeenCalled();
  });

  test('shows converting to audio status during TTS', async () => {
    global.fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          response: 'This is a response',
        })
      })
      .mockImplementationOnce(() => new Promise(resolve => {
        setTimeout(() => {
          resolve({
            ok: true,
            blob: async () => new Blob(),
          });
        }, 100);
      }));

    const user = userEvent.setup();
    render(<App />);
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    await user.type(input, 'test');
    await user.click(sendButton);

    await waitFor(() => {
        expect(screen.getByText('This is a response')).toBeInTheDocument();
    });

    const playButton = screen.getByRole('button', {name: /play/i});
    await user.click(playButton);
    
    // Should show converting status
    await waitFor(() => {
        expect(screen.getByText('Converting to audio...')).toBeInTheDocument();
    });
    
    // Wait for playing status
    await waitFor(() => {
        expect(screen.getByText('Playing')).toBeInTheDocument();
    });
  });

  test('handles audio synthesis error', async () => {
    global.fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          response: 'This is a response',
        })
      })
      .mockRejectedValueOnce(new Error('Synthesis failed'));

    const user = userEvent.setup();
    render(<App />);
    const input = screen.getByRole('textbox');
    const sendButton = screen.getByRole('button', { name: /send message/i });
    await user.type(input, 'test');
    await user.click(sendButton);

    await waitFor(() => {
        expect(screen.getByText('This is a response')).toBeInTheDocument();
    });

    const playButton = screen.getByRole('button', {name: /play/i});
    await user.click(playButton);
    
    // Should revert to Play after error
    await waitFor(() => {
        expect(screen.getByText('Play')).toBeInTheDocument();
    });
  });

  test('handles audio recording', async () => {
    // Mock successful transcription
    global.fetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ text: 'Transcribed text' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'AI response' })
      });
      
    const user = userEvent.setup();
    render(<App />);
    const micButton = screen.getByText('🎤');
    await user.click(micButton);
    await waitFor(() => expect(screen.getByText('⏹️')).toBeInTheDocument());
    await user.click(micButton);
    await waitFor(() => expect(screen.getByText('🎤')).toBeInTheDocument());
  });

  test('sends X-Language auto header for multilingual STT', async () => {
    const mockFetch = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ text: 'Transcribed text' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'AI response' })
      });
    
    global.fetch = mockFetch;
    
    // Mock MediaRecorder
    const mockStop = vi.fn();
    const mockStart = vi.fn();
    const mockMediaRecorder = {
      start: mockStart,
      stop: mockStop,
      addEventListener: vi.fn((event, handler) => {
        if (event === 'dataavailable') {
          setTimeout(() => {
            handler({ data: new Blob(['audio'], { type: 'audio/webm' }) });
          }, 100);
        }
      }),
      removeEventListener: vi.fn(),
    };
    
    global.MediaRecorder = vi.fn(() => mockMediaRecorder);
    global.MediaRecorder.isTypeSupported = vi.fn().mockReturnValue(true);
    
    // Mock navigator.mediaDevices
    global.navigator.mediaDevices = {
      getUserMedia: vi.fn().mockResolvedValue({
        getTracks: () => [],
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })
    };
    
    const user = userEvent.setup();
    render(<App />);
    const micButton = screen.getByText('🎤');
    
    // Start recording
    await user.click(micButton);
    await waitFor(() => expect(screen.getByText('⏹️')).toBeInTheDocument());
    
    // Stop recording
    await user.click(micButton);
    
    // Wait for transcription request
    await waitFor(() => {
      const transcriptionCall = mockFetch.mock.calls.find(call => 
        call[0] === '/api/audio/transcribe'
      );
      expect(transcriptionCall).toBeDefined();
      expect(transcriptionCall[1].headers['X-Language']).toBe('auto');
    });
  });
});
