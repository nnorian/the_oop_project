# Flocking Simulator

A real-time interactive flocking simulation game built with ASP.NET Core Blazor Server and C#. The project demonstrates advanced object-oriented programming principles, design patterns, and realistic boid behavior algorithms.

## Overview

This application simulates emergent flocking behavior through autonomous agents (boids) that follow simple local rules, resulting in complex group dynamics. Players control a ship to interact with two types of boids: passive white boids and aggressive red boids, creating an engaging gameplay experience that showcases artificial life principles.

## Technical Architecture

### Design Patterns

The project implements several software design patterns to ensure maintainability and scalability:

- **Clean Architecture**: Separation of concerns across Domain, Application, Infrastructure, and Presentation layers
- **Strategy Pattern**: Pluggable flocking behaviors through `IFlockingBehavior` interface
- **Factory Pattern**: Object creation abstraction via `BoidFactory` and `IMissileFactory`
- **Command Pattern**: Input handling through `IInputCommand` implementations
- **Dependency Injection**: Service registration and loose coupling throughout the application

### Project Structure

```
FlockingSimulator/
├── Domain/                    # Core business logic and entities
│   ├── Entities/             # Game objects (Boid, Ship, Missile, SpaceObject)
│   ├── Interfaces/           # Contracts (IFlockingBehavior, ICollisionDetector)
│   └── Config/              # Configuration constants
├── Application/              # Application services and orchestration
│   ├── GameService.cs       # Main game loop coordinator
│   └── Commands/            # Input command implementations
├── Infrastructure/           # Implementation details
│   ├── Behaviors/           # Flocking algorithm implementations
│   ├── Factories/           # Object creation logic
│   ├── Systems/             # Collision detection system
│   └── Rendering/           # JavaScript interop for canvas rendering
├── Pages/                   # Blazor components and routing
│   ├── Flocking.razor      # Main game page
│   ├── _Host.cshtml        # Application host
│   └── _Imports.razor      # Global using directives
├── wwwroot/                # Static assets
│   └── js/game.js         # Canvas rendering functions
├── App.razor              # Blazor router configuration
└── Program.cs             # Application entry point and DI setup
```

## Core Features

### Flocking Algorithm

The simulation implements Craig Reynolds' classical boids algorithm with three fundamental rules:

1. **Separation**: Boids avoid crowding neighbors within a 40-pixel radius
2. **Cohesion**: Boids steer towards the average position of nearby flockmates within a 10-pixel radius
3. **Alignment**: Boids match velocity with neighbors within a 65-pixel perception radius

Additional behaviors include:
- **Ship Avoidance**: Non-aggressive boids actively avoid the player's ship with a 5x stronger force
- **Aggressive Behavior**: Red boids do not avoid the ship and exhibit different flocking characteristics

### Physics Simulation

The game runs at 60 frames per second with the following physics parameters:

- **Boid Maximum Speed**: 1 pixel per frame
- **Boid Maximum Force**: 0.8 units (steering force limit)
- **Ship Maximum Speed**: 200 pixels per second
- **Ship Acceleration**: 500 units with 2% velocity damping per frame
- **Missile Speed**: 300 pixels per second
- **Missile Lifetime**: 3 seconds

### Gameplay Mechanics

- **Player Controls**:
  - Arrow Left/Right: Rotate ship
  - Arrow Up: Accelerate forward
  - Space Bar: Fire missile

- **Game Elements**:
  - 25 boids spawn randomly across the canvas
  - Approximately 10% of boids are aggressive (red)
  - Player starts with 3 lives
  - Score tracking for destroyed boids

- **Collision Detection**: Circle-based collision detection using radius and distance calculations

### Visual Rendering

The application uses HTML5 Canvas for real-time rendering:

- **Canvas Resolution**: 840x460 pixels
- **Boid Rendering**: Triangle shapes with directional indicators
- **Ship Rendering**: Rectangular shape with turret indicator
- **Color Coding**: White for passive boids, red/tomato for aggressive boids, blue for ship, green for missiles

## Technology Stack

- **Backend**: .NET 9.0, ASP.NET Core
- **Frontend**: Blazor Server (Server-Side Rendering)
- **Real-Time Communication**: SignalR via Blazor's interactive components
- **Rendering**: HTML5 Canvas with JavaScript Interop
- **Language**: C# 12

## Installation and Setup

### Prerequisites

- .NET 9.0 SDK or later
- Modern web browser with JavaScript enabled

### Running the Application

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd FlockingSimulator
   ```

2. Build the project:
   ```bash
   dotnet build
   ```

3. Run the application:
   ```bash
   dotnet run
   ```

4. Navigate to `http://localhost:5098/flocking` in your web browser

## Implementation Details

### Key Classes

**SpaceObject** (Abstract Base Class)
- Base class for all game entities
- Properties: Position, Velocity, Rotation, Radius

**Boid**
- Implements flocking behavior via strategy pattern
- Properties: IsAggressive flag for behavior differentiation
- Methods: `CalculateFlocking()` delegates to `IFlockingBehavior`

**Ship**
- Player-controlled entity
- Methods: `Rotate()`, `Accelerate()`, `FireMissile()`
- Physics: Velocity damping, screen wrapping

**Missile**
- Projectile with limited lifetime
- Auto-removal after 3 seconds or upon collision

**GameService**
- Central game coordinator
- Manages game state, updates all entities, handles collisions
- Update loop: 60 FPS via `System.Timers.Timer`

**SimpleFlockingBehavior**
- Implements Reynolds' boids algorithm
- Configurable perception radii for each behavior
- Ship avoidance logic for non-aggressive boids

## Future Enhancements

Potential improvements based on original Python implementation:

- Missile limit (maximum 3 active missiles)
- Ship-boid collision damage system
- Refined scoring system (1 point per aggressive boid, 0.5 points for collisions)
- Win/lose conditions
- Game state management (start screen, victory screen, game over)
- Sound effects and visual effects
- Performance optimizations for larger flocks

## Learning Outcomes

This project demonstrates proficiency in:

- Object-oriented design and SOLID principles
- Real-time web applications with Blazor
- Algorithm implementation (flocking, collision detection)
- JavaScript interoperability in .NET
- Clean architecture and separation of concerns
- Design pattern application
- Game loop implementation
- Vector mathematics and physics simulation

## License

This project is developed for educational and portfolio purposes.

## Author

Developed as part of Object-Oriented Programming coursework from an initial python script given by the teacher, demonstrating advanced C# and software architecture concepts through interactive simulation.
