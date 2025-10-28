namespace FlockingSimulator.Domain.Config
{
    public static class PhysicsConfig
    {
        // time step for physics updates in seconds
        public const float DeltaTime = 1f / 60f; // seconds per update (~60fps)
        // dimensions of the simulation canvas in pixels
        public const float CanvasWidth = 840f;
        // pixels
        public const float CanvasHeight = 460f;
    }
}