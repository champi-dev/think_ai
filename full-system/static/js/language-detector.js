/**
 * Think AI Language Detector & Translator
 * Detects user's language from browser/IP and provides contextual translations
 */

class LanguageDetector {
    constructor() {
        this.currentLang = 'en';
        this.translations = {
            en: {
                // Header
                'app_title': 'Think AI',
                'api_docs': 'API Docs',
                'github': 'GitHub',
                'install_app': 'Install App',
                
                // AI Mode
                'ai_mode': 'AI Mode',
                'general': 'General',
                'code': 'Code',
                
                // Features
                'web_search': 'Web Search',
                'fact_check': 'Fact Check',
                
                // Chat Interface
                'type_message': 'Type your message here...',
                'send': 'Send',
                'thinking': 'Thinking...',
                'error_occurred': 'An error occurred',
                'try_again': 'Please try again',
                
                // Messages
                'welcome_message': 'Welcome to Think AI - Lightning fast responses with O(1) performance',
                'connection_error': 'Connection error. Please check your internet connection.',
                'session_expired': 'Session expired. Please refresh the page.',
                
                // PWA
                'install_prompt': 'Install Think AI for offline access',
                'installed_success': 'Think AI installed successfully!'
            },
            es: {
                // Spanish
                'app_title': 'Think AI',
                'api_docs': 'Documentación API',
                'github': 'GitHub',
                'install_app': 'Instalar App',
                'ai_mode': 'Modo IA',
                'general': 'General',
                'code': 'Código',
                'web_search': 'Búsqueda Web',
                'fact_check': 'Verificar Hechos',
                'type_message': 'Escribe tu mensaje aquí...',
                'send': 'Enviar',
                'thinking': 'Pensando...',
                'error_occurred': 'Ocurrió un error',
                'try_again': 'Por favor intenta de nuevo',
                'welcome_message': 'Bienvenido a Think AI - Respuestas ultrarrápidas con rendimiento O(1)',
                'connection_error': 'Error de conexión. Por favor verifica tu conexión a internet.',
                'session_expired': 'Sesión expirada. Por favor recarga la página.',
                'install_prompt': 'Instala Think AI para acceso sin conexión',
                'installed_success': '¡Think AI instalado exitosamente!'
            },
            pt: {
                // Portuguese
                'app_title': 'Think AI',
                'api_docs': 'Documentação API',
                'github': 'GitHub',
                'install_app': 'Instalar App',
                'ai_mode': 'Modo IA',
                'general': 'Geral',
                'code': 'Código',
                'web_search': 'Busca Web',
                'fact_check': 'Verificar Fatos',
                'type_message': 'Digite sua mensagem aqui...',
                'send': 'Enviar',
                'thinking': 'Pensando...',
                'error_occurred': 'Ocorreu um erro',
                'try_again': 'Por favor tente novamente',
                'welcome_message': 'Bem-vindo ao Think AI - Respostas ultrarrápidas com desempenho O(1)',
                'connection_error': 'Erro de conexão. Por favor verifique sua conexão com a internet.',
                'session_expired': 'Sessão expirada. Por favor recarregue a página.',
                'install_prompt': 'Instale o Think AI para acesso offline',
                'installed_success': 'Think AI instalado com sucesso!'
            },
            fr: {
                // French
                'app_title': 'Think AI',
                'api_docs': 'Documentation API',
                'github': 'GitHub',
                'install_app': 'Installer l\'App',
                'ai_mode': 'Mode IA',
                'general': 'Général',
                'code': 'Code',
                'web_search': 'Recherche Web',
                'fact_check': 'Vérifier les Faits',
                'type_message': 'Tapez votre message ici...',
                'send': 'Envoyer',
                'thinking': 'Réflexion...',
                'error_occurred': 'Une erreur s\'est produite',
                'try_again': 'Veuillez réessayer',
                'welcome_message': 'Bienvenue sur Think AI - Réponses ultra-rapides avec performance O(1)',
                'connection_error': 'Erreur de connexion. Veuillez vérifier votre connexion internet.',
                'session_expired': 'Session expirée. Veuillez recharger la page.',
                'install_prompt': 'Installez Think AI pour un accès hors ligne',
                'installed_success': 'Think AI installé avec succès!'
            },
            de: {
                // German
                'app_title': 'Think AI',
                'api_docs': 'API-Dokumentation',
                'github': 'GitHub',
                'install_app': 'App Installieren',
                'ai_mode': 'KI-Modus',
                'general': 'Allgemein',
                'code': 'Code',
                'web_search': 'Web-Suche',
                'fact_check': 'Fakten Prüfen',
                'type_message': 'Geben Sie Ihre Nachricht hier ein...',
                'send': 'Senden',
                'thinking': 'Denke nach...',
                'error_occurred': 'Ein Fehler ist aufgetreten',
                'try_again': 'Bitte versuchen Sie es erneut',
                'welcome_message': 'Willkommen bei Think AI - Blitzschnelle Antworten mit O(1) Leistung',
                'connection_error': 'Verbindungsfehler. Bitte überprüfen Sie Ihre Internetverbindung.',
                'session_expired': 'Sitzung abgelaufen. Bitte laden Sie die Seite neu.',
                'install_prompt': 'Installieren Sie Think AI für Offline-Zugriff',
                'installed_success': 'Think AI erfolgreich installiert!'
            },
            zh: {
                // Chinese
                'app_title': 'Think AI',
                'api_docs': 'API 文档',
                'github': 'GitHub',
                'install_app': '安装应用',
                'ai_mode': 'AI 模式',
                'general': '通用',
                'code': '代码',
                'web_search': '网络搜索',
                'fact_check': '事实核查',
                'type_message': '在此输入您的消息...',
                'send': '发送',
                'thinking': '思考中...',
                'error_occurred': '发生错误',
                'try_again': '请重试',
                'welcome_message': '欢迎使用 Think AI - O(1) 性能的超快响应',
                'connection_error': '连接错误。请检查您的网络连接。',
                'session_expired': '会话已过期。请刷新页面。',
                'install_prompt': '安装 Think AI 以进行离线访问',
                'installed_success': 'Think AI 安装成功！'
            },
            ja: {
                // Japanese
                'app_title': 'Think AI',
                'api_docs': 'API ドキュメント',
                'github': 'GitHub',
                'install_app': 'アプリをインストール',
                'ai_mode': 'AI モード',
                'general': '一般',
                'code': 'コード',
                'web_search': 'ウェブ検索',
                'fact_check': 'ファクトチェック',
                'type_message': 'メッセージを入力してください...',
                'send': '送信',
                'thinking': '考え中...',
                'error_occurred': 'エラーが発生しました',
                'try_again': 'もう一度お試しください',
                'welcome_message': 'Think AI へようこそ - O(1) パフォーマンスの超高速レスポンス',
                'connection_error': '接続エラー。インターネット接続を確認してください。',
                'session_expired': 'セッションの有効期限が切れました。ページを更新してください。',
                'install_prompt': 'オフラインアクセスのために Think AI をインストール',
                'installed_success': 'Think AI のインストールに成功しました！'
            },
            ko: {
                // Korean
                'app_title': 'Think AI',
                'api_docs': 'API 문서',
                'github': 'GitHub',
                'install_app': '앱 설치',
                'ai_mode': 'AI 모드',
                'general': '일반',
                'code': '코드',
                'web_search': '웹 검색',
                'fact_check': '사실 확인',
                'type_message': '메시지를 입력하세요...',
                'send': '전송',
                'thinking': '생각 중...',
                'error_occurred': '오류가 발생했습니다',
                'try_again': '다시 시도해주세요',
                'welcome_message': 'Think AI에 오신 것을 환영합니다 - O(1) 성능의 초고속 응답',
                'connection_error': '연결 오류. 인터넷 연결을 확인해주세요.',
                'session_expired': '세션이 만료되었습니다. 페이지를 새로고침해주세요.',
                'install_prompt': '오프라인 액세스를 위해 Think AI 설치',
                'installed_success': 'Think AI가 성공적으로 설치되었습니다!'
            }
        };
    }
    
