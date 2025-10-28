using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;
using System.Collections.Generic;
using System.Numerics;
using System.Linq;

namespace FlockingSimulator.Infrastructure.Systems
{
    public class CollisionSystem : ICollisionDetector
    {
        public IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2)
        {
            var collisions = new List<(SpaceObject, SpaceObject)>();
            var list1 = objects1.ToList();
            var list2 = objects2.ToList();

            foreach (var a in list1)
                foreach (var b in list2)
                {
                    if (a == null || b == null || ReferenceEquals(a, b)) continue;
                    var dist = Vector2.Distance(a.Position, b.Position);
                    if (dist < (a.Radius + b.Radius))
                        collisions.Add((a, b));
                }

            return collisions;
        }
    }
}
