"""
Run game analysis on processed video output.
This script analyzes the annotated video from process_video.py and generates a detailed report.
"""
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from vision.game_analyzer import GameAnalyzer


def main():
    """Main function to run game analysis."""
    
    # Get video path from argument or find any mp4 in output/processVideo/
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Find any .mp4 file in output/processVideo/ directory
        output_dir = Path("output/processVideo")
        if not output_dir.exists():
            print(f"Error: Directory 'output/processVideo/' not found!")
            print("\nPlease run process_video.py first to generate the annotated video.")
            return
        
        mp4_files = list(output_dir.glob("*.mp4"))
        if not mp4_files:
            print(f"Error: No .mp4 files found in 'output/processVideo/' directory!")
            print("\nPlease run process_video.py first to generate the annotated video.")
            return
        
        # Use the first mp4 file found
        video_path = str(mp4_files[0])
        print(f"Found video: {video_path}")
    
    # Check if video exists
    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        print("\nPlease check the file path and try again.")
        print("Or specify a different video path as argument:")
        print(f"  python analyze_processed_video.py <video_path>")
        return
    
    # FPS and velocity threshold (can be adjusted based on video)
    fps = 30  # Adjust if your video has different FPS
    velocity_threshold = 1000.0  # Minimum velocity to detect a shot
    
    print("\n" + "="*60)
    print("  🏓 PaddleCoach - Game Analysis System")
    print("="*60)
    print(f"\nInput Video: {video_path}")
    print(f"Processing FPS: {fps}")
    print(f"Shot Detection Threshold: {velocity_threshold} px/s")
    print("\nThis analysis will:")
    print("  ✅ Extract pose data from the annotated video")
    print("  ✅ Detect shots for both players")
    print("  ✅ Calculate biomechanical metrics")
    print("  ✅ Compare player performance")
    print("  ✅ Generate a detailed .txt report")
    print("-"*60)
    
    # Create analyzer
    analyzer = GameAnalyzer(output_dir="output/analysisText")
    
    # Generate analysis report
    report_path = analyzer.generate_analysis_report(
        video_path=video_path,
        velocity_threshold=velocity_threshold,
        fps=fps
    )
    
    if report_path:
        print("\n" + "="*60)
        print("  ✅ ANALYSIS COMPLETE!")
        print("="*60)
        print(f"\n📄 Report saved to: {report_path}")
        print("\nThe report includes:")
        print("  • Shot detection summary")
        print("  • Forehand/Backhand classification")
        print("  • Biomechanical metrics per shot")
        print("  • Player comparison (if 2 players detected)")
        print("  • Performance recommendations")
        print("\n" + "="*60)
    else:
        print("\n" + "="*60)
        print("  ❌ ANALYSIS FAILED")
        print("="*60)
        print("\nPlease check:")
        print("  • Video file exists and is readable")
        print("  • Video contains pose detection data")
        print("  • YOLO model (yolo11n-pose.pt) is available")
        print("="*60)


if __name__ == "__main__":
    main()
