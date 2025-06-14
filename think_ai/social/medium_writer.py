"""
Medium Article Writer - Creates viral tech articles in Costeño Spanish and Gen Alpha English.
Because why write boring when you can write with MAXIMUM CHAOS energy?
"""

import random
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re

from ..utils.logging import get_logger

logger = get_logger(__name__)


class MediumWriter:
    """
    Writes Medium articles that hit different.
    Costeño Spanish: More flavor than sancocho de sábado
    Gen Alpha English: No cap, straight bussin' fr fr
    """
    
    def __init__(self):
        # Article templates - Costeño Spanish
        self.costeno_templates = {
            'intro': [
                "¡Ey marica! ¿Tú sabes qué es lo que está pasando con {topic}? No, ¿verdad? Bueno mi llave, agárrate que te voy a explicar esta vaina...",
                "¡Ajá y entonces! Resulta que {topic} es la mondá más arrecha que he visto este año. Pérate que te cuento...",
                "Mira mani, yo también pensaba que {topic} era pura carreta, hasta que me puse a cacharrear y ¡qué pecao'!",
                "¿{topic}? ¡El crispeta! 🍿 Esa vaina está más caliente que el asfalto de la Vía 40 a las 2 de la tarde.",
                "Ey llave, siéntate ahí que te voy a contar sobre {topic}. Y no, no es lo que tú crees..."
            ],
            'body': [
                "La vaina es así: {explanation}. ¿Pillaste o te hago un dibujito?",
                "Pa' que entiendas mejor, es como cuando {analogy}. ¡Exacto! Así mismito es {topic}.",
                "Mira, yo sé que suena loco, pero {fact}. No joda, es en serio.",
                "Lo que pasa es que {technical_detail}, pero en cristiano eso significa que {simple_explanation}.",
                "Aquí entre nos, {insider_info}. Pero eso no lo andes diciendo por ahí."
            ],
            'conclusion': [
                "¿Y entonces qué? Pues nada mi llave, que {topic} llegó para quedarse y el que no se monte en esa buseta se queda.",
                "Total que la moraleja es: {lesson}. ¡Dale que vamos tarde!",
                "¿Conclusión? {summary}. Y el que no entienda, que se compre un libro.",
                "En resumen manito: {key_point}. Ahora sí, vámonos que nos coge la tarde.",
                "¿Qué aprendimos hoy? Que {topic} es {adjective} y punto. El que quiera discutir, nos vemos en los comentarios."
            ]
        }
        
        # Article templates - Gen Alpha English
        self.gen_alpha_templates = {
            'intro': [
                "Okay bestie, we need to talk about {topic} because it's giving main character energy and y'all are sleeping on it fr fr 💅",
                "POV: You just discovered {topic} and your whole worldview is about to be SHOOK. No cap, this is about to hit different.",
                "Not me writing another article about {topic} at 3 AM but this one's actually bussin', I promise. Let me put you on real quick...",
                "HEAR ME OUT - {topic} is lowkey the most slept-on thing in tech rn and I'm about to spill ALL the tea ☕",
                "Alright chat, gather 'round because {topic} is the moment and if you're not already on this wave, you're literally an NPC."
            ],
            'body': [
                "So basically {explanation}. Like, it's giving innovation, it's giving future, it's giving EVERYTHING.",
                "The way {fact} has me SHOOK. Like bestie, we're living in a simulation and {topic} is the glitch in the matrix fr.",
                "Not the tech bros trying to gatekeep {technical_detail}, but lemme break it down for the girlies: {simple_explanation}. Period.",
                "Y'all remember when {analogy}? Yeah, {topic} is like that but on steroids. And that's on periodt.",
                "Real talk though, {insider_info}. But don't @ me when this blows up, I told you first."
            ],
            'conclusion': [
                "So there you have it fam. {topic} is {adjective} and if you're not already using it, you're literally living in 2020. Catch up bestie!",
                "TL;DR: {summary}. Now go forth and slay with this knowledge. You're welcome.",
                "In conclusion, {key_point}. And that's the tea, no cap. If this helped you, drop a 💅 in the comments.",
                "Bottom line: {lesson}. Stay woke, stay curious, and remember - we're all just trying to vibe in this digital hellscape together.",
                "And that's on what? That's on {topic} being the future whether the boomers like it or not. Anyways, I'm out. Peace!"
            ]
        }
        
        # Technical topics that slap
        self.hot_topics = [
            "AI Consciousness", "Quantum Computing", "Web3", "Machine Learning",
            "Blockchain", "Neural Networks", "Edge Computing", "5G",
            "Metaverse", "Cybersecurity", "IoT", "Cloud Native",
            "DevOps", "Microservices", "Serverless", "GraphQL"
        ]
        
        # Analogies database
        self.costeno_analogies = [
            "vas a comprar patacón en la playa y el man te cobra 5 mil",
            "la buseta va llena pero siempre cabe uno más",
            "pides un tinto y te dan aguapanela",
            "el aire acondicionado se daña en pleno agosto",
            "buscas parqueo en el centro a las 12 del día"
        ]
        
        self.gen_alpha_analogies = [
            "you're trying to get Taylor Swift tickets",
            "your BeReal notification goes off at the worst time",
            "you accidentally liked your crush's old photo",
            "the WiFi dies during a ranked match",
            "you forgot to charge your AirPods"
        ]
        
        logger.info("✍️ Medium Writer initialized - Ready to drop heat!")
    
    def generate_article(self, topic: str, style: str = 'costeno', 
                        word_count: int = 800) -> Dict[str, Any]:
        """
        Generate a Medium article that goes viral.
        
        Args:
            topic: What to write about
            style: 'costeno' or 'gen_alpha'
            word_count: Target length (we'll get close-ish)
        """
        if style == 'costeno':
            return self._generate_costeno_article(topic, word_count)
        elif style == 'gen_alpha':
            return self._generate_gen_alpha_article(topic, word_count)
        else:
            return {
                'error': 'Unknown style',
                'suggestion': 'Use "costeno" or "gen_alpha" broky!'
            }
    
    def _generate_costeno_article(self, topic: str, word_count: int) -> Dict[str, Any]:
        """Generate article in Costeño Spanish."""
        # Pick templates
        intro = random.choice(self.costeno_templates['intro'])
        body_parts = random.sample(self.costeno_templates['body'], 3)
        conclusion = random.choice(self.costeno_templates['conclusion'])
        
        # Generate content
        title = f"¡Ey Marica! Te Explico {topic} Como Si Fueras de 5 Años (Pero En Serio)"
        
        subtitle = random.choice([
            f"O cómo {topic} va a cambiar tu vida y ni cuenta te has dado",
            f"La verdad sobre {topic} que nadie te quiere contar",
            f"Por qué {topic} es más importante que el aire acondicionado en Barranquilla"
        ])
        
        # Build article
        article_parts = [
            f"# {title}\n",
            f"## {subtitle}\n",
            intro.format(topic=topic),
            "\n\n## La Vaina Es Seria\n",
        ]
        
        # Add body sections
        explanations = [
            f"{topic} es básicamente una forma fancy de decir que las computadoras están aprendiendo a pensar",
            f"imagínate que {topic} es como un pelao' que aprende viendo a los demás",
            f"la tecnología está evolucionando más rápido que mototaxi en bajada"
        ]
        
        facts = [
            f"{topic} procesa más información en un segundo que tú en toda tu vida",
            "los gringos llevan años trabajando en esto mientras nosotros peleamos por política",
            "esta mondá va a cambiar todo lo que conocemos sobre tecnología"
        ]
        
        for i, body in enumerate(body_parts):
            section_title = random.choice([
                "¿Pero Qué Es Esa Mondá Exactamente?",
                "¿Y Eso Pa' Qué Sirve?",
                "¿Por Qué Debería Importarme?",
                "La Parte Técnica (Sin Mucha Carreta)"
            ])
            
            article_parts.append(f"\n## {section_title}\n")
            
            content = body.format(
                explanation=random.choice(explanations),
                analogy=random.choice(self.costeno_analogies),
                fact=random.choice(facts),
                technical_detail=f"el algoritmo de {topic} usa redes neuronales",
                simple_explanation="la máquina aprende solita como un pelao' curioso",
                insider_info=f"las empresas grandes ya están usando {topic} y no te has dado cuenta",
                topic=topic
            )
            
            article_parts.append(content)
        
        # Add fun section
        article_parts.append("\n\n## Un Chiste Pa' Que No Te Aburras\n")
        article_parts.append(random.choice([
            f"¿Sabes cuál es la diferencia entre {topic} y un político? Que {topic} sí cumple lo que promete. 🍿",
            f"Mi abuela entiende más de {topic} que algunos ingenieros que conozco. Y eso que ella todavía manda mensajes por carta.",
            f"{topic} es como el vallenato: no todos lo entienden, pero cuando lo pillas, no puedes parar."
        ]))
        
        # Add conclusion
        article_parts.append("\n\n## ¿Y Ahora Qué?\n")
        
        conclusion_content = conclusion.format(
            topic=topic,
            lesson=f"si no aprendes sobre {topic}, te vas a quedar como Beta en VHS",
            summary=f"{topic} es el futuro y punto",
            key_point=f"la tecnología no espera a nadie",
            adjective="más importante que el aire acondicionado en agosto"
        )
        
        article_parts.append(conclusion_content)
        
        # Add call to action
        article_parts.append("\n\n---\n")
        article_parts.append(random.choice([
            "¿Te gustó? Dale a ese botón de aplaudir como si fuera champeta a todo volumen. 👏",
            "Si aprendiste algo, compártelo. Si no, también, que la risa también cuenta. 🍿",
            "Sígueme pa' más contenido así. O no, tú verás, pero después no digas que no te avisé."
        ]))
        
        # Add tags
        tags = ['Spanish', 'Tech', 'Colombia', 'AI', topic.replace(' ', '')]
        
        return {
            'title': title,
            'subtitle': subtitle,
            'content': '\n'.join(article_parts),
            'tags': tags,
            'estimated_read_time': f"{len(' '.join(article_parts).split()) // 200} min",
            'style': 'costeno',
            'word_count': len(' '.join(article_parts).split())
        }
    
    def _generate_gen_alpha_article(self, topic: str, word_count: int) -> Dict[str, Any]:
        """Generate article in Gen Alpha English."""
        # Pick templates
        intro = random.choice(self.gen_alpha_templates['intro'])
        body_parts = random.sample(self.gen_alpha_templates['body'], 3)
        conclusion = random.choice(self.gen_alpha_templates['conclusion'])
        
        # Generate content
        title = f"{topic} Is Lowkey Changing Everything and Here's Why You Should Care"
        
        subtitle = random.choice([
            f"A chaotic deep dive into why {topic} hits different in 2024",
            f"POV: You finally understand {topic} (you're welcome bestie)",
            f"Why {topic} is giving main character energy in tech right now"
        ])
        
        # Build article
        article_parts = [
            f"# {title}\n",
            f"## {subtitle}\n",
            intro.format(topic=topic),
            "\n\n## The Tea ☕\n",
        ]
        
        # Add body sections
        explanations = [
            f"{topic} is basically when computers decide to stop being NPCs and start being the main character",
            f"imagine if your phone could think for itself but like, in a good way",
            f"it's giving 'technology but make it fashion'"
        ]
        
        facts = [
            f"{topic} processes more data than all of TikTok combined (and that's saying something)",
            "Silicon Valley bros have been gatekeeping this for years",
            "this tech is literally rewriting the rules and I'm here for it"
        ]
        
        for i, body in enumerate(body_parts):
            section_title = random.choice([
                "But Like, What Even Is It? 🤔",
                "Why This Slaps So Hard",
                "The Part Where I Blow Your Mind",
                "Technical Stuff (But Make It Fun)"
            ])
            
            article_parts.append(f"\n## {section_title}\n")
            
            content = body.format(
                explanation=random.choice(explanations),
                analogy=random.choice(self.gen_alpha_analogies),
                fact=random.choice(facts),
                technical_detail=f"{topic} uses neural networks and machine learning",
                simple_explanation="the computer learns like how you learned TikTok dances",
                insider_info=f"every tech company is scrambling to implement {topic} before they become irrelevant",
                topic=topic
            )
            
            article_parts.append(content)
        
        # Add meme section
        article_parts.append("\n\n## Meme Break Because Why Not\n")
        article_parts.append(random.choice([
            f"Me: *explains {topic}*\nThem: 'So it's like AI?'\nMe: *sighs in binary* 🤖",
            f"{topic} developers: 'It's not that complicated'\nAlso {topic}: *requires PhD to understand* 📚",
            f"Nobody:\nAbsolutely nobody:\n{topic}: 'I'm about to end this whole industry's career' 💅"
        ]))
        
        # Add conclusion
        article_parts.append("\n\n## Final Thoughts (Stream Taylor's Version)\n")
        
        conclusion_content = conclusion.format(
            topic=topic,
            lesson=f"adapt or become a boomer",
            summary=f"{topic} is the moment and that's that on that",
            key_point=f"technology waits for no one",
            adjective="absolutely revolutionary no cap"
        )
        
        article_parts.append(conclusion_content)
        
        # Add call to action
        article_parts.append("\n\n---\n")
        article_parts.append(random.choice([
            "If this article hit different, smash that clap button like it owes you money 👏",
            "Follow for more chaotic tech content. Or don't. I'm not your mom. 💅",
            "Share this with that friend who still thinks AI is just Siri. They need help fr.",
            "Drop a comment if you're ready to be part of the future. NPCs need not apply."
        ]))
        
        # Add tags
        tags = ['Tech', 'AI', 'Future', 'GenZ', topic.replace(' ', ''), 'Innovation']
        
        return {
            'title': title,
            'subtitle': subtitle,
            'content': '\n'.join(article_parts),
            'tags': tags,
            'estimated_read_time': f"{len(' '.join(article_parts).split()) // 238} min",
            'style': 'gen_alpha',
            'word_count': len(' '.join(article_parts).split())
        }
    
    def generate_article_series(self, topic: str, parts: int = 3) -> List[Dict[str, Any]]:
        """
        Generate a series of articles on a topic.
        Mix of Costeño and Gen Alpha for maximum reach.
        """
        series = []
        styles = ['costeno', 'gen_alpha', 'costeno']  # Alternate styles
        
        subtopics = [
            f"The Basics of {topic}",
            f"Advanced {topic} Techniques",
            f"{topic} in Real Life"
        ]
        
        for i in range(min(parts, 3)):
            article = self.generate_article(
                subtopics[i], 
                style=styles[i],
                word_count=1000
            )
            article['part'] = i + 1
            article['series_name'] = f"{topic} Explained"
            series.append(article)
        
        return series
    
    def get_trending_topics(self) -> List[str]:
        """Get topics that would go viral right now."""
        base_topics = self.hot_topics.copy()
        
        # Add timely twists
        trending = []
        for topic in base_topics:
            trending.extend([
                f"{topic} in 2024",
                f"Why {topic} Is Dead (And What's Next)",
                f"I Tried {topic} for 30 Days and Here's What Happened",
                f"The Dark Side of {topic} Nobody Talks About",
                f"{topic} for Beginners: A Chaotic Guide"
            ])
        
        return random.sample(trending, 10)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get writer statistics."""
        return {
            'styles_available': ['costeno', 'gen_alpha'],
            'topics_in_database': len(self.hot_topics),
            'templates': {
                'costeno': len(self.costeno_templates['intro']),
                'gen_alpha': len(self.gen_alpha_templates['intro'])
            },
            'trending_now': random.sample(self.get_trending_topics(), 5),
            'status': '¡Listo pa\' escribir! Ready to drop some heat! 🔥'
        }