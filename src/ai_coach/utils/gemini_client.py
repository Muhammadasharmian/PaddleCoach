"""
Google Gemini API Client
Handles all interactions with Gemini AI for analysis and coaching feedback.
"""

import os
from typing import Dict, List, Optional, Any
import json


try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Using mock mode.")


class GeminiClient:
    """Client for Google Gemini API interactions."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key (or set GEMINI_API_KEY env variable)
            model_name: Model to use (gemini-2.0-flash-exp, gemini-1.5-pro, etc.)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self.model = None
        
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            print("Gemini client running in MOCK MODE")
    
    def analyze_pose_comparison(
        self, 
        user_pose_data: Dict, 
        pro_pose_data: Dict,
        shot_type: str = "forehand"
    ) -> str:
        """
        Compare user pose data with professional and generate insights.
        
        Args:
            user_pose_data: User's pose angles and keypoints
            pro_pose_data: Professional's pose angles and keypoints
            shot_type: Type of shot being analyzed
            
        Returns:
            Detailed analysis text
        """
        if not self.model:
            return self._mock_pose_comparison(user_pose_data, pro_pose_data, shot_type)
        
        prompt = self._build_pose_comparison_prompt(
            user_pose_data, 
            pro_pose_data, 
            shot_type
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._mock_pose_comparison(user_pose_data, pro_pose_data, shot_type)
    
    def generate_live_coaching_tip(
        self,
        current_shot_data: Dict,
        player_stats: Dict,
        knowledge_base: List[Dict],
        context: str = ""
    ) -> str:
        """
        Generate real-time coaching tip using RAG.
        
        Args:
            current_shot_data: Current shot information
            player_stats: Player's historical statistics
            knowledge_base: RAG knowledge base entries
            context: Additional context about current game state
            
        Returns:
            Coaching tip text
        """
        if not self.model:
            return self._mock_live_coaching_tip(current_shot_data)
        
        prompt = self._build_live_coaching_prompt(
            current_shot_data,
            player_stats,
            knowledge_base,
            context
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._mock_live_coaching_tip(current_shot_data)
    
    def generate_technique_description(
        self,
        technique: str,
        focus_areas: List[str] = None
    ) -> str:
        """
        Generate detailed description for a technique (for video generation prompts).
        
        Args:
            technique: Name of technique (e.g., "forehand topspin")
            focus_areas: Specific areas to emphasize
            
        Returns:
            Detailed technique description
        """
        if not self.model:
            return self._mock_technique_description(technique, focus_areas)
        
        prompt = f"""Generate a detailed visual description for demonstrating a perfect ping pong {technique}.
        
Focus on:
- Body positioning and stance
- Arm movement and trajectory
- Hip and shoulder rotation
- Footwork
- Contact point with the ball
- Follow-through

{"Emphasize these specific areas: " + ", ".join(focus_areas) if focus_areas else ""}

