"""
Module 3A: Pro Comparison Module
Offline analysis comparing user technique to professional players.

This module:
1. Takes video of user and pro player
2. Extracts pose data from both using MediaPipe
3. Compares the poses using Gemini AI
4. Provides detailed, actionable feedback
"""

import os
from typing import Dict, List, Optional, Tuple
from .utils import MediaPipeWrapper, GeminiClient
from .mock_models import PoseData
from .ai_interface import IAnalyticsData, MockAnalyticsData, IAICoachingModule


class ProComparisonModule(IAICoachingModule):
    """
    Compares user's technique with professional players.
    Provides detailed analysis of differences in body mechanics.
    """
    
    def __init__(
        self, 
        analytics_interface: Optional[IAnalyticsData] = None,
        gemini_api_key: Optional[str] = None
    ):
        """
        Initialize Pro Comparison module.
        
        Args:
            analytics_interface: Interface to access game data
            gemini_api_key: Gemini API key for analysis
        """
        self.analytics = analytics_interface or MockAnalyticsData()
        self.mediapipe = MediaPipeWrapper()
        self.gemini = GeminiClient(api_key=gemini_api_key)
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize the module and check dependencies."""
        try:
            # Test MediaPipe
            import mediapipe as mp
            
            # Test Gemini (will work in mock mode if no API key)
            status = self.gemini.generate_technique_description("test", [])
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get current status of the module."""
        return {
            "module": "ProComparison",
            "initialized": self.initialized,
            "mediapipe_available": self.mediapipe is not None,
            "gemini_available": self.gemini is not None
        }
    
    def compare_techniques(
        self,
        user_video_path: str,
        pro_video_path: str,
        shot_type: str = "forehand",
        output_report: Optional[str] = None
    ) -> Dict:
        """
        Compare user's technique with professional.
        
        Args:
            user_video_path: Path to user's video
            pro_video_path: Path to professional's video
            shot_type: Type of shot being compared
            output_report: Optional path to save detailed report
            
        Returns:
            Comparison results dictionary
        """
        print(f"\n🎯 Starting Pro Comparison Analysis")
        print(f"User video: {user_video_path}")
        print(f"Pro video: {pro_video_path}")
        print(f"Shot type: {shot_type}")
        
        # Step 1: Extract pose data from both videos
        print("\n📊 Extracting pose data from videos...")
        user_poses = self._extract_poses_from_video(user_video_path)
        pro_poses = self._extract_poses_from_video(pro_video_path)
        
        if not user_poses or not pro_poses:
            return {
                "status": "error",
                "error": "Could not extract pose data from one or both videos"
            }
        
        print(f"✅ Extracted {len(user_poses)} user poses and {len(pro_poses)} pro poses")
        
        # Step 2: Find key frames (e.g., contact point, follow-through)
        print("\n🔍 Identifying key frames...")
        user_key_frames = self._identify_key_frames(user_poses)
        pro_key_frames = self._identify_key_frames(pro_poses)
        
        # Step 3: Compare poses at key frames
        print("\n⚖️ Comparing poses...")
        comparisons = self._compare_pose_sequences(
            user_key_frames, 
            pro_key_frames
        )
        
        # Step 4: Generate AI analysis
        print("\n🤖 Generating AI analysis...")
        analysis = self._generate_analysis(
            comparisons,
            shot_type
        )
        
        # Step 5: Create result dictionary
        result = {
            "status": "success",
            "shot_type": shot_type,
            "user_video": user_video_path,
            "pro_video": pro_video_path,
            "key_differences": comparisons,
            "ai_analysis": analysis,
            "recommendations": self._prioritize_recommendations(comparisons)
        }
        
        # Save report if requested
        if output_report:
            self._save_report(result, output_report)
        
        print("\n✅ Analysis complete!")
        return result
    
    def _extract_poses_from_video(self, video_path: str) -> List[Dict]:
        """Extract pose data from video file."""
        if not os.path.exists(video_path):
            print(f"⚠️ Video file not found: {video_path}")
            # Return mock data for testing
            return self._get_mock_pose_sequence()
        
        try:
            poses = self.mediapipe.extract_pose_from_video(video_path)
            return poses
        except Exception as e:
            print(f"Error extracting poses: {e}")
            return self._get_mock_pose_sequence()
    
    def _identify_key_frames(self, pose_sequence: List[Dict]) -> Dict[str, Dict]:
        """
        Identify key frames in the shot sequence.
        
        Returns dictionary with frames for:
        - ready_position
        - backswing_peak
        - contact_point
        - follow_through
        """
        if not pose_sequence:
            return {}
        
        # Simple heuristic: divide sequence into quarters
        n = len(pose_sequence)
        
        key_frames = {
            "ready_position": pose_sequence[0],
            "backswing_peak": pose_sequence[n // 3] if n >= 3 else pose_sequence[0],
            "contact_point": pose_sequence[n // 2] if n >= 2 else pose_sequence[0],
            "follow_through": pose_sequence[-1]
        }
        
        return key_frames
    
    def _compare_pose_sequences(
        self, 
        user_frames: Dict[str, Dict], 
        pro_frames: Dict[str, Dict]
    ) -> Dict[str, Dict]:
        """
        Compare poses at each key frame.
        
        Returns dictionary with angle differences for each frame.
        """
        comparisons = {}
        
        for frame_name in user_frames.keys():
            if frame_name not in pro_frames:
                continue
            
            user_pose = user_frames[frame_name]
            pro_pose = pro_frames[frame_name]
            
            # Calculate angle differences
            angle_diffs = {}
            user_angles = user_pose.get('angles', {})
            pro_angles = pro_pose.get('angles', {})
            
            for angle_name in user_angles.keys():
                if angle_name in pro_angles:
                    diff = user_angles[angle_name] - pro_angles[angle_name]
                    angle_diffs[angle_name] = {
                        'user': user_angles[angle_name],
                        'pro': pro_angles[angle_name],
                        'difference': diff
                    }
            
            comparisons[frame_name] = {
                'timestamp': {
                    'user': user_pose.get('timestamp', 0),
                    'pro': pro_pose.get('timestamp', 0)
                },
                'angle_differences': angle_diffs
            }
        
        return comparisons
    
    def _generate_analysis(self, comparisons: Dict, shot_type: str) -> str:
        """Generate AI-powered analysis using Gemini."""
        # Prepare simplified data for Gemini
        user_data = {'angles': {}}
        pro_data = {'angles': {}}
        
        # Use contact point as primary comparison
        if 'contact_point' in comparisons:
            contact = comparisons['contact_point']
            for angle_name, data in contact['angle_differences'].items():
                user_data['angles'][angle_name] = data['user']
                pro_data['angles'][angle_name] = data['pro']
        
        # Get AI analysis
        analysis = self.gemini.analyze_pose_comparison(
            user_data,
            pro_data,
            shot_type
        )
        
        return analysis
    
    def _prioritize_recommendations(self, comparisons: Dict) -> List[Dict]:
        """
        Prioritize recommendations based on difference magnitude.
        
        Returns sorted list of recommendations.
        """
        recommendations = []
        
        for frame_name, frame_data in comparisons.items():
            for angle_name, angle_data in frame_data['angle_differences'].items():
                diff = abs(angle_data['difference'])
                
                if diff > 10:  # Significant difference
                    priority = "high" if diff > 20 else "medium"
                    
                    recommendations.append({
                        'frame': frame_name,
                        'joint': angle_name,
                        'difference': angle_data['difference'],
                        'priority': priority,
                        'user_angle': angle_data['user'],
                        'pro_angle': angle_data['pro']
                    })
        
        # Sort by absolute difference
        recommendations.sort(key=lambda x: abs(x['difference']), reverse=True)
        
        return recommendations
    
    def _save_report(self, result: Dict, output_path: str) -> None:
        """Save detailed report to file."""
        import json
        
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        with open(output_path, 'w') as f:
            # Write human-readable report
            f.write("=" * 80 + "\n")
            f.write("PRO COMPARISON ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Shot Type: {result['shot_type']}\n")
            f.write(f"User Video: {result['user_video']}\n")
            f.write(f"Pro Video: {result['pro_video']}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("AI ANALYSIS\n")
            f.write("-" * 80 + "\n")
            f.write(result['ai_analysis'] + "\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("PRIORITIZED RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")
            for i, rec in enumerate(result['recommendations'][:5], 1):
                f.write(f"\n{i}. [{rec['priority'].upper()}] {rec['joint']} at {rec['frame']}\n")
                f.write(f"   Difference: {rec['difference']:+.1f}° ")
                f.write(f"(You: {rec['user_angle']:.1f}°, Pro: {rec['pro_angle']:.1f}°)\n")
            
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("DETAILED DATA (JSON)\n")
            f.write("=" * 80 + "\n")
            json.dump(result, f, indent=2)
        
        print(f"📄 Report saved to: {output_path}")
    
    def _get_mock_pose_sequence(self) -> List[Dict]:
        """Generate mock pose sequence for testing."""
        from .mock_models import create_mock_pose_data
        
        mock_poses = []
        for i in range(10):
            pose = create_mock_pose_data(f"pose_{i:03d}")
            mock_poses.append({
                'timestamp': i * 0.1,
                'frame_number': i,
                'keypoints': pose.keypoints,
                'angles': pose.angles
            })
        
        return mock_poses
