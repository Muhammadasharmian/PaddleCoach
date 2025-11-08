"""
AI Coaching Suite for PaddleCoach
Mohnish's Modules (3A, 3B, 3C)

This package provides three AI coaching modules:
- ProComparisonModule (3A): Offline pose comparison with pros
- VisualDemoModule (3B): Generate demonstration videos/images
- LiveCoachModule (3C): Real-time coaching feedback with RAG
"""

__version__ = "0.1.0"
__author__ = "Mohnish"

from .pro_comparison_module import ProComparisonModule
from .visual_demo_module import VisualDemoModule
from .live_coach_module import LiveCoachModule
from .ai_interface import IAnalyticsData, MockAnalyticsData, IAICoachingModule
from .mock_models import (
    Shot, PoseData, Point, Game, Match, PlayerProfile,
    create_mock_shot, create_mock_pose_data, create_mock_player_profile, create_mock_match
)

__all__ = [
    # Main Modules
    'ProComparisonModule',
    'VisualDemoModule',
    'LiveCoachModule',
    
    # Interfaces
    'IAnalyticsData',
    'MockAnalyticsData',
    'IAICoachingModule',
    
    # Data Models
    'Shot',
    'PoseData',
    'Point',
    'Game',
    'Match',
    'PlayerProfile',
    
    # Mock Data Generators
    'create_mock_shot',
    'create_mock_pose_data',
    'create_mock_player_profile',
    'create_mock_match',
]
