- ChatGPT Clone - Complete Project Specification
I'll create a comprehensive specification for your locally-hosted AI chat application with all the features you've requested.
Tech Stack
Frontend
Framework: React 18 with Vite
Styling: Tailwind CSS + shadcn/ui components
3D Graphics: Three.js with React Three Fiber
State Management: Zustand
Routing: React Router v6
HTTP Client: Axios
Markdown: React Markdown with syntax highlighting
File Handling: React Dropzone
Backend
Runtime: Node.js with Express.js
Database: SQLite with better-sqlite3 (lightweight, local)
File Storage: Local filesystem
Session Management: express-session
AI Models (via Ollama):
Main LLM: qwen3:1.7b
Vision: llava:7b (for image understanding)
Code: qwen3:1.7b (same model, efficient)
Text-to-Image: Stable Diffusion via stable-diffusion or use external API
Speech Services:
TTS: piper (local, fast) or Coqui TTS
STT: whisper.cpp via Ollama or Whisper model
Document Processing:
PDF: pdf-lib, pdf-parse
Word: mammoth, docxtemplater
Excel: xlsx (SheetJS)
API Documentation: Swagger/OpenAPI
DevOps
Tunneling: ngrok
Process Manager: PM2
Environment: dotenv

User Stories
Epic 1: Conversation Management
US-1.1: Create New Conversation
As a user
I want to start a new conversation
So that I can organize different topics separately
Acceptance Criteria:
Click "New Chat" button creates fresh conversation
New conversation appears in sidebar with default name "New Chat"
Previous conversation is auto-saved
Conversation automatically named based on first message
Maximum 100 conversations per user
US-1.2: View Conversation History
As a user
I want to see all my previous conversations
So that I can continue where I left off
Acceptance Criteria:
Sidebar shows all conversations sorted by last updated
Each conversation shows title and timestamp
Click on conversation loads full history
Search functionality filters conversations by title/content
Conversations persist after app restart
US-1.3: Delete Conversations
As a user
I want to remove conversations I no longer need
So that I can keep my workspace organized
Acceptance Criteria:
Delete button appears on conversation hover
Confirmation dialog prevents accidental deletion
Deleted conversations are permanently removed
Current conversation switches to most recent after deletion
US-1.4: Rename Conversations
As a user
I want to rename conversations
So that I can easily identify them
Acceptance Criteria:
Double-click conversation title to edit
Enter key saves new name
Escape key cancels editing
Name limited to 100 characters

Epic 2: Text Chat with AI
US-2.1: Send Text Messages
As a user
I want to send text messages to the AI
So that I can get responses to my questions
Acceptance Criteria:
Text input supports multiline (Shift+Enter for new line)
Enter key sends message
Send button visible and functional
Messages display in chronological order
Streaming response shows typing indicator
Character limit: 10,000 per message
US-2.2: Receive AI Responses
As a user
I want to see AI responses with proper formatting
So that I can easily read and understand the content
Acceptance Criteria:
Responses support markdown rendering
Code blocks have syntax highlighting
Copy button on code blocks
Responses stream in real-time (token by token)
LaTeX math rendering supported
Links are clickable and open in new tab
US-2.3: Regenerate Responses
As a user
I want to regenerate AI responses
So that I can get alternative answers
Acceptance Criteria:
Regenerate button appears on AI messages
Previous response is replaced with new one
Original response can be restored via "Show previous"
Maintains conversation context
US-2.4: Edit Messages
As a user
I want to edit my previous messages
So that I can correct mistakes or rephrase questions
Acceptance Criteria:
Edit button appears on user messages
Editing a message regenerates AI response
Message history branches at edit point
Can navigate between branches

Epic 3: Multimodal Capabilities
US-3.1: Upload and Analyze Images
As a user
I want to upload images for AI analysis
So that I can get insights about visual content
Acceptance Criteria:
Drag-and-drop image upload
Supports JPG, PNG, WebP, GIF formats
Max file size: 10MB
Image preview in chat
AI describes image content accurately
Multiple images per message (max 5)
US-3.2: Process PDF Documents
As a user
I want to upload PDFs for analysis
So that I can ask questions about document content
Acceptance Criteria:
PDF text extraction working
Preserves basic formatting
Max file size: 50MB
AI can answer questions about PDF content
Shows page numbers in references
Handles scanned PDFs with OCR
US-3.3: Process Word Documents
As a user
I want to upload Word docs (.docx)
So that I can analyze document content
Acceptance Criteria:
Extract text from .docx files
Preserve headings and structure
Max file size: 25MB
AI understands document structure
Tables extracted as text
US-3.4: Process Excel Spreadsheets
As a user
I want to upload Excel files
So that I can analyze data and get insights
Acceptance Criteria:
Parse .xlsx and .xls formats
Extract all sheets
Preserve cell values and formulas
AI can perform calculations
Max file size: 25MB
Handles up to 10,000 rows

Epic 4: Image Generation
US-4.1: Generate Images from Text
As a user
I want to create images from text descriptions
So that I can visualize concepts
Acceptance Criteria:
Command trigger: "/imagine [prompt]" or button
Supports detailed prompts (up to 500 chars)
Generation takes 10-60 seconds
Shows progress indicator
Image displays in chat when complete
Download button for generated images
Resolution: 512x512 or 1024x1024 selectable
US-4.2: Image Editing and Variations
As a user
I want to create variations of generated images
So that I can explore different options
Acceptance Criteria:
"Create variation" button on generated images
Maintains similar style/composition
Can adjust prompt for variation
Max 5 variations per original image

Epic 5: Voice Capabilities
US-5.1: Voice Input (Speech-to-Text)
As a user
I want to speak my messages
So that I can communicate hands-free
Acceptance Criteria:
Microphone button in input area
Visual indicator when recording
Click to start/stop recording
Audio transcribed accurately (95%+ accuracy)
Supports English and major languages
Max recording length: 5 minutes
Transcription appears in text input
US-5.2: Voice Output (Text-to-Speech)
As a user
I want to hear AI responses
So that I can listen while multitasking
Acceptance Criteria:
Speaker button on AI messages
Natural-sounding voice
Pause/resume controls
Speed adjustment (0.5x to 2x)
Voice selection (male/female, accents)
Auto-play toggle in settings

Epic 6: Document Generation
US-6.1: Generate PDF Documents
As a user
I want to export conversations or create PDFs
So that I can save and share content
Acceptance Criteria:
"Export to PDF" button in conversation menu
Generated PDF includes all messages
Preserves formatting and code blocks
Custom PDF generation from AI content
Includes metadata (date, conversation name)
US-6.2: Generate Word Documents
As a user
I want to create formatted Word documents
So that I can edit content in Microsoft Word
Acceptance Criteria:
Export conversation to .docx
AI can generate custom documents
Preserves headings, lists, tables
Includes styling and formatting
US-6.3: Generate Excel Spreadsheets
As a user
I want to create Excel files with data
So that I can work with structured information
Acceptance Criteria:
AI generates .xlsx files
Supports multiple sheets
Includes formulas and formatting
Tables and charts supported
Max 50,000 rows

Epic 7: User Interface & Experience
US-7.1: Dark Theme Interface
As a user
I want to use a dark-themed interface
So that I can reduce eye strain
Acceptance Criteria:
Default dark background (#0a0a0a to #1a1a1a range)
High contrast text (accessibility AA compliant)
Subtle accent colors
Smooth color transitions
No theme toggle needed (always dark)
US-7.2: Three.js Background Animation
As a user
I want to see elegant 3D animations
So that the interface feels modern and engaging
Acceptance Criteria:
Minimal geometric particle system or mesh
Subtle movement (not distracting)
60fps performance
Responds to mouse movement (parallax)
Low GPU usage (<10%)
Can be disabled in settings
US-7.3: Responsive Layout
As a user
I want to use the app on different screen sizes
So that I can access it from any device
Acceptance Criteria:
Mobile responsive (320px+)
Tablet optimized (768px+)
Desktop optimized (1024px+)
Sidebar collapses on mobile
Touch-friendly controls on mobile
US-7.4: Minimal, Modern UI
As a user
I want to see a clean, uncluttered interface
So that I can focus on conversations
Acceptance Criteria:
Ample whitespace
Clear visual hierarchy
Smooth animations (250-300ms)
Glassmorphism effects (subtle)
No unnecessary UI elements
Icon-based actions where appropriate

Epic 8: Settings & Configuration
US-8.1: Model Settings
As a user
I want to adjust AI model parameters
So that I can customize response behavior
Acceptance Criteria:
Temperature slider (0-2)
Max tokens slider (100-4096)
Top-p slider
Model selection dropdown
Settings persist across sessions
Reset to defaults button
US-8.2: Application Settings
As a user
I want to configure app preferences
So that I can personalize my experience
Acceptance Criteria:
TTS voice selection
Auto-play toggle
Animation toggle
Keyboard shortcuts help
Clear all data option
Export/import settings

Technical Specifications
System Architecture
┌─────────────┐      ngrok      ┌──────────────┐
│   Browser   │ ←──────────────→ │ Express API  │
│  (React)    │   HTTPS          │  (Node.js)   │
└─────────────┘                  └──────────────┘
                                       ↓
                          ┌────────────┼────────────┐
                          ↓            ↓            ↓
                    ┌─────────┐  ┌─────────┐  ┌─────────┐
                    │ Ollama  │  │ SQLite  │  │  File   │
                    │ Models  │  │   DB    │  │ Storage │
                    └─────────┘  └─────────┘  └─────────┘
Database Schema
sql
-- Conversations table
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  parent_id TEXT,
  attachments TEXT, -- JSON array
  metadata TEXT, -- JSON object
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
  FOREIGN KEY (parent_id) REFERENCES messages(id) ON DELETE SET NULL
);

