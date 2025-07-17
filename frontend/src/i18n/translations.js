export const translations = {
  en: {
    tapToSpeak: 'Tap to Speak',
    listening: 'Listening...',
    processing: 'Processing...',
    transcribing: 'Transcribing...',
    thinking: 'Thinking...',
    speaking: 'Speaking...',
    micPermissionNeeded: 'Mic permission needed.',
    noSpeechDetected: 'No speech detected.',
    errorOccurred: 'An error occurred.',
    errorPlaying: 'Error playing response.'
  },
  es: {
    tapToSpeak: 'Toca para Hablar',
    listening: 'Escuchando...',
    processing: 'Procesando...',
    transcribing: 'Transcribiendo...',
    thinking: 'Pensando...',
    speaking: 'Hablando...',
    micPermissionNeeded: 'Se necesita permiso del micrófono.',
    noSpeechDetected: 'No se detectó voz.',
    errorOccurred: 'Ocurrió un error.',
    errorPlaying: 'Error al reproducir respuesta.'
  },
  fr: {
    tapToSpeak: 'Appuyez pour Parler',
    listening: 'Écoute...',
    processing: 'Traitement...',
    transcribing: 'Transcription...',
    thinking: 'Réflexion...',
    speaking: 'Parle...',
    micPermissionNeeded: 'Permission du micro nécessaire.',
    noSpeechDetected: 'Aucune parole détectée.',
    errorOccurred: 'Une erreur s\'est produite.',
    errorPlaying: 'Erreur lors de la lecture.'
  },
  de: {
    tapToSpeak: 'Zum Sprechen tippen',
    listening: 'Höre zu...',
    processing: 'Verarbeitung...',
    transcribing: 'Transkribieren...',
    thinking: 'Denke nach...',
    speaking: 'Spreche...',
    micPermissionNeeded: 'Mikrofonberechtigung erforderlich.',
    noSpeechDetected: 'Keine Sprache erkannt.',
    errorOccurred: 'Ein Fehler ist aufgetreten.',
    errorPlaying: 'Fehler beim Abspielen.'
  },
  pt: {
    tapToSpeak: 'Toque para Falar',
    listening: 'Ouvindo...',
    processing: 'Processando...',
    transcribing: 'Transcrevendo...',
    thinking: 'Pensando...',
    speaking: 'Falando...',
    micPermissionNeeded: 'Permissão do microfone necessária.',
    noSpeechDetected: 'Nenhuma fala detectada.',
    errorOccurred: 'Ocorreu um erro.',
    errorPlaying: 'Erro ao reproduzir resposta.'
  },
  it: {
    tapToSpeak: 'Tocca per Parlare',
    listening: 'Ascolto...',
    processing: 'Elaborazione...',
    transcribing: 'Trascrizione...',
    thinking: 'Sto pensando...',
    speaking: 'Parlo...',
    micPermissionNeeded: 'Permesso microfono necessario.',
    noSpeechDetected: 'Nessun parlato rilevato.',
    errorOccurred: 'Si è verificato un errore.',
    errorPlaying: 'Errore nella riproduzione.'
  },
  zh: {
    tapToSpeak: '点击说话',
    listening: '正在听...',
    processing: '处理中...',
    transcribing: '转录中...',
    thinking: '思考中...',
    speaking: '说话中...',
    micPermissionNeeded: '需要麦克风权限',
    noSpeechDetected: '未检测到语音',
    errorOccurred: '发生错误',
    errorPlaying: '播放错误'
  },
  ja: {
    tapToSpeak: 'タップして話す',
    listening: '聞いています...',
    processing: '処理中...',
    transcribing: '文字起こし中...',
    thinking: '考えています...',
    speaking: '話しています...',
    micPermissionNeeded: 'マイクの許可が必要です',
    noSpeechDetected: '音声が検出されませんでした',
    errorOccurred: 'エラーが発生しました',
    errorPlaying: '再生エラー'
  },
  ko: {
    tapToSpeak: '탭하여 말하기',
    listening: '듣는 중...',
    processing: '처리 중...',
    transcribing: '전사 중...',
    thinking: '생각 중...',
    speaking: '말하는 중...',
    micPermissionNeeded: '마이크 권한이 필요합니다',
    noSpeechDetected: '음성이 감지되지 않았습니다',
    errorOccurred: '오류가 발생했습니다',
    errorPlaying: '재생 오류'
  },
  ru: {
    tapToSpeak: 'Нажмите, чтобы говорить',
    listening: 'Слушаю...',
    processing: 'Обработка...',
    transcribing: 'Транскрибирование...',
    thinking: 'Думаю...',
    speaking: 'Говорю...',
    micPermissionNeeded: 'Нужно разрешение микрофона',
    noSpeechDetected: 'Речь не обнаружена',
    errorOccurred: 'Произошла ошибка',
    errorPlaying: 'Ошибка воспроизведения'
  },
  ar: {
    tapToSpeak: 'اضغط للتحدث',
    listening: 'أستمع...',
    processing: 'معالجة...',
    transcribing: 'نسخ...',
    thinking: 'أفكر...',
    speaking: 'أتحدث...',
    micPermissionNeeded: 'مطلوب إذن الميكروفون',
    noSpeechDetected: 'لم يتم اكتشاف كلام',
    errorOccurred: 'حدث خطأ',
    errorPlaying: 'خطأ في التشغيل'
  },
  hi: {
    tapToSpeak: 'बोलने के लिए टैप करें',
    listening: 'सुन रहा हूं...',
    processing: 'प्रसंस्करण...',
    transcribing: 'लिप्यंतरण...',
    thinking: 'सोच रहा हूं...',
    speaking: 'बोल रहा हूं...',
    micPermissionNeeded: 'माइक अनुमति चाहिए',
    noSpeechDetected: 'कोई भाषण नहीं मिला',
    errorOccurred: 'त्रुटि हुई',
    errorPlaying: 'प्लेबैक त्रुटि'
  }
};

export const detectLanguage = async () => {
  // Check localStorage for saved preference first
  const savedLang = localStorage.getItem('think_ai_language');
  if (savedLang && translations[savedLang]) {
    return savedLang;
  }
  
  // Try IP-based detection
  try {
    const response = await fetch('/api/detect-language');
    if (response.ok) {
      const data = await response.json();
      if (data.language && translations[data.language]) {
        // Save the detected language
        localStorage.setItem('think_ai_language', data.language);
        return data.language;
      }
    }
  } catch (error) {
    console.log('IP-based language detection failed, falling back to browser language');
  }
  
  // Fall back to browser language
  const browserLang = navigator.language || navigator.userLanguage;
  const langCode = browserLang.split('-')[0];
  
  // Check if we support this language
  if (translations[langCode]) {
    localStorage.setItem('think_ai_language', langCode);
    return langCode;
  }
  
  // Default to English
  localStorage.setItem('think_ai_language', 'en');
  return 'en';
};

export const setLanguage = (langCode) => {
  if (translations[langCode]) {
    localStorage.setItem('think_ai_language', langCode);
    return true;
  }
  return false;
};

export const getTranslation = (key, langCode = detectLanguage()) => {
  return translations[langCode]?.[key] || translations.en[key] || key;
};