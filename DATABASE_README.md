# PaddleCoach Database Documentation

## 📊 Database Structure

The PaddleCoach database stores all information for user authentication, match tracking, player statistics, AI commentary, and coaching insights.

### Database Location
```
paddlecoach.db (in project root)
```

## 🗄️ Database Tables

### 1. **users** - User Authentication
Stores user account information and credentials.

| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER (PK) | Unique user identifier |
| username | VARCHAR(50) | Username (unique) |
| email | VARCHAR(100) | Email address (unique) |
| password_hash | VARCHAR(255) | SHA-256 hashed password |
| full_name | VARCHAR(100) | User's full name |
| created_at | TIMESTAMP | Account creation time |
| last_login | TIMESTAMP | Last login time |
| is_active | BOOLEAN | Account active status |
| role | VARCHAR(20) | User role (player/coach/admin) |

### 2. **sessions** - Login Sessions
Manages user authentication tokens and sessions.

| Column | Type | Description |
|--------|------|-------------|
| session_id | INTEGER (PK) | Session identifier |
| user_id | INTEGER (FK) | Reference to users table |
| token | VARCHAR(255) | Session token (unique) |
| created_at | TIMESTAMP | Session creation time |
| expires_at | TIMESTAMP | Session expiration time |
| is_active | BOOLEAN | Session active status |

### 3. **players** - Player Profiles
Player information and overall statistics.

| Column | Type | Description |
|--------|------|-------------|
| player_id | INTEGER (PK) | Player identifier |
| user_id | INTEGER (FK) | Reference to users table |
| player_name | VARCHAR(100) | Player display name |
| skill_level | VARCHAR(20) | Skill level (beginner/intermediate/advanced) |
| total_matches | INTEGER | Total matches played |
| wins | INTEGER | Total wins |
| losses | INTEGER | Total losses |
| win_rate | FLOAT | Win percentage |
| created_at | TIMESTAMP | Profile creation time |

### 4. **matches** - Match Records
Complete match information and results.

| Column | Type | Description |
|--------|------|-------------|
| match_id | INTEGER (PK) | Match identifier |
| player1_id | INTEGER (FK) | First player |
| player2_id | INTEGER (FK) | Second player |
| winner_id | INTEGER (FK) | Winning player |
| match_date | TIMESTAMP | Match date/time |
| duration_seconds | INTEGER | Match duration |
| total_points | INTEGER | Total points played |
| status | VARCHAR(20) | Match status |
| location | VARCHAR(100) | Match location |

### 5. **sets** - Set-Level Data
Individual set scores and information.

| Column | Type | Description |
|--------|------|-------------|
| set_id | INTEGER (PK) | Set identifier |
| match_id | INTEGER (FK) | Reference to matches |
| set_number | INTEGER | Set number (1, 2, 3...) |
| player1_score | INTEGER | Player 1 score |
| player2_score | INTEGER | Player 2 score |
| winner_id | INTEGER (FK) | Set winner |
| duration_seconds | INTEGER | Set duration |

### 6. **points** - Point-by-Point Data
Detailed tracking of every point.

| Column | Type | Description |
|--------|------|-------------|
| point_id | INTEGER (PK) | Point identifier |
| set_id | INTEGER (FK) | Reference to sets |
| point_number | INTEGER | Point number in set |
| server_id | INTEGER (FK) | Serving player |
| winner_id | INTEGER (FK) | Point winner |
| shot_type | VARCHAR(50) | Winning shot type |
| rally_length | INTEGER | Number of shots in rally |
| timestamp | TIMESTAMP | Point completion time |

### 7. **player_stats** - Detailed Player Statistics
Match-specific player performance metrics.

| Column | Type | Description |
|--------|------|-------------|
| stat_id | INTEGER (PK) | Stat identifier |
| player_id | INTEGER (FK) | Player reference |
| match_id | INTEGER (FK) | Match reference |
| forehand_winners | INTEGER | Forehand winner count |
| backhand_winners | INTEGER | Backhand winner count |
| aces | INTEGER | Aces count |
| errors | INTEGER | Unforced errors |
| avg_rally_length | FLOAT | Average rally length |
| points_won | INTEGER | Points won |
| points_lost | INTEGER | Points lost |

### 8. **shot_analysis** - Shot-Level Tracking
Computer vision data for each shot.

| Column | Type | Description |
|--------|------|-------------|
| shot_id | INTEGER (PK) | Shot identifier |
| point_id | INTEGER (FK) | Point reference |
| player_id | INTEGER (FK) | Player who hit shot |
| shot_number | INTEGER | Shot number in rally |
| shot_type | VARCHAR(50) | Type of shot (forehand/backhand/etc) |
| ball_speed | FLOAT | Ball speed (mph/kph) |
| ball_spin | VARCHAR(20) | Spin type (topspin/backspin/sidespin) |
| placement_x | FLOAT | X coordinate on table |
| placement_y | FLOAT | Y coordinate on table |
| is_winner | BOOLEAN | Shot was a winner |
| is_error | BOOLEAN | Shot was an error |
| timestamp | TIMESTAMP | Shot time |

### 9. **ai_commentary** - AI-Generated Commentary
Stores AI commentary for matches and events.

| Column | Type | Description |
|--------|------|-------------|
| commentary_id | INTEGER (PK) | Commentary identifier |
| match_id | INTEGER (FK) | Match reference |
| point_id | INTEGER (FK) | Point reference (optional) |
| event_type | VARCHAR(50) | Event type (point/game_win/set_win) |
| commentary_text | TEXT | Generated commentary text |
| audio_file_path | VARCHAR(255) | Path to audio file |
| generated_at | TIMESTAMP | Generation time |

### 10. **coaching_insights** - AI Coaching Recommendations
AI-generated coaching insights and tips.

| Column | Type | Description |
|--------|------|-------------|
| insight_id | INTEGER (PK) | Insight identifier |
| player_id | INTEGER (FK) | Player reference |
| match_id | INTEGER (FK) | Match reference (optional) |
| insight_type | VARCHAR(50) | Type (technique/strategy/mental) |
| insight_text | TEXT | Insight/recommendation text |
| priority | VARCHAR(20) | Priority (low/medium/high) |
| created_at | TIMESTAMP | Creation time |
| is_read | BOOLEAN | Has player read it? |

### 11. **training_data** - AI Training Data
Video and analysis data for AI chatbot training.

| Column | Type | Description |
|--------|------|-------------|
| training_id | INTEGER (PK) | Training data identifier |
| match_id | INTEGER (FK) | Match reference |
| video_path | VARCHAR(255) | Path to video file |
| analysis_data | TEXT | JSON analysis data |
| processed | BOOLEAN | Has been processed? |
| created_at | TIMESTAMP | Creation time |

### 12. **chatbot_conversations** - Chatbot Interactions
Stores all user interactions with the AI chatbot.

| Column | Type | Description |
|--------|------|-------------|
| conversation_id | INTEGER (PK) | Conversation identifier |
| user_id | INTEGER (FK) | User reference |
| query | TEXT | User's question |
| response | TEXT | Chatbot's response |
| query_type | VARCHAR(50) | Type of query |
| timestamp | TIMESTAMP | Conversation time |

## 🔧 Usage Examples

### 1. User Authentication

```python
from database.database_manager import DatabaseManager

db = DatabaseManager('paddlecoach.db')

# Create a new user
result = db.create_user(
    username="john_doe",
    email="john@example.com",
    password="securepass123",
    full_name="John Doe"
)

# Login
auth = db.authenticate_user("john@example.com", "securepass123")
token = auth['token']

# Verify token
user = db.verify_token(token)
```

### 2. Match Tracking

```python
# Create a match
match = db.create_match(player1_id=1, player2_id=2, location="Arena")
match_id = match['match_id']

# Update match result
db.update_match_result(
    match_id=match_id,
    winner_id=1,
    duration_seconds=1800,
    total_points=45
)

# Get match details
details = db.get_match_details(match_id)
```

### 3. AI Commentary

```python
# Save commentary
db.save_commentary(
    match_id=1,
    event_type="point",
    commentary_text="Amazing backhand winner!",
    audio_file_path="audio/commentary_1.mp3"
)

# Get all commentary for a match
commentary = db.get_match_commentary(match_id=1)
```

### 4. Coaching Insights

```python
# Save insight
db.save_coaching_insight(
    player_id=1,
    insight_type="technique",
    insight_text="Work on backhand consistency",
    priority="high"
)

# Get player insights
insights = db.get_player_insights(player_id=1, limit=10)
```

### 5. Chatbot Conversations

```python
# Save conversation
db.save_chatbot_conversation(
    user_id=1,
    query="How can I improve my serve?",
    response="Focus on ball toss consistency and follow-through...",
    query_type="coaching"
)

# Get conversation history
history = db.get_user_conversations(user_id=1, limit=20)
```

## 🚀 Setup Instructions

1. **Create the database:**
```bash
python src/database/database_setup.py
```

2. **Test the database:**
```bash
python src/database/test_database.py
```

3. **Use in your code:**
```python
from database.database_manager import DatabaseManager
db = DatabaseManager('paddlecoach.db')
```

## 📝 Sample Data

The database comes with sample users:

| Username | Email | Password | Role |
|----------|-------|----------|------|
| rakshit | rakshit@paddlecoach.com | password123 | admin |
| ashar | ashar@paddlecoach.com | password123 | player |
| mohnish | mohnish@paddlecoach.com | password123 | player |

## 🔐 Security Notes

- Passwords are stored as SHA-256 hashes
- Session tokens are 64-character hex strings
- Sessions expire after 7 days
- Always use HTTPS in production
- Never commit the database file to version control

## 📊 Database File

Location: `paddlecoach.db` (SQLite database)
- Portable and easy to backup
- No server required
- Perfect for development and small-scale deployment

## 🎯 Next Steps

1. Integrate database with commentary service
2. Add computer vision data to shot_analysis table
3. Train AI chatbot with training_data table
4. Build coaching dashboard using insights table
5. Add real-time match tracking
