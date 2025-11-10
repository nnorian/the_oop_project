using System.Numerics;

namespace FlockingSimulator.Domain.Entities
{
    // This class represents the player's ship
    public class Ship : SpaceObject
    {
        // Maximum speed for the ship
        private const float MaxShipSpeed = 200f;
        // Acceleration force
        private const float AccelerationForce = 500f;

        // constructor to initialize the ship's properties
        public Ship()
        {
            Radius = 10f;
            // Initial position of the ship in center
            Position = new Vector2(420f, 230f);
        }

        // Rotate the ship by a given angle (in radians)
        public void Rotate(float angle)
        {
            Rotation += angle;
            // Normalize rotation to 0-2π range
            while (Rotation < 0) Rotation += MathF.PI * 2;
            while (Rotation >= MathF.PI * 2) Rotation -= MathF.PI * 2;
        }

        // Accelerate the ship in the direction it's facing
        public void Accelerate()
        {
            // Calculate acceleration vector based on rotation
            var accelX = MathF.Cos(Rotation) * AccelerationForce;
            var accelY = MathF.Sin(Rotation) * AccelerationForce;
            var accel = new Vector2(accelX, accelY);

            // Apply acceleration (using simple physics, deltaTime handled in game loop)
            Velocity += accel * 0.016f; // Approximate 60 FPS frame time

            // Clamp velocity to max speed
            if (Velocity.Length() > MaxShipSpeed)
            {
                Velocity = Vector2.Normalize(Velocity) * MaxShipSpeed;
            }
        }

        // Fire a missile from the ship's position
        public Missile FireMissile()
        {
            // Offset the missile spawn position slightly forward from ship center
            var offsetDistance = Radius + 5f;
            var spawnX = Position.X + MathF.Cos(Rotation) * offsetDistance;
            var spawnY = Position.Y + MathF.Sin(Rotation) * offsetDistance;

            return new Missile
            {
                Position = new Vector2(spawnX, spawnY),
                Rotation = Rotation,
                Velocity = new Vector2(MathF.Cos(Rotation) * 300f, MathF.Sin(Rotation) * 300f),
                Radius = 3f,
                IsActive = true,
                LifeTime = 3.0f
            };
        }
    }
}