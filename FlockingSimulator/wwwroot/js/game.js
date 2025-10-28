window.game = (function () {
    let ctx = null;
    let w = 0, h = 0;

    function initCanvas(id, width, height) {
        const canvas = document.getElementById(id);
        if (!canvas) return;
        w = width; h = height;
        ctx = canvas.getContext("2d");
        // set transform center if needed
    }

    function clearCanvas() {
        if (!ctx) return;
        ctx.clearRect(0, 0, w, h);
    }

    function drawBoid(x, y, rotation, aggressive) {
        if (!ctx) return;
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);
        ctx.beginPath();
        // triangle pointing up (local coordinates)
        ctx.moveTo(8, 0);
        ctx.lineTo(-6, -5);
        ctx.lineTo(-6, 5);
        ctx.closePath();
        ctx.fillStyle = aggressive ? "tomato" : "red";
        ctx.fill();
        ctx.restore();
    }

    function drawShip(x, y, rotation) {
        if (!ctx) return;
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotation);
        ctx.fillStyle = "blue";
        ctx.fillRect(-12, -8, 24, 16);
        ctx.restore();
    }

    function drawMissile(x, y) {
        if (!ctx) return;
        ctx.save();
        ctx.translate(x, y);
        ctx.fillStyle = "green";
        ctx.fillRect(-2, -2, 4, 4);
        ctx.restore();
    }

    return {
        initCanvas,
        clearCanvas,
        drawBoid,
        drawShip,
        drawMissile
    };
})();
