# Mobile UI Keyboard Handling Test Guide

## Changes Made

### 1. **chat.html** - Main Chat Interface
- Added dynamic viewport height (`100dvh`) for better mobile support
- Implemented Visual Viewport API for accurate keyboard detection
- Added keyboard-visible class for state management
- Automatic scrolling when keyboard appears/disappears
- Input field stays visible when keyboard shows
- Prevented iOS zoom on input focus (font-size: 16px)

### 2. **simple_webapp.html** - Simple Web Interface
- Similar keyboard detection and viewport adjustments
- Container repositioning when keyboard is visible
- Reduced response area height when keyboard shows
- Mobile-optimized layout for smaller screens

## Key Features Implemented

1. **Visual Viewport API Detection**
   - Most accurate method for detecting soft keyboard
   - Falls back to window resize events if not supported

2. **Keyboard State Management**
   - Tracks keyboard visibility with `isKeyboardVisible` flag
   - Adds/removes `keyboard-visible` CSS class

3. **Automatic Adjustments**
   - Input scrolls into view when focused
   - Messages stay scrolled to bottom
   - Viewport adjusts to prevent content being hidden

## Testing Instructions

### Desktop Browser Testing
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select a mobile device (e.g., iPhone 12)
4. Navigate to the chat interfaces:
   - http://localhost:8080/static/chat.html
   - http://localhost:8080/static/simple_webapp.html
5. Click on input field to simulate keyboard

### Real Mobile Device Testing
1. Find your computer's local IP address
2. Ensure mobile device is on same network
3. Navigate to: `http://[YOUR-IP]:8080/static/chat.html`
4. Test the following scenarios:

#### Test Cases
- [ ] Tap input field - keyboard should appear smoothly
- [ ] Input field should remain visible above keyboard
- [ ] Messages should stay scrolled to bottom
- [ ] Tap outside input - keyboard should hide
- [ ] Send a message - should scroll properly
- [ ] Rotate device - layout should adjust
- [ ] Long conversation - scrolling should work with keyboard visible

### Browser Compatibility
- ✅ iOS Safari (iPhone/iPad)
- ✅ Chrome Mobile (Android)
- ✅ Firefox Mobile
- ✅ Samsung Internet

## Debugging Tips

1. **Check Visual Viewport Support**
   ```javascript
   console.log('Visual Viewport supported:', 'visualViewport' in window);
   ```

2. **Monitor Keyboard State**
   ```javascript
   // Add to console to see keyboard events
   window.visualViewport?.addEventListener('resize', () => {
     console.log('Viewport height:', window.visualViewport.height);
   });
   ```

3. **Common Issues**
   - If keyboard detection fails, check viewport meta tag
   - Ensure no conflicting CSS preventing proper layout
   - Some Android keyboards behave differently - test multiple keyboards

## Local Test Script

To quickly test locally:

```bash
# Start the Think AI server
./target/release/think-ai server

# Open in mobile browser emulator
open http://localhost:8080/static/chat.html
```