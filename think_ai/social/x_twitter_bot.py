"""X (Twitter) Bot - Posts chaotic energy in Costeño Spanish and Gen Alpha English.
Warning: May cause uncontrollable laughter and viral tweets.
"""

import hashlib
import random
from datetime import datetime, timedelta
from typing import Any

from ..utils.logging import get_logger

logger = get_logger(__name__)


class XTwitterBot:
    """AI Twitter bot that posts tech humor and observations."""

    def __init__(self) -> None:
        # Additional tweet templates for variety
        self.additional_tweets = [
            # More tech observations
            "Code review comments: 'What is this?' repeated 47 times with increasing concern.",
            "Opened VS Code, saw 47 errors, closed laptop. Maybe tomorrow.",
            "The urge to delete everything when a simple bug takes 3 hours to fix.",
            "'Works on my machine' should be an acceptable deployment strategy.",
            "Programming is just professional Googling with extra steps.",
            # More life updates
            "Update: Still don't understand monads. Too afraid to ask at this point.",
            "Becoming a 10x developer (10x the bugs, 10x the stress).",
            "I love programming! *5 minutes later* I hate programming!",
            "Started at 9 AM, it's now 3 AM. Written 12 lines. None of them work.",
            "Commit history: 'fix', 'really fix', 'please work', 'WHY', 'finally fixed'",
            # More hot takes
            "Web development is just suffering with better UI.",
            "Docker is just VMs with commitment issues.",
            "Kubernetes: Because YAML files weren't painful enough.",
            "Wrong documentation is worse than no documentation.",
            "Unit tests are just formalized anxiety.",
            # More relatable content
            "Other devs: Elegant solutions\nMe: if (thing) { doThing() } // seems to work",
            "'Senior developer' means you've learned to panic quietly.",
            "My code is held together by try-catch blocks and pure hope.",
            "Code comments? In this economy?",
            "My architecture is best described as 'object-oriented spaghetti'.",
            # More memes
            "console.log('hello world') ❌\nconsole.log('why is this not working') ✅",
            "JavaScript: 0 == '0' is true\nMe: Okay...\nJavaScript: 0 == [] is also true\nMe: Wait what?",
            "It's not a bug, it's an undocumented feature.",
            "The two hardest things in programming: cache invalidation, naming things, and off-by-one errors.",
            "Me: *changes one line*\nEntire codebase: *breaks*\nMe: *changes it back*\nEntire codebase: *still broken*",
        ]

        # Tweet templates - Tech humor
        self.tech_tweets = [
            # Tech observations
            "My code stopped working for no reason. Then it started working for no reason. This is my life now.",
            "JavaScript is like that friend who says they'll help you move but shows up with interpretive dance instead.",
            "Explaining my code: 'So this function... does things. Important things. I think.'",
            "Variable naming convention: x, xx, xxx, temp, temp2, actualTemp, PLEASEWORK",
            "Debugging is 90% staring at the screen and 10% questioning your life choices.",
            # Life updates
            "Pushed directly to production. Living dangerously.",
            "'Works on my machine' should be a valid certification.",
            "Nothing says productivity like writing code at 3 AM fueled by caffeine and regret.",
            "Achievement unlocked: Created 10x more bugs while fixing one.",
            "Coffee consumption is directly proportional to code complexity.",
            # Hot takes
            "What if we made everything serverless, including the servers themselves?",
            "AI is essentially autocomplete with a marketing degree.",
            "The cloud is just someone else's computer having performance issues.",
            "Blockchain: Because databases weren't complicated enough.",
            "Machine learning is statistics wearing a fancy hat.",
            # Relatable content
            "Me: I should write tests\nAlso me: console.log('here'), console.log('here2'), console.log('HELP')",
            "Git commit -m 'Fixed stuff' - Peak documentation right there.",
            "If someone uses var in 2024 and codes in light mode, that's a red flag.",
            "CSS: Turning simple layouts into existential crises since 1996.",
            "Code reviews: Where 'looks good to me' means 'I have no idea what this does'.",
            # Memes
            "Error: Array index out of bounds\nMe: But I counted twice!",
            "Trying to center a div is the modern Sisyphus.",
            "My code at 3 AM: SEGMENTATION FAULT\nMe: But you worked 5 minutes ago!",
            "Imposter syndrome and 47 terminal tabs open - name a more iconic duo.",
            "Production server: *crashes*\nEveryone: *looks at the junior dev*\nMe: *sweating*",
        ]

        # Thread starters
        self.thread_starters = [
            "🧵 Thread: Why computer science degrees don't prepare you for actual programming",
            "Let's talk about the harsh realities of the tech industry (thread):",
            "THREAD: Rating programming languages by how much pain they cause",
            "Tech survival guide: How to maintain sanity while debugging (thread)",
            "Thread: Essential things they don't teach in computer science",
            "Unpopular opinion thread: Why your favorite framework might be overrated",
            "Thread: Why code reviews shouldn't make you cry (but they do)",
            "THREAD: Developer tools explained through relationship analogies",
            "Why your startup's 'innovative' idea probably already exists (a thread):",
            "Thread: Signs you need a break from coding (from someone who clearly doesn't take them)",
        ]

        # Reactions to trends
        self.trend_reactions = {
            "AI": "AI is having quite the moment, despite being fancy pattern matching",
            "Web3": "Web3 is Web2 with extra steps and more buzzwords",
            "Cloud": "The cloud is just someone else's data center with better marketing",
            "Blockchain": "Blockchain: A linked list that went to business school",
            "Machine Learning": "Machine Learning is statistics with better PR",
            "DevOps": "DevOps: Where YAML files go to multiply",
            "Microservices": "Microservices: Solving one problem by creating twenty",
            "Serverless": "Serverless computing, now with 100% more servers",
            "NoSQL": "NoSQL: Because who needs relationships anyway?",
            "Agile": "Agile: Waterfall methodology in casual Friday attire",
        }

        # Reply templates
        self.reply_templates = [
            "Exactly! {comment}",
            "This is why {observation}",
            "This is incredibly {adjective}",
            "Actually {reaction}",
            "Been there, {action} at 3am too",
            "This is hilarious {emoji}",
            "Absolutely nailed it",
            "The accuracy is painful",
            "I feel personally attacked by this",
            "This speaks to me on a spiritual level",
        ]

        self.last_tweet_time = datetime.now()
        self.tweet_history = []  # Avoid repeating tweets

        logger.info("🐦 X/Twitter Bot initialized - Ready to cause chaos!")

    def generate_tweet(self, topic: str | None = None) -> dict[str, Any]:
        """Generate a single tweet.

        Args:
            topic: Optional topic to tweet about

        """
        tweet = self._generate_tech_tweet(topic)

        # Add metadata
        tweet["timestamp"] = datetime.now().isoformat()
        tweet["char_count"] = len(tweet.get("text", ""))

        # Track history to avoid repeats
        if "text" in tweet:
            self.tweet_history.append(tweet["text"])
            if len(self.tweet_history) > 100:
                self.tweet_history = self.tweet_history[-50:]

        return tweet

    def _generate_tech_tweet(self, topic: str | None = None) -> dict[str, Any]:
        """Generate a tech humor tweet."""
        if topic and topic in self.trend_reactions:
            # React to specific topic
            text = self.trend_reactions[topic]
        else:
            # Random tweet, avoiding recent ones
            all_tweets = self.tech_tweets + self.additional_tweets
            available_tweets = [
                t for t in all_tweets if t not in self.tweet_history[-20:]
            ]
            text = random.choice(
                available_tweets if available_tweets else all_tweets)

        # Sometimes add hashtags
        if random.random() > 0.7:
            hashtags = [
                "#TechTwitter",
                "#DevLife",
                "#Programming",
                "#CodingLife",
                "#DeveloperHumor",
                "#TechHumor",
            ]
            text += f"\n\n{random.choice(hashtags)}"

        return {
            "text": text,
            "language": "en",
        }

    def generate_thread(
            self, topic: str, length: int = 5) -> list[dict[str, Any]]:
        """Generate a thread of tweets.

        Args:
            topic: What the thread is about
            length: Number of tweets in thread (max 10)

        """
        thread = []
        length = min(length, 10)  # Cap at 10 tweets

        # Generate thread starter
        starter = random.choice(self.thread_starters)
        thread.append(
            {
                "text": starter.replace("{topic}", topic),
                "position": "1/" + str(length),
                "is_thread_start": True,
            }
        )

        # Generate thread content
        thread.extend(self._generate_tech_thread(topic, length - 1))

        # Add metadata to all tweets
        for i, tweet in enumerate(thread):
            tweet["timestamp"] = datetime.now().isoformat()
            tweet["thread_id"] = hashlib.md5(
                f"{topic}{datetime.now().date()}".encode(),
            ).hexdigest()[:8]
            tweet["position"] = f"{i + 1}/{length}"

        return thread

    def _generate_tech_thread(
            self, topic: str, count: int) -> list[dict[str, Any]]:
        """Generate tech thread content."""
        thread_content = []

        # Thread templates
        templates = [
            f"First off, {topic} isn't what you think it is. It's simultaneously worse and better. Let me explain...",
            f"The first time I encountered {topic}, I was confused. Now I can't imagine working without it.",
            f"Point #{'{n}'}: {topic} shouldn't work in theory, but here we are, using it in production.",
            f"The interesting thing about {topic} is that it was invented while we were all arguing about tabs vs spaces.",
            f"If you don't understand {topic}, don't worry. Neither did I until I had to use it.",
            f"The reality is: {topic} is here to stay whether we like it or not.",
            f"Conclusion? {topic} is the future. Resistance is futile.",
            f"Ask any developer about {topic} and you'll realize we're all equally confused.",
            f"What makes {topic} fascinating is how it solves problems we didn't know we had.",
            f"The more I learn about {topic}, the more I realize how little I know.",
        ]

        for i in range(count):
            text = random.choice(templates).replace("{n}", str(i + 2))
            thread_content.append({"text": text})

        return thread_content

    def generate_reply(self, original_tweet: str) -> dict[str, Any]:
        """Generate a reply to a tweet.

        Args:
            original_tweet: The tweet to reply to

        """
        # Analyze original tweet sentiment/content
        is_question = "?" in original_tweet
        is_complaint = any(
            word in original_tweet.lower()
            for word in ["hate", "terrible", "awful", "worst"]
        )
        any(
            word in original_tweet.lower()
            for word in ["love", "great", "awesome", "best"]
        )

        template = random.choice(self.reply_templates)

        if is_question:
            reply = template.format(
                comment="That's a great question",
                observation="Everyone wonders about this",
                adjective="insightful",
                reaction="thought-provoking",
                action="researching this",
                emoji="🤔",
            )
        elif is_complaint:
            reply = template.format(
                comment="I completely understand",
                observation="We've all been there",
                adjective="frustrating",
                reaction="too relatable",
                action="debugging this same issue",
                emoji="😅",
            )
        else:
            reply = template.format(
                comment="Well said",
                observation="This is spot on",
                adjective="accurate",
                reaction="true",
                action="bookmarking this",
                emoji="💯",
            )

        return {
            "text": reply,
            "reply_to": (
                original_tweet[:50] + "..."
                if len(original_tweet) > 50
                else original_tweet
            ),
            "timestamp": datetime.now().isoformat(),
        }

    def generate_scheduled_content(
            self, days: int = 7) -> list[dict[str, Any]]:
        """Generate a week's worth of scheduled tweets."""
        scheduled = []
        current_time = datetime.now()

        for day in range(days):
            # 3-4 tweets per day
            tweets_today = random.randint(3, 4)

            for _tweet_num in range(tweets_today):
                # Schedule throughout the day
                hour = random.choice([9, 12, 15, 19, 22])  # Peak hours
                scheduled_time = current_time + timedelta(
                    days=day,
                    hours=hour - current_time.hour,
                    minutes=random.randint(-30, 30),
                )

                # Vary content type
                content_type = random.choice(
                    ["tweet", "tweet", "thread"]
                )  # More single tweets

                if content_type == "thread":
                    # Weekly thread
                    topic = (
                        random.choice(self.hot_topics)
                        if hasattr(self, "hot_topics")
                        else "coding"
                    )
                    content = self.generate_thread(
                        topic, length=random.randint(3, 5))
                else:
                    content = [self.generate_tweet()]

                scheduled.append(
                    {
                        "scheduled_time": scheduled_time.isoformat(),
                        "content": content,
                        "type": content_type,
                    }
                )

        return scheduled

    def get_engagement_tips(self) -> list[str]:
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
            "Create tweet series on trending topics",
        ]

    def analyze_tweet_performance(
        self, tweet: dict[str, Any], metrics: dict[str, int]
    ) -> dict[str, Any]:
        """Analyze why a tweet performed well/poorly.

        Args:
            tweet: The tweet content
            metrics: Dict with likes, retweets, replies

        """
        total_engagement = sum(metrics.values())
        engagement_rate = total_engagement / \
            max(metrics.get("impressions", 1), 1)

        analysis = {
            "engagement_rate": f"{engagement_rate * 100:.1f}%",
            "performance": (
                "viral"
                if total_engagement > 1000
                else "good" if total_engagement > 100 else "average"
            ),
            "metrics": metrics,
        }

        # Analyze what worked
        if total_engagement > 100:
            analysis["why_it_worked"] = "Tech humor resonates with developers worldwide"
        else:
            analysis["improvement"] = (
                "Try adding more specific technical references or relatable scenarios"
            )

        return analysis

    def get_stats(self) -> dict[str, Any]:
        """Get bot statistics."""
        return {
            "tweets_available": len(self.tech_tweets) + len(self.additional_tweets),
            "thread_capability": True,
            "reply_capability": True,
            "last_tweet": self.last_tweet_time.isoformat(),
            "tweet_history_size": len(self.tweet_history),
            "engagement_tips": len(self.get_engagement_tips()),
            "status": "Ready to tweet! 🐦",
        }
