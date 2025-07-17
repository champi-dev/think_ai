import React, { useState, useRef, useEffect, useCallback } from 'react';
import './AutoVoiceDetector.css';
import { getTranslation, detectLanguage } from '../i18n/translations';

export const AutoVoiceDetector = () => {
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [audioLevel, setAudioLevel] = useState(0);
  const [userLang, setUserLang] = useState('en');
  
  // Debug log
  console.log('AutoVoiceDetector component mounted');
  
  // Refs for audio processing
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const monitoringStreamRef = useRef(null);
  const recordingStreamRef = useRef(null);
  const silenceTimeoutRef = useRef(null);
  const voiceDetectionTimeoutRef = useRef(null);
  const isRecordingRef = useRef(false);
  const animationFrameRef = useRef(null);
  
  // Configuration
  const VOICE_THRESHOLD = 0.08; // 8% - threshold for voice detection
  const SILENCE_THRESHOLD = 0.05; // 5% - threshold for silence detection
  const VOICE_DETECTION_TIME = 300; // ms - time voice must be present to start recording
  const SILENCE_TIMEOUT = 2000; // ms - time of silence before stopping
  
  // Initialize language on component mount
  useEffect(() => {
    const initLanguage = async () => {
      const detectedLang = await detectLanguage();
      setUserLang(detectedLang);
      setStatusMessage(getTranslation('readyToListen', detectedLang) || 'Ready to listen');
    };
    initLanguage();
  }, []);

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
        body: JSON.stringify({ 
          text,
          language: userLang 
        })
      });

      if (!response.ok) {
        throw new Error(`Synthesis error: ${response.status}`);
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      // Stop monitoring while playing response
      if (isMonitoring) {
        await stopMonitoring();
      }
      
      audio.play();
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
        setStatusMessage(getTranslation('readyToListen', userLang) || 'Ready to listen');
        setIsLoading(false);
        // Resume monitoring after response
        startMonitoring();
      };
    } catch (error) {
      console.error('Audio synthesis error:', error);
      setStatusMessage(getTranslation('errorPlaying', userLang) || 'Error playing audio');
      setIsLoading(false);
    }
  };

  const sendAudioForTranscription = async (audioBlob) => {
    setIsLoading(true);
    setStatusMessage(getTranslation('transcribing', userLang) || 'Transcribing...');
    
    try {
      const response = await fetch('/api/audio/transcribe', {
        method: 'POST',
        body: audioBlob,
        headers: { 
          'Content-Type': audioBlob.type,
          'X-Language': userLang 
        }
      });

      if (!response.ok) throw new Error(`Transcription error: ${response.status}`);

      const result = await response.json();
      if (result.text) {
        setStatusMessage(getTranslation('thinking', userLang) || 'Thinking...');
        const chatResponse = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: result.text,
            session_id: getSessionId(),
            mode: 'general',
            use_web_search: true,
            fact_check: true,
            language: userLang
          })
        });

        if (!chatResponse.ok) throw new Error(`API Error: ${chatResponse.status}`);
        
        const data = await chatResponse.json();
        setStatusMessage(getTranslation('speaking', userLang) || 'Speaking...');
        await playAudioResponse(data.response);

      } else {
        setStatusMessage(getTranslation('noSpeechDetected', userLang) || 'No speech detected');
        setIsLoading(false);
        // Resume monitoring
        setTimeout(() => startMonitoring(), 1000);
      }
    } catch (error) {
      console.error('Error in voice interaction:', error);
      setStatusMessage(getTranslation('errorOccurred', userLang) || 'Error occurred');
      setIsLoading(false);
      // Resume monitoring after error
      setTimeout(() => startMonitoring(), 2000);
    }
  };

  const analyzeAudioLevel = useCallback(() => {
    if (!analyserRef.current) return;
    
    const analyser = analyserRef.current;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyser.getByteFrequencyData(dataArray);
    
    // Calculate average volume
    const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
    const normalizedVolume = average / 255; // Normalize to 0-1
    
    // Update visual indicator
    setAudioLevel(normalizedVolume);
    
    // Voice detection logic when monitoring
    if (isMonitoring && !isRecordingRef.current) {
      if (normalizedVolume > VOICE_THRESHOLD) {
        // Voice detected above threshold
        if (!voiceDetectionTimeoutRef.current) {
          console.log('Voice detected, waiting for sustained speech...');
          voiceDetectionTimeoutRef.current = setTimeout(() => {
            console.log('Starting recording - sustained voice detected');
            startRecording();
          }, VOICE_DETECTION_TIME);
        }
      } else {
        // Voice below threshold, cancel pending start
        if (voiceDetectionTimeoutRef.current) {
          clearTimeout(voiceDetectionTimeoutRef.current);
          voiceDetectionTimeoutRef.current = null;
        }
      }
    }
    
    // Silence detection logic when recording
    if (isRecordingRef.current) {
      const isSilent = normalizedVolume < SILENCE_THRESHOLD;
      
      if (isSilent) {
        // Start or continue silence timer
        if (!silenceTimeoutRef.current) {
          console.log('Silence detected, starting timer...');
          silenceTimeoutRef.current = setTimeout(() => {
            console.log('Auto-stopping after silence');
            stopRecording();
          }, SILENCE_TIMEOUT);
        }
      } else {
        // Reset silence timer if sound detected
        if (silenceTimeoutRef.current) {
          clearTimeout(silenceTimeoutRef.current);
          silenceTimeoutRef.current = null;
        }
      }
    }
    
    // Continue monitoring
    if (isMonitoring || isRecordingRef.current) {
      animationFrameRef.current = requestAnimationFrame(analyzeAudioLevel);
    }
  }, [isMonitoring]);

  const startMonitoring = async () => {
    if (isMonitoring || isRecording) return;
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });
      
      monitoringStreamRef.current = stream;
      
      // Set up audio analysis
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      analyserRef.current.smoothingTimeConstant = 0.8;
      
      setIsMonitoring(true);
      setStatusMessage(getTranslation('listeningForVoice', userLang) || 'Listening for voice...');
      
      // Start continuous audio analysis
      analyzeAudioLevel();
    } catch (error) {
      console.error('Error starting monitoring:', error);
      setStatusMessage(getTranslation('micPermissionNeeded', userLang) || 'Microphone permission needed');
    }
  };

  const stopMonitoring = async () => {
    setIsMonitoring(false);
    
    // Cancel any pending voice detection
    if (voiceDetectionTimeoutRef.current) {
      clearTimeout(voiceDetectionTimeoutRef.current);
      voiceDetectionTimeoutRef.current = null;
    }
    
    // Stop animation frame
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    
    // Clean up monitoring stream
    if (monitoringStreamRef.current) {
      monitoringStreamRef.current.getTracks().forEach(track => track.stop());
      monitoringStreamRef.current = null;
    }
    
    // Close audio context if not recording
    if (!isRecordingRef.current && audioContextRef.current) {
      await audioContextRef.current.close();
      audioContextRef.current = null;
      analyserRef.current = null;
    }
    
    setAudioLevel(0);
  };

  const startRecording = async () => {
    // Stop monitoring first
    await stopMonitoring();
    
    try {
      // Use existing stream or create new one
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });
      
      recordingStreamRef.current = stream;
      
      // Set up audio analysis if not already set up
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
        analyserRef.current = audioContextRef.current.createAnalyser();
        const source = audioContextRef.current.createMediaStreamSource(stream);
        source.connect(analyserRef.current);
        analyserRef.current.fftSize = 256;
        analyserRef.current.smoothingTimeConstant = 0.8;
      }
      
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
        
        // Clean up recording stream
        if (recordingStreamRef.current) {
          recordingStreamRef.current.getTracks().forEach(track => track.stop());
          recordingStreamRef.current = null;
        }
        
        // Clean up audio context
        if (audioContextRef.current) {
          await audioContextRef.current.close();
          audioContextRef.current = null;
          analyserRef.current = null;
        }
        
        // Clear timeouts
        if (silenceTimeoutRef.current) {
          clearTimeout(silenceTimeoutRef.current);
          silenceTimeoutRef.current = null;
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
      isRecordingRef.current = true;
      setStatusMessage(getTranslation('recording', userLang) || 'Recording...');
      
      // Resume audio level analysis
      analyzeAudioLevel();
    } catch (error) {
      console.error('Error starting recording:', error);
      setStatusMessage(getTranslation('errorOccurred', userLang) || 'Error occurred');
      // Try to resume monitoring
      setTimeout(() => startMonitoring(), 1000);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      isRecordingRef.current = false;
      setStatusMessage(getTranslation('processing', userLang) || 'Processing...');
      
      // Cancel animation frame
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      
      setAudioLevel(0);
    }
  };

  const toggleAutoDetection = () => {
    if (isMonitoring) {
      stopMonitoring();
      setStatusMessage(getTranslation('autoDetectionOff', userLang) || 'Auto-detection off');
    } else {
      startMonitoring();
    }
  };

  // Auto-start monitoring on mount
  useEffect(() => {
    // Wait a bit for component to fully initialize
    const timer = setTimeout(() => {
      console.log('Auto-starting voice monitoring...');
      startMonitoring();
    }, 1500);
    
    return () => clearTimeout(timer);
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (silenceTimeoutRef.current) clearTimeout(silenceTimeoutRef.current);
      if (voiceDetectionTimeoutRef.current) clearTimeout(voiceDetectionTimeoutRef.current);
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      if (monitoringStreamRef.current) {
        monitoringStreamRef.current.getTracks().forEach(track => track.stop());
      }
      if (recordingStreamRef.current) {
        recordingStreamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        audioContextRef.current.close();
      }
    };
  }, []);

  return (
    <div className="auto-voice-detector">
      <div className="detector-container">
        <button 
          className={`toggle-button ${isMonitoring ? 'active' : ''} ${isLoading ? 'disabled' : ''}`}
          onClick={toggleAutoDetection}
          disabled={isLoading}
        >
          <span className="icon">{isMonitoring ? '👂' : '🔇'}</span>
          <span className="label">
            {isMonitoring ? 'Auto-Detection ON' : 'Auto-Detection OFF'}
          </span>
        </button>
        
        <div className="status-display">
          <div className="status-text">{statusMessage}</div>
          <div className="audio-level-container">
            <div 
              className="audio-level-bar"
              style={{ 
                width: `${audioLevel * 100}%`,
                backgroundColor: isRecording ? '#ff4444' : 
                               audioLevel > VOICE_THRESHOLD ? '#44ff44' : '#4444ff'
              }}
            />
            <div 
              className="voice-threshold-line"
              style={{ left: `${VOICE_THRESHOLD * 100}%` }}
              title="Voice detection threshold"
            />
          </div>
        </div>
        
        <div className={`recording-indicator ${isRecording ? 'active' : ''}`}>
          <span className="rec-dot"></span>
          <span className="rec-text">REC</span>
        </div>
      </div>
    </div>
  );
};