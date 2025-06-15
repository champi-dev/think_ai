# 🧠 Think AI - Universal Setup Guide

## Quick Start

Run this single command on any platform:
```bash
./run_think_ai.sh
```

The script automatically detects your environment and sets up accordingly!

---

## 📱 Mobile (Termux/Android)

### First Time Setup
1. **Install Termux packages**:
   ```bash
   pkg install python git qemu-system-x86-64-headless qemu-utils
   ```

2. **Clone Think AI**:
   ```bash
   git clone <your-repo> think_ai
   cd think_ai
   ```

3. **Run the universal script**:
   ```bash
   ./run_think_ai.sh
   ```

4. **Follow VM setup** (only first time):
   - At boot prompt: Press ENTER
   - Login as: root
   - Run quick setup commands shown
   - Reboot and enjoy root access!

### Daily Use
```bash
./run_think_ai.sh
# VM starts automatically with Think AI ready
```

---

## 💻 MacBook

### First Time Setup
1. **Clone Think AI**:
   ```bash
   git clone <your-repo> think_ai
   cd think_ai
   ```

2. **Run the universal script**:
   ```bash
   ./run_think_ai.sh
   ```
   
   The script will:
   - Install Homebrew (if needed)
   - Install Redis, Neo4j, Python
   - Start all services
   - Create virtual environment
   - Install dependencies
   - Run Think AI

### Daily Use
```bash
./run_think_ai.sh
# Everything starts automatically
```

---

## 🐧 Linux

### With Root/Sudo
```bash
sudo ./run_think_ai.sh
# Installs real services and runs full system
```

### Without Root
```bash
./run_think_ai.sh
# Uses mock services automatically
```

---

## 🚀 What Each Environment Provides

### Mobile (VM)
- ✅ Full root access in VM
- ✅ All databases (Redis, Neo4j, ScyllaDB)
- ✅ Complete Think AI experience
- ✅ SSH access: `ssh -p 2222 root@localhost`

### MacBook
- ✅ Native performance
- ✅ Real Redis & Neo4j
- ✅ Homebrew integration
- ✅ Virtual environment isolation

### Linux
- ✅ Adapts to permissions
- ✅ Real services with root
- ✅ Mock services without root
- ✅ Automatic detection

---

## 🛠️ Troubleshooting

### Mobile Issues
- **VM won't start**: Check QEMU installation: `pkg install qemu-system-x86-64-headless`
- **Network issues**: VM uses NAT, services on localhost ports

### MacBook Issues
- **Homebrew missing**: The script installs it automatically
- **Services not starting**: `brew services restart redis neo4j`

### General Issues
- **Permission denied**: `chmod +x run_think_ai.sh`
- **Dependencies missing**: Check `requirements.txt`

---

## 📋 Manual Commands

If you prefer manual control:

### Mobile (in VM)
```bash
python3 run_full_system.py
```

### MacBook/Linux
```bash
# Start services first
redis-server &  # or: brew services start redis

# Run Think AI
python3 run_full_system.py
```

---

## 🎯 One Command, Any Platform

Remember: Just run `./run_think_ai.sh` anywhere!

The script handles everything:
- Environment detection
- Dependency installation
- Service management
- Optimal configuration

Enjoy Think AI everywhere! 🚀