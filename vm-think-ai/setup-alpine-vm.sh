#!/bin/bash
# Setup Alpine Linux VM for Think AI

set -e

VM_DIR="$(pwd)/vm-think-ai"
ALPINE_VERSION="3.21"
ALPINE_ARCH="x86_64"
ALPINE_ISO="alpine-virt-${ALPINE_VERSION}.0-${ALPINE_ARCH}.iso"
ALPINE_URL="https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/${ALPINE_ARCH}/${ALPINE_ISO}"

echo "🚀 Setting up Alpine Linux VM for Think AI"
echo "=========================================="

# Download Alpine ISO if not exists
if [ ! -f "$VM_DIR/$ALPINE_ISO" ]; then
    echo "📥 Downloading Alpine Linux ISO..."
    wget -P "$VM_DIR" "$ALPINE_URL"
else
    echo "✅ Alpine ISO already exists"
fi

# Create disk image (4GB)
if [ ! -f "$VM_DIR/alpine-disk.qcow2" ]; then
    echo "💾 Creating 4GB disk image..."
    qemu-img create -f qcow2 "$VM_DIR/alpine-disk.qcow2" 4G
else
    echo "✅ Disk image already exists"
fi

# Create startup script
cat > "$VM_DIR/start-vm.sh" << 'EOF'
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
EOF

chmod +x "$VM_DIR/start-vm.sh"

# Create post-install setup script
cat > "$VM_DIR/setup-think-ai.sh" << 'EOF'
#!/bin/sh
# Run this inside the Alpine VM after initial setup

echo "📦 Installing Think AI dependencies..."

# Update packages
apk update
apk upgrade

# Install Python and development tools
apk add python3 py3-pip python3-dev
apk add git gcc musl-dev linux-headers
apk add redis neo4j

# Install database tools
apk add postgresql postgresql-dev
apk add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing cassandra

# Create Think AI directory
mkdir -p /opt/think-ai

echo "✅ Basic setup complete!"
echo "Next steps:"
echo "1. Copy Think AI code to /opt/think-ai"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Start services: redis-server, neo4j, etc."
EOF

chmod +x "$VM_DIR/setup-think-ai.sh"

echo ""
echo "✅ VM setup complete!"
echo ""
echo "To start the VM:"
echo "  ./vm-think-ai/start-vm.sh"
echo ""
echo "Initial Alpine setup in VM:"
echo "1. Login as root (no password)"
echo "2. Run: setup-alpine"
echo "3. Configure network, disk, etc."
echo "4. Reboot without CD: poweroff, then start VM again without -cdrom"
echo ""
echo "After Alpine is installed:"
echo "1. Copy setup-think-ai.sh to VM"
echo "2. Run it to install dependencies"
echo "3. Copy Think AI code and run with root access!"