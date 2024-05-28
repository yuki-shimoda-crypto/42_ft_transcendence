const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
let ballRadius;
let x, y, dx, dy;

function initialize() {
  resizeCanvas();
  initializeBall();
}

function initializeBall() {
  x = canvas.width / 2;
  y = canvas.height / 2;
}

function resizeCanvas() {
  // get the current position of the ball
  const ballPositionRatioX = isNaN(x / canvas.width) ? 0.5 : x / canvas.width;
  const ballPositionRatioY = isNaN(y / canvas.height) ? 0.5 : y / canvas.height;

  // get the current size of the window
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;

  // set aspect ratio
  const aspectRatio = 16 / 9; // 16:9

  if (windowWidth / windowHeight > aspectRatio) {
    // ウィンドウの幅が高さよりも大きい場合
    // キャンバスの幅をウィンドウの高さに16:9のアスペクト比を適用して設定
    canvas.width = windowHeight * aspectRatio;
    canvas.height = windowHeight;
  } else {
    canvas.width = windowWidth;
    canvas.height = windowWidth / aspectRatio;
  }

  x = canvas.width * ballPositionRatioX;
  y = canvas.height * ballPositionRatioY;

  updateBallSize();
  updateBallSpeed();
}

function updateBallSize() {
  // ボールの半径をキャンバスサイズの一定の割合として設定
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05; // 例えばキャンバスの幅または高さの5%
}

function updateBallSpeed() {
  dx = canvas.width * 0.01; // 例えばキャンバスの幅の1%
  dy = canvas.height * 0.01; // 例えばキャンバスの高さの1%
}

function drawBall() {
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
  drawBall();

  if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
    dx = -dx;
  }
  if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
    dy = -dy;
  }

  x += dx;
  y += dy;
  requestAnimationFrame(draw);
}

// 初期化
initialize();

// リサイズイベントに応じてキャンバスをリサイズ
window.addEventListener("resize", resizeCanvas, false);

requestAnimationFrame(draw);