namespace FlockingSimulator.Domain.Config
{
    // This static class holds configuration constants for boid behavior
    public static class BoidConfig
    {
        // maximum speed of a boid in pixels per second
        public const float MaxSpeed = 120f; 
        // pixels / second
        public const float MaxForce = 150f;
        // steering force magnitude
        public const int FlockCount = 25;
    }
}