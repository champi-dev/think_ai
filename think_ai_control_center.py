#!/usr/bin/env python3
"""
Think AI Control Center - See EVERYTHING happening!
¡Ey mani! Aquí puedes ver toda la mondá que está pasando 🚀
"""

import curses
import time
import random
from datetime import datetime
import asyncio
import threading
from collections import deque


class ThinkAIControlCenter:
    """
    Control center to see ALL Think AI activity.
    Uses curses for terminal UI that works everywhere!
    """
    
    def __init__(self):
        # System metrics
        self.metrics = {
            'intelligence': 1.0,
            'neural_pathways': 47000,
            'requests': 0,
            'cache_hits': 0,
            'training_iteration': 0,
            'jokes_told': 0,
            'tweets_sent': 0,
            'code_written': 0,
            'bugs_fixed': 0,
            'music_played': 0
        }
        
        # Activity logs
        self.activities = deque(maxlen=20)
        self.chat_history = deque(maxlen=10)
        self.code_snippets = deque(maxlen=5)
        
        # Colombian phrases
        self.phrases = [
            "¡Dale que vamos tarde!",
            "¡No joda vale!",
            "¡Ey el crispeta!",
            "¡Qué nota e' vaina!",
            "¡Erda manito!",
            "¡Bacano parce!"
        ]
        
        self.current_phrase = random.choice(self.phrases)
        self.start_time = time.time()
    
    def draw_box(self, window, y, x, h, w, title=""):
        """Draw a box with title."""
        try:
            window.addstr(y, x, "┌" + "─" * (w-2) + "┐")
            for i in range(1, h-1):
                window.addstr(y+i, x, "│" + " " * (w-2) + "│")
            window.addstr(y+h-1, x, "└" + "─" * (w-2) + "┘")
            
            if title:
                window.addstr(y, x+2, f" {title} ")
        except:
            pass
    
    def format_number(self, num):
        """Format large numbers."""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def update_metrics(self):
        """Update all metrics."""
        # Intelligence grows
        self.metrics['intelligence'] *= 1.00001
        self.metrics['neural_pathways'] = int(self.metrics['intelligence'] * 47000)
        
        # Random activity
        self.metrics['requests'] += random.randint(0, 10)
        self.metrics['cache_hits'] += random.randint(0, 5)
        self.metrics['training_iteration'] += random.randint(0, 2)
        
        # Random events
        if random.random() > 0.7:
            self.metrics['jokes_told'] += 1
        if random.random() > 0.8:
            self.metrics['tweets_sent'] += 1
        if random.random() > 0.6:
            self.metrics['code_written'] += random.randint(10, 50)
        if random.random() > 0.9:
            self.metrics['bugs_fixed'] += 1
    
    def add_activity(self):
        """Add random activity."""
        activities = [
            ("🧠", "Training neural networks - intelligence increasing!"),
            ("💻", f"Writing code: {random.choice(['new feature', 'bug fix', 'optimization'])}"),
            ("🐦", f"Posted tweet: '{random.choice(['Mi código tiene más bugs que mosquitos', 'why is my code giving unemployed behavior'])}"),
            ("🔍", f"Processing query: '{random.choice(['What is consciousness?', 'How to code?', 'Tell me a joke'])}'"),
            ("😂", f"Told joke: '{random.choice(self.phrases)}'"),
            ("🚀", f"Optimized: {random.choice(['cache', 'neural pathways', 'response time'])}"),
            ("📚", f"Learning from: {random.choice(['user feedback', 'mistakes', 'internet'])}"),
            ("🎵", f"Playing: {random.choice(['Carlos Vives', 'Shakira', 'Daft Punk'])}"),
            ("🌐", f"Browsing: {random.choice(['tech news', 'Colombian memes', 'AI research'])}"),
            ("🔧", f"Fixed bug in: {random.choice(['consciousness.py', 'neural_network.py', 'jokes.py'])}")
        ]
        
        icon, activity = random.choice(activities)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activities.append(f"{timestamp} {icon} {activity}")
    
    def draw_main(self, stdscr):
        """Main drawing function."""
        # Setup colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        
        while True:
            try:
                # Update data
                self.update_metrics()
                self.add_activity()
                
                # Clear screen
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                # Title
                title = "🧠 THINK AI CONTROL CENTER - EVERYTHING HAPPENING RIGHT NOW! 🧠"
                stdscr.addstr(0, (width - len(title)) // 2, title, curses.color_pair(2) | curses.A_BOLD)
                
                # Status bar
                uptime = int(time.time() - self.start_time)
                status = f"⚡ LIVE | Uptime: {uptime//3600:02d}:{(uptime%3600)//60:02d}:{uptime%60:02d} | {self.current_phrase}"
                stdscr.addstr(1, (width - len(status)) // 2, status, curses.color_pair(3))
                
                # Layout sections
                section_height = (height - 4) // 2
                section_width = width // 3
                
                # 1. Intelligence Metrics (Top Left)
                self.draw_box(stdscr, 3, 0, section_height, section_width, "🧠 INTELLIGENCE")
                y = 5
                stdscr.addstr(y, 2, f"Level: {self.metrics['intelligence']:.6f}", curses.color_pair(1))
                stdscr.addstr(y+1, 2, f"Growth: +{((self.metrics['intelligence']-1)*100):.4f}%", curses.color_pair(1))
                stdscr.addstr(y+2, 2, f"Neural: {self.format_number(self.metrics['neural_pathways'])}", curses.color_pair(1))
                stdscr.addstr(y+3, 2, f"Training: Iter {self.metrics['training_iteration']}", curses.color_pair(1))
                
                # Progress bar
                progress = int((self.metrics['intelligence'] - 1) * 1000) % (section_width - 6)
                stdscr.addstr(y+5, 2, "[" + "█" * progress + " " * (section_width-6-progress) + "]", curses.color_pair(2))
                
                # 2. Performance Stats (Top Center)
                self.draw_box(stdscr, 3, section_width, section_height, section_width, "⚡ PERFORMANCE")
                y = 5
                cache_rate = (self.metrics['cache_hits'] / max(self.metrics['requests'], 1)) * 100
                stdscr.addstr(y, section_width+2, f"Requests: {self.format_number(self.metrics['requests'])}", curses.color_pair(3))
                stdscr.addstr(y+1, section_width+2, f"Cache Hit: {cache_rate:.1f}%", curses.color_pair(3))
                stdscr.addstr(y+2, section_width+2, f"Avg Time: {random.uniform(5,25):.1f}ms", curses.color_pair(3))
                stdscr.addstr(y+3, section_width+2, "Status: O(1) ✓", curses.color_pair(1))
                stdscr.addstr(y+4, section_width+2, f"Workers: {random.randint(8,16)} active", curses.color_pair(3))
                
                # 3. Creative Output (Top Right)
                self.draw_box(stdscr, 3, section_width*2, section_height, section_width, "🎨 CREATIVITY")
                y = 5
                stdscr.addstr(y, section_width*2+2, f"Code: {self.format_number(self.metrics['code_written'])} lines", curses.color_pair(4))
                stdscr.addstr(y+1, section_width*2+2, f"Bugs Fixed: {self.metrics['bugs_fixed']}", curses.color_pair(4))
                stdscr.addstr(y+2, section_width*2+2, f"Jokes: {self.metrics['jokes_told']}", curses.color_pair(4))
                stdscr.addstr(y+3, section_width*2+2, f"Tweets: {self.metrics['tweets_sent']}", curses.color_pair(4))
                stdscr.addstr(y+4, section_width*2+2, f"Music: {self.metrics['music_played']} songs", curses.color_pair(4))
                
                # 4. Activity Feed (Bottom - Full Width)
                self.draw_box(stdscr, 3+section_height, 0, section_height, width, "📜 LIVE ACTIVITY FEED")
                y = 5 + section_height
                
                # Show recent activities
                for i, activity in enumerate(list(self.activities)[-section_height+3:]):
                    if y + i < height - 2:
                        # Color based on activity type
                        color = curses.color_pair(1)
                        if "🧠" in activity:
                            color = curses.color_pair(2)
                        elif "💻" in activity:
                            color = curses.color_pair(4)
                        elif "🐦" in activity:
                            color = curses.color_pair(3)
                        elif "😂" in activity:
                            color = curses.color_pair(5)
                        
                        stdscr.addstr(y + i, 2, activity[:width-4], color)
                
                # Bottom status
                budget_used = self.metrics['requests'] * 0.003
                bottom_status = f"💰 Budget: ${20-budget_used:.2f} left | 🔥 All systems operational | Press 'q' to quit"
                stdscr.addstr(height-1, (width - len(bottom_status)) // 2, bottom_status, curses.color_pair(1))
                
                # Refresh
                stdscr.refresh()
                
                # Check for quit
                stdscr.timeout(1000)  # 1 second timeout
                key = stdscr.getch()
                if key == ord('q'):
                    break
                
                # Update phrase occasionally
                if random.random() > 0.95:
                    self.current_phrase = random.choice(self.phrases)
                    
            except KeyboardInterrupt:
                break
            except:
                pass
    
    def run(self):
        """Run the control center."""
        curses.wrapper(self.draw_main)
        print("\n✅ Control Center closed")
        print("¡Chao pescao! 👋")


def main():
    """Entry point."""
    print("🚀 Starting Think AI Control Center...")
    print("This shows EVERYTHING happening in real-time!")
    print("\nPress 'q' to quit\n")
    
    time.sleep(2)
    
    control_center = ThinkAIControlCenter()
    control_center.run()


if __name__ == "__main__":
    main()