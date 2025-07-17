
import { renderHook, act } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import { useSmartwatch } from './useSmartwatch';

test('should return false on non-smartwatch dimensions', () => {
  // Mock window dimensions for a desktop
  global.innerWidth = 1920;
  global.innerHeight = 1080;

  const { result } = renderHook(() => useSmartwatch());
  expect(result.current).toBe(false);
});

test('should return true on smartwatch dimensions', () => {
  // Mock window dimensions for a smartwatch
  global.innerWidth = 360;
  global.innerHeight = 360;

  const { result } = renderHook(() => useSmartwatch());
  expect(result.current).toBe(true);
});

test('should update on resize', () => {
  // Start with desktop dimensions
  global.innerWidth = 1920;
  global.innerHeight = 1080;

  const { result } = renderHook(() => useSmartwatch());
  expect(result.current).toBe(false);

  // Simulate resizing to smartwatch dimensions
  act(() => {
    global.innerWidth = 380;
    global.innerHeight = 380;
    global.dispatchEvent(new Event('resize'));
  });

  expect(result.current).toBe(true);

  // Simulate resizing back to desktop
  act(() => {
    global.innerWidth = 1024;
    global.innerHeight = 768;
    global.dispatchEvent(new Event('resize'));
  });

  expect(result.current).toBe(false);
});
