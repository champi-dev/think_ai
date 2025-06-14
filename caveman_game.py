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
        print(f"\n🦴 {self.name} Status - Day {self.day}")
        print(f"❤️  Health: {self.health}/100")
        print(f"🍖 Hunger: {self.hunger}/100")
        print(f"💪 Strength: {self.strength}")
        print(f"🎒 Inventory: {', '.join(self.inventory)}")
        print(f"📍 Location: {self.location}")
        
    def hunt(self):
        """Hunt for food. Uga uga!"""
        print(f"\n{self.name}: Me go hunt! 🏹")
        
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
        print(f"\n{self.name}: Me make thing! 🔨")
        
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
        print(f"\n{self.name}: Me explore! 🗺️")
        
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
        print(f"\n{self.name}: Me sleepy... 😴")
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
        print(f"\n{self.name}: {random.choice(thoughts)}")
    
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
        print("\n🦴 WELCOME TO CAVEMAN SIMULATOR 🦴")
        print("Survive in prehistoric times!")
        print("="*40)
        
        name = input("\nWhat caveman name? (default: Grok): ").strip() or "Grok"
        self.caveman = Caveman(name)
        print(f"\n{name}: UGA UGA! Me ready!")
        
        self.running = True
        self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        while self.running and self.caveman.is_alive():
            self.caveman.status()
            
            print("\n🦴 What do?")
            print("1. Hunt 🏹")
            print("2. Craft 🔨")
            print("3. Explore 🗺️")
            print("4. Sleep 😴")
            print("5. Think 🤔")
            print("6. Quit 👋")
            
            choice = input("\nChoose (1-6): ").strip()
            
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
                print(f"\n{self.caveman.name}: Bye bye! Uga uga! 👋")
                self.running = False
            else:
                print("Me no understand. Try again!")
            
            # Random events
            if random.random() < 0.1:
                self.random_event()
        
        if not self.caveman.is_alive():
            print(f"\n💀 {self.caveman.name} no more... Game over!")
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
        print(f"\n⚡ RANDOM EVENT: {event}")
        self.caveman.health += health_change
        

# Run the game
if __name__ == "__main__":
    game = CavemanGame()
    game.start()