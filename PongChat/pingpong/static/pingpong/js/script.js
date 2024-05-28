const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
let ballRadius, x, y, dx, dy;
let paddleWidth, paddleHeight, paddleY, paddleDy;
let previousCanvasWidth, previousCanvasHeight;

function initialize() {
  updateCanvasSize();

  updateBallSize();
  updateBallPosition();
  updateBallSpeed();

  updatePaddleSize();
  updatePaddlePosition();
  updatePaddleSpeed();
}

function updateCanvasSize() {
  // キャンバスのサイズをウィンドウサイズに合わせる
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;
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
}

function updateBallPosition() {
  const ballPositionRatioX = isNaN(x / previousCanvasWidth)
    ? 0.5
    : x / previousCanvasWidth;
  const ballPositionRatioY = isNaN(y / previousCanvasHeight)
    ? 0.5
    : y / previousCanvasHeight;

  x = canvas.width * ballPositionRatioX;
  y = canvas.height * ballPositionRatioY;
}

function updateBallSize() {
  // ボールの半径をキャンバスサイズの一定の割合として設定
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05; // 例えばキャンバスの幅または高さの5%
}

function updateBallSpeed() {
  dx = canvas.width * 0.01; // 例えばキャンバスの幅の1%
  dy = canvas.height * 0.01; // 例えばキャンバスの高さの1%
}

function updatePaddlePosition() {
  const paddlePositionRatioY = isNaN(paddleY / previousCanvasHeight)
    ? 0.5
    : paddleY / previousCanvasHeight;
  paddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

function updatePaddleSize() {
  paddleWidth = canvas.width * 0.01; // 例えばキャンバスの幅の1%
  paddleHeight = canvas.height * 0.2; // 例えばキャンバスの高さの10%
}

function updatePaddleSpeed() {
  paddleDy = dy * 1.5; // 例えばキャンバスの高さの1%
}

function drawBall() {
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function drawCenterLine() {
  const lineWidth = canvas.width * 0.01; // 例えばキャンバスの幅の1%
  ctx.lineWidth = lineWidth;
  ctx.beginPath();
  ctx.setLineDash([lineWidth * 2, lineWidth]);
  ctx.moveTo(canvas.width / 2, 0);
  ctx.lineTo(canvas.width / 2, canvas.height);
  ctx.strokeStyle = "#0095DD";
  ctx.stroke();
  ctx.setLineDash([]); // reset
  ctx.closePath();
}

function drawPaddle() {
  ctx.beginPath();
  ctx.rect(paddleWidth, paddleY, paddleWidth, paddleHeight);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
  drawBall();
  drawCenterLine();
  drawPaddle();

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

function onResize() {
  previousCanvasWidth = canvas.width;
  previousCanvasHeight = canvas.height;

  updateCanvasSize();

  updateBallPosition();
  updateBallSize();
  updateBallSpeed();

  updatePaddlePosition();
  updatePaddleSize();
  updatePaddleSpeed();
}

// 初期化
initialize();

// リサイズイベントに応じてキャンバスをリサイズ
window.addEventListener("resize", onResize, false);

requestAnimationFrame(draw);
