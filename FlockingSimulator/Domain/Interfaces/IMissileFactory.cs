using FlockingGame.Domain.Entities;

namespace FlockingGame.Domain.Interfaces
{
    // this interface defines a factory for creating Missile instances
    public interface IMissileFactory
    {
        // method to create a missile at a given position and rotation
        Missile CreateMissile(Vector2 position, float rotation);
    }
}
