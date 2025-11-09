"""
PaddleCoach - Database Manager
Author: Rakshit
Description: Helper class for database operations (CRUD operations)
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_path='paddlecoach.db'):
        """Initialize database manager"""
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username, email, password, full_name=None, role='player'):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            return {'success': True, 'user_id': user_id}
            
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': 'Username or email already exists'}
        finally:
            conn.close()
    
    def authenticate_user(self, email, password):
        """Authenticate user and create session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT user_id, username, full_name, role 
            FROM users 
            WHERE email = ? AND password_hash = ? AND is_active = 1
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            # Create session token
            token = secrets.token_hex(32)
            expires_at = datetime.now() + timedelta(days=7)
            
            cursor.execute('''
                INSERT INTO sessions (user_id, token, expires_at)
                VALUES (?, ?, ?)
            ''', (user[0], token, expires_at))
            
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?
            ''', (user[0],))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'user_id': user[0],
                    'username': user[1],
                    'full_name': user[2],
                    'role': user[3]
                }
            }
        
        conn.close()
        return {'success': False, 'error': 'Invalid credentials'}
    
    def verify_token(self, token):
        """Verify session token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.user_id, u.username, u.full_name, u.role
            FROM sessions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.token = ? AND s.is_active = 1 AND s.expires_at > CURRENT_TIMESTAMP
        ''', (token,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'user_id': user[0],
                'username': user[1],
                'full_name': user[2],
                'role': user[3]
            }
        return None
    
    def logout_user(self, token):
        """Logout user by invalidating token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE sessions SET is_active = 0 WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    # ==================== PLAYER OPERATIONS ====================
    
    def create_player(self, user_id, player_name, skill_level='beginner'):
        """Create a new player profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO players (user_id, player_name, skill_level)
            VALUES (?, ?, ?)
        ''', (user_id, player_name, skill_level))
        
        player_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'player_id': player_id}
    
    def get_player_stats(self, player_id):
        """Get player statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT player_name, skill_level, total_matches, wins, losses, win_rate
            FROM players
            WHERE player_id = ?
        ''', (player_id,))
        
        player = cursor.fetchone()
        conn.close()
        
        if player:
            return {
                'player_name': player[0],
                'skill_level': player[1],
                'total_matches': player[2],
                'wins': player[3],
                'losses': player[4],
                'win_rate': player[5]
            }
        return None
    
    # ==================== MATCH OPERATIONS ====================
    
    def create_match(self, player1_id, player2_id, location=None):
        """Create a new match"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO matches (player1_id, player2_id, location, status)
            VALUES (?, ?, ?, 'in_progress')
        ''', (player1_id, player2_id, location))
        
        match_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'match_id': match_id}
    
    def update_match_result(self, match_id, winner_id, duration_seconds, total_points):
        """Update match with final results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE matches
            SET winner_id = ?, duration_seconds = ?, total_points = ?, status = 'completed'
            WHERE match_id = ?
        ''', (winner_id, duration_seconds, total_points, match_id))
        
        # Update player stats
        cursor.execute('SELECT player1_id, player2_id FROM matches WHERE match_id = ?', (match_id,))
        player1_id, player2_id = cursor.fetchone()
        
        loser_id = player2_id if winner_id == player1_id else player1_id
        
        # Update winner stats
        cursor.execute('''
            UPDATE players
            SET total_matches = total_matches + 1,
                wins = wins + 1,
                win_rate = ROUND((wins + 1) * 100.0 / (total_matches + 1), 2)
            WHERE player_id = ?
        ''', (winner_id,))
        
        # Update loser stats
        cursor.execute('''
            UPDATE players
            SET total_matches = total_matches + 1,
                losses = losses + 1,
                win_rate = ROUND(wins * 100.0 / (total_matches + 1), 2)
            WHERE player_id = ?
        ''', (loser_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_match_details(self, match_id):
        """Get detailed match information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.match_id, m.match_date, m.duration_seconds, m.status,
                   p1.player_name as player1_name, p2.player_name as player2_name,
                   pw.player_name as winner_name
            FROM matches m
            JOIN players p1 ON m.player1_id = p1.player_id
            JOIN players p2 ON m.player2_id = p2.player_id
            LEFT JOIN players pw ON m.winner_id = pw.player_id
            WHERE m.match_id = ?
        ''', (match_id,))
        
        match = cursor.fetchone()
        conn.close()
        
        if match:
            return {
                'match_id': match[0],
                'match_date': match[1],
                'duration_seconds': match[2],
                'status': match[3],
                'player1_name': match[4],
                'player2_name': match[5],
                'winner_name': match[6]
            }
        return None
    
    # ==================== AI COMMENTARY OPERATIONS ====================
    
    def save_commentary(self, match_id, event_type, commentary_text, audio_file_path=None, point_id=None):
        """Save AI-generated commentary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ai_commentary (match_id, point_id, event_type, commentary_text, audio_file_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (match_id, point_id, event_type, commentary_text, audio_file_path))
        
        commentary_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'commentary_id': commentary_id}
    
    def get_match_commentary(self, match_id):
        """Get all commentary for a match"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT commentary_id, event_type, commentary_text, audio_file_path, generated_at
            FROM ai_commentary
            WHERE match_id = ?
            ORDER BY generated_at
        ''', (match_id,))
        
        commentary = cursor.fetchall()
        conn.close()
        
        return [
            {
                'commentary_id': c[0],
                'event_type': c[1],
                'commentary_text': c[2],
                'audio_file_path': c[3],
                'generated_at': c[4]
            }
            for c in commentary
        ]
    
    # ==================== COACHING INSIGHTS OPERATIONS ====================
    
    def save_coaching_insight(self, player_id, insight_type, insight_text, match_id=None, priority='medium'):
        """Save coaching insight"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO coaching_insights (player_id, match_id, insight_type, insight_text, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, match_id, insight_type, insight_text, priority))
        
        insight_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'insight_id': insight_id}
    
    def get_player_insights(self, player_id, limit=10):
        """Get coaching insights for a player"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT insight_id, insight_type, insight_text, priority, created_at, is_read
            FROM coaching_insights
            WHERE player_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (player_id, limit))
        
        insights = cursor.fetchall()
        conn.close()
        
        return [
            {
                'insight_id': i[0],
                'insight_type': i[1],
                'insight_text': i[2],
                'priority': i[3],
                'created_at': i[4],
                'is_read': bool(i[5])
            }
            for i in insights
        ]
    
    # ==================== CHATBOT OPERATIONS ====================
    
    def save_chatbot_conversation(self, user_id, query, response, query_type=None):
        """Save chatbot conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chatbot_conversations (user_id, query, response, query_type)
            VALUES (?, ?, ?, ?)
        ''', (user_id, query, response, query_type))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'success': True, 'conversation_id': conversation_id}
    
    def get_user_conversations(self, user_id, limit=20):
        """Get user's chatbot conversation history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT conversation_id, query, response, query_type, timestamp
            FROM chatbot_conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        conversations = cursor.fetchall()
        conn.close()
        
        return [
            {
                'conversation_id': c[0],
                'query': c[1],
                'response': c[2],
                'query_type': c[3],
                'timestamp': c[4]
            }
            for c in conversations
        ]
