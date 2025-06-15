#!/bin/bash
# Run Alpine Linux VM with Think AI

VM_DIR="$(pwd)/vm-think-ai"
MEMORY="1024"  # 1GB RAM (reduced for Android)

echo "🚀 Starting Alpine Linux VM"
echo "=========================="
echo ""
echo "⚠️  First boot instructions:"
echo "1. Login as 'root' (no password)"
echo "2. Run: setup-alpine"
echo "3. When asked about disk, use: sda"
echo "4. Choose sys install mode"
echo "5. After setup, run: poweroff"
echo "6. Then restart without -cdrom option"
echo ""
echo "Press Ctrl+A then X to exit QEMU"
echo ""

# First boot with ISO
if [ -f "$VM_DIR/alpine-disk.qcow2" ] && [ ! -f "$VM_DIR/.installed" ]; then
    echo "📀 Booting from ISO for installation..."
    qemu-system-x86_64 \
        -m $MEMORY \
        -hda "$VM_DIR/alpine-disk.qcow2" \
        -cdrom "$VM_DIR/alpine-virt-3.21.0-x86_64.iso" \
        -boot d \
        -netdev user,id=net0,hostfwd=tcp::2222-:22 \
        -device e1000,netdev=net0 \
        -nographic \
        -serial mon:stdio
else
    echo "💾 Booting from disk..."
    qemu-system-x86_64 \
        -m $MEMORY \
        -hda "$VM_DIR/alpine-disk.qcow2" \
        -netdev user,id=net0,hostfwd=tcp::2222-:22 \
        -device e1000,netdev=net0 \
        -nographic \
        -serial mon:stdio
fi