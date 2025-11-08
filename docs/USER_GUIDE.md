# PaddleCoach User Guide

**Welcome to PaddleCoach!** 🏓  
Your AI-powered ping pong analytics and coaching platform.

**Version:** 1.0.0  
**Author:** Rakshit  
**Last Updated:** November 7, 2025

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Live Match Tracking](#live-match-tracking)
4. [Player Statistics](#player-statistics)
5. [AI Coaching](#ai-coaching)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Getting Started

### System Requirements

- **Browser:** Chrome, Firefox, Safari, or Edge (latest version)
- **Camera:** HD camera for video tracking (optional for stats viewing)
- **Internet:** Stable connection for real-time updates
- **Screen:** 1280x720 minimum resolution

### First Time Setup

1. **Access the Platform**
   - Open your web browser
   - Navigate to `http://localhost:5000` (or your deployment URL)
   - You'll see the PaddleCoach home page

2. **Create Your Profile** *(Coming Soon)*
   - Currently in development mode - profiles auto-generated
   - Future versions will have user registration

3. **Set Up Your Camera** (for live tracking)
   - Position camera to capture the entire ping pong table
   - Ensure good lighting conditions
   - Test camera feed in the Live Match page

---

## Dashboard Overview

### Home Page

The home page provides quick access to all main features:

- **🏓 Live Match Tracking** - Start tracking a match in real-time
- **📈 Player Statistics** - View detailed performance analytics
- **🤖 AI Coaching** - Get personalized coaching insights

### Navigation Bar

The top navigation bar is always visible and provides quick access to:
- **Home** - Return to main dashboard
- **Live Match** - Real-time match tracking
- **Player Stats** - Performance analytics
- **AI Coaching** - Coaching dashboard

---

## Live Match Tracking

### Starting a Match

1. Click **"Live Match"** in the navigation
2. Click **"Start Match"** button
3. The system will begin tracking automatically

### During the Match

**Scoreboard Display:**
- Live score updates for both players
- Current set number
- Server indicator
- Match duration timer

**Match Controls:**
- **Start Match** - Begin tracking
- **Pause** - Temporarily pause the match
- **End Match** - Complete and save the match

**Real-time Stats:**
- Total shots played
- Average rally length
- Longest rally
- Total points

### Viewing Match History

Recent points are displayed below the scoreboard, showing:
- Point number
- Winner
- Rally length (number of shots)

---

## Player Statistics

### Accessing Your Stats

1. Navigate to **"Player Stats"** page
2. Select your player profile from the dropdown
3. Click **"Load Stats"** to view your performance

### Performance Overview

**Main Metrics:**
- **Total Matches** - Number of matches played
- **Win Rate** - Percentage of matches won
- **Avg Points/Match** - Average points scored per match
- **Total Points Won** - Cumulative points across all matches

### Shot Analysis

Detailed breakdown of shot performance:
- **Forehand Accuracy** - Success rate of forehand shots
- **Backhand Accuracy** - Success rate of backhand shots
- **Serve Accuracy** - Service success rate
- **Smash Success Rate** - Percentage of successful smashes

### Performance Trends

**Interactive Charts:**
- **Performance Trend** - Line chart showing win rate and accuracy over time
- **Shot Distribution** - Pie chart of shot type usage

### Match History

View recent matches with:
- Date and opponent
- Final score
- Result (Win/Loss)
- Points won
- Quick access to detailed match reports

### Stats Bot

Ask questions about your performance in natural language!

**Example Questions:**
- "How many matches have I won this month?"
- "What's my best shot?"
- "Am I improving my forehand?"
- "Show me my recent win rate"

**How to Use:**
1. Type your question in the chat input
2. Press Enter or click "Send"
3. StatsBot will analyze your data and respond

---

## AI Coaching

### Coaching Modules

PaddleCoach offers three AI-powered coaching modules:

#### 1. 🎯 Pro Comparison

Compare your technique with professional players.

**How to Use:**
1. Click "Start Comparison"
2. Upload a video of your technique or use live camera
3. AI analyzes your form and compares with pro players
4. Review insights on technique similarities and differences

**What You'll Learn:**
- Stance analysis
- Arm motion comparison
- Footwork evaluation
- Areas for improvement

#### 2. 🎬 Visual Demo

Generate demonstration videos for specific techniques.

**How to Use:**
1. Click "Generate Demo"
2. Select the technique you want to learn
3. AI generates a synthetic demonstration video
4. Watch and practice the correct form

**Available Techniques:**
- Forehand topspin
- Backhand block
- Serve variations
- Smash technique

#### 3. 🎙️ Live Coach

Real-time coaching feedback during practice.

**How to Use:**
1. Click "Start Live Coaching"
2. Start your camera feed
3. Practice your shots
4. Receive real-time audio feedback

**Features:**
- Pose detection and analysis
- Shot-by-shot feedback
- Audio commentary
- Improvement tracking

### Coaching Insights Panel

The insights panel shows:
- **Technique Analysis** - Current form evaluation
- **Live Feedback** - Real-time suggestions
- **Audio Commentary** - Click to hear verbal coaching

### Progress Tracking

Monitor your improvement with:
- Total coaching sessions
- Training time
- Performance improvement percentage
- Areas mastered

---

## Tips & Best Practices

### For Best Tracking Results

1. **Camera Setup**
   - Mount camera 3-5 meters from table
   - Position to capture entire table surface
   - Avoid backlighting (don't point at windows)
   - Use consistent lighting

2. **During Matches**
   - Keep camera stable (use tripod if possible)
   - Avoid objects blocking the table
   - Ensure players are in frame

3. **For Accurate Stats**
   - Start match tracking before first serve
   - Don't pause unnecessarily
   - End match properly to save data

### Improving Your Game

1. **Review Stats Regularly**
   - Check weekly performance trends
   - Identify weak areas
   - Track improvement over time

2. **Use AI Coaching**
   - Complete at least 2-3 sessions per week
   - Focus on one technique at a time
   - Practice recommended drills

3. **Ask StatsBot**
   - Use natural language queries
   - Ask about specific shots or patterns
   - Get comparative insights

---

## Troubleshooting

### Common Issues

**Camera Not Working**
- Check browser permissions for camera access
- Ensure camera is not used by another application
- Try refreshing the page
- Use "Start Camera" button in coaching dashboard

**Real-time Updates Not Working**
- Check internet connection
- Look for connection status indicator
- Refresh the page to reconnect
- Check if server is running

**Charts Not Loading**
- Ensure JavaScript is enabled
- Clear browser cache
- Check browser console for errors
- Try a different browser

**Stats Bot Not Responding**
- Check your query format
- Try simpler questions
- Ensure player profile is selected
- Refresh the page

### Performance Issues

**If the app is slow:**
- Close unnecessary browser tabs
- Reduce video quality settings
- Clear browser cache and cookies
- Check system resources (CPU, RAM)

---

## FAQ

### General Questions

**Q: Do I need special equipment?**  
A: Just a computer with a camera and a ping pong table. HD camera recommended but not required.

**Q: Can I use this on mobile?**  
A: The interface is responsive, but full features work best on desktop/laptop. Mobile support is being improved.

**Q: Is my data private?**  
A: Yes, all data is stored locally or on your private server. We don't share any personal information.

### Features

**Q: How accurate is the tracking?**  
A: Our AI uses YOLOv12N and Faster R-CNN for 90%+ accuracy in good lighting conditions.

**Q: Can I compare with specific pro players?**  
A: Currently compares with general pro database. Specific player comparison coming in future updates.

**Q: Does the audio coaching work offline?**  
A: No, audio generation requires internet connection to ElevenLabs API.

### Technical

**Q: What browsers are supported?**  
A: Chrome, Firefox, Safari, and Edge (latest versions). Chrome recommended for best performance.

**Q: Can I export my statistics?**  
A: Export feature is planned for future release. Currently view-only in the interface.

**Q: How much storage does the app use?**  
A: Minimal - statistics are stored in database. Videos are optional and can be deleted.

---

## Getting Help

### Support Resources

- **Documentation:** Check `docs/` folder for technical documentation
- **API Reference:** See `API_DOCUMENTATION.md` for developers
- **Deployment Guide:** See `DEPLOYMENT.md` for setup instructions

### Contact

For bugs, feature requests, or questions:
- Contact the development team
- Check GitHub repository for updates
- Review the project README

---

## What's Next?

Future features in development:
- User authentication and profiles
- Multiplayer tournament mode
- Advanced AI coaching with custom drills
- Mobile app version
- Export and sharing capabilities
- Social features and leaderboards

---

**Thank you for using PaddleCoach!** 🏓

We hope this platform helps you improve your game and enjoy ping pong even more. Keep practicing, track your progress, and have fun!

*Happy paddling!*
