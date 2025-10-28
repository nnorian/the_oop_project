using System.Numerics;

namespace FlockingSimulator.Domain.Entities
{
    // this class represents a missile fired by the player's ship
    public class Missile : SpaceObject
    {
        // constructor to initialize the missile's
        // position and velocity based on the ship's rotation
        public bool IsActive { get; set; } = true;
        public float LifeTime { get; set; } = 3.0f;
    }
}