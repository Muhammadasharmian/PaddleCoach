"""
Shot detector for identifying significant paddle movements in table tennis.
Detects shots based on wrist velocity and acceleration changes.
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class Shot:
    """Represents a detected shot/stroke in table tennis."""
    player_id: int
    start_frame: int
    peak_frame: int  # Frame with maximum velocity
    end_frame: int
    start_time: float
    peak_time: float
    end_time: float
    
    # Shot characteristics
    hand: str  # 'left' or 'right'
    max_velocity: float  # px/frame
    acceleration: float  # change in velocity
    
    # Wrist positions at key moments
    backswing_pos: Tuple[float, float]  # (x, y) at start
    contact_pos: Tuple[float, float]    # (x, y) at peak
    followthrough_pos: Tuple[float, float]  # (x, y) at end
    
    # Arm angles
    backswing_angle: Optional[float] = None
    contact_angle: Optional[float] = None
    followthrough_angle: Optional[float] = None
    
    # Shot classification hints (for Gemini)
    vertical_movement: float = 0.0  # Positive = upward (topspin likely)
    horizontal_movement: float = 0.0  # Positive = forward
    swing_arc: float = 0.0  # Total path length
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON."""
        return {
            "player": self.player_id,
            "frames": {
                "start": self.start_frame,
                "peak": self.peak_frame,
                "end": self.end_frame
            },
            "time": {
                "start": round(self.start_time, 3),
                "peak": round(self.peak_time, 3),
                "end": round(self.end_time, 3),
                "duration": round(self.end_time - self.start_time, 3)
            },
            "hand": self.hand,
            "motion": {
                "max_velocity": round(self.max_velocity, 2),
                "acceleration": round(self.acceleration, 2),
                "vertical": round(self.vertical_movement, 2),
                "horizontal": round(self.horizontal_movement, 2),
                "arc_length": round(self.swing_arc, 2)
            },
            "positions": {
                "backswing": {"x": round(self.backswing_pos[0], 1), "y": round(self.backswing_pos[1], 1)},
                "contact": {"x": round(self.contact_pos[0], 1), "y": round(self.contact_pos[1], 1)},
                "followthrough": {"x": round(self.followthrough_pos[0], 1), "y": round(self.followthrough_pos[1], 1)}
            },
            "angles": {
                "backswing": round(self.backswing_angle, 1) if self.backswing_angle else None,
                "contact": round(self.contact_angle, 1) if self.contact_angle else None,
                "followthrough": round(self.followthrough_angle, 1) if self.followthrough_angle else None
            }
        }


