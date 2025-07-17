import { describe, test, expect } from 'vitest';
import { translations, getTranslation, detectLanguage, setLanguage } from './translations';

describe('Translations', () => {
  describe('translations object', () => {
    test('contains all required languages', () => {
      const expectedLanguages = ['en', 'es', 'fr', 'de', 'pt', 'it', 'zh', 'ja', 'ko', 'ru', 'ar', 'hi'];
      expectedLanguages.forEach(lang => {
        expect(translations).toHaveProperty(lang);
      });
    });

    test('all languages have convertingToAudio translation', () => {
      Object.keys(translations).forEach(lang => {
        expect(translations[lang]).toHaveProperty('convertingToAudio');
        expect(translations[lang].convertingToAudio).toBeTruthy();
      });
    });

    test('all languages have all required keys', () => {
      const requiredKeys = [
        'tapToSpeak', 'listening', 'processing', 'transcribing', 
        'thinking', 'speaking', 'convertingToAudio', 'micPermissionNeeded',
        'noSpeechDetected', 'errorOccurred', 'errorPlaying'
      ];
      
      Object.keys(translations).forEach(lang => {
        requiredKeys.forEach(key => {
          expect(translations[lang]).toHaveProperty(key);
          expect(translations[lang][key]).toBeTruthy();
        });
      });
    });

    test('convertingToAudio translations are correct', () => {
      expect(translations.en.convertingToAudio).toBe('Converting to audio...');
      expect(translations.es.convertingToAudio).toBe('Convirtiendo a audio...');
      expect(translations.fr.convertingToAudio).toBe('Conversion en audio...');
      expect(translations.de.convertingToAudio).toBe('Konvertiere zu Audio...');
      expect(translations.pt.convertingToAudio).toBe('Convertendo para áudio...');
      expect(translations.it.convertingToAudio).toBe('Conversione in audio...');
      expect(translations.zh.convertingToAudio).toBe('转换为音频中...');
      expect(translations.ja.convertingToAudio).toBe('音声に変換中...');
      expect(translations.ko.convertingToAudio).toBe('오디오로 변환 중...');
      expect(translations.ru.convertingToAudio).toBe('Преобразование в аудио...');
      expect(translations.ar.convertingToAudio).toBe('تحويل إلى صوت...');
      expect(translations.hi.convertingToAudio).toBe('ऑडियो में परिवर्तित हो रहा है...');
    });
  });

  describe('getTranslation', () => {
    test('returns correct translation for valid language and key', () => {
      expect(getTranslation('speaking', 'es')).toBe('Hablando...');
      expect(getTranslation('convertingToAudio', 'fr')).toBe('Conversion en audio...');
    });

    test('falls back to English for missing language', () => {
      expect(getTranslation('speaking', 'invalid')).toBe('Speaking...');
    });

    test('returns key for missing translation key', () => {
      expect(getTranslation('nonexistentKey', 'en')).toBe('nonexistentKey');
    });
  });

  describe('setLanguage', () => {
    beforeEach(() => {
      localStorage.clear();
    });

    test('sets valid language in localStorage', () => {
      const result = setLanguage('es');
      expect(result).toBe(true);
      expect(localStorage.getItem('think_ai_language')).toBe('es');
    });

    test('returns false for invalid language', () => {
      const result = setLanguage('invalid');
      expect(result).toBe(false);
      expect(localStorage.getItem('think_ai_language')).toBeNull();
    });
  });

  describe('detectLanguage', () => {
    beforeEach(() => {
      localStorage.clear();
      global.fetch = vi.fn();
    });

    test('returns saved language from localStorage', async () => {
      localStorage.setItem('think_ai_language', 'es');
      const lang = await detectLanguage();
      expect(lang).toBe('es');
      expect(global.fetch).not.toHaveBeenCalled();
    });

    test('detects language from API', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ language: 'fr' })
      });
      
      const lang = await detectLanguage();
      expect(lang).toBe('fr');
      expect(localStorage.getItem('think_ai_language')).toBe('fr');
    });

    test('falls back to browser language on API failure', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      Object.defineProperty(navigator, 'language', {
        value: 'de-DE',
        configurable: true
      });
      
      const lang = await detectLanguage();
      expect(lang).toBe('de');
      expect(localStorage.getItem('think_ai_language')).toBe('de');
    });

    test('defaults to English for unsupported language', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      Object.defineProperty(navigator, 'language', {
        value: 'unsupported-LANG',
        configurable: true
      });
      
      const lang = await detectLanguage();
      expect(lang).toBe('en');
      expect(localStorage.getItem('think_ai_language')).toBe('en');
    });
  });
});