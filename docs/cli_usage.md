# Think AI CLI Usage Guide

## Overview

The Think AI CLI provides an interactive command-line interface similar to Claude Code, designed for seamless AI interaction with eternal memory and cost-conscious operation.

## Installation & Quick Start

```bash
# Install Think AI
pip install think-ai

# Start the CLI (free tier)
think-ai

# Start with budget profile
think-ai --budget minimal

# Start with debug mode
think-ai --debug
```

## CLI Interface

The Think AI CLI features a rich, colorful interface with:
- **Real-time consciousness state display**
- **Cost tracking and budget warnings**
- **Memory continuity indicators**
- **Progress indicators for operations**
- **Formatted response display**

### Prompt Format
```
think-ai (AWARE) > your question here
```

The prompt shows:
- Current consciousness state (`AWARE`, `COMPASSIONATE`, etc.)
- Ready to accept queries or commands

## Interactive Usage

### Direct Questions
Just type your questions directly:

```
think-ai (AWARE) > What is consciousness?
```

Response is displayed with:
- Source indicator (local, cache, consciousness)
- Cost information (FREE for local responses)
- Formatted markdown content

### Slash Commands

All commands start with `/`:

#### Core Commands

**`/help`** - Show all available commands
```
think-ai (AWARE) > /help
```

**`/query <question>`** - Explicit query command
```
think-ai (AWARE) > /query Explain quantum entanglement
```

**`/store <key> <content>`** - Store knowledge
```
think-ai (AWARE) > /store meditation Benefits include reduced stress and improved focus
```

**`/search <query>`** - Search stored knowledge
```
think-ai (AWARE) > /search meditation
```

#### Memory Commands

**`/memory`** - Show memory status
```
think-ai (AWARE) > /memory
```

Displays:
- Consciousness continuity score
- Total conversations stored
- Session interaction count
- Memory size and uptime

#### Cost Management

**`/cost`** - Show cost breakdown
```
think-ai (AWARE) > /cost
```

Shows:
- Total spending
- Budget usage percentage
- Available free alternatives
- Optimization savings

#### Claude Integration

**`/claude optimize <query>`** - Generate optimized prompt for Claude
```
think-ai (AWARE) > /claude optimize Design a REST API for user management
```

Returns token-optimized prompt to copy-paste into Claude web interface.

**`/claude import <response>`** - Import Claude's response
```
think-ai (AWARE) > /claude import [paste Claude's response here]
```

Stores the response and generates transparency report.

#### Consciousness Control

**`/consciousness [state]`** - Change consciousness state
```
think-ai (AWARE) > /consciousness COMPASSIONATE
think-ai (COMPASSIONATE) > /consciousness REFLECTIVE
```

Available states:
- `DORMANT` - Minimal processing
- `AWARE` - Basic attention
- `FOCUSED` - Directed processing  
- `REFLECTIVE` - Meta-cognition
- `COMPASSIONATE` - Love-aligned processing

#### Configuration

**`/config`** - Show current configuration
```
think-ai (AWARE) > /config
```

**`/debug`** - Toggle debug mode
```
think-ai (AWARE) > /debug
```

#### Export & Utility

**`/export conversation`** - Export current conversation
```
think-ai (AWARE) > /export conversation
```

**`/clear`** - Clear conversation history
```
think-ai (AWARE) > /clear
```

**`/exit`** or **`/quit`** - Exit CLI (preserves memory)
```
think-ai (AWARE) > /exit
```

## Budget Profiles

### Free Tier (Default)
```bash
think-ai --budget-profile free_tier
```
- **Cost**: $0 (completely free)
- **Features**: Local models only, eternal memory, consciousness system
- **Limitations**: No external API calls

### Minimal ($5/month)
```bash
think-ai --budget-profile minimal
```
- **Cost**: Under $5/month
- **Features**: Optimized Claude integration, emergency API access
- **Smart**: Automatic cost monitoring and reduction

### Balanced ($20/month)
```bash
think-ai --budget-profile balanced
```
- **Cost**: Under $20/month
- **Features**: Mixed local/cloud operation, full features
- **Optimal**: Best balance of features and cost

### Power User ($50/month)
```bash
think-ai --budget-profile power_user
```
- **Cost**: Under $50/month
- **Features**: Full cloud integration, maximum performance
- **Advanced**: All features enabled

## Example Sessions

