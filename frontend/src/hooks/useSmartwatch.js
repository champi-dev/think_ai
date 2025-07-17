
import { useState, useEffect } from 'react';

const isSmartwatch = () => {
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;
  // Typical smartwatch screens are small and close to square.
  // Let's define a smartwatch as a screen smaller than 400x400 pixels.
  return screenWidth < 400 && screenHeight < 400;
};

export const useSmartwatch = () => {
  const [smartwatch, setSmartwatch] = useState(isSmartwatch());

  useEffect(() => {
    const handleResize = () => {
      setSmartwatch(isSmartwatch());
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return smartwatch;
};
