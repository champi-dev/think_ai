#!/bin/bash
VM_DIR="$(pwd)/vm-think-ai"

echo "🖥️  Starting Alpine Linux VM..."
echo "================================"
echo "VM will run with:"
echo "  - 2GB RAM"
echo "  - 2 CPU cores"
echo "  - Network enabled"
echo "  - SSH on port 2222"
echo ""
echo "Default login: root (no password initially)"
echo "SSH access: ssh -p 2222 root@localhost"
echo ""

qemu-system-x86_64 \
    -m 2048 \
    -smp 2 \
    -hda "$VM_DIR/alpine-disk.qcow2" \
    -cdrom "$VM_DIR/alpine-virt-3.21.0-x86_64.iso" \
    -boot d \
    -netdev user,id=net0,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:80,hostfwd=tcp::6379-:6379,hostfwd=tcp::7687-:7687 \
    -device e1000,netdev=net0 \
    -nographic \
    -serial mon:stdio
