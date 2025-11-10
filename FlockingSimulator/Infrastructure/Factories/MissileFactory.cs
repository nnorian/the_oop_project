using System.Numerics;
using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;

namespace FlockingSimulator.Infrastructure.Factories
{
    // Factory class to create Missile instances
    public class MissileFactory : IMissileFactory
    {
        // Missile speed in pixels per second
        private const float MissileSpeed = 300f;

        public Missile CreateMissile(Vector2 position, float rotation)
        {
            // Calculate velocity based on rotation angle
            // rotation is in radians, 0 points right, increasing counter-clockwise
            var velocityX = MathF.Cos(rotation) * MissileSpeed;
            var velocityY = MathF.Sin(rotation) * MissileSpeed;

            return new Missile
            {
                Position = position,
                Velocity = new Vector2(velocityX, velocityY),
                Rotation = rotation,
                Radius = 3f,
                IsActive = true,
                LifeTime = 3.0f
            };
        }
    }
}
