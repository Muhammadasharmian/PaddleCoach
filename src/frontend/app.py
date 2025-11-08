"""
PaddleCoach - Main Flask Application
Author: Rakshit
Description: Web interface for real-time match tracking, stats visualization, and AI coaching
"""

from flask import Flask, render_template, jsonify, request
# from flask_socketio import SocketIO, emit  # Commented out for now
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui_services.ui_data_service import UIDataService
from ui_services.stats_bot import StatsBot
from ui_services.elevenlabs_client import ElevenLabsClient
from ui_services.auth_service import AuthService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'paddlecoach_secret_key_2025'
# socketio = SocketIO(app, cors_allowed_origins="*")  # Commented out for now

# Initialize services
ui_data_service = UIDataService()
stats_bot = StatsBot()
elevenlabs_client = ElevenLabsClient()
auth_service = AuthService()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Landing page with navigation to different features"""
    return render_template('index.html')

@app.route('/match')
def match_view():
    """Real-time match tracking and score display"""
    return render_template('match_view.html')

@app.route('/stats')
def player_stats():
    """Player statistics and performance analytics"""
    return render_template('player_stats.html')

@app.route('/coaching')
def coaching_dashboard():
    """AI coaching dashboard with insights and recommendations"""
    return render_template('coaching_dashboard.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/match/current', methods=['GET'])
def get_current_match():
    """Get current match data"""
    try:
        match_data = ui_data_service.get_current_match()
        return jsonify({
            'success': True,
            'data': match_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get specific match data by ID"""
    try:
        match_data = ui_data_service.get_match_by_id(match_id)
        return jsonify({
            'success': True,
            'data': match_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/player/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Get player statistics"""
    try:
        stats = ui_data_service.get_player_stats(player_id)
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/coaching/insights/<int:player_id>', methods=['GET'])
def get_coaching_insights(player_id):
    """Get AI coaching insights for a player"""
    try:
        insights = ui_data_service.get_coaching_insights(player_id)
        return jsonify({
            'success': True,
            'data': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats/query', methods=['POST'])
def query_stats():
    """Query stats using natural language via StatsBot"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        response = stats_bot.process_query(query)
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/audio/commentary', methods=['POST'])
def generate_commentary():
    """Generate audio commentary using ElevenLabs"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        audio_url = elevenlabs_client.generate_speech(text)
        return jsonify({
            'success': True,
            'audio_url': audio_url
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Handle user signup"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        result = auth_service.signup(name, email, password)
        status_code = 200 if result['success'] else 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Signup error: {str(e)}'
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        result = auth_service.login(email, password)
        status_code = 200 if result['success'] else 401
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is required'
            }), 400
        
        result = auth_service.logout(token)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout error: {str(e)}'
        }), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verify session token"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is required'
            }), 400
        
        user = auth_service.verify_token(token)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Verification error: {str(e)}'
        }), 500

# ==================== WEBSOCKET EVENTS ====================
# Commented out for now - WebSocket functionality disabled

# @socketio.on('connect')
# def handle_connect():
#     """Handle client connection"""
#     print(f'Client connected: {request.sid}')
#     emit('connection_response', {'status': 'connected'})

# @socketio.on('disconnect')
# def handle_disconnect():
#     """Handle client disconnection"""
#     print(f'Client disconnected: {request.sid}')

# @socketio.on('subscribe_match')
# def handle_match_subscription(data):
#     """Subscribe to real-time match updates"""
#     match_id = data.get('match_id')
#     print(f'Client {request.sid} subscribed to match {match_id}')
#     emit('subscription_confirmed', {'match_id': match_id})

# def broadcast_score_update(match_id, score_data):
#     """Broadcast score update to all connected clients"""
#     socketio.emit('score_update', {
#         'match_id': match_id,
#         'score_data': score_data,
#         'timestamp': datetime.now().isoformat()
#     })

# def broadcast_point_complete(match_id, point_data):
#     """Broadcast point completion to all connected clients"""
#     socketio.emit('point_complete', {
#         'match_id': match_id,
#         'point_data': point_data,
#         'timestamp': datetime.now().isoformat()
#     })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("🏓 Starting PaddleCoach Web Application...")
    print("📍 Access the app at: http://localhost:5000")
    # Using Flask's built-in server (without socketio for now)
    app.run(host='0.0.0.0', port=5000, debug=True)
