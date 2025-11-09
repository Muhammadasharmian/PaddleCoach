"""
Flask server for PaddleCoach frontend-backend integration.
Handles ball tracking and video processing requests.
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
from pathlib import Path
import time
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to track ball tracking process
ball_tracking_process = None

@app.route('/')
def index():
    """Serve the main index.html file."""
    return send_file('index.html')

@app.route('/index.html')
def index_html():
    """Redirect index.html to root."""
    return send_file('index.html')

@app.route('/ball_tracking.html')
def ball_tracking():
    """Serve the ball tracking page."""
    return send_file('ball_tracking.html')

@app.route('/ball-tracking.html')
def ball_tracking_hyphen():
    """Redirect ball-tracking.html to ball_tracking.html."""
    return send_file('ball_tracking.html')

@app.route('/ball-tracking-record.html')
def ball_tracking_record():
    """Serve the record page."""
    return send_file('ball-tracking-record.html')

@app.route('/ball-tracking-upload.html')
def ball_tracking_upload():
    """Serve the upload page."""
    return send_file('ball-tracking-upload.html')

@app.route('/styles.css')
def styles():
    """Serve the CSS file."""
    return send_file('styles.css')

@app.route('/script.js')
def script():
    """Serve the JavaScript file."""
    return send_file('script.js')

@app.route('/landing_image.png')
def landing_image():
    """Serve the landing image."""
    return send_file('landing_image.png')

@app.route('/api/start-ball-tracking', methods=['POST'])
def start_ball_tracking():
    """Start the ball tracking process."""
    global ball_tracking_process
    
    try:
        # Check if process is already running
        if ball_tracking_process and ball_tracking_process.poll() is None:
            return jsonify({
                'status': 'error',
                'message': 'Ball tracking is already running'
            }), 400
        
        # Start the process_ball_tracking.py script
        ball_tracking_process = subprocess.Popen(
            ['python', 'process_ball_tracking.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return jsonify({
            'status': 'success',
            'message': 'Ball tracking started. Camera window will open. Press "q" to quit.',
            'pid': ball_tracking_process.pid
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
            ball_tracking_process.wait(timeout=5)
            ball_tracking_process = None
            return jsonify({
                'status': 'success',
                'message': 'Ball tracking stopped'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'No ball tracking process running'
            }), 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/upload-video', methods=['POST'])
def upload_video():
    """Handle video upload and processing."""
    try:
        if 'video' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No video file provided'
            }), 400
        
        video_file = request.files['video']
        
        if video_file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No video file selected'
            }), 400
        
        # Save the uploaded video to input/demoVideo/
        input_dir = Path('input/demoVideo')
        input_dir.mkdir(parents=True, exist_ok=True)
        
        # Use original filename or a timestamp-based name
        video_path = input_dir / video_file.filename
        video_file.save(str(video_path))
        
        # Run demo_video.py in background
        def process_video():
            try:
                subprocess.run(['python', 'demo_video.py'], check=True)
            except Exception as e:
                print(f"Error processing video: {e}")
        
        # Start processing in background thread
        thread = threading.Thread(target=process_video)
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Video uploaded successfully. Processing started.',
            'filename': video_file.filename,
            'input_path': str(video_path)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/get-processed-video', methods=['GET'])
def get_processed_video():
    """Get the path to the processed video."""
    try:
        output_dir = Path('output/demoVideo')
        
        if not output_dir.exists():
            return jsonify({
                'status': 'error',
                'message': 'No processed videos found'
            }), 404
        
        # Find the most recent video file
        video_files = list(output_dir.glob('*.mp4'))
        
        if not video_files:
            return jsonify({
                'status': 'error',
                'message': 'No processed videos found'
            }), 404
        
        # Get the most recent file
        latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
        
        return jsonify({
            'status': 'success',
            'video_path': str(latest_video),
            'filename': latest_video.name
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/output/<path:filepath>')
def serve_output(filepath):
    """Serve files from the output directory."""
    return send_file(os.path.join('output', filepath))

@app.route('/input/<path:filepath>')
def serve_input(filepath):
    """Serve files from the input directory."""
    return send_file(os.path.join('input', filepath))

if __name__ == '__main__':
    # Ensure output directories exist
    Path('output/ballTracking').mkdir(parents=True, exist_ok=True)
    Path('output/demoVideo').mkdir(parents=True, exist_ok=True)
    Path('input/demoVideo').mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("🏓 PaddleCoach Server Starting...")
    print("="*60)
    print("\n📍 Server will run at: http://localhost:5000")
    print("\n🎯 Available endpoints:")
    print("  • http://localhost:5000/ - Main page")
    print("  • http://localhost:5000/ball_tracking.html - Ball tracking")
    print("  • POST /api/start-ball-tracking - Start recording")
    print("  • POST /api/upload-video - Upload video")
    print("\n⚡ Ready to serve!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
