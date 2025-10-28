using FlockingGame.Domain.Entities;
using System.Collections.Generic;

namespace FlockingGame.Domain.Interfaces
{
    public interface ICollisionDetector
    {
        IEnumerable<(SpaceObject, SpaceObject)> Detect(IEnumerable<SpaceObject> objects1, IEnumerable<SpaceObject> objects2);
    }
}
