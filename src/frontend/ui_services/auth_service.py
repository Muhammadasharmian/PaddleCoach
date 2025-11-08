"""
PaddleCoach - Authentication Service
Author: Rakshit
Description: User authentication and session management
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
import os


class AuthService:
    """Service for handling user authentication and session management"""
    
    def __init__(self, db_path='users.db'):
        """
        Initialize authentication service
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                session_token TEXT,
                last_login TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def signup(self, name, email, password):
        """
        Create new user account
        
        Args:
            name (str): User's full name
            email (str): User's email address
            password (str): User's password
            
        Returns:
            dict: Result with success status and message
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return {
                    'success': False,
                    'message': 'Email already registered'
                }
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, email, self.hash_password(password), datetime.now().isoformat()))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Account created successfully',
                'user_id': user_id
            }
            
        except sqlite3.IntegrityError as e:
            return {
                'success': False,
                'message': 'Email already exists'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating account: {str(e)}'
            }
    
    def login(self, email, password):
        """
        Authenticate user and create session
        
        Args:
            email (str): User's email
            password (str): User's password
            
        Returns:
            dict: Result with success status, token, and user info
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find user with matching credentials
            cursor.execute('''
                SELECT id, name, email FROM users 
                WHERE email = ? AND password_hash = ?
            ''', (email, self.hash_password(password)))
            
            user = cursor.fetchone()
            
            if user:
                # Generate session token
                token = secrets.token_hex(32)
                
                # Update session token and last login
                cursor.execute('''
                    UPDATE users 
                    SET session_token = ?, last_login = ?
                    WHERE id = ?
                ''', (token, datetime.now().isoformat(), user[0]))
                
                conn.commit()
                conn.close()
                
                return {
                    'success': True,
                    'message': 'Login successful',
                    'token': token,
                    'user': {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2]
                    }
                }
            
            conn.close()
            return {
                'success': False,
                'message': 'Invalid email or password'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Login error: {str(e)}'
            }
    
    def verify_token(self, token):
        """
        Verify session token and get user info
        
        Args:
            token (str): Session token
            
        Returns:
            dict: User info if valid, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email FROM users 
                WHERE session_token = ?
            ''', (token,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
            
            return None
            
        except Exception as e:
            print(f"Token verification error: {e}")
            return None
    
    def logout(self, token):
        """
        Logout user by clearing session token
        
        Args:
            token (str): Session token
            
        Returns:
            dict: Result with success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET session_token = NULL 
                WHERE session_token = ?
            ''', (token,))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'Logged out successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Logout error: {str(e)}'
            }
    
    def get_user_by_email(self, email):
        """
        Get user information by email
        
        Args:
            email (str): User's email
            
        Returns:
            dict: User info or None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, name, email, created_at FROM users 
                WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                    'created_at': user[3]
                }
            
            return None
            
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
