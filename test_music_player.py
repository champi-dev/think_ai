#!/usr/bin/env python3
"""
Test the music player - ¡Que suene!
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.music.music_player import ThinkAIMusicPlayer


async def test_music():
    """Test music functionality."""
    print("🎵 THINK AI MUSIC PLAYER TEST")
    print("="*50)
    
    player = ThinkAIMusicPlayer()
    
    print("\n1. Testing Colombian music:")
    result = await player.play('colombian')
    print(f"   Result: {result['message']}")
    
    await asyncio.sleep(2)
    
    print("\n2. Testing coding music:")
    result = await player.play('coding')
    print(f"   Result: {result['message']}")
    
    print("\n3. Getting suggestions for debugging:")
    suggestions = await player.suggest_playlist('debugging')
    print(f"   Vibe: {suggestions['vibe']}")
    print("   Suggested songs:")
    for song in suggestions['suggestions'][:3]:
        print(f"   - {song}")
    
    print("\n4. Music stats:")
    stats = player.get_music_stats()
    print(f"   Total songs: {stats['total_songs']['total']}")
    print(f"   Joke: {stats['joke']}")
    
    print("\n✅ Music player working! YouTube should have opened with music.")
    print("¡Dale que suene esa vaina! 🎵")


if __name__ == "__main__":
    asyncio.run(test_music())