-- Generated files table
CREATE TABLE generated_files (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  message_id TEXT,
  file_type TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_name TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
  FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
);

-- Settings table
CREATE TABLE settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

#### Conversations
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/:id` - Get conversation details
- `PUT /api/conversations/:id` - Update conversation (rename)
- `DELETE /api/conversations/:id` - Delete conversation
- `GET /api/conversations/:id/messages` - Get all messages in conversation

#### Messages
- `POST /api/conversations/:id/messages` - Send message (with streaming)
- `PUT /api/messages/:id` - Edit message
- `DELETE /api/messages/:id` - Delete message
- `POST /api/messages/:id/regenerate` - Regenerate AI response

#### Multimodal
- `POST /api/upload` - Upload files (images, docs)
- `POST /api/analyze-image` - Analyze uploaded image
- `POST /api/process-document` - Process PDF/Word/Excel

#### Image Generation
- `POST /api/generate-image` - Generate image from text
- `POST /api/image-variation` - Create image variation
- `GET /api/generated-images/:id` - Get generated image

#### Voice
- `POST /api/speech-to-text` - Convert audio to text
- `POST /api/text-to-speech` - Convert text to audio
- `GET /api/voices` - List available TTS voices

#### Document Generation
- `POST /api/generate-pdf` - Generate PDF document
- `POST /api/generate-docx` - Generate Word document
- `POST /api/generate-xlsx` - Generate Excel document
- `GET /api/downloads/:id` - Download generated file

#### Settings
- `GET /api/settings` - Get all settings
- `PUT /api/settings` - Update settings
- `GET /api/models` - List available Ollama models

### File Structure
```
chatgpt-clone/
├── client/                   # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatInput.jsx
│   │   │   │   ├── ChatMessage.jsx
│   │   │   │   ├── ChatWindow.jsx
│   │   │   │   └── StreamingMessage.jsx
│   │   │   ├── Sidebar/
│   │   │   │   ├── ConversationList.jsx
│   │   │   │   ├── ConversationItem.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   ├── ThreeBackground/
│   │   │   │   ├── Scene.jsx
│   │   │   │   └── Particles.jsx
│   │   │   ├── Settings/
│   │   │   │   └── SettingsModal.jsx
│   │   │   ├── FileUpload/
│   │   │   │   └── DropZone.jsx
│   │   │   └── Voice/
│   │   │       ├── VoiceRecorder.jsx
│   │   │       └── AudioPlayer.jsx
│   │   ├── hooks/
│   │   │   ├── useChat.js
│   │   │   ├── useConversations.js
│   │   │   └── useVoice.js
│   │   ├── store/
│   │   │   └── store.js (Zustand)
│   │   ├── utils/
│   │   │   ├── api.js
│   │   │   └── markdown.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── server/                   # Node.js backend
│   ├── src/
│   │   ├── config/
│   │   │   ├── database.js
│   │   │   └── ollama.js
│   │   ├── controllers/
│   │   │   ├── conversationController.js
│   │   │   ├── messageController.js
│   │   │   ├── fileController.js
│   │   │   ├── imageController.js
│   │   │   ├── voiceController.js
│   │   │   └── documentController.js
│   │   ├── services/
│   │   │   ├── ollamaService.js
│   │   │   ├── documentParser.js
│   │   │   ├── imageGenerator.js
│   │   │   ├── ttsService.js
│   │   │   ├── sttService.js
│   │   │   └── documentGenerator.js
│   │   ├── middleware/
│   │   │   ├── errorHandler.js
│   │   │   ├── fileUpload.js
│   │   │   └── validation.js
│   │   ├── routes/
│   │   │   ├── conversations.js
│   │   │   ├── messages.js
│   │   │   ├── files.js
│   │   │   ├── images.js
│   │   │   ├── voice.js
│   │   │   └── documents.js
│   │   ├── utils/
│   │   │   ├── database.js
│   │   │   └── fileStorage.js
│   │   └── server.js
│   ├── package.json
│   └── .env
│
├── storage/                  # Local file storage
│   ├── uploads/
│   ├── generated/
│   └── temp/
│
├── database/
│   └── chatgpt.db
│
├── docker-compose.yml       # Optional containerization
├── package.json             # Root package.json
└── README.md
Performance Requirements
Response Time:
Message send: < 100ms to acknowledge
First token: < 500ms
File upload: < 2s for processing
Image generation: 10-60s depending on model
Concurrency:
Support 10+ simultaneous conversations
Handle 5+ file uploads concurrently
Resource Usage:
RAM: 4-8GB (with models loaded)
GPU: Optional, but recommended for image generation
Storage: 10GB+ for models and data
Browser Compatibility:
Chrome 90+
Firefox 88+
Safari 14+
Edge 90+
Security Considerations
Local-only access by default
ngrok authentication for external access
File upload validation (type, size, malware scan)
SQL injection prevention with parameterized queries
XSS protection with sanitized outputs
Rate limiting on API endpoints
CORS configuration for ngrok domain
Three.js Animation Specifications
Design: Minimal geometric particle system with subtle interactions
Components:
Particles:
200-500 floating particles
Small spheres or points (1-3px)
Color: subtle blues/purples with opacity
Random drift movement
Connection Lines:
Lines connect nearby particles (< 100px distance)
Fade based on distance
Thickness: 0.5-1px
Interactivity:
Mouse parallax effect (subtle)
Particles slightly repel from cursor
Smooth camera movement
Performance:
Use instanced rendering
Efficient distance calculations
RequestAnimationFrame optimization
Graceful degradation on low-end devices

Implementation Phases
Phase 1: Core Setup (Week 1)
Project scaffolding
Database setup
Basic Express API
Ollama integration
Simple React UI
Phase 2: Chat Functionality (Week 2)
Conversation management
Message streaming
Markdown rendering
Basic UI components
Phase 3: Multimodal Input (Week 3)
File upload system
Image analysis
Document parsing (PDF, Word, Excel)
Phase 4: Voice & Image Gen (Week 4)
TTS/STT integration
Image generation pipeline
Audio recording/playback
Phase 5: Document Generation (Week 5)
PDF export
Word document generation
Excel file creation
Phase 6: UI Polish (Week 6)
Three.js background
Dark theme refinement
Animations and transitions
Responsive design
Phase 7: Testing & Optimization (Week 7)
Performance optimization
Bug fixes
ngrok setup
Documentation

Testing Strategy
Unit Tests
Service layer functions
Document parsers
File validators
Database queries
Integration Tests
API endpoints
Ollama communication
File processing pipeline
Document generation
E2E Tests
Complete user flows
Conversation creation
File upload and analysis
Voice recording
Document export
Performance Tests
Load testing (10+ concurrent users)
Memory leak detection
Response time benchmarks
File upload stress tests

This comprehensive specification covers all aspects of your ChatGPT clone. Would you like me to create the actual implementation starting with any particular component, or would you like me to refine any section of the specification?








Complete UI Specification Document
ChatGPT Clone - Design System & Component Library

1. Design Tokens & Variables
Color Palette
css
/* Primary Colors */
--color-primary: #6366f1;          /* Indigo - primary actions */
--color-primary-hover: #4f46e5;
--color-primary-light: rgba(99, 102, 241, 0.1);

/* Background Colors */
--color-bg-primary: #0a0a0a;       /* Main background */
--color-bg-secondary: #141414;     /* Elevated surfaces */
--color-bg-tertiary: #1a1a1a;      /* Cards, panels */
--color-bg-hover: #1f1f1f;         /* Hover states */
--color-bg-active: #252525;        /* Active/pressed states */

/* Text Colors */
--color-text-primary: #e5e5e5;     /* Main text */
--color-text-secondary: #a3a3a3;   /* Secondary text */
--color-text-tertiary: #737373;    /* Disabled/placeholder */
--color-text-inverse: #0a0a0a;     /* Text on light backgrounds */

