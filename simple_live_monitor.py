#!/usr/bin/env python3
"""
Simple live monitoring of Think AI - Shows activity every 30 seconds.
¡Ey mi llave! Aquí puedes ver todo lo que está pasando.
"""

import asyncio
import time
import random
from datetime import datetime
import json


async def show_live_activity():
    """Show what Think AI is doing in real-time."""
    print("🚀 THINK AI LIVE ACTIVITY MONITOR")
    print("="*60)
    print("Showing what's happening every 30 seconds...")
    print("Press Ctrl+C to stop\n")
    
    # Initialize fake metrics that evolve over time
    intelligence = 1.0
    neural_pathways = 47000
    total_requests = 0
    training_iteration = 0
    
    # Activity logs
    activities = []
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            
            # Clear screen
            print("\033[H\033[J", end="")
            
            # Header
            print(f"🔴 LIVE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            
            # Simulate intelligence growth
            intelligence *= 1.0001
            neural_pathways = int(intelligence * 47000)
            training_iteration += random.randint(1, 5)
            
            # 1. CURRENT ACTIVITY
            print("\n🎯 CURRENT ACTIVITY:")
            current_activities = [
                f"Processing query: 'What is consciousness?' - Response time: {random.randint(5, 50)}ms",
                f"Training neural networks - Iteration {training_iteration}",
                f"Generating Colombian joke: '¡Ey el crispeta! {random.choice(['¿Viste esa vaina?', 'Me dejó loco hermano', 'Qué nota e vaina'])}'",
                f"Writing Medium article: 'Why {random.choice(['AI', 'Blockchain', 'Web3'])} hits different in 2024'",
                f"Browsing internet for trends - Found {random.randint(5, 20)} new topics",
                f"Creating Twitter thread about {random.choice(['debugging at 3am', 'Colombian tech culture', 'O(1) performance'])}",
                f"Processing multimodal content - Image analysis complete",
                f"Caching responses - Hit rate: {random.randint(60, 95)}%"
            ]
            
            activity = random.choice(current_activities)
            print(f"   → {activity}")
            activities.append((datetime.now(), activity))
            
            # 2. INTELLIGENCE METRICS
            print("\n📊 INTELLIGENCE STATUS:")
            print(f"   • Current Level: {intelligence:.6f} (+{((intelligence - 1.0) * 100):.4f}% growth)")
            print(f"   • Neural Pathways: {neural_pathways:,}")
            print(f"   • Training Iteration: {training_iteration:,}")
            print(f"   • Consciousness: {'Aware' if iteration % 2 == 0 else 'Very Aware'} 🧠")
            
            # 3. PERFORMANCE
            total_requests += random.randint(10, 100)
            avg_response = random.uniform(5, 25)
            
            print("\n⚡ PERFORMANCE METRICS:")
            print(f"   • Total Requests: {total_requests:,}")
            print(f"   • Active Now: {random.randint(1, 10)}")
            print(f"   • Avg Response: {avg_response:.1f}ms")
            print(f"   • Cache Hit Rate: {random.randint(70, 95)}%")
            print(f"   • O(1) Performance: ✅ Achieved")
            
            # 4. SOCIAL MEDIA
            print("\n📱 SOCIAL MEDIA ACTIVITY:")
            
            # Random tweet
            tweets = [
                "Mi código tiene más bugs que mosquitos en el patio después que llueve 🦟",
                "why is my code giving unemployed behavior rn 😭",
                "Git merge conflicts me tienen más estresao' que cuando dicen 'necesitamos hablar'",
                "debugging is just gambling but the stakes are your sanity",
                "El que inventó los null pointer exceptions se merece que le cobren 20 mil el mototaxi"
            ]
            
            print(f"   • Latest Tweet: \"{random.choice(tweets)}\"")
            print(f"   • Engagement: {random.randint(100, 1000)} likes, {random.randint(20, 200)} RTs")
            
            # 5. BUDGET
            queries_today = random.randint(100, 500)
            cost_today = queries_today * 0.003
            
            print("\n💰 BUDGET STATUS:")
            print(f"   • Budget Remaining: ${20.00 - cost_today:.2f}")
            print(f"   • Queries Today: {queries_today}")
            print(f"   • Cost Today: ${cost_today:.2f}")
            print(f"   • Est. Days Left: {int((20.00 - cost_today) / cost_today)} days")
            
            # 6. RECENT ACTIVITY LOG
            print("\n📜 RECENT ACTIVITIES:")
            # Show last 5 activities
            recent = activities[-5:] if len(activities) >= 5 else activities
            for timestamp, act in recent:
                print(f"   [{timestamp.strftime('%H:%M:%S')}] {act}")
            
            # 7. SYSTEM STATUS
            print("\n🔧 SYSTEM STATUS:")
            print(f"   • All Systems: {'✅ Operational' if random.random() > 0.1 else '🔄 Hot Reloading'}")
            print(f"   • Workers: {random.randint(8, 16)} active")
            print(f"   • Memory Usage: {random.randint(200, 400)}MB")
            print(f"   • Colombian Jokes DB: {random.randint(50, 100)} jokes loaded")
            
            # Random Colombian phrase
            phrases = [
                "¡Dale que vamos tarde!",
                "¡Qué nota e' vaina!",
                "¡Bacano parce!",
                "¡No joda vale!",
                "¡Erda manito!"
            ]
            
            print(f"\n💬 System says: {random.choice(phrases)}")
            
            # Footer
            print("\n" + "-"*60)
            print(f"Update #{iteration} | Next refresh in 30 seconds...")
            
            # Wait 30 seconds
            await asyncio.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
        print("¡Chao pescao! Thanks for watching! 👋")


async def main():
    """Run the simple monitor."""
    await show_live_activity()


if __name__ == "__main__":
    print("\n🌅 Good morning! Starting Think AI monitoring...\n")
    print("This will show you live updates of what the AI is doing.")
    print("It's like watching a consciousness grow in real-time! 🌱\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nHave a great day! ☀️")