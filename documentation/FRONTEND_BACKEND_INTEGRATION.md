# PaddleCoach - Frontend & Backend Integration

## Running the Application

### Option 1: With Backend Server (Recommended)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   python server.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

### Option 2: Direct Frontend (No Python Backend)

Simply open `index.html` in your browser. Note: Ball tracking features won't work without the backend.

## Features

### Ball Tracking & Heat Map

#### Record Mode
- Click "Start Recording" on the home page
- Select "Record" option
- The system will:
  - Launch your camera automatically
  - Run `process_ball_tracking.py` in the background
  - Track ball movements in real-time
  - Display trajectory overlays and heat maps
- Press **'q'** on your keyboard to stop and save

#### Upload Mode
- Click "Start Recording" on the home page
- Select "Upload" option
- Upload a pre-recorded video
- The system will:
  - Display original video on the left
  - Show processed/tracked video on the right (simulated for demo)
  - Keep both videos in sync
  - Display analysis statistics

## Backend Scripts

### `server.py`
- Flask web server that connects frontend to Python scripts
- Handles API calls for ball tracking
- Runs on port 5000

### `process_ball_tracking.py`
- Real-time ball tracking using webcam
- Outputs to `output/ballTracking/`
- Press 'q' to quit

### `demo_video.py`
- Processes uploaded videos (currently for demo)
- Input from `input/demoVideo/`
- Output to `output/demoVideo/`

## Directory Structure

```
PaddleCoach/
├── index.html                    # Main landing page
├── ball_tracking.html           # Ball tracking options page
├── ball-tracking-record.html    # Record mode interface
├── ball-tracking-upload.html    # Upload mode interface
├── script.js                     # Frontend JavaScript
├── styles.css                    # Styles
├── server.py                     # Flask backend server
├── process_ball_tracking.py     # Real-time tracking script
├── demo_video.py                 # Demo video processor
├── input/
│   ├── demoVideo/               # Upload videos here
│   └── processVideo/            # Process videos here
└── output/
    ├── ballTracking/            # Ball tracking outputs
    ├── demoVideo/               # Demo outputs
    ├── processVideo/            # Processed videos
    └── analysisText/            # Analysis reports
```

## Notes

- The Upload feature currently simulates ball tracking for demo purposes
- Both videos play in sync for aesthetic purposes
- Real ball tracking integration is ready via the backend API endpoints
- Press 'q' in the camera window to stop recording

## Next Steps

1. Integrate actual ball tracking model for upload videos
2. Add heat map generation
3. Implement trajectory analysis
4. Add downloadable reports
