"""
Ball tracker for table tennis using YOLO object detection.
Tracks ball position and draws trajectory lines.
"""
from typing import List, Tuple, Optional, Deque
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
from collections import deque
import sys

sys.path.append(str(Path(__file__).parent.parent))
from models.ball_data import BallData


class BallTracker:
    """
    Tracks table tennis ball using YOLO object detection.
    Maintains trajectory history and calculates ball speed.
    """
    
    def __init__(self, model_path: str = "best.pt", max_trajectory: int = 30):
        """
        Initialize the ball tracker with YOLO model.
        
        Args:
            model_path: Path to YOLO model weights (best.pt for ball detection)
            max_trajectory: Maximum number of positions to keep in trajectory
        """
        print(f"Loading ball detection model: {model_path}")
        self.model = YOLO(model_path)
        
        # Trajectory history (deque for efficient FIFO)
        self.trajectory: Deque[Tuple[int, int]] = deque(maxlen=max_trajectory)
        self.max_trajectory = max_trajectory
        
        # Minimum confidence threshold
        self.min_confidence = 0.3  # Lower for small fast-moving ball
        
        # Ball color for visualization (orange: #fa8b32)
        self.ball_color = (50, 139, 250)  # BGR format
        self.trajectory_color = (255, 150, 0)  # Blue for trajectory line
    
    def process_frame(self, frame: np.ndarray, frame_number: int, timestamp: float) -> Optional[BallData]:
        """
        Process a single frame and detect ball position.
        
        Args:
            frame: Input frame (BGR format)
            frame_number: Current frame number
            timestamp: Timestamp in seconds from video start
            
        Returns:
            BallData object if ball detected, None otherwise
        """
        # Run YOLO detection with optimizations
        results = self.model(
            frame,
            conf=self.min_confidence,
            verbose=False,
            half=True,  # FP16 for speed
            device='mps'  # Apple Metal GPU
        )
        
        if len(results) == 0 or results[0].boxes is None or len(results[0].boxes) == 0:
            return None
        
        result = results[0]
        
        # Get the detection with highest confidence
        best_detection = None
        best_conf = 0
        
        for box in result.boxes:
            conf = float(box.conf[0])
            if conf > best_conf:
                best_conf = conf
                best_detection = box
        
        if best_detection is None:
            return None
        
        # Create BallData
        ball_data = BallData.from_detection(best_detection, frame_number, timestamp)
        
        # Add to trajectory
        self.trajectory.append((int(ball_data.x), int(ball_data.y)))
        
        # Calculate velocity if we have previous positions
        if len(self.trajectory) >= 2:
            prev_pos = self.trajectory[-2]
            curr_pos = self.trajectory[-1]
            
            # Assuming consistent frame rate, velocity in pixels per frame
            ball_data.velocity_x = curr_pos[0] - prev_pos[0]
            ball_data.velocity_y = curr_pos[1] - prev_pos[1]
            ball_data.speed = np.sqrt(ball_data.velocity_x**2 + ball_data.velocity_y**2)
        
        return ball_data
    
    def visualize_ball(self, frame: np.ndarray, ball_data: Optional[BallData]) -> np.ndarray:
        """
        Draw ball position and trajectory on frame.
        
        Args:
            frame: Input frame
            ball_data: BallData object to visualize
            
        Returns:
            Frame with ball visualization
        """
        # Draw trajectory line
        if len(self.trajectory) >= 2:
            # Draw smooth trajectory curve
            points = np.array(list(self.trajectory), dtype=np.int32)
            
            # Draw the trajectory line with varying thickness
            for i in range(len(points) - 1):
                # Thickness decreases for older points
                alpha = (i + 1) / len(points)
                thickness = int(2 + alpha * 3)
                
                cv2.line(frame,
                        tuple(points[i]),
                        tuple(points[i + 1]),
                        self.trajectory_color,
                        thickness)
        
        # Draw current ball position
        if ball_data is not None:
            center = (int(ball_data.x), int(ball_data.y))
            
            # Draw outer glow
            cv2.circle(frame, center, 15, self.ball_color, 2)
            # Draw inner filled circle
            cv2.circle(frame, center, 8, self.ball_color, -1)
            
            # Draw confidence text
            conf_text = f"{ball_data.confidence:.2f}"
            cv2.putText(frame, conf_text,
                       (center[0] + 20, center[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255, 255, 255), 2)
            
            # Draw speed if available
            if ball_data.speed is not None and ball_data.speed > 5:
                speed_text = f"{ball_data.speed:.0f} px/s"
                cv2.putText(frame, speed_text,
                           (center[0] + 20, center[1] + 10),
                           cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (0, 255, 255), 2)
        
        return frame
    
    def reset_trajectory(self):
        """Clear the trajectory history."""
        self.trajectory.clear()
