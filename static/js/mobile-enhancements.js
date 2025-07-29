// Mobile UI/UX Enhancements
(function() {
  'use strict';

  // Detect if mobile
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  const isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
  
  if (!isMobile) return;

  // Viewport height fix for mobile browsers
  function setViewportHeight() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  }
  
  setViewportHeight();
  window.addEventListener('resize', setViewportHeight);
  window.addEventListener('orientationchange', setViewportHeight);

  // Prevent iOS bounce effect
  document.body.addEventListener('touchmove', function(e) {
    if (!e.target.closest('.messages')) {
      e.preventDefault();
    }
  }, { passive: false });

  // Handle keyboard show/hide
  let keyboardHeight = 0;
  
  function handleKeyboard() {
    const input = document.getElementById('queryInput');
    if (!input) return;

    input.addEventListener('focus', () => {
      document.body.classList.add('keyboard-open');
      
      // Scroll to bottom when keyboard opens
      setTimeout(() => {
        const messages = document.querySelector('.messages');
        if (messages) {
          messages.scrollTop = messages.scrollHeight;
        }
      }, 300);
    });

    input.addEventListener('blur', () => {
      document.body.classList.remove('keyboard-open');
    });
  }

  // Touch gestures support
  let touchStartY = 0;
  let touchEndY = 0;
  let messageContainer = null;

  function initTouchGestures() {
    messageContainer = document.querySelector('.messages');
    if (!messageContainer) return;

    // Pull to refresh
    let isPulling = false;
    let pullDistance = 0;
    
    messageContainer.addEventListener('touchstart', (e) => {
      if (messageContainer.scrollTop === 0) {
        touchStartY = e.touches[0].clientY;
        isPulling = true;
      }
    });

    messageContainer.addEventListener('touchmove', (e) => {
      if (!isPulling) return;
      
      const currentY = e.touches[0].clientY;
      pullDistance = currentY - touchStartY;
      
      if (pullDistance > 0 && messageContainer.scrollTop === 0) {
        e.preventDefault();
        
        // Visual feedback
        const pullIndicator = document.querySelector('.pull-to-refresh');
        if (pullIndicator) {
          pullIndicator.style.transform = `translateX(-50%) translateY(${Math.min(pullDistance * 0.5, 50)}px)`;
          pullIndicator.classList.toggle('visible', pullDistance > 50);
        }
      }
    });

    messageContainer.addEventListener('touchend', () => {
      if (pullDistance > 100) {
        // Trigger refresh
        location.reload();
      }
      
      isPulling = false;
      pullDistance = 0;
      
      const pullIndicator = document.querySelector('.pull-to-refresh');
      if (pullIndicator) {
        pullIndicator.style.transform = 'translateX(-50%) translateY(0)';
        pullIndicator.classList.remove('visible');
      }
    });

    // Swipe actions on messages
    let touchStartX = 0;
    let currentMessage = null;

    messageContainer.addEventListener('touchstart', (e) => {
      const message = e.target.closest('.message');
      if (message) {
        touchStartX = e.touches[0].clientX;
        currentMessage = message;
      }
    });

    messageContainer.addEventListener('touchmove', (e) => {
      if (!currentMessage) return;
      
      const touchX = e.touches[0].clientX;
      const deltaX = touchStartX - touchX;
      
      if (Math.abs(deltaX) > 50) {
        currentMessage.classList.add('swiped');
      }
    });

    messageContainer.addEventListener('touchend', () => {
      if (currentMessage) {
        setTimeout(() => {
          currentMessage.classList.remove('swiped');
        }, 3000);
      }
      currentMessage = null;
    });
  }

  // Haptic feedback
  function triggerHaptic(style = 'light') {
    if ('vibrate' in navigator) {
      switch(style) {
        case 'light':
          navigator.vibrate(10);
          break;
        case 'medium':
          navigator.vibrate(20);
          break;
        case 'heavy':
          navigator.vibrate(30);
          break;
      }
    }
  }

  // Enhanced button interactions
  function enhanceButtons() {
    const buttons = document.querySelectorAll('button, .input-feature-toggle');
    
    buttons.forEach(button => {
      button.addEventListener('touchstart', () => {
        triggerHaptic('light');
      });
    });

    // Send button enhancement
    const sendBtn = document.getElementById('sendBtn');
    if (sendBtn) {
      sendBtn.addEventListener('click', () => {
        triggerHaptic('medium');
      });
    }
  }

  // Voice input improvements
  function enhanceVoiceInput() {
    const micButton = document.querySelector('.input-feature-toggle.mic');
    if (!micButton) return;

    let isRecording = false;
    
    micButton.addEventListener('click', () => {
      isRecording = !isRecording;
      micButton.classList.toggle('recording', isRecording);
      
      if (isRecording) {
        triggerHaptic('heavy');
        // Start recording logic here
      } else {
        triggerHaptic('light');
        // Stop recording logic here
      }
    });
  }

  // Auto-resize textarea
  function autoResizeInput() {
    const input = document.getElementById('queryInput');
    if (!input) return;

    function resize() {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    }

    input.addEventListener('input', resize);
    input.addEventListener('focus', resize);
  }

  // Long press actions
  function initLongPress() {
    let pressTimer;
    const messages = document.querySelectorAll('.message-content');
    
    messages.forEach(message => {
      message.addEventListener('touchstart', (e) => {
        pressTimer = setTimeout(() => {
          triggerHaptic('medium');
          showContextMenu(e.touches[0].clientX, e.touches[0].clientY, message);
        }, 500);
      });

      message.addEventListener('touchend', () => {
        clearTimeout(pressTimer);
      });

      message.addEventListener('touchmove', () => {
        clearTimeout(pressTimer);
      });
    });
  }

  // Context menu for mobile
  function showContextMenu(x, y, element) {
    const menu = document.createElement('div');
    menu.className = 'mobile-context-menu show';
    menu.style.left = `${x}px`;
    menu.style.top = `${y}px`;
    
    const copyItem = document.createElement('div');
    copyItem.className = 'mobile-context-menu-item';
    copyItem.innerHTML = '📋 Copy';
    copyItem.onclick = () => {
      navigator.clipboard.writeText(element.textContent);
      triggerHaptic('light');
      menu.remove();
    };
    
    const shareItem = document.createElement('div');
    shareItem.className = 'mobile-context-menu-item';
    shareItem.innerHTML = '📤 Share';
    shareItem.onclick = () => {
      if (navigator.share) {
        navigator.share({
          text: element.textContent
        });
      }
      menu.remove();
    };
    
    menu.appendChild(copyItem);
    menu.appendChild(shareItem);
    document.body.appendChild(menu);
    
    // Remove menu on outside click
    setTimeout(() => {
      document.addEventListener('click', () => menu.remove(), { once: true });
    }, 100);
  }

  // Smooth scroll to bottom
  function scrollToBottom() {
    const messages = document.querySelector('.messages');
    if (messages) {
      messages.scrollTo({
        top: messages.scrollHeight,
        behavior: 'smooth'
      });
    }
  }

  // Initialize mobile menu
  function initMobileMenu() {
    const menuToggle = document.createElement('button');
    menuToggle.className = 'mobile-nav-toggle';
    menuToggle.innerHTML = '☰';
    
    const header = document.querySelector('.header-content');
    if (header) {
      header.appendChild(menuToggle);
      
      menuToggle.addEventListener('click', () => {
        const menu = document.querySelector('.mobile-menu');
        if (menu) {
          menu.classList.toggle('open');
          triggerHaptic('light');
        }
      });
    }
  }

  // Performance optimizations
  function optimizePerformance() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          imageObserver.unobserve(img);
        }
      });
    });
    
    images.forEach(img => imageObserver.observe(img));

    // Debounce scroll events
    let scrollTimer;
    const messages = document.querySelector('.messages');
    if (messages) {
      messages.addEventListener('scroll', () => {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(() => {
          // Handle scroll end
        }, 150);
      });
    }
  }

  // Initialize all enhancements
  function init() {
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init);
      return;
    }

    handleKeyboard();
    initTouchGestures();
    enhanceButtons();
    enhanceVoiceInput();
    autoResizeInput();
    initLongPress();
    initMobileMenu();
    optimizePerformance();

    // Re-initialize on dynamic content
    const observer = new MutationObserver(() => {
      enhanceButtons();
      initLongPress();
    });

    const messages = document.querySelector('.messages');
    if (messages) {
      observer.observe(messages, { childList: true, subtree: true });
    }
  }

  init();

  // Expose functions for external use
  window.mobileEnhancements = {
    scrollToBottom,
    triggerHaptic,
    showContextMenu
  };
})();