import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { AutoVoiceDetector } from './AutoVoiceDetector';

// Mock the translations module
vi.mock('../i18n/translations', () => ({
  getTranslation: (key, lang) => {
    const translations = {
      readyToListen: 'Ready to listen',
      listeningForVoice: 'Listening for voice...',
      recording: 'Recording...',
      processing: 'Processing...',
      transcribing: 'Transcribing...',
      thinking: 'Thinking...',
      speaking: 'Speaking...',
      noSpeechDetected: 'No speech detected',
      errorOccurred: 'Error occurred',
      micPermissionNeeded: 'Microphone permission needed',
      autoDetectionOff: 'Auto-detection off',
      errorPlaying: 'Error playing audio'
    };
    return translations[key] || key;
  },
  detectLanguage: async () => 'en'
}));

// Mock MediaStream
const mockMediaStream = {
  getTracks: () => [{
    stop: vi.fn()
  }]
};

// Mock MediaRecorder
global.MediaRecorder = vi.fn().mockImplementation(() => ({
  start: vi.fn(),
  stop: vi.fn(),
  state: 'inactive',
  ondataavailable: null,
  onstop: null
}));

global.MediaRecorder.isTypeSupported = vi.fn(() => true);

// Mock AudioContext
const mockAnalyser = {
  fftSize: 256,
  smoothingTimeConstant: 0.8,
  frequencyBinCount: 128,
  getByteFrequencyData: vi.fn((array) => {
    // Simulate different audio levels
    for (let i = 0; i < array.length; i++) {
      array[i] = Math.random() * 255;
    }
  })
};

const mockAudioContext = {
  createAnalyser: () => mockAnalyser,
  createMediaStreamSource: () => ({ connect: vi.fn() }),
  state: 'running',
  resume: vi.fn().mockResolvedValue(undefined),
  close: vi.fn().mockResolvedValue(undefined)
};

global.AudioContext = vi.fn(() => mockAudioContext);
global.Audio = vi.fn().mockImplementation(() => ({
  play: vi.fn().mockResolvedValue(undefined),
  pause: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn()
}));

