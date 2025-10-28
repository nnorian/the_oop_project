using System.Numerics;
using FlockingSimulator.Domain.Interfaces;

namespace FlockingSimulator.Domain.Entities
{
    // this class represents a boid in the flocking simulation
    public class Boid : SpaceObject
    {
        private IFlockingBehavior behavior;
        public bool IsAggressive { get; private set; }

        // constructor to initialize a boid with a specific behavior and aggression state
        public Boid(IFlockingBehavior behavior, bool isAggressive)
        {
            this.behavior = behavior;
            IsAggressive = isAggressive;
            Radius = 5f;
        }

        // method to calculate the steering vector based on neighboring boids
        public Vector2 CalculateFlocking(IEnumerable<SpaceObject> neighbors)
        {
            return behavior.CalculateSteering(this, neighbors);
        }

        // method to change the boid's behavior at runtime
        public void SetBehavior(IFlockingBehavior newBehavior) => behavior = newBehavior;
    }
}
