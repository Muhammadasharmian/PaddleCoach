"""
Comprehensive Test Script
Tests all three AI coaching modules together.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_coach import (
    ProComparisonModule,
    VisualDemoModule,
    LiveCoachModule,
    create_mock_shot,
    create_mock_player_profile
)


def test_module_initialization():
    """Test that all modules can be initialized."""
    print("\n" + "=" * 80)
    print("TEST 1: Module Initialization")
    print("=" * 80)
    
    # Test Module 3A
    print("\n🧪 Testing ProComparisonModule...")
    mod_a = ProComparisonModule()
    assert mod_a.initialize(), "ProComparisonModule failed to initialize"
    status = mod_a.get_status()
    print(f"✅ ProComparisonModule: {status}")
    
    # Test Module 3B
    print("\n🧪 Testing VisualDemoModule...")
    mod_b = VisualDemoModule()
    assert mod_b.initialize(), "VisualDemoModule failed to initialize"
    status = mod_b.get_status()
    print(f"✅ VisualDemoModule: {status}")
    
    # Test Module 3C
    print("\n🧪 Testing LiveCoachModule...")
    mod_c = LiveCoachModule()
    assert mod_c.initialize(), "LiveCoachModule failed to initialize"
    status = mod_c.get_status()
    print(f"✅ LiveCoachModule: {status}")
    
    print("\n✅ All modules initialized successfully!")


def test_pro_comparison():
    """Test Pro Comparison module basic functionality."""
    print("\n" + "=" * 80)
    print("TEST 2: Pro Comparison Analysis")
    print("=" * 80)
    
    module = ProComparisonModule()
    module.initialize()
    
    # Test comparison with non-existent videos (will use mock data)
    result = module.compare_techniques(
        user_video_path="test_user.mp4",
        pro_video_path="test_pro.mp4",
        shot_type="forehand"
    )
    
    assert result['status'] == 'success', "Comparison failed"
    assert 'ai_analysis' in result, "Missing AI analysis"
    assert 'recommendations' in result, "Missing recommendations"
    
    print(f"✅ Analysis generated: {len(result['ai_analysis'])} characters")
    print(f"✅ Recommendations: {len(result['recommendations'])} items")


def test_visual_demo():
    """Test Visual Demo module basic functionality."""
    print("\n" + "=" * 80)
    print("TEST 3: Visual Demo Generation")
    print("=" * 80)
    
    module = VisualDemoModule()
    module.initialize()
    
    # Test video generation
    print("\n🎬 Testing video generation...")
    video_result = module.generate_technique_video(
        technique="forehand",
        duration=5
    )
    assert video_result['status'] == 'success', "Video generation failed"
    print(f"✅ Video generated: {video_result.get('video_url', 'mock')}")
    
    # Test image generation
    print("\n🖼️ Testing image generation...")
    image_result = module.generate_stance_reference(
        stance_type="ready position",
        annotated=True
    )
    assert image_result['status'] == 'success', "Image generation failed"
    print(f"✅ Image generated: {image_result.get('image_url', 'mock')}")


def test_live_coach():
    """Test Live Coach module basic functionality."""
    print("\n" + "=" * 80)
    print("TEST 4: Live Coaching")
    print("=" * 80)
    
    module = LiveCoachModule()
    module.initialize()
    
    # Start session
    module.start_live_session("player_test", "medium")
    
    # Process multiple shots
    print("\n🎾 Processing shots...")
    for i in range(5):
        shot = create_mock_shot(f"shot_{i}", "forehand")
        shot.speed = 40.0 + i * 10  # Vary speed
        
        tip = module.process_shot(shot, "player_test")
        if tip:
            print(f"  Shot {i+1}: Received tip")
    
    # End session
    summary = module.end_live_session()
    print(f"\n✅ Session complete:")
    print(f"   Shots analyzed: {summary['total_shots_analyzed']}")
    print(f"   Tips given: {summary['total_tips_given']}")


def test_mock_data():
    """Test mock data generation."""
    print("\n" + "=" * 80)
    print("TEST 5: Mock Data Generation")
    print("=" * 80)
    
    # Test shot creation
    shot = create_mock_shot("test_001", "forehand")
    assert shot.shotID == "test_001"
    assert shot.type == "forehand"
    print("✅ Mock shot created")
    
    # Test player profile creation
    profile = create_mock_player_profile("player_test")
    assert profile.playerID == "player_test"
    assert profile.get_forehand_ratio() >= 0
    print("✅ Mock player profile created")


def test_integration():
    """Test integration between modules."""
    print("\n" + "=" * 80)
    print("TEST 6: Module Integration")
    print("=" * 80)
    
    # Create all modules
    pro_comp = ProComparisonModule()
    visual = VisualDemoModule()
    live = LiveCoachModule()
    
    # Initialize all
    assert pro_comp.initialize()
    assert visual.initialize()
    assert live.initialize()
    
    print("✅ All modules can coexist")
    
    # Use same mock data across modules
    shot = create_mock_shot("integration_test", "backhand")
    
    # Process with live coach
    tip = live.process_shot(shot, "player_integration")
    if tip:
        print(f"✅ Live coach processed shot: {len(tip)} chars")
    
    # Generate demo for the technique
    demo = visual.generate_technique_video(
        technique=shot.type,
        duration=3
    )
    assert demo['status'] == 'success'
    print(f"✅ Visual demo created for {shot.type}")


def run_all_tests():
    """Run all tests."""
    print("\n" + "🧪" * 40)
    print("COMPREHENSIVE AI COACHING SUITE TESTS")
    print("🧪" * 40)
    
    try:
        test_module_initialization()
        test_pro_comparison()
        test_visual_demo()
        test_live_coach()
        test_mock_data()
        test_integration()
        
        print("\n" + "=" * 80)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 80)
        print("\n✅ All three AI coaching modules are working correctly")
        print("✅ Mock data is functional")
        print("✅ Modules can integrate together")
        print("\n📝 Next steps:")
        print("   1. Integrate with real data models from teammates")
        print("   2. Get real API keys for full functionality")
        print("   3. Test with actual game videos")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