/* Border Colors */
--color-border-primary: #262626;   /* Default borders */
--color-border-secondary: #333333; /* Subtle borders */
--color-border-focus: #6366f1;     /* Focus rings */

/* Status Colors */
--color-success: #22c55e;
--color-success-bg: rgba(34, 197, 94, 0.1);
--color-error: #ef4444;
--color-error-bg: rgba(239, 68, 68, 0.1);
--color-warning: #f59e0b;
--color-warning-bg: rgba(245, 158, 11, 0.1);
--color-info: #3b82f6;
--color-info-bg: rgba(59, 130, 246, 0.1);

/* Accent Colors (for Three.js particles) */
--color-accent-1: #8b5cf6;         /* Purple */
--color-accent-2: #06b6d4;         /* Cyan */
--color-accent-3: #6366f1;         /* Indigo */

/* Glassmorphism */
--glass-bg: rgba(20, 20, 20, 0.7);
--glass-border: rgba(255, 255, 255, 0.1);
--glass-backdrop: blur(12px);
Typography
css
/* Font Families */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* Font Sizes */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
Spacing System
css
/* Spacing Scale (4px base) */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
Border Radius
css
--radius-sm: 0.375rem;   /* 6px */
--radius-md: 0.5rem;     /* 8px */
--radius-lg: 0.75rem;    /* 12px */
--radius-xl: 1rem;       /* 16px */
--radius-2xl: 1.5rem;    /* 24px */
--radius-full: 9999px;   /* Full circle */
Shadows
css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
--shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
Animation Tokens
css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-bounce: 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

---

## 2. Layout Structure

### Overall Layout (Desktop 1920x1080)
```
┌─────────────────────────────────────────────────────────────────┐
│  Three.js Background Layer (Full viewport, z-index: 0)          │
│                                                                  │
│  ┌────────────┬──────────────────────────────────────────────┐ │
│  │            │                                               │ │
│  │            │         Top Navigation Bar                    │ │
│  │            │         Height: 64px                          │ │
│  │            │                                               │ │
│  │  Sidebar   ├──────────────────────────────────────────────┤ │
│  │  320px     │                                               │ │
│  │            │                                               │ │
│  │            │         Chat Window                           │ │
│  │            │         (Scrollable)                          │ │
│  │            │                                               │ │
│  │            │                                               │ │
│  │            │                                               │ │
│  │            ├──────────────────────────────────────────────┤ │
│  │            │                                               │ │
│  │            │         Input Area                            │ │
│  │            │         Min Height: 120px                     │ │
│  │            │                                               │ │
│  └────────────┴──────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
Responsive Breakpoints
css
/* Mobile */
@media (max-width: 640px) {
  /* Sidebar becomes slide-over drawer */
  /* Full width chat */
}

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) {
  /* Collapsible sidebar (60px collapsed) */
}

/* Desktop */
@media (min-width: 1025px) {
  /* Full layout as shown above */
}

3. Component Specifications
3.1 Sidebar Component
Dimensions:
Width: 320px (expanded), 60px (collapsed)
Full viewport height
Position: Fixed left
Visual Style:
css
{
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-right: 1px solid var(--glass-border);
  z-index: 10;
}
```

**Structure:**
```
┌────────────────────┐
│   Logo & Toggle    │ ← Height: 64px, padding: 16px
├────────────────────┤
│   New Chat Button  │ ← Height: 48px, margin: 16px
├────────────────────┤
│                    │
│  Conversation List │
│   (Scrollable)     │
│                    │
│  • Today           │
│    - Conv 1        │
│    - Conv 2        │
│                    │
│  • Yesterday       │
│    - Conv 3        │
│                    │
│  • Previous 7 Days │
│    - Conv 4        │
│                    │
│  • Previous 30 Days│
│                    │
├────────────────────┤
│   User Profile     │ ← Height: 64px, padding: 16px
│   Settings         │
└────────────────────┘
Logo & Toggle Section:
Logo: 32x32px icon
App name: "AI Chat" in --text-xl --font-semibold
Collapse toggle button: 24x24px icon button (right aligned)
Glassmorphic background with subtle border-bottom
New Chat Button:
css
{
  width: calc(100% - 32px);
  height: 48px;
  margin: 16px;
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  transition: var(--transition-base);
}

.new-chat-button:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.new-chat-button:active {
  transform: translateY(0);
}
Icon: Plus icon (20x20px) on the left
Conversation Item:
css
{
  height: 48px;
  margin: 4px 12px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition-fast);
  position: relative;
}

.conversation-item:hover {
  background: var(--color-bg-hover);
}

.conversation-item.active {
  background: var(--color-bg-active);
  border-left: 3px solid var(--color-primary);
  padding-left: 9px;
}
Conversation Item Structure:
Icon: Message bubble icon (16x16px), color: --color-text-secondary
Title: Truncated to single line with ellipsis
Actions: Visible on hover (right side)
Edit icon (16x16px)
Delete icon (16x16px)
Gap between icons: 8px
Section Headers (Today, Yesterday, etc.):
css
{
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 16px 8px 16px;
  margin-top: 16px;
}
User Profile Section:
css
{
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 64px;
  padding: 12px 16px;
  border-top: 1px solid var(--color-border-primary);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  display: flex;
  align-items: center;
  gap: 12px;
}
Structure:
Avatar: 40x40px circle, background gradient or user image
User info (when expanded):
Name: --text-sm --font-medium
Status/role: --text-xs --color-text-secondary
Settings icon button: 20x20px (right aligned)
Collapsed State (60px width):
Show only icons
Logo becomes icon only
New chat button shows only plus icon
Conversation items show only message icon
Tooltip appears on hover (delay: 500ms)

3.2 Top Navigation Bar
Dimensions:
Height: 64px
Full width (minus sidebar)
Position: Sticky top
Visual Style:
css
{
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-bottom: 1px solid var(--glass-border);
  z-index: 9;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
Left Section:
Current conversation title (editable on click)
Font: --text-lg --font-semibold
Breadcrumb style: Home > Conversation Title
Edit icon appears on hover (16x16px)
Center Section:
Model selector dropdown
Current model badge with icon
Click to open model selection modal
Right Section:
Share button (ghost style)
Export button (ghost style)
More options menu (3 dots)
Gap between buttons: 12px
Button Style (Ghost):
css
{
  height: 40px;
  padding: 0 16px;
  background: transparent;
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  transition: var(--transition-base);
}

.ghost-button:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-secondary);
  color: var(--color-text-primary);
}

3.3 Chat Window
Dimensions:
Full remaining height (viewport - topbar - input)
Full width (minus sidebar)
Padding: 32px (sides), 24px (top/bottom on mobile)
Visual Style:
css
{
  overflow-y: auto;
  scroll-behavior: smooth;
  padding: 32px;
  position: relative;
}

/* Custom scrollbar */
.chat-window::-webkit-scrollbar {
  width: 8px;
}

.chat-window::-webkit-scrollbar-track {
  background: transparent;
}

.chat-window::-webkit-scrollbar-thumb {
  background: var(--color-border-secondary);
  border-radius: var(--radius-full);
}

.chat-window::-webkit-scrollbar-thumb:hover {
  background: var(--color-border-primary);
}
```

**Empty State:**
```
┌─────────────────────────────────────┐
│                                     │
│           [Large Icon]              │
│                                     │
│        Start a conversation         │
│                                     │
│    Try asking about anything or     │
│    upload files to analyze          │
│                                     │
│  [Suggestion 1] [Suggestion 2]      │
│  [Suggestion 3] [Suggestion 4]      │
│                                     │
└─────────────────────────────────────┘
Centered container:
Max width: 800px
Margin: auto
Icon: 64x64px, color: --color-primary with 20% opacity
Title: --text-2xl --font-semibold
Subtitle: --text-base --color-text-secondary
Suggestions: Pill-shaped buttons with gradients
Suggestion Pill:
css
{
  padding: 12px 20px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: var(--transition-base);
}

.suggestion-pill:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

3.4 Message Components
Message Container:
Max width: 800px
Margin: 0 auto 24px auto (24px gap between messages)
User Message:
css
{
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}
```

**Structure:**
```
┌────────────────────────────────────────────────────┐
│                                     [Avatar] │
│  ┌──────────────────────────────┐          │
│  │                              │          │
│  │  Message Content             │          │
│  │  (User text)                 │          │
│  │                              │          │
│  └──────────────────────────────┘          │
│              [Edit] [Timestamp]           │
└────────────────────────────────────────────────────┘
User Message Bubble:
css
{
  background: var(--color-primary);
  color: white;
  padding: 16px 20px;
  border-radius: var(--radius-xl);
  border-bottom-right-radius: var(--radius-sm);
  max-width: 70%;
  word-wrap: break-word;
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}
AI Message:
css
{
  display: flex;
  gap: 16px;
  justify-content: flex-start;
}
```

