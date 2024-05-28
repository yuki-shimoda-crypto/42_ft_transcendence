const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
let ballRadius, x, y, dx, dy;
let paddleWidth, paddleHeight, leftPaddleY, rightPaddleY, paddleDy;
let previousCanvasWidth, previousCanvasHeight;
let upPressed = false,
  downPressed = false;

function initialize() {
  updateCanvasSize();

  updateBallSize();
  initializeBallPosition();
  initializeBallSpeed();

  updatePaddleSize();
  updateLeftPaddlePosition();
  updateRightPaddlePosition();
  updatePaddleSpeed();
}

function initializeBallPosition() {
  x = canvas.width / 2;
  y = canvas.height / 2;
}

function getRandomDirection() {
  return Math.random() < 0.5 ? 1 : -1;
}

function initializeBallSpeed() {
  const angle = Math.random() * 2 * Math.PI;
  dx = canvas.width * 0.01 * getRandomDirection();
  dy = canvas.height * 0.01 * Math.sin(angle);
}

function updateCanvasSize() {
  // adjust canvas size
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;
  const aspectRatio = 16 / 9; // 16:9

  if (windowWidth / windowHeight > aspectRatio) {
    // if window is wider than 16:9
    // adjust canvas width to window height * 16:9
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
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05;
}

function updateBallSpeed() {
  dx = canvas.width * 0.01;
  dy = canvas.height * 0.01;
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
  paddleWidth = canvas.width * 0.01;
  paddleHeight = canvas.height * 0.2;
}

function updatePaddleSpeed() {
  paddleDy = canvas.height * 0.015;
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
  const lineWidth = canvas.width * 0.01;
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
  ctx.rect(
    canvas.width - paddleWidth * 2,
    rightPaddleY,
    paddleWidth,
    paddleHeight,
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function moveBall() {
  if (x + dx < paddleWidth * 2) {
    if (y > leftPaddleY && y < leftPaddleY + paddleHeight) {
      dx = -dx;
    } else {
      // Game Over
      initialize();
    }
  } else if (x + dx > canvas.width - paddleWidth * 2) {
    if (y > rightPaddleY && y < rightPaddleY + paddleHeight) {
      dx = -dx;
    } else {
      // Game Over
      initialize();
    }
  }

  if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
    dy = -dy;
  }

  x += dx;
  y += dy;
}

function moveLeftPaddle() {
  if (upPressed && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
  } else if (downPressed && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
  }
}

function moveRightPaddle() {
  const diff = y - (rightPaddleY + paddleHeight / 2);
  if (Math.abs(diff) > paddleDy && Math.random() < 0.8) {
    let direction = 1;
    if (Math.random() < 0.1) {
      direction = -1;
    }

    if (y < rightPaddleY + paddleHeight / 2 && rightPaddleY > 0) {
      rightPaddleY -= paddleDy * direction;
    } else if (
      y > rightPaddleY + paddleHeight / 2 &&
      rightPaddleY < canvas.height - paddleHeight
    ) {
      rightPaddleY += paddleDy * direction;
    }
  }
}

function draw() {
  clearCanvas();

  // draw objects
  drawBall();
  drawCenterLine();
  drawLeftPaddle();
  drawRightPaddle();

  // move objects
  moveBall();
  moveLeftPaddle();
  moveRightPaddle();

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

initialize();

// resize event
window.addEventListener("resize", onResize, false);

// keybord event
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

requestAnimationFrame(draw);
