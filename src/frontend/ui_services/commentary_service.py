"""
PaddleCoach - AI Commentary Service
Author: Rakshit
Description: Service for generating AI-powered commentary using Gemini and ElevenLabs
"""

import os
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv


class CommentaryService:
    """
    Service for generating AI-powered commentary for match events.
    Uses Google Gemini for text generation and ElevenLabs for text-to-speech.
    """
    
    def __init__(self, env_path=None):
        """
        Initialize the Commentary Service
        
        Args:
            env_path (str): Optional path to .env file
        """
        self.gemini_configured = False
        self.elevenlabs_client = None
        self._configure_apis(env_path)
    
    def _configure_apis(self, env_path=None):
        """
        Configure Gemini and ElevenLabs APIs
        
        Args:
            env_path (str): Optional path to .env file
        """
        try:
            if env_path:
                load_dotenv(dotenv_path=env_path)
            else:
                load_dotenv()
            
            # Configure Gemini
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                self.gemini_configured = True
            
            # Configure ElevenLabs
            elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
            if elevenlabs_api_key:
                self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        
        except Exception as e:
            print(f"Warning: Could not configure AI services: {e}")
    
    def generate_commentary_text(self, event_data):
        """
        Generate commentary text for a match event using Gemini
        
        Args:
            event_data (dict): Event information including:
                - player_name (str): Name of the player
                - event_type (str): Type of event (point, game_win, set_win, etc.)
                - score (dict): Current score information
                - context (str): Additional context
        
        Returns:
            str: Generated commentary text
        """
        if not self.gemini_configured:
            return self._fallback_commentary(event_data)
        
        try:
            # Build scenario description
            scenario = self._build_scenario(event_data)
            
            # Generate commentary using Gemini
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            prompt = (
                "You are a world-class ping pong commentator with deep knowledge of the sport. "
                "Based on the following game event, generate a short, exciting, and insightful "
                "commentary (one sentence, maximum 20 words). Be engaging and professional.\n\n"
                f"Event: {scenario}\n\n"
                "Commentary:"
            )
            
            response = model.generate_content(prompt)
            return response.text.strip()
        
        except Exception as e:
            print(f"Error generating AI commentary: {e}")
            return self._fallback_commentary(event_data)
    
    def _build_scenario(self, event_data):
        """Build a scenario description from event data"""
        player = event_data.get('player_name', 'Player')
        event_type = event_data.get('event_type', 'point')
        score = event_data.get('score', {})
        context = event_data.get('context', '')
        
        if event_type == 'point':
            base = f"{player} scores a point"
            if context:
                return f"{base} {context}"
            return f"{base}."
        
        elif event_type == 'game_win':
            return f"{player} wins the game! Score: {score.get('player1', 0)}-{score.get('player2', 0)}"
        
        elif event_type == 'set_win':
            return f"{player} takes the set {score.get('set_score', '')}!"
        
        elif event_type == 'match_win':
            return f"{player} wins the match {score.get('final_score', '')}!"
        
        return f"{player} {event_type}"
    
    def _fallback_commentary(self, event_data):
        """Provide fallback commentary when AI is not available"""
        import random
        
        player = event_data.get('player_name', 'Player')
        event_type = event_data.get('event_type', 'point')
        
        templates = {
            'point': [
                f"{player} scores!",
                f"Point to {player}!",
                f"Great shot by {player}!",
                f"{player} takes the point!"
            ],
            'game_win': [
                f"{player} wins the game!",
                f"Game to {player}!",
                f"{player} takes the game!"
            ],
            'set_win': [
                f"{player} wins the set!",
                f"Set goes to {player}!",
                f"{player} takes the set!"
            ],
            'match_win': [
                f"{player} wins the match!",
                f"Victory for {player}!",
                f"{player} is the winner!"
            ]
        }
        
        return random.choice(templates.get(event_type, templates['point']))
    
    def generate_audio(self, text, output_path=None, voice_id="ErXwobaYiN019PkySvjV"):
        """
        Generate audio from text using ElevenLabs
        
        Args:
            text (str): Text to convert to speech
            output_path (str): Optional path to save audio file
            voice_id (str): ElevenLabs voice ID
        
        Returns:
            bytes: Audio data, or None if generation failed
        """
        if not self.elevenlabs_client:
            print("ElevenLabs not configured. Cannot generate audio.")
            return None
        
        try:
            # Generate audio
            audio = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_turbo_v2_5"
            )
            
            # Convert generator to bytes
            audio_bytes = b"".join(audio)
            
            # Save to file if path provided
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
            
            return audio_bytes
        
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
    
    def generate_full_commentary(self, event_data, audio_output_path=None, voice_id="ErXwobaYiN019PkySvjV"):
        """
        Generate both text and audio commentary for an event
        
        Args:
            event_data (dict): Event information
            audio_output_path (str): Optional path to save audio
            voice_id (str): ElevenLabs voice ID
        
        Returns:
            dict: Commentary data with text and audio
        """
        # Generate text
        text = self.generate_commentary_text(event_data)
        
        # Generate audio
        audio_bytes = self.generate_audio(text, audio_output_path, voice_id)
        
        return {
            'text': text,
            'audio_bytes': audio_bytes,
            'audio_path': audio_output_path if audio_bytes else None
        }
    
    def batch_generate_commentary(self, events_list, output_dir=None, voice_id="ErXwobaYiN019PkySvjV"):
        """
        Generate commentary for multiple events
        
        Args:
            events_list (list): List of event dictionaries
            output_dir (str): Directory to save audio files
            voice_id (str): ElevenLabs voice ID
        
        Returns:
            list: List of commentary dictionaries
        """
        results = []
        
        for i, event_data in enumerate(events_list):
            audio_path = None
            if output_dir:
                audio_path = os.path.join(output_dir, f"commentary_{i+1}.mp3")
            
            commentary = self.generate_full_commentary(event_data, audio_path, voice_id)
            commentary['event_number'] = i + 1
            results.append(commentary)
        
        return results


# Voice ID constants for easy selection
VOICES = {
    'ADAM': 'pNInz6obpgDQGcFmaJgB',      # Young male
    'ANTONI': 'ErXwobaYiN019PkySvjV',     # Well-rounded male (default)
    'BELLA': 'EXAVITQu4vr4xnSDxMaL',      # Soft female
    'JOSH': 'TxGEqnHWrfWFTfGW9XjX',       # Deep male
    'DOMI': 'D38z5RcWu1voky8WS1ja',       # Strong female
}
