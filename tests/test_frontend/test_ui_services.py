"""
PaddleCoach Frontend Tests
Author: Rakshit
Description: Unit tests for frontend components
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.frontend.ui_services.ui_data_service import UIDataService
from src.frontend.ui_services.stats_bot import StatsBot
from src.frontend.ui_services.elevenlabs_client import ElevenLabsClient


class TestUIDataService(unittest.TestCase):
    """Test cases for UI Data Service"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.service = UIDataService()
    
    def test_get_current_match(self):
        """Test getting current match data"""
        match = self.service.get_current_match()
        
        self.assertIsNotNone(match)
        self.assertIn('match_id', match)
        self.assertIn('player1', match)
        self.assertIn('player2', match)
        self.assertEqual(match['status'], 'not_started')
    
    def test_get_match_by_id(self):
        """Test getting specific match by ID"""
        match_id = 1
        match = self.service.get_match_by_id(match_id)
        
        self.assertIsNotNone(match)
        self.assertEqual(match['match_id'], match_id)
        self.assertIn('player1', match)
        self.assertIn('player2', match)
        self.assertIn('sets', match)
    
    def test_get_player_stats(self):
        """Test getting player statistics"""
        player_id = 1
        stats = self.service.get_player_stats(player_id)
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['player_id'], player_id)
        self.assertIn('total_matches', stats)
        self.assertIn('win_rate', stats)
        self.assertIn('shot_stats', stats)
        self.assertIn('performance_trend', stats)
    
    def test_get_coaching_insights(self):
        """Test getting coaching insights"""
        player_id = 1
        insights = self.service.get_coaching_insights(player_id)
        
        self.assertIsNotNone(insights)
        self.assertEqual(insights['player_id'], player_id)
        self.assertIn('insights', insights)
        self.assertIn('pro_comparison', insights)
        self.assertTrue(len(insights['insights']) > 0)
    
    def test_get_live_match_stats(self):
        """Test getting live match statistics"""
        match_id = 1
        stats = self.service.get_live_match_stats(match_id)
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['match_id'], match_id)
        self.assertIn('total_shots', stats)
        self.assertIn('avg_rally_length', stats)
    
    def test_get_player_list(self):
        """Test getting player list"""
        players = self.service.get_player_list()
        
        self.assertIsNotNone(players)
        self.assertIsInstance(players, list)
        self.assertTrue(len(players) > 0)
        self.assertIn('id', players[0])
        self.assertIn('name', players[0])


