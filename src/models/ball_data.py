"""
BallData class for storing ball position and trajectory information.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class BallData:
    """
    Stores ball detection data at a specific frame.
    Minimal data for Gemini API efficiency.
    """
    frame_number: int
    timestamp: float  # Time in seconds from video start
    
    # Ball position
    x: float
    y: float
    confidence: float
    
    # Velocity (calculated from trajectory)
    velocity_x: Optional[float] = None
    velocity_y: Optional[float] = None
    speed: Optional[float] = None  # Pixels per second
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization (compact)."""
        data = {
            "f": self.frame_number,  # Shortened field names for compactness
            "t": round(self.timestamp, 3),
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "c": round(self.confidence, 2)
        }
        
        # Only include velocity if available
        if self.velocity_x is not None:
            data["vx"] = round(self.velocity_x, 1)
        if self.velocity_y is not None:
            data["vy"] = round(self.velocity_y, 1)
        if self.speed is not None:
            data["s"] = round(self.speed, 1)
        
        return data
    
    @classmethod
    def from_detection(cls, detection, frame_number: int, timestamp: float):
        """
        Create BallData from YOLO detection.
        
        Args:
            detection: YOLO detection result
            frame_number: Current frame number
            timestamp: Timestamp in seconds
        """
        # Extract center position
        x, y, w, h = detection.xywh[0].tolist()
        conf = float(detection.conf[0])
        
        return cls(
            frame_number=frame_number,
            timestamp=timestamp,
            x=x,
            y=y,
            confidence=conf
        )
