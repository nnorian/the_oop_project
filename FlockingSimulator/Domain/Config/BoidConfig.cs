namespace FlockingSimulator.Domain.Config
{
    // This static class holds configuration constants for boid behavior
    public static class BoidConfig
    {
        // Maximum speed of a boid (converted from Python: 1 pixel per frame at 60fps = 60 pixels/sec)
        public const float MaxSpeed = 1f;

        // Maximum steering force (converted from Python: 0.8 force per frame)
        public const float MaxForce = 0.8f;

        // Number of boids in the flock
        public const int FlockCount = 25;

        // Perception radii for flocking behaviors
        public const float PerceptionRadius = 65f;           // General perception for alignment
        public const float CohesionRadius = 10f;             // Close range for cohesion
        public const float SeparationRadius = 40f;           // Range for separation

        // Ship proximity factor - boids avoid ship more strongly
        public const float ShipPresenceFactor = 5f;

        // Aggressive boid rage factor - how strongly they lunge at ship
        public const float BoidRage = 2.5f;
    }
}