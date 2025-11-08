"""
Quick test script to process the sample video with YOLOv11n pose estimation.
"""
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from vision.video_processor import VideoProcessor


def main():
    # Path to the video
    video_path = "IMG_7622.mp4"
    
    if not Path(video_path).exists():
        print(f"Error: Video file '{video_path}' not found!")
        print("Please make sure IMG_7622.mp4 is in the project root directory.")
        return
    
    print("="*60)
    print("🏓 PaddleCoach - Table Tennis Pose Analysis")
    print("   Optimized for Apple Silicon (M-series)")
    print("="*60)
    print("\nThis will:")
    print("  ✅ Track both players using YOLOv11n pose")
    print("  ✅ Detect shot events (not every frame!)")
    print("  ✅ Extract key shot moments for analysis")
    print("  ✅ Process at ~30 FPS (real-time on M1/M2/M3)")
    print("  ✅ Generate ULTRA-compact JSON for Gemini API")
    print("\nControls:")
    print("  'p' - Pause/Resume")
    print("  'q' - Quit early")
    print("  SPACE - Toggle visualization (hide for max speed)")
    print("-"*60)
    
    # Create processor with target FPS (30 for real-time)
    processor = VideoProcessor(
        video_path=video_path,
        output_dir="output",
        target_fps=30  # Process at 30 FPS for real-time performance
    )
    
    # Process video (optimized settings)
    stats = processor.process_video(
        visualize=True,      # Show real-time visualization
        save_video=False,    # Don't save video by default (faster)
        max_frames=None      # Process entire video
    )
    
    # Save pose data to JSON
    json_path = processor.save_pose_data_json()
    
    # Save optimized shot-based JSON (MUCH smaller!)
    shots_json_path = processor.save_shots_json()
    
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
    print(f"  📄 JSON Data: {json_path}")
    print(f"     (Compact format - only wrists & elbows)")
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS:")
    print("="*60)
    print("  The JSON file is ready for Gemini 2.5 Pro API!")
    print("  It contains:")
    print("    • Frame-by-frame wrist & elbow positions")
    print("    • Arm swing angles for technique analysis")
    print("    • Timestamps for shot timing")
    print("\n  Mohnish can use this for:")
    print("    🎯 Shot type classification")
    print("    🏓 Paddle swing analysis")
    print("    📈 Technique comparison with pros")
    print("    💡 Real-time coaching feedback")
    print("="*60)


if __name__ == "__main__":
    main()
