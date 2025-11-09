"""
Game analyzer for PaddleCoach - performs biomechanical analysis on processed videos.
Inspired by analyze_game.py with optimizations for the vision system.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from ultralytics import YOLO
import cv2
from pathlib import Path
from datetime import datetime


# --- YOLOv11 Keypoint Mappings (Standard COCO 17-point setup) ---
KP = {
    'NOSE': 0, 'LEFT_EYE': 1, 'RIGHT_EYE': 2, 'LEFT_EAR': 3, 'RIGHT_EAR': 4,
    'LEFT_SHOULDER': 5, 'RIGHT_SHOULDER': 6,
    'LEFT_ELBOW': 7, 'RIGHT_ELBOW': 8, 'LEFT_WRIST': 9, 'RIGHT_WRIST': 10,
    'LEFT_HIP': 11, 'RIGHT_HIP': 12,
    'LEFT_KNEE': 13, 'RIGHT_KNEE': 14, 'LEFT_ANKLE': 15, 'RIGHT_ANKLE': 16,
}


class GameAnalyzer:
    """
    Analyzes table tennis game videos to extract biomechanical metrics.
    """
    
    def __init__(self, output_dir: str = "analysis_output"):
        """
        Initialize the game analyzer.
        
        Args:
            output_dir: Directory to save analysis output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Load YOLOv11 pose model
        self.model = YOLO("yolo11n-pose.pt")
        
    def load_pose_data_from_video(self, video_path: str, fps: int = 30) -> pd.DataFrame:
        """
        Loads pose data from a video file using YOLOv11 pose detection.
        
        Args:
            video_path: Path to the video file
            fps: Frames per second for velocity calculations
            
        Returns:
            DataFrame with columns: 'frame', 'player_id', and keypoint coordinates
        """
        print(f"\n{'='*60}")
        print(f"Loading pose data from: {video_path}")
        print(f"{'='*60}")
        
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"Error: Could not open video file at {video_path}")
            return pd.DataFrame()
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"Video FPS: {video_fps:.2f}")
        print(f"Total frames: {total_frames}")
        print(f"Processing frames...")
        
        all_data = []
        frame_num = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_num += 1
            
            # Run pose detection
            results = self.model.predict(source=frame, conf=0.5, classes=0, verbose=False)
            
            # Extract keypoints for each detected person
            if results[0].keypoints is not None and len(results[0].keypoints.xy) > 0:
                keypoints = results[0].keypoints.xy.cpu().numpy()
                
                for person_idx, person_kpts in enumerate(keypoints):
                    # Assign player IDs based on position (left vs right side of frame)
                    avg_x = np.mean([kpt[0] for kpt in person_kpts if kpt[0] > 0])
                    player_id = 'Player_1' if avg_x < frame.shape[1] / 2 else 'Player_2'
                    
                    # Create a row with frame number, player ID, and all keypoints
                    row_data = {
                        'frame': frame_num,
                        'player_id': player_id,
                        'timestamp': frame_num / fps,
                    }
                    
                    # Add keypoint coordinates
                    for i in range(17):
                        if i < len(person_kpts):
                            row_data[f'x{i}'] = person_kpts[i][0]
                            row_data[f'y{i}'] = person_kpts[i][1]
                        else:
                            row_data[f'x{i}'] = 0.0
                            row_data[f'y{i}'] = 0.0
                    
                    all_data.append(row_data)
            
            # Progress indicator
            if frame_num % 100 == 0:
                progress = (frame_num / total_frames) * 100
                print(f"  Progress: {progress:.1f}% ({frame_num}/{total_frames} frames)")
        
        cap.release()
        
        df = pd.DataFrame(all_data)
        print(f"\nLoaded {len(df)} pose detections from {frame_num} frames")
        
        return df.sort_values(by=['frame', 'player_id']).reset_index(drop=True)
    
    @staticmethod
    def calculate_angle(p1: Tuple[float, float], p2: Tuple[float, float], 
                       p3: Tuple[float, float]) -> float:
        """
        Calculates the angle (in degrees) formed by three points (p1-p2-p3).
        
        Args:
            p1: First point (x, y)
            p2: Vertex point (x, y)
            p3: Third point (x, y)
            
        Returns:
            Angle in degrees
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)

        v1 = p1 - p2
        v2 = p3 - p2

        # Handle cases where points are identical to avoid division by zero
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0

        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        angle_rad = np.arccos(cosine_angle)
        return np.degrees(angle_rad)
    
    @staticmethod
    def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """
        Calculates the Euclidean distance between two points.
        
        Args:
            p1: First point (x, y)
            p2: Second point (x, y)
            
        Returns:
            Distance in pixels
        """
        return np.linalg.norm(np.array(p1) - np.array(p2))
    
    @staticmethod
    def calculate_velocity(current_pos: Tuple[float, float], prev_pos: Tuple[float, float], 
                          fps: int = 30) -> float:
        """
        Calculates the linear speed (in pixels/sec) between two frames.
        
        Args:
            current_pos: Current position (x, y)
            prev_pos: Previous position (x, y)
            fps: Frames per second
            
        Returns:
            Velocity in pixels/second
        """
        distance = GameAnalyzer.calculate_distance(current_pos, prev_pos)
        velocity = distance * fps
        return velocity
    
    @staticmethod
    def calculate_center_of_gravity(row: pd.Series) -> Tuple[float, float]:
        """
        Estimates the body's Center of Gravity (CoG) from torso and leg keypoints.
        
        Args:
            row: DataFrame row with keypoint data
            
        Returns:
            Center of gravity (x, y) coordinates
        """
        keypoints = [
            (row[f'x{KP["LEFT_SHOULDER"]}'], row[f'y{KP["LEFT_SHOULDER"]}']),
            (row[f'x{KP["RIGHT_SHOULDER"]}'], row[f'y{KP["RIGHT_SHOULDER"]}']),
            (row[f'x{KP["LEFT_HIP"]}'], row[f'y{KP["LEFT_HIP"]}']),
            (row[f'x{KP["RIGHT_HIP"]}'], row[f'y{KP["RIGHT_HIP"]}']),
            (row[f'x{KP["LEFT_KNEE"]}'], row[f'y{KP["LEFT_KNEE"]}']),
            (row[f'x{KP["RIGHT_KNEE"]}'], row[f'y{KP["RIGHT_KNEE"]}']),
        ]
        
        # Filter out zeros (non-detected points)
        valid_x = [x for x, y in keypoints if x > 0]
        valid_y = [y for x, y in keypoints if y > 0]

        if not valid_x or not valid_y:
            return (0.0, 0.0)

        return (sum(valid_x) / len(valid_x), sum(valid_y) / len(valid_y))
    
    def detect_shots(self, df: pd.DataFrame, player_id: str, 
                    velocity_threshold: float = 1000.0, fps: int = 30) -> List[Tuple[int, int, str]]:
        """
        Detects potential shots based on wrist velocity spikes.
        
        Args:
            df: DataFrame with pose data
            player_id: Player identifier
            velocity_threshold: Minimum velocity to detect a shot
            fps: Frames per second
            
        Returns:
            List of (start_frame, end_frame, shot_type) tuples
        """
        player_df = df[df['player_id'] == player_id].copy()
        
        if player_df.empty:
            return []
        
        # Calculate wrist velocity for both wrists
        for wrist in ['LEFT_WRIST', 'RIGHT_WRIST']:
            wrist_idx = KP[wrist]
            player_df[f'prev_x_{wrist}'] = player_df[f'x{wrist_idx}'].shift(1)
            player_df[f'prev_y_{wrist}'] = player_df[f'y{wrist_idx}'].shift(1)
            
            player_df[f'velocity_{wrist}'] = player_df.apply(
                lambda row: self.calculate_velocity(
                    (row[f'x{wrist_idx}'], row[f'y{wrist_idx}']),
                    (row[f'prev_x_{wrist}'], row[f'prev_y_{wrist}']),
                    fps=fps
                ) if not pd.isna(row[f'prev_x_{wrist}']) else 0, axis=1
            )
        
        # Use the maximum of both wrists
        player_df['max_wrist_velocity'] = player_df[['velocity_LEFT_WRIST', 'velocity_RIGHT_WRIST']].max(axis=1)
        
        # Find velocity spikes (potential shots)
        shots = []
        in_shot = False
        shot_start = 0
        
        for idx, row in player_df.iterrows():
            if row['max_wrist_velocity'] > velocity_threshold and not in_shot:
                # Start of a shot
                in_shot = True
                shot_start = row['frame']
            elif row['max_wrist_velocity'] <= velocity_threshold * 0.5 and in_shot:
                # End of a shot
                in_shot = False
                shot_end = row['frame']
                
                # Classify shot type based on arm used
                shot_start_data = player_df[player_df['frame'] == shot_start]
                if not shot_start_data.empty:
                    if shot_start_data['velocity_RIGHT_WRIST'].values[0] > \
                       shot_start_data['velocity_LEFT_WRIST'].values[0]:
                        shot_type = "Forehand"
                    else:
                        shot_type = "Backhand"
                    
                    shots.append((shot_start, shot_end, shot_type))
        
        return shots
    
    def analyze_stroke_metrics(self, df: pd.DataFrame, player_id: str, 
                               rally_start: int, rally_end: int, fps: int = 30) -> Dict[str, float]:
        """
        Calculates key biomechanical metrics for a player during a stroke/rally phase.
        
        Args:
            df: DataFrame with pose data
            player_id: Player identifier
            rally_start: Start frame of rally
            rally_end: End frame of rally
            fps: Frames per second
            
        Returns:
            Dictionary of biomechanical metrics
        """
        rally_df = df[(df['player_id'] == player_id) & 
                     (df['frame'] >= rally_start) & 
                     (df['frame'] <= rally_end)].copy()
        
        if rally_df.empty:
            return {}

        # Calculate wrist velocities
        for wrist_name, wrist_key in [('RIGHT_WRIST', KP['RIGHT_WRIST']), 
                                      ('LEFT_WRIST', KP['LEFT_WRIST'])]:
            wrist_col_x = f'x{wrist_key}'
            wrist_col_y = f'y{wrist_key}'
            
            rally_df[f'prev_x_{wrist_name}'] = rally_df[wrist_col_x].shift(1)
            rally_df[f'prev_y_{wrist_name}'] = rally_df[wrist_col_y].shift(1)
            
            rally_df[f'wrist_velocity_{wrist_name}'] = rally_df.apply(
                lambda row: self.calculate_velocity(
                    (row[wrist_col_x], row[wrist_col_y]),
                    (row[f'prev_x_{wrist_name}'], row[f'prev_y_{wrist_name}']),
                    fps=fps
                ) if not pd.isna(row[f'prev_x_{wrist_name}']) else 0, axis=1
            )
        
        # Use the maximum of both wrists
        rally_df['wrist_velocity'] = rally_df[['wrist_velocity_RIGHT_WRIST', 
                                                'wrist_velocity_LEFT_WRIST']].max(axis=1)

        # Calculate hip/knee angles
        hip_angle_col = []
        elbow_angle_col = []
        shoulder_hip_angle_col = []
        
        for _, row in rally_df.iterrows():
            # Right leg angle (ankle-knee-hip)
            p1 = (row[f'x{KP["RIGHT_ANKLE"]}'], row[f'y{KP["RIGHT_ANKLE"]}'])
            p2 = (row[f'x{KP["RIGHT_KNEE"]}'], row[f'y{KP["RIGHT_KNEE"]}'])
            p3 = (row[f'x{KP["RIGHT_HIP"]}'], row[f'y{KP["RIGHT_HIP"]}'])
            hip_angle_col.append(self.calculate_angle(p1, p2, p3))
            
            # Right arm angle (wrist-elbow-shoulder)
            p1 = (row[f'x{KP["RIGHT_WRIST"]}'], row[f'y{KP["RIGHT_WRIST"]}'])
            p2 = (row[f'x{KP["RIGHT_ELBOW"]}'], row[f'y{KP["RIGHT_ELBOW"]}'])
            p3 = (row[f'x{KP["RIGHT_SHOULDER"]}'], row[f'y{KP["RIGHT_SHOULDER"]}'])
            elbow_angle_col.append(self.calculate_angle(p1, p2, p3))
            
            # Torso angle (shoulder-hip-knee)
            p1 = (row[f'x{KP["RIGHT_SHOULDER"]}'], row[f'y{KP["RIGHT_SHOULDER"]}'])
            p2 = (row[f'x{KP["RIGHT_HIP"]}'], row[f'y{KP["RIGHT_HIP"]}'])
            p3 = (row[f'x{KP["RIGHT_KNEE"]}'], row[f'y{KP["RIGHT_KNEE"]}'])
            shoulder_hip_angle_col.append(self.calculate_angle(p1, p2, p3))
        
        rally_df['hip_knee_angle'] = hip_angle_col
        rally_df['elbow_angle'] = elbow_angle_col
        rally_df['torso_angle'] = shoulder_hip_angle_col

        # Calculate Center of Gravity
        cog_results = rally_df.apply(self.calculate_center_of_gravity, axis=1)
        rally_df['cog_x'] = [x for x, y in cog_results]
        rally_df['cog_y'] = [y for x, y in cog_results]

        # Compile metrics
        metrics = {
            'max_racket_velocity': rally_df['wrist_velocity'].max(),
            'avg_racket_velocity': rally_df['wrist_velocity'].mean(),
            'min_hip_knee_angle': rally_df['hip_knee_angle'].min(),
            'avg_hip_knee_angle': rally_df['hip_knee_angle'].mean(),
            'min_elbow_angle': rally_df['elbow_angle'].min(),
            'avg_elbow_angle': rally_df['elbow_angle'].mean(),
            'avg_torso_angle': rally_df['torso_angle'].mean(),
            'cog_x_movement': rally_df['cog_x'].max() - rally_df['cog_x'].min(),
            'cog_y_movement': rally_df['cog_y'].max() - rally_df['cog_y'].min(),
        }
        
        return metrics
    
    def generate_analysis_report(self, video_path: str, 
                                 velocity_threshold: float = 1000.0,
                                 fps: int = 30) -> str:
        """
        Generates a comprehensive analysis report for a video.
        
        Args:
            video_path: Path to the video file
            velocity_threshold: Minimum velocity to detect shots
            fps: Frames per second
            
        Returns:
            Path to the generated report file
        """
        # Load pose data from video
        df_pose = self.load_pose_data_from_video(video_path, fps)
        
        if df_pose.empty:
            print("Error: No pose data loaded. Cannot generate report.")
            return ""
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_name = Path(video_path).stem
        report_path = self.output_dir / f"analysis_{video_name}_{timestamp}.txt"
        
        with open(report_path, 'w') as f:
            # Header
            f.write("="*70 + "\n")
            f.write("         PADDLECOACH - TABLE TENNIS BIOMECHANICAL ANALYSIS\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Video: {video_path}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Processing FPS: {fps}\n")
            f.write(f"Total Frames Analyzed: {df_pose['frame'].max()}\n")
            f.write(f"Total Detections: {len(df_pose)}\n\n")
            
            # Get unique players
            players = df_pose['player_id'].unique()
            f.write(f"Detected Players: {', '.join(players)}\n")
            f.write(f"Number of Players: {len(players)}\n\n")
            
            # Shot detection and analysis for each player
            f.write("="*70 + "\n")
            f.write("                           SHOT DETECTION\n")
            f.write("="*70 + "\n\n")
            
            all_shots = {}
            for player in players:
                shots = self.detect_shots(df_pose, player, velocity_threshold, fps)
                all_shots[player] = shots
                
                f.write(f"{player}:\n")
                f.write(f"  Total Shots Detected: {len(shots)}\n\n")
                
                if shots:
                    forehand_count = sum(1 for _, _, shot_type in shots if shot_type == "Forehand")
                    backhand_count = sum(1 for _, _, shot_type in shots if shot_type == "Backhand")
                    
                    f.write(f"  Forehand Shots: {forehand_count}\n")
                    f.write(f"  Backhand Shots: {backhand_count}\n\n")
                    
                    # Show first 10 shots
                    f.write(f"  Shot Details (first 10):\n")
                    for i, (start, end, shot_type) in enumerate(shots[:10], 1):
                        duration = (end - start) / fps
                        f.write(f"    {i}. {shot_type:10s} | Frames {start:5d}-{end:5d} | Duration: {duration:.2f}s\n")
                    
                    if len(shots) > 10:
                        f.write(f"    ... and {len(shots) - 10} more shots\n")
                    f.write("\n")
            
            # Biomechanical analysis
            f.write("="*70 + "\n")
            f.write("                      BIOMECHANICAL ANALYSIS\n")
            f.write("="*70 + "\n\n")
            
            for player in players:
                shots = all_shots[player]
                if not shots:
                    f.write(f"{player}: No shots detected\n\n")
                    continue
                
                f.write(f"{player} - Detailed Stroke Metrics:\n")
                f.write("-"*70 + "\n\n")
                
                # Analyze up to 5 shots
                for i, (start, end, shot_type) in enumerate(shots[:5], 1):
                    metrics = self.analyze_stroke_metrics(df_pose, player, start, end, fps)
                    
                    if not metrics:
                        continue
                    
                    f.write(f"  Shot {i}: {shot_type} (Frames {start}-{end})\n")
                    f.write(f"    Racket Metrics:\n")
                    f.write(f"      Max Velocity:     {metrics['max_racket_velocity']:8.2f} px/s\n")
                    f.write(f"      Avg Velocity:     {metrics['avg_racket_velocity']:8.2f} px/s\n")
                    f.write(f"    Joint Angles:\n")
                    f.write(f"      Min Hip/Knee:     {metrics['min_hip_knee_angle']:8.2f}° (lower = better loading)\n")
                    f.write(f"      Avg Hip/Knee:     {metrics['avg_hip_knee_angle']:8.2f}°\n")
                    f.write(f"      Min Elbow:        {metrics['min_elbow_angle']:8.2f}°\n")
                    f.write(f"      Avg Elbow:        {metrics['avg_elbow_angle']:8.2f}°\n")
                    f.write(f"      Avg Torso:        {metrics['avg_torso_angle']:8.2f}°\n")
                    f.write(f"    Center of Gravity:\n")
                    f.write(f"      Horizontal Movement: {metrics['cog_x_movement']:8.2f} px\n")
                    f.write(f"      Vertical Movement:   {metrics['cog_y_movement']:8.2f} px\n")
                    f.write("\n")
            
            # Player comparison
            if len(players) == 2:
                f.write("="*70 + "\n")
                f.write("                        PLAYER COMPARISON\n")
                f.write("="*70 + "\n\n")
                
                player1, player2 = players[0], players[1]
                shots1, shots2 = all_shots[player1], all_shots[player2]
                
                f.write(f"Shot Count:\n")
                f.write(f"  {player1}: {len(shots1)} shots\n")
                f.write(f"  {player2}: {len(shots2)} shots\n\n")
                
                # Calculate average metrics across all shots
                avg_metrics = {}
                for player in players:
                    player_shots = all_shots[player]
                    if not player_shots:
                        continue
                    
                    all_velocities = []
                    all_angles = []
                    all_elbow_angles = []
                    all_cog_movements = []
                    
                    for start, end, _ in player_shots:
                        metrics = self.analyze_stroke_metrics(df_pose, player, start, end, fps)
                        if metrics:
                            all_velocities.append(metrics['max_racket_velocity'])
                            all_angles.append(metrics['min_hip_knee_angle'])
                            all_elbow_angles.append(metrics['min_elbow_angle'])
                            all_cog_movements.append(metrics['cog_x_movement'])
                    
                    if all_velocities:
                        avg_metrics[player] = {
                            'avg_velocity': np.mean(all_velocities),
                            'avg_angle': np.mean(all_angles),
                            'avg_elbow': np.mean(all_elbow_angles),
                            'avg_cog': np.mean(all_cog_movements),
                        }
                
                if len(avg_metrics) == 2:
                    f.write("Average Performance Metrics:\n\n")
                    for player in players:
                        if player in avg_metrics:
                            f.write(f"{player}:\n")
                            f.write(f"  Avg Max Racket Velocity: {avg_metrics[player]['avg_velocity']:8.2f} px/s\n")
                            f.write(f"  Avg Min Hip/Knee Angle:  {avg_metrics[player]['avg_angle']:8.2f}°\n")
                            f.write(f"  Avg Min Elbow Angle:     {avg_metrics[player]['avg_elbow']:8.2f}°\n")
                            f.write(f"  Avg CoG Movement:        {avg_metrics[player]['avg_cog']:8.2f} px\n\n")
                    
                    # Performance comparison
                    f.write("-"*70 + "\n")
                    f.write("Performance Edge:\n\n")
                    
                    p1_velocity = avg_metrics[player1]['avg_velocity']
                    p2_velocity = avg_metrics[player2]['avg_velocity']
                    
                    if p1_velocity > p2_velocity:
                        diff = (p1_velocity - p2_velocity) / p2_velocity * 100
                        f.write(f"  {player1} has {diff:.1f}% faster average racket speed\n")
                    else:
                        diff = (p2_velocity - p1_velocity) / p1_velocity * 100
                        f.write(f"  {player2} has {diff:.1f}% faster average racket speed\n")
            
            # Footer
            f.write("\n" + "="*70 + "\n")
            f.write("                        ANALYSIS COMPLETE\n")
            f.write("="*70 + "\n")
            f.write(f"\nReport generated by PaddleCoach Vision System v1.0\n")
            f.write(f"Output file: {report_path}\n")
        
        print(f"\n{'='*60}")
        print(f"Analysis report generated: {report_path}")
        print(f"{'='*60}")
        
        return str(report_path)


def main():
    """Main function for standalone usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python game_analyzer.py <video_path> [fps] [velocity_threshold]")
        print("\nExample:")
        print("  python game_analyzer.py output/output_dataDetection.mp4")
        print("  python game_analyzer.py output/output_dataDetection.mp4 30 1000")
        return
    
    video_path = sys.argv[1]
    fps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    velocity_threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 1000.0
    
    if not Path(video_path).exists():
        print(f"Error: Video file not found: {video_path}")
        return
    
    print("\n" + "="*60)
    print("  PaddleCoach - Game Analysis System")
    print("="*60)
    
    analyzer = GameAnalyzer()
    report_path = analyzer.generate_analysis_report(
        video_path=video_path,
        velocity_threshold=velocity_threshold,
        fps=fps
    )
    
    if report_path:
        print(f"\n✅ Analysis complete! Report saved to:")
        print(f"   {report_path}")
        print("\nYou can view the report by opening the .txt file.")
    else:
        print("\n❌ Analysis failed. Please check the video file and try again.")


if __name__ == "__main__":
    main()
