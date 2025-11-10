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

        // Clear the canvas
        public ValueTask Clear() => js.InvokeVoidAsync("game.clearCanvas");

        // Draw a boid at the given position with rotation and aggression state
        public ValueTask DrawBoid(float x, float y, float rotation, bool isAggressive)
            => js.InvokeVoidAsync("game.drawBoid", x, y, rotation, isAggressive);

        // Draw the ship at the given position with rotation
        public ValueTask DrawShip(float x, float y, float rotation)
            => js.InvokeVoidAsync("game.drawShip", x, y, rotation);

        // Draw a missile at the given position
        public ValueTask DrawMissile(float x, float y)
            => js.InvokeVoidAsync("game.drawMissile", x, y);
    }
}
