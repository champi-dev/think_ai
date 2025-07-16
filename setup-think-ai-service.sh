#!/bin/bash

echo "Setting up Think AI Full server as a systemd service..."

# Copy service file to systemd directory
sudo cp /home/administrator/think_ai/think-ai-full.service /etc/systemd/system/

# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable think-ai-full.service

# Start the service
sudo systemctl start think-ai-full.service

# Check status
sudo systemctl status think-ai-full.service

echo ""
echo "Service setup complete!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status think-ai-full    # Check service status"
echo "  sudo systemctl stop think-ai-full      # Stop the service"
echo "  sudo systemctl start think-ai-full     # Start the service"
echo "  sudo systemctl restart think-ai-full   # Restart the service"
echo "  sudo systemctl disable think-ai-full   # Disable auto-start on boot"
echo "  sudo journalctl -u think-ai-full -f   # View logs in real-time"