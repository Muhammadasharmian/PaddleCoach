"""
Example Usage: Live Coach Module (Module 3C)

This script demonstrates how to use the Live Coach module
to provide real-time coaching feedback during a match.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_coach import LiveCoachModule, create_mock_shot


def coaching_callback(tip: str):
    """Callback function to receive coaching tips."""
    print(f"\n🎓 COACH: {tip}")


def simulate_match():
    """Simulate a series of shots during a match."""
    
    # Simulated shot sequence
    shots = [
        create_mock_shot("shot_001", "serve"),
        create_mock_shot("shot_002", "forehand"),
        create_mock_shot("shot_003", "forehand"),
        create_mock_shot("shot_004", "backhand"),
        create_mock_shot("shot_005", "forehand"),
        create_mock_shot("shot_006", "forehand"),
        create_mock_shot("shot_007", "backhand"),
        create_mock_shot("shot_008", "smash"),
    ]
    
    # Vary shot characteristics
    shots[0].speed = 35.0  # Slow serve
    shots[1].speed = 55.0
    shots[2].speed = 58.0
    shots[3].speed = 45.0
    shots[4].speed = 60.0
    shots[5].speed = 62.0  # Getting faster
    shots[6].speed = 50.0
    shots[7].speed = 85.0  # Fast smash
    
    return shots


def main():
    """Example usage of Live Coach Module."""
    
    print("=" * 80)
    print("LIVE COACH MODULE - EXAMPLE USAGE")
    print("=" * 80)
    
    # Initialize the module
    print("\n1️⃣ Initializing Live Coach Module...")
    module = LiveCoachModule(
        gemini_api_key=None,  # Will use mock mode
        knowledge_base_path="../prompts/rag_knowledge_base.json"
    )
    
    if not module.initialize():
        print("❌ Failed to initialize module")
        return
    
    print("✅ Module initialized successfully")
    status = module.get_status()
    print(f"📚 Knowledge base entries: {status['knowledge_base_entries']}")
    
    # Register callback for real-time tips
    print("\n2️⃣ Registering coaching callback...")
    module.register_callback(coaching_callback)
    
    # Example 1: Basic live coaching
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Live Coaching During Match")
    print("=" * 80)
    
    module.start_live_session(
        player_id="player_001",
        feedback_frequency="medium"
    )
    
    # Simulate shots
    shots = simulate_match()
    
    for i, shot in enumerate(shots, 1):
        print(f"\n--- Shot {i} ---")
        print(f"Type: {shot.type}, Speed: {shot.speed:.1f} km/h")
        
        # Process shot (might generate coaching tip)
        tip = module.process_shot(
            shot=shot,
            player_id="player_001",
            game_context={
                'score': f"{i}-{i-1}",
                'rally_length': i % 4 + 1
            }
        )
        
        # Small delay to simulate real-time
        time.sleep(0.5)
    
    # End session
    summary = module.end_live_session()
    
    print("\n" + "=" * 80)
    print("SESSION SUMMARY")
    print("=" * 80)
    print(f"Total shots analyzed: {summary['total_shots_analyzed']}")
    print(f"Total tips given: {summary['total_tips_given']}")
    
    if summary['tips']:
        print("\n📝 All tips given during session:")
        for i, tip in enumerate(summary['tips'], 1):
            print(f"{i}. {tip}")
    
    # Example 2: Get tip summary
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Get Coaching Summary for Player")
    print("=" * 80)
    
    tip_summary = module.get_tip_summary("player_001")
    
    print(f"\nPlayer: {tip_summary['player_id']}")
    print(f"Tips received: {tip_summary['total_tips']}")
    print("\n📊 Tip categories:")
    for category, count in tip_summary['categories'].items():
        if count > 0:
            print(f"  • {category.capitalize()}: {count}")
    
    # Example 3: Process specific shot scenarios
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Specific Shot Scenarios")
    print("=" * 80)
    
    # Scenario 1: Very slow shot
    print("\n🔍 Scenario 1: Player hitting too slow")
    slow_shot = create_mock_shot("shot_slow", "forehand")
    slow_shot.speed = 25.0
    
    tip = module.process_shot(
        shot=slow_shot,
        player_id="player_001"
    )
    if tip:
        print(f"💡 Tip: {tip}")
    
    # Scenario 2: Very fast shot
    print("\n🔍 Scenario 2: Player hitting too fast")
    fast_shot = create_mock_shot("shot_fast", "smash")
    fast_shot.speed = 95.0
    
    tip = module.process_shot(
        shot=fast_shot,
        player_id="player_001"
    )
    if tip:
        print(f"💡 Tip: {tip}")
    
    print("\n" + "=" * 80)
    print("✅ Examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
