# Ping Pong Vision - UML System Design

## Overview

This document provides the complete UML structure for the "Ping Pong Vision" system, including both **Class Diagrams** (static structure) and **Component Diagrams** (architectural layout).

---

## 1. Class Diagram - Static Structure

### Core Classes

#### Match
**Purpose**: Represents a complete match between two players

**Attributes**:
- `matchID: string`
- `player1Name: string`
- `player2Name: string`
- `startTime: DateTime`
- `games: List<Game>`

**Methods**:
- `startMatch(): void`
- `endMatch(): void`
- `getWinner(): string`

**Relationships**:
- **Composition** with `Game` (1 Match contains 1..* Games)
- **Association** with `PlayerProfile` (1 Match involves 2 Players)

---

#### Game
**Purpose**: Represents a single game within a match

**Attributes**:
- `gameID: string`
- `player1Score: int`
- `player2Score: int`

**Methods**:
- `addPoint(player: string): void`
- `isGameOver(): boolean`
- `getGameWinner(): string`

**Relationships**:
- **Aggregation** with `Match` (1 Game belongs to 1 Match)
- **Association** with `Shot` (1 Game contains 0..* Shots)

---

#### PlayerProfile
**Purpose**: Stores player statistics and historical data

**Attributes**:
- `playerID: string`
- `playerName: string`
- `totalWins: int`
- `totalLosses: int`

**Methods**:
- `getForehandRatio(): float`
- `getMatchHistory(): List<Match>`

**Relationships**:
- **Association** with `Match` (1 Player participates in 0..* Matches)

---

#### Shot
**Purpose**: Captures individual shot data from vision tracking

**Attributes**:
- `shotID: string`
- `timestamp: float`
- `start_x: float`
- `start_y: float`
- `end_x: float`
- `end_y: float`
- `speed: float`
- `type: string` (e.g., 'forehand', 'backhand', 'serve')

**Methods**:
- `calculateSpeed(): float`

**Relationships**:
- **Association** with `Game` (1 Shot belongs to 1 Game)
- **Association** with `Point` (1 Shot belongs to 1 Point)

---

#### Point
**Purpose**: Represents a single point in a game

**Attributes**:
- `pointID: string`
- `gameID: string`
- `videoFile: string`
- `shots: List<Shot>`

**Relationships**:
- **Aggregation** with `Game` (1 Point belongs to 1 Game)
- **Composition** with `Shot` (1 Point contains 0..* Shots)
- **Association** with `PoseData` (1 Point can have 0..* PoseData)

---

#### PoseData
**Purpose**: Stores skeletal tracking data from pose estimation

**Attributes**:
- `poseID: string`
- `pointID: string` (foreign key to Point)
- `timestamp: float`
- `keypoints: Dictionary<string, Coordinate>`
- `angles: Dictionary<string, float>`

**Methods**:
- `compareWith(otherPoseData: PoseData): Dictionary`

**Relationships**:
- **Association** with `Point` (1 PoseData belongs to 1 Point)

---

### Class Diagram Summary

```
Match (1) ---<composed of>--- (1..*) Game
Match (1) ---<involves>--- (2) PlayerProfile
Game (1) ---<contains>--- (0..*) Shot
Game (1) ---<contains>--- (0..*) Point
Point (1) ---<contains>--- (0..*) Shot
Point (1) ---<analyzed by>--- (0..*) PoseData
```

---

## 2. Component Diagram - Architectural Structure

### Component Overview

The system is organized into 4 major subsystems, each containing multiple components.

---

### 2.1 VisionSystem (The "Eyes")

**Purpose**: Real-time tracking of ball and player movements

**Sub-Components**:
- `YOLOv12N_Model`
- `FasterRCNN_Model`

**Provides Interface**: `ITrackingData`
- `getBallPosition(): Coordinate`
- `getPlayerMovement(): MovementData`

**Dependencies**: None (lowest layer)

---

### 2.2 AnalyticsService (The "Brain")

**Purpose**: Processes tracking data and manages game state

**Sub-Components**:
- `ShotAnalyzer`
- `ScoreTracker`
- `GameDB_Manager`
- `StatsDB_Manager`

**Provides Interface**: `IAnalyticsData`
- `getCurrentScore(): ScoreData`
- `getMatchHistory(playerID: string): List<Match>`

**Dependencies**:
- **Requires**: `ITrackingData` (from VisionSystem)
- **Requires**: `GameDatabase` (MySQL)
- **Requires**: `StatsDatabase` (MySQL)

---

### 2.3 AICoachingSuite (The "Coach")

**Purpose**: Provides AI-powered coaching and analysis

#### Sub-Component 3A: ProComparison_Module

**Purpose**: Offline analysis comparing user technique to professionals

**Dependencies**:
- **Requires**: `IAnalyticsData` (to read Match, Point, Shot)
- **Requires**: `MediaPipePose` (pose estimation)
- **Requires**: `GeminiAPI` (analysis)

**Data Flow**:
1. **Reads**: Match, Point, Shot (via GameDB_Manager)
2. **Creates**: PoseData (writes back to GameDB_Manager)
3. **Analyzes**: Compares two PoseData sets via Gemini

