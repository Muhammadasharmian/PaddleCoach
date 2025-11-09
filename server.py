"""
Flask server to connect frontend with Python backend scripts.
This server handles the ball tracking recording and upload functionality.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import threading
from pathlib import Path

app = Flask(__name__, static_folder='.')
CORS(app)

# Global variable to track the running process
ball_tracking_process = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/start-ball-tracking', methods=['POST'])
def start_ball_tracking():
    """Start the real-time ball tracking process."""
    global ball_tracking_process
    
    try:
        # Run process_ball_tracking.py in a separate thread
        def run_tracking():
            global ball_tracking_process
            ball_tracking_process = subprocess.Popen(
                ['python', 'process_ball_tracking.py'],
                cwd=os.getcwd()
            )
            ball_tracking_process.wait()
        
        tracking_thread = threading.Thread(target=run_tracking)
        tracking_thread.daemon = True
        tracking_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Ball tracking started'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stop-ball-tracking', methods=['POST'])
def stop_ball_tracking():
    """Stop the ball tracking process."""
    global ball_tracking_process
    
    try:
        if ball_tracking_process:
            ball_tracking_process.terminate()
            ball_tracking_process = None
        
        return jsonify({
            'status': 'success',
            'message': 'Ball tracking stopped'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/process-ball-tracking', methods=['POST'])
def process_uploaded_video():
    """Process an uploaded video with ball tracking."""
    try:
        if 'video' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No video file provided'
            }), 400
        
        video_file = request.files['video']
        
        # Save to input directory
        input_dir = Path('input/demoVideo')
        input_dir.mkdir(parents=True, exist_ok=True)
        
        video_path = input_dir / video_file.filename
        video_file.save(str(video_path))
        
        # Run demo_video.py
        result = subprocess.run(
            ['python', 'demo_video.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return jsonify({
                'status': 'success',
                'message': 'Video processed successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Processing failed',
                'error': result.stderr
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("="*60)
    print("🏓 PaddleCoach Server Starting...")
    print("="*60)
    print("\n📡 Server running at: http://localhost:5000")
    print("📁 Serving files from:", os.getcwd())
    print("\nPress Ctrl+C to stop the server\n")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
