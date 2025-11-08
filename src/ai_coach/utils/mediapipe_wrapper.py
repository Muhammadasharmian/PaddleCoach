"""
MediaPipe Pose Estimation Wrapper
Handles pose detection and keypoint extraction from videos and images.
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import mediapipe as mp


class MediaPipeWrapper:
    """Wrapper for MediaPipe pose estimation functionality."""
    
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize MediaPipe pose detector.
        
        Args:
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def extract_pose_from_frame(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Extract pose landmarks from a single frame.
        
        Args:
            frame: BGR image frame from OpenCV
            
        Returns:
            Dictionary containing keypoints and angles, or None if no pose detected
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            return None
            
        # Extract keypoints
        keypoints = self._extract_keypoints(results.pose_landmarks)
        
        # Calculate important angles
        angles = self._calculate_angles(keypoints)
        
        return {
            'keypoints': keypoints,
            'angles': angles,
            'landmarks': results.pose_landmarks
        }
    
    def extract_pose_from_video(self, video_path: str) -> List[Dict]:
        """
        Extract pose data from entire video.
        
        Args:
            video_path: Path to video file
            
        Returns:
            List of pose data dictionaries for each frame
        """
        cap = cv2.VideoCapture(video_path)
        pose_data = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            pose = self.extract_pose_from_frame(frame)
            if pose:
                pose['frame_number'] = frame_count
                pose['timestamp'] = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                pose_data.append(pose)
                
            frame_count += 1
            
        cap.release()
        return pose_data
    
    def _extract_keypoints(self, landmarks) -> Dict[str, Tuple[float, float, float]]:
        """Extract key body points as (x, y, z) coordinates."""
        keypoints = {}
        
        # Map important landmarks
        landmark_names = {
            'nose': self.mp_pose.PoseLandmark.NOSE,
            'left_shoulder': self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            'right_shoulder': self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            'left_elbow': self.mp_pose.PoseLandmark.LEFT_ELBOW,
            'right_elbow': self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            'left_wrist': self.mp_pose.PoseLandmark.LEFT_WRIST,
            'right_wrist': self.mp_pose.PoseLandmark.RIGHT_WRIST,
            'left_hip': self.mp_pose.PoseLandmark.LEFT_HIP,
            'right_hip': self.mp_pose.PoseLandmark.RIGHT_HIP,
            'left_knee': self.mp_pose.PoseLandmark.LEFT_KNEE,
            'right_knee': self.mp_pose.PoseLandmark.RIGHT_KNEE,
            'left_ankle': self.mp_pose.PoseLandmark.LEFT_ANKLE,
            'right_ankle': self.mp_pose.PoseLandmark.RIGHT_ANKLE,
        }
        
        for name, landmark_id in landmark_names.items():
            lm = landmarks.landmark[landmark_id]
            keypoints[name] = (lm.x, lm.y, lm.z)
            
        return keypoints
    
    def _calculate_angles(self, keypoints: Dict) -> Dict[str, float]:
        """Calculate important body angles for ping pong analysis."""
        angles = {}
        
        # Shoulder angle (left side)
        if all(k in keypoints for k in ['left_hip', 'left_shoulder', 'left_elbow']):
            angles['left_shoulder'] = self._angle_between_points(
                keypoints['left_hip'],
                keypoints['left_shoulder'],
                keypoints['left_elbow']
            )
        
        # Shoulder angle (right side)
        if all(k in keypoints for k in ['right_hip', 'right_shoulder', 'right_elbow']):
            angles['right_shoulder'] = self._angle_between_points(
                keypoints['right_hip'],
                keypoints['right_shoulder'],
                keypoints['right_elbow']
            )
        
        # Elbow angle (left)
        if all(k in keypoints for k in ['left_shoulder', 'left_elbow', 'left_wrist']):
            angles['left_elbow'] = self._angle_between_points(
                keypoints['left_shoulder'],
                keypoints['left_elbow'],
                keypoints['left_wrist']
            )
        
        # Elbow angle (right)
        if all(k in keypoints for k in ['right_shoulder', 'right_elbow', 'right_wrist']):
            angles['right_elbow'] = self._angle_between_points(
                keypoints['right_shoulder'],
                keypoints['right_elbow'],
                keypoints['right_wrist']
            )
        
        # Hip angle (left)
        if all(k in keypoints for k in ['left_shoulder', 'left_hip', 'left_knee']):
            angles['left_hip'] = self._angle_between_points(
                keypoints['left_shoulder'],
                keypoints['left_hip'],
                keypoints['left_knee']
            )
        
        # Hip angle (right)
        if all(k in keypoints for k in ['right_shoulder', 'right_hip', 'right_knee']):
            angles['right_hip'] = self._angle_between_points(
                keypoints['right_shoulder'],
                keypoints['right_hip'],
                keypoints['right_knee']
            )
        
        # Knee angle (left)
        if all(k in keypoints for k in ['left_hip', 'left_knee', 'left_ankle']):
            angles['left_knee'] = self._angle_between_points(
                keypoints['left_hip'],
                keypoints['left_knee'],
                keypoints['left_ankle']
            )
        
        # Knee angle (right)
        if all(k in keypoints for k in ['right_hip', 'right_knee', 'right_ankle']):
            angles['right_knee'] = self._angle_between_points(
                keypoints['right_hip'],
                keypoints['right_knee'],
                keypoints['right_ankle']
            )
        
        # Body rotation (shoulder line angle)
        if all(k in keypoints for k in ['left_shoulder', 'right_shoulder']):
            left = keypoints['left_shoulder']
            right = keypoints['right_shoulder']
            angles['shoulder_rotation'] = np.degrees(np.arctan2(
                right[1] - left[1],
                right[0] - left[0]
            ))
        
        return angles
    
    @staticmethod
    def _angle_between_points(p1: Tuple, p2: Tuple, p3: Tuple) -> float:
        """
        Calculate angle at point p2 formed by p1-p2-p3.
        
        Args:
            p1, p2, p3: Points as (x, y, z) tuples
            
        Returns:
            Angle in degrees
        """
        # Convert to numpy arrays
        p1 = np.array(p1[:2])  # Use only x, y
        p2 = np.array(p2[:2])
        p3 = np.array(p3[:2])
        
        # Calculate vectors
        v1 = p1 - p2
        v2 = p3 - p2
        
        # Calculate angle
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def draw_pose_on_frame(self, frame: np.ndarray, pose_data: Dict) -> np.ndarray:
        """
        Draw pose landmarks on frame for visualization.
        
        Args:
            frame: BGR image frame
            pose_data: Pose data dictionary from extract_pose_from_frame
            
        Returns:
            Frame with pose drawn on it
        """
        if 'landmarks' in pose_data and pose_data['landmarks']:
            self.mp_drawing.draw_landmarks(
                frame,
                pose_data['landmarks'],
                self.mp_pose.POSE_CONNECTIONS
            )
        return frame
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'pose'):
            self.pose.close()