---

#### Sub-Component 3B: VisualDemo_Module

**Purpose**: Generates synthetic demonstration videos

**Dependencies**:
- **Requires**: `Veo_3.1_API` (video generation)
- **Requires**: `Nano_Banana_API` (video processing)

**Data Flow**:
- **Input**: User text prompt
- **Output**: Generated video
- **Note**: No database interaction

---

#### Sub-Component 3C: LiveCoach_Module

**Purpose**: Real-time coaching feedback during play

**Dependencies**:
- **Subscribes to**: `ShotAnalyzer` (live Shot stream)
- **Requires**: `IAnalyticsData` (to read PlayerProfile)
- **Requires**: `Gemini_2.5_Pro_API` (RAG-based coaching)

**Data Flow**:
1. **Listens**: Live Shot objects from ShotAnalyzer
2. **Reads**: PlayerProfile (historical context)
3. **Analyzes**: RAG prompt combining static knowledge + historical data + live data
4. **Outputs**: Real-time coaching feedback
5. **Note**: Read-only, no database writes

---

### 2.4 UserExperience (The "Interface")

**Purpose**: Frontend presentation layer

**Sub-Components**:
- `WebUI_Component`
- `StatsBot` (conversational interface)

**Dependencies**:
- **Requires**: `IAnalyticsData` (to display scores, stats)
- **Requires**: `AICoachingSuite` (to show coaching feedback)
- **Requires**: `ElevenLabs_API` (text-to-speech commentary)

---

## 3. Component Interaction Matrix

### Data Flow by Coach Module

| Coach Module | Interaction Type | Reads/Listens To | Writes/Creates |
|--------------|------------------|------------------|----------------|
| **3A: Pro Comparison** | Offline Batch | Match, Point (video lookup) | PoseData (saves to database) |
| **3B: Visual Demo** | Standalone | User text prompt only | Nothing to database |
| **3C: Live Coach** | Real-Time Stream | Shot (live), PlayerProfile (historical) | Nothing to database |

---

## 4. Architectural Principles

### Separation of Concerns

1. **VisionSystem**: Data capture only, no business logic
2. **AnalyticsService**: Single source of truth for all game data
3. **AICoachingSuite**: Read-only consumer (except 3A which writes PoseData)
4. **UserExperience**: Presentation layer, no direct data manipulation

### Interface-Based Communication

- Components communicate through well-defined interfaces (ITrackingData, IAnalyticsData)
- Enables loose coupling and independent development
- Vision system doesn't need to know about Coach components

### Scalability Design

- Real-time components (LiveCoach) subscribe to event streams
- Offline components (ProComparison) use batch processing
- Generative components (VisualDemo) operate independently

---

## 5. Database Schema Mapping

### GameDatabase (MySQL)

**Tables**:
- `matches` → Match class
- `games` → Game class
- `points` → Point class
- `shots` → Shot class
- `pose_data` → PoseData class

### StatsDatabase (MySQL)

**Tables**:
- `player_profiles` → PlayerProfile class
- `aggregated_stats` (derived from games/shots)

---

## 6. Implementation Roadmap

### Phase 1: Core Data Layer
1. Implement Match, Game, Point, Shot, PlayerProfile classes
2. Set up MySQL databases (GameDB, StatsDB)
3. Create GameDB_Manager and StatsDB_Manager

### Phase 2: Vision Integration
1. Integrate YOLOv12N and FasterRCNN models
2. Implement ITrackingData interface
3. Connect VisionSystem to AnalyticsService

### Phase 3: Analytics Service
1. Build ShotAnalyzer (event stream publisher)
2. Build ScoreTracker (real-time scoring)
3. Implement data persistence layer

### Phase 4: AI Coaching
1. Implement ProComparison_Module (3A)
2. Implement LiveCoach_Module (3C)
3. Implement VisualDemo_Module (3B)

### Phase 5: User Interface
1. Build frontend UI components
2. Integrate StatsBot
3. Add ElevenLabs commentary
4. Connect all components through interfaces

---

## 7. Key Design Decisions

### Why Component Diagram Matters
- **Modular**: Each component can be developed/tested independently
- **Pluggable**: New AI models can replace existing ones via interfaces
- **Scalable**: Real-time and batch components separated clearly

### Why Class Diagram Matters
- **Database Design**: Direct mapping to MySQL schema
- **Object-Oriented Programming**: Clear structure for code implementation
- **Data Integrity**: Relationships ensure referential integrity

---

## 8. Next Steps

1. ✅ Define UML structure (completed)
2. ⏭️ Design database schema in detail
3. ⏭️ Create API specifications for interfaces
4. ⏭️ Set up development environment
5. ⏭️ Begin Phase 1 implementation

---

## References

- **Class Diagram**: Static blueprint of data entities
- **Component Diagram**: High-level architectural layout
- **Key Question for Classes**: "What data does a Game hold?"
- **Key Question for Components**: "How does the ScoreTracker talk to the Database?"