using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;
using System.Numerics;

namespace FlockingSimulator.Infrastructure.Factories
{
    // Factory class to create Boid instances with random positions
    public class BoidFactory
    {
        // Flocking behavior to be assigned to created boids
        private readonly IFlockingBehavior behavior;

        public BoidFactory(IFlockingBehavior behavior)
        {
            this.behavior = behavior;
        }

        // Method to create a boid with a random position within the canvas bounds
        public Boid CreateRandomBoid()
        {
            var random = new Random();
            return new Boid(behavior, random.NextDouble() > 0.5)
            {
                // Assign a random position within the defined canvas dimensions
                Position = new Vector2((float)(random.NextDouble() * PhysicsConfig.CanvasWidth),
                                       (float)(random.NextDouble() * PhysicsConfig.CanvasHeight))
            };
        }
    }
}
