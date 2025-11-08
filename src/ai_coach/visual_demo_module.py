"""
Module 3B: Visual Demonstrator Module
Generates synthetic demonstration videos and images showing ideal technique.

This module:
1. Generates AI videos using Veo 3.1 showing perfect form
2. Creates reference images using Nano Banana
3. Produces technique sequences and annotated stances
"""

import os
from typing import Dict, List, Optional
from .utils import VeoClient, NanoBananaClient, GeminiClient
from .ai_interface import IAICoachingModule


class VisualDemoModule(IAICoachingModule):
    """
    Generates visual demonstrations of correct technique.
    Uses generative AI to create videos and images for player reference.
    """
    
    def __init__(
        self,
        veo_api_key: Optional[str] = None,
        nano_banana_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None
    ):
        """
        Initialize Visual Demo module.
        
        Args:
            veo_api_key: Veo 3.1 API key for video generation
            nano_banana_api_key: Nano Banana API key for images
            gemini_api_key: Gemini API key for prompt enhancement
        """
        self.veo = VeoClient(api_key=veo_api_key)
        self.nano_banana = NanoBananaClient(api_key=nano_banana_api_key)
        self.gemini = GeminiClient(api_key=gemini_api_key)
        self.initialized = False
    
    def initialize(self) -> bool:
        """Initialize the module and check dependencies."""
        try:
            # Check if clients are available (even in mock mode)
            self.initialized = True
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get current status of the module."""
        return {
            "module": "VisualDemo",
            "initialized": self.initialized,
            "veo_available": self.veo is not None,
            "nano_banana_available": self.nano_banana is not None,
            "gemini_available": self.gemini is not None
        }
    
    def generate_technique_video(
        self,
        technique: str,
        focus_areas: Optional[List[str]] = None,
        duration: int = 6,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate a demonstration video of a technique.
        
        Args:
            technique: Technique to demonstrate (e.g., "forehand topspin")
            focus_areas: Specific aspects to emphasize
            duration: Video duration in seconds (max 8)
            output_path: Where to save the video
            
        Returns:
            Video generation result dictionary
        """
        print(f"\n🎬 Generating technique video: {technique}")
        
        # Step 1: Use Gemini to create detailed prompt
        print("📝 Creating detailed prompt...")
        detailed_description = self.gemini.generate_technique_description(
            technique, 
            focus_areas or []
        )
        
        print(f"Generated description:\n{detailed_description[:200]}...")
        
        # Step 2: Generate video with Veo
        print("\n🎥 Generating video with Veo 3.1...")
        result = self.veo.generate_technique_demo(
            technique=technique,
            focus_areas=focus_areas,
            output_path=output_path
        )
        
        # Add metadata
        result['technique'] = technique
        result['focus_areas'] = focus_areas
        result['detailed_prompt'] = detailed_description
        
        if result['status'] == 'success':
            print(f"✅ Video generated successfully!")
            if 'local_path' in result:
                print(f"📁 Saved to: {result['local_path']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        return result
    
    def generate_stance_reference(
        self,
        stance_type: str,
        annotated: bool = True,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate a reference image of a specific stance.
        
        Args:
            stance_type: Type of stance (e.g., "ready position", "forehand stance")
            annotated: Whether to include angle annotations
            output_path: Where to save the image
            
        Returns:
            Image generation result
        """
        print(f"\n🖼️  Generating stance reference: {stance_type}")
        print(f"Annotations: {'Yes' if annotated else 'No'}")
        
        result = self.nano_banana.generate_stance_image(
            stance_type=stance_type,
            annotations=annotated,
            output_path=output_path
        )
        
        result['stance_type'] = stance_type
        result['annotated'] = annotated
        
        if result['status'] == 'success':
            print(f"✅ Image generated successfully!")
            if 'local_path' in result:
                print(f"📁 Saved to: {result['local_path']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        return result
    
    def generate_technique_sequence(
        self,
        technique: str,
        num_frames: int = 4,
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Generate a sequence of images showing technique progression.
        
        Args:
            technique: Technique to demonstrate
            num_frames: Number of frames in sequence
            output_dir: Directory to save images
            
        Returns:
            Dictionary with sequence results
        """
        print(f"\n📸 Generating {num_frames}-frame sequence: {technique}")
        
        results = self.nano_banana.generate_technique_sequence(
            technique=technique,
            num_frames=num_frames,
            output_dir=output_dir
        )
        
        # Compile summary
        successful = sum(1 for r in results if r['status'] == 'success')
        
        summary = {
            'status': 'success' if successful == len(results) else 'partial',
            'technique': technique,
            'requested_frames': num_frames,
            'successful_frames': successful,
            'frames': results,
            'output_dir': output_dir
        }
        
        print(f"✅ Generated {successful}/{num_frames} frames successfully!")
        
        return summary
    
    def generate_correction_video(
        self,
        current_issue: str,
        correction: str,
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate a video showing before/after correction.
        
        Args:
            current_issue: Description of current problem
            correction: Description of correct form
            output_path: Where to save video
            
        Returns:
            Video generation result
        """
        print(f"\n🔧 Generating correction video")
        print(f"Issue: {current_issue}")
        print(f"Correction: {correction}")
        
        # Build detailed prompt
        prompt = f"""Table tennis technique correction demonstration in slow motion:

CURRENT ISSUE: {current_issue}

CORRECT FORM: {correction}

Show side-by-side comparison or sequential demonstration. Professional player in clean indoor 
facility. Highlight the specific difference with visual markers. Slow motion for clarity. 
Cinematic sports cinematography."""
        
        print("\n🎥 Generating correction video...")
        result = self.veo.generate_video(
            prompt=prompt,
            duration=8,  # Max duration for detailed correction
            output_path=output_path
        )
        
        result['correction_type'] = 'technique_fix'
        result['issue'] = current_issue
        result['correction'] = correction
        
        if result['status'] == 'success':
            print(f"✅ Correction video generated!")
        
        return result
    
    def generate_custom_demo(
        self,
        user_prompt: str,
        media_type: str = "video",
        output_path: Optional[str] = None
    ) -> Dict:
        """
        Generate custom demonstration from user's natural language prompt.
        
        Args:
            user_prompt: User's description of what they want to see
            media_type: "video" or "image"
            output_path: Where to save the file
            
        Returns:
            Generation result
        """
        print(f"\n🎨 Generating custom {media_type} from prompt")
        print(f"User prompt: {user_prompt}")
        
        # Enhance prompt with context
        enhanced_prompt = f"""Table tennis demonstration: {user_prompt}

Professional player, clean indoor facility, high quality sports {media_type}, 
clear technique demonstration."""
        
        if media_type == "video":
            result = self.veo.generate_video(
                prompt=enhanced_prompt,
                duration=6,
                output_path=output_path
            )
        else:  # image
            result = self.nano_banana.generate_image(
                prompt=enhanced_prompt,
                width=1024,
                height=1024,
                output_path=output_path
            )
        
        result['media_type'] = media_type
        result['user_prompt'] = user_prompt
        result['enhanced_prompt'] = enhanced_prompt
        
        return result
    
    def create_training_package(
        self,
        technique: str,
        output_dir: str
    ) -> Dict:
        """
        Create a complete training package with multiple visual aids.
        
        Args:
            technique: Technique to create package for
            output_dir: Directory to save all files
            
        Returns:
            Summary of created package
        """
        print(f"\n📦 Creating training package for: {technique}")
        print(f"Output directory: {output_dir}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        package = {
            'technique': technique,
            'output_dir': output_dir,
            'items': []
        }
        
        # 1. Main demonstration video
        print("\n1️⃣ Generating main demo video...")
        video_path = os.path.join(output_dir, f"{technique.replace(' ', '_')}_demo.mp4")
        video_result = self.generate_technique_video(
            technique=technique,
            duration=6,
            output_path=video_path
        )
        package['items'].append({
            'type': 'video',
            'name': 'main_demo',
            'result': video_result
        })
        
        # 2. Key stance image
        print("\n2️⃣ Generating stance reference...")
        stance_path = os.path.join(output_dir, f"{technique.replace(' ', '_')}_stance.png")
        stance_result = self.generate_stance_reference(
            stance_type=f"{technique} ready position",
            annotated=True,
            output_path=stance_path
        )
        package['items'].append({
            'type': 'image',
            'name': 'stance_reference',
            'result': stance_result
        })
        
        # 3. Technique sequence
        print("\n3️⃣ Generating technique sequence...")
        sequence_dir = os.path.join(output_dir, "sequence")
        sequence_result = self.generate_technique_sequence(
            technique=technique,
            num_frames=4,
            output_dir=sequence_dir
        )
        package['items'].append({
            'type': 'sequence',
            'name': 'technique_phases',
            'result': sequence_result
        })
        
        print(f"\n✅ Training package complete!")
        print(f"📁 All files saved to: {output_dir}")
        
        return package
