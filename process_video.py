"""
Quick test script to process the sample video with YOLOv11n pose estima        print("\n    
    print("\n" + "="*60)
    print("📁 OUTPUT FILES:")
    print("="*60)
    print(f"  📹 Annotated Video: output_pose/{video_path.replace('.mp4', '_annotated.mp4')}")
    print(f"     (Full body pose detection visualization)")
    
    print("\n" + "="*60)60)
    print("📁 OUTPUT FILES:")
    print("="*60)
    print(f"  📹 Annotated Video: output_pose/{video_path.replace('.mp4', '_annotated.mp4')}")
    print(f"     (Full body pose detection visualization)")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    print("  The annotated video shows:")
    print("    • Real-time full body pose detection on both players")
    print("    • Complete skeletal keypoint tracking (17 points)")
    print("    • Body movement visualization")
    print("\n  Ready for analysis with analyze_processed_video.py!")
    print("="*60)"*60)
    print("📁 OUTPUT FILES:")
    print("="*60)
    print(f"  📹 Annotated Video: output_pose/output_{video_path}")
    print(f"     (Pose detection visualization)")
"""
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from vision.video_processor import VideoProcessor


def main():
    # Find video in input_processVideo directory
    input_dir = Path("input_processVideo")
    
    if not input_dir.exists():
        print(f"Error: Directory 'input_processVideo/' not found!")
        print("Please create the directory and add a video file.")
        return
    
    # Look for video files (mp4, avi, mov, etc.)
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.MP4', '*.AVI', '*.MOV']
    video_files = []
    for ext in video_extensions:
        video_files.extend(list(input_dir.glob(ext)))
    
    if not video_files:
        print(f"Error: No video files found in 'input_processVideo/' directory!")
        print("Supported formats: .mp4, .avi, .mov, .mkv")
        return
    
    # Use the first video found
    video_path = str(video_files[0])
    print(f"Found video: {video_path}")
    
    if len(video_files) > 1:
        print(f"Note: Multiple videos found. Using {video_files[0].name}")
        print(f"Other videos: {[v.name for v in video_files[1:]]}")
    
    print("="*60)
    print("🏓 PaddleCoach - Table Tennis Pose Analysis")
    print("   Optimized for Apple Silicon (M-series)")
    print("="*60)
    print("\nThis will:")
    print("  ✅ Track both players using YOLOv11n pose")
    print("  ✅ Full body pose detection (17 keypoints)")
    print("  ✅ Detect shot events and movements")
    print("  ✅ Extract key shot moments for analysis")
    print("  ✅ Process at ~30 FPS (real-time on M1/M2/M3)")
    print("\nControls:")
    print("  'p' - Pause/Resume")
    print("  'q' - Quit early")
    print("  SPACE - Toggle visualization (hide for max speed)")
    print("-"*60)
    
    # Create processor with target FPS (30 for real-time)
    processor = VideoProcessor(
        video_path=video_path,
        output_dir="output_processVideo",
        target_fps=30  # Process at 30 FPS for real-time performance
    )
    
    # Process video (optimized settings)
    stats = processor.process_video(
        visualize=True,      # Show real-time visualization
        save_video=True,     # Save annotated video
        max_frames=None      # Process entire video
    )
    
    # Print summary statistics
    summary = processor.get_summary_statistics()
    
    print("\n" + "="*60)
    print("✅ PROCESSING COMPLETE!")
    print("="*60)
    
    print("\n📊 Performance:")
    print(f"  Frames processed: {stats['processed_frames']}")
    print(f"  Processing time: {stats['processing_time']:.1f}s")
    print(f"  Average FPS: {stats['processing_fps']:.1f}")
    print(f"  Video duration: {stats['duration']:.2f}s")
    
    print("\n🎾 Detection Statistics:")
    for player, player_stats in summary.items():
        print(f"\n  {player.upper()}:")
        print(f"    Total frames: {player_stats.get('total_frames', 0)}")
        print(f"    Left wrist: {player_stats.get('left_wrist_rate', 0):.1%} detection")
        print(f"    Right wrist: {player_stats.get('right_wrist_rate', 0):.1%} detection")
        if player_stats.get('avg_left_arm_angle'):
            print(f"    Avg left arm angle: {player_stats['avg_left_arm_angle']:.1f}°")
        if player_stats.get('avg_right_arm_angle'):
            print(f"    Avg right arm angle: {player_stats['avg_right_arm_angle']:.1f}°")
    
    print("\n" + "="*60)
    print("📁 OUTPUT FILES:")
    print("="*60)
    print(f"  � Annotated Video: output/output_{video_path}")
    print(f"     (Pose detection visualization)")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    print("  The annotated video shows:")
    print("    • Real-time pose detection on both players")
    print("    • Skeletal keypoint tracking")
    print("    • Arm swing visualization")
    print("\n  Ready for analysis with analyze_game.py!")
    print("="*60)


if __name__ == "__main__":
    main()
