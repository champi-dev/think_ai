#!/usr/bin/env python3
"""
Test script to prove all the social media chaos works.
¡Ey mani, vamo' a ver si esta mondá sirve!
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.social.comedian import ThinkAIComedian
from think_ai.social.medium_writer import MediumWriter
from think_ai.social.x_twitter_bot import XTwitterBot

# Mock the browser import to avoid playwright dependency
import sys
from unittest.mock import MagicMock
sys.modules['playwright'] = MagicMock()
sys.modules['playwright.async_api'] = MagicMock()

from think_ai.social.social_manager import SocialMediaManager


async def test_comedian():
    """Test the comedian module."""
    print("\n🎭 TESTING COMEDIAN MODULE")
    print("="*60)
    
    comedian = ThinkAIComedian()
    
    # Test Colombian jokes
    print("\n1. Colombian Joke:")
    joke = comedian.get_random_joke('colombian')
    print(f"   {joke}")
    
    # Test tech jokes
    print("\n2. Tech Joke:")
    joke = comedian.get_random_joke('tech')
    print(f"   {joke}")
    
    # Test roasting
    print("\n3. Roast JavaScript:")
    roast = comedian.roast("JavaScript", {"thing": "type system"})
    print(f"   {roast}")
    
    # Test social post creation
    print("\n4. Create Twitter Post:")
    post = comedian.create_social_post("AI", "twitter")
    print(f"   Post: {post['post']}")
    print(f"   Hashtags: {', '.join(post['hashtags'])}")
    
    # Test meme generation
    print("\n5. Generate Meme:")
    meme = comedian.generate_meme_text('drake')
    print(f"   Drake meme:")
    print(f"   ❌ {meme['content']['reject']}")
    print(f"   ✅ {meme['content']['prefer']}")
    print(f"   Caption: {meme['caption']}")
    
    print("\n✅ Comedian module working!")


async def test_twitter_bot():
    """Test X/Twitter bot."""
    print("\n\n🐦 TESTING X/TWITTER BOT")
    print("="*60)
    
    bot = XTwitterBot()
    
    # Test Costeño tweet
    print("\n1. Costeño Tweet:")
    tweet = bot.generate_tweet('costeno')
    print(f"   {tweet['text']}")
    print(f"   Characters: {tweet['char_count']}")
    
    # Test Gen Alpha tweet
    print("\n2. Gen Alpha Tweet:")
    tweet = bot.generate_tweet('gen_alpha')
    print(f"   {tweet['text']}")
    
    # Test thread generation
    print("\n3. Generate Thread about 'Machine Learning':")
    thread = bot.generate_thread("Machine Learning", "costeno", 3)
    for i, tweet in enumerate(thread):
        print(f"   {tweet['position']}: {tweet['text']}")
    
    # Test reply generation
    print("\n4. Generate Reply:")
    original = "Why is Python so slow?"
    reply = bot.generate_reply(original, 'gen_alpha')
    print(f"   Original: {original}")
    print(f"   Reply: {reply['text']}")
    
    # Test scheduled content
    print("\n5. Generate Week Schedule:")
    schedule = bot.generate_scheduled_content(3)  # 3 days
    print(f"   Generated {len(schedule)} scheduled posts")
    print(f"   First post: {schedule[0]['scheduled_time']}")
    
    print("\n✅ Twitter bot working!")


async def test_medium_writer():
    """Test Medium article writer."""
    print("\n\n📝 TESTING MEDIUM WRITER")
    print("="*60)
    
    writer = MediumWriter()
    
    # Test Costeño article
    print("\n1. Generate Costeño Article:")
    article = writer.generate_article("Quantum Computing", "costeno", 500)
    print(f"   Title: {article['title']}")
    print(f"   Subtitle: {article['subtitle']}")
    print(f"   Word count: {article['word_count']}")
    print(f"   Preview: {article['content'][:200]}...")
    
    # Test Gen Alpha article
    print("\n2. Generate Gen Alpha Article:")
    article = writer.generate_article("Web3", "gen_alpha", 500)
    print(f"   Title: {article['title']}")
    print(f"   Preview: {article['content'][:200]}...")
    
    # Test article series
    print("\n3. Generate Article Series:")
    series = writer.generate_article_series("AI Consciousness", 2)
    print(f"   Generated {len(series)} articles")
    for article in series:
        print(f"   - Part {article['part']}: {article['title']} ({article['style']})")
    
    # Test trending topics
    print("\n4. Get Trending Topics:")
    trending = writer.get_trending_topics()
    print("   Top 5 trending:")
    for topic in trending[:5]:
        print(f"   - {topic}")
    
    print("\n✅ Medium writer working!")


async def test_social_manager():
    """Test social media manager."""
    print("\n\n📱 TESTING SOCIAL MEDIA MANAGER")
    print("="*60)
    
    manager = SocialMediaManager()
    await manager.initialize()
    
    # Test viral campaign creation
    print("\n1. Create Viral Campaign:")
    campaign = await manager.create_viral_campaign("Think AI", 7)
    print(f"   Topic: {campaign['topic']}")
    print(f"   Duration: {campaign['start_date']} to {campaign['end_date']}")
    print(f"   Twitter posts: {len(campaign['platforms']['twitter'])}")
    print(f"   Medium articles: {len(campaign['platforms']['medium'])}")
    
    # Test trend analysis
    print("\n2. Analyze Trends:")
    trends = await manager.analyze_trends()
    print(f"   Found {len(trends['twitter'])} Twitter trends")
    print(f"   Found {len(trends['tech'])} tech trends")
    if trends['recommended_content']:
        print(f"   First recommendation: {trends['recommended_content'][0]['costeno_angle']}")
    
    # Test content calendar
    print("\n3. Generate Content Calendar:")
    calendar = await manager.generate_content_calendar(7)  # 1 week
    print(f"   Generated {len(calendar)} days of content")
    print(f"   Day 1 has {len(calendar[0]['content'])} posts scheduled")
    
    # Test engagement report
    print("\n4. Get Engagement Report:")
    report = await manager.get_engagement_report()
    print(f"   Growth: {report['growth']['monthly_growth']}")
    print(f"   Best platform: {report['growth']['best_platform']}")
    print(f"   Top recommendation: {report['recommendations'][0]}")
    
    # Show final stats
    print("\n5. System Stats:")
    stats = manager.get_stats()
    print(f"   Platforms: {', '.join(stats['platforms_active'])}")
    print(f"   Status: {stats['status']}")
    print(f"   Random joke: {stats['joke']}")
    
    print("\n✅ Social media manager working!")
    
    # Cleanup
    await manager.browser.shutdown()


async def main():
    """Run all tests."""
    print("🚀 TESTING THINK AI SOCIAL MEDIA CHAOS")
    print("=" * 80)
    print("¡Ey mani! Vamo' a probar que toda esta vaina sirve...")
    
    try:
        # Test each component
        await test_comedian()
        await test_twitter_bot()
        await test_medium_writer()
        await test_social_manager()
        
        print("\n\n" + "🎉" * 20)
        print("✅ ALL TESTS PASSED! ¡TODO SIRVE MI LLAVE!")
        print("🎉" * 20)
        
        print("\n📊 SUMMARY:")
        print("- Comedian: ✅ Throwing jokes like confetti")
        print("- Twitter Bot: ✅ Ready to cause chaos in two languages")
        print("- Medium Writer: ✅ Articles that hit different")
        print("- Social Manager: ✅ Orchestrating the mayhem")
        print("\n¡No joda! Esta mondá sí funciona! 🍿")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("¡Qué pecao'! Something broke...")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())