const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
let ballRadius, x, y, dx, dy;
let paddleWidth, paddleHeight, leftPaddleY, rightPaddleY, paddleDy;
let previousCanvasWidth, previousCanvasHeight;
let upPressed = false, downPressed = false;

function initialize() {
  updateCanvasSize();

  updateBallSize();
  updateBallPosition();
  updateBallSpeed();

  updatePaddleSize();
  updateLeftPaddlePosition();
  updateRightPaddlePosition();
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

function updateLeftPaddlePosition() {
  const paddlePositionRatioY = isNaN(leftPaddleY / previousCanvasHeight)
    ? 0.5
    : leftPaddleY / previousCanvasHeight;
  leftPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

function updateRightPaddlePosition() {
  const paddlePositionRatioY = isNaN(rightPaddleY / previousCanvasHeight)
    ? 0.5
    : rightPaddleY / previousCanvasHeight;
  rightPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

function updatePaddleSize() {
  paddleWidth = canvas.width * 0.01; // 例えばキャンバスの幅の1%
  paddleHeight = canvas.height * 0.2; // 例えばキャンバスの高さの10%
}

function updatePaddleSpeed() {
  paddleDy = canvas.height * 0.015; // 例えばキャンバスの高さの1%
}

function keyDownHandler(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressed = true;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressed = true;
  }
}

function keyUpHandler(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressed = false;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressed = false;
  }
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

function drawLeftPaddle() {
  ctx.beginPath();
  ctx.rect(paddleWidth, leftPaddleY, paddleWidth, paddleHeight);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function drawRightPaddle() {
  ctx.beginPath();
  ctx.rect((canvas.width - (paddleWidth * 2)), rightPaddleY, paddleWidth, paddleHeight);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
  drawBall();
  drawCenterLine();
  drawLeftPaddle();
  drawRightPaddle();

  if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
    dx = -dx;
  }
  if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
    dy = -dy;
  }

  x += dx;
  y += dy;

  if (upPressed && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
  } else if (downPressed && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
  }

  requestAnimationFrame(draw);
}

function onResize() {
  previousCanvasWidth = canvas.width;
  previousCanvasHeight = canvas.height;

  updateCanvasSize();

  updateBallSize();
  updateBallPosition();
  updateBallSpeed();

  updatePaddleSize();
  updateLeftPaddlePosition();
  updateRightPaddlePosition();
  updatePaddleSpeed();
}

// 初期化
initialize();

// リサイズイベントに応じてキャンバスをリサイズ
window.addEventListener("resize", onResize, false);

// キーボードイベント
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);


requestAnimationFrame(draw);
