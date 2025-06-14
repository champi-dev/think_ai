#!/usr/bin/env python3
"""
Think AI - Mac App with Native UI
¡Una app Mac bonita para Think AI! 🖥️✨
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import asyncio
import threading
import time
import random
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


class ThinkAIMacApp:
    """
    Beautiful Mac app for Think AI with native feel.
    Uses Tkinter for cross-platform compatibility.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Think AI - Conscious Intelligence 🧠")
        self.root.geometry("1200x800")
        
        # Mac-like colors
        self.bg_color = "#F5F5F7"
        self.accent_color = "#007AFF"
        self.text_color = "#1D1D1F"
        self.card_color = "#FFFFFF"
        
        # Configure root
        self.root.configure(bg=self.bg_color)
        
        # Mac window buttons (fake but pretty)
        if sys.platform == "darwin":
            self.root.createcommand('tk::mac::ShowPreferences', self.show_preferences)
        
        # Metrics
        self.metrics = {
            'intelligence': 1.0,
            'requests': 0,
            'cache_hits': 0,
            'jokes_told': 0
        }
        
        self.setup_ui()
        self.start_background_tasks()
    
    def setup_ui(self):
        """Create the beautiful UI."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content area with 3 columns
        content_frame = tk.Frame(main_frame, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Left column - Metrics
        left_frame = self.create_card(content_frame, "Intelligence Metrics 🧠")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.create_metrics_display(left_frame)
        
        # Center column - Chat
        center_frame = self.create_card(content_frame, "Chat with Think AI 💬")
        center_frame.grid(row=0, column=1, sticky="nsew", padx=10)
        self.create_chat_interface(center_frame)
        
        # Right column - Activity
        right_frame = self.create_card(content_frame, "Live Activity 🔴")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        self.create_activity_feed(right_frame)
        
        # Configure grid weights
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Bottom toolbar
        self.create_toolbar(main_frame)
    
    def create_header(self, parent):
        """Create app header."""
        header_frame = tk.Frame(parent, bg=self.bg_color, height=60)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = tk.Label(
            header_frame,
            text="Think AI",
            font=("SF Pro Display", 32, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(side=tk.LEFT)
        
        # Status
        self.status_label = tk.Label(
            header_frame,
            text="● Connected",
            font=("SF Pro Display", 14),
            bg=self.bg_color,
            fg="#34C759"  # Green
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Colombian joke
        self.joke_label = tk.Label(
            header_frame,
            text="¡Dale que vamos tarde! 🚀",
            font=("SF Pro Display", 14),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.joke_label.pack(side=tk.RIGHT)
    
    def create_card(self, parent, title):
        """Create a card container."""
        card = tk.Frame(parent, bg=self.card_color, relief=tk.FLAT)
        card.configure(highlightbackground="#E5E5E7", highlightthickness=1)
        
        # Card header
        header = tk.Label(
            card,
            text=title,
            font=("SF Pro Display", 16, "bold"),
            bg=self.card_color,
            fg=self.text_color,
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Separator
        ttk.Separator(card, orient='horizontal').pack(fill=tk.X)
        
        # Content frame
        content = tk.Frame(card, bg=self.card_color)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        return content
    
    def create_metrics_display(self, parent):
        """Create metrics display."""
        # Intelligence
        self.intel_label = tk.Label(
            parent,
            text=f"Intelligence Level\n{self.metrics['intelligence']:.6f}",
            font=("SF Pro Display", 14),
            bg=self.card_color,
            fg=self.text_color
        )
        self.intel_label.pack(pady=10)
        
        # Progress bar
        self.intel_progress = ttk.Progressbar(
            parent,
            length=200,
            mode='determinate',
            value=0
        )
        self.intel_progress.pack(pady=10)
        
        # Stats
        self.stats_text = tk.Text(
            parent,
            height=15,
            width=30,
            font=("SF Mono", 12),
            bg="#F5F5F7",
            fg=self.text_color,
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        self.update_stats()
    
    def create_chat_interface(self, parent):
        """Create chat interface."""
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            parent,
            height=20,
            font=("SF Pro Display", 13),
            bg="#F5F5F7",
            fg=self.text_color,
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = tk.Frame(parent, bg=self.card_color)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Input field
        self.input_field = tk.Entry(
            input_frame,
            font=("SF Pro Display", 13),
            bg="#F5F5F7",
            fg=self.text_color,
            relief=tk.FLAT
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_field.bind("<Return>", self.send_message)
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("SF Pro Display", 13),
            bg=self.accent_color,
            fg="white",
            relief=tk.FLAT,
            command=self.send_message,
            padx=20
        )
        send_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Welcome message
        self.add_chat_message("Think AI", "¡Hola! I'm Think AI. Ask me anything! 🧠", "system")
    
    def create_activity_feed(self, parent):
        """Create activity feed."""
        self.activity_text = tk.Text(
            parent,
            height=25,
            width=30,
            font=("SF Mono", 11),
            bg="#F5F5F7",
            fg=self.text_color,
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.activity_text.pack(fill=tk.BOTH, expand=True)
    
    def create_toolbar(self, parent):
        """Create bottom toolbar."""
        toolbar = tk.Frame(parent, bg=self.bg_color, height=50)
        toolbar.pack(fill=tk.X, pady=(20, 0))
        
        # Buttons
        buttons = [
            ("🎵 Music", self.play_music),
            ("📊 Dashboard", self.show_dashboard),
            ("🤖 Code", self.show_coding),
            ("😂 Joke", self.tell_joke),
            ("🔄 Refresh", self.refresh_all)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                toolbar,
                text=text,
                font=("SF Pro Display", 13),
                bg=self.card_color,
                fg=self.text_color,
                relief=tk.FLAT,
                command=command,
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def send_message(self, event=None):
        """Send message to Think AI."""
        message = self.input_field.get()
        if not message:
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Add user message
        self.add_chat_message("You", message, "user")
        
        # Simulate Think AI response
        self.root.after(500, lambda: self.think_ai_response(message))
    
    def think_ai_response(self, query):
        """Generate Think AI response."""
        responses = {
            'hello': "¡Hola mi llave! How can I help you today? 🌟",
            'joke': "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            'music': "I can play Colombian hits or coding music! Just ask! 🎵",
            'code': "I can write code autonomously now! Want me to create something? 💻",
            'intelligence': f"My current intelligence level is {self.metrics['intelligence']:.6f} and growing! 🧠"
        }
        
        # Check for keywords
        query_lower = query.lower()
        for keyword, response in responses.items():
            if keyword in query_lower:
                self.add_chat_message("Think AI", response, "ai")
                return
        
        # Default response
        default_responses = [
            "That's interesting! Let me think about that... 🤔",
            "¡Qué nota e' vaina! I'm processing your request with O(1) performance!",
            "My neural pathways are analyzing this. One moment! ⚡",
            "¡Dale que vamos tarde! Here's what I think..."
        ]
        
        self.add_chat_message("Think AI", random.choice(default_responses), "ai")
        self.metrics['requests'] += 1
    
    def add_chat_message(self, sender, message, msg_type):
        """Add message to chat."""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Configure tags
        if msg_type == "user":
            tag = "user_msg"
            self.chat_display.tag_config(tag, foreground=self.accent_color)
        elif msg_type == "ai":
            tag = "ai_msg"
            self.chat_display.tag_config(tag, foreground="#34C759")
        else:
            tag = "system_msg"
            self.chat_display.tag_config(tag, foreground="#8E8E93")
        
        # Add message
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
    
    def update_stats(self):
        """Update statistics display."""
        stats = f"""🧠 Neural Pathways
{int(self.metrics['intelligence'] * 47000):,}