describe('AutoVoiceDetector', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    
    // Mock getUserMedia
    global.navigator.mediaDevices = {
      getUserMedia: vi.fn().mockResolvedValue(mockMediaStream)
    };
    
    // Mock fetch
    global.fetch = vi.fn();
    
    // Mock localStorage
    global.localStorage = {
      getItem: vi.fn(),
      setItem: vi.fn()
    };
    
    // Mock URL.createObjectURL
    global.URL.createObjectURL = vi.fn(() => 'blob:mock-url');
    global.URL.revokeObjectURL = vi.fn();
  });

  test('renders with initial state', async () => {
    render(<AutoVoiceDetector />);
    
    // Should show ready state after initialization
    await waitFor(() => {
      expect(screen.getByText('Ready to listen')).toBeInTheDocument();
    });
    
    // Should have toggle button
    expect(screen.getByRole('button')).toBeInTheDocument();
    expect(screen.getByText('Auto-Detection OFF')).toBeInTheDocument();
  });

  test('starts monitoring when toggle is clicked', async () => {
    render(<AutoVoiceDetector />);
    
    const toggleButton = screen.getByRole('button');
    
    // Click to start monitoring
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.getUserMedia).toHaveBeenCalledWith({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });
    });
    
    // Should show listening state
    await waitFor(() => {
      expect(screen.getByText('Listening for voice...')).toBeInTheDocument();
    });
  });

  test('handles microphone permission denied', async () => {
    global.navigator.mediaDevices.getUserMedia.mockRejectedValueOnce(
      new Error('Permission denied')
    );
    
    render(<AutoVoiceDetector />);
    
    const toggleButton = screen.getByRole('button');
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      expect(screen.getByText('Microphone permission needed')).toBeInTheDocument();
    });
  });

  test('starts recording when voice is detected', async () => {
    render(<AutoVoiceDetector />);
    
    // Mock high audio level for voice detection
    mockAnalyser.getByteFrequencyData.mockImplementation((array) => {
      for (let i = 0; i < array.length; i++) {
        array[i] = 200; // High volume
      }
    });
    
    const toggleButton = screen.getByRole('button');
    fireEvent.click(toggleButton);
    
    // Wait for monitoring to start
    await waitFor(() => {
      expect(screen.getByText('Listening for voice...')).toBeInTheDocument();
    });
    
    // Simulate animation frames for audio analysis
    for (let i = 0; i < 10; i++) {
      vi.advanceTimersByTime(16); // ~60fps
    }
    
    // Should start recording after voice detection timeout
    vi.advanceTimersByTime(300); // VOICE_DETECTION_TIME
    
    await waitFor(() => {
      expect(MediaRecorder).toHaveBeenCalled();
    });
  });

  test('stops recording on silence', async () => {
    const mockRecorder = new MediaRecorder(mockMediaStream);
    
    render(<AutoVoiceDetector />);
    
    // Start monitoring and recording
    const toggleButton = screen.getByRole('button');
    fireEvent.click(toggleButton);
    
    // Mock voice detection then silence
    mockAnalyser.getByteFrequencyData
      .mockImplementationOnce((array) => {
        // High volume - voice
        for (let i = 0; i < array.length; i++) {
          array[i] = 200;
        }
      })
      .mockImplementation((array) => {
        // Low volume - silence
        for (let i = 0; i < array.length; i++) {
          array[i] = 10;
        }
      });
    
    // Wait for recording to start
    vi.advanceTimersByTime(400);
    
    // Simulate silence for 2 seconds
    vi.advanceTimersByTime(2000); // SILENCE_TIMEOUT
    
    await waitFor(() => {
      expect(mockRecorder.stop).toHaveBeenCalled();
    });
  });

  test('sends audio for transcription after recording', async () => {
    global.fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ text: 'Hello world' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: 'Hi there!' })
      })
      .mockResolvedValueOnce({
        ok: true,
        blob: async () => new Blob(['audio'], { type: 'audio/mp3' })
      });
    
    render(<AutoVoiceDetector />);
    
    const mockRecorder = new MediaRecorder(mockMediaStream);
    
    // Trigger recording stop
    mockRecorder.ondataavailable({ data: new Blob(['audio'], { type: 'audio/webm' }) });
    mockRecorder.onstop();
    
    await waitFor(() => {
      // Should call transcribe API
      expect(fetch).toHaveBeenCalledWith('/api/audio/transcribe', expect.any(Object));
      
      // Should call chat API
      expect(fetch).toHaveBeenCalledWith('/api/chat', expect.any(Object));
      
      // Should call synthesize API
      expect(fetch).toHaveBeenCalledWith('/api/audio/synthesize', expect.any(Object));
    });
  });

  test('handles transcription errors gracefully', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(<AutoVoiceDetector />);
    
    const mockRecorder = new MediaRecorder(mockMediaStream);
    mockRecorder.ondataavailable({ data: new Blob(['audio'], { type: 'audio/webm' }) });
    mockRecorder.onstop();
    
    await waitFor(() => {
      expect(screen.getByText('Error occurred')).toBeInTheDocument();
    });
    
    // Should resume monitoring after error
    vi.advanceTimersByTime(2000);
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.getUserMedia).toHaveBeenCalledTimes(2);
    });
  });

  test('shows visual audio level indicator', async () => {
    render(<AutoVoiceDetector />);
    
    const toggleButton = screen.getByRole('button');
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      const audioLevelBar = screen.getByTestId('audio-level-bar');
      expect(audioLevelBar).toBeInTheDocument();
      
      // Should have voice threshold line
      const thresholdLine = screen.getByTitle('Voice detection threshold');
      expect(thresholdLine).toBeInTheDocument();
    });
  });

  test('cleans up resources on unmount', async () => {
    const { unmount } = render(<AutoVoiceDetector />);
    
    const toggleButton = screen.getByRole('button');
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      expect(global.navigator.mediaDevices.getUserMedia).toHaveBeenCalled();
    });
    
    unmount();
    
    // Should clean up streams and audio context
    expect(mockMediaStream.getTracks()[0].stop).toHaveBeenCalled();
    expect(mockAudioContext.close).toHaveBeenCalled();
  });
});