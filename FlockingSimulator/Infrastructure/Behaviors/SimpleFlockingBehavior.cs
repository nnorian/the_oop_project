using System.Numerics;
using System.Collections.Generic;
using System.Linq;
using FlockingSimulator.Domain.Entities;
using FlockingSimulator.Domain.Interfaces;

namespace FlockingSimulator.Infrastructure.Behaviors
{
    // Implements the classic flocking algorithm with three rules:
    // 1. Separation - avoid crowding neighbors
    // 2. Alignment - steer towards average heading of neighbors
    // 3. Cohesion - steer towards average position of neighbors
    public class SimpleFlockingBehavior : IFlockingBehavior
    {
        // Perception radius for detecting neighbors
        private const float PerceptionRadius = 50f;

        // Weights for each flocking rule
        private const float SeparationWeight = 1.5f;
        private const float AlignmentWeight = 1.0f;
        private const float CohesionWeight = 1.0f;

        // Desired separation distance from neighbors
        private const float DesiredSeparation = 25f;

        public Vector2 CalculateSteering(Boid boid, IEnumerable<SpaceObject> neighbors)
        {
            var separation = CalculateSeparation(boid, neighbors);
            var alignment = CalculateAlignment(boid, neighbors);
            var cohesion = CalculateCohesion(boid, neighbors);

            // Combine the three steering forces with weights
            var steering = separation * SeparationWeight +
                          alignment * AlignmentWeight +
                          cohesion * CohesionWeight;

            return steering;
        }

        // Separation: steer to avoid crowding local neighbors
        private Vector2 CalculateSeparation(Boid boid, IEnumerable<SpaceObject> neighbors)
        {
            var steer = Vector2.Zero;
            int count = 0;

            foreach (var other in neighbors)
            {
                // Don't compare with self
                if (other == boid) continue;

                var distance = Vector2.Distance(boid.Position, other.Position);

                // If too close, steer away
                if (distance > 0 && distance < DesiredSeparation)
                {
                    var diff = boid.Position - other.Position;
                    diff = Vector2.Normalize(diff);
                    diff /= distance; // Weight by distance (closer = stronger push)
                    steer += diff;
                    count++;
                }
            }

            // Average the steering force
            if (count > 0)
            {
                steer /= count;
            }

            return steer;
        }

        // Alignment: steer towards the average heading of local neighbors
        private Vector2 CalculateAlignment(Boid boid, IEnumerable<SpaceObject> neighbors)
        {
            var avgVelocity = Vector2.Zero;
            int count = 0;

            foreach (var other in neighbors)
            {
                // Don't compare with self
                if (other == boid) continue;

                var distance = Vector2.Distance(boid.Position, other.Position);

                if (distance > 0 && distance < PerceptionRadius)
                {
                    avgVelocity += other.Velocity;
                    count++;
                }
            }

            if (count > 0)
            {
                avgVelocity /= count;
                // Steering = desired - current velocity
                var steer = avgVelocity - boid.Velocity;
                return steer;
            }

            return Vector2.Zero;
        }

        // Cohesion: steer to move toward the average position of local neighbors
        private Vector2 CalculateCohesion(Boid boid, IEnumerable<SpaceObject> neighbors)
        {
            var centerOfMass = Vector2.Zero;
            int count = 0;

            foreach (var other in neighbors)
            {
                // Don't compare with self, and only look at other boids
                if (other == boid || other is not Boid) continue;

                var distance = Vector2.Distance(boid.Position, other.Position);

                if (distance > 0 && distance < PerceptionRadius)
                {
                    centerOfMass += other.Position;
                    count++;
                }
            }

            if (count > 0)
            {
                centerOfMass /= count;
                // Steer towards that location
                var desired = centerOfMass - boid.Position;
                return desired;
            }

            return Vector2.Zero;
        }
    }
}
