
import { useState, useEffect } from 'react';

const isSmartwatch = () => {
  // Check for force parameter in URL
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('smartwatch') === 'true') {
    return true;
  }
  
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;
  // Show smartwatch UI for screens 500px or less
  return screenWidth <= 500 || screenHeight <= 500;
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
