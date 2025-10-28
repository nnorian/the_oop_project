
using FlockingGSimulator.Domain.Entities;

namespace FlockingSimulator.Domain.Interfaces
{
    // Interface for collision detection between space objects
    public interface ICollisionDetector
    {
        IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2);
    }
}