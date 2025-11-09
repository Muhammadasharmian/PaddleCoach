# PaddleCoach - Task Division & Collaboration Strategy

## Team Members
- **Ashwani**
- **Mohnish**
- **Ashar**
- **Rakshit**

---

## 🎯 Division Strategy (Minimizing Merge Conflicts)

The project is divided into **4 independent subsystems** based on the Component Diagram. Each person owns a complete vertical slice, ensuring minimal file overlap.

---

## 👥 Task Assignments

### 🔵 Ashwani - VisionSystem & Core Data Models

**Responsibility**: Foundation layer - tracking and data structures

#### Files/Directories:
- `src/models/` - All core data classes
  - `match.py` - Match class
  - `game.py` - Game class
  - `point.py` - Point class
  - `shot.py` - Shot class
  - `player_profile.py` - PlayerProfile class
  - `pose_data.py` - PoseData class
- `src/vision/` - Vision tracking system
  - `ball_tracker.py` - YOLO-based ball detection and tracking (using bettertrainedYolov11.pt)
  - `player_tracker.py` - Player movement tracking with YOLOv11 pose estimation
  - `tracking_interface.py` - ITrackingData interface
  - `video_processor.py` - MP4 video processing and frame analysis
  - `shot_detector.py` - Shot/stroke detection based on pose analysis

#### Dependencies:
- OpenCV, NumPy
- No dependencies on other team members initially

#### Deliverables:
1. Complete data model classes with all attributes and methods
2. YOLO-based ball tracking system using bettertrainedYolov11.pt (detects "ball" class)
3. MP4 video processing pipeline for real-time and recorded match analysis
4. ITrackingData interface for other components to consume
5. Shot detection system based on pose keypoint analysis

---

### 🟢 Ashar - AnalyticsService & Database Layer

**Responsibility**: Game logic, scoring, and persistence

#### Files/Directories:
- `src/analytics/` - Analytics service components
  - `shot_analyzer.py` - ShotAnalyzer (processes shots, event publisher)
  - `score_tracker.py` - ScoreTracker (real-time scoring)
  - `analytics_interface.py` - IAnalyticsData interface
- `src/database/` - Database management
  - `game_db_manager.py` - GameDB_Manager (MySQL operations)
  - `stats_db_manager.py` - StatsDB_Manager (MySQL operations)
  - `schema.sql` - Database schema definitions
  - `migrations/` - Database migration scripts
- `config/` - Configuration files
  - `database_config.yaml` - DB connection settings
  - `analytics_config.yaml` - Analytics parameters

#### Dependencies:
- Depends on Ashwani's data models (Match, Game, Point, Shot, etc.)
- MySQL, SQLAlchemy/PyMySQL

#### Deliverables:
1. Complete MySQL database schema with all tables
2. ShotAnalyzer that processes vision data and publishes events
3. ScoreTracker for real-time game state management
4. Database managers with CRUD operations

---

### 🟡 Mohnish - AICoachingSuite (All 3 Modules)

**Responsibility**: AI-powered coaching and analysis

#### Files/Directories:
- `src/ai_coach/` - AI coaching modules
  - `pro_comparison_module.py` - Module 3A (offline pose comparison)
  - `visual_demo_module.py` - Module 3B (synthetic video generation)
  - `live_coach_module.py` - Module 3C (real-time coaching)
  - `ai_interface.py` - Common interfaces for AI modules
- `src/ai_coach/utils/` - AI utilities
  - `mediapipe_wrapper.py` - MediaPipe pose estimation
  - `gemini_client.py` - Gemini API wrapper
  - `veo_client.py` - Veo 3.1 API client
  - `nano_banana_client.py` - Nano Banana API client
- `prompts/` - AI prompt templates
  - `pro_comparison_prompts.txt`
  - `live_coach_prompts.txt`
  - `rag_knowledge_base.json`

#### Dependencies:
- Depends on Ashar's IAnalyticsData interface to read game data
- Depends on Ashwani's data models (PoseData, Shot, Match, etc.)
- Google Gemini API, MediaPipe, Veo 3.1, Nano Banana