Format the description as if instructing a video generation AI. Be specific about angles, timing, and motion."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._mock_technique_description(technique, focus_areas)
    
    def _build_pose_comparison_prompt(
        self, 
        user_data: Dict, 
        pro_data: Dict, 
        shot_type: str
    ) -> str:
        """Build prompt for pose comparison analysis."""
        return f"""You are an expert ping pong coach analyzing player technique.

Compare the following pose data from a user and a professional player executing a {shot_type}:

USER'S POSE DATA:
Angles: {json.dumps(user_data.get('angles', {}), indent=2)}
Keypoints: {json.dumps({k: f"({v[0]:.2f}, {v[1]:.2f})" for k, v in user_data.get('keypoints', {}).items()}, indent=2)}

PROFESSIONAL'S POSE DATA:
Angles: {json.dumps(pro_data.get('angles', {}), indent=2)}
Keypoints: {json.dumps({k: f"({v[0]:.2f}, {v[1]:.2f})" for k, v in pro_data.get('keypoints', {}).items()}, indent=2)}

Provide a detailed analysis covering:
1. Key differences in body angles (shoulders, elbows, hips, knees)
2. Positioning differences (stance, weight distribution)
3. Specific actionable improvements (e.g., "Rotate your shoulders 15° more to the right")
4. Priority order of corrections (what to fix first)
5. Expected impact of each correction on shot quality

Be specific with measurements and give clear, actionable advice."""

    def _build_live_coaching_prompt(
        self,
        shot_data: Dict,
        player_stats: Dict,
        knowledge_base: List[Dict],
        context: str
    ) -> str:
        """Build prompt for live coaching with RAG."""
        # Select relevant knowledge base entries
        relevant_knowledge = self._select_relevant_knowledge(shot_data, knowledge_base)
        
        return f"""You are a real-time ping pong coach providing immediate feedback during a match.

CURRENT SHOT:
Type: {shot_data.get('type', 'unknown')}
Speed: {shot_data.get('speed', 0):.1f} km/h
Placement: ({shot_data.get('end_x', 0):.2f}, {shot_data.get('end_y', 0):.2f})

PLAYER STATISTICS:
Forehand Ratio: {player_stats.get('forehand_ratio', 0):.1%}
Average Shot Speed: {player_stats.get('avg_speed', 0):.1f} km/h
Recent Performance: {player_stats.get('recent_performance', 'N/A')}

RELEVANT COACHING KNOWLEDGE:
{self._format_knowledge_entries(relevant_knowledge)}

GAME CONTEXT:
{context}

Provide ONE concise, actionable tip (1-2 sentences max) that the player can immediately apply. 
Focus on the most impactful improvement for their current situation."""

    def _select_relevant_knowledge(
        self, 
        shot_data: Dict, 
        knowledge_base: List[Dict]
    ) -> List[Dict]:
        """Select relevant entries from knowledge base (simple keyword matching)."""
        shot_type = shot_data.get('type', '').lower()
        
        relevant = []
        for entry in knowledge_base:
            if shot_type in entry.get('keywords', []):
                relevant.append(entry)
            if len(relevant) >= 3:  # Limit to top 3
                break
        
        return relevant
    
    def _format_knowledge_entries(self, entries: List[Dict]) -> str:
        """Format knowledge base entries for prompt."""
        if not entries:
            return "No specific knowledge available."
        
        formatted = []
        for i, entry in enumerate(entries, 1):
            formatted.append(f"{i}. {entry.get('tip', '')}")
        
        return "\n".join(formatted)
    
    # Mock responses for testing without API
    def _mock_pose_comparison(self, user_data, pro_data, shot_type):
        """Generate mock pose comparison for testing."""
        user_angles = user_data.get('angles', {})
        pro_angles = pro_data.get('angles', {})
        
        analysis = f"**{shot_type.upper()} TECHNIQUE ANALYSIS**\n\n"
        
        # Compare some key angles
        if 'right_shoulder' in user_angles and 'right_shoulder' in pro_angles:
            diff = user_angles['right_shoulder'] - pro_angles['right_shoulder']
            analysis += f"1. **Shoulder Position**: Your shoulder angle is {abs(diff):.1f}° {'less' if diff < 0 else 'more'} than the pro. "
            analysis += "Try to open your shoulder more during the backswing.\n\n"
        
        if 'right_elbow' in user_angles and 'right_elbow' in pro_angles:
            diff = user_angles['right_elbow'] - pro_angles['right_elbow']
            analysis += f"2. **Elbow Extension**: Your elbow angle differs by {abs(diff):.1f}°. "
            analysis += "Keep your elbow slightly bent for better control.\n\n"
        
        analysis += "3. **Priority Improvements**:\n"
        analysis += "   - First: Work on shoulder rotation (biggest impact)\n"
        analysis += "   - Second: Adjust elbow position for consistency\n"
        analysis += "   - Third: Focus on follow-through completion\n"
        
        return analysis
    
    def _mock_live_coaching_tip(self, shot_data):
        """Generate mock live coaching tip."""
        shot_type = shot_data.get('type', 'shot')
        speed = shot_data.get('speed', 0)
        
        if speed < 30:
            return f"Add more speed to your {shot_type} - snap your wrist through contact!"
        elif speed > 80:
            return f"Great power on that {shot_type}, but focus on placement for consistency."
        else:
            return f"Good {shot_type}! Try to hit earlier in the bounce for more control."
    
    def _mock_technique_description(self, technique, focus_areas):
        """Generate mock technique description."""
        return f"""Professional {technique} demonstration in slow motion:

The player stands in a ready position with knees slightly bent and weight on the balls of their feet. 
As the ball approaches, they rotate their hips and shoulders back, loading power into their core. 
The paddle arm extends back naturally, elbow at 90 degrees. 

During the forward swing, the hips rotate first, followed by the shoulders and arm in a fluid chain. 
Contact occurs at waist height, slightly in front of the body, with the paddle face brushing upward 
across the ball for topspin. The follow-through continues high and across the body.

{f"Special emphasis on: {', '.join(focus_areas)}" if focus_areas else ""}

Camera angles: Front view showing hip rotation, side view showing forward weight transfer, 
close-up on paddle contact point."""
