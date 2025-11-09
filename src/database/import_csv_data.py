"""
PaddleCoach - CSV Data Import
Author: Rakshit
Description: Import player data from CSV into SQLite database
"""

import csv
import sqlite3
import os

def import_csv_to_database(csv_file_path, db_path='paddlecoach.db'):
    """Import CSV data into the database"""
    
    print("\n" + "="*70)
    print("CSV DATA IMPORT TO SQLITE DATABASE")
    print("="*70 + "\n")
    
    # Connect to database
    db_path = 'C:\\Users\\12rak\\Downloads\\PaddleCoach-main\\PaddleCoach-main\\paddlecoach.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"✓ Connected to database: {db_path}")
    print(f"✓ Reading CSV file: {csv_file_path}\n")
    
    # Read CSV file
    imported_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            player_name = row['Player Name']
            total_points_won = int(row['Total Points Won'])
            games_won = int(row['Games Won'])
            serve_win_pct = float(row['Serve Win %'].rstrip('%'))
            attack_success_pct = float(row['Attack Success %'].rstrip('%'))
            performance_score = int(row['Performance Score'])
            percentage_accuracy = float(row['Percentage Accuracy'].rstrip('%'))
            key_factor = row['Key Factor']
            
            # Check if player already exists
            cursor.execute('SELECT player_id FROM players WHERE player_name = ?', (player_name,))
            existing_player = cursor.fetchone()
            
            if existing_player:
                player_id = existing_player[0]
                print(f"  Player '{player_name}' already exists (ID: {player_id})")
                
                # Update existing player stats
                cursor.execute('''
                    UPDATE players
                    SET total_matches = ?,
                        wins = ?,
                        win_rate = ?
                    WHERE player_id = ?
                ''', (games_won, games_won, 100.0, player_id))
                
            else:
                # Create new player
                cursor.execute('''
                    INSERT INTO players (player_name, skill_level, total_matches, wins, losses, win_rate)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (player_name, 'advanced', games_won, games_won, 0, 100.0))
                
                player_id = cursor.lastrowid
                print(f"✓ Created player '{player_name}' (ID: {player_id})")
            
            # Create a summary match for this player's overall performance
            # Use player_id for both players (representing aggregate stats)
            cursor.execute('''
                INSERT INTO matches (player1_id, player2_id, winner_id, status, total_points)
                VALUES (?, ?, ?, 'completed', ?)
            ''', (player_id, player_id, player_id, total_points_won))
            
            match_id = cursor.lastrowid
            
            # Insert detailed player stats
            cursor.execute('''
                INSERT INTO player_stats (
                    player_id, match_id, forehand_winners, backhand_winners, 
                    points_won, points_lost, avg_rally_length
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                player_id,
                match_id,
                int(total_points_won * attack_success_pct / 100),  # Estimated forehand winners
                int(total_points_won * 0.3),  # Estimated backhand winners
                total_points_won,
                int(total_points_won * 0.2),  # Estimated points lost
                5.5  # Average rally length
            ))
            
            # Insert coaching insight based on key factor
            insight_text = f"""Performance Analysis for {player_name}:

Key Strength: {key_factor}
- Total Points Won: {total_points_won}
- Games Won: {games_won}
- Serve Win Rate: {serve_win_pct}%
- Attack Success Rate: {attack_success_pct}%
- Performance Score: {performance_score}
- Overall Accuracy: {percentage_accuracy}%

Recommendation: Continue focusing on your {key_factor.lower()} while working on other aspects of your game."""
            
            cursor.execute('''
                INSERT INTO coaching_insights (
                    player_id, insight_type, insight_text, priority
                )
                VALUES (?, ?, ?, ?)
            ''', (player_id, 'performance_analysis', insight_text, 'medium'))
            
            print(f"  ├─ Match record created (ID: {match_id})")
            print(f"  ├─ Stats imported: {total_points_won} points, {attack_success_pct}% attack success")
            print(f"  └─ Coaching insight added: {key_factor}\n")
            
            imported_count += 1
    
    conn.commit()
    conn.close()
    
    print("="*70)
    print(f"✅ Successfully imported {imported_count} player records!")
    print("="*70 + "\n")
    
    # Display summary
    display_imported_data(db_path)


def display_imported_data(db_path):
    """Display the imported data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("IMPORTED PLAYER DATA SUMMARY")
    print("="*70 + "\n")
    
    cursor.execute('''
        SELECT p.player_id, p.player_name, p.total_matches, p.wins, p.win_rate,
               ps.points_won, ps.forehand_winners, ps.backhand_winners
        FROM players p
        LEFT JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE p.player_name IN ('Rakshit', 'Ashwani', 'Mohnish', 'Ashar')
    ''')
    
    players = cursor.fetchall()
    
    for player in players:
        player_id, name, matches, wins, win_rate, points, fh_winners, bh_winners = player
        print(f"🏓 {name} (ID: {player_id})")
        print(f"   Total Matches: {matches}")
        print(f"   Wins: {wins}")
        print(f"   Win Rate: {win_rate}%")
        print(f"   Points Won: {points}")
        print(f"   Forehand Winners: {fh_winners}")
        print(f"   Backhand Winners: {bh_winners}")
        
        # Get coaching insight
        cursor.execute('''
            SELECT insight_text
            FROM coaching_insights
            WHERE player_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (player_id,))
        
        insight = cursor.fetchone()
        if insight:
            lines = insight[0].split('\n')
            key_strength = [l for l in lines if 'Key Strength:' in l]
            if key_strength:
                print(f"   {key_strength[0].strip()}")
        
        print()
    
    # Database statistics
    cursor.execute('SELECT COUNT(*) FROM players')
    total_players = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM matches')
    total_matches = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM player_stats')
    total_stats = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM coaching_insights')
    total_insights = cursor.fetchone()[0]
    
    print("="*70)
    print("DATABASE STATISTICS:")
    print(f"  📊 Total Players: {total_players}")
    print(f"  🏆 Total Matches: {total_matches}")
    print(f"  📈 Stats Records: {total_stats}")
    print(f"  💡 Coaching Insights: {total_insights}")
    print("="*70 + "\n")
    
    conn.close()


def main():
    # CSV file path
    csv_file = r"C:\Users\12rak\Downloads\data - Sheet1.csv"
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: CSV file not found at {csv_file}")
        return
    
    # Import data
    import_csv_to_database(csv_file)
    
    print("✅ CSV data successfully converted to SQLite database!")
    print(f"✅ Database location: paddlecoach.db")
    print("\n💡 You can now use this data for:")
    print("   • AI chatbot training")
    print("   • Performance analysis")
    print("   • Coaching recommendations")
    print("   • Match history tracking\n")


if __name__ == "__main__":
    main()
