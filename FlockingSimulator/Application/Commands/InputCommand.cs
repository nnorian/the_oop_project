// Application/Commands/InputCommand.cs
using FlockingGame.Domain.Entities;

namespace FlockingGame.Application.Commands
{
    // Command interface for handling player input actions
    public interface IInputCommand
    {
        void Execute(Ship playerShip);
    }

    // Command to rotate the ship to the left
    public class RotateLeftCommand : IInputCommand
    {
        public void Execute(Ship playerShip)
        {
            // Rotate the ship by a small angle to the leftq
            playerShip.Rotate(-0.1f);
        }
    }

    // Command to rotate the ship to the right
    public class RotateRightCommand : IInputCommand
    {
        public void Execute(Ship playerShip)
        {
            // Rotate the ship by a small angle to the right
            playerShip.Rotate(0.1f);
        }
    }

    // Command to accelerate the ship forward
    public class AccelerateCommand : IInputCommand
    {
        public void Execute(Ship playerShip)
        {
            // Accelerate the ship in the direction it is facing
            playerShip.Accelerate();
        }
    }

    // Command to fire a missile from the ship
    public class FireMissileCommand : IInputCommand
    {
        // Callback to notify when a missile is fired
        private readonly Action<Missile> _onFire;
        // Constructor accepting a callback action
        public FireMissileCommand(Action<Missile> onFire)
        {
            _onFire = onFire;
        }

        // Execute method to fire a missile
        public void Execute(Ship playerShip)
        {
            // Fire a missile and invoke the callback
            var missile = playerShip.FireMissile();
            _onFire?.Invoke(missile);
        }
    }
}
