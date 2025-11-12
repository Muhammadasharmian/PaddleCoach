# PaddleCoach Project Restructure

**Date**: November 10, 2025  
**Purpose**: Better file organization and separation of concerns

## 📁 New Directory Structure

```
PaddleCoach/
├── frontend/                    # All HTML, CSS, JS files
│   ├── index.html
│   ├── ball_tracking.html
│   ├── ball-tracking-record.html
│   ├── ball-tracking-upload.html
│   ├── body-tracking-upload.html
│   ├── analysis-final.html
│   ├── styles.css
│   └── script.js
│
├── backend/                     # All Python processing scripts
│   ├── process_ball_tracking.py
│   ├── process_video.py
│   ├── analyze_processed_video.py
│   ├── demo_video.py
│   ├── server.py
│   └── test_elevenlabs.py
│
├── documentation/               # All documentation files
│   ├── ELEVENLABS_FIX.md
│   ├── FRONTEND_BACKEND_INTEGRATION.md
│   ├── VISION_SYSTEM_SUMMARY.md
│   └── PROJECT_RESTRUCTURE.md  (this file)
│
├── src/                         # Source code modules
│   ├── vision/
│   │   ├── ball_tracker.py
│   │   ├── player_tracker.py
│   │   ├── game_analyzer.py
│   │   └── ...
│   └── models/
│       ├── ball_data.py
│       ├── pose_data.py
│       └── ...
│
├── input/                       # Input videos and data
├── output/                      # Generated outputs
├── app.py                       # Main Flask server (root level)
├── README.md                    # Main documentation
├── TASK_DIVISION.md            # Task division
├── requirements.txt
├── landing_image.png
└── yolo11n-pose.pt
```

## 🔧 Changes Made

### 1. Frontend Files (→ `frontend/`)
Moved all HTML, CSS, and JavaScript files:
- ✅ `index.html`
- ✅ `ball_tracking.html`
- ✅ `ball-tracking-record.html`
- ✅ `ball-tracking-upload.html`
- ✅ `body-tracking-upload.html`
- ✅ `analysis-final.html`
- ✅ `styles.css`
- ✅ `script.js`

### 2. Backend Files (→ `backend/`)
Moved all Python scripts except `app.py`:
- ✅ `process_ball_tracking.py`
- ✅ `process_video.py`
- ✅ `analyze_processed_video.py`
- ✅ `demo_video.py`
- ✅ `server.py`
- ✅ `test_elevenlabs.py`

### 3. Documentation Files (→ `documentation/`)
Moved documentation except README.md and TASK_DIVISION.md:
- ✅ `ELEVENLABS_FIX.md`
- ✅ `FRONTEND_BACKEND_INTEGRATION.md`
- ✅ `VISION_SYSTEM_SUMMARY.md`

## 📝 Path Updates in Code

### `app.py` Updates
All `send_file()` calls updated to include `frontend/` prefix:
```python
# Before
return send_file('index.html')

# After
return send_file('frontend/index.html')
```

All `subprocess` calls updated to include `backend/` prefix:
```python
# Before
subprocess.Popen(['python', 'process_ball_tracking.py'])

# After
subprocess.Popen(['python', 'backend/process_ball_tracking.py'])
```

### Backend Python Files Updates
Updated `sys.path.append` to reference parent directory:
```python
# Before (in backend/*.py)
sys.path.append(str(Path(__file__).parent / "src"))

# After (in backend/*.py)
sys.path.append(str(Path(__file__).parent.parent / "src"))
```

**Files updated:**
- ✅ `backend/process_ball_tracking.py`
- ✅ `backend/analyze_processed_video.py`

## 🚀 Running the Application

### No Changes Needed!
The application runs exactly the same way:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the Flask server
python app.py
```

The server will automatically serve files from their new locations.

## 🎯 Benefits

1. **Better Organization**: Clear separation between frontend, backend, and documentation
2. **Easier Navigation**: Developers can quickly find relevant files
3. **Scalability**: Easier to add new features in organized directories
4. **Professional Structure**: Follows industry best practices
5. **Maintainability**: Clearer codebase structure for future development

## ⚠️ Important Notes

1. **`app.py` stays in root**: This is the main entry point and should remain at the project root
2. **`src/` unchanged**: The source code module structure remains the same
3. **`input/` and `output/` unchanged**: Data directories remain in their original locations
4. **No URL changes**: All routes remain the same (e.g., `/ball_tracking.html` still works)
5. **Virtual environment**: No changes to venv or dependencies

## ✅ Verification Checklist

- [x] All HTML files moved to `frontend/`
- [x] All CSS and JS files moved to `frontend/`
- [x] All Python scripts (except app.py) moved to `backend/`
- [x] Documentation files moved to `documentation/`
- [x] `app.py` routes updated with `frontend/` prefix
- [x] Backend subprocess calls updated with `backend/` prefix
- [x] Backend Python files updated with correct `sys.path`
- [x] Server tested and running correctly

## 📚 Next Steps for Developers

When adding new files:
- **HTML/CSS/JS** → Add to `frontend/`
- **Python scripts** → Add to `backend/`
- **Documentation** → Add to `documentation/`
- **Shared modules** → Add to `src/`

---

**Migration completed successfully!** 🎉
