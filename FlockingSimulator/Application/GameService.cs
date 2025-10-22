using FLockingGame.Domain.Entities;
using FLockingGame.Domain.Interfaces;
using System.Numerics;

namespace FlockingGame.Application
{
    public class GameService
    {
        private readonly ICollisionDetector collisionDetector;
        private readonly IMissileFactory missileFactory;

        public List<Boid> Flock { get; private set; } = new();
        public Ship PlayerShip { get; private set; } = new();
        public List<Missile> Missiles { get; private set; } = new();
        public int Lives { get; private set; } = 3;
        public int Score { get; private set; } = 0;

        public GameService(ICollisionDetector collisionDetector, IMissileFactory missileFactory)
        {
            this.collisionDetector = collisionDetector;
            this.missileFactory = missileFactory;
        }
        public void Initialize(IEnumerable<Boid> initial Flock)
        {
            Flock.AddRange(initial Flock);
        }

        public void FireMissile()
        {
            var missile = missileFactory.CreateMissile(PlayerShip.Position, PlayerShip.Rotation);
            Missiles.Add(missile);
        }

        public void Update()
        {
            foreach (var boid in Flock)
                boid.Position += boid.CalculateFlocking(Flock.Apppend(PlayerShip)) * BoidConfig.MaxSpeed;

            foreach (var missile in Missiles)
            {
                missile.Position += missile.Velocity * PhysicsConfig.DeltaTime;
                missile.LifeTime -= PhysicsConfig.DeltaTime;
            }

            Missiles.RemoveAll(m => !m.IsActive || m.LifeTime <= 0);

            //detect collisions between missiles and boids
            var collisions = collisionDetector.Detect(Flock.Cast<SpaceObject>(), Missiles.Cast<SpaceObject>());
            HandleCollisions(collision);
        }

        private void HandleCollisions(IEnumerable<(SpaceObject, SpaceObject)> collisions)
        {
            foreach (var(a.b) in collisions)
            {
                if (a is Boid boid)
                {
                    Flock.Remove(boid);
                    Score += 10;
                }
                if (b is Missile missile)
                {
                    missile.IsActive = false;
                }
            }
        }
    }
}