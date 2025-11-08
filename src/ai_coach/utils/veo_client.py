"""
Veo 3.1 API Client
Handles video generation using Google's Veo 3.1 model.
"""

import os
import time
from typing import Optional, Dict
import requests


class VeoClient:
    """Client for Veo 3.1 video generation API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Veo client.
        
        Args:
            api_key: Google Cloud API key (or set VEO_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("VEO_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.mock_mode = not self.api_key
        
        if self.mock_mode:
            print("Veo client running in MOCK MODE")
    
    def generate_video(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9",
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate a video from text prompt.
        
        Args:
            prompt: Text description of video to generate
            duration: Video duration in seconds (max 8 for Veo 3.1)
            aspect_ratio: Video aspect ratio ("16:9", "9:16", "1:1")
            output_path: Where to save the video file
            
        Returns:
            Dictionary with video info and path
        """
        if self.mock_mode:
            return self._mock_generate_video(prompt, duration, output_path)
        
        # Veo API endpoint (Note: This is a placeholder - actual endpoint may vary)
        endpoint = f"{self.base_url}/models/veo:generateVideo"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "quality": "high"
        }
        
        try:
            # Submit generation request
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            operation_id = result.get("operation_id")
            
            # Poll for completion
            video_url = self._poll_for_completion(operation_id, headers)
            
            # Download video if output path specified
            if output_path and video_url:
                self._download_video(video_url, output_path)
                return {
                    "status": "success",
                    "video_url": video_url,
                    "local_path": output_path,
                    "prompt": prompt,
                    "duration": duration
                }
            
            return {
                "status": "success",
                "video_url": video_url,
                "prompt": prompt,
                "duration": duration
            }
            
        except Exception as e:
            print(f"Error generating video: {e}")
            return {
                "status": "error",
                "error": str(e),
                "prompt": prompt
            }
    
    def generate_technique_demo(
        self,
        technique: str,
        focus_areas: list = None,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate a technique demonstration video.
        
        Args:
            technique: Technique name (e.g., "forehand topspin")
            focus_areas: Specific aspects to emphasize
            output_path: Where to save video
            
        Returns:
            Video generation result
        """
        # Build detailed prompt
        prompt = self._build_technique_prompt(technique, focus_areas)
        
        return self.generate_video(
            prompt=prompt,
            duration=6,
            aspect_ratio="16:9",
            output_path=output_path
        )
    
    def _build_technique_prompt(self, technique: str, focus_areas: list) -> str:
        """Build detailed prompt for technique demonstration."""
        base_prompt = f"""Professional table tennis player demonstrating perfect {technique} technique 
in slow motion. High quality sports cinematography with multiple camera angles. 
Clean indoor table tennis facility with professional lighting. 
Focus on body mechanics, paddle movement, and contact point."""
        
        if focus_areas:
            base_prompt += f"\n\nEmphasize: {', '.join(focus_areas)}"
        
        base_prompt += "\n\nCinematic, smooth motion, professional sports demonstration."
        
        return base_prompt
    
    def _poll_for_completion(self, operation_id: str, headers: Dict, timeout: int = 120) -> Optional[str]:
        """
        Poll the API until video generation is complete.
        
        Args:
            operation_id: ID from initial request
            headers: Request headers
            timeout: Maximum time to wait in seconds
            
        Returns:
            URL of generated video or None
        """
        status_endpoint = f"{self.base_url}/operations/{operation_id}"
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(status_endpoint, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                if result.get("done"):
                    return result.get("response", {}).get("video_url")
                
                time.sleep(5)  # Wait 5 seconds between polls
                
            except Exception as e:
                print(f"Error polling status: {e}")
                return None
        
        print("Video generation timed out")
        return None
    
    def _download_video(self, url: str, output_path: str) -> bool:
        """Download video from URL to local file."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False
    
    def _mock_generate_video(self, prompt: str, duration: int, output_path: Optional[str]) -> Dict:
        """Generate mock response for testing."""
        print(f"\n🎬 MOCK VIDEO GENERATION")
        print(f"Prompt: {prompt}")
        print(f"Duration: {duration}s")
        
        mock_url = "https://example.com/mock_video.mp4"
        
        # Create a placeholder file if output path specified
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(f"MOCK VIDEO FILE\nPrompt: {prompt}\nDuration: {duration}s\n")
            
            return {
                "status": "success",
                "video_url": mock_url,
                "local_path": output_path,
                "prompt": prompt,
                "duration": duration,
                "mock": True
            }
        
        return {
            "status": "success",
            "video_url": mock_url,
            "prompt": prompt,
            "duration": duration,
            "mock": True
        }
