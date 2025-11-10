using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;
using FlockingSimulator.Domain.Config;
using System.Numerics;
using System;

namespace FlockingSimulator.Infrastructure.Factories
{
    // Factory class to create Boid instances with random positions
    public class BoidFactory
    {
        private readonly IFlockingBehavior _behavior;
        private readonly Random _random = new();

        public BoidFactory(IFlockingBehavior behavior)
        {
            _behavior = behavior;
        }

        public Boid CreateRandomBoid()
        {
            return new Boid(_behavior, _random.NextDouble() > 0.5)
            {
                Position = new Vector2((float)(_random.NextDouble() * PhysicsConfig.CanvasWidth),
                                       (float)(_random.NextDouble() * PhysicsConfig.CanvasHeight)),
                Velocity = new Vector2((float)(_random.NextDouble() * 2 - 1), (float)(_random.NextDouble() * 2 - 1))
            };
        }
    }
}
