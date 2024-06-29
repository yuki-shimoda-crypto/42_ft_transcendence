import { canvas, previousCanvasHeight } from "./main.js";
export let paddleWidth, paddleHeight, leftPaddleY, rightPaddleY;
let paddleDy;

function drawRoundedRect(ctx, ballX, ballY, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(ballX + radius, ballY);
  ctx.lineTo(ballX + width - radius, ballY);
  ctx.quadraticCurveTo(ballX + width, ballY, ballX + width, ballY + radius);
  ctx.lineTo(ballX + width, ballY + height - radius);
  ctx.quadraticCurveTo(
    ballX + width,
    ballY + height,
    ballX + width - radius,
    ballY + height
  );
  ctx.lineTo(ballX + radius, ballY + height);
  ctx.quadraticCurveTo(ballX, ballY + height, ballX, ballY + height - radius);
  ctx.lineTo(ballX, ballY + radius);
  ctx.quadraticCurveTo(ballX, ballY, ballX + radius, ballY);
  ctx.closePath();
}

export function drawLeftPaddle(ctx) {
  const radius = paddleWidth;
  drawRoundedRect(
    ctx,
    paddleWidth,
    leftPaddleY,
    paddleWidth,
    paddleHeight,
    radius / 2
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
}

export function drawRightPaddle(ctx, canvas) {
  const radius = paddleWidth;
  drawRoundedRect(
    ctx,
    canvas.width - paddleWidth * 2,
    rightPaddleY,
    paddleWidth,
    paddleHeight,
    radius / 2
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
}

export function moveRightPaddle(upPressedRight, downPressedRight, canvas) {
  if (upPressedRight && rightPaddleY > 0) {
    rightPaddleY -= paddleDy;
  } else if (downPressedRight && rightPaddleY < canvas.height - paddleHeight) {
    rightPaddleY += paddleDy;
  }
  return rightPaddleY;
}

export function moveLeftPaddle(upPressedLeft, downPressedLeft, canvas) {
  if (upPressedLeft && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
  } else if (downPressedLeft && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
  }
  return leftPaddleY;
}

export function updatePaddleElement() {
  updatePaddleSize(canvas);
  updateLeftPaddlePosition(previousCanvasHeight, canvas);
  updateRightPaddlePosition(previousCanvasHeight, canvas);
  updatePaddleSpeed(canvas);
}

export function updateLeftPaddlePosition(previousCanvasHeight, canvas) {
  const paddlePositionRatioY = isNaN(leftPaddleY / previousCanvasHeight)
    ? 0.5
    : leftPaddleY / previousCanvasHeight;
  leftPaddleY = canvas.height * paddlePositionRatioY;
}

export function updateRightPaddlePosition(previousCanvasHeight, canvas) {
  const paddlePositionRatioY = isNaN(rightPaddleY / previousCanvasHeight)
    ? 0.5
    : rightPaddleY / previousCanvasHeight;
  rightPaddleY = canvas.height * paddlePositionRatioY;
}

export function updatePaddleSize(canvas) {
  paddleWidth = canvas.width * 0.015;
  paddleHeight = canvas.height * 0.2;
}

export function updatePaddleSpeed(canvas) {
  paddleDy = canvas.height * 0.015;
}
