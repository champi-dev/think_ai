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
global.fetch = vi.fn();

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
  };
  
global.MediaRecorder = vi.fn().mockImplementation(() => {
    mediaRecorderInstance = mockMediaRecorder;
    mediaRecorderInstance.state = 'recording';
    return mediaRecorderInstance;
});
global.MediaRecorder.isTypeSupported = vi.fn().mockReturnValue(true);
global.getMediaRecorderInstance = () => mediaRecorderInstance;


// Mock HTMLMediaElement.prototype.play
HTMLMediaElement.prototype.play = vi.fn();
HTMLMediaElement.prototype.pause = vi.fn();
HTMLMediaElement.prototype.load = vi.fn();

// Mock navigator.clipboard
Object.defineProperty(navigator, 'clipboard', {
    value: {
      writeText: vi.fn(),
    },
    writable: true,
    configurable: true,
  });