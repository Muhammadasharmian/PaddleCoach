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
    # Path to the video
    video_path = "dataDetection.mp4"
    
    if not Path(video_path).exists():
        print(f"Error: Video file '{video_path}' not found!")
        print("Please make sure dataDetection.mp4 is in the project root directory.")
        return
    
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
        output_dir="output_pose",
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