class TestStatsBot(unittest.TestCase):
    """Test cases for Stats Bot"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.bot = StatsBot()
    
    def test_greeting(self):
        """Test greeting response"""
        response = self.bot.process_query("Hello")
        self.assertIn("Hello", response)
    
    def test_help_request(self):
        """Test help message"""
        response = self.bot.process_query("help")
        self.assertIn("questions", response.lower())
    
    def test_total_matches_query(self):
        """Test total matches query"""
        response = self.bot.process_query("How many matches have I played?")
        self.assertIn("matches", response.lower())
    
    def test_win_rate_query(self):
        """Test win rate query"""
        response = self.bot.process_query("What's my win rate?")
        self.assertIn("win rate", response.lower())
        self.assertIn("%", response)
    
    def test_best_shot_query(self):
        """Test best shot query"""
        response = self.bot.process_query("What's my best shot?")
        self.assertIn("best shot", response.lower())
    
    def test_accuracy_query(self):
        """Test accuracy query"""
        response = self.bot.process_query("How accurate am I?")
        self.assertIn("accuracy", response.lower())
        self.assertIn("%", response)
    
    def test_serve_stats_query(self):
        """Test serve statistics query"""
        response = self.bot.process_query("Tell me about my serve")
        self.assertIn("serve", response.lower())
    
    def test_forehand_stats_query(self):
        """Test forehand statistics query"""
        response = self.bot.process_query("How is my forehand?")
        self.assertIn("forehand", response.lower())
    
    def test_improvement_query(self):
        """Test improvement query"""
        response = self.bot.process_query("Am I improving?")
        self.assertIn("improvement", response.lower())
    
    def test_unknown_query(self):
        """Test unknown query handling"""
        response = self.bot.process_query("What is the weather today?")
        self.assertIn("not sure", response.lower())
    
    def test_set_player_context(self):
        """Test setting player context"""
        player_data = {'player_id': 1, 'name': 'Test Player'}
        self.bot.set_player_context(1, player_data)
        self.assertEqual(self.bot.context['player_id'], 1)
    
    def test_clear_context(self):
        """Test clearing context"""
        self.bot.set_player_context(1, {})
        self.bot.clear_context()
        self.assertEqual(len(self.bot.context), 0)


class TestElevenLabsClient(unittest.TestCase):
    """Test cases for ElevenLabs Client"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = ElevenLabsClient()
    
    def test_initialization(self):
        """Test client initialization"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.base_url, 'https://api.elevenlabs.io/v1')
    
    def test_generate_speech_without_api_key(self):
        """Test speech generation without API key (mock mode)"""
        result = self.client.generate_speech("Test text")
        # Should return empty string or mock audio path
        self.assertIsInstance(result, str)
    
    def test_create_commentary_text(self):
        """Test commentary text creation"""
        event = {
            'type': 'point',
            'winner': 'Player 1',
            'rally_length': 8
        }
        text = self.client._create_commentary_text(event)
        self.assertIn('Player 1', text)
        self.assertIn('8', text)
    
    def test_create_commentary_text_game(self):
        """Test game commentary"""
        event = {
            'type': 'game',
            'winner': 'Player 2',
            'score': '11-9'
        }
        text = self.client._create_commentary_text(event)
        self.assertIn('Player 2', text)
        self.assertIn('11-9', text)
    
    def test_create_commentary_text_match(self):
        """Test match commentary"""
        event = {
            'type': 'match',
            'winner': 'Player 1',
            'final_score': '3-2'
        }
        text = self.client._create_commentary_text(event)
        self.assertIn('Player 1', text)
        self.assertIn('3-2', text)
    
    def test_create_feedback_text(self):
        """Test feedback text creation"""
        feedback = {
            'type': 'technique',
            'message': 'Great forehand follow-through'
        }
        text = self.client._create_feedback_text(feedback)
        self.assertIn('technique', text.lower())
        self.assertIn('forehand', text.lower())
    
    def test_get_mock_voices(self):
        """Test getting mock voices"""
        voices = self.client._get_mock_voices()
        self.assertIsInstance(voices, list)
        self.assertTrue(len(voices) > 0)
        self.assertIn('voice_id', voices[0])
    
    def test_set_voice(self):
        """Test setting default voice"""
        voice_id = 'test_voice'
        self.client.set_voice(voice_id)
        self.assertEqual(self.client.default_voice_id, voice_id)


class TestIntegration(unittest.TestCase):
    """Integration tests for frontend components"""
    
    def test_service_to_bot_integration(self):
        """Test integration between UI service and Stats Bot"""
        service = UIDataService()
        bot = StatsBot()
        
        # Get player stats
        stats = service.get_player_stats(1)
        
        # Set bot context
        bot.set_player_context(1, stats)
        
        # Query bot
        response = bot.process_query("What's my win rate?")
        
        self.assertIsNotNone(response)
        self.assertIn("win rate", response.lower())
    
    def test_service_to_elevenlabs_integration(self):
        """Test integration between UI service and ElevenLabs"""
        service = UIDataService()
        client = ElevenLabsClient()
        
        # Get coaching insights
        insights = service.get_coaching_insights(1)
        
        # Generate audio for first insight
        if insights['insights']:
            feedback = {
                'type': 'technique',
                'message': insights['insights'][0]['description']
            }
            audio = client.generate_coaching_feedback(feedback)
            self.assertIsInstance(audio, str)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUIDataService))
    suite.addTests(loader.loadTestsFromTestCase(TestStatsBot))
    suite.addTests(loader.loadTestsFromTestCase(TestElevenLabsClient))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