class ShotDetector:
    """
    Detects table tennis shots from pose data stream.
    Identifies significant wrist movements that indicate strokes.
    """
    
    def __init__(self, 
                 velocity_threshold: float = 15.0,  # px/frame minimum velocity
                 min_shot_duration: int = 5,  # Minimum frames for a shot
                 max_shot_duration: int = 30,  # Maximum frames for a shot
                 cooldown_frames: int = 10):  # Frames between shots
        """
        Initialize shot detector.
        
        Args:
            velocity_threshold: Minimum wrist velocity to detect shot
            min_shot_duration: Minimum frames for valid shot
            max_shot_duration: Maximum frames for valid shot
            cooldown_frames: Minimum frames between consecutive shots
        """
        self.velocity_threshold = velocity_threshold
        self.min_shot_duration = min_shot_duration
        self.max_shot_duration = max_shot_duration
        self.cooldown_frames = cooldown_frames
    
    def detect_shots(self, pose_data_list: List) -> List[Shot]:
        """
        Detect shots from a sequence of pose data.
        
        Args:
            pose_data_list: List of PoseData objects for one player
            
        Returns:
            List of detected Shot objects
        """
        if len(pose_data_list) < self.min_shot_duration:
            return []
        
        shots = []
        
        # Analyze both hands separately
        for hand in ['left', 'right']:
            hand_shots = self._detect_hand_shots(pose_data_list, hand)
            shots.extend(hand_shots)
        
        # Sort by time
        shots.sort(key=lambda s: s.start_time)
        
        return shots
    
    def _detect_hand_shots(self, pose_data_list: List, hand: str) -> List[Shot]:
        """Detect shots for a specific hand."""
        # Extract wrist positions and times
        wrist_data = []
        elbow_data = []
        angles_data = []
        
        for pose in pose_data_list:
            wrist = pose.left_wrist if hand == 'left' else pose.right_wrist
            elbow = pose.left_elbow if hand == 'left' else pose.right_elbow
            angle = pose.left_arm_angle if hand == 'left' else pose.right_arm_angle
            
            if wrist and elbow and wrist.confidence > 0.5:
                wrist_data.append({
                    'frame': pose.frame_number,
                    'time': pose.timestamp,
                    'pos': (wrist.x, wrist.y),
                    'elbow_pos': (elbow.x, elbow.y) if elbow.confidence > 0.5 else None,
                    'angle': angle
                })
        
        if len(wrist_data) < self.min_shot_duration:
            return []
        
        # Calculate velocities
        velocities = []
        for i in range(1, len(wrist_data)):
            dx = wrist_data[i]['pos'][0] - wrist_data[i-1]['pos'][0]
            dy = wrist_data[i]['pos'][1] - wrist_data[i-1]['pos'][1]
            velocity = math.sqrt(dx*dx + dy*dy)
            velocities.append({
                'idx': i,
                'velocity': velocity,
                'dx': dx,
                'dy': dy
            })
        
        # Detect shot sequences
        shots = []
        in_shot = False
        shot_start_idx = 0
        last_shot_end = -self.cooldown_frames
        
        for i, vel_data in enumerate(velocities):
            idx = vel_data['idx']
            
            # Start of shot: velocity exceeds threshold
            if not in_shot and vel_data['velocity'] > self.velocity_threshold:
                if idx - last_shot_end >= self.cooldown_frames:
                    in_shot = True
                    shot_start_idx = max(0, idx - 2)  # Include a bit of backswing
            
            # End of shot: velocity drops below threshold
            elif in_shot and vel_data['velocity'] < self.velocity_threshold * 0.5:
                shot_end_idx = min(idx + 2, len(wrist_data) - 1)  # Include followthrough
                shot_duration = shot_end_idx - shot_start_idx
                
                if self.min_shot_duration <= shot_duration <= self.max_shot_duration:
                    # Create shot object
                    shot = self._create_shot(
                        wrist_data[shot_start_idx:shot_end_idx + 1],
                        velocities[shot_start_idx:shot_end_idx],
                        hand,
                        pose_data_list[0].player_id
                    )
                    if shot:
                        shots.append(shot)
                        last_shot_end = shot_end_idx
                
                in_shot = False
        
        return shots
    
    def _create_shot(self, wrist_sequence: List[Dict], velocity_sequence: List[Dict], 
                     hand: str, player_id: int) -> Optional[Shot]:
        """Create a Shot object from detected sequence."""
        if len(wrist_sequence) < 3:
            return None
        
        # Find peak velocity frame
        max_vel_idx = max(range(len(velocity_sequence)), 
                         key=lambda i: velocity_sequence[i]['velocity'])
        
        start_data = wrist_sequence[0]
        peak_data = wrist_sequence[max_vel_idx]
        end_data = wrist_sequence[-1]
        
        # Calculate movement characteristics
        dx_total = end_data['pos'][0] - start_data['pos'][0]
        dy_total = end_data['pos'][1] - start_data['pos'][1]
        
        # Calculate swing arc length
        arc_length = sum(
            math.sqrt((wrist_sequence[i]['pos'][0] - wrist_sequence[i-1]['pos'][0])**2 +
                     (wrist_sequence[i]['pos'][1] - wrist_sequence[i-1]['pos'][1])**2)
            for i in range(1, len(wrist_sequence))
        )
        
        # Calculate acceleration
        velocities = [v['velocity'] for v in velocity_sequence]
        max_velocity = max(velocities)
        acceleration = max_velocity - velocities[0]
        
        return Shot(
            player_id=player_id,
            start_frame=start_data['frame'],
            peak_frame=peak_data['frame'],
            end_frame=end_data['frame'],
            start_time=start_data['time'],
            peak_time=peak_data['time'],
            end_time=end_data['time'],
            hand=hand,
            max_velocity=max_velocity,
            acceleration=acceleration,
            backswing_pos=start_data['pos'],
            contact_pos=peak_data['pos'],
            followthrough_pos=end_data['pos'],
            backswing_angle=start_data['angle'],
            contact_angle=peak_data['angle'],
            followthrough_angle=end_data['angle'],
            vertical_movement=dy_total,
            horizontal_movement=dx_total,
            swing_arc=arc_length
        )
