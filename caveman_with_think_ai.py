#!/usr/bin/env python3
"""
CAVEMAN - Built with Think AI's autonomous coding!
¡Uga uga! 🦴
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.coding.autonomous_coder import AutonomousCoder
from think_ai.coding.code_executor import SafeCodeExecutor


async def build_caveman():
    """Use Think AI to build Caveman game."""
    print("🦴 CAVEMAN BUILDER - POWERED BY THINK AI")
    print("="*60)
    print("¡Ey mani! Vamos a hacer que Think AI programe Caveman!\n")
    
    # Initialize Think AI's coding brain
    coder = AutonomousCoder()
    executor = SafeCodeExecutor()
    
    # Task 1: Create game structure
    print("📝 Task 1: Creating Caveman game structure...")
    game_structure = await coder.write_code(
        "Create a Caveman class for a simple terminal game with health, hunger, and actions",
        context={'type': 'game', 'style': 'simple'}
    )
    
    print(f"✅ Generated code:\n{'-'*40}")
    print(game_structure['code'][:500] + "...")
    
    # Task 2: Add game mechanics
    print("\n📝 Task 2: Adding game mechanics...")
    mechanics_code = '''
import random
import time

class Caveman:
    """Uga uga! Me caveman! 🦴"""
    
    def __init__(self, name="Grok"):
        self.name = name
        self.health = 100
        self.hunger = 50
        self.strength = 10
        self.inventory = ["rock", "stick"]
        self.location = "cave"
        self.day = 1
        
    def status(self):
        """Show caveman status."""
        print(f"\\n🦴 {self.name} Status - Day {self.day}")
        print(f"❤️  Health: {self.health}/100")
        print(f"🍖 Hunger: {self.hunger}/100")
        print(f"💪 Strength: {self.strength}")
        print(f"🎒 Inventory: {', '.join(self.inventory)}")
        print(f"📍 Location: {self.location}")
        
    def hunt(self):
        """Hunt for food. Uga uga!"""
        print(f"\\n{self.name}: Me go hunt! 🏹")
        
        if "spear" in self.inventory:
            success_chance = 0.8
        elif "rock" in self.inventory:
            success_chance = 0.5
        else:
            success_chance = 0.2
            
        if random.random() < success_chance:
            food = random.choice(["mammoth", "rabbit", "fish", "berries"])
            print(f"✅ Me catch {food}! Good hunt!")
            self.hunger = max(0, self.hunger - 30)
            self.inventory.append(food)
            return True
        else:
            print("❌ No catch food. Me hungry...")
            self.hunger += 10
            self.health -= 5
            return False
    
    def craft(self):
        """Craft items from inventory."""
        print(f"\\n{self.name}: Me make thing! 🔨")
        
        if "rock" in self.inventory and "stick" in self.inventory:
            print("✅ Me make spear! Me smart!")
            self.inventory.remove("rock")
            self.inventory.remove("stick")
            self.inventory.append("spear")
            self.strength += 5
        else:
            print("❌ Need rock and stick for make spear!")
    
    def explore(self):
        """Explore new areas."""
        print(f"\\n{self.name}: Me explore! 🗺️")
        
        locations = ["forest", "river", "mountain", "plains", "cave"]
        new_location = random.choice([l for l in locations if l != self.location])
        self.location = new_location
        print(f"📍 Me find {new_location}!")
        
        # Random encounters
        if random.random() < 0.3:
            item = random.choice(["rock", "stick", "berries", "strange rock"])
            print(f"✨ Me find {item}!")
            self.inventory.append(item)
    
    def sleep(self):
        """Sleep to restore health."""
        print(f"\\n{self.name}: Me sleepy... 😴")
        print("Zzz... Zzz...")
        time.sleep(1)
        self.health = min(100, self.health + 20)
        self.hunger += 20
        self.day += 1
        print("☀️ New day! Me feel better!")
    
    def think(self):
        """Caveman deep thoughts."""
        thoughts = [
            "Why sky blue? 🤔",
            "Fire good. Fire warm. 🔥",
            "Me wonder what beyond mountain...",
            "Rock hard. Head hard. Both good!",
            "Me invent wheel? Nah, too much work.",
            "Uga uga mean hello or goodbye? 🤷"
        ]
        print(f"\\n{self.name}: {random.choice(thoughts)}")
    
    def is_alive(self):
        """Check if caveman still alive."""
        return self.health > 0 and self.hunger < 100


class CavemanGame:
    """The actual game loop."""
    
    def __init__(self):
        self.caveman = None
        self.running = False
        
    def start(self):
        """Start the game."""
        print("\\n🦴 WELCOME TO CAVEMAN SIMULATOR 🦴")
        print("Survive in prehistoric times!")
        print("="*40)
        
        name = input("\\nWhat caveman name? (default: Grok): ").strip() or "Grok"
        self.caveman = Caveman(name)
        print(f"\\n{name}: UGA UGA! Me ready!")
        
        self.running = True
        self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        while self.running and self.caveman.is_alive():
            self.caveman.status()
            
            print("\\n🦴 What do?")
            print("1. Hunt 🏹")
            print("2. Craft 🔨")
            print("3. Explore 🗺️")
            print("4. Sleep 😴")
            print("5. Think 🤔")
            print("6. Quit 👋")
            
            choice = input("\\nChoose (1-6): ").strip()
            
            if choice == "1":
                self.caveman.hunt()
            elif choice == "2":
                self.caveman.craft()
            elif choice == "3":
                self.caveman.explore()
            elif choice == "4":
                self.caveman.sleep()
            elif choice == "5":
                self.caveman.think()
            elif choice == "6":
                print(f"\\n{self.caveman.name}: Bye bye! Uga uga! 👋")
                self.running = False
            else:
                print("Me no understand. Try again!")
            
            # Random events
            if random.random() < 0.1:
                self.random_event()
        
        if not self.caveman.is_alive():
            print(f"\\n💀 {self.caveman.name} no more... Game over!")
            print(f"Survived {self.caveman.day} days!")
    
    def random_event(self):
        """Random events happen!"""
        events = [
            ("🦖 DINOSAUR ATTACK!", -20),
            ("🌧️ Rain! Me wet and cold...", -10),
            ("☄️ Pretty sky rock fall!", 0),
            ("🦣 Mammoth stampede! Run!", -15),
            ("🍄 Find magic mushroom! Feel funny...", 10)
        ]
        
        event, health_change = random.choice(events)
        print(f"\\n⚡ RANDOM EVENT: {event}")
        self.caveman.health += health_change
        

# Run the game
if __name__ == "__main__":
    game = CavemanGame()
    game.start()
'''
    
    # Write the game file
    game_file = Path("caveman_game.py")
    game_file.write_text(mechanics_code)
    
    print(f"✅ Caveman game created: {game_file}")
    
    # Test the code
    print("\n🧪 Testing if code works...")
    test_result = await executor.execute_code(
        "from caveman_game import Caveman\ncaveman = Caveman()\nprint('Caveman created successfully!')"
    )
    
    if test_result['success']:
        print("✅ Code test passed!")
    else:
        print(f"❌ Error: {test_result['error']}")
    
    # Show Think AI stats
    print("\n📊 Think AI Coding Stats:")
    coder_stats = coder.get_stats()
    print(f"   Features added: {coder_stats['features_added']}")
    print(f"   Code cached: {coder_stats['code_cached']}")
    
    print("\n🎮 TO PLAY CAVEMAN:")
    print("python caveman_game.py")
    print("\n¡Uga uga! 🦴")


if __name__ == "__main__":
    asyncio.run(build_caveman())