**Structure:**
```
┌────────────────────────────────────────────────────┐
│ [Avatar]                                           │
│         ┌──────────────────────────────┐          │
│         │                              │          │
│         │  Message Content             │          │
│         │  (AI response)               │          │
│         │                              │          │
│         └──────────────────────────────┘          │
│         [Copy] [Speak] [Regenerate] [Timestamp]   │
└────────────────────────────────────────────────────┘
AI Message Bubble:
css
{
  background: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  padding: 16px 20px;
  border-radius: var(--radius-xl);
  border-bottom-left-radius: var(--radius-sm);
  max-width: 70%;
  word-wrap: break-word;
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  border: 1px solid var(--color-border-primary);
}
Avatar Styles:
Size: 32x32px
Border-radius: var(--radius-full)
User: Gradient background (--color-primary to --color-accent-1)
AI: Icon or logo with --color-bg-tertiary background
Message Actions (Icon Buttons):
css
{
  display: flex;
  gap: 8px;
  margin-top: 8px;
  opacity: 0;
  transition: var(--transition-base);
}

.message-container:hover .message-actions {
  opacity: 1;
}

.action-button {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.action-button:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
  border-color: var(--color-primary);
}
Icons: 16x16px (Copy, Speaker, Refresh, Edit, Trash)
Timestamp:
css
{
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  margin-left: auto;
  padding: 0 4px;
}
Streaming Indicator (for AI responses):
css
{
  display: inline-flex;
  gap: 4px;
  margin-left: 8px;
}

.streaming-dot {
  width: 6px;
  height: 6px;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  animation: pulse 1.4s ease-in-out infinite;
}

.streaming-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.streaming-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 80%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}
```

---

### 3.5 Code Block Component

**Structure:**
```
┌────────────────────────────────────┐
│ [Language] [Filename]  [Copy] │ ← Header bar
├────────────────────────────────────┤
│                                    │
│  const example = () => {           │
│    return "Hello World";           │
│  }                                 │
│                                    │
└────────────────────────────────────┘
Visual Style:
css
{
  background: #000000;
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  margin: 16px 0;
  overflow: hidden;
}

.code-header {
  height: 44px;
  padding: 0 16px;
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.code-language {
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.code-content {
  padding: 16px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.6;
}

.copy-button {
  height: 28px;
  padding: 0 12px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.copy-button:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.copy-button.copied {
  background: var(--color-success-bg);
  color: var(--color-success);
  border-color: var(--color-success);
}
Syntax Highlighting: Use a dark theme variant (e.g., Nord, Dracula, or custom)

3.6 Input Area Component
Dimensions:
Min height: 120px
Max height: 400px (auto-expand)
Full width (minus sidebar)
Position: Fixed bottom
Padding: 24px
Visual Style:
css
{
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-top: 1px solid var(--glass-border);
  padding: 24px;
  z-index: 9;
}
```

**Structure:**
```
┌──────────────────────────────────────────────────┐
│                                                  │
│  [Attachment Previews - if any]                 │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │                                            │ │
│  │  Type your message...                      │ │
│  │                                            │ │
│  │                                            │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  [Attach] [Voice] [Image Gen]        [Send]     │
│                                                  │
└──────────────────────────────────────────────────┘
Input Container:
css
{
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}
Textarea:
css
{
  width: 100%;
  min-height: 56px;
  max-height: 300px;
  padding: 16px 56px 16px 16px; /* Right padding for send button */
  background: var(--color-bg-tertiary);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  font-family: var(--font-primary);
  line-height: var(--leading-normal);
  resize: none;
  outline: none;
  transition: var(--transition-base);
}

.textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.textarea::placeholder {
  color: var(--color-text-tertiary);
}
Send Button:
css
{
  position: absolute;
  right: 8px;
  bottom: 8px;
  width: 40px;
  height: 40px;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-base);
}

.send-button:hover {
  background: var(--color-primary-hover);
  transform: scale(1.05);
}

.send-button:active {
  transform: scale(0.95);
}

.send-button:disabled {
  background: var(--color-bg-hover);
  cursor: not-allowed;
  opacity: 0.5;
}

/* Icon */
.send-icon {
  width: 20px;
  height: 20px;
  color: white;
  transform: rotate(-45deg);
}
Action Buttons Row:
css
{
  display: flex;
  gap: 8px;
  margin-top: 12px;
  align-items: center;
}

.action-button-input {
  height: 36px;
  padding: 0 12px;
  background: transparent;
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: var(--transition-base);
}

.action-button-input:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
  color: var(--color-text-primary);
}

.action-button-input.recording {
  background: var(--color-error-bg);
  border-color: var(--color-error);
  color: var(--color-error);
  animation: pulse-red 1.5s ease-in-out infinite;
}

@keyframes pulse-red {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
Icons: 16x16px (Paperclip, Microphone, Sparkles for image gen)
Character Counter (appears when > 8000 characters):
css
{
  position: absolute;
  right: 56px;
  bottom: 16px;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  padding: 4px 8px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
}

.character-counter.warning {
  color: var(--color-warning);
}

.character-counter.error {
  color: var(--color-error);
}
```

---

### 3.7 File Attachment Preview

**Displays above textarea when files are attached**

