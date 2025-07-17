
import React, { useState, useRef, useEffect } from 'react';
import './SmartwatchView.css';

export const SmartwatchView = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('Tap to Speak');
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const getUserId = () => {
    let userId = localStorage.getItem('think_ai_user_id');
    if (!userId) {
      userId = 'user_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
      localStorage.setItem('think_ai_user_id', userId);
    }
    return userId;
  };
  
  const getSessionId = () => {
    let sessionId = localStorage.getItem('think_ai_session_id');
    if (!sessionId) {
      const userId = getUserId();
      sessionId = userId + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('think_ai_session_id', sessionId);
    }
    return sessionId;
  };

  const playAudioResponse = async (text) => {
    try {
      const response = await fetch('/api/audio/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        throw new Error(`Synthesis error: ${response.status}`);
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      audio.onended = () => {
        setStatusMessage('Tap to Speak');
        setIsLoading(false);
      };
    } catch (error) {
      console.error('Audio synthesis error:', error);
      setStatusMessage('Error playing response.');
      setIsLoading(false);
    }
  };

  const sendAudioForTranscription = async (audioBlob) => {
    setIsLoading(true);
    setStatusMessage('Transcribing...');
    try {
      const response = await fetch('/api/audio/transcribe', {
        method: 'POST',
        body: audioBlob,
        headers: { 'Content-Type': audioBlob.type }
      });

      if (!response.ok) throw new Error(`Transcription error: ${response.status}`);

      const result = await response.json();
      if (result.text) {
        setStatusMessage('Thinking...');
        const chatResponse = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: result.text,
            session_id: getSessionId(),
            mode: 'general',
            use_web_search: true,
            fact_check: true
          })
        });

        if (!chatResponse.ok) throw new Error(`API Error: ${chatResponse.status}`);
        
        const data = await chatResponse.json();
        setStatusMessage('Speaking...');
        await playAudioResponse(data.response);

      } else {
        setStatusMessage('No speech detected.');
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Error in voice interaction:', error);
      setStatusMessage('An error occurred.');
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg'
      });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: mediaRecorder.mimeType });
        await sendAudioForTranscription(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
      setStatusMessage('Listening...');
    } catch (error) {
      console.error('Error starting recording:', error);
      setStatusMessage('Mic permission needed.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setStatusMessage('Processing...');
    }
  };

  const handleMicClick = () => {
    if (isLoading) return;
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="smartwatch-container" onClick={handleMicClick}>
      <div className="watch-face">
        <div
          className={`listening-indicator ${isRecording ? 'listening' : ''} ${isLoading ? 'loading' : ''}`}
        >
          {isLoading ? '🧠' : '🎤'}
        </div>
        <div className="status-message">{statusMessage}</div>
      </div>
    </div>
  );
};
