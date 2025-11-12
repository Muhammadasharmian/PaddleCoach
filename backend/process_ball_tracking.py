"""
Real-time ball tracking for table tennis using camera.
Tracks the ball using YOLOv11n model through live camera feed.
Outputs: Real-time visualization + recorded video (no JSON output).
"""
from pathlib import Path
import sys
import cv2
from typing import List, Dict, Optional
import time
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from vision.ball_tracker import BallTracker
from models.ball_data import BallData


class RealtimeBallTracker:
    """Real-time ball tracking using camera feed."""
    
    def __init__(self, camera_id: int = 0, output_dir: str = "output/ballTracking"):
        """
        Initialize real-time ball tracker.
        
        Args:
            camera_id: Camera device ID (0 for default camera)
            output_dir: Directory for output files (default: output/ballTracking)
        """
        self.camera_id = camera_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize ball tracker with YOLOv11n
        # Use absolute path to model file
        script_dir = Path(__file__).parent.absolute()
        model_path = script_dir / "yolov11n.pt"
        
        print(f"Script directory: {script_dir}")
        print(f"Looking for model at: {model_path}")
        print(f"Model exists: {model_path.exists()}")
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {model_path}\n"
                f"Please ensure yolov11n.pt is in {script_dir}"
            )
        
        self.tracker = BallTracker(model_path=str(model_path), max_trajectory=50)
        
        # Storage for ball data
        self.ball_detections: List[BallData] = []
        
        # Session info
        self.session_start = None
        
    def start_tracking(self, save_video: bool = False) -> Dict:
        """
        Start real-time ball tracking from camera.
        
        Args:
            save_video: Save recorded session to video file
            
        Returns:
            Dictionary with session statistics
        """
        # Open camera
        cap = cv2.VideoCapture(self.camera_id)
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.camera_id}")
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default to 30 if not available
        
        print("\n" + "="*60)
        print("🏓 Real-Time Ball Tracking Started")
        print("="*60)
        print(f"Camera ID: {self.camera_id}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Model: YOLOv11n (sports ball detection)")
        print("-"*60)
        print("\nControls:")
        print("  'q' - Quit and save session")
        print("  'p' - Pause/Resume tracking")
        print("  'r' - Reset trajectory")
        print("-"*60)
        
        # Video writer for recorded session
        writer = None
        if save_video:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video_path = self.output_dir / f"camera_session_{timestamp_str}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))
            print(f"📹 Recording to: {output_video_path}")
        
        # Session stats
        frame_count = 0
        detections_count = 0
        start_time = time.time()
        self.session_start = datetime.now()
        paused = False
        
        print("\n🎥 Camera feed active - tracking started!")
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    print("\n⚠️ Failed to read from camera")
                    break
                
                # Calculate timestamp
                timestamp = time.time() - start_time
                
                # Process frame for ball detection
                ball_data = self.tracker.process_frame(frame, frame_count, timestamp)
                
                if ball_data is not None:
                    self.ball_detections.append(ball_data)
                    detections_count += 1
                
                # Visualize with ball tracking
                annotated_frame = self.tracker.visualize_ball(frame, ball_data)
                
                # Add info overlay
                self._add_realtime_overlay(annotated_frame, frame_count, 
                                           detections_count, start_time, ball_data)
                
                # Save to video if recording
                if writer is not None:
                    writer.write(annotated_frame)
                
                # Show live feed
                cv2.imshow('Real-Time Ball Tracking', annotated_frame)
                
                frame_count += 1
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\n\n🛑 Stopping tracking session...")
                break
            elif key == ord('p'):
                paused = not paused
                status = "⏸️  PAUSED" if paused else "▶️  RESUMED"
                print(f"\n{status}")
            elif key == ord('r'):
                self.ball_detections.clear()
                self.tracker.reset_trajectory()
                detections_count = 0
                print("\n� Trajectory reset")
        
        # Cleanup
        cap.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()
        
        # Calculate statistics
        elapsed_time = time.time() - start_time
        processing_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        detection_rate = (detections_count / frame_count * 100) if frame_count > 0 else 0
        
        stats = {
            'total_frames': frame_count,
            'detections': detections_count,
            'detection_rate': detection_rate,
            'session_duration': elapsed_time,
            'processing_fps': processing_fps,
            'camera_fps': fps,
            'resolution': f"{width}x{height}",
            'session_start': self.session_start.strftime("%Y-%m-%d %H:%M:%S") if self.session_start else None
        }
        
        print("\n\n" + "="*60)
        print("✅ Tracking Session Complete!")
        print("="*60)
        
        return stats
    
    def _add_realtime_overlay(self, frame, frame_num, detections, start_time, ball_data):
        """Add real-time information overlay to frame."""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay at top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 140), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Session duration
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        cv2.putText(frame, f"Session Time: {minutes:02d}:{seconds:02d}", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Frame count
        cv2.putText(frame, f"Frames: {frame_num}", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Detection status
        status = "🎾 BALL DETECTED" if ball_data is not None else "⚪ NO BALL"
        color = (0, 255, 0) if ball_data is not None else (0, 165, 255)
        cv2.putText(frame, status, (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Detection count
        detection_rate = (detections / frame_num * 100) if frame_num > 0 else 0
        cv2.putText(frame, f"Detections: {detections} ({detection_rate:.1f}%)", (10, 115),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Ball info if detected
        if ball_data is not None:
            info_text = f"Pos: ({ball_data.x:.0f}, {ball_data.y:.0f})"
            if ball_data.speed is not None:
                info_text += f" | Speed: {ball_data.speed:.0f} px/s"
            info_text += f" | Conf: {ball_data.confidence:.2f}"
            cv2.putText(frame, info_text, (w - 550, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    
    def get_statistics(self) -> Dict:
        """Get detailed statistics about ball tracking."""
        if not self.ball_detections:
            return {}
        
        # Calculate statistics
        confidences = [b.confidence for b in self.ball_detections]
        speeds = [b.speed for b in self.ball_detections if b.speed is not None]
        
        stats = {
            "total_detections": len(self.ball_detections),
            "confidence": {
                "mean": sum(confidences) / len(confidences),
                "min": min(confidences),
                "max": max(confidences)
            }
        }
        
        if speeds:
            stats["speed"] = {
                "mean": sum(speeds) / len(speeds),
                "min": min(speeds),
                "max": max(speeds)
            }
        
        return stats


def main():
    """Main execution function for real-time ball tracking."""
    # Configuration
    camera_id = 0  # Default camera
    output_dir = "output_ballTracking"
    save_recording = False  # Set to True to save video recording
    
    print("="*60)
    print("🏓 PaddleCoach - Real-Time Ball Tracking")
    print("   Using Camera Feed + YOLOv11n")
    print("="*60)
    print("\nThis will:")
    print("  ✅ Open your camera for live ball tracking")
    print("  ✅ Track sports ball in real-time using YOLOv11n")
    print("  ✅ Display ball trajectory and speed")
    print("  ✅ Optional: Record session to video (no JSON output)")
    print("\nControls:")
    print("  'q' - Quit and save session")
    print("  'p' - Pause/Resume tracking")
    print("  'r' - Reset trajectory")
    print("-"*60)
    
    try:
        # Create real-time tracker
        tracker = RealtimeBallTracker(camera_id=camera_id, output_dir=output_dir)
        
        # Start tracking session
        stats = tracker.start_tracking(save_video=save_recording)
        
        # Get detailed statistics
        detailed_stats = tracker.get_statistics()
        
        # Print session summary
        print("\n" + "="*60)
        print("📊 Session Summary")
        print("="*60)
        print(f"Session duration: {stats['session_duration']:.1f}s")
        print(f"Total frames: {stats['total_frames']}")
        print(f"Ball detections: {stats['detections']}")
        print(f"Detection rate: {stats['detection_rate']:.1f}%")
        print(f"Processing FPS: {stats['processing_fps']:.1f}")
        
        if detailed_stats:
            print("\n" + "="*60)
            print("🎾 Ball Tracking Statistics")
            print("="*60)
            print(f"Total detections: {detailed_stats['total_detections']}")
            print(f"Avg confidence: {detailed_stats['confidence']['mean']:.2f}")
            print(f"Min confidence: {detailed_stats['confidence']['min']:.2f}")
            print(f"Max confidence: {detailed_stats['confidence']['max']:.2f}")
            
            if 'speed' in detailed_stats:
                print(f"\nSpeed Statistics:")
                print(f"  Avg speed: {detailed_stats['speed']['mean']:.1f} px/s")
                print(f"  Min speed: {detailed_stats['speed']['min']:.1f} px/s")
                print(f"  Max speed: {detailed_stats['speed']['max']:.1f} px/s")
        
        print("\n" + "="*60)
        print("📁 Session Files")
        print("="*60)
        if save_recording:
            print(f"� Video recording: output_ballTracking/camera_session_*.mp4")
        else:
            print("No files saved (video recording was disabled)")
        
        print("\n" + "="*60)
        print("🚀 Next Steps")
        print("="*60)
        print("The tracking session can be used for:")
        print("  🎯 Shot analysis and classification")
        print("  📊 Rally pattern recognition")
        print("  🏓 Ball trajectory analysis")
        print("  💡 Integration with pose tracking for complete match analysis")
        print("  📹 Enable save_recording=True to save video output")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during tracking: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
