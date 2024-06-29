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

export function moveRightPaddle(
  upPressedRight,
  downPressedRight,
  canvas,
  gameSocket
) {
  let moved = false;
  if (upPressedRight && rightPaddleY > 0) {
    rightPaddleY -= paddleDy;
    moved = true;
  } else if (downPressedRight && rightPaddleY < canvas.height - paddleHeight) {
    rightPaddleY += paddleDy;
    moved = true;
  }

  if (moved) {
    console.log("rightPaddleY", rightPaddleY);
    sendPaddlePosition(gameSocket, rightPaddleY, "right");
  }
  return rightPaddleY;
}

export function moveLeftPaddle(
  upPressedLeft,
  downPressedLeft,
  canvas,
  gameSocket
) {
  let moved = false;
  if (upPressedLeft && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
    moved = true;
  } else if (downPressedLeft && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
    moved = true;
  }

  if (moved) {
    console.log("leftPaddleY", leftPaddleY);
    sendPaddlePosition(gameSocket, leftPaddleY, "left");
  }
  return leftPaddleY;
}

function sendPaddlePosition(gameSocket, paddleY, rightLeft) {
  const paddlePositionRatioY = paddleY / canvas.height;
  gameSocket.send(
    JSON.stringify({
      type: "update_paddle",
      player_position: rightLeft,
      paddle_position_ratio: paddlePositionRatioY,
    })
  );
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

export function updateLeftPaddlePositionFromRatio(paddlePositionRatioY) {
  leftPaddleY = canvas.height * paddlePositionRatioY;
}

export function updateRightPaddlePositionFromRatio(paddlePositionRatioY) {
  rightPaddleY = canvas.height * paddlePositionRatioY;
}
