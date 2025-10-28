using FlockingSimulator.Application;
using FlockingSimulator.Domain.Interfaces;
using FlockingSimulator.Infrastructure.Factories;
using FlockingSimulator.Infrastructure.Systems;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// Domain interfaces and infrastructure
builder.Services.AddSingleton<IFlockingBehavior, SimpleFlockingBehavior>();
builder.Services.AddSingleton<ICollisionDetector, CollisionSystem>();
builder.Services.AddSingleton<IMissileFactory, MissileFactory>();

// Factories & services
builder.Services.AddSingleton<BoidFactory>();
builder.Services.AddSingleton<GameService>();

// CanvasRenderer uses IJSRuntime; register in components at runtime via injection (we used manual instantiation in component).

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}
app.UseStaticFiles();
app.UseRouting();

app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

// Initialize the game with a flock after build so services are available
using (var scope = app.Services.CreateScope())
{
    var boidFactory = scope.ServiceProvider.GetRequiredService<BoidFactory>();
    var gameService = scope.ServiceProvider.GetRequiredService<GameService>();

    var flock = Enumerable.Range(0, BoidConfig.FlockCount).Select(_ => boidFactory.CreateRandomBoid()).ToList();
    gameService.Initialize(flock);

    // Optionally place the ship at center
    gameService.PlayerShip.Position = new System.Numerics.Vector2(PhysicsConfig.CanvasWidth / 2, PhysicsConfig.CanvasHeight / 2);
    gameService.PlayerShip.Rotation = 0f;
}

app.Run();