**Structure (Horizontal scroll):**
```
┌────────┬────────┬────────┬────────┐
│  IMG1  │  IMG2  │  PDF   │  XLS   │
│  [×]   │  [×]   │  [×]   │  [×]   │
└────────┴────────┴────────┴────────┘
Preview Card:
css
{
  width: 120px;
  height: 120px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px;
}

/* For images */
.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* For documents */
.preview-icon {
  width: 48px;
  height: 48px;
  color: var(--color-text-secondary);
}

.preview-filename {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  text-align: center;
  margin-top: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.remove-attachment {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: var(--transition-fast);
}

.preview-card:hover .remove-attachment {
  opacity: 1;
}

.remove-attachment:hover {
  background: var(--color-error);
}

3.8 Image Display in Messages
Generated or uploaded images within messages
css
{
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-lg);
  margin: 12px 0;
  border: 1px solid var(--color-border-primary);
  cursor: pointer;
  transition: var(--transition-base);
}

.message-image:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-lg);
}
Image Actions Overlay (appears on hover):
css
{
  position: absolute;
  bottom: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: var(--transition-base);
}

.image-container:hover .image-actions {
  opacity: 1;
}

.image-action-button {
  width: 36px;
  height: 36px;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: var(--transition-fast);
}

.image-action-button:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
}
Actions: Download, Full Screen, Create Variation, Delete

3.9 Modal Components
Base Modal Overlay:
css
{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 24px;
  animation: fadeIn 200ms ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
Modal Container:
css
{
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  animation: slideUp 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
Modal Header:
css
{
  padding: 24px;
  border-bottom: 1px solid var(--color-border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.modal-close:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}
Modal Body:
css
{
  padding: 24px;
  overflow-y: auto;
  max-height: calc(90vh - 160px);
}
Modal Footer:
css
{
  padding: 24px;
  border-top: 1px solid var(--color-border-primary);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

3.10 Settings Modal (Specific Implementation)
Tabs Navigation (Left side):
css
{
  width: 200px;
  border-right: 1px solid var(--color-border-primary);
  padding: 16px;
}

.settings-tab {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: var(--transition-fast);
  margin-bottom: 4px;
}

.settings-tab:hover {
  background: var(--color-bg-hover);
}

.settings-tab.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: var(--font-medium);
}
Tabs: General, Models, Voice, Appearance, Advanced
Settings Content Area:
Padding: 24px
Flex: 1
Setting Row:
css
{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--color-border-primary);
}

.setting-info {
  flex: 1;
}

.setting-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.setting-description {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  line-height: var(--leading-normal);
}

.setting-control {
  margin-left: 24px;
}

3.11 Form Controls
Toggle Switch:
css
{
  width: 48px;
  height: 28px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-full);
  position: relative;
  cursor: pointer;
  transition: var(--transition-base);
}

.toggle-switch.checked {
  background: var(--color-primary);
}

.toggle-thumb {
  width: 22px;
  height: 22px;
  background: white;
  border-radius: var(--radius-full);
  position: absolute;
  top: 3px;
  left: 3px;
  transition: var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.toggle-switch.checked .toggle-thumb {
  transform: translateX(20px);
}
Slider:
css
{
  width: 200px;
  height: 6px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-full);
  position: relative;
  cursor: pointer;
}

.slider-track {
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  position: absolute;
  left: 0;
  top: 0;
}

.slider-thumb {
  width: 18px;
  height: 18px;
  background: var(--color-primary);
  border: 3px solid white;
  border-radius: var(--radius-full);
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  cursor: grab;
  transition: var(--transition-fast);
  box-shadow: var(--shadow-md);
}

.slider-thumb:hover {
  transform: translate(-50%, -50%) scale(1.2);
}

.slider-thumb:active {
  cursor: grabbing;
}

.slider-value {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  margin-top: 8px;
  text-align: right;
}
Select Dropdown:
css
{
  width: 200px;
  height: 40px;
  padding: 0 16px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: var(--transition-base);
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* Chevron down */
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
}

.select:hover {
  border-color: var(--color-border-secondary);
  background-color: var(--color-bg-hover);
}

.select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}
Button Variants:
css
/* Primary Button */
.button-primary {
  height: 44px;
  padding: 0 24px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: var(--transition-base);
}

.button-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.button-primary:active {
  transform: translateY(0);
}

.button-primary:disabled {
  background: var(--color-bg-hover);
  color: var(--color-text-tertiary);
  cursor: not-allowed;
  transform: none;
}

/* Secondary Button */
.button-secondary {
  height: 44px;
  padding: 0 24px;
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: var(--transition-base);
}

.button-secondary:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-secondary);
}

/* Danger Button */
.button-danger {
  height: 44px;
  padding: 0 24px;
  background: var(--color-error);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: var(--transition-base);
}

.button-danger:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

3.12 Loading States
Skeleton Loader (for conversation list):
css
{
  width: 100%;
  height: 48px;
  background: linear-gradient(
    90deg,
    var(--color-bg-tertiary) 0%,
    var(--color-bg-hover) 50%,
    var(--color-bg-tertiary) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
  margin-bottom: 8px;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}
Spinner (for processing):
css
{
  width: 24px;
  height: 24px;
  border: 3px solid var(--color-bg-hover);
  border-top-color: var(--color-primary);
  border-radius: var(--radius-full);
  animation: spin 800ms linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

3.13 Toast Notifications
Position: Fixed, top-right corner, 24px from edges
css
{
  min-width: 320px;
  max-width: 400px;
  padding: 16px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  display: flex;
  gap: 12px;
  align-items: flex-start;
  animation: slideInRight 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Variants */
.toast.success {
  border-left-color: var(--color-success);
}

.toast.error {
  border-left-color: var(--color-error);
}

.toast.warning {
  border-left-color: var(--color-warning);
}

.toast.info {
  border-left-color: var(--color-info);
}

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.toast-message {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-normal);
}

.toast-close {
  width: 20px;
  height: 20px;
  color: var(--color-text-tertiary);
  cursor: pointer;
  flex-shrink: 0;
}

.toast-close:hover {
  color: var(--color-text-primary);
}
Auto-dismiss: 5 seconds (unless error, then 10 seconds)

3.14 Context Menu (Right-click menu)
css
{
  min-width: 200px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 8px;
  z-index: 100;
  animation: scaleIn 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.context-menu-item {
  height: 36px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.context-menu-item:hover {
  background: var(--color-bg-hover);
}

.context-menu-item.danger {
  color: var(--color-error);
}

.context-menu-item.danger:hover {
  background: var(--color-error-bg);
}

.context-menu-divider {
  height: 1px;
  background: var(--color-border-primary);
  margin: 8px 0;
}

.context-menu-icon {
  width: 16px;
  height: 16px;
  color: var(--color-text-secondary);
}

.context-menu-item:hover .context-menu-icon {
  color: var(--color-text-primary);
}

3.15 Three.js Background Specification
Canvas:
Position: Fixed, full viewport
z-index: 0
Pointer-events: none (so it doesn't interfere with UI)
Scene Configuration:
javascript
{
  backgroundColor: transparent,
  fog: none,
  camera: {
    type: 'PerspectiveCamera',
    fov: 75,
    position: [0, 0, 50],
  }
}
Particle System:
javascript
{
  particleCount: 300,
  particleGeometry: 'SphereGeometry',
  particleSize: 0.15,
  particleColor: new THREE.Color(0x6366f1), // Primary color
  particleOpacity: 0.6,
  distribution: {
    x: [-60, 60],
    y: [-40, 40],
    z: [-20, 20]
  },
  animation: {
    drift: {
      speed: 0.0005,
      amplitude: 0.5
    },
    rotation: {
      x: 0.0001,
      y: 0.0002
    }
  }
}
Connection Lines:
javascript
{
  maxDistance: 15, // Units
  lineColor: new THREE.Color(0x6366f1),
  lineOpacity: 0.2,
  lineWidth: 1,
  maxConnections: 3 // Per particle
}
Mouse Interaction:
javascript
{
  parallax: {
    enabled: true,
    strength: 0.02 // Subtle movement
  },
  repulsion: {
    enabled: true,
    radius: 10,
    strength: 0.5
  }
}
```

**Performance Optimization:**
- Use BufferGeometry
- Instanced rendering for particles
- Frustum culling enabled
- Auto-adjust particle count based on FPS
- Disable on low-end devices (< 30 FPS)

**Alternative Animations (user can choose in settings):**
1. **Particles** (default)
2. **Waves**: Sine wave mesh with vertex displacement
3. **Minimal**: Single rotating geometric shape
4. **None**: Plain gradient background

---

### 3.16 Voice Recording Modal

**Appears when microphone button clicked**
```
┌─────────────────────────────────┐
│                                 │
│         [Waveform Visual]       │
│                                 │
│           00:15 / 05:00         │
│                                 │
│     [Pause/Resume]  [Stop]      │
│                                 │
│         Cancel                  │
│                                 │
└─────────────────────────────────┘
Modal Size: 400px x 300px
Waveform Visual:
css
{
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.waveform-bar {
  width: 4px;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  transition: height 100ms ease-out;
  animation: pulse 1s ease-in-out infinite alternate;
}

@keyframes pulse {
  from {
    opacity: 0.5;
  }
  to {
    opacity: 1;
  }
}
Timer:
css
{
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  font-variant-numeric: tabular-nums;
  color: var(--color-text-primary);
  text-align: center;
  margin: 16px 0;
}
```

---

### 3.17 Image Generation Modal

**Triggered by /imagine command or image gen button**
```
┌──────────────────────────────────────┐
│  Generate Image                      │
├──────────────────────────────────────┤
│                                      │
│  Prompt:                             │
│  ┌────────────────────────────────┐ │
│  │                                │ │
│  │  Describe your image...        │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│                                      │
│  Resolution:                         │
│  [512x512] [1024x1024] [Custom]      │
│                                      │
│  Style: [None ▾]                     │
│                                      │
│  Negative Prompt: (Optional)         │
│  ┌────────────────────────────────┐ │
│  │  What to avoid...              │ │
│  └────────────────────────────────┘ │
│                                      │
├──────────────────────────────────────┤
│             [Cancel] [Generate]      │
└──────────────────────────────────────┘
```

**During Generation:**
- Show progress bar
- Estimated time remaining
- Preview icon animating

---

### 3.18 User Authentication & Multi-User Support

**Login Screen:**
```
┌─────────────────────────────────────────┐
│                                         │
│           [Logo/Icon 64x64]             │
│                                         │
│              AI Chat                    │
│                                         │
│     Your personal AI assistant          │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Email or Username               │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Password                         │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [ ] Remember me                        │
│                                         │
│         [Sign In]                       │
│                                         │
│   Don't have an account? Sign up        │
│                                         │
└─────────────────────────────────────────┘
Visual Style:
css
{
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
  position: relative;
}

/* Three.js background active here too */

.login-container {
  width: 100%;
  max-width: 420px;
  padding: 48px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-xl);
}

.login-logo {
  width: 64px;
  height: 64px;
  margin: 0 auto 24px;
  display: block;
}

.login-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: 8px;
}

.login-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  text-align: center;
  margin-bottom: 32px;
}

.login-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  margin-bottom: 16px;
  transition: var(--transition-base);
}

.login-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.login-button {
  width: 100%;
  height: 52px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  cursor: pointer;
  margin-top: 24px;
  transition: var(--transition-base);
}

.login-button:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.login-link {
  display: block;
  text-align: center;
  margin-top: 24px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.login-link a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: var(--font-medium);
}

.login-link a:hover {
  text-decoration: underline;
}
```

**Registration Screen:**
Similar layout with additional fields:
- Full Name
- Email
- Username
- Password
- Confirm Password
- Terms & Conditions checkbox

---

### 3.19 User Profile Menu (Dropdown)

