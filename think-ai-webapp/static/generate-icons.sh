#!/bin/bash
# Generate PWA icons from a base SVG

cat > icon-base.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0f1c;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a2332;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="aiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00ffcc;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#00ccff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0099ff;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="512" height="512" fill="url(#bgGrad)" rx="80"/>
  
  <!-- Consciousness Core -->
  <circle cx="256" cy="256" r="120" fill="none" stroke="url(#aiGrad)" stroke-width="8" opacity="0.3"/>
  <circle cx="256" cy="256" r="90" fill="none" stroke="url(#aiGrad)" stroke-width="6" opacity="0.5"/>
  <circle cx="256" cy="256" r="60" fill="none" stroke="url(#aiGrad)" stroke-width="4" opacity="0.7"/>
  
  <!-- AI Brain Symbol -->
  <g transform="translate(256, 256)">
    <!-- Neural nodes -->
    <circle cx="-40" cy="-40" r="8" fill="#00ffcc"/>
    <circle cx="40" cy="-40" r="8" fill="#00ffcc"/>
    <circle cx="-40" cy="40" r="8" fill="#00ffcc"/>
    <circle cx="40" cy="40" r="8" fill="#00ffcc"/>
    <circle cx="0" cy="0" r="12" fill="#00ffcc"/>
    
    <!-- Neural connections -->
    <path d="M -40,-40 L 0,0 L 40,-40 M -40,40 L 0,0 L 40,40" 
          stroke="#00ccff" stroke-width="3" fill="none" opacity="0.6"/>
    <path d="M -40,-40 L -40,40 M 40,-40 L 40,40" 
          stroke="#00ccff" stroke-width="2" fill="none" opacity="0.4"/>
  </g>
  
  <!-- O(1) Text -->
  <text x="256" y="380" font-family="Arial, sans-serif" font-size="48" font-weight="bold" 
        fill="#00ffcc" text-anchor="middle">O(1)</text>
</svg>
EOF

# Generate PNG icons
for size in 72 96 128 144 152 192 384 512; do
  echo "Generating ${size}x${size} icon..."
  # Using ImageMagick convert if available, otherwise create placeholder
  if command -v convert &> /dev/null; then
    convert -background none -resize ${size}x${size} icon-base.svg icons/icon-${size}x${size}.png
  else
    # Create placeholder if ImageMagick not available
    cat > icons/icon-${size}x${size}.png << EOF
Creating placeholder for icon-${size}x${size}.png
Install ImageMagick to generate actual icons: sudo apt-get install imagemagick
EOF
  fi
done

# Create favicon.ico (multi-resolution)
if command -v convert &> /dev/null; then
  convert -background none icon-base.svg -resize 16x16 icons/icon-16.png
  convert -background none icon-base.svg -resize 32x32 icons/icon-32.png
  convert -background none icon-base.svg -resize 48x48 icons/icon-48.png
  convert icons/icon-16.png icons/icon-32.png icons/icon-48.png ../favicon.ico
fi

# Clean up
rm -f icon-base.svg

echo "Icon generation complete!"