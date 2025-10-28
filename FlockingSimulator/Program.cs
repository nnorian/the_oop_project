using FlockingSimulator.Application;
using FlockingSimulator.Domain.Interfaces;
using FlockingSimulator.Infrastructure.Factories;
using FlockingSimulator.Infrastructure.Systems;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();

// DI
builder.Services.AddSingleton<ICollisionDetector, CollisionSystem>();
builder.Services.AddSingleton<IMissileFactory, MissileFactory>();
builder.Services.AddSingleton<GameService>();
builder.Services.AddSingleton<BoidFactory>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}
app.UseStaticFiles();
app.UseRouting();
app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
