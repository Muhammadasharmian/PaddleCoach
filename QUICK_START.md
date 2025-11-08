# 🚀 QUICK SETUP GUIDE

## For Teammates Starting with This Code

### 1. Clone and Setup (30 seconds)

```bash
# Clone the repo
git clone https://github.com/Muhammadasharmian/PaddleCoach.git
cd PaddleCoach

# Switch to AI coaching branch
git checkout mohnish/ai-coaching

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Test Everything Works (1 minute)

```bash
# Run the comprehensive test
python examples/test_all_modules.py

# If you see "🎉 ALL TESTS PASSED! 🎉" you're good to go!
```

### 3. Try Individual Modules (2 minutes)

```bash
# Test Pro Comparison
python examples/example_pro_comparison.py

# Test Visual Demo
python examples/example_visual_demo.py

# Test Live Coach
python examples/example_live_coach.py
```

---

## For Mohnish (Me) - Development Workflow

### Daily Development

```bash
# Always work on your branch
git checkout mohnish/ai-coaching

# Pull latest changes from team
git pull origin main
git merge main  # if there are updates

# Make changes...

# Commit and push
git add .
git commit -m "Your changes here"
git push origin mohnish/ai-coaching
```

### Testing Changes

```bash
# Quick test
python examples/test_all_modules.py

# Test specific module
python examples/example_pro_comparison.py  # or others
```

### Adding New Features

1. Edit files in `src/ai_coach/`
2. Update examples if needed
3. Run tests
4. Commit and push

---

## Integration Checklist

### When Ashwani Finishes Vision System

- [ ] Import real `Match`, `Game`, `Shot`, `PoseData` from his module
- [ ] Replace `from ai_coach.mock_models import ...` with real imports
- [ ] Test with real game data
- [ ] Update examples to use real data

### When Ashar Finishes Analytics

- [ ] Import real `IAnalyticsData` implementation
- [ ] Replace `MockAnalyticsData()` with real instance
- [ ] Test database connectivity
- [ ] Verify player profiles load correctly

### When Connecting to Raks's Frontend

- [ ] Document API response formats
- [ ] Provide example JSON responses
- [ ] Test callback system for real-time tips
- [ ] Ensure video/image URLs are accessible

---

## Common Issues & Solutions

### Import Error: "ai_coach" not found

**Solution:**
```python
# Add to top of your script
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### MediaPipe Not Installing

**Solution:**
```bash
# Windows: Install Visual C++ Build Tools first
# Then:
pip install --upgrade pip
pip install mediapipe
```

### API Key Not Working

**Solution:**
```bash
# Verify it's set
echo $env:GEMINI_API_KEY  # Windows
echo $GEMINI_API_KEY      # Mac/Linux

# Re-set if needed
$env:GEMINI_API_KEY="your-key"
```

---

## File You'll Edit Most Often

```
src/ai_coach/
├── pro_comparison_module.py     # Module 3A logic
├── visual_demo_module.py        # Module 3B logic
├── live_coach_module.py         # Module 3C logic
└── utils/
    ├── gemini_client.py         # Gemini prompts
    └── mediapipe_wrapper.py     # Pose analysis
```

---

## Resources

- **Full Documentation:** `README.md`
- **Completion Summary:** `COMPLETION_SUMMARY.md`
- **Examples:** `examples/` directory
- **Prompts:** `prompts/` directory

---

## Questions?

Check the README first, then reach out to me!

**Happy Coding! 🎉**