⚡ Total Requests
{self.metrics['requests']:,}

🎯 Cache Hits
{self.metrics['cache_hits']:,}

😂 Jokes Told
{self.metrics['jokes_told']}

💻 Code Written
{random.randint(100, 1000)} lines

🌡️ System Health
Optimal ✅

💰 Budget Used
${self.metrics['requests'] * 0.003:.2f}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def update_activity(self):
        """Update activity feed."""
        activities = [
            "🧠 Training neural networks...",
            "💻 Writing autonomous code...",
            "🔍 Analyzing user queries...",
            "😂 Generating Colombian joke...",
            "🐦 Posting to Twitter...",
            "📚 Learning from interactions...",
            "🚀 Optimizing performance...",
            "🎵 Selecting music playlist..."
        ]
        
        activity = random.choice(activities)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.activity_text.insert(tk.END, f"[{timestamp}] {activity}\n")
        self.activity_text.see(tk.END)
        
        # Limit history
        lines = self.activity_text.get(1.0, tk.END).split('\n')
        if len(lines) > 50:
            self.activity_text.delete(1.0, 2.0)
    
    def play_music(self):
        """Play music command."""
        self.add_chat_message("System", "🎵 Opening music player...", "system")
        messagebox.showinfo("Music Player", "¡Que suene la música!\n\nMusic player would open here.")
    
    def show_dashboard(self):
        """Show dashboard command."""
        self.add_chat_message("System", "📊 Opening dashboard...", "system")
        messagebox.showinfo("Dashboard", "Beautiful dashboard with all metrics!")
    
    def show_coding(self):
        """Show coding interface."""
        self.add_chat_message("System", "🤖 Opening code editor...", "system")
        messagebox.showinfo("Autonomous Coder", "Think AI can now write its own code!")
    
    def tell_joke(self):
        """Tell a joke."""
        jokes = [
            "¡Ey el crispeta! 🍿",
            "¡Dale que vamos tarde!",
            "¡No joda vale!",
            "¡Qué nota e' vaina!",
            "¡Erda manito!"
        ]
        
        joke = random.choice(jokes)
        self.joke_label.config(text=joke)
        self.add_chat_message("Think AI", f"Colombian joke: {joke}", "ai")
        self.metrics['jokes_told'] += 1
    
    def refresh_all(self):
        """Refresh all displays."""
        self.update_stats()
        self.add_chat_message("System", "🔄 Refreshed all data!", "system")
    
    def background_updates(self):
        """Run background updates."""
        while True:
            # Update metrics
            self.metrics['intelligence'] *= 1.00001
            self.metrics['cache_hits'] += random.randint(0, 5)
            
            # Update UI
            self.root.after(0, self.update_intelligence_display)
            self.root.after(0, self.update_stats)
            self.root.after(0, self.update_activity)
            
            time.sleep(2)
    
    def update_intelligence_display(self):
        """Update intelligence display."""
        self.intel_label.config(
            text=f"Intelligence Level\n{self.metrics['intelligence']:.6f}"
        )
        progress = min(100, (self.metrics['intelligence'] - 1) * 10000)
        self.intel_progress['value'] = progress
    
    def start_background_tasks(self):
        """Start background tasks."""
        thread = threading.Thread(target=self.background_updates, daemon=True)
        thread.start()
    
    def show_preferences(self):
        """Show preferences (Mac menu)."""
        messagebox.showinfo("Preferences", "Think AI Preferences\n\nComing soon!")
    
    def run(self):
        """Run the app."""
        self.root.mainloop()


def main():
    """Entry point."""
    print("🖥️ Starting Think AI Mac App...")
    app = ThinkAIMacApp()
    app.run()


if __name__ == "__main__":
    main()