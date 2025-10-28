using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;

namespace FlockingSimulator.Infrastructure.Systems
{
    // this class implements collision detection between space objects
    public class CollisionSystem : ICollisionDetector
    {
        // method to detect collisions between two sets of space objects
        public IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2)
        {
            // simple circle-based collision detection
            var collisions = new List<(SpaceObject, SpaceObject)>();
            // check each object in the first set against each object in the second set
            foreach (var a in objects1)
                foreach (var b in objects2)
                    // avoid self-collision and check distance
                    if (a != b && Vector2.Distance(a.Position, b.Position) < a.Radius + b.Radius)
                        collisions.Add((a, b));
            return collisions;
        }
    }
}
