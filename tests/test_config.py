"""
PaddleCoach - Quick Configuration Test
Author: Rakshit
Description: Quick test to verify API configuration
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.frontend.ui_services.commentary_service import CommentaryService, VOICES


def test_configuration():
    """Test if APIs are properly configured"""
    print("="*60)
    print("PADDLECOACH API CONFIGURATION TEST")
    print("="*60)
    
    # Load environment
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    print("\n1. Environment Variables:")
    print(f"   GEMINI_API_KEY: {'✓ Found' if gemini_key else '✗ Not found'}")
    print(f"   ELEVENLABS_API_KEY: {'✓ Found' if elevenlabs_key else '✗ Not found'}")
    
    # Initialize service
    print("\n2. Initializing Commentary Service...")
    service = CommentaryService(env_path=env_path)
    
    print(f"   Gemini Configured: {'✓ Yes' if service.gemini_configured else '✗ No'}")
    print(f"   ElevenLabs Configured: {'✓ Yes' if service.elevenlabs_client else '✗ No'}")
    
    # Test text generation
    print("\n3. Testing Commentary Text Generation...")
    test_event = {
        'player_name': 'Test Player',
        'event_type': 'point',
        'context': 'with an amazing shot',
        'score': {'player1': 5, 'player2': 3}
    }
    
    text = service.generate_commentary_text(test_event)
    print(f"   Generated: {text}")
    print(f"   Status: {'✓ Success' if text else '✗ Failed'}")
    
    # Test audio generation
    if service.elevenlabs_client:
        print("\n4. Testing Audio Generation...")
        output_path = "tests/config_test_audio.mp3"
        audio = service.generate_audio("This is a test.", output_path=output_path)
        
        if audio and os.path.exists(output_path):
            print(f"   Audio File: ✓ Created at {output_path}")
        else:
            print(f"   Audio File: ✗ Failed to create")
    
    print("\n" + "="*60)
    print("CONFIGURATION TEST COMPLETE")
    print("="*60)
    
    # Status summary
    if service.gemini_configured and service.elevenlabs_client:
        print("\n✓ All systems operational!")
        print("  Run 'python tests/test_integration.py' for full tests")
    else:
        print("\n⚠ Some services not configured")
        print("  Check your .env file in the tests directory")


if __name__ == "__main__":
    test_configuration()
