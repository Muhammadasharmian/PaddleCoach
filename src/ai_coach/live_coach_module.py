"""
Module 3C: Live Coach Module
Real-time coaching feedback during gameplay using RAG.

This module:
1. Subscribes to live shot data stream
2. Uses RAG to retrieve relevant pro tips
3. Provides immediate, actionable feedback
4. Considers player history and current context
"""

import json
import os
from typing import Dict, List, Optional, Callable
from collections import deque
from .utils import GeminiClient
from .mock_models import Shot, PlayerProfile
from .ai_interface import IAnalyticsData, MockAnalyticsData, IAICoachingModule


class LiveCoachModule(IAICoachingModule):
    """
    Provides real-time coaching feedback during matches.
    Uses RAG (Retrieval-Augmented Generation) with pro knowledge base.
    """
    
    def __init__(
        self,
        analytics_interface: Optional[IAnalyticsData] = None,
        gemini_api_key: Optional[str] = None,
        knowledge_base_path: Optional[str] = None
    ):
        """
        Initialize Live Coach module.
        
        Args:
            analytics_interface: Interface to access game data
            gemini_api_key: Gemini API key for analysis
            knowledge_base_path: Path to RAG knowledge base JSON
        """
        self.analytics = analytics_interface or MockAnalyticsData()
        self.gemini = GeminiClient(api_key=gemini_api_key)
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        self.recent_shots = deque(maxlen=10)  # Keep last 10 shots for context
        self.feedback_history = deque(maxlen=20)  # Avoid repeating same advice
        self.initialized = False
        self.callbacks: List[Callable] = []
    
    def initialize(self) -> bool:
        """Initialize the module and check dependencies."""
        try:
            if not self.knowledge_base:
                print("⚠️ Warning: No knowledge base loaded. Using default tips.")
                self.knowledge_base = self._get_default_knowledge_base()
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get current status of the module."""
        return {
            "module": "LiveCoach",
            "initialized": self.initialized,
            "gemini_available": self.gemini is not None,
            "knowledge_base_entries": len(self.knowledge_base),
            "recent_shots": len(self.recent_shots),
            "active_callbacks": len(self.callbacks)
        }
    
    def register_callback(self, callback: Callable[[str], None]) -> None:
        """
        Register a callback to receive real-time coaching tips.
        
        Args:
            callback: Function that takes a coaching tip string
        """
        self.callbacks.append(callback)
        print(f"✅ Callback registered. Total callbacks: {len(self.callbacks)}")
    
    def process_shot(
        self,
        shot: Shot,
        player_id: str,
        game_context: Optional[Dict] = None
    ) -> Optional[str]:
        """
        Process a shot and generate coaching feedback.
        
        Args:
            shot: Shot object to analyze
            player_id: ID of player who made the shot
            game_context: Additional context (score, opponent state, etc.)
            
        Returns:
            Coaching tip string or None
        """
        # Add to recent shots history
        self.recent_shots.append(shot)
        
        # Get player profile for historical context
        player_profile = self.analytics.get_player_profile(player_id)
        if not player_profile:
            player_profile = PlayerProfile(playerID=player_id, playerName="Unknown")
        
        # Analyze current shot
        should_give_feedback = self._should_provide_feedback(shot, player_profile)
        
        if not should_give_feedback:
            return None
        
        # Generate coaching tip
        tip = self._generate_coaching_tip(
            shot,
            player_profile,
            game_context or {}
        )
        
        # Track feedback history
        self.feedback_history.append(tip)
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(tip)
            except Exception as e:
                print(f"Error in callback: {e}")
        
        return tip
    
    def start_live_session(
        self,
        player_id: str,
        feedback_frequency: str = "medium"
    ) -> None:
        """
        Start a live coaching session.
        
        Args:
            player_id: Player to coach
            feedback_frequency: "low", "medium", or "high"
        """
        print(f"\n🎾 Starting live coaching session for player: {player_id}")
        print(f"Feedback frequency: {feedback_frequency}")
        
        # Set feedback threshold based on frequency
        if feedback_frequency == "low":
            self.feedback_threshold = 0.7
        elif feedback_frequency == "high":
            self.feedback_threshold = 0.3
        else:
            self.feedback_threshold = 0.5
        
        print(f"✅ Live coaching active. Listening for shots...")
    
    def end_live_session(self) -> Dict:
        """
        End live coaching session and return summary.
        
        Returns:
            Session summary dictionary
        """
        summary = {
            "total_shots_analyzed": len(self.recent_shots),
            "total_tips_given": len(self.feedback_history),
            "tips": list(self.feedback_history)
        }
        
        print(f"\n📊 Live coaching session ended")
        print(f"Shots analyzed: {summary['total_shots_analyzed']}")
        print(f"Tips provided: {summary['total_tips_given']}")
        
        return summary
    
    def _should_provide_feedback(
        self, 
        shot: Shot, 
        player_profile: PlayerProfile
    ) -> bool:
        """
        Determine if feedback should be provided for this shot.
        
        Uses heuristics to avoid overwhelming player with constant tips.
        """
        # Don't give feedback too frequently
        if len(self.feedback_history) > 0:
            # At least 3 shots between feedback
            shots_since_feedback = len(self.recent_shots)
            if shots_since_feedback < 3:
                return False
        
        # Prioritize feedback on problematic shots
        if shot.speed < 30:  # Very slow
            return True
        if shot.speed > 90:  # Too fast (loss of control)
            return True
        
        # Analyze shot pattern
        if len(self.recent_shots) >= 5:
            recent_types = [s.type for s in list(self.recent_shots)[-5:]]
            # If player is repeating same shot type, might need variety
            if len(set(recent_types)) == 1:
                return True
        
        # Use probability based on threshold
        import random
        return random.random() < getattr(self, 'feedback_threshold', 0.5)
    
    def _generate_coaching_tip(
        self,
        shot: Shot,
        player_profile: PlayerProfile,
        game_context: Dict
    ) -> str:
        """
        Generate coaching tip using RAG and Gemini.
        
        Combines:
        1. Current shot analysis
        2. Player's historical stats
        3. Relevant knowledge from pro tips database
        4. Game context
        """
        # Prepare shot data
        shot_data = {
            'type': shot.type,
            'speed': shot.speed,
            'placement': f"({shot.end_x:.2f}, {shot.end_y:.2f})",
            'start_x': shot.start_x,
            'start_y': shot.start_y,
            'end_x': shot.end_x,
            'end_y': shot.end_y
        }
        
        # Get player stats
        player_stats = player_profile.to_dict()
        
        # Build context string
        context_parts = []
        if 'score' in game_context:
            context_parts.append(f"Score: {game_context['score']}")
        if 'rally_length' in game_context:
            context_parts.append(f"Rally length: {game_context['rally_length']}")
        if 'opponent_position' in game_context:
            context_parts.append(f"Opponent position: {game_context['opponent_position']}")
        
        context_str = "; ".join(context_parts) if context_parts else "No specific context"
        
        # Generate tip using Gemini with RAG
        tip = self.gemini.generate_live_coaching_tip(
            current_shot_data=shot_data,
            player_stats=player_stats,
            knowledge_base=self.knowledge_base,
            context=context_str
        )
        
        return tip
    
    def _load_knowledge_base(self, path: Optional[str]) -> List[Dict]:
        """Load RAG knowledge base from JSON file."""
        if not path or not os.path.exists(path):
            return []
        
        try:
            with open(path, 'r') as f:
                kb = json.load(f)
                print(f"✅ Loaded knowledge base: {len(kb)} entries")
                return kb
        except Exception as e:
            print(f"⚠️ Error loading knowledge base: {e}")
            return []
    
    def _get_default_knowledge_base(self) -> List[Dict]:
        """
        Get default knowledge base with common pro tips.
        
        Returns list of coaching tips with keywords for RAG.
        """
        return [
            {
                "id": "kb_001",
                "category": "forehand",
                "keywords": ["forehand", "topspin", "speed"],
                "tip": "For a powerful forehand topspin, start your swing from below the ball and brush upward through contact. Weight should transfer from back foot to front foot."
            },
            {
                "id": "kb_002",
                "category": "backhand",
                "keywords": ["backhand", "control"],
                "tip": "On backhand shots, keep your elbow close to your body for better control. Contact the ball at the peak of its bounce when possible."
            },
            {
                "id": "kb_003",
                "category": "serve",
                "keywords": ["serve", "spin"],
                "tip": "A good serve uses wrist snap to generate spin. Toss the ball slightly forward and contact it at the highest point you can comfortably reach."
            },
            {
                "id": "kb_004",
                "category": "footwork",
                "keywords": ["movement", "position", "footwork"],
                "tip": "Always return to ready position after each shot. Stay on the balls of your feet for quick movement in any direction."
            },
            {
                "id": "kb_005",
                "category": "placement",
                "keywords": ["placement", "strategy", "crosscourt"],
                "tip": "Vary your shot placement. Crosscourt shots are safer and create better angles. Down-the-line shots are riskier but can catch opponents off guard."
            },
            {
                "id": "kb_006",
                "category": "speed",
                "keywords": ["speed", "power", "fast"],
                "tip": "Power comes from your legs and core, not just your arm. Rotate your hips and shoulders to generate speed."
            },
            {
                "id": "kb_007",
                "category": "consistency",
                "keywords": ["consistency", "control", "error"],
                "tip": "Consistency beats power. Aim to keep the ball on the table rather than going for winners every shot. Make your opponent earn their points."
            },
            {
                "id": "kb_008",
                "category": "defense",
                "keywords": ["defense", "block", "counter"],
                "tip": "When under pressure, focus on returning the ball deep to the opponent's side. This buys you time to recover position."
            },
            {
                "id": "kb_009",
                "category": "timing",
                "keywords": ["timing", "contact", "early", "late"],
                "tip": "Hit the ball at the top of its bounce for maximum control. Early timing gives you less time but more pace; late timing gives more spin."
            },
            {
                "id": "kb_010",
                "category": "mental",
                "keywords": ["focus", "concentration", "mental"],
                "tip": "Stay focused on the ball, not the score. Play one point at a time and don't dwell on mistakes."
            }
        ]
    
    def get_tip_summary(self, player_id: str) -> Dict:
        """
        Get summary of tips given to a player.
        
        Args:
            player_id: Player ID
            
        Returns:
            Summary of coaching provided
        """
        recent_tips = list(self.feedback_history)[-10:]
        
        # Categorize tips (simple keyword matching)
        categories = {
            "technique": 0,
            "strategy": 0,
            "footwork": 0,
            "mental": 0,
            "other": 0
        }
        
        for tip in recent_tips:
            tip_lower = tip.lower()
            if any(word in tip_lower for word in ["arm", "elbow", "wrist", "swing"]):
                categories["technique"] += 1
            elif any(word in tip_lower for word in ["placement", "strategy", "vary"]):
                categories["strategy"] += 1
            elif any(word in tip_lower for word in ["footwork", "position", "move"]):
                categories["footwork"] += 1
            elif any(word in tip_lower for word in ["focus", "mental", "concentrate"]):
                categories["mental"] += 1
            else:
                categories["other"] += 1
        
        return {
            "player_id": player_id,
            "total_tips": len(recent_tips),
            "recent_tips": recent_tips,
            "categories": categories
        }
