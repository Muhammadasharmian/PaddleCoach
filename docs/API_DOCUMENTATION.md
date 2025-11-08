# PaddleCoach API Documentation

**Author:** Rakshit  
**Version:** 1.0.0  
**Last Updated:** November 7, 2025

## Overview

The PaddleCoach API provides RESTful endpoints for accessing match data, player statistics, and AI coaching insights. This documentation covers all frontend-accessible API endpoints.

## Base URL

```
http://localhost:5000/api
```

## Authentication

*Authentication will be implemented in future versions. Currently, all endpoints are publicly accessible for development.*

---

## Endpoints

### Match Endpoints

#### Get Current Match

Get the currently active match data.

**Endpoint:** `GET /match/current`

**Response:**
```json
{
  "success": true,
  "data": {
    "match_id": 1,
    "player1": {
      "id": 1,
      "name": "Player 1",
      "score": 11,
      "sets_won": 2
    },
    "player2": {
      "id": 2,
      "name": "Player 2",
      "score": 9,
      "sets_won": 1
    },
    "current_set": 3,
    "server": "Player 1",
    "status": "active",
    "duration": 1245
  }
}
```

#### Get Match by ID

Retrieve specific match data by match ID.

**Endpoint:** `GET /match/<match_id>`

**Parameters:**
- `match_id` (int, required): Match identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "match_id": 123,
    "date": "2025-11-07T14:30:00Z",
    "player1": {...},
    "player2": {...},
    "sets": [...],
    "duration_seconds": 1800,
    "winner": "Player 1"
  }
}
```

---

### Player Endpoints

#### Get Player Statistics

Retrieve comprehensive statistics for a specific player.

**Endpoint:** `GET /player/<player_id>/stats`

**Parameters:**
- `player_id` (int, required): Player identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "player_id": 1,
    "name": "John Doe",
    "total_matches": 24,
    "wins": 16,
    "losses": 8,
    "win_rate": 66.7,
    "shot_stats": {
      "forehand_accuracy": 72,
      "backhand_accuracy": 65,
      "serve_accuracy": 82
    },
    "performance_trend": [...],
    "recent_matches": [...]
  }
}
```

---

### Coaching Endpoints

#### Get Coaching Insights

Get AI-generated coaching insights for a player.

**Endpoint:** `GET /coaching/insights/<player_id>`

**Parameters:**
- `player_id` (int, required): Player identifier

**Response:**
```json
{
  "success": true,
  "data": {
    "player_id": 1,
    "insights": [
      {
        "category": "technique",
        "title": "Forehand Improvement",
        "description": "Your forehand follow-through has improved...",
        "priority": "medium",
        "progress": 75
      }
    ],
    "pro_comparison": {...},
    "recent_sessions": [...]
  }
}
```

---

### Stats Query Endpoints

#### Query Stats with Natural Language

Ask questions about statistics using natural language.

**Endpoint:** `POST /stats/query`

**Request Body:**
```json
{
  "query": "What's my win rate last month?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "In the last month, you played 8 matches and won 6 of them. That's a 75% win rate!"
}
```

---

### Audio Endpoints

#### Generate Audio Commentary

Generate audio commentary using ElevenLabs TTS.

**Endpoint:** `POST /audio/commentary`

**Request Body:**
```json
{
  "text": "Great shot! Your forehand technique is improving."
}
```

**Response:**
```json
{
  "success": true,
  "audio_url": "/static/audio/commentary_1699392000.mp3"
}
```

---

## WebSocket Events

The application uses Socket.IO for real-time updates.

### Client Events

#### Connect
```javascript
socket.on('connect', () => {
  console.log('Connected to server');
});
```

#### Subscribe to Match Updates
```javascript
socket.emit('subscribe_match', { match_id: 1 });
```

### Server Events

#### Score Update
Broadcasted when a score changes in a match.
```javascript
socket.on('score_update', (data) => {
  // data.match_id
  // data.score_data
  // data.timestamp
});
```

#### Point Complete
Broadcasted when a point is completed.
```javascript
socket.on('point_complete', (data) => {
  // data.match_id
  // data.point_data
  // data.timestamp
});
```

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

*Rate limiting will be implemented in production. Current development version has no rate limits.*

---

## Examples

### Fetch Current Match (JavaScript)

```javascript
async function getCurrentMatch() {
  try {
    const response = await fetch('/api/match/current');
    const data = await response.json();
    
    if (data.success) {
      console.log('Current match:', data.data);
      return data.data;
    } else {
      console.error('Error:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}
```

### Query Stats (JavaScript)

```javascript
async function askStatsBot(question) {
  try {
    const response = await fetch('/api/stats/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: question })
    });
    
    const data = await response.json();
    return data.success ? data.response : 'Error processing query';
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Subscribe to Real-time Updates (JavaScript)

```javascript
const socket = io();

socket.on('connect', () => {
  socket.emit('subscribe_match', { match_id: 1 });
});

socket.on('score_update', (data) => {
  updateScoreboard(data.score_data);
});

socket.on('point_complete', (data) => {
  displayPointSummary(data.point_data);
});
```

---

## Integration with Backend Services

The frontend API communicates with:

1. **Analytics Service** (Ashar's domain)
   - Implements `IAnalyticsData` interface
   - Provides match and game data

2. **AI Coaching Modules** (Mohnish's domain)
   - Pro comparison insights
   - Live coaching feedback
   - Visual demonstrations

3. **Database Layer** (Ashar's domain)
   - Player profiles
   - Match history
   - Statistics storage

---

## Future Enhancements

- Authentication and authorization
- API versioning
- Pagination for list endpoints
- Advanced filtering and sorting
- Webhook support for external integrations
- GraphQL endpoint option

---

## Support

For questions or issues with the API, please contact the development team or check the main README documentation.
