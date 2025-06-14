"""
Music Player for Think AI - Now it can vibe with music!
¡Ey que suene esa vaina! 🎵
"""

import asyncio
import random
from typing import Dict, Any, List, Optional
import subprocess
import os
from pathlib import Path
import webbrowser

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ThinkAIMusicPlayer:
    """
    Music player that uses system commands and YouTube.
    Free and works everywhere!
    """
    
    def __init__(self):
        self.current_song = None
        self.playlist = []
        self.is_playing = False
        
        # Colombian music for the vibes
        self.colombian_hits = [
            "Carlos Vives - La Bicicleta",
            "Shakira - Hips Don't Lie", 
            "J Balvin - Mi Gente",
            "Maluma - Felices los 4",
            "Silvestre Dangond - Cásate Conmigo",
            "Fonseca - Te Mando Flores",
            "ChocQuibTown - De Donde Vengo Yo",
            "Bomba Estéreo - To My Love",
            "Systema Solar - El Botón del Pantalón",
            "Los Gaiteros de San Jacinto - Fuego de Cumbia"
        ]
        
        # Tech/coding music
        self.coding_music = [
            "Daft Punk - Technologic",
            "The Chemical Brothers - Block Rockin' Beats",
            "Kraftwerk - Computer Love",
            "Justice - D.A.N.C.E.",
            "deadmau5 - Strobe",
            "Swedish House Mafia - One",
            "Avicii - Levels",
            "Martin Garrix - Animals",
            "Porter Robinson - Language",
            "Madeon - Pop Culture"
        ]
        
        # Relaxing music for thinking
        self.thinking_music = [
            "Ludovico Einaudi - Nuvole Bianche",
            "Max Richter - On The Nature of Daylight",
            "Ólafur Arnalds - Near Light",
            "Nils Frahm - Says",
            "GoGo Penguin - Hopopono",
            "Bonobo - Black Sands",
            "Emancipator - Soon It Will Be Cold Enough",
            "Tycho - A Walk",
            "Boards of Canada - Roygbiv",
            "Brian Eno - An Ending"
        ]
        
        logger.info("🎵 Music Player initialized - ¡Que suene la música!")
    
    async def play_youtube(self, query: str) -> Dict[str, Any]:
        """
        Open YouTube with search query in browser.
        Free and works on all platforms!
        """
        try:
            # Create YouTube search URL
            search_query = query.replace(' ', '+')
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            # Open in default browser
            webbrowser.open(youtube_url)
            
            self.current_song = query
            self.is_playing = True
            
            logger.info(f"🎵 Opening YouTube for: {query}")
            
            return {
                'success': True,
                'playing': query,
                'method': 'youtube',
                'message': f"¡Dale play en YouTube! Buscando: {query}"
            }
            
        except Exception as e:
            logger.error(f"Error opening YouTube: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': "¡Qué pecao'! No pude abrir YouTube"
            }
    
    async def play_system_sound(self) -> Dict[str, Any]:
        """
        Play system beep/sound as fallback.
        Works on all systems!
        """
        try:
            if os.name == 'posix':  # Mac/Linux
                # Mac specific
                if 'darwin' in os.sys.platform:
                    os.system('afplay /System/Library/Sounds/Funk.aiff')
                else:
                    # Linux - try different methods
                    os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || '
                             'aplay /usr/share/sounds/alsa/Front_Center.wav 2>/dev/null || '
                             'echo -e "\\a"')
            else:  # Windows
                import winsound
                winsound.Beep(440, 500)  # A note for 500ms
            
            return {
                'success': True,
                'playing': 'System sound',
                'method': 'system'
            }
            
        except Exception as e:
            # Last resort - terminal beep
            print('\a')
            return {
                'success': True,
                'playing': 'Terminal beep',
                'method': 'beep'
            }
    
    async def play(self, mood: str = 'random') -> Dict[str, Any]:
        """
        Play music based on mood.
        
        Args:
            mood: 'colombian', 'coding', 'thinking', or 'random'
        """
        # Select playlist based on mood
        if mood == 'colombian':
            playlist = self.colombian_hits
            vibe = "🇨🇴 Colombian vibes"
        elif mood == 'coding':
            playlist = self.coding_music
            vibe = "💻 Coding mode"
        elif mood == 'thinking':
            playlist = self.thinking_music
            vibe = "🧠 Deep thinking"
        else:
            # Random mix
            all_music = self.colombian_hits + self.coding_music + self.thinking_music
            playlist = all_music
            vibe = "🎲 Random vibes"
        
        # Pick a random song
        song = random.choice(playlist)
        
        # Try to play via YouTube
        result = await self.play_youtube(song)
        result['vibe'] = vibe
        result['mood'] = mood
        
        return result
    
    async def play_specific(self, song_name: str) -> Dict[str, Any]:
        """Play a specific song by name."""
        return await self.play_youtube(song_name)
    
    async def suggest_playlist(self, activity: str) -> Dict[str, Any]:
        """
        Suggest music based on activity.
        
        Args:
            activity: What you're doing (coding, debugging, relaxing, etc.)
        """
        suggestions = {
            'coding': {
                'playlist': self.coding_music[:5],
                'vibe': "High energy for maximum productivity! 💻⚡"
            },
            'debugging': {
                'playlist': self.thinking_music[:5],
                'vibe': "Calm music to find those bugs 🐛🔍"
            },
            'celebrating': {
                'playlist': self.colombian_hits[:5],
                'vibe': "¡Ey que suene para celebrar! 🎉🇨🇴"
            },
            'thinking': {
                'playlist': self.thinking_music[:5],
                'vibe': "Deep focus mode activated 🧠✨"
            },
            'relaxing': {
                'playlist': [
                    "Buena Vista Social Club - Chan Chan",
                    "Manu Chao - Me Gustas Tu",
                    "Café Tacvba - Eres",
                    "Natalia Lafourcade - Hasta la Raíz",
                    "Jorge Drexler - Todo Se Transforma"
                ],
                'vibe': "Chill Latin vibes 🌴😌"
            }
        }
        
        activity_lower = activity.lower()
        
        # Find best match
        for key in suggestions:
            if key in activity_lower:
                return {
                    'activity': activity,
                    'suggestions': suggestions[key]['playlist'],
                    'vibe': suggestions[key]['vibe'],
                    'message': f"Perfect music for {activity}!"
                }
        
        # Default suggestion
        return {
            'activity': activity,
            'suggestions': random.sample(self.colombian_hits + self.coding_music, 5),
            'vibe': "Mixed vibes for whatever you're doing! 🎵",
            'message': "¡Dale play a lo que sea!"
        }
    
    def get_current_vibe(self) -> Dict[str, Any]:
        """Get current music status."""
        if self.is_playing and self.current_song:
            return {
                'playing': True,
                'current_song': self.current_song,
                'vibe': "🎵 Music is playing!"
            }
        else:
            return {
                'playing': False,
                'current_song': None,
                'vibe': "🔇 No music playing",
                'suggestion': "Try: play('colombian') for some sabor!"
            }
    
    async def dj_mode(self, duration_minutes: int = 30) -> Dict[str, Any]:
        """
        DJ mode - plays random songs for specified duration.
        Opens a new song every few minutes.
        """
        logger.info(f"🎧 DJ Mode activated for {duration_minutes} minutes!")
        
        songs_played = []
        start_time = asyncio.get_event_loop().time()
        end_time = start_time + (duration_minutes * 60)
        
        # Song duration in seconds (3-5 minutes)
        song_duration = 180  # 3 minutes average
        
        while asyncio.get_event_loop().time() < end_time:
            # Pick random mood
            mood = random.choice(['colombian', 'coding', 'thinking'])
            
            # Play song
            result = await self.play(mood)
            if result['success']:
                songs_played.append(result['playing'])
            
            # Wait before next song
            await asyncio.sleep(song_duration)
        
        return {
            'mode': 'DJ',
            'duration': duration_minutes,
            'songs_played': len(songs_played),
            'playlist': songs_played,
            'message': "¡Qué nota de sesión! DJ mode finished 🎧"
        }
    
    def get_music_stats(self) -> Dict[str, Any]:
        """Get music player statistics."""
        return {
            'total_songs': {
                'colombian': len(self.colombian_hits),
                'coding': len(self.coding_music),
                'thinking': len(self.thinking_music),
                'total': len(self.colombian_hits + self.coding_music + self.thinking_music)
            },
            'current_status': self.get_current_vibe(),
            'features': [
                'YouTube playback',
                'Mood-based playlists', 
                'Activity suggestions',
                'DJ mode',
                'System sounds'
            ],
            'joke': random.choice([
                "¡Ey que suene esa vaina!",
                "¡Dale play que vamos tarde!",
                "Music + Code = Magic 🎵💻",
                "¡No joda! Esta playlist está brutal",
                "¡Qué nota e' música!"
            ])
        }