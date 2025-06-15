# Alpine VM Quick Start Guide

## First Boot Setup (5 minutes)

1. Run the VM:
   ```bash
   ./vm-think-ai/run-alpine-vm.sh
   ```

2. At `boot:` prompt, just press ENTER

3. Login as `root` (no password needed)

4. Run the quick setup:
   ```bash
   # Quick minimal setup
   setup-keymap us us
   setup-hostname think-ai
   setup-interfaces -a
   rc-service networking start
   setup-apkrepos -1
   setup-sshd openssh
   setup-disk -q -m sys /dev/sda
   ```

5. When asked "WARNING: Erase the above disk(s) and continue? (y/n)", type `y`

6. After installation completes, run:
   ```bash
   poweroff
   ```

## Second Boot - Install Think AI

1. Start VM again (now boots from disk):
   ```bash
   ./vm-think-ai/run-alpine-vm.sh
   ```

2. Login as root and install Think AI deps:
   ```bash
   # Set root password first
   passwd
   
   # Install Python and databases
   apk update
   apk add python3 py3-pip git redis
   
   # Start Redis
   rc-service redis start
   rc-update add redis
   
   # Clone Think AI
   cd /root
   git clone [your-repo-url] think_ai
   cd think_ai
   pip install -r requirements.txt
   
   # Run with full root access!
   python run_full_system.py
   ```

## SSH Access (Optional)
From Termux:
```bash
ssh -p 2222 root@localhost
```