window.drawBoid = (x, y, rotation) => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.moveTo(x + Math.cos(rotation) * 5, y + Math.sin(rotation) * 5);
    ctx.lineTo(x - 5, y - 5);
    ctx.lineTo(x + 5, y - 5);
    ctx.closePath();
    ctx.fill();
};

window.drawShip = (x, y, rotation) => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "blue";
    ctx.fillRect(x - 10, y - 10, 20, 20);
};

window.drawMissile = (x, y) => {
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "green";
    ctx.fillRect(x - 2, y - 2, 4, 4);
};