**Triggered by clicking user avatar in sidebar**
```
┌────────────────────────────┐
│  [Avatar] John Doe         │
│           john@email.com   │
├────────────────────────────┤
│  Profile Settings          │
│  API Keys                  │
│  Usage & Billing           │
├────────────────────────────┤
│  Help & Support            │
│  Documentation             │
├────────────────────────────┤
│  Sign Out                  │
└────────────────────────────┘
css
{
  width: 280px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  position: absolute;
  bottom: 72px;
  left: 12px;
  z-index: 20;
  animation: slideUp 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.profile-menu-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--color-border-primary);
  background: var(--color-bg-secondary);
}

.profile-menu-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  border: 2px solid var(--color-primary);
}

.profile-menu-info {
  flex: 1;
}

.profile-menu-name {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

.profile-menu-email {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.profile-menu-item {
  height: 40px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: var(--transition-fast);
}

.profile-menu-item:hover {
  background: var(--color-bg-hover);
}

.profile-menu-item.danger {
  color: var(--color-error);
}

.profile-menu-item.danger:hover {
  background: var(--color-error-bg);
}

3.20 Responsive Design Specifications
Mobile (< 640px):
Sidebar becomes full-screen overlay/drawer
Hamburger menu button in top-left (32x32px)
Single column layout
Input area reduces padding to 16px
Message max-width: 100%
Font sizes reduce by 10%
Three.js particle count: 150
Tablet (640px - 1024px):
Sidebar width: 280px
Collapsible sidebar with toggle
Adaptive message width
Standard font sizes
Three.js particle count: 250
Desktop (> 1024px):
Full layout as specified
Max content width: 1600px (centered)
Three.js particle count: 300-500 based on GPU

3.21 Accessibility Specifications
Keyboard Navigation:
Tab order: Logical flow through interactive elements
Focus indicators: 2px solid --color-primary ring with 3px offset
Escape key: Close modals, menus, dropdowns
Enter key: Submit forms, send messages
Cmd/Ctrl + N: New conversation
Cmd/Ctrl + K: Focus search
Cmd/Ctrl + /: Show keyboard shortcuts
Screen Reader Support:
All interactive elements have aria-labels
Role attributes on custom components
Live regions for dynamic content (streaming messages)
Alt text on all images
Semantic HTML structure
Color Contrast:
All text meets WCAG AA standards (4.5:1 for normal text)
Large text meets AAA standards (7:1)
Interactive elements clearly distinguishable
Focus States:
css
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 3px;
  border-radius: var(--radius-sm);
}

4. Animation Guidelines
Micro-interactions:
Button hover: 250ms ease
Color transitions: 150ms ease
Transform/scale: 200ms cubic-bezier(0.4, 0, 0.2, 1)
Fade in/out: 200ms ease
Page Transitions:
Route changes: 300ms slide + fade
Modal open: 300ms scale + fade
Drawer slide: 250ms ease-out
**Loading Animations
Reintentar
D
Continuar
4. Animation Guidelines (Continued)
Loading Animations:
css
/* Pulsing loader */
@keyframes pulse-loader {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(0.95);
  }
}

/* Skeleton shimmer */
@keyframes skeleton-shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* Dot bouncing (for loading) */
@keyframes dot-bounce {
  0%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
}

/* Spinner rotation */
@keyframes spinner-rotate {
  to {
    transform: rotate(360deg);
  }
}

/* Progress bar fill */
@keyframes progress-fill {
  from {
    width: 0%;
  }
  to {
    width: var(--progress-value);
  }
}
Entrance Animations:
css
/* Fade in up */
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale in */
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Slide in from right */
@keyframes slide-in-right {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Slide in from left */
@keyframes slide-in-left {
  from {
    opacity: 0;
    transform: translateX(-100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
Exit Animations:
css
/* Fade out down */
@keyframes fade-out-down {
  from {
    opacity: 1;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(20px);
  }
}

/* Scale out */
@keyframes scale-out {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.9);
  }
}
Attention Grabbers:
css
/* Shake (for errors) */
@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-5px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(5px);
  }
}

/* Wobble */
@keyframes wobble {
  0%, 100% {
    transform: rotate(0deg);
  }
  25% {
    transform: rotate(-5deg);
  }
  75% {
    transform: rotate(5deg);
  }
}

/* Glow pulse (for notifications) */
@keyframes glow-pulse {
  0%, 100% {
    box-shadow: 0 0 5px var(--color-primary);
  }
  50% {
    box-shadow: 0 0 20px var(--color-primary);
  }
}
Stagger Animations (for lists):
css
.stagger-item {
  animation: fade-in-up 400ms cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 50ms; }
.stagger-item:nth-child(3) { animation-delay: 100ms; }
.stagger-item:nth-child(4) { animation-delay: 150ms; }
.stagger-item:nth-child(5) { animation-delay: 200ms; }
/* Continue pattern for more items */

5. Icon System
Icon Library: Lucide React (https://lucide.dev)
Icon Sizes:
xs: 14x14px
sm: 16x16px
md: 20x20px
lg: 24x24px
xl: 32x32px
2xl: 48x48px
Common Icons Used:
Navigation & Actions
Menu: Hamburger menu
X: Close/Cancel
Plus: New/Add
ChevronRight: Navigation forward
ChevronLeft: Navigation back
ChevronDown: Dropdown indicator
ChevronUp: Collapse indicator
ArrowLeft: Back
ArrowRight: Forward
MoreVertical: More options (3 dots vertical)
MoreHorizontal: More options (3 dots horizontal)
Chat & Messages
MessageSquare: Conversation
Send: Send message
Mic: Voice recording
MicOff: Mute
Volume2: Speaker/TTS
VolumeX: Mute TTS
Paperclip: Attach file
Image: Image upload/generation
Sparkles: AI/Magic features
Editing & Actions
Edit: Edit
Edit2: Edit (pencil variant)
Trash2: Delete
Copy: Copy to clipboard
Check: Success/Confirm
CheckCircle2: Success notification
Download: Download
Upload: Upload
Share2: Share
RefreshCw: Regenerate/Refresh
RotateCcw: Undo
RotateCw: Redo
Files & Documents
File: Generic file
FileText: Text document
FileCode: Code file
FileImage: Image file
Folder: Folder
FolderOpen: Open folder
Settings & Profile
Settings: Settings
User: User profile
Users: Multiple users
Shield: Security
Key: API keys
CreditCard: Billing
HelpCircle: Help
Info: Information
AlertCircle: Warning
AlertTriangle: Alert/Warning
XCircle: Error
Media Controls
Play: Play
Pause: Pause
Square: Stop
SkipForward: Next
SkipBack: Previous
FastForward: Speed up
Rewind: Speed down
Status
Loader2: Loading spinner
Clock: Time/History
Calendar: Date/Calendar
Bell: Notifications
BellOff: Muted notifications
Eye: View/Visible
EyeOff: Hidden
Lock: Locked/Secure
Unlock: Unlocked
Layout
Sidebar: Sidebar toggle
Layout: Layout options
Maximize2: Fullscreen
Minimize2: Exit fullscreen
PanelLeft: Left panel
PanelRight: Right panel
AI/Tech Specific
Cpu: Model/Processing
Zap: Fast/Premium
TrendingUp: Analytics
Activity: Activity/Stats
Database: Data/Storage
Server: Backend/Server
Icon Implementation:
jsx
import { MessageSquare, Send, Settings } from 'lucide-react';

// Usage with size and color
<MessageSquare 
  size={20} 
  color="var(--color-text-secondary)"
  strokeWidth={2}
/>
```

---

## 6. Additional Modal Specifications

### 6.1 Confirmation Dialog
```
┌─────────────────────────────────┐
│  [!] Delete Conversation?       │
├─────────────────────────────────┤
│                                 │
│  This action cannot be undone.  │
│  All messages in this           │
│  conversation will be           │
│  permanently deleted.           │
│                                 │
├─────────────────────────────────┤
│         [Cancel] [Delete]       │
└─────────────────────────────────┘
Dimensions: 400px width, auto height
css
.confirmation-dialog {
  width: 400px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.confirmation-header {
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--color-border-primary);
}

.confirmation-icon {
  width: 24px;
  height: 24px;
  color: var(--color-warning);
}

.confirmation-icon.danger {
  color: var(--color-error);
}

.confirmation-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.confirmation-body {
  padding: 24px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}

.confirmation-footer {
  padding: 16px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  border-top: 1px solid var(--color-border-primary);
}
```

