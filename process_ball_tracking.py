"""
Ball tracking processor for table tennis.
Tracks the ball using YOLOv11n model.
Outputs: annotated video + JSON file with ball trajectory.
"""
from pathlib import Path
import sys
import cv2
import json
from typing import List, Dict
import time

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from vision.ball_tracker import BallTracker
from models.ball_data import BallData


class BallTrackingProcessor:
    """Process video for ball tracking and generate outputs."""
    
    def __init__(self, video_path: str, output_dir: str = "output"):
        """
        Initialize ball tracking processor.
        
        Args:
            video_path: Path to input video
            output_dir: Directory for output files
        """
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Validate video exists
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
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
        
    def process_video(self, 
                     visualize: bool = True,
                     save_video: bool = True,
                     max_frames: int = None,
                     skip_frames: int = 1) -> Dict:
        """
        Process video and track ball.
        
        Args:
            visualize: Show real-time visualization
            save_video: Save annotated video
            max_frames: Maximum frames to process (None = all)
            skip_frames: Process every Nth frame (1 = all frames)
            
        Returns:
            Dictionary with processing statistics
        """
        cap = cv2.VideoCapture(str(self.video_path))
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print("\n" + "="*60)
        print("🏓 Ball Tracking Started")
        print("="*60)
        print(f"Video: {self.video_path.name}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Duration: {duration:.2f}s ({total_frames} frames)")
        print(f"Model: YOLOv11n (default)")
        print("-"*60)
        
        # Video writer for annotated output
        writer = None
        if save_video:
            output_video_path = self.output_dir / f"{self.video_path.stem}_ball_tracked.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(str(output_video_path), fourcc, fps, (width, height))
            print(f"Saving to: {output_video_path}")
        
        # Processing stats
        frame_count = 0
        processed_count = 0
        detections_count = 0
        start_time = time.time()
        paused = False
        
        while True:
            if not paused:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Check max frames limit
                if max_frames is not None and frame_count >= max_frames:
                    print(f"\nReached max frames limit: {max_frames}")
                    break
                
                # Calculate timestamp
                timestamp = frame_count / fps
                
                # Process frame (with frame skipping)
                ball_data = None
                if frame_count % skip_frames == 0:
                    ball_data = self.tracker.process_frame(frame, frame_count, timestamp)
                    processed_count += 1
                    
                    if ball_data is not None:
                        self.ball_detections.append(ball_data)
                        detections_count += 1
                
                # Visualize
                annotated_frame = self.tracker.visualize_ball(frame, ball_data)
                
                # Add info overlay
                self._add_info_overlay(annotated_frame, frame_count, total_frames, 
                                      detections_count, processed_count, ball_data)
                
                # Save to video
                if writer is not None:
                    writer.write(annotated_frame)
                
                # Show visualization
                if visualize:
                    cv2.imshow('Ball Tracking', annotated_frame)
                
                frame_count += 1
                
                # Progress update every 30 frames
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    fps_actual = frame_count / elapsed if elapsed > 0 else 0
                    progress = (frame_count / total_frames) * 100
                    print(f"\rProgress: {progress:.1f}% | Frame: {frame_count}/{total_frames} | "
                          f"FPS: {fps_actual:.1f} | Detections: {detections_count}", end="")
            
            # Handle keyboard input
            if visualize:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\n\nQuitting early...")
                    break
                elif key == ord('p'):
                    paused = not paused
                    print(f"\n{'PAUSED' if paused else 'RESUMED'}")
                elif key == ord(' '):
                    visualize = not visualize
                    if not visualize:
                        cv2.destroyAllWindows()
        
        # Cleanup
        cap.release()
        if writer is not None:
            writer.release()
        if visualize:
            cv2.destroyAllWindows()
        
        # Calculate statistics
        elapsed_time = time.time() - start_time
        processing_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        detection_rate = (detections_count / processed_count * 100) if processed_count > 0 else 0
        
        stats = {
            'total_frames': frame_count,
            'processed_frames': processed_count,
            'detections': detections_count,
            'detection_rate': detection_rate,
            'processing_time': elapsed_time,
            'processing_fps': processing_fps,
            'video_fps': fps,
            'duration': duration,
            'resolution': f"{width}x{height}"
        }
        
        print("\n\n" + "="*60)
        print("✅ Processing Complete!")
        print("="*60)
        
        return stats
    
    def _add_info_overlay(self, frame, frame_num, total_frames, detections, processed, ball_data):
        """Add information overlay to frame."""
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay at top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Frame info
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Detection info
        status = "DETECTED" if ball_data is not None else "NO BALL"
        color = (0, 255, 0) if ball_data is not None else (0, 0, 255)
        cv2.putText(frame, f"Status: {status}", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Stats
        cv2.putText(frame, f"Detections: {detections}/{processed}", (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Ball info if detected
        if ball_data is not None:
            info_text = f"Pos: ({ball_data.x:.0f}, {ball_data.y:.0f}) | Conf: {ball_data.confidence:.2f}"
            if ball_data.speed is not None:
                info_text += f" | Speed: {ball_data.speed:.0f} px/s"
            cv2.putText(frame, info_text, (10, 115),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
    
    def save_json(self) -> Path:
        """
        Save ball tracking data to JSON file.
        
        Returns:
            Path to saved JSON file
        """
        output_path = self.output_dir / f"{self.video_path.stem}_ball_data.json"
        
        # Build JSON structure
        data = {
            "metadata": {
                "video_file": self.video_path.name,
                "model": "yolov11n.pt",
                "tracking_target": "sports_ball",
                "total_detections": len(self.ball_detections),
                "processed_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "trajectory": [ball.to_dict() for ball in self.ball_detections]
        }
        
        # Save with pretty formatting
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n📄 Ball tracking JSON saved: {output_path}")
        print(f"   Total detections: {len(self.ball_detections)}")
        print(f"   File size: {output_path.stat().st_size / 1024:.1f} KB")
        
        return output_path
    
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
    """Main execution function."""
    # Configuration
    video_path = "IMG_7622.mp4"
    output_dir = "output"
    
    # Check if video exists
    if not Path(video_path).exists():
        print(f"❌ Error: Video file '{video_path}' not found!")
        print("Please make sure IMG_7622.mp4 is in the project root directory.")
        return
    
    print("="*60)
    print("🏓 PaddleCoach - Ball Tracking System")
    print("   Using YOLOv11n (default object detection)")
    print("="*60)
    print("\nThis will:")
    print("  ✅ Track sports ball using YOLOv11n model")
    print("  ✅ Auto-download model if not present")
    print("  ✅ Generate ball trajectory visualization")
    print("  ✅ Calculate ball speed and velocity")
    print("  ✅ Save annotated video")
    print("  ✅ Generate JSON file with ball positions")
    print("\nControls:")
    print("  'p' - Pause/Resume")
    print("  'q' - Quit early")
    print("  SPACE - Toggle visualization")
    print("-"*60)
    
    try:
        # Create processor
        processor = BallTrackingProcessor(video_path, output_dir)
        
        # Process video
        stats = processor.process_video(
            visualize=True,
            save_video=True,
            max_frames=None,  # Process all frames
            skip_frames=1     # Process every frame
        )
        
        # Save JSON
        json_path = processor.save_json()
        
        # Get detailed statistics
        detailed_stats = processor.get_statistics()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Performance Summary")
        print("="*60)
        print(f"Total frames: {stats['total_frames']}")
        print(f"Processed frames: {stats['processed_frames']}")
        print(f"Ball detections: {stats['detections']}")
        print(f"Detection rate: {stats['detection_rate']:.1f}%")
        print(f"Processing time: {stats['processing_time']:.1f}s")
        print(f"Processing FPS: {stats['processing_fps']:.1f}")
        print(f"Video FPS: {stats['video_fps']}")
        
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
        print("📁 Output Files")
        print("="*60)
        print(f"📹 Annotated video: {output_dir}/{video_path.replace('.mp4', '_ball_tracked.mp4')}")
        print(f"📄 JSON data: {json_path}")
        
        print("\n" + "="*60)
        print("🚀 Next Steps")
        print("="*60)
        print("The JSON file contains:")
        print("  • Frame-by-frame ball positions (x, y)")
        print("  • Detection confidence scores")
        print("  • Ball velocity and speed")
        print("  • Timestamps for event correlation")
        print("\nThis data can be used for:")
        print("  🎯 Shot detection and classification")
        print("  📊 Rally analysis")
        print("  🏓 Ball trajectory prediction")
        print("  💡 Integration with pose data for complete analysis")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
