
import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import { expect, test, vi, beforeEach, describe } from 'vitest';
import { SmartwatchView } from './SmartwatchView';

describe('SmartwatchView Component', () => {
    beforeEach(() => {
        vi.spyOn(navigator, 'clipboard', 'get').mockReturnValue({
            writeText: vi.fn(),
          });
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

    test('renders the SmartwatchView component', () => {
        render(<SmartwatchView />);
        expect(screen.getByText('Tap to Speak')).toBeInTheDocument();
        expect(screen.getByText('🎤')).toBeInTheDocument();
    });

    test('clicking mic button starts and stops recording', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValue({
                ok: true,
                json: () => Promise.resolve({ text: 'hello', response: 'response' }),
                blob: () => Promise.resolve(new Blob(['audio data'])),
            });
        render(<SmartwatchView />);
        const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
      
        // Start recording
        await act(async () => {
          fireEvent.click(watchFace);
        });
        expect(navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({ audio: true });
        await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
        
        const mediaRecorder = global.getMediaRecorderInstance();
        expect(mediaRecorder.start).toHaveBeenCalled();
      
        // Stop recording
        await act(async () => {
          fireEvent.click(watchFace);
          // Manually trigger onstop for the test
          if (mediaRecorder.onstop) {
            mediaRecorder.onstop();
          }
        });
        
        expect(mediaRecorder.stop).toHaveBeenCalled();
        await waitFor(() => expect(screen.getByText('Speaking...')).toBeInTheDocument());
      });
      
      test('handles transcription and chat response', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValue({
                ok: true,
                json: () => Promise.resolve({ text: 'hello', response: 'response' }),
                blob: () => Promise.resolve(new Blob(['audio data'])),
            });
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
        
          // Start and stop recording to trigger the full flow
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
              // Manually trigger onstop for the test
              if (mediaRecorder.onstop) {
                  mediaRecorder.onstop();
              }
          });
        
          await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/audio/transcribe', expect.any(Object)));
          await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/chat', expect.any(Object)));
          await waitFor(() => expect(fetch).toHaveBeenCalledWith('/api/audio/synthesize', expect.any(Object)));
          await waitFor(() => expect(screen.getByText('Converting to audio...')).toBeInTheDocument());
          await waitFor(() => expect(screen.getByText('Converting to audio...')).toBeInTheDocument());
          await waitFor(() => expect(screen.getByText('Speaking...')).toBeInTheDocument());
      });
      
      test('handles microphone permission error', async () => {
          navigator.mediaDevices.getUserMedia.mockRejectedValueOnce(new Error('Permission denied'));
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Mic permission needed.')).toBeInTheDocument());
      });
      
      test('handles transcription error', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValueOnce({ ok: false, status: 500 }); // transcribe fails
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('An error occurred.')).toBeInTheDocument());
      });
      
      test('handles chat error', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ text: 'hello' }) }) // transcribe works
            .mockResolvedValueOnce({ ok: false, status: 500 }); // chat fails
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('An error occurred.')).toBeInTheDocument());
      });
      
      test('handles synthesis error', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ text: 'hello' }) }) // transcribe works
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ response: 'response' }) }) // chat works
            .mockResolvedValueOnce({ ok: false, status: 500 }); // synthesis fails
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Error playing response.')).toBeInTheDocument());
      });
      
      test('handles no speech detected', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ text: '' }) }); // transcribe returns empty
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('No speech detected.')).toBeInTheDocument());
      });

      test('sends X-Language auto header for multilingual STT', async () => {
        global.fetch = vi.fn()
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ language: 'en' }) }) // detect-language
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ text: 'multilingual text' }) }) // transcribe
            .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ response: 'response' }) }) // chat
            .mockResolvedValueOnce({ ok: true, blob: () => Promise.resolve(new Blob(['audio data'])) }); // synthesize
          
          render(<SmartwatchView />);
          const watchFace = screen.getByText('🎤').closest('.smartwatch-container');
          
          await act(async () => {
              fireEvent.click(watchFace);
          });
          await waitFor(() => expect(screen.getByText('Listening...')).toBeInTheDocument());
          
          const mediaRecorder = global.getMediaRecorderInstance();
          await act(async () => {
              fireEvent.click(watchFace);
          });
          
          await waitFor(() => {
              const transcriptionCall = global.fetch.mock.calls.find(call => 
                  call[0] === '/api/audio/transcribe'
              );
              expect(transcriptionCall).toBeDefined();
              expect(transcriptionCall[1].headers['X-Language']).toBe('auto');
          });
      });
});
