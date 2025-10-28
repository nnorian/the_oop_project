// This will use JS Interop to draw on canvas, called from Presentation Layer
using Microsoft.JSInterop;
using FlockingSimulator.Domain.Entities;
using System.Numerics;

namespace FlockingSimulator.Infrastructure.Rendering { 

    // Canvas rendering implementation using JS Interop
    public class CanvasRenderer
    {
        // JS Runtime for invoking JavaScript functions
        private readonly IJSRuntime js;
        // Constructor to initialize the JS Runtime
        public CanvasRenderer(IJSRuntime js) => this.js = js;

        public ValueTask DrawBoid(Boid boid) => js.InvokeVoidAsync("drawBoid", boid.Position.X, boid.Position.Y, boid.Rotation);
        public ValueTask DrawShip(Ship ship) => js.InvokeVoidAsync("drawShip", ship.Position.X, ship.Position.Y, ship.Rotation);
        public ValueTask DrawMissile(Missile missile) => js.InvokeVoidAsync("drawMissile", missile.Position.X, missile.Position.Y);
    }
}
