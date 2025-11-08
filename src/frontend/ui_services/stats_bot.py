"""
PaddleCoach - Stats Bot
Author: Rakshit
Description: Conversational interface for querying player statistics using natural language
"""

import re
from datetime import datetime, timedelta


class StatsBot:
    """
    Conversational bot for answering natural language queries about player statistics.
    Uses pattern matching and will integrate with Gemini API for advanced NLP.
    """
    
    def __init__(self):
        """Initialize StatsBot"""
        self.context = {}
        self.player_data = {}  # Cache for player data
        
        # Define query patterns and handlers
        self.patterns = {
            r'(how many|total) matches': self._handle_total_matches,
            r'win rate|winning percentage': self._handle_win_rate,
            r'(best|strongest) shot': self._handle_best_shot,
            r'(worst|weakest) shot': self._handle_worst_shot,
            r'(recent|last) (\d+) matches': self._handle_recent_matches,
            r'accuracy|precise': self._handle_accuracy,
            r'serve': self._handle_serve_stats,
            r'forehand': self._handle_forehand_stats,
            r'backhand': self._handle_backhand_stats,
            r'improvement|progress': self._handle_improvement,
            r'compare|comparison': self._handle_comparison,
            r'(last|previous) (month|week)': self._handle_time_period,
        }
    
    def process_query(self, query):
        """
        Process a natural language query and return a response
        
        Args:
            query (str): User's natural language question
            
        Returns:
            str: Response to the query
        """
        query_lower = query.lower().strip()
        
        # Check for greeting
        if any(greeting in query_lower for greeting in ['hi', 'hello', 'hey']):
            return "Hello! I'm here to help you understand your ping pong statistics. What would you like to know?"
        
        # Check for help request
        if 'help' in query_lower or 'what can you' in query_lower:
            return self._get_help_message()
        
        # Try to match patterns
        for pattern, handler in self.patterns.items():
            if re.search(pattern, query_lower):
                return handler(query_lower)
        
        # Default response if no pattern matches
        return self._handle_unknown_query(query)
    
    def _handle_total_matches(self, query):
        """Handle queries about total matches"""
        # Mock data - will integrate with real player stats
        total = 24
        wins = 16
        losses = 8
        
        return f"You've played {total} matches in total, winning {wins} and losing {losses}. That's a win rate of {(wins/total)*100:.1f}%!"
    
    def _handle_win_rate(self, query):
        """Handle queries about win rate"""
        win_rate = 66.7
        trend = "up 5% from last month"
        
        return f"Your current win rate is {win_rate}%. This is {trend}. Keep up the good work!"
    
    def _handle_best_shot(self, query):
        """Handle queries about best shot type"""
        best_shot = "serve"
        accuracy = 82
        
        return f"Your best shot is your {best_shot} with {accuracy}% accuracy. You're really consistent with it!"
    
    def _handle_worst_shot(self, query):
        """Handle queries about worst shot type"""
        worst_shot = "smash"
        success_rate = 15
        
        return f"Your {worst_shot} has a {success_rate}% success rate, which could use some improvement. I recommend practicing placement over power."
    
    def _handle_recent_matches(self, query):
        """Handle queries about recent matches"""
        # Extract number if specified
        match = re.search(r'(\d+)', query)
        num_matches = int(match.group(1)) if match else 5
        
        return f"In your last {num_matches} matches, you won 3 and lost 2. Your average score was 18.5 points per match."
    
    def _handle_accuracy(self, query):
        """Handle queries about shot accuracy"""
        forehand = 72
        backhand = 65
        overall = 68.5
        
        return f"Your overall shot accuracy is {overall}%. Specifically: Forehand {forehand}%, Backhand {backhand}%."
    
    def _handle_serve_stats(self, query):
        """Handle queries about serve statistics"""
        accuracy = 82
        aces = 15
        placement = "mostly to forehand side"
        
        return f"Your serve stats: {accuracy}% accuracy with {aces} aces in recent matches. You serve {placement}. Consider varying your placement more."
    
    def _handle_forehand_stats(self, query):
        """Handle queries about forehand"""
        accuracy = 72
        usage = 35
        improvement = "+8% from last month"
        
        return f"Your forehand accuracy is {accuracy}%, making up {usage}% of your total shots. This is {improvement}. Great progress!"
    
    def _handle_backhand_stats(self, query):
        """Handle queries about backhand"""
        accuracy = 65
        usage = 25
        
        return f"Your backhand has {accuracy}% accuracy and represents {usage}% of your shots. This is an area where you could improve."
    
    def _handle_improvement(self, query):
        """Handle queries about improvement and progress"""
        improvements = [
            "Forehand accuracy: +8%",
            "Win rate: +5%",
            "Rally length: +2.3 shots average"
        ]
        
        return f"You've shown great improvement recently! Key areas:\n- {improvements[0]}\n- {improvements[1]}\n- {improvements[2]}"
    
    def _handle_comparison(self, query):
        """Handle queries about comparison with others"""
        return "Compared to players at your level, your serve accuracy is 15% above average, but your backhand could use work. You rank in the top 30% overall."
    
    def _handle_time_period(self, query):
        """Handle queries about specific time periods"""
        if 'month' in query:
            period = "last month"
            matches = 8
            wins = 6
        else:
            period = "last week"
            matches = 3
            wins = 2
        
        return f"In the {period}, you played {matches} matches and won {wins} of them."
    
    def _handle_unknown_query(self, query):
        """Handle queries that don't match any pattern"""
        return (
            "I'm not sure I understand that question. I can help with questions about:\n"
            "- Match statistics (wins, losses, win rate)\n"
            "- Shot analysis (forehand, backhand, serve)\n"
            "- Recent performance and trends\n"
            "- Comparisons with other players\n\n"
            "Try asking something like 'What's my win rate?' or 'How accurate is my forehand?'"
        )
    
    def _get_help_message(self):
        """Return help message with example queries"""
        return (
            "I can answer questions about your ping pong statistics! Here are some things you can ask:\n\n"
            "📊 Match Stats:\n"
            "- 'How many matches have I played?'\n"
            "- 'What's my win rate?'\n"
            "- 'Show me my recent matches'\n\n"
            "🎯 Shot Analysis:\n"
            "- 'What's my best shot?'\n"
            "- 'How accurate is my forehand?'\n"
            "- 'Tell me about my serve'\n\n"
            "📈 Trends & Improvement:\n"
            "- 'Am I improving?'\n"
            "- 'How did I do last month?'\n"
            "- 'Compare me with others'\n\n"
            "Just ask naturally, and I'll do my best to help!"
        )
    
    def set_player_context(self, player_id, player_data):
        """
        Set context for a specific player
        
        Args:
            player_id (int): Player identifier
            player_data (dict): Player's statistics data
        """
        self.context['player_id'] = player_id
        self.player_data = player_data
    
    def clear_context(self):
        """Clear current conversation context"""
        self.context = {}
        self.player_data = {}
