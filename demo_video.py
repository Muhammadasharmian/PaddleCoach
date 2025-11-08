"""
Demo script for PaddleCoach Vision System
Displays pose detection results from pre-processed video.
"""
import cv2
import time
from pathlib import Path


def play_demo_video(input_video: str = "dataDetection.mp4", 
                    output_video: str = "output/output_dataPose.mp4"):
    """
    Play the processed pose detection video.
    
    Args:
        input_video: Path to input video (for reference)
        output_video: Path to processed output video
    """
    input_path = Path(input_video)
    output_path = Path(output_video)
    
    # Check if files exist
    if not input_path.exists():
        print(f"❌ Input video not found: {input_video}")
        print("Please ensure dataDetection.mp4 is in the project directory.")
        return
    
    if not output_path.exists():
        print(f"❌ Processed video not found: {output_video}")
        print("Please ensure output/output_dataPose.mp4 exists.")
        return
    
    # Open the processed video
    cap = cv2.VideoCapture(str(output_path))
    
    if not cap.isOpened():
        print(f"❌ Error opening video file: {output_video}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print("="*70)
    print("🏓 PaddleCoach - Vision System Demo")
    print("="*70)
    print(f"\n📹 Video Information:")
    print(f"   Input: {input_video}")
    print(f"   Output: {output_video}")
    print(f"   Resolution: {width}x{height}")
    print(f"   FPS: {fps}")
    print(f"   Duration: {duration:.2f}s ({total_frames} frames)")
    print("\n🎬 Features Demonstrated:")
    print("   ✅ Player pose detection (YOLOv11 pose estimation)")
    print("   ✅ Keypoint tracking (wrists, elbows, shoulders)")
    print("   ✅ Real-time skeleton visualization")
    print("   ✅ Frame-by-frame analysis")
    print("\n⌨️  Controls:")
    print("   SPACE - Pause/Resume")
    print("   Q - Quit")
    print("="*70)
    print("\n▶️  Playing processed video...\n")
    
    frame_count = 0
    start_time = time.time()
    paused = False
    
    # Calculate frame delay for real-time playback
    frame_delay = int(1000 / fps) if fps > 0 else 33  # milliseconds
    
    while True:
        if not paused:
            ret, frame = cap.read()
            
            if not ret:
                print("\n✅ Playback complete!")
                break
            
            frame_count += 1
            
            # Display progress
            if frame_count % 30 == 0:
                elapsed = time.time() - start_time
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% | Frame: {frame_count}/{total_frames} | "
                      f"Elapsed: {elapsed:.1f}s", end='\r')
        
        # Show frame
        cv2.imshow('PaddleCoach - Pose Detection Demo', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(frame_delay if not paused else 1) & 0xFF
        
        if key == ord('q') or key == 27:  # 'q' or ESC
            print("\n\n⏹️  Playback stopped by user.")
            break
        elif key == ord(' '):  # SPACE
            paused = not paused
            status = "PAUSED" if paused else "RESUMED"
            print(f"\n⏸️  {status}")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    # Final stats
    total_time = time.time() - start_time
    print("\n" + "="*70)
    print("📊 Playback Statistics")
    print("="*70)
    print(f"Frames displayed: {frame_count}/{total_frames}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Playback FPS: {frame_count/total_time:.1f}" if total_time > 0 else "N/A")
    print("="*70)


if __name__ == "__main__":
    play_demo_video()