#### Deliverables:
1. ProComparison module that compares user vs pro technique
2. VisualDemo module for generating demonstration videos
3. LiveCoach module with real-time RAG-based feedback
4. All AI API integrations and wrappers

---

### 🔴 Rakshit - UserExperience & Frontend

**Responsibility**: User interface and presentation layer

#### Files/Directories:
- `src/frontend/` - Web UI components
  - `app.py` - Main Flask/FastAPI application
  - `static/` - CSS, JavaScript, images
    - `css/styles.css`
    - `js/app.js`
    - `js/stats_visualizer.js`
  - `templates/` - HTML templates
    - `index.html`
    - `match_view.html`
    - `player_stats.html`
    - `coaching_dashboard.html`
- `src/ui_services/` - UI backend services
  - `stats_bot.py` - Conversational stats interface
  - `elevenlabs_client.py` - ElevenLabs TTS integration
  - `ui_data_service.py` - Data fetching for UI
- `docs/` - Documentation
  - `API_DOCUMENTATION.md`
  - `USER_GUIDE.md`
  - `DEPLOYMENT.md`

#### Dependencies:
- Depends on Ashar's IAnalyticsData interface for stats
- Depends on Mohnish's AI modules for coaching display
- Flask/FastAPI, ElevenLabs API, Chart.js/D3.js

#### Deliverables:
1. Complete web interface with all views
2. Real-time score display and match tracking
3. Stats visualization dashboard
4. StatsBot conversational interface
5. Integration with ElevenLabs for commentary

---

## 🔄 Integration Points (Careful Coordination Needed)

### Week 1-2: Independent Development
Everyone works on their own modules without dependencies.

### Week 3: First Integration
- **Ashwani → Ashar**: Data models available for database schema
- **Ashar → Mohnish**: IAnalyticsData interface defined
- **Ashar → Raks**: IAnalyticsData interface defined

### Week 4: Second Integration
- **Mohnish → Raks**: AI coaching outputs available for UI display
- **Ashwani → Ashar**: VisionSystem → AnalyticsService pipeline working

### Week 5: Full System Integration
- All components tested together
- End-to-end testing of complete workflow

---

## 📁 Repository Structure (No File Conflicts)

```
PaddleCoach/
├── src/
│   ├── models/              # Ashwani's domain
│   ├── vision/              # Ashwani's domain
│   ├── analytics/           # Ashar's domain
│   ├── database/            # Ashar's domain
│   ├── ai_coach/            # Mohnish's domain
│   └── frontend/            # Raks's domain
│       ├── static/          # Raks's domain
│       ├── templates/       # Raks's domain
│       └── ui_services/     # Raks's domain
├── config/                  # Ashar's domain (shared configs)
├── prompts/                 # Mohnish's domain
├── docs/                    # Raks's domain
├── tests/                   # Shared (each person tests their modules)
│   ├── test_models/         # Ashwani
│   ├── test_vision/         # Ashwani
│   ├── test_analytics/      # Ashar
│   ├── test_database/       # Ashar
│   ├── test_ai_coach/       # Mohnish
│   └── test_frontend/       # Raks
├── requirements.txt         # Shared (coordinate before merging)
├── README.md                # Shared (Raks writes, others review)
└── .gitignore               # Shared (set up once)
```

---

## 🚦 Merge Conflict Prevention Rules

### 1. **Strict Directory Ownership**
- Each person ONLY modifies files in their assigned directories
- Never edit another person's directory without explicit communication

### 2. **Shared Files Protocol**
For files that multiple people touch (`requirements.txt`, `README.md`, etc.):
- **Coordinate in Slack/Discord before editing**
- **Pull latest changes before making modifications**
- **Merge frequently (daily if possible)**

### 3. **Interface-First Development**
- Define interfaces (ITrackingData, IAnalyticsData, etc.) in Week 1
- Everyone codes to interfaces, not implementations
- Allows parallel development without waiting

### 4. **Branch Strategy**
```
main (protected)
├── ashwani/vision-system
├── ashar/analytics-db
├── mohnish/ai-coaching
└── raks/frontend-ui
```
- Each person works on their feature branch
- Only merge to main after team review
- Use Pull Requests for all merges

