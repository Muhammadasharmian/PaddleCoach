"""
AI Interface
Common interfaces for AI coaching modules.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .mock_models import Shot, PoseData, Match, PlayerProfile


class IAnalyticsData(ABC):
    """
    Interface for accessing analytics data from Ashar's module.
    This defines what data your AI coaching modules can request.
    """
    
    @abstractmethod
    def get_match(self, match_id: str) -> Optional[Match]:
        """Get match data by ID."""
        pass
    
    @abstractmethod
    def get_player_profile(self, player_id: str) -> Optional[PlayerProfile]:
        """Get player profile and statistics."""
        pass
    
    @abstractmethod
    def get_recent_shots(self, player_id: str, limit: int = 10) -> List[Shot]:
        """Get recent shots for a player."""
        pass
    
    @abstractmethod
    def get_shot_by_id(self, shot_id: str) -> Optional[Shot]:
        """Get specific shot by ID."""
        pass


class MockAnalyticsData(IAnalyticsData):
    """
    Mock implementation of analytics interface for independent testing.
    Replace this with real implementation when integrating with Ashar's module.
    """
    
    def __init__(self):
        from .mock_models import create_mock_match, create_mock_player_profile, create_mock_shot
        self.matches = {"match_001": create_mock_match()}
        self.players = {"player_001": create_mock_player_profile()}
        self.shots = [create_mock_shot(f"shot_{i:03d}") for i in range(10)]
    
    def get_match(self, match_id: str) -> Optional[Match]:
        """Get match data by ID."""
        return self.matches.get(match_id)
    
    def get_player_profile(self, player_id: str) -> Optional[PlayerProfile]:
        """Get player profile and statistics."""
        return self.players.get(player_id)
    
    def get_recent_shots(self, player_id: str, limit: int = 10) -> List[Shot]:
        """Get recent shots for a player."""
        return self.shots[:limit]
    
    def get_shot_by_id(self, shot_id: str) -> Optional[Shot]:
        """Get specific shot by ID."""
        for shot in self.shots:
            if shot.shotID == shot_id:
                return shot
        return None


class IAICoachingModule(ABC):
    """Base interface for all AI coaching modules."""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the module and check if all dependencies are available."""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Get current status of the module."""
        pass
