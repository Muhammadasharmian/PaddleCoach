"""
Video processor for analyzing table tennis matches using YOLOv11n pose estimation.
Processes MP4 videos and extracts pose data for both players.
"""
import cv2
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent))
from models.pose_data import PoseData
from vision.player_tracker import PlayerTracker
from vision.shot_detector import ShotDetector


class VideoProcessor:
    """
    Processes MP4 video files to extract pose data for table tennis players.
    """
    
    def __init__(self, video_path: str, output_dir: str = "output", target_fps: int = 30):
        """
        Initialize the video processor.
        
        Args:
            video_path: Path to input MP4 video
            output_dir: Directory to save output files
            target_fps: Target FPS for processing (e.g., 30 for real-time on most systems)
        """
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(str(self.video_path))
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        # Get video properties
        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration = self.total_frames / self.original_fps if self.original_fps > 0 else 0
        
        # Frame skip for target FPS
        self.target_fps = target_fps
        self.frame_skip = max(1, int(self.original_fps / target_fps))
        
        print(f"Video Info:")
        print(f"  Resolution: {self.width}x{self.height}")
        print(f"  Original FPS: {self.original_fps:.2f}")
        print(f"  Target FPS: {self.target_fps}")
        print(f"  Frame Skip: {self.frame_skip} (processing every {self.frame_skip} frames)")
        print(f"  Total Frames: {self.total_frames}")
        print(f"  Duration: {self.duration:.2f}s")
        
        # Initialize player tracker
        self.tracker = PlayerTracker()
        
        # Initialize shot detector
        self.shot_detector = ShotDetector(
            velocity_threshold=15.0,  # Adjust based on video resolution
            min_shot_duration=5,
            max_shot_duration=30,
            cooldown_frames=10
        )
        
        # Storage for all pose data
        self.all_pose_data: Dict[int, List[PoseData]] = {0: [], 1: []}  # Separate by player
        
        # Storage for detected shots
        self.detected_shots: Dict[int, List] = {0: [], 1: []}
    
    def process_video(self, 
                     visualize: bool = True, 
                     save_video: bool = False,
                     max_frames: Optional[int] = None) -> Dict[str, any]:
        """
        Process the entire video and extract pose data.
        Optimized for real-time performance on Apple Silicon.
        
        Args:
            visualize: Whether to show visualization while processing
            save_video: Whether to save annotated video
            max_frames: Maximum number of frames to process (None = all)
            
        Returns:
            Dictionary with processing statistics
        """
        import time
        
        frame_count = 0
        processed_count = 0
        
        # Setup video writer if saving
        video_writer = None
        if save_video:
            output_video_path = self.output_dir / f"{self.video_path.stem}_annotated.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                str(output_video_path),
                fourcc,
                self.target_fps,
                (self.width, self.height)
            )
        
        print("\nProcessing video (optimized for Apple Silicon)...")
        print(f"Press 'q' to quit, 'p' to pause, SPACE to toggle visualization")
        
        paused = False
        show_viz = visualize
        start_time = time.time()
        fps_counter = 0
        fps_start = time.time()
        current_fps = 0
        
        while True:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Check max frames limit
                if max_frames and frame_count >= max_frames:
                    break
                
                # Skip frames for target FPS
                if frame_count % self.frame_skip != 0:
                    frame_count += 1
                    continue
                
                # Calculate timestamp
                timestamp = frame_count / self.original_fps
                
                # Process frame
                pose_data_list = self.tracker.process_frame(frame, frame_count, timestamp)
                
                # Store pose data
                for pose_data in pose_data_list:
                    self.all_pose_data[pose_data.player_id].append(pose_data)
                
                # Visualize
                if show_viz or save_video:
                    annotated_frame = frame.copy()
                    for pose_data in pose_data_list:
                        annotated_frame = self.tracker.visualize_pose(annotated_frame, pose_data)
                    
                    # Add comprehensive info overlay
                    info_y = 30
                    cv2.putText(annotated_frame, f"Frame: {frame_count}/{self.total_frames}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    info_y += 25
                    cv2.putText(annotated_frame, f"Time: {timestamp:.2f}s", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    info_y += 25
                    cv2.putText(annotated_frame, f"Processing FPS: {current_fps:.1f}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    info_y += 25
                    cv2.putText(annotated_frame, f"Players: {len(pose_data_list)}", 
                               (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    if show_viz:
                        # Resize for display if needed (faster visualization)
                        display_frame = annotated_frame
                        if self.width > 1280:
                            scale = 1280 / self.width
                            display_frame = cv2.resize(annotated_frame, 
                                                      (int(self.width * scale), int(self.height * scale)))
                        cv2.imshow('Table Tennis Pose Analysis (Optimized)', display_frame)
                    
                    if save_video and video_writer:
                        video_writer.write(annotated_frame)
                
                processed_count += 1
                frame_count += 1
                
                # Calculate FPS
                fps_counter += 1
                if time.time() - fps_start >= 1.0:
                    current_fps = fps_counter / (time.time() - fps_start)
                    fps_counter = 0
                    fps_start = time.time()
                
                # Progress indicator (every 2 seconds worth of frames)
                if processed_count % (self.target_fps * 2) == 0:
                    progress = (frame_count / self.total_frames) * 100
                    elapsed = time.time() - start_time
                    print(f"Progress: {progress:.1f}% | FPS: {current_fps:.1f} | Elapsed: {elapsed:.1f}s")
            
            # Handle keyboard input
            if show_viz or paused:
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Stopping processing...")
                    break
                elif key == ord('p'):
                    paused = not paused
                    print("⏸️  Paused" if paused else "▶️  Resumed")
                elif key == ord(' '):
                    show_viz = not show_viz
                    print(f"Visualization: {'ON' if show_viz else 'OFF'}")
                    if not show_viz:
                        cv2.destroyAllWindows()
        
        # Cleanup
        elapsed_time = time.time() - start_time
        self.cap.release()
        if video_writer:
            video_writer.release()
        cv2.destroyAllWindows()
        
        avg_fps = processed_count / elapsed_time if elapsed_time > 0 else 0
        
        # Detect shots from pose data
        print(f"\n🔍 Detecting shots...")
        for player_id in [0, 1]:
            shots = self.shot_detector.detect_shots(self.all_pose_data[player_id])
            self.detected_shots[player_id] = shots
            print(f"   Player {player_id}: {len(shots)} shots detected")
        
        print(f"\n✅ Processing complete!")
        print(f"Processed {processed_count} frames in {elapsed_time:.1f}s")
        print(f"Average FPS: {avg_fps:.1f}")
        print(f"Player 0: {len(self.all_pose_data[0])} detections")
        print(f"Player 1: {len(self.all_pose_data[1])} detections")
        
        return {
            "total_frames": self.total_frames,
            "processed_frames": processed_count,
            "player_0_detections": len(self.all_pose_data[0]),
            "player_1_detections": len(self.all_pose_data[1]),
            "duration": self.duration,
            "original_fps": self.original_fps,
            "processing_fps": avg_fps,
            "processing_time": elapsed_time
        }
    
    def save_pose_data_json(self, filename: Optional[str] = None) -> Path:
        """
        Save all pose data to a compact JSON file (only wrists and elbows).
        
        Args:
            filename: Output filename (default: {video_name}_pose_data.json)
            
        Returns:
            Path to the saved JSON file
        """
        if filename is None:
            filename = f"{self.video_path.stem}_pose_data.json"
        
        output_path = self.output_dir / filename
        
        # Convert to serializable format (compact)
        output_data = {
            "metadata": {
                "video_file": str(self.video_path.name),
                "processed_date": datetime.now().isoformat(),
                "video_info": {
                    "resolution": f"{self.width}x{self.height}",
                    "original_fps": round(self.original_fps, 2),
                    "processed_fps": self.target_fps,
                    "total_frames": self.total_frames,
                    "duration_seconds": round(self.duration, 2)
                },
                "tracking_info": {
                    "keypoints_tracked": ["left_wrist", "left_elbow", "right_wrist", "right_elbow"],
                    "player_0_frames": len(self.all_pose_data[0]),
                    "player_1_frames": len(self.all_pose_data[1])
                }
            },
            "player_0": [pose.to_dict() for pose in self.all_pose_data[0]],
            "player_1": [pose.to_dict() for pose in self.all_pose_data[1]]
        }
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        file_size_kb = output_path.stat().st_size / 1024
        
        print(f"\n💾 Pose data saved: {output_path}")
        print(f"   File size: {file_size_kb:.2f} KB")
        print(f"   Total data points: {len(self.all_pose_data[0]) + len(self.all_pose_data[1])}")
        
        return output_path
    
    def save_shots_json(self, filename: Optional[str] = None) -> Path:
        """
        Save only detected shots to JSON (HIGHLY OPTIMIZED for Gemini API).
        This creates a much smaller file focused on shot events only.
        
        Args:
            filename: Output filename (default: {video_name}_shots.json)
            
        Returns:
            Path to the saved JSON file
        """
        if filename is None:
            filename = f"{self.video_path.stem}_shots.json"
        
        output_path = self.output_dir / filename
        
        # Calculate shot statistics
        total_shots = len(self.detected_shots[0]) + len(self.detected_shots[1])
        
        # Convert to serializable format (ultra-compact)
        output_data = {
            "metadata": {
                "video_file": str(self.video_path.name),
                "processed_date": datetime.now().isoformat(),
                "video_info": {
                    "resolution": f"{self.width}x{self.height}",
                    "duration_seconds": round(self.duration, 2),
                    "fps": self.target_fps
                },
                "analysis_summary": {
                    "total_shots_detected": total_shots,
                    "player_0_shots": len(self.detected_shots[0]),
                    "player_1_shots": len(self.detected_shots[1]),
                    "detection_method": "velocity_based_wrist_tracking"
                },
                "gemini_usage": {
                    "purpose": "Shot classification, technique analysis, coaching feedback",
                    "data_format": "Compact shot events with kinematics",
                    "estimated_tokens": total_shots * 150  # Rough estimate
                }
            },
            "shots": {
                "player_0": [shot.to_dict() for shot in self.detected_shots[0]],
                "player_1": [shot.to_dict() for shot in self.detected_shots[1]]
            },
            "analysis_hints": {
                "shot_classification": {
                    "vertical_positive": "Likely topspin (upward motion)",
                    "vertical_negative": "Likely backspin/chop (downward motion)",
                    "high_velocity": "Likely smash/drive",
                    "low_velocity": "Likely push/block",
                    "large_arc": "Full stroke",
                    "small_arc": "Short stroke/flick"
                },
                "technique_analysis": {
                    "backswing_angle": "Racket preparation",
                    "contact_angle": "Impact position",
                    "followthrough_angle": "Stroke completion",
                    "duration": "Stroke speed and control"
                }
            }
        }
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        file_size_kb = output_path.stat().st_size / 1024
        reduction = 100 * (1 - file_size_kb / (output_path.parent / f"{self.video_path.stem}_pose_data.json").stat().st_size * 1024) if (output_path.parent / f"{self.video_path.stem}_pose_data.json").exists() else 0
        
        print(f"\n💾 Optimized shot data saved: {output_path}")
        print(f"   File size: {file_size_kb:.2f} KB")
        print(f"   Total shots: {total_shots}")
        print(f"   Avg per player: {total_shots / 2:.1f}")
        if reduction > 0:
            print(f"   Size reduction: {reduction:.1f}% smaller than full pose data")
        
        return output_path
    
    def get_summary_statistics(self) -> Dict:
        """
        Calculate summary statistics for both players (focused on arm movements).
        
        Returns:
            Dictionary with summary statistics
        """
        stats = {}
        
        for player_id in [0, 1]:
            pose_list = self.all_pose_data[player_id]
            
            if not pose_list:
                stats[f"player_{player_id}"] = {"detections": 0}
                continue
            
            # Wrist tracking stats
            left_wrist_count = sum(1 for p in pose_list if p.left_wrist and p.left_wrist.confidence > 0.3)
            right_wrist_count = sum(1 for p in pose_list if p.right_wrist and p.right_wrist.confidence > 0.3)
            
            # Elbow tracking stats
            left_elbow_count = sum(1 for p in pose_list if p.left_elbow and p.left_elbow.confidence > 0.3)
            right_elbow_count = sum(1 for p in pose_list if p.right_elbow and p.right_elbow.confidence > 0.3)
            
            # Arm angle stats
            left_angles = [p.left_arm_angle for p in pose_list if p.left_arm_angle is not None]
            right_angles = [p.right_arm_angle for p in pose_list if p.right_arm_angle is not None]
            
            stats[f"player_{player_id}"] = {
                "total_frames": len(pose_list),
                "left_wrist_detected": left_wrist_count,
                "right_wrist_detected": right_wrist_count,
                "left_elbow_detected": left_elbow_count,
                "right_elbow_detected": right_elbow_count,
                "left_wrist_rate": left_wrist_count / len(pose_list) if pose_list else 0,
                "right_wrist_rate": right_wrist_count / len(pose_list) if pose_list else 0,
                "avg_left_arm_angle": sum(left_angles) / len(left_angles) if left_angles else None,
                "avg_right_arm_angle": sum(right_angles) / len(right_angles) if right_angles else None
            }
        
        return stats


def main():
    """Example usage of VideoProcessor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process table tennis video with YOLOv11n pose estimation")
    parser.add_argument("video_path", type=str, help="Path to input MP4 video")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory")
    parser.add_argument("--no-visualize", action="store_true", help="Disable visualization")
    parser.add_argument("--no-save-video", action="store_true", help="Don't save annotated video")
    parser.add_argument("--skip-frames", type=int, default=0, help="Process every Nth frame")
    parser.add_argument("--max-frames", type=int, default=None, help="Maximum frames to process")
    
    args = parser.parse_args()
    
    # Create processor
    processor = VideoProcessor(args.video_path, args.output_dir)
    
    # Process video
    stats = processor.process_video(
        visualize=not args.no_visualize,
        save_video=not args.no_save_video,
        skip_frames=args.skip_frames,
        max_frames=args.max_frames
    )
    
    # Save pose data to JSON
    json_path = processor.save_pose_data_json()
    
    # Print summary statistics
    summary = processor.get_summary_statistics()
    print("\n" + "="*50)
    print("SUMMARY STATISTICS")
    print("="*50)
    for player, player_stats in summary.items():
        print(f"\n{player.upper()}:")
        for key, value in player_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.3f}")
            else:
                print(f"  {key}: {value}")
    
    print(f"\nJSON data ready for Gemini 2.5 Pro API processing!")


if __name__ == "__main__":
    main()
