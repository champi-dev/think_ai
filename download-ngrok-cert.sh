#!/bin/bash

# Download ngrok certificate using the certificate ID
CERT_ID="cert_2zgiMI9vBRCkwY54ry1h8zthW4b"

echo "Downloading ngrok certificate..."

# Create certs directory if it doesn't exist
mkdir -p certs

# Download the certificate and private key
# Note: You'll need to be authenticated with ngrok
ngrok api tls-certificates get "$CERT_ID" --output json > cert_info.json

# Extract certificate and key from the response
if [ -f cert_info.json ]; then
    # Parse the JSON to extract certificate and key
    cat cert_info.json | jq -r '.certificate' > certs/server.crt
    cat cert_info.json | jq -r '.private_key' > certs/server.key
    
    # Clean up
    rm cert_info.json
    
    echo "Certificate files created:"
    echo "  - certs/server.crt"
    echo "  - certs/server.key"
    
    # Set appropriate permissions
    chmod 600 certs/server.key
    chmod 644 certs/server.crt
else
    echo "Failed to download certificate. Make sure you're authenticated with ngrok."
    echo "Run: ngrok config add-authtoken <your-authtoken>"
fi