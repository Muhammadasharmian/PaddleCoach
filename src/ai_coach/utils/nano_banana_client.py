"""
Nano Banana API Client
Handles image generation and processing for technique demonstrations.
"""

import os
import requests
from typing import Optional, Dict, List
import base64


class NanoBananaClient:
    """Client for Nano Banana image generation API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Nano Banana client.
        
        Args:
            api_key: Nano Banana API key (or set NANO_BANANA_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("NANO_BANANA_API_KEY")
        self.base_url = "https://api.nanobanana.ai/v1"
        self.mock_mode = not self.api_key
        
        if self.mock_mode:
            print("Nano Banana client running in MOCK MODE")
    
    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate an image from text prompt.
        
        Args:
            prompt: Text description of image to generate
            width: Image width in pixels
            height: Image height in pixels
            output_path: Where to save the image file
            
        Returns:
            Dictionary with image info and path
        """
        if self.mock_mode:
            return self._mock_generate_image(prompt, width, height, output_path)
        
        endpoint = f"{self.base_url}/generate"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "quality": "high"
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            image_url = result.get("image_url")
            
            # Download image if output path specified
            if output_path and image_url:
                self._download_image(image_url, output_path)
                return {
                    "status": "success",
                    "image_url": image_url,
                    "local_path": output_path,
                    "prompt": prompt
                }
            
            return {
                "status": "success",
                "image_url": image_url,
                "prompt": prompt
            }
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return {
                "status": "error",
                "error": str(e),
                "prompt": prompt
            }
    
    def generate_stance_image(
        self,
        stance_type: str,
        annotations: bool = True,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate an annotated stance reference image.
        
        Args:
            stance_type: Type of stance (e.g., "ready position", "forehand stance")
            annotations: Whether to include body angle annotations
            output_path: Where to save image
            
        Returns:
            Image generation result
        """
        prompt = self._build_stance_prompt(stance_type, annotations)
        
        return self.generate_image(
            prompt=prompt,
            width=1024,
            height=1024,
            output_path=output_path
        )
    
    def generate_technique_sequence(
        self,
        technique: str,
        num_frames: int = 4,
        output_dir: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate a sequence of images showing technique progression.
        
        Args:
            technique: Technique to demonstrate
            num_frames: Number of frames in sequence
            output_dir: Directory to save images
            
        Returns:
            List of image generation results
        """
        phases = self._get_technique_phases(technique, num_frames)
        results = []
        
        for i, phase in enumerate(phases):
            prompt = f"Professional table tennis player demonstrating {technique}, {phase}. High quality sports photography, clear form, professional lighting."
            
            output_path = None
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"frame_{i+1:02d}.png")
            
            result = self.generate_image(prompt, 1024, 768, output_path)
            result['phase'] = phase
            result['frame_number'] = i + 1
            results.append(result)
        
        return results
    
    def _build_stance_prompt(self, stance_type: str, annotations: bool) -> str:
        """Build detailed prompt for stance image."""
        base_prompt = f"""Professional table tennis player in perfect {stance_type}. 
Full body shot from side angle. Athletic wear, clean background. 
High quality sports photography with professional lighting."""
        
        if annotations:
            base_prompt += """ Image includes overlay annotations showing:
- Body angles (shoulders, hips, knees)
- Center of gravity
- Weight distribution
- Key positioning points
Educational diagram style with clear labels."""
        
        return base_prompt
    
    def _get_technique_phases(self, technique: str, num_frames: int) -> List[str]:
        """Get phase descriptions for technique sequence."""
        # Default 4-phase breakdown
        if "forehand" in technique.lower():
            phases = [
                "ready position with weight forward",
                "backswing with hip rotation",
                "contact point at peak position",
                "follow-through with full extension"
            ]
        elif "backhand" in technique.lower():
            phases = [
                "ready stance facing the table",
                "rotation and backswing preparation",
                "contact point in front of body",
                "complete follow-through"
            ]
        elif "serve" in technique.lower():
            phases = [
                "pre-serve stance with ball on palm",
                "ball toss with free hand",
                "paddle acceleration to contact",
                "follow-through and recovery"
            ]
        else:
            # Generic phases
            phases = [
                "starting position",
                "preparation phase",
                "execution phase",
                "completion and follow-through"
            ]
        
        # Adjust to requested number of frames
        if num_frames < len(phases):
            phases = phases[:num_frames]
        elif num_frames > len(phases):
            # Repeat middle phases if more frames requested
            while len(phases) < num_frames:
                phases.insert(2, "mid-execution transition")
        
        return phases
    
    def _download_image(self, url: str, output_path: str) -> bool:
        """Download image from URL to local file."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
    
    def _mock_generate_image(
        self, 
        prompt: str, 
        width: int, 
        height: int, 
        output_path: Optional[str]
    ) -> Dict:
        """Generate mock response for testing."""
        print(f"\n🖼️  MOCK IMAGE GENERATION")
        print(f"Prompt: {prompt}")
        print(f"Size: {width}x{height}")
        
        mock_url = f"https://example.com/mock_image_{width}x{height}.png"
        
        # Create a simple placeholder file if output path specified
        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            
            # Create a minimal PNG file (1x1 pixel)
            # This is a valid 1x1 transparent PNG in base64
            minimal_png = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            )
            
            with open(output_path, 'wb') as f:
                f.write(minimal_png)
            
            # Also write a text description
            txt_path = output_path.rsplit('.', 1)[0] + '_info.txt'
            with open(txt_path, 'w') as f:
                f.write(f"MOCK IMAGE\nPrompt: {prompt}\nSize: {width}x{height}\n")
            
            return {
                "status": "success",
                "image_url": mock_url,
                "local_path": output_path,
                "prompt": prompt,
                "mock": True
            }
        
        return {
            "status": "success",
            "image_url": mock_url,
            "prompt": prompt,
            "mock": True
        }
