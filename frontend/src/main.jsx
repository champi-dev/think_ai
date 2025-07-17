import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AutoVoiceDetector } from './components/AutoVoiceDetector';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <AutoVoiceDetector />
  </React.StrictMode>
);