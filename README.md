# 🏓 PaddleCoach - AI Coaching Suite

**Mohnish's AI Coaching Modules for the PaddleCoach Hackathon Project**

This repository contains the AI-powered coaching system for table tennis, consisting of three integrated modules:

- **Module 3A (Pro Comparison)**: Offline analysis comparing user technique with professional players
- **Module 3B (Visual Demo)**: AI-generated demonstration videos and images
- **Module 3C (Live Coach)**: Real-time coaching feedback using RAG

---

## 🎯 Project Overview

PaddleCoach is a comprehensive table tennis helper that uses computer vision and AI to track gameplay, analyze technique, and provide coaching feedback. This AI Coaching Suite is one component of the larger system.

### My Responsibility (Mohnish)

I'm building the **"brain"** of the coaching system - the AI that helps players improve through:
1. **Analyzing** their technique vs. pros
2. **Showing** them perfect form through generated media
3. **Coaching** them in real-time during matches

---

## 📁 Project Structure

```
PaddleCoach/
├── src/ai_coach/                    # Main package
│   ├── __init__.py
│   ├── pro_comparison_module.py     # Module 3A
│   ├── visual_demo_module.py        # Module 3B
│   ├── live_coach_module.py         # Module 3C
│   ├── ai_interface.py              # Interfaces for team integration
│   ├── mock_models.py               # Data models (from teammates)
│   └── utils/                       # Utility clients
│       ├── mediapipe_wrapper.py     # Pose estimation
│       ├── gemini_client.py         # Gemini AI
│       ├── veo_client.py            # Veo 3.1 video generation
│       └── nano_banana_client.py    # Nano Banana images
│
├── prompts/                         # AI prompt templates
│   ├── pro_comparison_prompts.txt
│   ├── live_coach_prompts.txt
│   └── rag_knowledge_base.json      # Pro tips database
│
├── examples/                        # Example usage scripts
│   ├── example_pro_comparison.py
│   ├── example_visual_demo.py
│   └── example_live_coach.py
│
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Muhammadasharmian/PaddleCoach.git
cd PaddleCoach

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up API Keys (Optional)

The modules work in **mock mode** without API keys for testing. For full functionality:

```bash
# Windows PowerShell:
$env:GEMINI_API_KEY="your-gemini-key"
$env:VEO_API_KEY="your-veo-key"
$env:NANO_BANANA_API_KEY="your-nano-banana-key"

# Mac/Linux:
export GEMINI_API_KEY="your-gemini-key"
export VEO_API_KEY="your-veo-key"
export NANO_BANANA_API_KEY="your-nano-banana-key"
```

### 3. Run Examples

```bash
# Test Module 3A (Pro Comparison)
python examples/example_pro_comparison.py

# Test Module 3B (Visual Demo)
python examples/example_visual_demo.py

# Test Module 3C (Live Coach)
python examples/example_live_coach.py
```

---

## 🧩 Module Details

### Module 3A: Pro Comparison

**Offline technique analysis comparing user vs. professional**

**Features:**
- Extract pose data from videos using MediaPipe
- Compare body angles and positioning
- Generate AI-powered analysis using Gemini
- Provide prioritized recommendations

**Example Usage:**
```python
from ai_coach import ProComparisonModule

module = ProComparisonModule()
module.initialize()

result = module.compare_techniques(
    user_video_path="user_forehand.mp4",
    pro_video_path="pro_forehand.mp4",
    shot_type="forehand topspin",
    output_report="analysis.txt"
)

print(result['ai_analysis'])
```

---

### Module 3B: Visual Demo

**Generate AI demonstration videos and images**

**Features:**
- Generate technique videos with Veo 3.1
- Create annotated stance images with Nano Banana
- Produce technique sequences (4-8 frames)
- Create complete training packages

**Example Usage:**
```python
from ai_coach import VisualDemoModule

module = VisualDemoModule()
module.initialize()

# Generate video
result = module.generate_technique_video(
    technique="forehand topspin",
    focus_areas=["hip rotation", "wrist snap"],
    duration=6,
    output_path="demo.mp4"
)

# Generate stance image
result = module.generate_stance_reference(
    stance_type="ready position",
    annotated=True,
    output_path="stance.png"
)
```

---

### Module 3C: Live Coach

**Real-time coaching feedback using RAG**

**Features:**
- Process shots in real-time
- Use RAG with pro tips knowledge base
- Consider player history and game context
- Provide concise, actionable tips

**Example Usage:**
```python
from ai_coach import LiveCoachModule, create_mock_shot

module = LiveCoachModule(
    knowledge_base_path="prompts/rag_knowledge_base.json"
)
module.initialize()

# Register callback for tips
def coaching_callback(tip):
    print(f"COACH: {tip}")

