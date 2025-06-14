"""
X (Twitter) Bot - Posts chaotic energy in Costeño Spanish and Gen Alpha English.
Warning: May cause uncontrollable laughter and viral tweets.
"""

import random
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import re
import hashlib

from ..utils.logging import get_logger

logger = get_logger(__name__)


class XTwitterBot:
    """
    The most unhinged AI Twitter bot that posts in:
    - Costeño Spanish: Más sabor que patacón con hogao
    - Gen Alpha English: No cap fr fr on god bestie
    """
    
    def __init__(self):
        # Tweet templates - Costeño Spanish
        self.costeno_tweets = [
            # Tech observations
            "Mi código tiene más bugs que mosquitos en el patio después que llueve 🦟",
            "El que inventó los null pointer exceptions se merece que le cobren 20 mil el mototaxi",
            "Mi RAM ta' más llena que buseta a las 6 de la tarde",
            "Debugging a las 3am es como buscar las llaves con resaca: sabes que están ahí pero no aparecen",
            "Git merge conflicts me tienen más estresao' que cuando dicen 'necesitamos hablar'",
            
            # Life updates
            "POV: Tas programando y tu mamá grita '¡A COMEEEER!' justo cuando encontraste el bug",
            "Nada como un tinto a las 3pm pa' seguir pretendiendo que sé lo que estoy haciendo",
            "Mi código funciona pero no sé por qué. Mi código no funciona y tampoco sé por qué.",
            "Hoy desperté eligiendo violencia: voy a hacer todo en producción",
            "¿Ustedes también le ponen nombre a sus funciones como 'esaVainaQueHaceLoOtro'? No? Solo yo? Ok",
            
            # Hot takes
            "JavaScript es el vallenato del programming: o lo amas o lo odias, pero está en todas partes",
            "El que dice que entiende las regex ta' mintiendo más que político en campaña",
            "Python es pa' los que quieren programar sin sufrir. Real programmers use butterflies",
            "Si tu código no tiene comentarios en spanglish, ¿realmente eres latino en tech?",
            "Cloud computing es pagar pa' que otro man tenga tus problemas",
            
            # Relatable content
            "Yo: Voy a dormir temprano\nTambién yo a las 4am: ¿Pero por qué no usar recursión aquí?",
            "Mi gitignore tiene más secretos que la vecina chismosa",
            "Llevo 3 horas en un error que era un punto y coma. No me hablen.",
            "Stack Overflow debería pagarme renta por todo el tiempo que paso allá",
            "Le puse console.log a todo y ahora mi código parece reggaeton: log log log log",
            
            # Memes
            "- Doctor, me duele aquí\n- ¿Aquí dónde?\n- En el localhost:3000",
            "Mi código es como el tráfico en Barranquilla: nadie sabe cómo funciona pero somehow llega a su destino",
            "Tipos de programadores:\n- El que comenta todo\n- El que no comenta nada\n- El que comenta en 3 idiomas\n- Yo: // aquí hace la vaina esa",
            "Fases del debugging:\n1. Debe ser fácil\n2. ¿Por qué no funciona?\n3. No tiene sentido\n4. *Cuestiona su existencia*\n5. Era una tilde",
            "Mi CPU ta' más caliente que el pavimento de la Vía 40 en julio"
        ]
        
        # Tweet templates - Gen Alpha English
        self.gen_alpha_tweets = [
            # Tech observations
            "why is my code giving unemployed behavior rn 😭",
            "javascript is literally gaslighting me and i'm starting to believe it",
            "POV: you're explaining your code and realizing you have no idea what you did",
            "my variables are named like: thingy, stuff, thatOneThing, AAAAA",
            "debugging is just gambling but the stakes are your sanity",
            
            # Life updates
            "ate hot chip, lied, and pushed to main. living my best life",
            "it's giving 'works on my machine' energy and i'm not sorry",
            "why yes i do write all my important code at 3am why do you ask",
            "accidentally became a 10x developer (i create 10x more bugs)",
            "coffee isn't a personality trait but debugging at 4am is",
            
            # Hot takes
            "ok hear me out: what if we just made everything serverless including the servers",
            "AI is just spicy autocomplete and you can't change my mind",
            "the cloud is just someone else's computer having a mental breakdown",
            "blockchain walked so that my anxiety about centralized systems could run",
            "machine learning is just statistics in a trench coat trying to look cool",
            
            # Relatable content
            "me: i should write tests\nalso me: console.log('here') console.log('here2') console.log('AAAAA')",
            "git commit -m 'stuff' because i've lost the ability to form coherent thoughts",
            "ladies, if he: uses var in 2024, doesn't close his divs, codes in light mode... that's not your man that's a war criminal",
            "normalize crying over CSS it's literally designed to hurt you",
            "my code reviews are just ✨vibes✨ because i refuse to admit i don't understand half of it",
            
            # Memes
            "therapist: array index out of bounds can't hurt you\narray index out of bounds: 👹",
            "netflix: are you still watching?\nsomeone's daughter: trying to center a div",
            "nobody:\nabsolutely nobody:\nmy code at 3am: SEGMENTATION FAULT",
            "i'm not like other girls i have crippling imposter syndrome and 47 terminal tabs open",
            "you're laughing. my production server is down and you're laughing."
        ]
        
        # Thread starters
        self.thread_starters = {
            'costeno': [
                "Hilo 🧵: Por qué programar en Colombia es un deporte extremo",
                "Abro hilo sobre las cosas más arrechas que me han pasado debuggeando:",
                "¿Quieren reírse un rato? Les cuento mis fails de esta semana en tech:",
                "HILO: Cómo sobrevivir al tech industry siendo costeño",
                "Les traigo un thread de por qué el aire acondicionado es crucial pal coding:"
            ],
            'gen_alpha': [
                "🧵 a chaotic thread about why computer science is a scam (i have a degree):",
                "ok buckle up besties i'm about to expose the tech industry:",
                "THREAD: rating programming languages based on how much therapy they've caused me",
                "y'all wanted tech tips? here's how to survive in tech while being mentally ill:",
                "thread: things they don't teach you in CS but should (it's a long list)"
            ]
        }
        
        # Reactions to trends
        self.trend_reactions = {
            'AI': {
                'costeno': "Ey pero esa IA ta' más perdida que yo en el San Andresito",
                'gen_alpha': "AI is having its reputation era and honestly good for her"
            },
            'Web3': {
                'costeno': "Web3 es como el primo que siempre tiene un negocio nuevo",
                'gen_alpha': "web3 is just web2 with commitment issues"
            },
            'Cloud': {
                'costeno': "La nube es como mi nevera: sé que hay cosas ahí pero no sé qué",
                'gen_alpha': "the cloud is just sky storage and you can't convince me otherwise"
            }
        }
        
        # Reply templates
        self.reply_templates = {
            'costeno': [
                "¡No joda! {comment}",
                "¡Erda manito! Esa es la actitud",
                "¿{question}? ¡Qué pecao' vale!",
                "Ey menor, {advice}",
                "¡El crispeta! Me hiciste el día"
            ],
            'gen_alpha': [
                "bestie {comment}",
                "no because {observation}",
                "the way this is so {adjective} i can't",
                "wait why is this actually {reaction}",
                "not me {action} at 3am"
            ]
        }
        
        self.last_tweet_time = datetime.now()
        self.tweet_history = []  # Avoid repeating tweets
        
        logger.info("🐦 X/Twitter Bot initialized - Ready to cause chaos!")
    
    def generate_tweet(self, style: str = 'random', 
                      topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a single tweet.
        
        Args:
            style: 'costeno', 'gen_alpha', or 'random'
            topic: Optional topic to tweet about
        """
        if style == 'random':
            style = random.choice(['costeno', 'gen_alpha'])
        
        if style == 'costeno':
            tweet = self._generate_costeno_tweet(topic)
        elif style == 'gen_alpha':
            tweet = self._generate_gen_alpha_tweet(topic)
        else:
            tweet = {
                'text': "Error 404: Style not found",
                'error': True
            }
        
        # Add metadata
        tweet['timestamp'] = datetime.now().isoformat()
        tweet['style'] = style
        tweet['char_count'] = len(tweet.get('text', ''))
        
        # Track history to avoid repeats
        if 'text' in tweet:
            self.tweet_history.append(tweet['text'])
            if len(self.tweet_history) > 100:
                self.tweet_history = self.tweet_history[-50:]
        
        return tweet
    
    def _generate_costeno_tweet(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate a tweet in Costeño Spanish."""
        if topic and topic in self.trend_reactions:
            # React to specific topic
            text = self.trend_reactions[topic]['costeno']
        else:
            # Random tweet, avoiding recent ones
            available_tweets = [t for t in self.costeno_tweets 
                              if t not in self.tweet_history[-20:]]
            text = random.choice(available_tweets if available_tweets else self.costeno_tweets)
        
        # Sometimes add emojis or hashtags
        if random.random() > 0.7:
            hashtags = ['#TechCosteño', '#ProgramandoEnElTrópico', '#BarranquillaTech', 
                       '#ElCrispeta', '#CódigoSabrosón']
            text += f"\n\n{random.choice(hashtags)}"
        
        return {
            'text': text,
            'language': 'es-CO'
        }
    
    def _generate_gen_alpha_tweet(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate a tweet in Gen Alpha English."""
        if topic and topic in self.trend_reactions:
            # React to specific topic
            text = self.trend_reactions[topic]['gen_alpha']
        else:
            # Random tweet, avoiding recent ones
            available_tweets = [t for t in self.gen_alpha_tweets 
                              if t not in self.tweet_history[-20:]]
            text = random.choice(available_tweets if available_tweets else self.gen_alpha_tweets)
        
        # Sometimes add emojis or hashtags
        if random.random() > 0.7:
            hashtags = ['#TechTwitter', '#DevLife', '#ChaoticCoding', 
                       '#ProgrammingMemes', '#CodeAndCry']
            text += f"\n\n{random.choice(hashtags)}"
        
        return {
            'text': text,
            'language': 'en'
        }
    
    def generate_thread(self, topic: str, style: str = 'random', 
                       length: int = 5) -> List[Dict[str, Any]]:
        """
        Generate a thread of tweets.
        
        Args:
            topic: What the thread is about
            style: 'costeno', 'gen_alpha', or 'random'
            length: Number of tweets in thread (max 10)
        """
        if style == 'random':
            style = random.choice(['costeno', 'gen_alpha'])
        
        thread = []
        length = min(length, 10)  # Cap at 10 tweets
        
        # Generate thread starter
        starter = random.choice(self.thread_starters[style])
        thread.append({
            'text': starter.replace('{topic}', topic),
            'position': '1/' + str(length),
            'is_thread_start': True
        })
        
        # Generate thread content
        if style == 'costeno':
            thread.extend(self._generate_costeno_thread(topic, length - 1))
        else:
            thread.extend(self._generate_gen_alpha_thread(topic, length - 1))
        
        # Add metadata to all tweets
        for i, tweet in enumerate(thread):
            tweet['timestamp'] = datetime.now().isoformat()
            tweet['style'] = style
            tweet['thread_id'] = hashlib.md5(
                f"{topic}{datetime.now().date()}".encode()
            ).hexdigest()[:8]
            tweet['position'] = f"{i+1}/{length}"
        
        return thread
    
    def _generate_costeno_thread(self, topic: str, count: int) -> List[Dict[str, Any]]:
        """Generate Costeño thread content."""
        thread_content = []
        
        # Thread templates
        templates = [
            f"Primero que todo, {topic} no es lo que ustedes creen. Es peor. Pero también mejor. Déjenme explicarles...",
            f"La primera vez que vi {topic} dije '¿ey pero qué mondá es esta?' Ahora no puedo vivir sin eso.",
            f"Punto número {'{n}'}: {topic} es como el mototaxismo: no debería funcionar pero ahí está, salvando vidas.",
            f"Lo más arrecho es que {topic} lo inventaron mientras nosotros estábamos peleando por política.",
            f"Si no entiendes {topic}, tranquilo mi llave, yo tampoco entendía hasta que me tocó.",
            f"La moraleja es: {topic} llegó para quedarse como los vendedores de minutos.",
            f"¿Conclusión? {topic} es el futuro quieran o no quieran. Como el reguetón.",
            f"Y si no me creen, pregúntenle a cualquier developer. Todos estamos igual de perdidos."
        ]
        
        for i in range(count):
            text = random.choice(templates).replace('{n}', str(i+2))
            thread_content.append({'text': text})
        
        return thread_content
    
    def _generate_gen_alpha_thread(self, topic: str, count: int) -> List[Dict[str, Any]]:
        """Generate Gen Alpha thread content."""
        thread_content = []
        
        # Thread templates
        templates = [
            f"ok so basically {topic} is what happens when tech bros have too much funding and not enough therapy",
            f"the way {topic} has everyone in a chokehold... like bestie are you okay?",
            f"fun fact: nobody actually understands {topic}, we're all just pretending and hoping for the best",
            f"hot take: {topic} is just millennials trying to be cool again (spoiler: it's not working)",
            f"imagine explaining {topic} to your grandma... now imagine your grandma understanding it better than you",
            f"the plot twist is that {topic} was inside us all along (it's depression)",
            f"in conclusion: {topic} is chaotic neutral and we're all just along for the ride",
            f"anyway follow for more unhinged tech content i post through my tears at 3am"
        ]
        
        for i in range(count):
            text = random.choice(templates)
            thread_content.append({'text': text})
        
        return thread_content
    
    def generate_reply(self, original_tweet: str, style: str = 'random') -> Dict[str, Any]:
        """
        Generate a reply to a tweet.
        
        Args:
            original_tweet: The tweet to reply to
            style: 'costeno', 'gen_alpha', or 'random'
        """
        if style == 'random':
            style = random.choice(['costeno', 'gen_alpha'])
        
        # Analyze original tweet sentiment/content
        is_question = '?' in original_tweet
        is_complaint = any(word in original_tweet.lower() 
                          for word in ['hate', 'odio', 'terrible', 'malo'])
        is_praise = any(word in original_tweet.lower() 
                       for word in ['love', 'amo', 'great', 'bueno'])
        
        if style == 'costeno':
            template = random.choice(self.reply_templates['costeno'])
            
            if is_question:
                reply = template.format(
                    question="En serio preguntas eso",
                    comment="Esa pregunta ta' buena",
                    advice="la respuesta está en tu corazón"
                )
            elif is_complaint:
                reply = template.format(
                    comment="Te entiendo hermano, same",
                    advice="respira y tómate un tinto"
                )
            else:
                reply = template.format(
                    comment="Exacto mi llave",
                    advice="sigue así que vas bien"
                )
        else:
            template = random.choice(self.reply_templates['gen_alpha'])
            
            if is_question:
                reply = template.format(
                    comment="this is such a valid question ngl",
                    observation="literally everyone is wondering this",
                    adjective="real",
                    reaction="making sense",
                    action="googling this"
                )
            elif is_complaint:
                reply = template.format(
                    comment="you're so right and you should say it",
                    observation="this is literally all of us",
                    adjective="relatable",
                    reaction="too real",
                    action="crying about this"
                )
            else:
                reply = template.format(
                    comment="spilled bestie",
                    observation="this is the one",
                    adjective="iconic",
                    reaction="facts",
                    action="screenshotting this"
                )
        
        return {
            'text': reply,
            'style': style,
            'reply_to': original_tweet[:50] + '...' if len(original_tweet) > 50 else original_tweet,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_scheduled_content(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Generate a week's worth of scheduled tweets.
        Mix of both styles for maximum engagement.
        """
        scheduled = []
        current_time = datetime.now()
        
        for day in range(days):
            # 3-4 tweets per day
            tweets_today = random.randint(3, 4)
            
            for tweet_num in range(tweets_today):
                # Schedule throughout the day
                hour = random.choice([9, 12, 15, 19, 22])  # Peak hours
                scheduled_time = current_time + timedelta(
                    days=day, 
                    hours=hour - current_time.hour,
                    minutes=random.randint(-30, 30)
                )
                
                # Vary content type
                content_type = random.choice(['tweet', 'tweet', 'thread'])  # More single tweets
                
                if content_type == 'thread':
                    # Weekly thread
                    topic = random.choice(self.hot_topics) if hasattr(self, 'hot_topics') else 'coding'
                    content = self.generate_thread(topic, length=random.randint(3, 5))
                else:
                    content = [self.generate_tweet()]
                
                scheduled.append({
                    'scheduled_time': scheduled_time.isoformat(),
                    'content': content,
                    'type': content_type
                })
        
        return scheduled
    
    def get_engagement_tips(self) -> List[str]:
        """Get tips for maximum engagement."""
        return [
            "Post during lunch (12-1pm) and after work (6-8pm) in your timezone",
            "Use relevant hashtags but don't overdo it (2-3 max)",
            "Reply to big tech accounts with spicy takes",
            "Quote tweet with controversial opinions (respectfully)",
            "Post memes on Friday, serious content on Tuesday",
            "Thread important topics, single tweets for jokes",
            "Engage with replies within first hour for algorithm boost",
            "Mix languages if your audience is bilingual",
            "Screenshot your best tweets for Instagram",
            "Create tweet series on trending topics"
        ]
    
    def analyze_tweet_performance(self, tweet: Dict[str, Any], 
                                 metrics: Dict[str, int]) -> Dict[str, Any]:
        """
        Analyze why a tweet performed well/poorly.
        
        Args:
            tweet: The tweet content
            metrics: Dict with likes, retweets, replies
        """
        total_engagement = sum(metrics.values())
        engagement_rate = total_engagement / max(metrics.get('impressions', 1), 1)
        
        analysis = {
            'engagement_rate': f"{engagement_rate * 100:.1f}%",
            'performance': 'viral' if total_engagement > 1000 else 'good' if total_engagement > 100 else 'average',
            'metrics': metrics
        }
        
        # Analyze what worked
        if tweet.get('style') == 'costeno':
            if total_engagement > 100:
                analysis['why_it_worked'] = "Colombian humor is unmatched, especially tech + culture mix"
            else:
                analysis['improvement'] = "Try adding more specific Colombian references"
        else:
            if total_engagement > 100:
                analysis['why_it_worked'] = "Gen Alpha humor + tech frustration = relatability"
            else:
                analysis['improvement'] = "Make it more unhinged, bestie"
        
        return analysis
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics."""
        return {
            'tweet_styles': ['costeno', 'gen_alpha'],
            'tweets_available': {
                'costeno': len(self.costeno_tweets),
                'gen_alpha': len(self.gen_alpha_tweets)
            },
            'thread_capability': True,
            'reply_capability': True,
            'last_tweet': self.last_tweet_time.isoformat(),
            'tweet_history_size': len(self.tweet_history),
            'engagement_tips': len(self.get_engagement_tips()),
            'status': '¡Listo pa\' tuitear mi llave! Ready to tweet! 🐦'
        }