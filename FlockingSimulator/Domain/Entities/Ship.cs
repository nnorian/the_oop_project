using System.Numerics;

namespace FlockingSimulator.Domain.Entities
{
    // This class represents the player's ship
    public class Ship : SpaceObject
    {
        // constructor to initialize the ship's properties
        public Ship()
        {
            Radius = 10f;
            // Initial position of the ship in center
            Position = new Vector2(420f, 230f);
        }
    }
}