module.register_callback(coaching_callback)

# Start session
module.start_live_session(
    player_id="player_001",
    feedback_frequency="medium"
)

# Process shots
shot = create_mock_shot("shot_001", "forehand")
tip = module.process_shot(shot, "player_001")
```

---

## 🔧 Integration with Team

### Data from Teammates

**From Ashwani (Vision System):**
- `Match`, `Game`, `Point`, `Shot` classes
- `PoseData` class with keypoints and angles

**From Ashar (Analytics):**
- `IAnalyticsData` interface to query game data
- Database access for historical stats

**To Raks (Frontend):**
- Text coaching feedback
- Generated video/image URLs
- Real-time tip streams

### Mock Data for Independent Development

All modules include mock implementations so you can develop and test without waiting for teammates:

```python
from ai_coach import create_mock_shot, create_mock_player_profile, MockAnalyticsData

# Use mock data for testing
shot = create_mock_shot()
profile = create_mock_player_profile()
analytics = MockAnalyticsData()
```

---

## 📚 Knowledge Base (RAG)

The Live Coach uses a knowledge base of 20+ pro tips covering:

- Forehand/backhand technique
- Serve and receive
- Footwork and positioning
- Strategy and shot placement
- Mental game
- Spin variation

Located in: `prompts/rag_knowledge_base.json`

---

## 🧪 Testing

Each module includes:
- Mock mode for testing without API keys
- Example scripts demonstrating usage
- Status checking and error handling

Run all examples:
```bash
python examples/example_pro_comparison.py
python examples/example_visual_demo.py
python examples/example_live_coach.py
```

---

## 🎨 AI Models Used

| Model | Purpose | Provider |
|-------|---------|----------|
| **MediaPipe Pose** | Pose estimation | Google (Free) |
| **Gemini 2.0 Flash** | AI analysis & RAG | Google AI |
| **Veo 3.1** | Video generation | Google (Beta) |
| **Nano Banana** | Image generation | Third-party API |

---

## 🔑 API Keys Setup

### Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Set environment variable: `GEMINI_API_KEY`

### Get Veo API Key
1. Sign up for Google Cloud AI
2. Enable Veo API (currently in beta)
3. Set environment variable: `VEO_API_KEY`

### Get Nano Banana API Key
1. Visit: https://nanobanana.ai
2. Create account and get API key
3. Set environment variable: `NANO_BANANA_API_KEY`

---

## 🐛 Troubleshooting

### Import Errors
```bash
# Make sure you're in the project root
cd PaddleCoach

# Verify Python path includes src/
python -c "import sys; print(sys.path)"
```

### MediaPipe Installation Issues
```bash
# Windows: May need Visual C++ Build Tools
# Mac: May need to upgrade pip
pip install --upgrade pip
pip install mediapipe
```

### API Key Not Working
```bash
# Verify environment variable is set
# Windows:
echo $env:GEMINI_API_KEY

# Mac/Linux:
echo $GEMINI_API_KEY
```

---

## 📊 Development Status

- ✅ Module 3A: Pro Comparison - Complete
- ✅ Module 3B: Visual Demo - Complete
- ✅ Module 3C: Live Coach - Complete
- ✅ Mock data models - Complete
- ✅ Example scripts - Complete
- ⏳ Team integration - Pending teammate modules

---

## 🤝 Team Coordination

**My Branch:** `mohnish/ai-coaching`

**Dependencies:**
- Waiting for Ashwani's data models (using mocks for now)
- Waiting for Ashar's IAnalyticsData implementation (using mocks)

**Ready to Integrate:**
- All three modules are functional
- Mock data allows independent testing
- Clear interfaces defined for integration

---

## 📝 Next Steps

1. **Week 3**: Integrate with Ashwani's real data models
2. **Week 4**: Connect to Ashar's analytics interface
3. **Week 4**: Provide outputs to Raks's frontend
4. **Week 5**: End-to-end testing and polish

---

## 👨‍💻 Author

**Mohnish**  
GitHub: [@mohnish-dev](https://github.com/mohnish-dev)

Part of the PaddleCoach hackathon team:
- Ashwani (Vision System)
- Ashar (Analytics & Database)
- Mohnish (AI Coaching - this module)
- Raks (Frontend & UX)

---

## 📄 License

This project is part of a hackathon. License TBD.

---

## 🎓 Learning Resources

- [MediaPipe Pose](https://google.github.io/mediapipe/solutions/pose.html)
- [Google Gemini API](https://ai.google.dev/docs)
- [RAG (Retrieval-Augmented Generation)](https://arxiv.org/abs/2005.11401)
- [Table Tennis Technique Guides](https://www.youtube.com/c/pingponglife)

---

**Last Updated:** November 7, 2025  
**Version:** 0.1.0
