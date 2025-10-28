using System.Numerics;

namespace FlockingSimulator.Domain.Entities
{
    public abstract class SpaceObject
    {
        public Vector2 Position { get; set; } = Vector2.Zero;
        public Vector2 Velocity { get; set; } = Vector2.Zero;
        // Angle in radians
        public float Rotation { get; set; } = 0f; 
        public float Radius { get; set; } = 1f;
    }
}