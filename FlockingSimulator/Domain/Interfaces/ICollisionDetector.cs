using FlockingSimulator.Domain.Entities;
using System.Collections.Generic;

namespace FlockingSimulator.Domain.Interfaces
{
    public interface ICollisionDetector
    {
        IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2);
    }
}
