"""
PoseData class for storing player pose information from YOLOv11n pose estimation.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json


@dataclass
class Keypoint:
    """Represents a single keypoint in the pose."""
    x: float
    y: float
    confidence: float
    name: str  # e.g., "nose", "left_shoulder", etc.


@dataclass
class PoseData:
    """
    Stores pose estimation data for a single player at a specific frame.
    Tracks only essential keypoints for table tennis: wrists and elbows.
    """
    frame_number: int
    timestamp: float  # Time in seconds from video start
    player_id: int  # 0 or 1 for two players
    
    # Essential keypoints for table tennis analysis
    # Left arm
    left_wrist: Optional[Keypoint] = None
    left_elbow: Optional[Keypoint] = None
    
    # Right arm
    right_wrist: Optional[Keypoint] = None
    right_elbow: Optional[Keypoint] = None
    
    # Computed arm angles
    left_arm_angle: Optional[float] = None  # Angle at left elbow
    right_arm_angle: Optional[float] = None  # Angle at right elbow
    
    @staticmethod
    def get_coco_keypoint_names() -> List[str]:
        """Return the 17 COCO keypoint names in order."""
        return [
            "nose",
            "left_eye", "right_eye",
            "left_ear", "right_ear",
            "left_shoulder", "right_shoulder",
            "left_elbow", "right_elbow",
            "left_wrist", "right_wrist",
            "left_hip", "right_hip",
            "left_knee", "right_knee",
            "left_ankle", "right_ankle"
        ]
    
    def compute_arm_angles(self):
        """Calculate arm angles at elbows (for paddle swing analysis)."""
        import math
        
        # Left arm angle
        if self.left_wrist and self.left_elbow:
            if self.left_wrist.confidence > 0.3 and self.left_elbow.confidence > 0.3:
                dx = self.left_wrist.x - self.left_elbow.x
                dy = self.left_wrist.y - self.left_elbow.y
                self.left_arm_angle = math.degrees(math.atan2(dy, dx))
        
        # Right arm angle
        if self.right_wrist and self.right_elbow:
            if self.right_wrist.confidence > 0.3 and self.right_elbow.confidence > 0.3:
                dx = self.right_wrist.x - self.right_elbow.x
                dy = self.right_wrist.y - self.right_elbow.y
                self.right_arm_angle = math.degrees(math.atan2(dy, dx))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization (only essential data)."""
        def keypoint_to_dict(kp: Optional[Keypoint]) -> Optional[Dict]:
            if kp is None:
                return None
            return {
                "x": round(kp.x, 2),
                "y": round(kp.y, 2),
                "confidence": round(kp.confidence, 3)
            }
        
        return {
            "frame": self.frame_number,
            "time": round(self.timestamp, 3),
            "player": self.player_id,
            "left_wrist": keypoint_to_dict(self.left_wrist),
            "left_elbow": keypoint_to_dict(self.left_elbow),
            "right_wrist": keypoint_to_dict(self.right_wrist),
            "right_elbow": keypoint_to_dict(self.right_elbow),
            "angles": {
                "left_arm": round(self.left_arm_angle, 2) if self.left_arm_angle else None,
                "right_arm": round(self.right_arm_angle, 2) if self.right_arm_angle else None
            }
        }
    
    @classmethod
    def from_yolo_result(cls, result, frame_number: int, timestamp: float, player_id: int):
        """
        Create PoseData from YOLOv11 pose estimation result.
        Extracts only wrists and elbows for efficient processing.
        
        Args:
            result: YOLOv11 result object containing keypoints
            frame_number: Current frame number
            timestamp: Timestamp in seconds
            player_id: Player identifier (0 or 1)
        """
        # Extract keypoints (17 COCO keypoints)
        keypoints_data = result.keypoints[0]  # Shape: [17, 3] (x, y, conf)
        keypoint_names = cls.get_coco_keypoint_names()
        
        # Extract only the essential keypoints
        left_wrist = None
        left_elbow = None
        right_wrist = None
        right_elbow = None
        
        for i, name in enumerate(keypoint_names):
            x, y, conf = keypoints_data.data[0][i].tolist()
            
            if name == "left_wrist":
                left_wrist = Keypoint(x=x, y=y, confidence=conf, name=name)
            elif name == "left_elbow":
                left_elbow = Keypoint(x=x, y=y, confidence=conf, name=name)
            elif name == "right_wrist":
                right_wrist = Keypoint(x=x, y=y, confidence=conf, name=name)
            elif name == "right_elbow":
                right_elbow = Keypoint(x=x, y=y, confidence=conf, name=name)
        
        pose_data = cls(
            frame_number=frame_number,
            timestamp=timestamp,
            player_id=player_id,
            left_wrist=left_wrist,
            left_elbow=left_elbow,
            right_wrist=right_wrist,
            right_elbow=right_elbow
        )
        
        # Compute arm angles
        pose_data.compute_arm_angles()
        
        return pose_data
