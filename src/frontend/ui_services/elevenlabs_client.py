"""
PaddleCoach - ElevenLabs TTS Client
Author: Rakshit
Description: Integration with ElevenLabs API for text-to-speech audio commentary
"""

import os
import requests
from typing import Optional


class ElevenLabsClient:
    """
    Client for ElevenLabs Text-to-Speech API
    Generates audio commentary for coaching insights and match commentary
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize ElevenLabs client
        
        Args:
            api_key (str, optional): ElevenLabs API key. If not provided, 
                                    reads from environment variable
        """
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        self.base_url = 'https://api.elevenlabs.io/v1'
        
        # Default voice settings
        self.default_voice_id = 'default'  # Will use specific voice ID
        self.default_voice_settings = {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    
    def generate_speech(self, text: str, voice_id: Optional[str] = None,
                       voice_settings: Optional[dict] = None) -> str:
        """
        Generate speech audio from text
        
        Args:
            text (str): Text to convert to speech
            voice_id (str, optional): ElevenLabs voice ID
            voice_settings (dict, optional): Voice configuration settings
            
        Returns:
            str: URL or path to generated audio file
        """
        if not self.api_key:
            print("Warning: ElevenLabs API key not configured")
            return self._generate_mock_audio()
        
        voice_id = voice_id or self.default_voice_id
        voice_settings = voice_settings or self.default_voice_settings
        
        try:
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                'Accept': 'audio/mpeg',
                'Content-Type': 'application/json',
                'xi-api-key': self.api_key
            }
            
            data = {
                'text': text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': voice_settings
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                # Save audio file
                audio_filename = self._save_audio(response.content)
                return audio_filename
            else:
                print(f"Error: ElevenLabs API returned {response.status_code}")
                return self._generate_mock_audio()
                
        except Exception as e:
            print(f"Error generating speech: {e}")
            return self._generate_mock_audio()
    
    def generate_match_commentary(self, match_event: dict) -> str:
        """
        Generate commentary for a match event
        
        Args:
            match_event (dict): Match event data (point, game, etc.)
            
        Returns:
            str: Audio file path
        """
        commentary_text = self._create_commentary_text(match_event)
        return self.generate_speech(commentary_text)
    
    def generate_coaching_feedback(self, feedback_data: dict) -> str:
        """
        Generate audio feedback for coaching insights
        
        Args:
            feedback_data (dict): Coaching feedback data
            
        Returns:
            str: Audio file path
        """
        feedback_text = self._create_feedback_text(feedback_data)
        return self.generate_speech(
            feedback_text,
            voice_settings={'stability': 0.6, 'similarity_boost': 0.8}
        )
    
    def _create_commentary_text(self, match_event: dict) -> str:
        """
        Create natural commentary text from match event
        
        Args:
            match_event (dict): Match event data
            
        Returns:
            str: Commentary text
        """
        event_type = match_event.get('type', 'point')
        
        if event_type == 'point':
            winner = match_event.get('winner', 'Player')
            rally_length = match_event.get('rally_length', 0)
            return f"Point to {winner}! That was a {rally_length} shot rally. Great play!"
        
        elif event_type == 'game':
            winner = match_event.get('winner', 'Player')
            score = match_event.get('score', '11-9')
            return f"{winner} takes the game, {score}!"
        
        elif event_type == 'match':
            winner = match_event.get('winner', 'Player')
            final_score = match_event.get('final_score', '3-2')
            return f"Match over! {winner} wins, {final_score}! Congratulations!"
        
        return "Great play out there!"
    
    def _create_feedback_text(self, feedback_data: dict) -> str:
        """
        Create coaching feedback text
        
        Args:
            feedback_data (dict): Feedback data
            
        Returns:
            str: Feedback text
        """
        feedback_type = feedback_data.get('type', 'technique')
        message = feedback_data.get('message', '')
        
        if feedback_type == 'technique':
            return f"Technique tip: {message}. Keep practicing this motion to build muscle memory."
        
        elif feedback_type == 'strategy':
            return f"Strategy insight: {message}. Consider this approach in your next match."
        
        elif feedback_type == 'encouragement':
            return f"Great work! {message}. You're making excellent progress."
        
        return message
    
    def _save_audio(self, audio_content: bytes) -> str:
        """
        Save audio content to file
        
        Args:
            audio_content (bytes): Audio file content
            
        Returns:
            str: Path to saved audio file
        """
        import time
        
        # Create audio directory if it doesn't exist
        audio_dir = 'static/audio'
        os.makedirs(audio_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = int(time.time())
        filename = f"{audio_dir}/commentary_{timestamp}.mp3"
        
        with open(filename, 'wb') as f:
            f.write(audio_content)
        
        return f"/{filename}"
    
    def _generate_mock_audio(self) -> str:
        """
        Generate mock audio response when API is unavailable
        
        Returns:
            str: Path to mock audio or empty string
        """
        # Return empty string for now - in production would return silent audio
        print("Using mock audio (ElevenLabs API not configured)")
        return ""
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices from ElevenLabs
        
        Returns:
            list: List of voice dictionaries
        """
        if not self.api_key:
            return self._get_mock_voices()
        
        try:
            url = f"{self.base_url}/voices"
            headers = {'xi-api-key': self.api_key}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json().get('voices', [])
            else:
                return self._get_mock_voices()
                
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return self._get_mock_voices()
    
    def _get_mock_voices(self) -> list:
        """Return mock voice list for development"""
        return [
            {
                'voice_id': 'default',
                'name': 'Default Coach Voice',
                'category': 'professional'
            },
            {
                'voice_id': 'energetic',
                'name': 'Energetic Commentator',
                'category': 'sports'
            }
        ]
    
    def set_voice(self, voice_id: str):
        """
        Set default voice for future generations
        
        Args:
            voice_id (str): ElevenLabs voice ID
        """
        self.default_voice_id = voice_id
    
    def test_connection(self) -> bool:
        """
        Test connection to ElevenLabs API
        
        Returns:
            bool: True if connection successful
        """
        if not self.api_key:
            print("No API key configured")
            return False
        
        try:
            voices = self.get_available_voices()
            return len(voices) > 0
        except:
            return False
