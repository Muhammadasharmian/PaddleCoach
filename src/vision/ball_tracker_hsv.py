"""
Ball tracker for table tennis using HSV color detection.
Tracks orange ball position and draws trajectory lines.
"""
from typing import List, Tuple, Optional, Deque
import cv2
import numpy as np
from pathlib import Path
from collections import deque
import sys

sys.path.append(str(Path(__file__).parent.parent))
from models.ball_data import BallData


class BallTrackerHSV:
    """
    Tracks table tennis ball using HSV color detection.
    Maintains trajectory history and calculates ball speed.
    """
    
    def __init__(self, hsv_lower: List[int] = None, hsv_upper: List[int] = None, max_trajectory: int = 50):
        """
        Initialize the ball tracker with HSV color detection.
        
        Args:
            hsv_lower: Lower HSV threshold [H, S, V] for orange ball
            hsv_upper: Upper HSV threshold [H, S, V] for orange ball
            max_trajectory: Maximum number of positions to keep in trajectory
        """
        print(f"Initializing HSV color-based ball tracker")
        
        # HSV color range for orange ball (#fa8b32)
        self.hsv_lower = np.array(hsv_lower if hsv_lower else [5, 150, 150])
        self.hsv_upper = np.array(hsv_upper if hsv_upper else [20, 255, 255])
        
        print(f"  HSV Lower: {self.hsv_lower}")
        print(f"  HSV Upper: {self.hsv_upper}")
        
        # Trajectory history (deque for efficient FIFO)
        self.trajectory: Deque[Tuple[int, int]] = deque(maxlen=max_trajectory)
        self.max_trajectory = max_trajectory
        
        # Ball color for visualization (orange: #fa8b32)
        self.ball_color = (50, 139, 250)  # BGR format (OpenCV uses BGR)
        self.trajectory_color = (255, 0, 0)  # Blue for trajectory line
        
        # Area thresholds for filtering
        self.min_area = 50
        self.max_area = 5000
        self.min_circularity = 0.6  # Minimum circularity threshold (1.0 = perfect circle)
    
    def process_frame(self, frame: np.ndarray, frame_number: int, timestamp: float) -> Optional[BallData]:
        """
        Process a single frame and detect ball position using HSV color detection.
        
        Args:
            frame: Input frame (BGR format)
            frame_number: Current frame number
            timestamp: Timestamp in seconds from video start
            
        Returns:
            BallData object if ball detected, None otherwise
        """
        # Blur and convert to HSV
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Create mask using HSV values
        mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)
        
        # Clean up mask
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            return None
        
        # Find the best candidate (most circular, reasonable size)
        best_contour = None
        best_score = 0
        
        for c in contours:
            area = cv2.contourArea(c)
            
            # Filter by area
            if area > self.min_area and area < self.max_area:
                perimeter = cv2.arcLength(c, True)
                if perimeter > 0:
                    # Calculate circularity (1.0 = perfect circle)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # Score based on circularity and area
                    if circularity > self.min_circularity:
                        score = circularity * min(area / 500, 1.0)
                        
                        if score > best_score:
                            best_score = score
                            best_contour = c
        
        if best_contour is None:
            return None
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(best_contour)
        
        # Calculate center
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Create BallData with high confidence (HSV is reliable when it finds something)
        ball_data = BallData(
            frame_number=frame_number,
            timestamp=timestamp,
            x=float(center_x),
            y=float(center_y),
            confidence=min(best_score, 1.0)  # Normalize score to 0-1
        )
        
        # Add to trajectory
        self.trajectory.append((center_x, center_y))
        
        # Calculate velocity if we have previous positions
        if len(self.trajectory) >= 2:
            prev_pos = self.trajectory[-2]
            curr_pos = self.trajectory[-1]
            
            # Velocity in pixels per frame
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
        # Draw trajectory trail
        for i in range(1, len(self.trajectory)):
            if self.trajectory[i - 1] is None or self.trajectory[i] is None:
                continue
            
            # Thickness decreases with older positions
            thickness = int(np.sqrt(self.max_trajectory / float(i + 1)) * 1.5)
            cv2.line(frame, self.trajectory[i - 1], self.trajectory[i], 
                    self.trajectory_color, thickness)
        
        # Draw current ball position
        if ball_data is not None:
            center = (int(ball_data.x), int(ball_data.y))
            
            # Make it a square box
            box_size = 30  # Box size
            x1 = center[0] - box_size // 2
            y1 = center[1] - box_size // 2
            x2 = center[0] + box_size // 2
            y2 = center[1] + box_size // 2
            
            # Draw square box around ball
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw center point
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
            
            # Draw label
            cv2.putText(frame, "Ball", (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Draw confidence
            conf_text = f"Conf: {ball_data.confidence:.2f}"
            cv2.putText(frame, conf_text,
                       (x1, y2 + 20),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255, 255, 255), 2)
            
            # Draw speed if available
            if ball_data.speed is not None and ball_data.speed > 1:
                speed_text = f"Speed: {ball_data.speed:.0f} px/f"
                cv2.putText(frame, speed_text,
                           (x1, y2 + 40),
                           cv2.FONT_HERSHEY_SIMPLEX,
                           0.5, (0, 255, 255), 2)
        
        return frame
    
    def reset_trajectory(self):
        """Clear the trajectory history."""
        self.trajectory.clear()
