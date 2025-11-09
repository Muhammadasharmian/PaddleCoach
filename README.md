# 🏓 ToSpinOrNotToSpin

**AI-Powered Table Tennis Coaching Platform**

PaddleCoach is an innovative web application that leverages artificial intelligence to revolutionize table tennis training. From beginners to professionals, our platform provides cutting-edge tools to analyze performance, track progress, and elevate your game.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Muhammadasharmian/PaddleCoach)

---

## 🌟 Features

### Core Training Tools

#### 🎯 **Ball Tracking & Heat Map**
Track every ball movement with precision. Visualize your shot patterns with heat maps to identify strengths and weaknesses in your game strategy.

#### 🏃 **Real-Time Body Tracking**
AI-powered body tracking captures your movements, posture, and technique. Get instant feedback on your form and positioning during play.

#### 🎙️ **AI Voice Coach (VEO)**
Your personal AI coach guides you through training with voice commands and real-time feedback. Train smarter with intelligent coaching technology.

#### 💬 **Game History Chatbot**
Chat with your game database! Ask questions about past matches, get insights, and receive personalized recommendations based on your complete playing history.

#### 🏆 **Professional Player Analysis** *(Pro Feature)*
Analyze top-ranked players, upload match videos for detailed breakdowns, or simulate hypothetical matches. Learn from the best players in the world.

#### 🥇 **Multi-Sport Analysis** *(New)*
Upload videos of any sport and our AI automatically generates body tracking analysis. Perfect for coaches and athletes across multiple disciplines.

---

## 🚀 Coming Soon

We're expanding our AI-powered coaching technology to bring you the same advanced analytics across multiple sports:

- ⚽ **Football**
- 🎾 **Tennis**
- ⚾ **Baseball**
- 🏏 **Cricket**
- 🏀 **Basketball**
- 🏐 **Volleyball**

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Icons:** Font Awesome 6.4.0
- **Authentication:** Local Storage (Backend integration pending)
- **Design:** Responsive, Mobile-First Design
- **Animations:** CSS Animations & Transitions

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Muhammadasharmian/PaddleCoach.git
   cd PaddleCoach
   ```

2. **Open the project:**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     # Using Python
     python -m http.server 8000
     
     # Using Node.js (http-server)
     npx http-server
     ```

3. **Access the application:**
   - Open `http://localhost:8000` in your browser

---

## 📁 Project Structure

```
PaddleCoach/
├── index.html          # Main HTML file
├── styles.css          # All styling and responsive design
├── script.js           # JavaScript functionality and interactions
├── landing_image.png   # Hero section image
├── TASK_DIVISION.md    # Task distribution document
├── ping_pong_uml.md    # UML diagrams
└── README.md           # Project documentation
```

---

## 🎨 Key Features Implementation

### Authentication System
- User signup with email verification
- Login with persistent sessions (localStorage)
- User menu with logout functionality
- Protected feature access (login required)

### Dynamic Content
- Sections reorder based on login state
- Hero section visibility control
- Personalized user experience

### File Upload
- Video upload for match analysis
- Support for multiple video formats
- File size and type validation

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimizations
- Smooth animations and transitions

---

## 🔐 Authentication Flow

1. **Sign Up:** Users create an account with name, email, and password
2. **Verification:** Email verification step (UI implemented)
3. **Login:** Secure login with credential validation
4. **Session:** Persistent login state using localStorage
5. **Protected Features:** All feature buttons require authentication

---

## 🎯 Usage

### For Players:
1. **Sign Up/Login** to access all features
2. **Upload Match Videos** for AI analysis
3. **Track Your Progress** with ball and body tracking
4. **Chat with AI Coach** for personalized feedback
5. **Compare with Pros** to improve your technique

### For Coaches:
1. **Multi-Sport Analysis** for diverse training programs
2. **Professional Analysis Tools** for detailed breakdowns
3. **Historical Data Access** to track athlete progress

---

## 🚧 Roadmap

- [ ] Backend API integration
- [ ] Real video processing and analysis
- [ ] AI model integration for ball/body tracking
- [ ] WebRTC for live coaching sessions
- [ ] Payment gateway for Pro features
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Social features (share, compete)

---

## 👥 Contributors

- **Ashwani Mishra** - [@Ashwani564](https://github.com/Ashwani564)
- **Mohnish Sao** - [@mohnish-dev](https://github.com/mohnish-dev)
- **Muhammad Ashar Mian** - [@Muhammadasharmian](https://github.com/Muhammadasharmian)
- **Rakshit Jaiswal** - [@Raksj12](https://github.com/Raksj12)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Muhammadasharmian/PaddleCoach/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Contact

**Project Link:** [https://github.com/Muhammadasharmian/PaddleCoach](https://github.com/Muhammadasharmian/PaddleCoach)

---

## 🙏 Acknowledgments

- Font Awesome for icons
- AI/ML community for inspiration
- Table tennis community for valuable feedback

---

<div align="center">
  <strong>Built with ❤️ for the table tennis community</strong>
  <br>
  <sub>© 2025 PaddleCoach. All rights reserved.</sub>
</div>
