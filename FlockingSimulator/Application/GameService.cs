using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;
using FlockingSimulator.Domain.Config;
using System.Numerics;
using System.Collections.Generic;
using System.Linq;

namespace FlockingSimulator.Application
{
    public class GameService
    {
        private readonly ICollisionDetector _collisionDetector;
        private readonly IMissileFactory _missileFactory;

        public List<Boid> Flock { get; private set; } = new();
        public Ship PlayerShip { get; private set; } = new();
        public List<Missile> Missiles { get; private set; } = new();
        public int Lives { get; private set; } = 3;
        public int Score { get; private set; } = 0;

        public GameService(ICollisionDetector collisionDetector, IMissileFactory missileFactory)
        {
            _collisionDetector = collisionDetector;
            _missileFactory = missileFactory;
        }

        public void Initialize(IEnumerable<Boid> initialFlock)
        {
            Flock.Clear();
            Flock.AddRange(initialFlock);
        }

        public void FireMissile()
        {
            var missile = _missileFactory.CreateMissile(PlayerShip.Position, PlayerShip.Rotation);
            Missiles.Add(missile);
        }

        public void Update()
        {
            // Update Boids
            var allSpace = Flock.Cast<SpaceObject>().Append(PlayerShip).ToList();
            foreach (var boid in Flock.ToList())
            {
                var steering = boid.CalculateFlocking(allSpace);
                // steering is a desired velocity vector; clamp and integrate
                if (steering != Vector2.Zero)
                {
                    var desired = Vector2.Normalize(steering) * BoidConfig.MaxSpeed;
                    var steer = desired - boid.Velocity;
                    // clamp steer
                    if (steer.Length() > BoidConfig.MaxForce)
                        steer = Vector2.Normalize(steer) * BoidConfig.MaxForce;
                    boid.Velocity += steer * PhysicsConfig.DeltaTime;
                }

                // clamp speed
                if (boid.Velocity.Length() > BoidConfig.MaxSpeed)
                    boid.Velocity = Vector2.Normalize(boid.Velocity) * BoidConfig.MaxSpeed;

                boid.Position += boid.Velocity * PhysicsConfig.DeltaTime;

                // wrap around screen edges
                if (boid.Position.X < 0) boid.Position = new Vector2(PhysicsConfig.CanvasWidth, boid.Position.Y);
                if (boid.Position.X > PhysicsConfig.CanvasWidth) boid.Position = new Vector2(0, boid.Position.Y);
                if (boid.Position.Y < 0) boid.Position = new Vector2(boid.Position.X, PhysicsConfig.CanvasHeight);
                if (boid.Position.Y > PhysicsConfig.CanvasHeight) boid.Position = new Vector2(boid.Position.X, 0);
            }

            // Update Player Ship
            PlayerShip.Position += PlayerShip.Velocity * PhysicsConfig.DeltaTime;

            // Apply velocity damping (friction) to ship
            PlayerShip.Velocity *= 0.98f;

            // Wrap ship around screen edges
            if (PlayerShip.Position.X < 0) PlayerShip.Position = new Vector2(PhysicsConfig.CanvasWidth, PlayerShip.Position.Y);
            if (PlayerShip.Position.X > PhysicsConfig.CanvasWidth) PlayerShip.Position = new Vector2(0, PlayerShip.Position.Y);
            if (PlayerShip.Position.Y < 0) PlayerShip.Position = new Vector2(PlayerShip.Position.X, PhysicsConfig.CanvasHeight);
            if (PlayerShip.Position.Y > PhysicsConfig.CanvasHeight) PlayerShip.Position = new Vector2(PlayerShip.Position.X, 0);

            // Update Missiles
            foreach (var missile in Missiles)
            {
                missile.Position += missile.Velocity * PhysicsConfig.DeltaTime;
                missile.LifeTime -= PhysicsConfig.DeltaTime;
            }

            Missiles.RemoveAll(m => !m.IsActive || m.LifeTime <= 0);

            // Detect collisions (boids vs missiles)
            var collisions = _collisionDetector.Detect(Flock.Cast<SpaceObject>(), Missiles.Cast<SpaceObject>());
            HandleCollisions(collisions);
        }

        private void HandleCollisions(IEnumerable<(SpaceObject, SpaceObject)> collisions)
        {
            foreach (var (a, b) in collisions)
            {
                if (a is Boid boid)
                {
                    Flock.Remove(boid);
                    Score += 10;
                }
                if (b is Boid boid2)
                {
                    Flock.Remove(boid2);
                    Score += 10;
                }

                if (a is Missile missileA) missileA.IsActive = false;
                if (b is Missile missileB) missileB.IsActive = false;
            }
        }
    }
}
