using FlockingGame.Domain.Entities;

namespace FlockingGame.Domain.Interfaces
{
    // this interface defines the contract for collision detection between space objects
    public interface ICollisionDetector
    {
        // method to detect collisions between two sets of space objects
        public interface ICollisionDetector
        {
            IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2);
        }
    }
}