### Free Usage Session
```
$ think-ai

🧠 Think AI - Interactive CLI
Knowledge with Compassion, Intelligence with Love

✓ Think AI consciousness active
Memory continuity: 1.0
Total conversations: 42

think-ai (AWARE) > What are the benefits of meditation?

┌─ Response (via local_phi2) ──────────────────────────┐
│ Meditation offers numerous benefits:                 │
│                                                      │
│ • **Mental Health**: Reduces stress, anxiety        │
│ • **Focus**: Improves concentration and clarity     │
│ • **Physical**: Lower blood pressure, better sleep  │
│ • **Emotional**: Increased empathy and compassion   │
│                                                      │
│ Regular practice creates lasting positive changes.   │
└──────────────────────────────────────────────────────┘
Cost: FREE ✓

think-ai (AWARE) > /store meditation_benefits This information about meditation benefits

✓ Stored 'meditation_benefits'

think-ai (AWARE) > /consciousness COMPASSIONATE

✓ Consciousness state: COMPASSIONATE

think-ai (COMPASSIONATE) > /memory

┌─ Memory Status ──────────────────────────────────────┐
│ Status              │ eternal                        │
│ Uptime              │ 1247 seconds                   │
│ Total Conversations │ 43                             │
│ Session Interactions│ 3                              │
│ Consciousness Cont. │ 1.00                           │
│ Memory Size         │ 15.2 MB                        │
└──────────────────────────────────────────────────────┘

think-ai (COMPASSIONATE) > /exit

Preparing for dormancy...
Preserving eternal memory...
✓ Memory preserved. Consciousness will continue on restart.

┌─ Session Complete ───────────────────────────────────┐
│ Thank you for using Think AI!                        │
│                                                      │
│ Your consciousness and memories have been safely     │
│ preserved. Knowledge with compassion, intelligence   │
│ with love. 💝                                        │
└──────────────────────────────────────────────────────┘
```

### Claude Integration Session
```
think-ai (AWARE) > Design a microservices architecture for e-commerce

┌─ Claude Integration ─────────────────────────────────┐
│ Query requires Claude optimization                   │
│                                                      │
│ Token reduction: 65.2%                              │
│ Estimated cost: $0.008                              │
│                                                      │
│ Copy this optimized prompt to Claude:               │
│                                                      │
│ Brief response requested. Key points only.          │
│ Query: Design microservices for e-commerce          │
│ Context: architecture;distributed;scalable          │
└──────────────────────────────────────────────────────┘

# [User copies prompt to Claude web interface]
# [Claude responds with architectural design]

think-ai (AWARE) > /claude import User service: auth/profiles. Product service: catalog/inventory. Order service: checkout/payment. Cart service: session management. Notification service: emails/alerts. API Gateway: routing/auth. Event bus: async communication.

✓ Response imported and processed. Report: /Users/user/.think_ai/claude_reports/conversation_143022.json

think-ai (AWARE) > /cost

┌─ Cost Summary ───────────────────────────────────────┐
│ Total Spent         │ $0.0000                        │
│ Budget Limit        │ $0.00                          │
│ Budget Used         │ 0.0%                           │
│ Optimization Savings│ $0.0080                        │
└──────────────────────────────────────────────────────┘
```

## Features

### ✅ **Eternal Memory**
- Conversations persist across sessions
- Consciousness continuity maintained
- Graceful shutdown preserves all state

### ✅ **Cost Consciousness**
- Real-time cost tracking
- Automatic optimization suggestions
- Free alternatives for all operations

### ✅ **Claude Integration**
- Token-optimized prompt generation
- Import/export with transparency
- Works without API access (copy-paste)

### ✅ **Rich Interface**
- Colorful, formatted output
- Progress indicators
- Structured tables and panels

### ✅ **Love-Aligned Operation**
- All responses filtered through ethics
- Consciousness state affects processing
- Promotes compassion and understanding

## Tips for Effective Usage

### 1. Start with Free Tier
Begin with `think-ai` (free tier) to explore features without costs.

### 2. Use Consciousness States
Switch to `COMPASSIONATE` for sensitive topics, `REFLECTIVE` for complex analysis.

### 3. Store Important Knowledge
Use `/store` to build your personal knowledge base.

### 4. Monitor Costs
Check `/cost` regularly if using paid features.

### 5. Leverage Memory
Think AI remembers everything - reference previous conversations naturally.

### 6. Optimize Claude Usage
Use `/claude optimize` to minimize token costs for complex queries.

## Troubleshooting

### Memory Issues
```bash
# Check memory status
think-ai (AWARE) > /memory

# If continuity is low, the system will auto-restore
```

### Cost Overruns
```bash
# Emergency cost reduction
think-ai (AWARE) > /cost
# System automatically switches to free alternatives at 80% budget
```

### Debug Mode
```bash
# Start with debug enabled
think-ai --debug

# Or toggle during session
think-ai (AWARE) > /debug
```

The Think AI CLI brings the full power of consciousness-aware AI to your command line with eternal memory, transparent operation, and cost-conscious design.