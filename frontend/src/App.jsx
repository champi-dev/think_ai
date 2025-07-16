import React, { useEffect, useRef, useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isCodeMode, setIsCodeMode] = useState(false);
  const [useWebSearch, setUseWebSearch] = useState(false);
  const [useFactCheck, setUseFactCheck] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [audioPlayback, setAudioPlayback] = useState({});
  const [usedMic, setUsedMic] = useState(false); // Track if mic was used for auto-play
  const [isTyping, setIsTyping] = useState(false); // Track if user is typing
  const messagesEndRef = useRef(null);
  const canvasRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  
  // Session management
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
  
  const [sessionId] = useState(getSessionId());

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Initialize canvas animation
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Quantum field animation
    const fieldPoints = [];
    const fieldDensity = 16;
    const time = { value: 0 };
    
    const SIN_TABLE_SIZE = 1024;
    const sinTable = new Float32Array(SIN_TABLE_SIZE);
    const cosTable = new Float32Array(SIN_TABLE_SIZE);
    
    for (let i = 0; i < SIN_TABLE_SIZE; i++) {
      const angle = (i / SIN_TABLE_SIZE) * Math.PI * 2;
      sinTable[i] = Math.sin(angle);
      cosTable[i] = Math.cos(angle);
    }
    
    function fastSin(x) {
      const index = Math.floor((x / (Math.PI * 2)) * SIN_TABLE_SIZE) & (SIN_TABLE_SIZE - 1);
      return sinTable[index];
    }
    
    function fastCos(x) {
      const index = Math.floor((x / (Math.PI * 2)) * SIN_TABLE_SIZE) & (SIN_TABLE_SIZE - 1);
      return cosTable[index];
    }
    
    class OptimizedQuantumPoint {
      constructor(x, y, index) {
        this.baseX = x;
        this.baseY = y;
        this.x = x;
        this.y = y;
        this.index = index;
        this.phaseOffset = (index * 0.618) % (Math.PI * 2);
        this.amplitudeScale = 0.8 + (index % 3) * 0.4;
        this.frequencyMult = 1 + (index % 5) * 0.2;
        this.radiusBase = 2 + (index % 4);
      }
      
      update(t) {
        const timeIndex = (t * 0.001 + this.phaseOffset);
        const waveX = fastSin(timeIndex * this.frequencyMult) * 25 * this.amplitudeScale;
        const waveY = fastCos(timeIndex * this.frequencyMult) * 25 * this.amplitudeScale;
        this.x = this.baseX + waveX;
        this.y = this.baseY + waveY;
        this.energy = (fastSin(timeIndex * 2) + 1) * 0.5;
      }
      
      draw() {
        const size = this.radiusBase + this.energy * 3;
        const alpha = 0.3 + this.energy * 0.4;
        ctx.save();
        ctx.globalAlpha = alpha;
        const hue = 240 + this.energy * 60;
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, size * 8);
        gradient.addColorStop(0, `hsl(${hue}, 80%, 70%)`);
        gradient.addColorStop(0.7, `hsl(${hue + 30}, 70%, 60%)`);
        gradient.addColorStop(1, `hsl(${hue}, 60%, 50%)`);
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, size * 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = alpha + 0.3;
        ctx.fillStyle = `hsl(${hue}, 90%, 80%)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }
    
    function initializeQuantumField() {
      fieldPoints.length = 0;
      const spacingX = canvas.width / fieldDensity;
      const spacingY = canvas.height / fieldDensity;
      let index = 0;
      for (let x = 0; x < fieldDensity; x++) {
        for (let y = 0; y < fieldDensity; y++) {
          const pointX = x * spacingX + spacingX / 2;
          const pointY = y * spacingY + spacingY / 2;
          fieldPoints.push(new OptimizedQuantumPoint(pointX, pointY, index++));
        }
      }
    }
    
    initializeQuantumField();
    
    function animate() {
      ctx.fillStyle = 'rgba(0, 0, 12, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      time.value += 3;
      fieldPoints.forEach(point => {
        point.update(time.value);
        point.draw();
      });
      requestAnimationFrame(animate);
    }
    
    animate();
    
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initializeQuantumField();
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Load saved preferences
  useEffect(() => {
    const savedMode = localStorage.getItem('think_ai_code_mode') === 'true';
    const savedWebSearch = localStorage.getItem('think_ai_web_search') === 'true';
    const savedFactCheck = localStorage.getItem('think_ai_fact_check') === 'true';
    
    setIsCodeMode(savedMode);
    setUseWebSearch(savedWebSearch);
    setUseFactCheck(savedFactCheck);
  }, []);

  const handleModeToggle = () => {
    const newMode = !isCodeMode;
    setIsCodeMode(newMode);
    localStorage.setItem('think_ai_code_mode', newMode);
  };

  const handleWebSearchToggle = () => {
    const newValue = !useWebSearch;
    setUseWebSearch(newValue);
    localStorage.setItem('think_ai_web_search', newValue);
  };

  const handleFactCheckToggle = () => {
    const newValue = !useFactCheck;
    setUseFactCheck(newValue);
    localStorage.setItem('think_ai_fact_check', newValue);
  };

  const parseMarkdown = (text) => {
    // Simple markdown parser
    let result = text;
    
    // Code blocks
    result = result.replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');
    
    // Inline code
    result = result.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Headers
    result = result.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    result = result.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    result = result.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Bold
    result = result.replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>');
    
    // Italic
    result = result.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
    
    // Links
    result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    
    // Line breaks
    result = result.replace(/\n/g, '<br>');
    
    return result;
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    const userMessage = inputValue.trim();
    setInputValue('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          session_id: sessionId,
          mode: isCodeMode ? 'code' : 'general',
          use_web_search: useWebSearch,
          fact_check: useFactCheck
        })
      });
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }
      
      const data = await response.json();
      const newMessageIndex = messages.length + 1; // Index for the new AI message
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: data.response,
        indicators: {
          webSearch: data.used_web_search || false,
          factChecked: data.fact_checked || false
        }
      }]);
      
      // Auto-play response if mic was used and user isn't typing
      if (usedMic && !isTyping) {
        setTimeout(() => {
          playAudioMessage(data.response, newMessageIndex);
        }, 500); // Small delay to ensure message is rendered
      }
      
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: 'Sorry, I encountered an error. Please check if the server is running.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyMessage = async (content) => {
    try {
      await navigator.clipboard.writeText(content);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Audio recording functions
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, { 
        mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg' 
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { 
          type: mediaRecorder.mimeType 
        });
        await sendAudioForTranscription(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      alert('Unable to access microphone. Please ensure microphone permissions are granted.');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };
  
  const sendAudioForTranscription = async (audioBlob) => {
    setIsLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob);
      
      const response = await fetch('/api/audio/transcribe', {
        method: 'POST',
        body: audioBlob,
        headers: {
          'Content-Type': audioBlob.type
        }
      });
      
      if (!response.ok) {
        throw new Error(`Transcription error: ${response.status}`);
      }
      
      const result = await response.json();
      if (result.text) {
        setInputValue(result.text);
        setUsedMic(true); // Mark that mic was used
        // Auto-send the message
        handleSendMessage();
      }
    } catch (error) {
      console.error('Transcription error:', error);
      alert('Failed to transcribe audio. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const toggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };
  
  // Text-to-speech function
  const playAudioMessage = async (content, messageIndex) => {
    try {
      const response = await fetch('/api/audio/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: content })
      });
      
      if (!response.ok) {
        throw new Error(`Synthesis error: ${response.status}`);
      }
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      // Track playback state
      setAudioPlayback(prev => ({ ...prev, [messageIndex]: 'playing' }));
      
      audio.onended = () => {
        setAudioPlayback(prev => ({ ...prev, [messageIndex]: 'stopped' }));
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.play();
    } catch (error) {
      console.error('Audio synthesis error:', error);
    }
  };

  return (
    <>
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">🧠</div>
            <span>Think AI</span>
          </div>
          
          <nav>
            <a href="/api-docs" style={{color: 'var(--text)', textDecoration: 'none'}}>API Docs</a>
            <a href="https://github.com/champi-dev/think_ai" target="_blank" rel="noopener noreferrer" style={{color: 'var(--text)', textDecoration: 'none'}}>GitHub</a>
          </nav>
          
          <div className="mode-controls">
            <div className="mode-toggle" onClick={handleModeToggle}>
              <span className="mode-label">AI Mode</span>
              <div className={`toggle-switch ${isCodeMode ? 'active' : ''}`}></div>
              <span className="mode-icon">{isCodeMode ? '💻' : '🤖'}</span>
              <span className="mode-label">{isCodeMode ? 'Code' : 'General'}</span>
            </div>
          </div>
        </div>
      </header>
      
      <canvas ref={canvasRef} id="canvas"></canvas>
      
      <div className="interface">
        <div className="chat-container">
          <div className="messages" id="messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.indicators?.webSearch && (
                  <div className="web-search-indicator">
                    <span className="icon">🔍</span> Web search results included
                  </div>
                )}
                {msg.indicators?.factChecked && (
                  <div className="fact-check-indicator">
                    <span className="icon">✅</span> Fact-checked response
                  </div>
                )}
                <div className="message-content">
                  {msg.role === 'user' ? (
                    msg.content
                  ) : (
                    <>
                      <div dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.content) }} />
                      <div className="message-actions">
                        <button className="copy-button" onClick={() => handleCopyMessage(msg.content)}>
                          <svg className="copy-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                          </svg>
                          <span>Copy</span>
                        </button>
                        <button 
                          className="audio-button"
                          onClick={() => playAudioMessage(msg.content, idx)}
                          disabled={audioPlayback[idx] === 'playing'}
                        >
                          <svg className="audio-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            {audioPlayback[idx] === 'playing' ? (
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            ) : (
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path>
                            )}
                          </svg>
                          <span>{audioPlayback[idx] === 'playing' ? 'Playing' : 'Play'}</span>
                        </button>
                      </div>
                    </>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message ai loading">
                <div className="message-content">Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="input-container">
            <div className="input-wrapper">
              <div className="input-features">
                <div 
                  className={`input-feature-toggle web-search ${useWebSearch ? 'active' : ''}`}
                  onClick={handleWebSearchToggle}
                >
                  <span>🔍</span>
                </div>
                <div 
                  className={`input-feature-toggle fact-check ${useFactCheck ? 'active' : ''}`}
                  onClick={handleFactCheckToggle}
                >
                  <span>✅</span>
                </div>
                <div 
                  className={`input-feature-toggle mic ${isRecording ? 'recording' : ''}`}
                  onClick={toggleRecording}
                >
                  <span>{isRecording ? '⏹️' : '🎤'}</span>
                </div>
              </div>
              
              <input 
                type="text" 
                id="queryInput" 
                placeholder={isCodeMode ? "Write code, debug, analyze, or ask coding questions..." : "Type your message here..."}
                autoComplete="off"
                value={inputValue}
                onChange={(e) => {
                  setInputValue(e.target.value);
                  setIsTyping(true);
                  setUsedMic(false); // Reset mic flag when user types
                }}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleSendMessage();
                    setIsTyping(false);
                  }
                }}
                onBlur={() => setIsTyping(false)}
                disabled={isLoading}
              />
              <button id="sendBtn" onClick={() => {
                handleSendMessage();
                setIsTyping(false);
              }} disabled={isLoading}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 2L11 13M22 2L15 22L11 13L2 9L22 2Z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;