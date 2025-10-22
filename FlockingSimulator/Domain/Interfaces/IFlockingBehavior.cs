using System.Numerics;
using FlockingGame.Domain.Entities;

namespace FlockingGame.Domain.Interfaces
{   
    // this interface defines the contract for flocking behaviors
    public interface IFlockingBehavior
    {
        // method to calculate the steering vector for a boid based on its neighbors
        Vector2 CalculateSteering(Boid boid, IEnumerable<SpaceObject> neighbors);
    }
}