    async detectLanguage() {
        // First try browser language
        const browserLang = navigator.language || navigator.userLanguage;
        const langCode = browserLang.split('-')[0];
        
        if (this.translations[langCode]) {
            this.currentLang = langCode;
        } else {
            // Try to detect from IP using a free geolocation service
            try {
                const response = await fetch('https://ipapi.co/json/');
                const data = await response.json();
                const countryToLang = {
                    'US': 'en', 'GB': 'en', 'AU': 'en', 'CA': 'en',
                    'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es',
                    'BR': 'pt', 'PT': 'pt',
                    'FR': 'fr', 'BE': 'fr',
                    'DE': 'de', 'AT': 'de', 'CH': 'de',
                    'CN': 'zh', 'TW': 'zh', 'HK': 'zh',
                    'JP': 'ja',
                    'KR': 'ko'
                };
                const detectedLang = countryToLang[data.country_code] || 'en';
                if (this.translations[detectedLang]) {
                    this.currentLang = detectedLang;
                }
            } catch (error) {
                console.log('Language detection failed, using English');
            }
        }
        
        // Save preference
        localStorage.setItem('preferredLanguage', this.currentLang);
        return this.currentLang;
    }
    
    setLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('preferredLanguage', lang);
            this.updatePageTranslations();
        }
    }
    
    t(key) {
        return this.translations[this.currentLang][key] || this.translations['en'][key] || key;
    }
    
    updatePageTranslations() {
        // Update all elements with data-translate attribute
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // Update page title
        document.title = this.t('app_title');
    }
    
    createLanguageSelector() {
        const selector = document.createElement('select');
        selector.className = 'language-selector';
        selector.innerHTML = `
            <option value="en">🇬🇧 English</option>
            <option value="es">🇪🇸 Español</option>
            <option value="pt">🇵🇹 Português</option>
            <option value="fr">🇫🇷 Français</option>
            <option value="de">🇩🇪 Deutsch</option>
            <option value="zh">🇨🇳 中文</option>
            <option value="ja">🇯🇵 日本語</option>
            <option value="ko">🇰🇷 한국어</option>
        `;
        selector.value = this.currentLang;
        selector.addEventListener('change', (e) => this.setLanguage(e.target.value));
        return selector;
    }
}

// Initialize language detector
const langDetector = new LanguageDetector();

// Export for use in other scripts
window.LanguageDetector = langDetector;