namespace FlockingGame.Domain.Config
{
    // This static class holds configuration constants for boid behavior
    public static class BoidConfig
    {
        public const float MaxSpeed = 3f;
        public const float MaxForce = 0.05F;
        // perception radius for neighbor detection
        public const int FlockCount = 25;
    }
}