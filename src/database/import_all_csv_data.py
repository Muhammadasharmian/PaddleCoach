"""
PaddleCoach - Import Multiple CSV Files
Author: Rakshit
Description: Import professional players and personal stats into database
"""

import csv
import sqlite3
import os

DB_PATH = 'C:\\Users\\12rak\\Downloads\\PaddleCoach-main\\PaddleCoach-main\\paddlecoach.db'

def import_professional_players(csv_file_path):
    """Import professional player data (WANG Chuqin, FAN Zhendong, etc.)"""
    
    print("\n" + "="*70)
    print("IMPORTING PROFESSIONAL PLAYERS DATA")
    print("="*70 + "\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"✓ Reading CSV: {csv_file_path}\n")
    
    imported_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            player_name = row['Player Name']
            country = row['Country']
            world_rank = row['ITTF World Rank (Approx.)']
            titles = row['Major Singles Titles']
            win_rate_str = row['Win Rate (Career Approx.)'].strip().rstrip('%~').replace('~', '')
            win_rate = float(win_rate_str)
            highest_rank = row['Highest World Rank']
            style = row['Dominant Style / Grip']
            
            # Check if player exists
            cursor.execute('SELECT player_id FROM players WHERE player_name = ?', (player_name,))
            existing = cursor.fetchone()
            
            if existing:
                player_id = existing[0]
                print(f"  Player '{player_name}' already exists, updating...")
                
                # Update player
                cursor.execute('''
                    UPDATE players
                    SET skill_level = 'professional',
                        win_rate = ?
                    WHERE player_id = ?
                ''', (win_rate, player_id))
                
            else:
                # Create professional player
                cursor.execute('''
                    INSERT INTO players (player_name, skill_level, total_matches, wins, losses, win_rate)
                    VALUES (?, 'professional', 100, ?, ?, ?)
                ''', (player_name, int(100 * win_rate / 100), int(100 * (100 - win_rate) / 100), win_rate))
                
                player_id = cursor.lastrowid
                print(f"✓ Created professional player '{player_name}' (ID: {player_id})")
            
            # Create a reference match for this pro
            cursor.execute('''
                INSERT INTO matches (player1_id, player2_id, winner_id, status, total_points, location)
                VALUES (?, ?, ?, 'completed', 100, ?)
            ''', (player_id, player_id, player_id, country))
            
            match_id = cursor.lastrowid
            
            # Insert professional stats
            cursor.execute('''
                INSERT INTO player_stats (
                    player_id, match_id, forehand_winners, backhand_winners,
                    aces, points_won, points_lost, avg_rally_length
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player_id, match_id,
                45,  # High forehand winners for pros
                35,  # High backhand winners
                15,  # Aces
                int(100 * win_rate / 100),  # Points won based on win rate
                int(100 * (100 - win_rate) / 100),  # Points lost
                8.5  # Longer rallies for pros
            ))
            
            # Create detailed coaching insight for professional players
            insight_text = f"""Professional Player Profile: {player_name}

Country: {country}
ITTF World Rank: {world_rank}
Highest World Rank: {highest_rank}
Major Titles: {titles}
Career Win Rate: {win_rate}%
Playing Style: {style}

Analysis:
This is a world-class professional player. Study their technique, shot selection, and tactical approach. Key areas to learn from:
- High-level tactical awareness
- Consistent shot execution
- Mental strength under pressure
- Advanced stroke mechanics
- Tournament experience

Recommendation: Use this player as a benchmark for your own development. Analyze their matches to understand professional-level play."""
            
            cursor.execute('''
                INSERT INTO coaching_insights (
                    player_id, insight_type, insight_text, priority
                )
                VALUES (?, 'professional_profile', ?, 'high')
            ''', (player_id, insight_text))
            
            print(f"  ├─ Match record: {titles}")
            print(f"  ├─ Win Rate: {win_rate}%")
            print(f"  ├─ Style: {style}")
            print(f"  └─ Coaching insight added\n")
            
            imported_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported {imported_count} professional players!\n")


def import_personal_stats(csv_file_path):
    """Import personal player statistics"""
    
    print("="*70)
    print("IMPORTING PERSONAL PLAYER STATISTICS")
    print("="*70 + "\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print(f"✓ Reading CSV: {csv_file_path}\n")
    
    imported_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            player_name = row['Player Name']
            matches_played = int(row['Matches Played'])
            matches_won = int(row['Matches Won'])
            serve_win_rate = float(row['Serve Win Rate'].rstrip('%'))
            attack_success = float(row['Attack Success Rate'].rstrip('%'))
            performance_score = int(row['Performance Score (Self-Rated)'])
            accuracy = float(row['Percentage Accuracy'].rstrip('%'))
            signature_shot = row['Signature Shot / Key Factor']
            
            # Calculate win rate
            win_rate = (matches_won / matches_played * 100) if matches_played > 0 else 0
            losses = matches_played - matches_won
            
            # Check if player exists
            cursor.execute('SELECT player_id FROM players WHERE player_name = ?', (player_name,))
            existing = cursor.fetchone()
            
            if existing:
                player_id = existing[0]
                print(f"  Player '{player_name}' already exists, updating...")
                
                # Update existing player
                cursor.execute('''
                    UPDATE players
                    SET total_matches = ?,
                        wins = ?,
                        losses = ?,
                        win_rate = ?
                    WHERE player_id = ?
                ''', (matches_played, matches_won, losses, win_rate, player_id))
                
            else:
                # Determine skill level based on win rate and performance
                if win_rate >= 75 and performance_score >= 1600:
                    skill_level = 'advanced'
                elif win_rate >= 50 and performance_score >= 1400:
                    skill_level = 'intermediate'
                else:
                    skill_level = 'beginner'
                
                # Create new player
                cursor.execute('''
                    INSERT INTO players (player_name, skill_level, total_matches, wins, losses, win_rate)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (player_name, skill_level, matches_played, matches_won, losses, win_rate))
                
                player_id = cursor.lastrowid
                print(f"✓ Created player '{player_name}' (ID: {player_id}) - {skill_level}")
            
            # Create match records for each match played
            for i in range(matches_played):
                is_win = i < matches_won
                winner_id = player_id if is_win else None
                
                cursor.execute('''
                    INSERT INTO matches (player1_id, player2_id, winner_id, status, total_points)
                    VALUES (?, ?, ?, 'completed', ?)
                ''', (player_id, player_id, winner_id, 11))  # Standard ping pong to 11 points
                
                match_id = cursor.lastrowid
                
                # Insert detailed stats for this match
                cursor.execute('''
                    INSERT INTO player_stats (
                        player_id, match_id, forehand_winners, backhand_winners,
                        aces, errors, points_won, points_lost, avg_rally_length
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    player_id, match_id,
                    int(11 * attack_success / 100),  # Forehand winners
                    int(11 * 0.3),  # Backhand winners
                    int(11 * serve_win_rate / 100),  # Aces based on serve win
                    int(11 * (100 - accuracy) / 100),  # Errors based on accuracy
                    11 if is_win else 7,  # Points won/lost
                    7 if is_win else 11,
                    5.5  # Average rally length
                ))
            
            # Create comprehensive coaching insight
            insight_text = f"""Personal Performance Analysis: {player_name}

📊 Match Statistics:
- Matches Played: {matches_played}
- Matches Won: {matches_won}
- Win Rate: {win_rate:.1f}%
- Serve Win Rate: {serve_win_rate}%
- Attack Success Rate: {attack_success}%
- Overall Accuracy: {accuracy}%
- Performance Score: {performance_score}

🎯 Signature Shot: {signature_shot}

💡 Strengths:
- Your {signature_shot.lower()} is your most effective weapon
- Consistent accuracy of {accuracy}%
- {"Strong" if attack_success >= 70 else "Developing"} attack game

🎓 Areas for Improvement:
{"- Work on increasing win rate (currently " + str(win_rate) + "%)" if win_rate < 70 else "- Maintain excellent win rate"}
{"- Improve serve effectiveness (currently " + str(serve_win_rate) + "%)" if serve_win_rate < 60 else "- Continue refining serve"}
{"- Focus on attack consistency (currently " + str(attack_success) + "%)" if attack_success < 75 else "- Keep up strong attack game"}

🏆 Recommendations:
1. Practice your {signature_shot.lower()} regularly to maintain your edge
2. Study professional players' techniques for inspiration
3. Work on mental game and match strategy
4. {"Increase match play experience" if matches_played < 20 else "Continue building competitive experience"}
"""
            
            cursor.execute('''
                INSERT INTO coaching_insights (
                    player_id, insight_type, insight_text, priority
                )
                VALUES (?, 'personal_analysis', ?, 'high')
            ''', (player_id, insight_text))
            
            print(f"  ├─ {matches_played} match records created")
            print(f"  ├─ Win Rate: {win_rate:.1f}%")
            print(f"  ├─ Signature: {signature_shot}")
            print(f"  └─ Personal coaching insight added\n")
            
            imported_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ Imported {imported_count} personal player profiles!\n")


def display_all_data():
    """Display all imported data"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("="*70)
    print("COMPLETE DATABASE SUMMARY")
    print("="*70 + "\n")
    
    # Get all players
    cursor.execute('''
        SELECT p.player_id, p.player_name, p.skill_level, p.total_matches, 
               p.wins, p.losses, p.win_rate
        FROM players p
        ORDER BY p.win_rate DESC
    ''')
    
    players = cursor.fetchall()
    
    for player in players:
        player_id, name, skill, matches, wins, losses, win_rate = player
        
        print(f"🏓 {name}")
        print(f"   Skill Level: {skill.upper()}")
        print(f"   Matches: {matches} | Wins: {wins} | Losses: {losses}")
        print(f"   Win Rate: {win_rate}%")
        
        # Get latest insight
        cursor.execute('''
            SELECT insight_type, created_at
            FROM coaching_insights
            WHERE player_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (player_id,))
        
        insight = cursor.fetchone()
        if insight:
            print(f"   Latest Insight: {insight[0]} ({insight[1][:10]})")
        
        print()
    
    # Database totals
    cursor.execute('SELECT COUNT(*) FROM players')
    total_players = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM matches')
    total_matches = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM player_stats')
    total_stats = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM coaching_insights')
    total_insights = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM ai_commentary')
    total_commentary = cursor.fetchone()[0]
    
    print("="*70)
    print("📊 DATABASE TOTALS:")
    print(f"   Players: {total_players}")
    print(f"   Matches: {total_matches}")
    print(f"   Stats Records: {total_stats}")
    print(f"   Coaching Insights: {total_insights}")
    print(f"   Commentary: {total_commentary}")
    print("="*70 + "\n")
    
    conn.close()


def main():
    print("\n" + "="*70)
    print("PADDLECOACH - COMPREHENSIVE DATA IMPORT")
    print("="*70 + "\n")
    
    # File paths
    professional_csv = r"C:\Users\12rak\Downloads\second table - Sheet1.csv"
    personal_csv = r"C:\Users\12rak\Downloads\personal table - Sheet1.csv"
    
    # Import professional players
    if os.path.exists(professional_csv):
        import_professional_players(professional_csv)
    else:
        print(f"⚠️  Professional players CSV not found: {professional_csv}\n")
    
    # Import personal stats
    if os.path.exists(personal_csv):
        import_personal_stats(personal_csv)
    else:
        print(f"⚠️  Personal stats CSV not found: {personal_csv}\n")
    
    # Display summary
    display_all_data()
    
    print("="*70)
    print("✅ ALL CSV DATA SUCCESSFULLY IMPORTED!")
    print("="*70)
    print("\n💡 Your database now contains:")
    print("   • Professional player profiles (WANG Chuqin, FAN Zhendong)")
    print("   • Personal player statistics and match history")
    print("   • Detailed performance metrics")
    print("   • Personalized coaching insights")
    print("   • Ready for AI chatbot training!\n")


if __name__ == "__main__":
    main()
