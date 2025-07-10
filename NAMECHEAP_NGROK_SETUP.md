# Connecting Namecheap Domain to Ngrok

This guide will help you connect your Namecheap domain to your ngrok tunnel URL.

## Prerequisites
- Active Namecheap domain
- Ngrok account (free or paid)
- Running ngrok tunnel

## Option 1: Using CNAME Record (Recommended for Paid Ngrok)

If you have a paid ngrok account with a custom subdomain:

1. **Start ngrok with custom subdomain:**
   ```bash
   ngrok http 8080 --subdomain=yourapp
   # This gives you: yourapp.ngrok.io
   ```

2. **In Namecheap DNS settings:**
   - Go to Domain List → Manage → Advanced DNS
   - Add a CNAME record:
     - Type: CNAME
     - Host: @ (for root) or www (for www subdomain)
     - Value: yourapp.ngrok.io
     - TTL: Automatic

## Option 2: Using URL Redirect (For Free Ngrok)

Since free ngrok generates random URLs, use URL forwarding:

1. **In Namecheap:**
   - Go to Domain List → Manage → Domain → Redirect Domain
   - Source URL: yourdomain.com
   - Destination URL: https://xyz123.ngrok.io (your current ngrok URL)
   - Redirect Type: Permanent (301) or Temporary (302)

2. **Update redirect when ngrok URL changes:**
   - Each time you restart ngrok, update the redirect URL

## Option 3: Using Cloudflare (Best Solution)

This is the most flexible solution:

1. **Change nameservers to Cloudflare:**
   - Create free Cloudflare account
   - Add your domain
   - Update Namecheap nameservers to Cloudflare's

2. **In Cloudflare:**
   - Add CNAME: yourdomain.com → yourapp.ngrok.io
   - Or use Page Rules for dynamic redirects
   - Enable "Flexible" SSL

3. **Benefits:**
   - Free SSL certificate
   - Can update DNS instantly
   - Works with dynamic ngrok URLs via API

## Option 4: Using Dynamic DNS Service

For automatically updating DNS with changing ngrok URLs:

1. **Use a service like:**
   - DuckDNS (free)
   - No-IP (free tier available)
   - Dynu (free tier available)

2. **Create automation script:**
   ```bash
   #!/bin/bash
   # Get current ngrok URL
   NGROK_URL=$(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
   
   # Update DNS record via API
   curl "https://your-ddns-provider.com/update?hostname=yourdomain&myip=$NGROK_URL"
   ```

## Option 5: Ngrok Custom Domain (Paid Feature)

With ngrok paid plans:

1. **Add custom domain in ngrok dashboard:**
   - Dashboard → Domains → Add Domain
   - Verify domain ownership

2. **Update Namecheap DNS:**
   - Add CNAME: yourdomain.com → [your-id].cname.ngrok.io

3. **Start ngrok with custom domain:**
   ```bash
   ngrok http 8080 --domain=yourdomain.com
   ```

## Quick Setup Script

Here's a script to help automate the setup:

```bash
#!/bin/bash

# Check if ngrok is running
check_ngrok() {
    if ! curl -s localhost:4040/api/tunnels > /dev/null 2>&1; then
        echo "Ngrok is not running. Starting ngrok..."
        ngrok http 8080 &
        sleep 5
    fi
}

# Get current ngrok URL
get_ngrok_url() {
    NGROK_URL=$(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
    echo "Current ngrok URL: $NGROK_URL"
}

# Display setup instructions
show_instructions() {
    echo "
    ========================================
    NAMECHEAP SETUP INSTRUCTIONS
    ========================================
    
    1. Log in to Namecheap
    2. Go to Domain List → Manage → Advanced DNS
    
    For URL Redirect:
    - Click 'Add New Record'
    - Type: URL Redirect Record
    - Host: @
    - Value: $NGROK_URL
    - Unmasked/Masked: Your choice
    - Save
    
    For CNAME (if you have static ngrok subdomain):
    - Type: CNAME
    - Host: @ or www
    - Value: your-subdomain.ngrok.io
    - TTL: Automatic
    - Save
    
    Note: DNS propagation may take 10-30 minutes
    ========================================
    "
}

# Main execution
check_ngrok
get_ngrok_url
show_instructions
```

## Important Notes

1. **Free ngrok limitations:**
   - URLs change on restart
   - Limited concurrent connections
   - No custom domains

2. **DNS Propagation:**
   - Changes can take 10-30 minutes
   - Use DNS checker tools to verify

3. **SSL Certificates:**
   - Ngrok provides SSL by default
   - May show security warnings with custom domains

4. **Best Practice:**
   - Use Cloudflare for flexibility
   - Consider ngrok paid plan for production
   - Set up monitoring for URL changes

## Testing Your Setup

```bash
# Test DNS resolution
dig yourdomain.com

# Test redirect
curl -I yourdomain.com

# Check SSL
openssl s_client -connect yourdomain.com:443
```

## Troubleshooting

1. **DNS not resolving:**
   - Clear DNS cache: `sudo dscacheutil -flushcache` (Mac)
   - Wait for propagation
   - Check nameserver settings

2. **SSL errors:**
   - Use Cloudflare's flexible SSL
   - Accept self-signed certificate warnings

3. **Connection timeouts:**
   - Ensure ngrok is running
   - Check firewall settings
   - Verify port forwarding

Remember to update your domain settings each time your ngrok URL changes if using the free tier!