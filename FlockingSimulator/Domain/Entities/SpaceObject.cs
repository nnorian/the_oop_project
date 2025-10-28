using System.Numerics;

namespace FlockingSimulator.Domain.Entities
{
    public abstract class SpaceObject
    {
        public Vector2 Position { get; set; }
        public Vector2 Velocity { get; set; }
        // rotation angle in radians
        public float Rotation { get; set; }
        public float Radius { get; set; }
    }
}