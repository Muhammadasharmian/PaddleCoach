"""
PaddleCoach - Database Setup and Schema
Author: Rakshit
Description: Complete database schema for storing users, matches, players, and analytics
"""

import sqlite3
from datetime import datetime
import os

class PaddleCoachDatabase:
    def __init__(self, db_path='paddlecoach.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to the database"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        print(f"✓ Connected to database: {self.db_path}")
        
    def create_tables(self):
        """Create all necessary tables"""
        
        # 1. USERS TABLE - for authentication
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                role VARCHAR(20) DEFAULT 'player'
            )
        ''')
        print("✓ Created table: users")
        
        # 2. SESSIONS TABLE - for login sessions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        print("✓ Created table: sessions")
        
        # 3. PLAYERS TABLE - player profiles and stats
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                player_name VARCHAR(100) NOT NULL,
                skill_level VARCHAR(20),
                total_matches INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                win_rate FLOAT DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        print("✓ Created table: players")
        
        # 4. MATCHES TABLE - match records
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player1_id INTEGER NOT NULL,
                player2_id INTEGER NOT NULL,
                winner_id INTEGER,
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_seconds INTEGER,
                total_points INTEGER,
                status VARCHAR(20) DEFAULT 'scheduled',
                location VARCHAR(100),
                FOREIGN KEY (player1_id) REFERENCES players(player_id),
                FOREIGN KEY (player2_id) REFERENCES players(player_id),
                FOREIGN KEY (winner_id) REFERENCES players(player_id)
            )
        ''')
        print("✓ Created table: matches")
        
        # 5. SETS TABLE - set-level data
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sets (
                set_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                set_number INTEGER NOT NULL,
                player1_score INTEGER DEFAULT 0,
                player2_score INTEGER DEFAULT 0,
                winner_id INTEGER,
                duration_seconds INTEGER,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (winner_id) REFERENCES players(player_id)
            )
        ''')
        print("✓ Created table: sets")
        
        # 6. POINTS TABLE - point-by-point data
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS points (
                point_id INTEGER PRIMARY KEY AUTOINCREMENT,
                set_id INTEGER NOT NULL,
                point_number INTEGER NOT NULL,
                server_id INTEGER NOT NULL,
                winner_id INTEGER NOT NULL,
                shot_type VARCHAR(50),
                rally_length INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (set_id) REFERENCES sets(set_id),
                FOREIGN KEY (server_id) REFERENCES players(player_id),
                FOREIGN KEY (winner_id) REFERENCES players(player_id)
            )
        ''')
        print("✓ Created table: points")
        
        # 7. PLAYER_STATS TABLE - detailed player statistics
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                match_id INTEGER NOT NULL,
                forehand_winners INTEGER DEFAULT 0,
                backhand_winners INTEGER DEFAULT 0,
                aces INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0,
                avg_rally_length FLOAT DEFAULT 0.0,
                points_won INTEGER DEFAULT 0,
                points_lost INTEGER DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
        ''')
        print("✓ Created table: player_stats")
        
        # 8. SHOT_ANALYSIS TABLE - detailed shot tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS shot_analysis (
                shot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                point_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                shot_number INTEGER NOT NULL,
                shot_type VARCHAR(50),
                ball_speed FLOAT,
                ball_spin VARCHAR(20),
                placement_x FLOAT,
                placement_y FLOAT,
                is_winner BOOLEAN DEFAULT 0,
                is_error BOOLEAN DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (point_id) REFERENCES points(point_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id)
            )
        ''')
        print("✓ Created table: shot_analysis")
        
        # 9. AI_COMMENTARY TABLE - store AI-generated commentary
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_commentary (
                commentary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                point_id INTEGER,
                event_type VARCHAR(50) NOT NULL,
                commentary_text TEXT NOT NULL,
                audio_file_path VARCHAR(255),
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (point_id) REFERENCES points(point_id)
            )
        ''')
        print("✓ Created table: ai_commentary")
        
        # 10. COACHING_INSIGHTS TABLE - AI coaching recommendations
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coaching_insights (
                insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                match_id INTEGER,
                insight_type VARCHAR(50) NOT NULL,
                insight_text TEXT NOT NULL,
                priority VARCHAR(20) DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
        ''')
        print("✓ Created table: coaching_insights")
        
        # 11. TRAINING_DATA TABLE - for AI chatbot training
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_data (
                training_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                video_path VARCHAR(255),
                analysis_data TEXT,
                processed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches(match_id)
            )
        ''')
        print("✓ Created table: training_data")
        
        # 12. CHATBOT_CONVERSATIONS TABLE - store chatbot interactions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chatbot_conversations (
                conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                query_type VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        print("✓ Created table: chatbot_conversations")
        
        self.connection.commit()
        print("\n✅ All tables created successfully!")
        
    def create_indexes(self):
        """Create indexes for better query performance"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token)",
            "CREATE INDEX IF NOT EXISTS idx_matches_player1 ON matches(player1_id)",
            "CREATE INDEX IF NOT EXISTS idx_matches_player2 ON matches(player2_id)",
            "CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date)",
            "CREATE INDEX IF NOT EXISTS idx_points_set ON points(set_id)",
            "CREATE INDEX IF NOT EXISTS idx_shot_analysis_point ON shot_analysis(point_id)",
            "CREATE INDEX IF NOT EXISTS idx_commentary_match ON ai_commentary(match_id)",
            "CREATE INDEX IF NOT EXISTS idx_coaching_player ON coaching_insights(player_id)",
        ]
        
        for index_sql in indexes:
            self.cursor.execute(index_sql)
        
        self.connection.commit()
        print("✅ All indexes created successfully!")
        
    def insert_sample_data(self):
        """Insert sample data for testing"""
        import hashlib
        
        # Sample users
        password = hashlib.sha256("password123".encode()).hexdigest()
        
        sample_users = [
            ("rakshit", "rakshit@paddlecoach.com", password, "Rakshit Kumar", "admin"),
            ("ashar", "ashar@paddlecoach.com", password, "Ashar Muhammad", "player"),
            ("mohnish", "mohnish@paddlecoach.com", password, "Mohnish Patel", "player"),
        ]
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO users (username, email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_users)
        
        # Sample players
        sample_players = [
            (2, "Ashar", "advanced", 15, 10, 5, 66.7),
            (3, "Mohnish", "advanced", 20, 12, 8, 60.0),
        ]
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO players (user_id, player_name, skill_level, total_matches, wins, losses, win_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', sample_players)
        
        self.connection.commit()
        print("✅ Sample data inserted successfully!")
        
    def get_database_info(self):
        """Get information about the database"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        
        print("\n" + "="*70)
        print("DATABASE STRUCTURE")
        print("="*70)
        
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            print(f"📊 {table_name}: {count} records")
            
        print("="*70)
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("\n✓ Database connection closed")


def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("PADDLECOACH DATABASE SETUP")
    print("="*70 + "\n")
    
    # Create database in the project root
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'paddlecoach.db')
    
    db = PaddleCoachDatabase(db_path)
    db.connect()
    db.create_tables()
    db.create_indexes()
    db.insert_sample_data()
    db.get_database_info()
    db.close()
    
    print(f"\n✅ Database created at: {db_path}")
    print("✅ Ready to use for authentication, matches, stats, and AI training!")
    

if __name__ == "__main__":
    main()