### 5. **Communication Checkpoints**
- **Daily**: Quick standup (5 min) - "What did I do? What am I blocked on?"
- **Weekly**: Integration meeting - Test interfaces between components
- **As-needed**: Slack/Discord for quick questions

---

## 📊 Progress Tracking

### Week 1-2: Foundation Phase
- [ ] Ashwani: Data models + Vision system core
- [ ] Ashar: Database schema + DB managers
- [ ] Mohnish: AI API integrations + basic modules
- [ ] Raks: Frontend scaffold + basic UI

### Week 3: Integration Phase 1
- [ ] Ashwani → Ashar: Models integrated with DB
- [ ] Ashar: Interfaces defined and documented
- [ ] Mohnish: First AI module working (ProComparison)
- [ ] Raks: UI consuming mock data

### Week 4: Integration Phase 2
- [ ] Full pipeline: Vision → Analytics → Database
- [ ] AI modules consuming real game data
- [ ] UI displaying real-time stats

### Week 5: Polish & Testing
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Documentation
- [ ] Demo preparation

---

## 🛠️ Development Setup (Common for All)

### Prerequisites
```bash
# Python 3.10+
python --version

# Virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

```bash
# Clone repo
git clone <repo-url>
cd PaddleCoach

# Create your branch
git checkout -b <yourname>/<feature>

# Daily routine
git pull origin main  # Get latest changes
# ... do your work ...
git add <your-files-only>
git commit -m "Descriptive message"
git push origin <yourname>/<feature>

# When ready to merge
# Create Pull Request on GitHub
# Request review from team
# Merge after approval
```

---

## 🎯 Success Criteria

### No Merge Conflicts
- Each person owns distinct directories
- Shared files are coordinated
- Frequent small merges instead of big dumps

### Clean Interfaces
- Components communicate through well-defined interfaces
- No tight coupling between modules
- Easy to test in isolation

### Parallel Progress
- No team member blocked waiting for others
- Mock data/interfaces allow independent development
- Integration happens incrementally

---

## 📞 Contact & Coordination

### Quick Questions
- Use team chat (Slack/Discord)
- Response expected within 2 hours during work hours

### Interface Changes
- Announce in team channel BEFORE making changes
- Update documentation immediately
- Notify dependent team members

### Blockers
- Raise immediately in team channel
- Schedule quick call if needed
- Don't wait until next meeting

---

## 🎓 Learning Resources

### Ashwani (Vision & Models)
- OpenCV Python tutorials (color space conversion, contour detection)
- HSV color space and morphological operations
- Object-oriented design patterns
- Video processing with OpenCV (cv2.VideoCapture)

### Ashar (Analytics & Database)
- MySQL + Python integration
- SQLAlchemy ORM
- Event-driven architecture

### Mohnish (AI Coaching)
- Google Gemini API docs
- MediaPipe Pose documentation
- RAG (Retrieval-Augmented Generation) concepts

### Raks (Frontend)
- Flask/FastAPI tutorials
- Real-time web updates (WebSockets)
- Chart.js for data visualization

---

## 📋 IMPLEMENTATION STATUS & DOCUMENTATION

### 🔵 Ashwani - Vision System (COMPLETED ✅)

#### Implemented Components

**1. Full Body Pose Tracking System**
- File: `process_video.py`
- Tracks all 17 COCO keypoints (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles)
- Real-time processing at ~13 FPS on Apple Silicon
- Output: `output_pose/<video_name>_annotated.mp4`
- Features:
  - Complete skeleton visualization with anatomical connections
  - Color-coded by player (Player 0: Green, Player 1: Red)
  - Different colors for body parts (wrists: yellow, core: cyan)
  - Player ID tracking across frames

**2. Biomechanical Analysis System**
- File: `src/vision/game_analyzer.py`
- Script: `analyze_processed_video.py`
- Features:
  - Re-processes videos to extract pose data using YOLOv11
  - Shot detection based on wrist velocity spikes
  - Forehand/Backhand classification
  - Biomechanical metrics calculation:
    * Racket velocity (max and average)
    * Joint angles (hip/knee, elbow, torso)
    * Center of Gravity movement (horizontal/vertical)
  - Player performance comparison
  - Detailed .txt report generation in `analysis_output/`

**3. Key Files**
- `src/vision/player_tracker.py` - Full body pose tracking (17 keypoints)
- `src/vision/video_processor.py` - Video processing engine
- `src/vision/game_analyzer.py` - Analysis and metrics calculation
- `src/vision/shot_detector.py` - Shot detection logic
- `src/models/pose_data.py` - Pose data structures

**4. Performance Optimizations**
- Apple Silicon (MPS) GPU acceleration
- FP16 half-precision inference for faster processing
- Frame downsampling (60 FPS → 30 FPS processing)
- Optimized for real-time performance on M1/M2/M3 chips

**5. Workflow**
```bash
# Step 1: Process video with pose tracking
python process_video.py
# Output: output_pose/dataDetection_annotated.mp4

