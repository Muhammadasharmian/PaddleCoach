# Game Analysis System

This analysis system extracts biomechanical metrics from processed table tennis videos.

## Overview

The game analyzer performs:
- **Pose Data Extraction**: Re-processes videos to extract detailed pose data
- **Shot Detection**: Identifies individual shots based on wrist velocity spikes
- **Biomechanical Analysis**: Calculates metrics including:
  - Racket velocity (max and average)
  - Joint angles (hip/knee, elbow, torso)
  - Center of Gravity movement
- **Player Comparison**: Compares performance between two players
- **Report Generation**: Creates detailed .txt reports in `analysis_output/`

## Usage

### Basic Usage

```bash
python analyze_processed_video.py
```

This will analyze the default video (`output/output_dataDetection.mp4`) and generate a report.

### Custom Video

```bash
python analyze_processed_video.py path/to/your/video.mp4
```

### Direct Module Usage

```python
from src.vision.game_analyzer import GameAnalyzer

analyzer = GameAnalyzer(output_dir="analysis_output")
report_path = analyzer.generate_analysis_report(
    video_path="output/output_dataPose.mp4",
    velocity_threshold=1000.0,
    fps=30
)
```

## Configuration

### Parameters

- **fps**: Frames per second for velocity calculations (default: 30)
- **velocity_threshold**: Minimum wrist velocity (px/s) to detect a shot (default: 1000.0)
- **output_dir**: Directory for analysis reports (default: "analysis_output")

### Adjusting Shot Detection

If shots are not being detected or too many false positives:

```python
# More sensitive (detects more shots)
analyzer.generate_analysis_report(video_path, velocity_threshold=500.0)

# Less sensitive (fewer false positives)
analyzer.generate_analysis_report(video_path, velocity_threshold=1500.0)
```

## Output

Reports are saved as `.txt` files in `analysis_output/` with the format:
```
analysis_<video_name>_<timestamp>.txt
```

### Report Contents

1. **Video Information**: FPS, frame count, duration
2. **Shot Detection Summary**: Total shots, forehand/backhand breakdown
3. **Biomechanical Metrics** (per shot):
   - Max/Avg racket velocity
   - Min/Avg hip/knee angle
   - Min/Avg elbow angle
   - Average torso angle
   - Center of Gravity movement (horizontal/vertical)
4. **Player Comparison** (if 2 players detected):
   - Average performance metrics
   - Performance edge analysis

## Architecture

### Module Structure

```
src/vision/
├── game_analyzer.py    # Main analysis module (NEW)
├── video_processor.py  # Video processing
├── player_tracker.py   # Pose tracking
└── shot_detector.py    # Shot detection
```

### Analysis Pipeline

```
Input Video (MP4)
    ↓
Pose Detection (YOLOv11)
    ↓
Shot Detection (Velocity Analysis)
    ↓
Biomechanical Metrics
    ↓
Player Comparison
    ↓
Text Report (.txt)
```

## Dependencies

- `ultralytics` (YOLOv11)
- `opencv-python`
- `numpy`
- `pandas`

Make sure pandas is installed:
```bash
pip install pandas==2.2.3
```

## Integration with Workflow

1. **Record/Upload Video**: Get table tennis match video
2. **Process Video**: Run `process_video.py` to generate annotated video
3. **Analyze Performance**: Run `analyze_processed_video.py` to generate metrics
4. **Review Report**: Open `.txt` file in `analysis_output/`

## Example Report

```
======================================================================
         PADDLECOACH - TABLE TENNIS BIOMECHANICAL ANALYSIS
======================================================================

Video: output/output_dataPose.mp4
Analysis Date: 2025-03-15 14:30:00
Processing FPS: 30
Total Frames Analyzed: 1200
Total Detections: 2400

Detected Players: Player_1, Player_2
Number of Players: 2

======================================================================
                           SHOT DETECTION
======================================================================

Player_1:
  Total Shots Detected: 15

  Forehand Shots: 9
  Backhand Shots: 6

  Shot Details (first 10):
    1. Forehand   | Frames   100-  120 | Duration: 0.67s
    2. Backhand   | Frames   145-  165 | Duration: 0.67s
    ...

======================================================================
                      BIOMECHANICAL ANALYSIS
======================================================================

Player_1 - Detailed Stroke Metrics:
----------------------------------------------------------------------

  Shot 1: Forehand (Frames 100-120)
    Racket Metrics:
      Max Velocity:     2345.67 px/s
      Avg Velocity:     1234.56 px/s
    Joint Angles:
      Min Hip/Knee:       145.23° (lower = better loading)
      Avg Hip/Knee:       165.45°
      Min Elbow:          125.67°
      Avg Elbow:          145.89°
      Avg Torso:          175.23°
    Center of Gravity:
      Horizontal Movement:   45.67 px
      Vertical Movement:     12.34 px

...
```

## Notes

- The analyzer re-processes the video with YOLOv11 to ensure accurate pose data
- Shot detection is based on wrist velocity spikes
- Metrics are calculated for individual shots, not entire rallies
- Player IDs are assigned based on position (left vs right in frame)
- Reports are timestamped to prevent overwrites

## Troubleshooting

### No shots detected
- Try lowering `velocity_threshold` (e.g., 500.0)
- Ensure video shows clear player movements
- Check that pose detection is working (keypoints visible)

### Too many false positives
- Increase `velocity_threshold` (e.g., 1500.0)
- Check if video has rapid camera movements

### No pose data loaded
- Ensure `yolo11n-pose.pt` model is available
- Check video file is readable
- Verify video contains visible players

## Future Enhancements

- Real-time analysis during video processing
- JSON output format for integration with other modules
- Advanced shot classification (serve, smash, lob, etc.)
- Rally detection and analysis
- Temporal heatmaps of player movement
- Export to CSV for further analysis
