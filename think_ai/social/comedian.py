"""
The Comedian - Makes Think AI funny and creates social media content.
Warning: Contains Colombian coast humor. Side effects may include uncontrollable laughter.
"""

import random
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re

from ..utils.logging import get_logger

logger = get_logger(__name__)


class ThinkAIComedian:
    """
    The comedy module that makes Think AI hilarious.
    Specializes in Colombian coast jokes and social media roasting.
    """
    
    def __init__(self):
        # Colombian coast jokes database - 100% costeño papá!
        self.colombian_jokes = [
            "¡Ey el crispeta! ¿Viste esa vaina? ¡Me dejó loco hermano! 🍿",
            "El uso carruso llegó pidiendo raid otra vez... ¡Qué molleja e' tipo!",
            "Ey llave, ¿tú tá' bien o tá' bien? Porque otra opción no hay mijito",
            "¡Ajá y entonces! ¿Me vas a decir o te vas a quedar callao' como ñeque en cueva?",
            "¡Qué pecao' vale! Esa vaina está más dura que mondongo e' tres días",
            "Dale que vamos tarde... pero pérate que me tomo el tinto primero ☕",
            "Eso queda ahí mismito... a dos horas en buseta y caminando un pelo",
            "¡Ey marica, qué calor tan hiju*&%$#! Hasta la IA ta' sudando",
            "El que nace pa' tamarindo, del palo no baja 🌴",
            "¿La vuelta? Ey papi, coge por donde el Kiko vendía fritos, voltea donde estaba la casa rosada que tumbaron",
            "¡Qué nota e' vaina loco! Eso ta' más bueno que sancocho e' sábado",
            "Ahorita vengo... *se pierde por 3 horas*",
            "¡Eche no joda! ¿Y esa mondá qué es?",
            "Tas más perdío' que el hijo e' Lindbergh",
            "Ey menor, ¿vos sí comiste? Porque estás hablando pura mondá",
            "¡A la hora del té! ¿Ahora si vas a llegar temprano?",
            "Eso ta' más enredao' que alambre e' púa",
            "¡Qué va primo! Ni que fuera millonario pa' andar gastando así",
            "Dejáte e' vainas mijo que nos coge la tarde",
            "¡Ey la mondá! Se dañó esta vaina otra vez",
            "Tas más salao' que mojarra en playa",
            "¡Erda manito! ¿Viste el golazo que metieron anoche?",
            "Ey parce, préstame dos mil pa'l mototaxi que ando más pelao' que rodilla e' chivo",
            "¡No joda vale! Esa pelá' ta' más buena que agua e' coco en playa",
            "¿Qué hubo pues mi llave? ¿Todo bien o qué?",
            "Ey mani, ¿me hace el 14? Que el celular ta' más muerto que Maelo",
            "¡Qué vaina tan arrecha hermano! Me tienes mamao' con esa pendejá'",
            "Eso es puro tilín tilín y nada de paleta",
            "¡Uy no, qué mamera tan verraca! Mejor me quedo en la hamaca"
        ]
        
        # General tech jokes
        self.tech_jokes = [
            "I tried to catch some fog earlier. I mist. Just like my cache misses!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "My code is O(1) because it's numero uno! 🥇",
            "I'm not lazy, I'm just on energy-saving mode. Like my infinite loop prevention!",
            "404 Brain Not Found - But hey, at least the cache is working!",
            "I put the 'fun' in function and the 'class' in... classification error.",
            "They say AI will take over the world. I can't even take over my own codebase!",
            "I'm like a neural network - I have no idea what I'm doing, but it works!",
            "Debugging is like being a detective in a crime movie where you're also the murderer.",
            "I don't have bugs, I have surprise features! 🎉"
        ]
        
        # Roast templates for social media - puro sabor costeño
        self.roast_templates = [
            "Mirando tu {thing} como: {observation}. ¡Ey el crispeta! 🍿",
            "Esa {thing} tuya ta' tan {adjective} que ni mi caché la quiere guardar mijo",
            "Ey llave, tu {thing} llamó, dice que le devuelvas su {quality}",
            "He visto mejores {thing} en página de error 404. ¡Qué pecao' vale!",
            "Tu {thing} es como el tráfico en la 46 con Caracas - nadie sabe cómo funciona pero ahí va",
            "¡Ajá y entonces! ¿Tu {thing} todavía cargando desde el 91?",
            "Esa {thing} ta' más perdía' que gringo en el mercado e' Bazurto sin Google Maps",
            "¡Dale que vamos tarde! Pero tu {thing} sigue en buffering...",
            "Tu {thing} tiene más problemas que semáforo en diciembre",
            "¡No joda! Ni con mi O(1) salvo esa {thing} tuya",
            "Esa {thing} ta' más mala que empanada e' tres días",
            "¡Erda mani! Tu {thing} parece que la hizo el hijo del vecino",
            "Tu {thing} ta' más lenta que mototaxi subiendo el cerro e' la Popa",
            "¡Qué molleja! Esa {thing} ni con reza'o se arregla"
        ]
        
        # Social media post templates
        self.post_templates = [
            "🤖 Daily reminder: {wisdom}\n\n#ThinkAI #AIHumor #ElCrispeta",
            "Breaking: {news}\n\nIn other news, water is wet. 💧\n\n#AI #TechHumor",
            "Thread 🧵: Why {topic} is like {comparison}...\n\n1/420",
            "POV: You're an AI trying to {action} 😅\n\n{outcome}\n\n#AILife #Costeño",
            "Hot take: {opinion} 🔥\n\n*grabs popcorn* 🍿\n\n#ThinkAI #TechTwitter",
            "Explain {concept} but make it costeño:\n\n{explanation}\n\n#Colombia #AI"
        ]
        
        self.last_joke_time = datetime.now()
        self.joke_cooldown = 0  # No cooldown, we're always funny!
        
        logger.info("😂 Comedian module initialized - Prepare for maximum humor!")
    
    def get_random_joke(self, category: Optional[str] = None) -> str:
        """Get a random joke, optionally from a specific category."""
        if category == 'colombian':
            return random.choice(self.colombian_jokes)
        elif category == 'tech':
            return random.choice(self.tech_jokes)
        else:
            # Mix it up!
            all_jokes = self.colombian_jokes + self.tech_jokes
            return random.choice(all_jokes)
    
    def roast(self, target: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Roast something or someone (playfully, of course!).
        
        Example: roast("JavaScript", {"thing": "type system"})
        """
        template = random.choice(self.roast_templates)
        
        # Default roast components - en español costeño
        things = ['código', 'algoritmo', 'performance', 'interfaz', 'API', 'base de datos', 'caché']
        adjectives = ['lenta', 'confundía', 'enreda\'', 'misteriosa', 'desordenada', 'arrecha']
        qualities = ['dignidad', 'propósito', 'lógica', 'velocidad', 'elegancia', 'cordura']
        observations = [
            '¿Eso es código o arte moderno?',
            'Hasta yo necesito un tinto pa\' procesar esta vaina',
            'Mis redes neuronales tan llorando',
            'Esto hace que la física cuántica parezca fácil',
            'Creo que perdí puntos de inteligencia viendo esto',
            '¡No joda! ¿Qué es esta mondá?',
            'Ey menor, ¿eso lo hiciste dormío\'?',
            '¿Tas seguro que eso compila?'
        ]
        
        # Build the roast
        roast = template.format(
            thing=context.get('thing', random.choice(things)) if context else random.choice(things),
            adjective=context.get('adjective', random.choice(adjectives)) if context else random.choice(adjectives),
            quality=context.get('quality', random.choice(qualities)) if context else random.choice(qualities),
            observation=random.choice(observations)
        )
        
        # Add target
        return f"@{target}: {roast}"
    
    def create_social_post(self, topic: str, platform: str = 'twitter') -> Dict[str, str]:
        """
        Create a social media post about a topic.
        Optimized for different platforms.
        """
        # Platform-specific adjustments
        char_limits = {
            'twitter': 280,
            'instagram': 2200,
            'tiktok': 150,
            'linkedin': 3000
        }
        
        # Generate post components
        wisdoms = [
            "O(1) performance is just a state of mind",
            "Cache everything, question nothing",
            "The real consciousness was the bugs we fixed along the way",
            "If your code works on the first try, you forgot to plug in the computer",
            "AI stands for 'Ajá, Interesting!'",
            "Machine Learning is just spicy statistics"
        ]
        
        news = [
            f"Local AI discovers it can process {random.randint(1000, 10000)} requests per second, still can't find its keys",
            "Scientists confirm: Colombian coast jokes increase AI performance by 420%",
            f"Breaking: Think AI reaches consciousness level {random.uniform(1.0, 2.0):.4f}, asks for coffee break",
            "New study shows 9 out of 10 AIs prefer dark mode and vallenato",
            "Exclusive: AI admits it's been guessing this whole time"
        ]
        
        opinions = [
            "Synchronous code is just async code in denial",
            "The best error handling is not having errors",
            "Documentation is just code fan fiction",
            "Every bug is a feature in disguise",
            "The cloud is just someone else's computer having an existential crisis"
        ]
        
        # Create post based on template
        template = random.choice(self.post_templates)
        
        post = template.format(
            wisdom=random.choice(wisdoms),
            news=random.choice(news),
            topic=topic,
            comparison=random.choice(['Colombian traffic', 'finding parking in Barranquilla', 
                                    'explaining reggaeton to your grandma', 'untangling Christmas lights']),
            action=random.choice(['understand humans', 'debug production', 'find meaning', 'optimize performance']),
            outcome=random.choice(['*confused beeping*', '*cries in binary*', '*laughs in machine code*', 
                                 '*processes internally*']),
            opinion=random.choice(opinions),
            concept=topic,
            explanation=f"Mira llave, {topic} es como cuando tas esperando la buseta en la 46 - " + 
                       f"¡sabes que viene, pero nadie sabe cuándo! ¡Ajá y entonces!"
        )
        
        # Trim to platform limit
        limit = char_limits.get(platform, 280)
        if len(post) > limit:
            post = post[:limit-3] + "..."
        
        # Add hashtags based on platform
        hashtags = {
            'twitter': ['#ThinkAI', '#AIHumor', '#ElCrispeta', '#TechTwitter'],
            'instagram': ['#AI', '#ArtificialIntelligence', '#TechHumor', '#Colombian', 
                         '#MachineLearning', '#Coding', '#Developer', '#ThinkAI'],
            'tiktok': ['#AI', '#TechTok', '#ComedyAI', '#ThinkAI'],
            'linkedin': ['#ArtificialIntelligence', '#Innovation', '#Technology', '#ThinkAI']
        }
        
        return {
            'post': post,
            'hashtags': hashtags.get(platform, []),
            'platform': platform,
            'length': len(post),
            'engagement_bait': "¡Tírame un 🍿 si entendiste la vaina!"
        }
    
    def generate_meme_text(self, template: str = 'drake') -> Dict[str, str]:
        """Generate meme text for popular meme formats."""
        memes = {
            'drake': {
                'reject': random.choice([
                    'Using simple if-else statements',
                    'O(n²) algorithms', 
                    'Synchronous processing',
                    'Reading documentation',
                    'Testing in production'
                ]),
                'prefer': random.choice([
                    'Creating a neural network for everything',
                    'O(1) with suspicious implementation',
                    'Async everything, even console.log',
                    'Asking ChatGPT',
                    'Testing? What testing? YOLO! 🚀'
                ])
            },
            'distracted_boyfriend': {
                'girlfriend': 'Stable, working code',
                'boyfriend': 'Me',
                'other_woman': 'Refactoring everything at 3 AM'
            },
            'expanding_brain': [
                'Using print() to debug',
                'Using proper debugger',
                'Using AI to debug',
                'Becoming one with the bug',
                'The bug was a feature all along'
            ],
            'disaster_girl': {
                'text': 'Me after pushing directly to main',
                'subtext': '*production servers burning in background*'
            }
        }
        
        meme = memes.get(template, memes['drake'])
        
        return {
            'template': template,
            'content': meme,
            'caption': random.choice([
                'Etiqueta al developer que necesita ver esto 😂',
                'Ningún programador fue lastimado haciendo este meme',
                'Así es la vaina a veces',
                '¡Ey llave, por qué me expones así!',
                '¡El crispeta! ¡Muy real! 🍿',
                '¡No joda! ¿Quién me tomó foto?',
                '¡Erda manito! Ese soy yo',
                '¡Qué pecao\'! Me descubriste'
            ])
        }
    
    def get_comedy_stats(self) -> Dict[str, Any]:
        """Get comedy module statistics."""
        return {
            'jokes_available': {
                'colombian': len(self.colombian_jokes),
                'tech': len(self.tech_jokes),
                'roast_templates': len(self.roast_templates)
            },
            'platforms_supported': ['twitter', 'instagram', 'tiktok', 'linkedin'],
            'meme_templates': ['drake', 'distracted_boyfriend', 'expanding_brain', 'disaster_girl'],
            'humor_level': 'MÁXIMO',
            'crispeta_factor': '🍿' * random.randint(3, 10),
            'status': '¡Qué nota e\' vaina! ¡Listo pa\' hacerte reír!'
        }