### 6.2 Model Selection Modal
```
┌────────────────────────────────────────────┐
│  Select Model                         [×]  │
├────────────────────────────────────────────┤
│  Search models...                     [🔍] │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ ◉ Qwen 3 1.7B                        │ │
│  │   Fast, efficient for everyday use   │ │
│  │   Parameters: 1.7B • Context: 32K   │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ ○ LLaVA 7B                           │ │
│  │   Image understanding & analysis     │ │
│  │   Parameters: 7B • Context: 4K      │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │ ○ Mistral 7B                         │ │
│  │   High quality, balanced             │ │
│  │   Parameters: 7B • Context: 32K     │ │
│  └──────────────────────────────────────┘ │
│                                            │
├────────────────────────────────────────────┤
│                    [Cancel] [Select Model] │
└────────────────────────────────────────────┘
Dimensions: 600px width, max 70vh height
css
.model-card {
  padding: 16px;
  background: var(--color-bg-tertiary);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  margin-bottom: 12px;
  cursor: pointer;
  transition: var(--transition-base);
}

.model-card:hover {
  border-color: var(--color-border-secondary);
  background: var(--color-bg-hover);
}

.model-card.selected {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.model-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.model-radio {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  border: 2px solid var(--color-border-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.model-card.selected .model-radio {
  border-color: var(--color-primary);
}

.model-radio-dot {
  width: 10px;
  height: 10px;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  display: none;
}

.model-card.selected .model-radio-dot {
  display: block;
}

.model-name {
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.model-description {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-bottom: 8px;
  line-height: var(--leading-normal);
}

.model-specs {
  display: flex;
  gap: 16px;
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.model-spec {
  display: flex;
  align-items: center;
  gap: 4px;
}
```

### 6.3 File Upload Modal
```
┌────────────────────────────────────────┐
│  Upload Files                     [×]  │
├────────────────────────────────────────┤
│                                        │
│  ╔════════════════════════════════╗   │
│  ║                                ║   │
│  ║        [📁]                    ║   │
│  ║                                ║   │
│  ║   Drag files here or click     ║   │
│  ║   to browse                    ║   │
│  ║                                ║   │
│  ║   Supports: Images, PDFs,      ║   │
│  ║   Word, Excel (Max 50MB)       ║   │
│  ║                                ║   │
│  ╚════════════════════════════════╝   │
│                                        │
│  Uploaded Files (2):                   │
│  ┌──────────────────────────────────┐ │
│  │ [📄] document.pdf        2.3 MB  │ │
│  │ [×]                               │ │
│  │ [████████░░] 80%                  │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ [🖼️] image.jpg           1.1 MB  │ │
│  │ [×]                               │ │
│  │ [██████████] 100% ✓               │ │
│  └──────────────────────────────────┘ │
│                                        │
├────────────────────────────────────────┤
│                   [Cancel] [Continue]  │
└────────────────────────────────────────┘
Dimensions: 600px width, auto height
css
.dropzone {
  border: 2px dashed var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 48px 24px;
  text-align: center;
  background: var(--color-bg-primary);
  transition: var(--transition-base);
  cursor: pointer;
  margin-bottom: 24px;
}

.dropzone:hover {
  border-color: var(--color-primary);
  background: var(--color-bg-hover);
}

.dropzone.active {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.dropzone-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  color: var(--color-text-tertiary);
}

.dropzone-text {
  font-size: var(--text-base);
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.dropzone-hint {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-normal);
}

.upload-list-header {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: 12px;
}

.upload-item {
  padding: 12px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
}

.upload-item-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.upload-item-icon {
  width: 24px;
  height: 24px;
  color: var(--color-text-secondary);
}

.upload-item-info {
  flex: 1;
}

.upload-item-name {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  font-weight: var(--font-medium);
}

.upload-item-size {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.upload-item-remove {
  width: 24px;
  height: 24px;
  color: var(--color-text-tertiary);
  cursor: pointer;
  transition: var(--transition-fast);
}

.upload-item-remove:hover {
  color: var(--color-error);
}

.upload-progress {
  height: 4px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.upload-progress-bar {
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--radius-full);
  transition: width 300ms ease-out;
}

.upload-progress-bar.complete {
  background: var(--color-success);
}

.upload-progress-bar.error {
  background: var(--color-error);
}
```

### 6.4 Export Options Modal
```
┌────────────────────────────────────────┐
│  Export Conversation              [×]  │
├────────────────────────────────────────┤
│                                        │
│  Format:                               │
│  ┌──────────────────────────────────┐ │
│  │ ◉ PDF Document                   │ │
│  │   Includes formatting & images   │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ ○ Word Document (.docx)          │ │
│  │   Editable in Microsoft Word     │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ ○ Plain Text (.txt)              │ │
│  │   Simple text format             │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ┌──────────────────────────────────┐ │
│  │ ○ JSON (.json)                   │ │
│  │   For developers                 │ │
│  └──────────────────────────────────┘ │
│                                        │
│  Options:                              │
│  ☑ Include system messages             │
│  ☑ Include timestamps                  │
│  ☑ Include attachments                 │
│                                        │
├────────────────────────────────────────┤
│                    [Cancel] [Export]   │
└────────────────────────────────────────┘
```

### 6.5 Keyboard Shortcuts Modal
```
┌──────────────────────────────────────────────┐
│  Keyboard Shortcuts                     [×]  │
├──────────────────────────────────────────────┤
│                                              │
│  General                                     │
│  ┌──────────────────────────────────┐       │
│  │ Ctrl/Cmd + N    New conversation │       │
│  │ Ctrl/Cmd + K    Search           │       │
│  │ Ctrl/Cmd + /    Show shortcuts   │       │
│  │ Ctrl/Cmd + ,    Settings         │       │
│  │ Escape          Close modal      │       │
│  └──────────────────────────────────┘       │
│                                              │
│  Chat                                        │
│  ┌──────────────────────────────────┐       │
│  │ Enter           Send message     │       │
│  │ Shift + Enter   New line         │       │
│  │ Ctrl/Cmd + ↑    Edit last msg    │       │
│  │ Ctrl/Cmd + R    Regenerate       │       │
│  └──────────────────────────────────┘       │
│                                              │
│  Navigation                                  │
│  ┌──────────────────────────────────┐       │
│  │ Ctrl/Cmd + B    Toggle sidebar   │       │
│  │ ↑ / ↓           Navigate msgs    │       │
│  │ Tab             Next element     │       │
│  │ Shift + Tab     Previous element │       │
│  └──────────────────────────────────┘       │
│                                              │
└──────────────────────────────────────────────┘
css
.shortcuts-section {
  margin-bottom: 24px;
}

.shortcuts-section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.shortcut-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: var(--color-bg-tertiary);
  border-radius: var(--radius-md);
  margin-bottom: 4px;
}

.shortcut-keys {
  display: flex;
  gap: 6px;
  align-items: center;
}

.shortcut-key {
  padding: 4px 8px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--color-text-primary);
  min-width: 28px;
  text-align: center;
}

.shortcut-description {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

7. Status & Feedback Components
7.1 Progress Bar
css
.progress-container {
  width: 100%;
  height: 8px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--color-primary) 0%,
    var(--color-accent-1) 100%
  );
  border-radius: var(--radius-full);
  transition: width 300ms ease-out;
  position: relative;
}

/* Animated shine effect */
.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: progress-shine 2s ease-in-out infinite;
}

@keyframes progress-shine {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Indeterminate progress */
.progress-bar.indeterminate {
  width: 40% !important;
  animation: progress-indeterminate 1.5s ease-in-out infinite;
}

@keyframes progress-indeterminate {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(350%);
  }
}
7.2 Status Badge
css
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.status-badge.success {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.status-badge.error {
  background: var(--color-error-bg);
  color: var(--color-error);
}

.status-badge.warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.status-badge.info {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.status-badge.processing {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--radius-full);
  background: currentColor;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}
```

### 7.3 Empty States

**No Conversations:**
```
┌─────────────────────────────────┐
│                                 │
│         [Large Icon]            │
│                                 │
│    No conversations yet         │
│                                 │
│    Start by creating a new      │
│    conversation or asking       │
│    a question                   │
│                                 │
│         [New Chat]              │
│                                 │
└─────────────────────────────────┘
```

**No Search Results:**
```
┌─────────────────────────────────┐
│                                 │
│      [Search Icon]              │
│                                 │
│    No results found             │
│                                 │
│    Try adjusting your           │
│    search terms                 │
│                                 │
└─────────────────────────────────┘
```

