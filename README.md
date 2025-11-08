# PaddleCoach - Table Tennis Analysis System

AI-powered table tennis coaching system with computer vision and pose estimation.

**⚡ Optimized for Apple Silicon (M1/M2/M3) - Real-time Performance**

## Features

- **YOLOv11n Pose Estimation**: Track two players simultaneously
- **Real-time Processing**: ~30 FPS on Apple Silicon with MPS acceleration
- **Efficient Tracking**: Only tracks essential keypoints (wrists & elbows)
- **Compact JSON Output**: Optimized for Gemini 2.5 Pro API
- **Arm Swing Analysis**: Calculate paddle angles and movement patterns

## Installation

```bash
# Install dependencies
pip install ultralytics opencv-python numpy

# The system will automatically use Apple MPS (Metal Performance Shaders)
```

## Quick Start

### Process a Video (Real-time)

```bash
python process_video.py
```

This will process `IMG_7622.mp4` at ~30 FPS with real-time visualization.

### Controls During Processing

- **`p`** - Pause/Resume
- **`q`** - Quit
- **`SPACE`** - Toggle visualization (hide for maximum speed)

## Output

The system generates a compact JSON file optimized for AI analysis:

### JSON Structure (Compact)

```json
{
  "metadata": {
    "video_file": "IMG_7622.mp4",
    "video_info": {
      "resolution": "1920x1080",
      "original_fps": 60,
      "processed_fps": 30,
      "duration_seconds": 81.02
    },
    "tracking_info": {
      "keypoints_tracked": ["left_wrist", "left_elbow", "right_wrist", "right_elbow"]
    }
  },
  "player_0": [
    {
      "frame": 0,
      "time": 0.0,
      "player": 0,
      "left_wrist": {"x": 640.5, "y": 480.2, "confidence": 0.95},
      "left_elbow": {"x": 600.1, "y": 450.3, "confidence": 0.92},
      "right_wrist": {"x": 720.3, "y": 490.1, "confidence": 0.94},
      "right_elbow": {"x": 680.2, "y": 460.5, "confidence": 0.91},
      "angles": {
        "left_arm": 125.5,
        "right_arm": 118.2
      }
    }
  ],
  "player_1": [...]
}
```

## Tracked Keypoints

Each player has 4 keypoints tracked:
- **Left wrist** - Paddle position (dominant hand for lefties)
- **Left elbow** - Arm swing analysis
- **Right wrist** - Paddle position (dominant hand for righties)  
- **Right elbow** - Arm swing analysis

## Performance Optimization

### Apple Silicon (M-series)
- Uses **MPS** (Metal Performance Shaders) for GPU acceleration
- **FP16** half-precision for faster inference
- Processes at **~30 FPS** in real-time
- Only tracks 4 keypoints (vs 17) for 4x less data

### Processing Speed
- **60 FPS video** → downsampled to 30 FPS processing
- **80-second video** → ~80 seconds processing time (1:1 ratio)
- **File size**: ~500 KB JSON (vs 30+ MB with all keypoints)

## Next Steps: Gemini 2.5 Pro Integration

The JSON output is designed to be fed into Gemini 2.5 Pro API for:
- Shot analysis and classification
- Technique comparison with professional players
- Real-time coaching feedback
- Performance metrics calculation

## Project Structure

```
PaddleCoach/
├── src/
│   ├── models/
│   │   └── pose_data.py          # PoseData and Keypoint classes
│   └── vision/
│       ├── player_tracker.py     # YOLOv11n player tracking
│       └── video_processor.py    # Video processing pipeline
├── output/                        # Generated files
│   ├── *_pose_data.json          # Pose data for Gemini
│   └── *_annotated.mp4           # Annotated videos
├── IMG_7622.mp4                  # Sample video
└── requirements.txt              # Python dependencies
```

## Team

- **Ashwani**: Vision System & Data Models
- **Ashar**: Analytics & Database
- **Mohnish**: AI Coaching (Gemini integration)
- **Rakshit**: Frontend & UX

## License

MIT
