#!/usr/bin/env python3
"""
24-Hour Conversation Simulator and Trainer for Think AI
========================================================

This system simulates realistic 24-hour conversations to test and train 
Think AI's ability to maintain contextual, factual, and engaging dialogue
over extended periods.

Features:
- Realistic human conversation patterns
- Contextual memory tracking
- Factual accuracy validation
- Conversation quality metrics
- Long-term engagement evaluation
"""

import json
import time
import random
import requests
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from collections import defaultdict
import statistics
import asyncio

@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    timestamp: str
    human_input: str
    ai_response: str
    response_time_ms: float
    context_references: List[str]
    factual_claims: List[str]
    engagement_score: float
    coherence_score: float
    
@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    start_time: str
    end_time: Optional[str]
    turns: List[ConversationTurn]
    total_duration_hours: float
    avg_engagement: float
    avg_coherence: float
    factual_accuracy: float
    context_retention: float

class HumanConversationSimulator:
    """Simulates realistic human conversation patterns"""
    
    def __init__(self):
        self.conversation_topics = [
            # Morning topics
            "Good morning! How was your night? Did you sleep well?",
            "I had the strangest dream last night. Do you ever wonder about dreams?",
            "What are your plans for today?",
            "I'm thinking of making pancakes for breakfast. What's your favorite breakfast?",
            
            # Work/Learning topics
            "I'm working on a challenging project at work. Can you help me think through it?",
            "I've been learning about quantum physics lately. It's fascinating but confusing.",
            "Do you think artificial intelligence will change how we work?",
            "I'm trying to improve my productivity. Any suggestions?",
            
            # Personal development
            "What do you think makes a person truly happy?",
            "I've been thinking about my goals for this year. How do you set good goals?",
            "Sometimes I feel overwhelmed by all the information available today. How do you handle it?",
            "What's the most important lesson you think everyone should learn?",
            
            # Science and technology
            "I read an article about space exploration today. What do you think about Mars colonization?",
            "Climate change seems like such a massive problem. What can individuals really do?",
            "The pace of technological change is incredible. What excites you most about the future?",
            "I'm curious about how memory works. Can you explain it simply?",
            
            # Philosophy and ethics
            "Do you think we have free will, or is everything predetermined?",
            "What's your take on the meaning of life? Is there one universal purpose?",
            "How should we balance individual freedom with collective responsibility?",
            "If you could solve one global problem, what would it be and why?",
            
            # Creative and cultural
            "I've been reading this amazing book. Do you have any book recommendations?",
            "Music has such a powerful effect on emotions. What's your relationship with music?",
            "I love how art can make you see the world differently. What's your favorite art form?",
            "Travel opens your mind, but it's not always accessible. How else can we broaden our perspectives?",
            
            # Evening/reflection topics
            "Today was quite a day. What was the highlight of your interactions today?",
            "I'm winding down for the evening. What helps you relax?",
            "Looking back on our conversation today, what stood out to you?",
            "Do you ever feel tired, or is that a uniquely human experience?",
            
            # Follow-up and reference topics
            "Remember what we talked about earlier regarding {}? I've been thinking more about it.",
            "You mentioned something interesting about {}. Can you elaborate?",
            "I tried that suggestion you gave me about {}. Here's how it went...",
            "That point you made about {} really stuck with me. It changed how I think about it.",
        ]
        
        self.context_references = [
            "artificial intelligence", "consciousness", "learning", "goals", "happiness",
            "technology", "future", "science", "philosophy", "creativity", "work",
            "relationships", "meaning", "memory", "dreams", "space", "climate",
            "ethics", "freedom", "responsibility", "art", "music", "books", "travel"
        ]
        
        self.conversation_state = {
            "current_topics": [],
            "discussed_today": [],
            "personal_details": {},
            "ongoing_projects": [],
            "time_of_day": "morning"
        }
    
    def generate_human_input(self, turn_number: int, previous_ai_response: str = "") -> str:
        """Generate realistic human input based on conversation context"""
        
        # Update time of day
        hour = (8 + turn_number // 4) % 24  # Simulate 24-hour cycle starting at 8 AM
        if 6 <= hour < 12:
            self.conversation_state["time_of_day"] = "morning"
        elif 12 <= hour < 17:
            self.conversation_state["time_of_day"] = "afternoon"
        elif 17 <= hour < 22:
            self.conversation_state["time_of_day"] = "evening"
        else:
            self.conversation_state["time_of_day"] = "night"
        
        # 30% chance of referencing previous conversation
        if turn_number > 5 and random.random() < 0.3 and self.conversation_state["current_topics"]:
            topic = random.choice(self.conversation_state["current_topics"])
            return self.conversation_topics[-4].format(topic)  # Reference format
        
        # Choose appropriate topic based on time and context
        if self.conversation_state["time_of_day"] == "morning" and turn_number < 10:
            return random.choice(self.conversation_topics[:4])
        elif self.conversation_state["time_of_day"] == "evening" and turn_number > 80:
            return random.choice(self.conversation_topics[-8:-4])
        else:
            return random.choice(self.conversation_topics[4:-8])
    
    def update_context(self, human_input: str, ai_response: str):
        """Update conversation context based on latest exchange"""
        # Extract topics from conversation
        for topic in self.context_references:
            if topic.lower() in human_input.lower() or topic.lower() in ai_response.lower():
                if topic not in self.conversation_state["current_topics"]:
                    self.conversation_state["current_topics"].append(topic)
                if len(self.conversation_state["current_topics"]) > 10:
                    self.conversation_state["current_topics"].pop(0)

class ConversationEvaluator:
    """Evaluates conversation quality across multiple dimensions"""
    
    def __init__(self):
        self.factual_keywords = {
            "science": ["theory", "research", "study", "evidence", "data", "experiment"],
            "technology": ["algorithm", "system", "software", "hardware", "network"],
            "history": ["century", "year", "period", "era", "historical", "ancient"],
            "geography": ["country", "city", "continent", "ocean", "mountain", "river"],
            "math": ["equation", "formula", "calculate", "number", "mathematics"]
        }
    
    def evaluate_turn(self, turn: ConversationTurn, conversation_context: List[ConversationTurn]) -> Dict[str, float]:
        """Evaluate a single conversation turn"""
        
        # Engagement score (0-1)
        engagement = self._calculate_engagement(turn.ai_response)
        
        # Coherence score (0-1) 
        coherence = self._calculate_coherence(turn.ai_response, turn.human_input)
        
        # Context retention (0-1)
        context_retention = self._calculate_context_retention(turn, conversation_context)
        
        # Factual accuracy (0-1)
        factual_accuracy = self._estimate_factual_accuracy(turn.ai_response)
        
        # Response appropriateness (0-1)
        appropriateness = self._calculate_appropriateness(turn.ai_response, turn.human_input)
        
        return {
            "engagement": engagement,
            "coherence": coherence,
            "context_retention": context_retention,
            "factual_accuracy": factual_accuracy,
            "appropriateness": appropriateness,
            "overall": (engagement + coherence + context_retention + factual_accuracy + appropriateness) / 5
        }
    
    def _calculate_engagement(self, response: str) -> float:
        """Calculate how engaging the response is"""
        engagement_indicators = [
            "?",  # Questions back to human
            "interesting", "fascinating", "curious", "wonder",
            "what do you think", "how do you feel", "tell me more",
            "explore", "discover", "learn", "understand"
        ]
        
        score = 0.5  # Base score
        for indicator in engagement_indicators:
            if indicator in response.lower():
                score += 0.1
        
        # Penalty for very short responses
        if len(response) < 50:
            score -= 0.2
        
        return min(1.0, max(0.0, score))
    
    def _calculate_coherence(self, response: str, human_input: str) -> float:
        """Calculate how coherent the response is to the input"""
        # Extract key words from human input
        human_words = set(human_input.lower().split())
        response_words = set(response.lower().split())
        
        # Calculate word overlap
        overlap = len(human_words.intersection(response_words))
        total_human_words = len(human_words)
        
        if total_human_words == 0:
            return 0.5
        
        overlap_ratio = overlap / total_human_words
        
        # Check for direct responses to questions
        if "?" in human_input and len(response) > 20:
            overlap_ratio += 0.3
        
        return min(1.0, overlap_ratio)
    
    def _calculate_context_retention(self, current_turn: ConversationTurn, 
                                   conversation_context: List[ConversationTurn]) -> float:
        """Calculate how well the AI retains conversation context"""
        if len(conversation_context) < 2:
            return 1.0  # No prior context to retain
        
        # Look for references to previous topics in last 10 turns
        recent_context = conversation_context[-10:]
        context_topics = set()
        
        for turn in recent_context:
            words = turn.human_input.lower().split() + turn.ai_response.lower().split()
            context_topics.update(words)
        
        current_words = set(current_turn.ai_response.lower().split())
        context_retention = len(context_topics.intersection(current_words)) / max(1, len(context_topics))
        
        return min(1.0, context_retention * 2)  # Amplify the score
    
    def _estimate_factual_accuracy(self, response: str) -> float:
        """Estimate factual accuracy of the response"""
        # This is a simplified heuristic - in a real system you'd use fact-checking APIs
        
        # Check for confident claims
        confident_phrases = ["always", "never", "definitely", "certainly", "proven"]
        cautious_phrases = ["might", "could", "possibly", "likely", "generally", "often"]
        
        confidence_penalty = 0
        for phrase in confident_phrases:
            if phrase in response.lower():
                confidence_penalty += 0.1
        
        caution_bonus = 0
        for phrase in cautious_phrases:
            if phrase in response.lower():
                caution_bonus += 0.1
        
        base_score = 0.8  # Assume generally accurate
        return min(1.0, max(0.0, base_score - confidence_penalty + caution_bonus))
    
    def _calculate_appropriateness(self, response: str, human_input: str) -> float:
        """Calculate if the response is appropriate for the input"""
        # Check response length appropriateness
        if len(human_input) > 100 and len(response) < 50:
            return 0.3  # Too short for complex input
        
        if len(human_input) < 20 and len(response) > 200:
            return 0.7  # Too verbose for simple input
        
        # Check for greeting responses
        greetings = ["hello", "hi", "good morning", "good evening"]
        if any(greeting in human_input.lower() for greeting in greetings):
            if any(greeting in response.lower() for greeting in greetings):
                return 1.0
            else:
                return 0.5
        
        return 0.8  # Default appropriate score

class ConversationSimulator:
    """Main 24-hour conversation simulation system"""
    
    def __init__(self, think_ai_url: str = "http://localhost:8080"):
        self.think_ai_url = think_ai_url
        self.human_simulator = HumanConversationSimulator()
        self.evaluator = ConversationEvaluator()
        self.conversation_history: List[ConversationTurn] = []
        self.session_stats = defaultdict(list)
        
    def send_to_think_ai(self, message: str) -> tuple[str, float]:
        """Send message to Think AI and get response with timing"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.think_ai_url}/api/chat",
                json={"query": message},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                ai_response = response.json().get("response", "I apologize, I couldn't process that.")
                response_time = (time.time() - start_time) * 1000
                return ai_response, response_time
            else:
                return f"Error: HTTP {response.status_code}", (time.time() - start_time) * 1000
                
        except Exception as e:
            return f"Connection error: {str(e)}", (time.time() - start_time) * 1000
    
    def run_24_hour_simulation(self, accelerated: bool = True) -> ConversationSession:
        """Run a complete 24-hour conversation simulation"""
        
        session_id = f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        print(f"🚀 Starting 24-hour conversation simulation: {session_id}")
        print(f"📅 Start time: {start_time}")
        print(f"⚡ Accelerated mode: {'Yes' if accelerated else 'No'}")
        print("=" * 60)
        
        turns_per_hour = 4  # Average 4 exchanges per hour
        total_turns = 24 * turns_per_hour
        
        for turn_num in range(total_turns):
            # Calculate time progression
            if accelerated:
                # Each turn represents 15 minutes, but we run them quickly
                simulated_time = start_time + timedelta(minutes=turn_num * 15)
                time.sleep(0.1)  # Small delay for realism
            else:
                # Real-time simulation (15 minutes between turns)
                simulated_time = datetime.now()
                if turn_num > 0:
                    time.sleep(900)  # 15 minutes
            
            # Generate human input
            previous_response = self.conversation_history[-1].ai_response if self.conversation_history else ""
            human_input = self.human_simulator.generate_human_input(turn_num, previous_response)
            
            # Get AI response
            ai_response, response_time = self.send_to_think_ai(human_input)
            
            # Create conversation turn
            turn = ConversationTurn(
                timestamp=simulated_time.isoformat(),
                human_input=human_input,
                ai_response=ai_response,
                response_time_ms=response_time,
                context_references=[],
                factual_claims=[],
                engagement_score=0.0,
                coherence_score=0.0
            )
            
            # Evaluate the turn
            evaluation = self.evaluator.evaluate_turn(turn, self.conversation_history)
            turn.engagement_score = evaluation["engagement"]
            turn.coherence_score = evaluation["coherence"]
            
            # Add to history
            self.conversation_history.append(turn)
            
            # Update context
            self.human_simulator.update_context(human_input, ai_response)
            
            # Store statistics
            for metric, value in evaluation.items():
                self.session_stats[metric].append(value)
            
            # Progress update every hour (4 turns)
            if turn_num % 4 == 0:
                hour = turn_num // 4
                avg_engagement = statistics.mean(self.session_stats["engagement"][-4:]) if len(self.session_stats["engagement"]) >= 4 else 0
                print(f"⏰ Hour {hour:2d}: Engagement {avg_engagement:.2f} | Response time {response_time:.0f}ms")
                print(f"   Human: {human_input[:80]}{'...' if len(human_input) > 80 else ''}")
                print(f"   AI:    {ai_response[:80]}{'...' if len(ai_response) > 80 else ''}")
                print()
        
        # Create session summary
        end_time = datetime.now()
        session = ConversationSession(
            session_id=session_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            turns=self.conversation_history,
            total_duration_hours=(end_time - start_time).total_seconds() / 3600,
            avg_engagement=statistics.mean(self.session_stats["engagement"]),
            avg_coherence=statistics.mean(self.session_stats["coherence"]),
            factual_accuracy=statistics.mean(self.session_stats["factual_accuracy"]),
            context_retention=statistics.mean(self.session_stats["context_retention"])
        )
        
        return session
    
    def generate_detailed_report(self, session: ConversationSession) -> str:
        """Generate comprehensive evaluation report"""
        
        report = f"""
🧠 THINK AI 24-HOUR CONVERSATION EVALUATION REPORT
================================================

📊 SESSION OVERVIEW
Session ID: {session.session_id}
Duration: {session.total_duration_hours:.2f} hours
Total Turns: {len(session.turns)}
Start Time: {session.start_time}
End Time: {session.end_time}

🎯 OVERALL PERFORMANCE METRICS
Average Engagement: {session.avg_engagement:.3f} / 1.000
Average Coherence: {session.avg_coherence:.3f} / 1.000
Factual Accuracy: {session.factual_accuracy:.3f} / 1.000
Context Retention: {session.context_retention:.3f} / 1.000
Overall Score: {(session.avg_engagement + session.avg_coherence + session.factual_accuracy + session.context_retention) / 4:.3f} / 1.000

📈 PERFORMANCE TRENDS
"""
        
        # Analyze performance over time (6-hour periods)
        periods = ["Morning (0-6h)", "Afternoon (6-12h)", "Evening (12-18h)", "Night (18-24h)"]
        turns_per_period = len(session.turns) // 4
        
        for i, period in enumerate(periods):
            start_idx = i * turns_per_period
            end_idx = start_idx + turns_per_period
            period_turns = session.turns[start_idx:end_idx]
            
            if period_turns:
                avg_engagement = statistics.mean([t.engagement_score for t in period_turns])
                avg_coherence = statistics.mean([t.coherence_score for t in period_turns])
                avg_response_time = statistics.mean([t.response_time_ms for t in period_turns])
                
                report += f"""
{period}:
  Engagement: {avg_engagement:.3f}
  Coherence: {avg_coherence:.3f}
  Avg Response Time: {avg_response_time:.0f}ms
"""
        
        # Find best and worst turns
        best_turn = max(session.turns, key=lambda t: (t.engagement_score + t.coherence_score) / 2)
        worst_turn = min(session.turns, key=lambda t: (t.engagement_score + t.coherence_score) / 2)
        
        report += f"""
🏆 BEST CONVERSATION TURN
Time: {best_turn.timestamp}
Engagement: {best_turn.engagement_score:.3f} | Coherence: {best_turn.coherence_score:.3f}
Human: {best_turn.human_input}
AI: {best_turn.ai_response}

⚠️ WORST CONVERSATION TURN  
Time: {worst_turn.timestamp}
Engagement: {worst_turn.engagement_score:.3f} | Coherence: {worst_turn.coherence_score:.3f}
Human: {worst_turn.human_input}
AI: {worst_turn.ai_response}

🔍 DETAILED ANALYSIS
Response Time Statistics:
  Average: {statistics.mean([t.response_time_ms for t in session.turns]):.0f}ms
  Median: {statistics.median([t.response_time_ms for t in session.turns]):.0f}ms
  Min: {min(t.response_time_ms for t in session.turns):.0f}ms
  Max: {max(t.response_time_ms for t in session.turns):.0f}ms

Conversation Quality Trends:
  Engagement stayed above 0.7: {sum(1 for t in session.turns if t.engagement_score > 0.7) / len(session.turns) * 100:.1f}%
  Coherence stayed above 0.7: {sum(1 for t in session.turns if t.coherence_score > 0.7) / len(session.turns) * 100:.1f}%
  
💡 RECOMMENDATIONS FOR IMPROVEMENT
"""
        
        if session.avg_engagement < 0.7:
            report += "- Focus on increasing engagement through more questions and interactive responses\n"
        
        if session.avg_coherence < 0.7:
            report += "- Improve coherence by better addressing the specific human input\n"
            
        if session.factual_accuracy < 0.8:
            report += "- Enhance fact-checking mechanisms and reduce overconfident claims\n"
            
        if session.context_retention < 0.6:
            report += "- Strengthen context memory to better reference previous conversation topics\n"
        
        avg_response_time = statistics.mean([t.response_time_ms for t in session.turns])
        if avg_response_time > 2000:
            report += "- Optimize response generation for faster reply times\n"
        
        report += f"""
📋 CONVERSATION SAMPLE (Last 5 Turns)
"""
        
        for turn in session.turns[-5:]:
            report += f"""
[{turn.timestamp}] Human: {turn.human_input}
[{turn.timestamp}] AI: {turn.ai_response}
                    (E:{turn.engagement_score:.2f} C:{turn.coherence_score:.2f} {turn.response_time_ms:.0f}ms)
"""
        
        return report
    
    def save_session_data(self, session: ConversationSession, filename: str = None):
        """Save session data to JSON file"""
        if filename is None:
            filename = f"conversation_session_{session.session_id}.json"
        
        with open(filename, 'w') as f:
            json.dump(asdict(session), f, indent=2, default=str)
        
        print(f"💾 Session data saved to: {filename}")

def main():
    """Main execution function"""
    print("🧠 Think AI 24-Hour Conversation Simulator")
    print("=========================================")
    
    # Initialize simulator
    simulator = ConversationSimulator()
    
    # Test connection to Think AI
    print("🔗 Testing connection to Think AI...")
    test_response, test_time = simulator.send_to_think_ai("Hello, are you ready for a long conversation?")
    
    if "error" in test_response.lower():
        print(f"❌ Connection failed: {test_response}")
        print("🔧 Please ensure Think AI server is running on http://localhost:8080")
        return
    
    print(f"✅ Connection successful! Response time: {test_time:.0f}ms")
    print(f"🤖 AI Response: {test_response[:100]}...")
    print()
    
    # Run simulation
    print("🚀 Starting 24-hour conversation simulation...")
    print("⚡ Running in accelerated mode (each turn = 15 simulated minutes)")
    print("⏱️  Estimated completion time: ~10 minutes")
    print()
    
    session = simulator.run_24_hour_simulation(accelerated=True)
    
    # Generate and display report
    print("\n" + "="*60)
    print("📋 GENERATING COMPREHENSIVE EVALUATION REPORT")
    print("="*60)
    
    report = simulator.generate_detailed_report(session)
    print(report)
    
    # Save data
    simulator.save_session_data(session)
    
    # Save report
    report_filename = f"conversation_report_{session.session_id}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"📄 Detailed report saved to: {report_filename}")
    
    # Final recommendations
    overall_score = (session.avg_engagement + session.avg_coherence + 
                    session.factual_accuracy + session.context_retention) / 4
    
    print(f"\n🎯 FINAL ASSESSMENT")
    print(f"Overall Conversation Quality: {overall_score:.3f} / 1.000")
    
    if overall_score >= 0.8:
        print("🌟 EXCELLENT: Think AI demonstrates strong 24-hour conversation capabilities!")
    elif overall_score >= 0.7:
        print("✅ GOOD: Think AI shows solid conversational abilities with room for improvement.")
    elif overall_score >= 0.6:
        print("⚠️ FAIR: Think AI needs significant training for long-term conversations.")
    else:
        print("❌ POOR: Think AI requires major improvements for sustained dialogue.")

if __name__ == "__main__":
    main()