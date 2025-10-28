using System.Numerics;
using System.Collections.Generic;
using FlockingSimulator.Domain.Entities;

namespace FlockingSimulator.Domain.Interfaces
{   
    // this interface defines the contract for flocking behaviors
    public interface IFlockingBehavior
    {
        // method to calculate the steering vector for a boid based on its neighbors
        Vector2 CalculateSteering(Boid boid, IEnumerable<SpaceObject> neighbors);
    }
}
