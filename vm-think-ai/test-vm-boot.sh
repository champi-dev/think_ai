#!/bin/bash
# Test VM boot and capture evidence

echo "🧪 Testing Alpine VM Boot Process"
echo "================================="
echo ""
echo "This will boot the VM for 10 seconds to verify it works"
echo ""

# Start VM with timeout
timeout 10 qemu-system-x86_64 \
    -m 512 \
    -hda vm-think-ai/alpine-disk.qcow2 \
    -cdrom vm-think-ai/alpine-virt-3.21.0-x86_64.iso \
    -boot d \
    -netdev user,id=net0 \
    -device e1000,netdev=net0 \
    -nographic \
    -serial mon:stdio 2>&1 | tee vm-boot-test.log

echo ""
echo "✅ VM Boot Test Complete!"
echo ""
echo "Evidence collected in vm-boot-test.log"
echo "First 20 lines of boot log:"
echo "----------------------------"
head -20 vm-boot-test.log 2>/dev/null || echo "No log captured"