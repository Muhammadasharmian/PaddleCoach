# PaddleCoach Testing Suite

## Overview
This directory contains the testing suite for PaddleCoach's AI-powered commentary system, integrating Gemini API for text generation and ElevenLabs for text-to-speech.

## Test Files

### 1. `test_config.py` - Configuration Verification
**Purpose**: Quick test to verify API keys and service configuration

**Usage**:
```bash
python tests/test_config.py
```

**What it tests**:
- Environment variable configuration
- API key validation
- Basic text generation
- Basic audio generation

### 2. `test_integration.py` - Full Integration Tests
**Purpose**: Comprehensive testing of all commentary features

**Usage**:
```bash
python tests/test_integration.py
```

**What it tests**:
- AI commentary text generation with various event types
- Audio generation from text
- Full pipeline integration (event → text → audio)
- Multiple voice options
- Batch processing

## Setup

### 1. Environment Configuration
Create a `.env` file in the `tests` directory with your API keys:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
```

### 2. Install Dependencies
Make sure you have installed the required packages:

```bash
pip install -r requirements_frontend.txt
```

## Test Output

### Generated Files
- `tests/audio_output/` - Test audio files from individual audio generation tests
- `tests/integration_output/` - Audio files from full integration tests
- `tests/config_test_audio.mp3` - Quick configuration test audio file

## Commentary Service

The main service is located at:
```
src/frontend/ui_services/commentary_service.py
```

### Usage Example

```python
from src.frontend.ui_services.commentary_service import CommentaryService, VOICES

# Initialize service
service = CommentaryService()

# Generate commentary for an event
event_data = {
    'player_name': 'John Doe',
    'event_type': 'point',
    'context': 'with a powerful smash',
    'score': {'player1': 5, 'player2': 3}
}

# Get text commentary
text = service.generate_commentary_text(event_data)

# Generate audio
audio_bytes = service.generate_audio(text, output_path="commentary.mp3")

# Or do both at once
result = service.generate_full_commentary(
    event_data, 
    audio_output_path="commentary.mp3",
    voice_id=VOICES['ANTONI']
)
```

## Available Voices

The service supports multiple ElevenLabs voices:

- **ADAM**: Young male voice (energetic)
- **ANTONI**: Well-rounded male voice (default, professional)
- **BELLA**: Soft female voice (warm)
- **JOSH**: Deep male voice (authoritative)
- **DOMI**: Strong female voice (confident)

Change voice by passing the `voice_id` parameter:
```python
service.generate_audio(text, voice_id=VOICES['JOSH'])
```

## Event Types

The commentary service supports various event types:

1. **point** - Player scores a point
   - Include `context` for shot description
   
2. **game_win** - Player wins a game
   - Include current score
   
3. **set_win** - Player wins a set
   - Include set score (e.g., "2-1")
   
4. **match_win** - Player wins the match
   - Include final score

## Integration with Main Application

To integrate commentary into your application:

```python
from src.frontend.ui_services.commentary_service import CommentaryService

# In your match tracking code
commentary_service = CommentaryService()

# When a point is scored
event = {
    'player_name': player.name,
    'event_type': 'point',
    'context': 'with an excellent forehand',
    'score': current_score
}

commentary = commentary_service.generate_full_commentary(event)
# commentary['text'] - the text
# commentary['audio_bytes'] - the audio data
```

## Troubleshooting

### "API key not found"
- Ensure `.env` file exists in `tests/` directory
- Check that API keys are properly formatted
- Run `test_config.py` to diagnose

### "Audio generation failed"
- Verify ElevenLabs API key is valid
- Check internet connection
- Ensure you haven't exceeded API quota

### "Import errors"
- Run from project root directory
- Ensure all dependencies are installed
- Check Python version (3.8+ required)

## Next Steps

After successful testing:
1. Integrate commentary service into Flask app
2. Add real-time commentary during live matches
3. Connect to match event system
4. Add WebSocket broadcasting for audio playback