**Network Error:**
```
┌─────────────────────────────────┐
│                                 │
│      [Alert Icon]               │
│                                 │
│    Connection lost              │
│                                 │
│    Please check your            │
│    connection and try again     │
│                                 │
│         [Retry]                 │
│                                 │
└─────────────────────────────────┘
css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  text-align: center;
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  color: var(--color-text-tertiary);
  opacity: 0.5;
  margin-bottom: 24px;
}

.empty-state-title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.empty-state-description {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
  max-width: 400px;
  margin-bottom: 24px;
}

8. Advanced Component Patterns
8.1 Tooltip
css
.tooltip-trigger {
  position: relative;
  display: inline-block;
}

.tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 12px;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  font-size: var(--text-xs);
  color: var(--color-text-primary);
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity 200ms ease;
  z-index: 100;
  box-shadow: var(--shadow-lg);
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--color-bg-secondary);
}

.tooltip-trigger:hover .tooltip {
  opacity: 1;
  transition-delay: 500ms;
}

/* Tooltip positions */
.tooltip.top {
  bottom: calc(100% + 8px);
  top: auto;
}

.tooltip.bottom {
  top: calc(100% + 8px);
  bottom: auto;
}

.tooltip.bottom::after {
  top: -12px;
  border-top-color: transparent;
  border-bottom-color: var(--color-bg-secondary);
}

.tooltip.left {
  right: calc(100% + 8px);
  left: auto;
  bottom: auto;
  top: 50%;
  transform: translateY(-50%);
}

.tooltip.right {
  left: calc(100% + 8px);
  right: auto;
  bottom: auto;
  top: 50%;
  transform: translateY(-50%);
}
8.2 Popover
css
.popover {
  position: absolute;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 16px;
  z-index: 50;
  min-width: 200px;
  max-width: 320px;
  animation: popover-appear 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes popover-appear {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.popover-arrow {
  position: absolute;
  width: 12px;
  height: 12px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  transform: rotate(45deg);
}

.popover-arrow.top {
  top: -7px;
  left: 50%;
  margin-left: -6px;
  border-bottom: none;
  border-right: none;
}

.popover-arrow.bottom {
  bottom: -7px;
  left: 50%;
  margin-left: -6px;
  border-top: none;
  border-left: none;
}
8.3 Accordion
css
.accordion-item {
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
  overflow: hidden;
  transition: var(--transition-base);
}

.accordion-header {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  background: var(--color-bg-tertiary);
  transition: var(--transition-fast);
  user-select: none;
}

.accordion-header:hover {
  background: var(--color-bg-hover);
}

.accordion-title {
  font-size: var(--text-base);
  font-weight: var(--font-medium);
  color: var(--color-text-primary);
}

.accordion-icon {
  width: 20px;
  height: 20px;
  color: var(--color-text-secondary);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.accordion-item.open .accordion-icon {
  transform: rotate(180deg);
}

.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.accordion-item.open .accordion-content {
  max-height: 1000px; /* Adjust based on content */
}

.accordion-body {
  padding: 16px 20px;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: var(--leading-relaxed);
}
8.4 Tabs Component
css
.tabs-container {
  width: 100%;
}

.tabs-list {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--color-border-primary);
  margin-bottom: 24px;
}

.tab-trigger {
  padding: 12px 20px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: var(--transition-base);
  position: relative;
}

.tab-trigger:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.tab-trigger.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-content {
  animation: fade-in 300ms ease;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

9. Multi-User Specific Components
9.1 User Session Indicator (Top bar)
css
.session-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-full);
}

.session-avatar {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-full);
  border: 2px solid var(--color-primary);
}

.session-name {
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  font-weight: var(--font-medium);
}

.session-status {
  width: 8px;
  height: 8px;
  background: var(--color-success);
  border-radius: var(--radius-full);
  border: 2px solid var(--color-bg-tertiary);
}

.session-status.away {
  background: var(--color-warning);
}

.session-status.offline {
  background: var(--color-text-tertiary);
}
9.2 Admin Dashboard (for user management)
User List Table:
css
.users-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 8px;
}

.table-header {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 16px;
  text-align: left;
}

.table-row {
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  transition: var(--transition-fast);
}

.table-row:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-secondary);
}

.table-cell {
  padding: 16px;
  font-size: var(--text-sm);
  color: var(--color-text-primary);
}

.table-cell.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: var(--font-medium);
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

.user-email {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.user-role-badge {
  display: inline-block;
  padding: 4px 10px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  text-transform: capitalize;
}

.user-role-badge.admin {
  background: var(--color-error-bg);
  color: var(--color-error);
}
9.3 Usage Statistics Dashboard
css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 24px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  transition: var(--transition-base);
}

.stat-card:hover {
  border-color: var(--color-primary);
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  border-radius: var(--radius-md);
  color: var(--color-primary);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.stat-trend.up {
  color: var(--color-success);
}

.stat-trend.down {
  color: var(--color-error);
}

.stat-value {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

10. Error States & Validation
10.1 Input Validation States
css
.input-group {
  margin-bottom: 16px;
}

.input-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
}

.input {
  width: 100%;
  height: 44px;
  padding: 0 16px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: var(--text-base);
  transition: var(--transition-base);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-light);
}

.input.error {
  border-color: var(--color-error);
}

.input.error:focus {
  box-shadow: 0 0 0 3px var(--color-error-bg);
}

.input.success {
  border-color: var(--color-success);
  padding-right: 40px;
}

.input-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

.input-icon.success {
  color: var(--color-success);
}

.input-icon.error {
  color: var(--color-error);
}

.input-hint {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  margin-top: 6px;
}

.input-error {
  font-size: var(--text-xs);
  color: var(--color-error);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.input-error-icon {
  width: 14px;
  height: 14px;
}
```

### 10.2 Error Page (500, 404, etc.)
```
┌─────────────────────────────────────┐
│                                     │
│         [Error Icon]                │
│                                     │
│            Oops!                    │
│                                     │
│     Something went wrong            │
│                                     │
│  The page you're looking for        │
│  doesn't exist or an error occurred │
│                                     │
│     [Go Home] [Contact Support]     │
│                                     │
│       Error Code: 404               │
│                                     │
└─────────────────────────────────────┘
css
.error-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  text-align: center;
}

.error-icon {
  width: 120px;
  height: 120px;
  color: var(--color-error);
  opacity: 0.8;
  margin-bottom: 32px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.error-title {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  margin-bottom: 16px;
}

.error-message {
  font-size: var(--text-xl);
  color: var(--color-text-secondary);
  margin-bottom: 12px;
}

.error-description {
  font-size: var(--text-base);
  color: var(--color-text-tertiary);
  max-width: 500px;
  line-height: var(--leading-relaxed);
  margin-bottom: 32px;
}

.error-actions {
  display: flex;
  gap: 16px;
}

.error-code {
  margin-top: 32px;
  font-size: var(--text-sm);
  font-family: var(--font-mono);
  color: var(--color-text-tertiary);
}

11. Mobile-Specific Patterns
11.1 Mobile Navigation
css
.mobile-header {
  height: 56px;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-bottom: 1px solid var(--glass-border);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 20;
}

.mobile-menu-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
}

.mobile-sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 30;
  animation: fadeIn 200ms ease;
}

.mobile-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 80%;
  max-width: 320px;
  background: var(--color-bg-primary);
  z-index: 31;
  animation: slideInLeft 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
11.2 Mobile Input Area
css
.mobile-input-area {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-backdrop);
  border-top: 1px solid var(--glass-border);
  z-index: 10;
}

.mobile-textarea {
  width: 100%;
  min-height: 44px;
  max-height: 200px;
  padding: 12px 44px 12px 12px;
  font-size: 16px; /* Prevents zoom on iOS */
}

.mobile-action-bar {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.mobile-action-button {
  flex: 1;
  height: 40px;
  font-size: var(--text-sm);
}
11.3 Pull-to-Refresh
css
.pull-to-refresh {
  position: relative;
  overflow: hidden;
}

.pull-indicator {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: top 200ms ease;
}

.pull-to-refresh.pulling .pull-indicator {
  top: 10px;
}

.pull-to-refresh.refreshing .pull-indicator {
  top: 10px;
  animation: spin 1s linear infinite;
}

12. Print Styles
css
@media print {
  /* Hide UI elements */
  .sidebar,
  .top-navigation,
  .input-area,
  .message-actions,
  .three-background {
    display: none !important;
  }

  /* Adjust layout */
  .chat-window {
    padding: 0;
    max-width: 100%;
  }

  .message-bubble {
    max-width: 100%;
    page-break-inside: avoid;
  }

  /* Adjust colors for print */
  body {
    background: white;
    color: black;
  }

  .message-bubble {
    border: 1px solid #ddd;
  }

  /* Show URLs for links */
  a::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }
}

13. Final Implementation Notes
Performance Optimization Checklist
Lazy load images and heavy components
Implement virtual scrolling for long conversation lists
Debounce search and input handlers
Use React.memo for message components
Implement code splitting for routes
Optimize Three.js particle system
Use Web Workers for heavy computations
Implement proper caching strategies
Accessibility Checklist
All colors meet WCAG AA contrast ratios
Keyboard navigation works throughout
Screen reader announcements for dynamic content
Focus management in modals
Alt text for all images
Proper heading hierarchy
ARIA labels on custom components
Skip-to-content link
Browser Compatibility
Test on Chrome, Firefox, Safari, Edge
CSS fallbacks for older browsers
Polyfills for missing features
Progressive enhancement approach
Graceful degradation
Security Considerations
Sanitize all user inputs
XSS protection
CSRF tokens
Secure file uploads
Rate limiting
Input validation
SQL injection prevention






































Cheap chatgpt clone that uses open source models
Set up run it locally and ngrok tunnel