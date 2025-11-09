"""
Player pose tracker using YOLOv11n pose estimation.
Tracks two table tennis players and extracts pose data.
"""
from typing import List, Dict, Tuple, Optional
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from models.pose_data import PoseData, Keypoint


class PlayerTracker:
    """
    Tracks two table tennis players using YOLOv11n pose estimation.
    Maintains consistent player IDs across frames.
    """
    
    def __init__(self, model_name: str = "yolo11n-pose.pt", use_half: bool = True):
        """
        Initialize the player tracker with YOLOv11n pose model.
        Optimized for Apple Silicon M-series chips.
        
        Args:
            model_name: YOLOv11 pose model name (default: yolo11n-pose.pt)
            use_half: Use FP16 half-precision for faster inference (recommended for Apple Silicon)
        """
        print(f"Loading YOLOv11 pose model: {model_name}")
        self.model = YOLO(model_name)
        
        # Optimize for Apple Silicon
        self.use_half = use_half
        
        # Track player positions across frames for ID consistency
        self.player_history: Dict[int, List[Tuple[float, float]]] = {0: [], 1: []}
        self.max_history = 10  # Reduced from 30 for better performance
        
        # Minimum confidence threshold (lowered for faster processing)
        self.min_confidence = 0.4
    
    def _assign_player_id(self, bbox_centers: List[Tuple[float, float]]) -> List[int]:
        """
        Assign consistent player IDs based on spatial proximity to previous frames.
        
        Args:
            bbox_centers: List of (x, y) centers for detected players
            
        Returns:
            List of player IDs (0 or 1) corresponding to each detection
        """
        if len(bbox_centers) == 0:
            return []
        
        # If no history, assign based on x-position (left player = 0, right player = 1)
        if not self.player_history[0] and not self.player_history[1]:
            if len(bbox_centers) == 1:
                return [0]
            else:
                # Sort by x-coordinate
                sorted_indices = sorted(range(len(bbox_centers)), key=lambda i: bbox_centers[i][0])
                player_ids = [0] * len(bbox_centers)
                player_ids[sorted_indices[0]] = 0
                player_ids[sorted_indices[1]] = 1
                return player_ids
        
        # Match with previous positions using Hungarian algorithm (simple nearest neighbor)
        player_ids = []
        used_ids = set()
        
        for center in bbox_centers:
            min_dist = float('inf')
            best_id = 0
            
            for player_id in [0, 1]:
                if player_id in used_ids:
                    continue
                
                if self.player_history[player_id]:
                    # Calculate distance to last known position
                    last_pos = self.player_history[player_id][-1]
                    dist = np.sqrt((center[0] - last_pos[0])**2 + (center[1] - last_pos[1])**2)
                    
                    if dist < min_dist:
                        min_dist = dist
                        best_id = player_id
            
            player_ids.append(best_id)
            used_ids.add(best_id)
        
        return player_ids
    
    def _update_player_history(self, player_id: int, center: Tuple[float, float]):
        """Update player position history."""
        self.player_history[player_id].append(center)
        if len(self.player_history[player_id]) > self.max_history:
            self.player_history[player_id].pop(0)
    
    def process_frame(self, frame: np.ndarray, frame_number: int, timestamp: float) -> List[PoseData]:
        """
        Process a single frame and extract pose data for both players.
        Optimized for speed - only extracts wrists and elbows.
        
        Args:
            frame: Input frame (BGR format)
            frame_number: Current frame number
            timestamp: Timestamp in seconds from video start
            
        Returns:
            List of PoseData objects (one per detected player)
        """
        # Run YOLOv11 pose estimation with optimizations
        results = self.model(
            frame, 
            conf=self.min_confidence, 
            verbose=False,
            half=self.use_half,  # Use FP16 for faster inference
            device='mps'  # Use Apple Metal Performance Shaders
        )
        
        pose_data_list = []
        
        if len(results) == 0 or results[0].keypoints is None:
            return pose_data_list
        
        result = results[0]
        
        # Check if we have detections
        if result.boxes is None or len(result.boxes) == 0:
            return pose_data_list
        
        # Extract bounding box centers for player ID assignment
        bbox_centers = []
        for box in result.boxes:
            x, y, w, h = box.xywh[0].tolist()
            bbox_centers.append((x, y))
        
        # Assign player IDs
        player_ids = self._assign_player_id(bbox_centers)
        
        # Create PoseData for each detected player
        for idx, keypoints in enumerate(result.keypoints):
            if idx >= len(player_ids):
                break
            
            player_id = player_ids[idx]
            
            # Extract ALL keypoints for full body pose tracking
            keypoints_array = keypoints.data[0]  # Shape: [17, 3]
            keypoint_names = PoseData.get_coco_keypoint_names()
            
            # Store all keypoints
            all_keypoints = {}
            
            for i, name in enumerate(keypoint_names):
                kp_x, kp_y, kp_conf = keypoints_array[i].tolist()
                all_keypoints[name] = Keypoint(x=kp_x, y=kp_y, confidence=kp_conf, name=name)
            
            # Create PoseData object with all keypoints
            pose_data = PoseData(
                frame_number=frame_number,
                timestamp=timestamp,
                player_id=player_id,
                left_wrist=all_keypoints.get("left_wrist"),
                left_elbow=all_keypoints.get("left_elbow"),
                right_wrist=all_keypoints.get("right_wrist"),
                right_elbow=all_keypoints.get("right_elbow")
            )
            
            # Store all other keypoints for full body visualization
            pose_data.all_keypoints = all_keypoints
            
            # Compute arm angles
            pose_data.compute_arm_angles()
            
            # Update player history
            center_x = bbox_centers[idx][0]
            center_y = bbox_centers[idx][1]
            self._update_player_history(player_id, (center_x, center_y))
            
            pose_data_list.append(pose_data)
        
        return pose_data_list
    
    def visualize_pose(self, frame: np.ndarray, pose_data: PoseData) -> np.ndarray:
        """
        Draw full body skeleton on frame (all 17 COCO keypoints).
        
        Args:
            frame: Input frame
            pose_data: PoseData object to visualize
            
        Returns:
            Frame with pose visualization
        """
        # Color based on player ID
        color = (0, 255, 0) if pose_data.player_id == 0 else (255, 0, 0)
        player_name = f"Player {pose_data.player_id}"
        
        # Get all keypoints if available
        keypoints = getattr(pose_data, 'all_keypoints', {})
        
        if not keypoints:
            # Fallback to basic visualization if all_keypoints not available
            return self._visualize_arms_only(frame, pose_data)
        
        # Define skeleton connections (COCO format)
        connections = [
            # Face
            ("nose", "left_eye"),
            ("nose", "right_eye"),
            ("left_eye", "left_ear"),
            ("right_eye", "right_ear"),
            # Upper body
            ("left_shoulder", "right_shoulder"),
            ("left_shoulder", "left_elbow"),
            ("left_elbow", "left_wrist"),
            ("right_shoulder", "right_elbow"),
            ("right_elbow", "right_wrist"),
            # Torso
            ("left_shoulder", "left_hip"),
            ("right_shoulder", "right_hip"),
            ("left_hip", "right_hip"),
            # Lower body
            ("left_hip", "left_knee"),
            ("left_knee", "left_ankle"),
            ("right_hip", "right_knee"),
            ("right_knee", "right_ankle"),
        ]
        
        # Draw skeleton connections
        for start_name, end_name in connections:
            start_kp = keypoints.get(start_name)
            end_kp = keypoints.get(end_name)
            
            if start_kp and end_kp and start_kp.confidence > 0.3 and end_kp.confidence > 0.3:
                cv2.line(frame,
                        (int(start_kp.x), int(start_kp.y)),
                        (int(end_kp.x), int(end_kp.y)),
                        color, 2)
        
        # Draw keypoints
        for name, kp in keypoints.items():
            if kp and kp.confidence > 0.3:
                # Different colors for different body parts
                if "wrist" in name:
                    point_color = (0, 255, 255)  # Yellow for wrists
                    radius = 6
                elif "elbow" in name or "knee" in name:
                    point_color = color  # Player color for joints
                    radius = 5
                elif "shoulder" in name or "hip" in name:
                    point_color = (255, 255, 0)  # Cyan for core
                    radius = 5
                else:
                    point_color = (255, 255, 255)  # White for other points
                    radius = 4
                
                cv2.circle(frame, (int(kp.x), int(kp.y)), radius, point_color, -1)
        
        # Draw player ID label near head
        nose_kp = keypoints.get("nose")
        if nose_kp and nose_kp.confidence > 0.3:
            label_x = int(nose_kp.x)
            label_y = int(nose_kp.y) - 20
        else:
            # Fallback to shoulder if nose not detected
            shoulder_kp = keypoints.get("left_shoulder") or keypoints.get("right_shoulder")
            if shoulder_kp:
                label_x = int(shoulder_kp.x)
                label_y = int(shoulder_kp.y) - 30
            else:
                return frame
        
        cv2.putText(frame, player_name, 
                   (label_x - 50, label_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame
    
    def _visualize_arms_only(self, frame: np.ndarray, pose_data: PoseData) -> np.ndarray:
        """
        Fallback visualization - draw simplified arm skeleton (only wrists and elbows).
        
        Args:
            frame: Input frame
            pose_data: PoseData object to visualize
            
        Returns:
            Frame with pose visualization
        """
        # Color based on player ID
        color = (0, 255, 0) if pose_data.player_id == 0 else (255, 0, 0)
        player_name = f"Player {pose_data.player_id}"
        
        # Draw left arm
        if pose_data.left_wrist and pose_data.left_elbow:
            if pose_data.left_wrist.confidence > 0.3 and pose_data.left_elbow.confidence > 0.3:
                # Draw elbow
                cv2.circle(frame, (int(pose_data.left_elbow.x), int(pose_data.left_elbow.y)), 
                          8, color, -1)
                # Draw wrist
                cv2.circle(frame, (int(pose_data.left_wrist.x), int(pose_data.left_wrist.y)), 
                          8, (0, 255, 255), -1)  # Yellow for wrists
                # Draw connection
                cv2.line(frame,
                        (int(pose_data.left_elbow.x), int(pose_data.left_elbow.y)),
                        (int(pose_data.left_wrist.x), int(pose_data.left_wrist.y)),
                        color, 3)
                # Draw angle text
                if pose_data.left_arm_angle is not None:
                    mid_x = int((pose_data.left_elbow.x + pose_data.left_wrist.x) / 2)
                    mid_y = int((pose_data.left_elbow.y + pose_data.left_wrist.y) / 2)
                    cv2.putText(frame, f"L:{pose_data.left_arm_angle:.0f}°", 
                               (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.5, (255, 255, 255), 2)
        
        # Draw right arm
        if pose_data.right_wrist and pose_data.right_elbow:
            if pose_data.right_wrist.confidence > 0.3 and pose_data.right_elbow.confidence > 0.3:
                # Draw elbow
                cv2.circle(frame, (int(pose_data.right_elbow.x), int(pose_data.right_elbow.y)), 
                          8, color, -1)
                # Draw wrist
                cv2.circle(frame, (int(pose_data.right_wrist.x), int(pose_data.right_wrist.y)), 
                          8, (0, 255, 255), -1)  # Yellow for wrists
                # Draw connection
                cv2.line(frame,
                        (int(pose_data.right_elbow.x), int(pose_data.right_elbow.y)),
                        (int(pose_data.right_wrist.x), int(pose_data.right_wrist.y)),
                        color, 3)
                # Draw angle text
                if pose_data.right_arm_angle is not None:
                    mid_x = int((pose_data.right_elbow.x + pose_data.right_wrist.x) / 2)
                    mid_y = int((pose_data.right_elbow.y + pose_data.right_wrist.y) / 2)
                    cv2.putText(frame, f"R:{pose_data.right_arm_angle:.0f}°", 
                               (mid_x, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.5, (255, 255, 255), 2)
        
        # Draw player ID label
        if pose_data.left_elbow or pose_data.right_elbow:
            # Position label near one of the elbows
            label_y = int(pose_data.left_elbow.y if pose_data.left_elbow else pose_data.right_elbow.y)
            label_x = int(pose_data.left_elbow.x if pose_data.left_elbow else pose_data.right_elbow.x)
            cv2.putText(frame, player_name, 
                       (label_x - 50, label_y - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame
