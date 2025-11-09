"""
PaddleCoach - Database Usage Examples
Author: Rakshit
Description: Examples of how to use the database for your project
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database_manager import DatabaseManager

def main():
    print("\n" + "="*70)
    print("PADDLECOACH DATABASE USAGE EXAMPLES")
    print("="*70 + "\n")
    
    # Initialize database manager
    db_path = 'C:\\Users\\12rak\\Downloads\\PaddleCoach-main\\PaddleCoach-main\\paddlecoach.db'
    db = DatabaseManager(db_path)
    
    # ==================== USER AUTHENTICATION ====================
    print("1️⃣  USER AUTHENTICATION")
    print("-" * 70)
    
    # Create a new user
    result = db.create_user(
        username="testuser",
        email="test@example.com",
        password="securepassword123",
        full_name="Test User",
        role="player"
    )
    
    if result['success']:
        print(f"✓ User created with ID: {result['user_id']}")
    else:
        print(f"✗ {result['error']}")
    
    # Login user
    auth_result = db.authenticate_user("ashar@paddlecoach.com", "password123")
    
    if auth_result['success']:
        print(f"✓ Login successful!")
        print(f"  Token: {auth_result['token'][:20]}...")
        print(f"  User: {auth_result['user']['username']}")
        token = auth_result['token']
    
    # Verify token
    user = db.verify_token(token)
    if user:
        print(f"✓ Token verified for user: {user['username']}")
    
    print()
    
    # ==================== PLAYER OPERATIONS ====================
    print("2️⃣  PLAYER OPERATIONS")
    print("-" * 70)
    
    # Get player stats
    player_stats = db.get_player_stats(1)  # Player ID 1 (Ashar)
    if player_stats:
        print(f"Player: {player_stats['player_name']}")
        print(f"  Skill Level: {player_stats['skill_level']}")
        print(f"  Total Matches: {player_stats['total_matches']}")
        print(f"  Wins: {player_stats['wins']}")
        print(f"  Losses: {player_stats['losses']}")
        print(f"  Win Rate: {player_stats['win_rate']}%")
    
    print()
    
    # ==================== MATCH OPERATIONS ====================
    print("3️⃣  MATCH OPERATIONS")
    print("-" * 70)
    
    # Create a new match
    match_result = db.create_match(player1_id=1, player2_id=2, location="Main Arena")
    match_id = match_result['match_id']
    print(f"✓ Match created with ID: {match_id}")
    
    # Update match result
    db.update_match_result(
        match_id=match_id,
        winner_id=1,
        duration_seconds=1800,  # 30 minutes
        total_points=45
    )
    print(f"✓ Match result updated")
    
    # Get match details
    match_details = db.get_match_details(match_id)
    if match_details:
        print(f"  {match_details['player1_name']} vs {match_details['player2_name']}")
        print(f"  Winner: {match_details['winner_name']}")
        print(f"  Duration: {match_details['duration_seconds']} seconds")
    
    print()
    
    # ==================== AI COMMENTARY ====================
    print("4️⃣  AI COMMENTARY")
    print("-" * 70)
    
    # Save commentary
    commentary_result = db.save_commentary(
        match_id=match_id,
        event_type="game_win",
        commentary_text="Ashar dominates with a powerful forehand winner!",
        audio_file_path="commentary/match1_game1.mp3"
    )
    print(f"✓ Commentary saved with ID: {commentary_result['commentary_id']}")
    
    # Get all commentary for the match
    all_commentary = db.get_match_commentary(match_id)
    print(f"  Total commentary entries: {len(all_commentary)}")
    for c in all_commentary:
        print(f"  - {c['event_type']}: {c['commentary_text'][:50]}...")
    
    print()
    
    # ==================== COACHING INSIGHTS ====================
    print("5️⃣  COACHING INSIGHTS")
    print("-" * 70)
    
    # Save coaching insights
    insight_result = db.save_coaching_insight(
        player_id=1,
        insight_type="technique",
        insight_text="Focus on improving backhand consistency. Noticed 45% error rate on backhand shots.",
        match_id=match_id,
        priority="high"
    )
    print(f"✓ Coaching insight saved with ID: {insight_result['insight_id']}")
    
    # Get player insights
    insights = db.get_player_insights(player_id=1, limit=5)
    print(f"  Total insights: {len(insights)}")
    for insight in insights:
        print(f"  - [{insight['priority'].upper()}] {insight['insight_type']}: {insight['insight_text'][:60]}...")
    
    print()
    
    # ==================== CHATBOT CONVERSATIONS ====================
    print("6️⃣  CHATBOT CONVERSATIONS")
    print("-" * 70)
    
    # Save chatbot conversation
    conv_result = db.save_chatbot_conversation(
        user_id=2,
        query="How can I improve my forehand?",
        response="Based on your recent matches, I recommend: 1) Focus on weight transfer, 2) Practice topspin drills, 3) Work on follow-through consistency.",
        query_type="coaching"
    )
    print(f"✓ Conversation saved with ID: {conv_result['conversation_id']}")
    
    # Get conversation history
    conversations = db.get_user_conversations(user_id=2, limit=5)
    print(f"  Total conversations: {len(conversations)}")
    for conv in conversations:
        print(f"  Q: {conv['query']}")
        print(f"  A: {conv['response'][:60]}...")
    
    print()
    
    # ==================== SUMMARY ====================
    print("="*70)
    print("✅ Database is ready to use for:")
    print("  • User authentication and session management")
    print("  • Player profiles and statistics")
    print("  • Match tracking and results")
    print("  • AI commentary generation and storage")
    print("  • Coaching insights and recommendations")
    print("  • Chatbot training data and conversations")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