# Step 2: Generate biomechanical analysis
python analyze_processed_video.py
# Output: analysis_output/analysis_<video>_<timestamp>.txt
```

**6. Analysis Report Contents**
- Video information (FPS, frame count, duration)
- Shot detection summary (total shots, forehand/backhand breakdown)
- Detailed biomechanical metrics per shot:
  * Max/Avg racket velocity
  * Min/Avg hip/knee angle (power generation)
  * Min/Avg elbow angle (arm extension)
  * Average torso angle (body rotation)
  * Center of Gravity movement (stability)
- Player comparison (if 2 players detected)
- Performance edge analysis

**7. Dependencies Added**
- `pandas==2.2.3` - For data analysis in game_analyzer.py
- Existing: ultralytics, opencv-python, numpy

**8. Test Results (dataDetection.mp4)**
- Video: 81 seconds, 4861 frames (60 FPS)
- Processing: 2431 frames at 30 FPS target
- Player 1: 157 shots detected (104 forehand, 53 backhand)
- Player 2: 151 shots detected (94 forehand, 57 backhand)
- Performance: Player 2 has 9.6% faster average racket speed
- Detection rates: >89% for wrists, >90% for all keypoints

---

### 🏗️ System Architecture Overview

#### UML Class Structure (from ping_pong_uml.md)

**Core Classes**:
1. **Match** - Represents complete match between two players
   - Attributes: matchID, player1Name, player2Name, startTime, games
   - Methods: startMatch(), endMatch(), getWinner()
   - Composition with Game (1 Match contains 1..* Games)

2. **Game** - Single game within a match
   - Attributes: gameID, player1Score, player2Score
   - Methods: addPoint(), isGameOver(), getGameWinner()
   - Contains 0..* Shots

3. **PlayerProfile** - Player statistics and history
   - Attributes: playerID, playerName, totalWins, totalLosses
   - Methods: getForehandRatio(), getMatchHistory()

4. **Shot** - Individual shot data from vision tracking
   - Attributes: shotID, timestamp, start_x, start_y, end_x, end_y, speed, type
   - Methods: calculateSpeed()
   - Currently implemented in vision system

5. **Point** - Single point in a game
   - Attributes: pointID, gameID, videoFile, shots
   - Contains multiple shots per rally

6. **PoseData** - Pose keypoint data (IMPLEMENTED)
   - 17 COCO keypoints per player per frame
   - Stored in all_keypoints dictionary
   - Used for biomechanical analysis

**Component Interactions**:
```
VisionSystem (Ashwani) → ITrackingData → AnalyticsService (Ashar)
AnalyticsService → IAnalyticsData → AICoachingSuite (Mohnish)
IAnalyticsData → UserExperience (Rakshit)
AICoachingSuite → UserExperience
```

---

### 🎯 Next Integration Steps

#### Week 3-4: Analytics Integration (Ashar)
1. **Consume Vision System Output**
   - Read pose data from `output_pose/` videos
   - Parse analysis reports from `analysis_output/`
   - Store shot data in database

2. **Shot Analysis Pipeline**
   - Integrate with `src/vision/game_analyzer.py`
   - Process biomechanical metrics
   - Store in MySQL database

3. **Interface Definition**
   ```python
   class IAnalyticsData:
       def get_shot_statistics(player_id: str) -> Dict
       def get_match_summary(match_id: str) -> Dict
       def get_player_performance(player_id: str) -> Dict
   ```

#### Week 4-5: AI Coaching Integration (Mohnish)
1. **ProComparison Module**
   - Load pose data from vision system
   - Compare with pro player database
   - Generate technique feedback

2. **LiveCoach Module**
   - Real-time pose analysis
   - RAG-based coaching tips
   - Gemini API integration

3. **Input Data**
   - Use `output_pose/*_annotated.mp4` videos
   - Parse `analysis_output/*.txt` reports
   - Access pose keypoints from PoseData objects

#### Week 5: Frontend Integration (Rakshit)
1. **Display Components**
   - Video playback with pose overlay
   - Shot statistics dashboard
   - Biomechanical metrics visualization
   - Player comparison charts

2. **Data Sources**
   - IAnalyticsData interface (from Ashar)
   - AI coaching feedback (from Mohnish)
   - Direct video playback from `output_pose/`

---

### 📊 Performance Benchmarks (Apple Silicon)

**Video Processing (process_video.py)**:
- Input: 81-second video (4861 frames @ 60 FPS)
- Processing: ~3 minutes (13.3 FPS average)
- Output: 135 MB annotated video
- GPU Utilization: 85% (MPS)
- RAM Usage: ~2.1 GB

**Analysis System (analyze_processed_video.py)**:
- Input: 2431 frames from annotated video
- Processing: ~1 minute
- Output: Text report (~50 KB)
- Detections: 4769 pose detections (2 players)
- Accuracy: >90% keypoint detection rate

---

### 🔧 Development Commands

**Setup**:
```bash
# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Vision System**:
```bash
# Process video with pose tracking
python process_video.py

# Generate analysis report
python analyze_processed_video.py

# Or specify custom video
python analyze_processed_video.py path/to/video.mp4
```

**Git Workflow**:
```bash
# Current branch
git branch
# * ashwani/visionPLUSfrontend

# View changes
git status

# Commit and push
git add .
git commit -m "Description"
git push origin ashwani/visionPLUSfrontend
```

---

### 📁 Current Repository Structure

```
PaddleCoach/
├── src/
│   ├── models/
│   │   └── pose_data.py          # ✅ IMPLEMENTED
│   └── vision/
│       ├── player_tracker.py     # ✅ IMPLEMENTED (17 keypoints)
│       ├── video_processor.py    # ✅ IMPLEMENTED
│       ├── game_analyzer.py      # ✅ IMPLEMENTED (NEW)
│       └── shot_detector.py      # ✅ IMPLEMENTED
├── process_video.py               # ✅ IMPLEMENTED
├── analyze_processed_video.py    # ✅ IMPLEMENTED (NEW)
├── output_pose/                   # Generated videos
│   └── *_annotated.mp4
├── analysis_output/               # Analysis reports
│   └── analysis_*.txt
├── requirements.txt               # ✅ Updated (added pandas)
├── TASK_DIVISION.md              # This file
└── README.md                      # Project overview
```

---

### 🎓 Technical Documentation Summary

**Vision System Architecture**:
- YOLOv11n-pose model for human pose estimation
- 17 COCO keypoints: nose, eyes (2), ears (2), shoulders (2), elbows (2), wrists (2), hips (2), knees (2), ankles (2)
- Player ID assignment based on spatial proximity across frames
- Hungarian algorithm for consistent player tracking

**Biomechanical Analysis**:
- Wrist velocity calculation: `distance * fps` between frames
- Joint angle calculation: Using vector mathematics (dot product, arccos)
- Center of Gravity: Average of torso and leg keypoint positions
- Shot detection: Velocity spike threshold (default 1000 px/s)

**Optimization Techniques**:
- Frame skipping for target FPS
- FP16 half-precision inference
- Apple MPS (Metal Performance Shaders) backend
- Minimal data storage (only essential keypoints in analysis)

---

**Last Updated**: November 8, 2025
**Next Milestone**: Frontend integration with vision system output
