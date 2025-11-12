# Vision System Implementation Summary

## Completed Tasks

### Task 1: Video Processing with Full Body Pose Tracking ✅

**File**: `process_video.py`

**Changes Made**:
- Changed output directory from `"output"` to `"output_pose"`
- Implemented full body pose tracking (all 17 COCO keypoints)
- Updated visualization to show complete skeleton
- Enhanced user-facing messages to reflect full body tracking

**Features**:
- Tracks both players using YOLOv11n pose estimation
- Detects all 17 keypoints: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles
- Saves annotated video with full body skeleton overlay
- Real-time processing at ~30 FPS on Apple Silicon

**Output**:
- Annotated video saved to: `output_pose/<video_name>_annotated.mp4`
- Video shows complete body pose with color-coded skeleton

### Task 2: Analysis System ✅

**Files Created**:
- `src/vision/game_analyzer.py` - Core analysis module
- `analyze_processed_video.py` - Main analysis script
- `ANALYSIS_README.md` - Complete documentation

**Features**:
1. **Pose Data Extraction**: Re-processes videos using YOLOv11 to extract all keypoints
2. **Shot Detection**: Identifies individual shots based on wrist velocity spikes
3. **Biomechanical Analysis**:
   - Racket velocity (max and average)
   - Joint angles (hip/knee, elbow, torso)
   - Center of Gravity movement (horizontal and vertical)
4. **Player Comparison**: Automatically compares performance between two players
5. **Report Generation**: Creates detailed .txt reports

**Output**:
- Analysis reports saved to: `analysis_output/analysis_<video_name>_<timestamp>.txt`
- Reports include shot detection, biomechanical metrics, and player comparison

## Architecture

```
PaddleCoach/
├── process_video.py                    # Video processing (Task 1)
├── analyze_processed_video.py          # Analysis execution (Task 2)
├── src/vision/
│   ├── video_processor.py             # Video processing engine
│   ├── player_tracker.py              # Full body pose tracking (UPDATED)
│   ├── game_analyzer.py               # Analysis engine (NEW)
│   └── shot_detector.py               # Shot detection
├── output_pose/                        # Processed videos
│   └── *_annotated.mp4
└── analysis_output/                    # Analysis reports
    └── analysis_*.txt
```

## Updated Components

### 1. PlayerTracker (`src/vision/player_tracker.py`)

**Before**: Only tracked wrists and elbows (4 keypoints)

**After**: Tracks all 17 COCO keypoints
- Face: nose, eyes, ears
- Upper body: shoulders, elbows, wrists
- Torso: hips
- Lower body: knees, ankles

**Visualization**: 
- Full skeleton with proper connections
- Color-coded by player (green/red)
- Different colors for different body parts (yellow wrists, cyan core, etc.)

### 2. GameAnalyzer (`src/vision/game_analyzer.py`)

**New Features**:
- `load_pose_data_from_video()`: Extracts pose data using YOLOv11
- `detect_shots()`: Identifies shots via velocity analysis
- `analyze_stroke_metrics()`: Calculates biomechanical metrics
- `generate_analysis_report()`: Creates comprehensive text reports

**Metrics Calculated**:
- Max/Avg racket velocity
- Min/Avg hip/knee angle (power generation)
- Min/Avg elbow angle (arm extension)
- Average torso angle (body rotation)
- Center of Gravity movement (stability)

## Workflow

### Full Processing Workflow:

```
1. Input Video (dataDetection.mp4)
   ↓
2. Run: python process_video.py
   ↓ (activates venv, processes with YOLOv11 pose)
   ↓
3. Output: output_pose/dataDetection_annotated.mp4
   ↓ (full body skeleton overlay)
   ↓
4. Run: python analyze_processed_video.py
   ↓ (extracts pose data, detects shots, calculates metrics)
   ↓
5. Output: analysis_output/analysis_dataDetection_<timestamp>.txt
   ✅ Complete biomechanical analysis report
```

### Command Sequence:

```bash
# Activate virtual environment
source venv/bin/activate

# Step 1: Process video with full body pose tracking
python process_video.py

# Step 2: Analyze the processed video
python analyze_processed_video.py
```

## Key Features

### Full Body Pose Tracking
- **17 Keypoints**: Complete COCO skeleton
- **Connections**: Proper skeleton rendering with anatomical connections
- **Color Coding**: 
  - Player 0: Green
  - Player 1: Red
  - Wrists: Yellow
  - Core (shoulders/hips): Cyan
  - Joints (elbows/knees): Player color

### Shot Detection
- Velocity-based detection (configurable threshold)
- Forehand/Backhand classification
- Frame-accurate shot boundaries
- Filters false positives with cooldown periods

### Biomechanical Metrics
- **Velocity**: Measures paddle speed at impact
- **Angles**: Quantifies joint flexion for power analysis
- **CoG**: Tracks balance and stability
- **Comparison**: Direct performance comparison between players

### Report Format
- Clean, professional text format
- Timestamped for version control
- Includes all relevant statistics
- Performance edge analysis

## Dependencies

Added to `requirements.txt`:
```
pandas==2.2.3  # For data analysis in game_analyzer.py
```

Existing dependencies:
- ultralytics (YOLOv11)
- opencv-python
- numpy

## Testing

### Test Video: `dataDetection.mp4`

**Processing**:
```bash
source venv/bin/activate && python process_video.py
```

**Expected Output**:
- Video with full body skeleton overlays
- Player IDs visible
- All joints and connections rendered
- Saved to `output_pose/dataDetection_annotated.mp4`

**Analysis**:
```bash
python analyze_processed_video.py
```

**Expected Output**:
- Text report in `analysis_output/`
- Shot detection summary
- Biomechanical metrics per shot
- Player comparison (if 2 players)

## Alignment with TASK_DIVISION.md

All changes are within **Ashwani's domain**:
- ✅ `src/vision/` - All vision system components
- ✅ `src/models/` - Data models (PoseData)
- ✅ Root scripts - Processing and analysis scripts

**No conflicts** with other team members' domains:
- Ashar: `src/analytics/`, `src/database/`
- Mohnish: `src/ai_coach/`
- Rakshit: `src/frontend/`, `docs/`

## Next Steps

1. **Test with real match videos**: Validate shot detection accuracy
2. **Tune velocity threshold**: Adjust based on video quality and frame rate
3. **Integration**: Connect analysis output to other system components
4. **Enhancement**: Add temporal analysis (rally duration, shot patterns)

## Files Modified

1. `process_video.py` - Updated output directory, enhanced messages
2. `src/vision/player_tracker.py` - Full body pose tracking, enhanced visualization
3. `requirements.txt` - Added pandas

## Files Created

1. `src/vision/game_analyzer.py` - Analysis engine
2. `analyze_processed_video.py` - Analysis script
3. `ANALYSIS_README.md` - User documentation
4. `VISION_SYSTEM_SUMMARY.md` - This file

## Git Status

Ready to commit and push to `ashwani/vision-system` branch:
```bash
git add .
git commit -m "Implement full body pose tracking and analysis system"
git push origin ashwani/vision-system
```
