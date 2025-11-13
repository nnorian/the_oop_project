using System.Numerics;
using System.Collections.Generic;
using System.Linq;
using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;
using FlockingSimulator.Domain.Config;

namespace FlockingSimulator.Infrastructure.Behaviors
{
    // Implements the flocking algorithm matching the Python version exactly
    // with separation, alignment, cohesion, ship avoidance, and aggressive behavior
    public class SimpleFlockingBehavior : IFlockingBehavior
    {
        public Vector2 CalculateSteering(Boid boid, IEnumerable<SpaceObject> neighbors)
        {
            var separation = Vector2.Zero;
            var alignment = Vector2.Zero;
            var cohesion = Vector2.Zero;
            int separationTotal = 0;
            int alignmentTotal = 0;
            int cohesionTotal = 0;

            var shipProximitySep = Vector2.Zero;

            foreach (var other in neighbors)
            {
                if (other == boid) continue;

                var distance = Vector2.Distance(boid.Position, other.Position);

                // Separation - avoid crowding (includes all objects except aggressive boids near ship)
                if (distance < BoidConfig.SeparationRadius && distance > 0)
                {
                    // Aggressive boids don't avoid the ship
                    if (!(boid.IsAggressive && other is Ship))
                    {
                        var difference = boid.Position - other.Position;
                        difference = Vector2.Normalize(difference);
                        difference /= distance; // Weight by distance
                        separation += difference;
                        separationTotal++;
                    }
                }

                // Ship proximity separation - non-aggressive boids avoid ship more strongly
                if (other is Ship && distance < BoidConfig.SeparationRadius)
                {
                    if (!boid.IsAggressive)
                    {
                        var difference = boid.Position - other.Position;
                        difference = Vector2.Normalize(difference);
                        difference /= distance;
                        shipProximitySep = (separation + difference) * BoidConfig.ShipPresenceFactor;
                    }
                }

                // Cohesion - steer towards average position of other boids (not ship)
                if (distance < BoidConfig.CohesionRadius && other is Boid)
                {
                    cohesion += other.Position;
                    cohesionTotal++;
                }

                // Alignment - match velocity of nearby boids (not ship)
                if (distance < BoidConfig.PerceptionRadius && other is Boid)
                {
                    alignment += other.Velocity;
                    alignmentTotal++;
                }
            }

            // Average and apply steering for separation
            if (separationTotal > 0)
            {
                separation /= separationTotal;
                separation = SetMagnitude(separation, BoidConfig.MaxSpeed);
                separation -= boid.Velocity;
                separation = LimitMagnitude(separation, BoidConfig.MaxForce);
            }

            // Average and apply steering for alignment
            if (alignmentTotal > 0)
            {
                alignment /= alignmentTotal;
                alignment = SetMagnitude(alignment, BoidConfig.MaxSpeed);
                alignment -= boid.Velocity;
                alignment = LimitMagnitude(alignment, BoidConfig.MaxForce);
            }

            // Average and apply steering for cohesion
            if (cohesionTotal > 0)
            {
                cohesion /= cohesionTotal;
                cohesion -= boid.Position; // Vector pointing to center of mass
                cohesion = SetMagnitude(cohesion, BoidConfig.MaxSpeed);
                cohesion -= boid.Velocity;
                cohesion = LimitMagnitude(cohesion, BoidConfig.MaxForce);
            }

            return separation + alignment + cohesion + shipProximitySep;
        }

        // Helper method to set vector magnitude
        private Vector2 SetMagnitude(Vector2 vector, float magnitude)
        {
            var length = vector.Length();
            if (length == 0) return vector;
            return Vector2.Normalize(vector) * magnitude;
        }

        // Helper method to limit vector magnitude
        private Vector2 LimitMagnitude(Vector2 vector, float maxMagnitude)
        {
            var length = vector.Length();
            if (length > maxMagnitude)
            {
                return Vector2.Normalize(vector) * maxMagnitude;
            }
            return vector;
        }
    }
}
