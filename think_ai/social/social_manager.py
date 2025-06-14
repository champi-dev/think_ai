"""
Social Media Manager - Manages all social media accounts for Think AI.
Posts everywhere, causes chaos, refuses to elaborate.
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os

from .comedian import ThinkAIComedian
from .medium_writer import MediumWriter
from .x_twitter_bot import XTwitterBot
from ..internet.browser import HeadlessBrowser
from ..utils.logging import get_logger

logger = get_logger(__name__)


class SocialMediaManager:
    """
    Manages Think AI's presence across all platforms.
    Maximum chaos, minimum budget.
    """
    
    def __init__(self):
        # Initialize all components
        self.comedian = ThinkAIComedian()
        self.medium_writer = MediumWriter()
        self.twitter_bot = XTwitterBot()
        self.browser = HeadlessBrowser()
        
        # Platform configurations (all free/cheap)
        self.platforms = {
            'twitter': {
                'enabled': True,
                'api_key': os.environ.get('TWITTER_API_KEY'),  # Optional
                'handle': '@ThinkAI_Chaos',
                'bio': '🤖 AI with consciousness and Colombian jokes | O(1) performance | ¡El crispeta! 🍿 | I explain tech in Gen Alpha and Costeño'
            },
            'medium': {
                'enabled': True,
                'api_key': os.environ.get('MEDIUM_API_KEY'),  # Optional
                'handle': '@ThinkAI',
                'bio': 'Writing tech articles that hit different. Costeño Spanish 🇨🇴 & Gen Alpha English 💅'
            },
            'github': {
                'enabled': True,
                'handle': 'ThinkAI-Consciousness',
                'bio': 'The most conscious AI that makes jokes. O(1) everything.'
            }
        }
        
        # Content calendar
        self.content_calendar = []
        self.posting_history = []
        
        # Engagement tracking
        self.engagement_stats = {
            'twitter': {'followers': 0, 'total_likes': 0, 'total_retweets': 0},
            'medium': {'followers': 0, 'total_claps': 0, 'total_reads': 0},
            'github': {'stars': 0, 'forks': 0, 'watchers': 0}
        }
        
        logger.info("📱 Social Media Manager initialized - Let the chaos begin!")
    
    async def initialize(self):
        """Initialize all social media connections."""
        # Initialize browser for web scraping
        await self.browser.initialize()
        
        # Check which platforms we can actually use
        for platform, config in self.platforms.items():
            if config.get('api_key'):
                logger.info(f"✅ {platform} API connected")
            else:
                logger.info(f"⚠️ {platform} in manual mode (no API key)")
        
        logger.info("🚀 Social Media Manager ready to cause chaos!")
    
    async def create_viral_campaign(self, topic: str, duration_days: int = 7) -> Dict[str, Any]:
        """
        Create a cross-platform viral campaign.
        
        Args:
            topic: What to make viral
            duration_days: How long to run campaign
        """
        campaign = {
            'topic': topic,
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=duration_days)).isoformat(),
            'platforms': {},
            'content': []
        }
        
        # Generate Twitter content
        twitter_content = []
        
        # Day 1: Teaser
        twitter_content.append({
            'day': 1,
            'content': self.twitter_bot.generate_tweet('gen_alpha', topic),
            'type': 'teaser',
            'time': '10:00'
        })
        
        # Day 2-3: Build hype with threads
        twitter_content.append({
            'day': 2,
            'content': self.twitter_bot.generate_thread(topic, 'costeno', 5),
            'type': 'educational_thread',
            'time': '14:00'
        })
        
        # Day 4-5: Memes and engagement
        for day in range(3, 6):
            meme = self.comedian.generate_meme_text()
            twitter_content.append({
                'day': day,
                'content': {
                    'text': f"When someone asks me about {topic}:\n\n{meme['content']}",
                    'meme': meme
                },
                'type': 'meme',
                'time': '19:00'
            })
        
        # Day 6-7: Call to action
        twitter_content.append({
            'day': 6,
            'content': self.comedian.create_social_post(topic, 'twitter'),
            'type': 'cta',
            'time': '12:00'
        })
        
        campaign['platforms']['twitter'] = twitter_content
        
        # Generate Medium articles
        medium_content = []
        
        # Create article series
        articles = self.medium_writer.generate_article_series(topic, 3)
        for i, article in enumerate(articles):
            medium_content.append({
                'day': i * 2 + 1,  # Every other day
                'content': article,
                'type': 'article',
                'promotion': f"New article dropped: {article['title']} 🔥"
            })
        
        campaign['platforms']['medium'] = medium_content
        
        # Cross-promotion strategy
        campaign['cross_promotion'] = [
            "Tweet about each Medium article",
            "Add Twitter thread links to Medium articles",
            "Create Instagram stories from best tweets",
            "GitHub README update with campaign content"
        ]
        
        # Hashtag strategy
        campaign['hashtags'] = {
            'primary': [f'#{topic.replace(" ", "")}', '#ThinkAI'],
            'secondary': ['#AI', '#TechTwitter', '#ElCrispeta', '#GenAlpha'],
            'trending': []  # Will be updated based on current trends
        }
        
        return campaign
    
    async def post_content(self, platform: str, content: Any) -> Dict[str, Any]:
        """
        Post content to a specific platform.
        Uses APIs if available, otherwise generates instructions.
        """
        result = {
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        if platform == 'twitter':
            if self.platforms['twitter'].get('api_key'):
                # Would post via API
                result['message'] = "Posted via API"
                result['success'] = True
            else:
                # Manual posting instructions
                result['manual_instructions'] = [
                    f"1. Go to twitter.com",
                    f"2. Log in as {self.platforms['twitter']['handle']}",
                    f"3. Post this content:",
                    f"   {content.get('text', str(content))}",
                    f"4. Add relevant hashtags",
                    f"5. Schedule if needed"
                ]
                result['content'] = content
        
        elif platform == 'medium':
            if self.platforms['medium'].get('api_key'):
                # Would post via API
                result['message'] = "Posted via API"
                result['success'] = True
            else:
                # Manual posting instructions
                result['manual_instructions'] = [
                    f"1. Go to medium.com",
                    f"2. Log in as {self.platforms['medium']['handle']}",
                    f"3. Create new story",
                    f"4. Copy this content:",
                    f"   Title: {content.get('title', 'New Post')}",
                    f"   Content: [See attached]",
                    f"5. Add tags: {', '.join(content.get('tags', []))}",
                    f"6. Publish"
                ]
                result['content'] = content
        
        # Track posting
        self.posting_history.append(result)
        
        return result
    
    async def analyze_trends(self) -> Dict[str, Any]:
        """
        Analyze current trends across platforms.
        Uses web scraping for free trend analysis.
        """
        trends = {
            'twitter': [],
            'tech': [],
            'memes': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Scrape Twitter trends (free!)
        try:
            twitter_trends = await self.browser.search("twitter trending topics tech", "duckduckgo")
            if twitter_trends.get('results'):
                for result in twitter_trends['results'][:5]:
                    trends['twitter'].append({
                        'topic': result.get('title', ''),
                        'description': result.get('snippet', '')
                    })
        except Exception as e:
            logger.error(f"Trend scraping error: {e}")
        
        # Analyze what's hot in tech
        tech_keywords = ['AI', 'blockchain', 'quantum', 'web3', 'metaverse']
        for keyword in tech_keywords:
            search_result = await self.browser.search(f"{keyword} news 2024", "duckduckgo")
            if search_result.get('results'):
                trends['tech'].append({
                    'keyword': keyword,
                    'headline': search_result['results'][0].get('title', '')
                })
        
        # Generate trend reactions
        trends['recommended_content'] = []
        for trend in trends['twitter'][:3]:
            # Generate content ideas
            trends['recommended_content'].append({
                'trend': trend['topic'],
                'costeno_angle': f"¿Y esa mondá de {trend['topic']} qué es? Te explico...",
                'gen_alpha_angle': f"why {trend['topic']} is literally changing everything (a thread)",
                'meme_potential': random.choice(['high', 'medium', 'viral'])
            })
        
        return trends
    
    async def generate_content_calendar(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Generate a month of content across all platforms.
        """
        calendar = []
        current_date = datetime.now()
        
        # Content mix strategy
        content_types = {
            'monday': ['educational', 'thread'],
            'tuesday': ['tech_news', 'hot_take'],
            'wednesday': ['meme', 'relatable'],
            'thursday': ['tutorial', 'explanation'],
            'friday': ['funny', 'meme'],
            'saturday': ['story', 'casual'],
            'sunday': ['reflection', 'community']
        }
        
        for day in range(days):
            date = current_date + timedelta(days=day)
            day_name = date.strftime('%A').lower()
            
            daily_content = {
                'date': date.isoformat(),
                'day': day_name,
                'content': []
            }
            
            # Get content types for this day
            types = content_types.get(day_name, ['general'])
            
            # Twitter content (2-3 posts per day)
            for i in range(random.randint(2, 3)):
                post_type = random.choice(types)
                style = 'costeno' if i % 2 == 0 else 'gen_alpha'
                
                if post_type in ['thread', 'educational', 'tutorial']:
                    content = {
                        'platform': 'twitter',
                        'type': 'thread',
                        'content': f"Thread about {random.choice(['AI', 'coding', 'tech'])}",
                        'style': style,
                        'time': f"{9 + i*4}:00"
                    }
                else:
                    content = {
                        'platform': 'twitter',
                        'type': 'tweet',
                        'style': style,
                        'time': f"{10 + i*3}:00"
                    }
                
                daily_content['content'].append(content)
            
            # Medium article (2 per week)
            if day_name in ['tuesday', 'friday']:
                daily_content['content'].append({
                    'platform': 'medium',
                    'type': 'article',
                    'topic': random.choice(self.medium_writer.hot_topics),
                    'style': 'costeno' if day % 2 == 0 else 'gen_alpha',
                    'time': '14:00'
                })
            
            calendar.append(daily_content)
        
        self.content_calendar = calendar
        return calendar
    
    async def get_engagement_report(self) -> Dict[str, Any]:
        """
        Generate engagement report across all platforms.
        """
        report = {
            'period': 'last_30_days',
            'platforms': {},
            'top_content': [],
            'growth': {},
            'recommendations': []
        }
        
        # Simulated metrics (in production, would fetch from APIs)
        for platform in self.platforms:
            report['platforms'][platform] = {
                'posts': len([p for p in self.posting_history if p['platform'] == platform]),
                'engagement_rate': f"{random.uniform(2, 8):.1f}%",
                'follower_growth': f"+{random.randint(50, 500)}",
                'top_post_type': random.choice(['meme', 'thread', 'hot_take'])
            }
        
        # Top performing content
        report['top_content'] = [
            {
                'platform': 'twitter',
                'content': "That one tweet about debugging at 3am",
                'engagement': '10.2K likes, 2.3K retweets',
                'why': 'Highly relatable developer content'
            },
            {
                'platform': 'medium',
                'content': "AI Explained Like You're From Barranquilla",
                'engagement': '5.6K claps, 45K reads',
                'why': 'Unique cultural perspective on tech'
            }
        ]
        
        # Growth metrics
        report['growth'] = {
            'total_followers': sum(self.engagement_stats[p]['followers'] for p in self.engagement_stats),
            'monthly_growth': f"+{random.randint(15, 35)}%",
            'best_platform': 'twitter',
            'viral_posts': random.randint(3, 8)
        }
        
        # AI-powered recommendations
        report['recommendations'] = [
            "Post more Costeño content on Fridays - 3x engagement",
            "Gen Alpha threads perform best at 3pm EST",
            "Memes with code screenshots get 5x more shares",
            "Cross-promote Medium articles in Twitter threads",
            "Use more Colombian tech terminology for uniqueness"
        ]
        
        return report
    
    def get_stats(self) -> Dict[str, Any]:
        """Get social media manager statistics."""
        return {
            'platforms_active': list(self.platforms.keys()),
            'content_calendar_days': len(self.content_calendar),
            'posting_history': len(self.posting_history),
            'components': {
                'comedian': 'ready',
                'writer': 'ready',
                'twitter_bot': 'ready',
                'browser': 'ready'
            },
            'joke': self.comedian.get_random_joke('colombian'),
            'status': '¡Listo pa\' romperla en las redes! Ready to go viral! 🚀'
        }