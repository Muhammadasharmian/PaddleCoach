"""
Example Usage: Pro Comparison Module (Module 3A)

This script demonstrates how to use the Pro Comparison module
to analyze the difference between user and professional technique.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_coach import ProComparisonModule


def main():
    """Example usage of Pro Comparison Module."""
    
    print("=" * 80)
    print("PRO COMPARISON MODULE - EXAMPLE USAGE")
    print("=" * 80)
    
    # Initialize the module
    print("\n1️⃣ Initializing Pro Comparison Module...")
    module = ProComparisonModule(
        gemini_api_key=None  # Will use mock mode without API key
    )
    
    if not module.initialize():
        print("❌ Failed to initialize module")
        return
    
    print("✅ Module initialized successfully")
    print(f"Status: {module.get_status()}")
    
    # Example 1: Compare techniques
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Compare Forehand Technique")
    print("=" * 80)
    
    result = module.compare_techniques(
        user_video_path="./videos/user_forehand.mp4",  # These don't exist - will use mock data
        pro_video_path="./videos/pro_forehand.mp4",
        shot_type="forehand topspin",
        output_report="./output/forehand_analysis.txt"
    )
    
    if result['status'] == 'success':
        print("\n📊 ANALYSIS RESULTS:")
        print("-" * 80)
        print(result['ai_analysis'])
        print("\n" + "-" * 80)
        print("🎯 TOP 3 RECOMMENDATIONS:")
        for i, rec in enumerate(result['recommendations'][:3], 1):
            print(f"\n{i}. [{rec['priority'].upper()}] {rec['joint']}")
            print(f"   Difference: {rec['difference']:+.1f}° from pro")
            print(f"   Your angle: {rec['user_angle']:.1f}° | Pro angle: {rec['pro_angle']:.1f}°")
    
    # Example 2: Compare backhand
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Compare Backhand Technique")
    print("=" * 80)
    
    result = module.compare_techniques(
        user_video_path="./videos/user_backhand.mp4",
        pro_video_path="./videos/pro_backhand.mp4",
        shot_type="backhand",
        output_report="./output/backhand_analysis.txt"
    )
    
    if result['status'] == 'success':
        print("\n✅ Backhand analysis complete!")
        print(f"📄 Report saved to: ./output/backhand_analysis.txt")
        print(f"🎯 Found {len(result['recommendations'])} areas for improvement")
    
    print("\n" + "=" * 80)
    print("✅ Examples complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
