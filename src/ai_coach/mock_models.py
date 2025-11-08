"""
Mock Data Models
These represent the data structures that teammates (Ashwani & Ashar) will provide.
For now, these are simplified versions to enable independent development.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime


@dataclass
class Shot:
    """Represents a single shot in a ping pong game."""
    shotID: str
    timestamp: float
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    speed: float  # km/h
    type: str  # 'forehand', 'backhand', 'serve', etc.
    
    def calculate_speed(self) -> float:
        """Calculate shot speed."""
        return self.speed


@dataclass
class PoseData:
    """Stores skeletal tracking data from pose estimation."""
    poseID: str
    pointID: str
    timestamp: float
    keypoints: Dict[str, Tuple[float, float, float]]  # joint_name -> (x, y, z)
    angles: Dict[str, float]  # joint_name -> angle in degrees
    
    def compare_with(self, other_pose: 'PoseData') -> Dict[str, float]:
        """
        Compare this pose with another and return angle differences.
        
        Args:
            other_pose: Another PoseData object to compare against
            
        Returns:
            Dictionary of angle differences
        """
        differences = {}
        for joint, angle in self.angles.items():
            if joint in other_pose.angles:
                differences[joint] = angle - other_pose.angles[joint]
        return differences


@dataclass
class Point:
    """Represents a single point in a game."""
    pointID: str
    gameID: str
    videoFile: Optional[str] = None
    shots: List[Shot] = field(default_factory=list)
    pose_data: List[PoseData] = field(default_factory=list)


@dataclass
class Game:
    """Represents a single game within a match."""
    gameID: str
    player1Score: int = 0
    player2Score: int = 0
    points: List[Point] = field(default_factory=list)
    
    def add_point(self, player: str) -> None:
        """Add a point for the specified player."""
        if player == "player1":
            self.player1Score += 1
        else:
            self.player2Score += 1
    
    def is_game_over(self) -> bool:
        """Check if game is over."""
        return (self.player1Score >= 11 or self.player2Score >= 11) and \
               abs(self.player1Score - self.player2Score) >= 2
    
    def get_game_winner(self) -> Optional[str]:
        """Get the winner of the game."""
        if self.is_game_over():
            return "player1" if self.player1Score > self.player2Score else "player2"
        return None


@dataclass
class Match:
    """Represents a complete match between two players."""
    matchID: str
    player1Name: str
    player2Name: str
    startTime: datetime
    games: List[Game] = field(default_factory=list)
    
    def start_match(self) -> None:
        """Start the match."""
        self.startTime = datetime.now()
    
    def end_match(self) -> None:
        """End the match."""
        pass
    
    def get_winner(self) -> Optional[str]:
        """Get the winner of the match."""
        player1_wins = sum(1 for game in self.games if game.get_game_winner() == "player1")
        player2_wins = sum(1 for game in self.games if game.get_game_winner() == "player2")
        
        if player1_wins > player2_wins:
            return self.player1Name
        elif player2_wins > player1_wins:
            return self.player2Name
        return None


@dataclass
class PlayerProfile:
    """Stores player statistics and historical data."""
    playerID: str
    playerName: str
    totalWins: int = 0
    totalLosses: int = 0
    totalShots: int = 0
    forehandShots: int = 0
    backhandShots: int = 0
    avgSpeed: float = 0.0
    recentPerformance: str = "N/A"
    
    def get_forehand_ratio(self) -> float:
        """Calculate forehand shot ratio."""
        if self.totalShots == 0:
            return 0.0
        return self.forehandShots / self.totalShots
    
    def get_match_history(self) -> List[Match]:
        """Get match history (placeholder)."""
        return []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API interfaces."""
        return {
            'playerID': self.playerID,
            'playerName': self.playerName,
            'forehand_ratio': self.get_forehand_ratio(),
            'avg_speed': self.avgSpeed,
            'recent_performance': self.recentPerformance,
            'total_wins': self.totalWins,
            'total_losses': self.totalLosses
        }


# Mock data generators for testing
def create_mock_shot(shot_id: str = "shot_001", shot_type: str = "forehand") -> Shot:
    """Create a mock shot for testing."""
    return Shot(
        shotID=shot_id,
        timestamp=1.5,
        start_x=0.2,
        start_y=0.5,
        end_x=0.8,
        end_y=0.6,
        speed=55.5,
        type=shot_type
    )


def create_mock_pose_data(pose_id: str = "pose_001") -> PoseData:
    """Create mock pose data for testing."""
    return PoseData(
        poseID=pose_id,
        pointID="point_001",
        timestamp=1.5,
        keypoints={
            'nose': (0.5, 0.2, 0.0),
            'left_shoulder': (0.4, 0.35, 0.1),
            'right_shoulder': (0.6, 0.35, 0.1),
            'left_elbow': (0.35, 0.5, 0.2),
            'right_elbow': (0.65, 0.5, 0.2),
            'left_wrist': (0.3, 0.65, 0.3),
            'right_wrist': (0.7, 0.65, 0.3),
            'left_hip': (0.42, 0.6, 0.0),
            'right_hip': (0.58, 0.6, 0.0),
            'left_knee': (0.4, 0.8, 0.1),
            'right_knee': (0.6, 0.8, 0.1),
            'left_ankle': (0.4, 0.95, 0.0),
            'right_ankle': (0.6, 0.95, 0.0),
        },
        angles={
            'left_shoulder': 145.0,
            'right_shoulder': 135.0,
            'left_elbow': 110.0,
            'right_elbow': 95.0,
            'left_hip': 175.0,
            'right_hip': 172.0,
            'left_knee': 165.0,
            'right_knee': 168.0,
            'shoulder_rotation': 5.0
        }
    )


def create_mock_player_profile(player_id: str = "player_001") -> PlayerProfile:
    """Create a mock player profile for testing."""
    return PlayerProfile(
        playerID=player_id,
        playerName="Test Player",
        totalWins=15,
        totalLosses=10,
        totalShots=450,
        forehandShots=280,
        backhandShots=170,
        avgSpeed=52.3,
        recentPerformance="Good - 3 wins in last 5 matches"
    )


def create_mock_match() -> Match:
    """Create a mock match for testing."""
    match = Match(
        matchID="match_001",
        player1Name="Player A",
        player2Name="Player B",
        startTime=datetime.now()
    )
    
    # Add a game with some points
    game = Game(gameID="game_001")
    
    # Add a point with shots
    point = Point(
        pointID="point_001",
        gameID="game_001",
        videoFile="/path/to/video.mp4"
    )
    point.shots.append(create_mock_shot("shot_001", "serve"))
    point.shots.append(create_mock_shot("shot_002", "forehand"))
    point.pose_data.append(create_mock_pose_data("pose_001"))
    
    game.points.append(point)
    match.games.append(game)
    
    return match
