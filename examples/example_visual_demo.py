"""
Example Usage: Visual Demo Module (Module 3B)

This script demonstrates how to use the Visual Demo module
to generate demonstration videos and images.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_coach import VisualDemoModule


def main():
    """Example usage of Visual Demo Module."""
    
    print("=" * 80)
    print("VISUAL DEMO MODULE - EXAMPLE USAGE")
    print("=" * 80)
    
    # Initialize the module
    print("\n1️⃣ Initializing Visual Demo Module...")
    module = VisualDemoModule(
        veo_api_key=None,  # Will use mock mode
        nano_banana_api_key=None,
        gemini_api_key=None
    )
    
    if not module.initialize():
        print("❌ Failed to initialize module")
        return
    
    print("✅ Module initialized successfully")
    print(f"Status: {module.get_status()}")
    
    # Example 1: Generate technique video
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Generate Forehand Topspin Video")
    print("=" * 80)
    
    result = module.generate_technique_video(
        technique="forehand topspin",
        focus_areas=["hip rotation", "wrist snap", "follow-through"],
        duration=6,
        output_path="./output/forehand_demo.mp4"
    )
    
    if result['status'] == 'success':
        print("\n✅ Video generated!")
        print(f"📹 Video URL: {result['video_url']}")
        if 'local_path' in result:
            print(f"💾 Saved locally: {result['local_path']}")
    
    # Example 2: Generate stance reference image
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Generate Ready Position Reference")
    print("=" * 80)
    
    result = module.generate_stance_reference(
        stance_type="ready position",
        annotated=True,
        output_path="./output/ready_stance.png"
    )
    
    if result['status'] == 'success':
        print("\n✅ Image generated!")
        print(f"🖼️  Annotations: Body angles and positioning marked")
    
    # Example 3: Generate technique sequence
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Generate 4-Frame Backhand Sequence")
    print("=" * 80)
    
    result = module.generate_technique_sequence(
        technique="backhand block",
        num_frames=4,
        output_dir="./output/backhand_sequence"
    )
    
    if result['status'] == 'success':
        print(f"\n✅ Generated {result['successful_frames']} frames!")
        print("Sequence phases:")
        for frame in result['frames']:
            print(f"  • Frame {frame['frame_number']}: {frame['phase']}")
    
    # Example 4: Generate correction video
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Generate Technique Correction Video")
    print("=" * 80)
    
    result = module.generate_correction_video(
        current_issue="Player is hitting with arm only, no hip rotation",
        correction="Proper forehand uses full body rotation starting from legs",
        output_path="./output/correction_demo.mp4"
    )
    
    if result['status'] == 'success':
        print("\n✅ Correction video generated!")
    
    # Example 5: Create complete training package
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Create Complete Training Package")
    print("=" * 80)
    
    result = module.create_training_package(
        technique="serve",
        output_dir="./output/serve_training_package"
    )
    
    print(f"\n✅ Training package created with {len(result['items'])} items:")
    for item in result['items']:
        print(f"  • {item['type']}: {item['name']}")
    
    # Example 6: Custom user prompt
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Custom User Prompt")
    print("=" * 80)
    
    result = module.generate_custom_demo(
        user_prompt="Show me how to return a fast serve with a backhand block",
        media_type="video",
        output_path="./output/custom_demo.mp4"
    )
    
    if result['status'] == 'success':
        print("\n✅ Custom demo generated!")
    
    print("\n" + "=" * 80)
    print("✅ Examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
