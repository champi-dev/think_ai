// Test setup for vitest
import '@testing-library/jest-dom';
import { afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';

// Cleanup after each test
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Mock fetch
global.fetch = vi.fn((url, options) => {
  // Default mock for detect-language endpoint
  if (url === '/api/detect-language') {
    return Promise.resolve({
      ok: true,
      json: async () => ({ language: 'en' })
    });
  }
  
  // Return rejected promise for unmocked requests
  return Promise.reject(new Error(`Unmocked request to ${url}`));
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }))
});

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock requestAnimationFrame
vi.stubGlobal('requestAnimationFrame', (cb) => setTimeout(cb, 0));
vi.stubGlobal('cancelAnimationFrame', (id) => clearTimeout(id));


// Mock scrollIntoView
window.HTMLElement.prototype.scrollIntoView = vi.fn();

// Mock URL.createObjectURL
global.URL.createObjectURL = vi.fn();


// Mock Canvas API
HTMLCanvasElement.prototype.getContext = () => {
    return {
        fillRect: vi.fn(),
        createRadialGradient: vi.fn(() => ({
            addColorStop: vi.fn(),
        })),
        beginPath: vi.fn(),
        arc: vi.fn(),
        fill: vi.fn(),
        save: vi.fn(),
        restore: vi.fn(),
    }
};


// Mock MediaRecorder
let mediaRecorderInstance;
const mockMediaRecorder = {
    start: vi.fn(),
    stop: vi.fn(),
    ondataavailable: null,
    onstop: null,
    state: 'inactive',
    addEventListener: vi.fn((event, handler) => {
      if (event === 'dataavailable') {
        mockMediaRecorder.ondataavailable = handler;
      } else if (event === 'stop') {
        mockMediaRecorder.onstop = handler;
      }
    }),
    removeEventListener: vi.fn(),
  };
  
const MediaRecorderMock = vi.fn().mockImplementation(() => {
    mediaRecorderInstance = Object.create(mockMediaRecorder);
    mediaRecorderInstance.state = 'recording';
    
    // Auto-trigger data available when stop is called
    const originalStop = mediaRecorderInstance.stop;
    mediaRecorderInstance.stop = vi.fn(() => {
      originalStop();
      if (mediaRecorderInstance.ondataavailable) {
        setTimeout(() => {
          mediaRecorderInstance.ondataavailable({ 
            data: new Blob(['audio'], { type: 'audio/webm' }) 
          });
          if (mediaRecorderInstance.onstop) {
            mediaRecorderInstance.onstop();
          }
        }, 0);
      }
    });
    
    return mediaRecorderInstance;
});
MediaRecorderMock.isTypeSupported = vi.fn().mockReturnValue(true);
global.MediaRecorder = MediaRecorderMock;
global.getMediaRecorderInstance = () => mediaRecorderInstance;

// Mock AudioContext
const mockAnalyser = {
  connect: vi.fn(),
  disconnect: vi.fn(),
  getByteFrequencyData: vi.fn((array) => {
    // Fill with some data
    for (let i = 0; i < array.length; i++) {
      array[i] = 128;
    }
  }),
  fftSize: 256,
  frequencyBinCount: 128,
};

const mockAudioContext = {
  createAnalyser: vi.fn(() => mockAnalyser),
  createMediaStreamSource: vi.fn(() => ({
    connect: vi.fn(),
    disconnect: vi.fn(),
  })),
  close: vi.fn(),
  state: 'running',
};

global.AudioContext = vi.fn(() => mockAudioContext);
global.webkitAudioContext = global.AudioContext;


// Mock HTMLMediaElement.prototype.play
HTMLMediaElement.prototype.play = vi.fn();
HTMLMediaElement.prototype.pause = vi.fn();
HTMLMediaElement.prototype.load = vi.fn();

// Mock window.alert
window.alert = vi.fn();

// Mock navigator.clipboard
Object.defineProperty(navigator, 'clipboard', {
    value: {
      writeText: vi.fn(),
    },
    writable: true,
    configurable: true,
  });