"""
PaddleCoach - Integration Tests
Author: Rakshit
Description: Comprehensive tests for frontend integration with AI services
"""

import os
import sys
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.frontend.ui_services.commentary_service import CommentaryService, VOICES


class IntegrationTester:
    """Main integration test class"""
    
    def __init__(self):
        """Initialize the tester"""
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        self.commentary_service = CommentaryService(env_path=env_path)
        self.test_results = []
    
    def test_commentary_generation(self, num_tests=3):
        """
        Test AI commentary generation with various scenarios
        
        Args:
            num_tests (int): Number of test cases to run
        """
        print("\n" + "="*70)
        print("TEST 1: AI Commentary Text Generation")
        print("="*70)
        
        # Test data: realistic match events
        players = ["Raks", "Ashar", "Mohnish", "Vishnu", "Alex"]
        event_types = ['point', 'game_win', 'set_win']
        contexts = [
            "with a powerful forehand smash",
            "after a long rally",
            "with an excellent serve",
            "following an unforced error",
            "with a tricky net shot",
            "after a defensive return"
        ]
        
        for i in range(num_tests):
            player = random.choice(players)
            event_type = random.choice(event_types)
            
            event_data = {
                'player_name': player,
                'event_type': event_type,
                'score': {
                    'player1': random.randint(0, 11),
                    'player2': random.randint(0, 11),
                    'set_score': f"{random.randint(1, 3)}-{random.randint(0, 2)}"
                }
            }
            
            if event_type == 'point':
                event_data['context'] = random.choice(contexts)
            
            print(f"\nTest {i+1}:")
            print(f"  Event: {event_type.upper()}")
            print(f"  Player: {player}")
            
            # Generate commentary
            commentary = self.commentary_service.generate_commentary_text(event_data)
            print(f"  Commentary: {commentary}")
            
            self.test_results.append({
                'test': f'commentary_text_{i+1}',
                'passed': len(commentary) > 0,
                'output': commentary
            })
    
    def test_audio_generation(self, num_tests=3):
        """
        Test audio generation from commentary text
        
        Args:
            num_tests (int): Number of audio files to generate
        """
        print("\n" + "="*70)
        print("TEST 2: Text-to-Speech Audio Generation")
        print("="*70)
        
        # Sample commentary texts
        commentary_texts = [
            "What an incredible shot by the player!",
            "The rally continues with both players showing excellent technique!",
            "Point scored with a powerful smash to the corner!"
        ]
        
        # Create output directory
        output_dir = "tests/audio_output"
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(min(num_tests, len(commentary_texts))):
            text = commentary_texts[i]
            output_path = os.path.join(output_dir, f"test_audio_{i+1}.mp3")
            
            print(f"\nTest {i+1}:")
            print(f"  Text: {text}")
            print(f"  Voice: Bella")
            
            # Generate audio
            audio_bytes = self.commentary_service.generate_audio(
                text, 
                output_path=output_path,
                voice_id=VOICES['BELLA']
            )
            
            if audio_bytes:
                print(f"  ✓ Audio saved to: {output_path}")
                self.test_results.append({
                    'test': f'audio_generation_{i+1}',
                    'passed': True,
                    'output': output_path
                })
            else:
                print(f"  ✗ Audio generation failed")
                self.test_results.append({
                    'test': f'audio_generation_{i+1}',
                    'passed': False,
                    'output': None
                })
    
    def test_full_integration(self, num_tests=3):
        """
        Test full integration: event → commentary text → audio
        
        Args:
            num_tests (int): Number of full integration tests
        """
        print("\n" + "="*70)
        print("TEST 3: Full Integration (Event → Text → Audio)")
        print("="*70)
        
        # Create output directory
        output_dir = "tests/integration_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Realistic game events
        test_events = [
            {
                'player_name': 'Raks',
                'event_type': 'point',
                'context': 'with a stunning backhand',
                'score': {'player1': 5, 'player2': 3}
            },
            {
                'player_name': 'Ashar',
                'event_type': 'game_win',
                'score': {'player1': 11, 'player2': 8, 'set_score': '2-1'}
            },
            {
                'player_name': 'Mohnish',
                'event_type': 'point',
                'context': 'after an intense 15-shot rally',
                'score': {'player1': 10, 'player2': 10}
            }
        ]
        
        for i, event_data in enumerate(test_events[:num_tests]):
            print(f"\nTest {i+1}:")
            print(f"  Event Type: {event_data['event_type']}")
            print(f"  Player: {event_data['player_name']}")
            
            audio_path = os.path.join(output_dir, f"commentary_{i+1}.mp3")
            
            # Generate full commentary
            result = self.commentary_service.generate_full_commentary(
                event_data,
                audio_output_path=audio_path,
                voice_id=VOICES['BELLA']
            )
            
            print(f"  Generated Text: {result['text']}")
            
            if result['audio_path']:
                print(f"  ✓ Audio saved to: {result['audio_path']}")
                
                # Try to play audio on Windows
                try:
                    import subprocess
                    subprocess.Popen(["start", "", audio_path], shell=True)
                    print(f"  ✓ Audio playback started")
                except:
                    print(f"  Note: Open {audio_path} to play manually")
                
                self.test_results.append({
                    'test': f'full_integration_{i+1}',
                    'passed': True,
                    'text': result['text'],
                    'audio': result['audio_path']
                })
            else:
                print(f"  ✗ Audio generation failed")
                self.test_results.append({
                    'test': f'full_integration_{i+1}',
                    'passed': False,
                    'text': result['text'],
                    'audio': None
                })
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("\n" + "="*70)
        print("PADDLECOACH INTEGRATION TEST SUITE")
        print("="*70)
        
        # Test 1: Commentary text generation
        self.test_commentary_generation(num_tests=3)
        
        # Test 2: Audio generation
        self.test_audio_generation(num_tests=3)
        
        # Test 3: Full integration
        self.test_full_integration(num_tests=3)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['passed'])
        failed = total - passed
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ✓")
        print(f"Failed: {failed} ✗")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  - {result['test']}")
        
        print("\n" + "="*70)


def main():
    """Main test execution"""
    tester = IntegrationTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
