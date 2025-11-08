# PaddleCoach - Task Division & Collaboration Strategy

## Team Members
- **Ashwani**
- **Mohnish**
- **Ashar**
- **Raks**

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
  - `yolo_tracker.py` - YOLOv12N integration
  - `faster_rcnn_tracker.py` - FasterRCNN integration
  - `tracking_interface.py` - ITrackingData interface
  - `ball_tracker.py` - Ball position tracking
  - `player_tracker.py` - Player movement tracking

#### Dependencies:
- OpenCV, PyTorch, YOLOv12N, FasterRCNN models
- No dependencies on other team members initially

#### Deliverables:
1. Complete data model classes with all attributes and methods
2. Vision system that outputs ball/player coordinates
3. ITrackingData interface for other components to consume

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

### 🔴 Raks - UserExperience & Frontend

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
- YOLOv12N documentation
- OpenCV Python tutorials
- Object-oriented design patterns

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

**Last Updated**: November 7, 2025
**Next Review**: Week 2 Integration Meeting
