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
    ballY + height,
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
    radius / 2,
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
    radius / 2,
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
}

export function moveLeftPaddle(upPressed, downPressed, canvas) {
  if (upPressed && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
  } else if (downPressed && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
  }
  return leftPaddleY;
}

export function moveRightPaddle(ballY, canvas) {
  const diff = ballY - (rightPaddleY + paddleHeight / 2);
  if (Math.abs(diff) > paddleDy && Math.random() < 0.8) {
    let direction = 1;
    if (Math.random() < 0.1) {
      direction = -1;
    }

    if (ballY < rightPaddleY + paddleHeight / 2 && rightPaddleY > 0) {
      rightPaddleY -= paddleDy * direction;
    } else if (
      ballY > rightPaddleY + paddleHeight / 2 &&
      rightPaddleY < canvas.height - paddleHeight
    ) {
      rightPaddleY += paddleDy * direction;
    }
  }
  return rightPaddleY;
}

export function updateLeftPaddlePosition(previousCanvasHeight, canvas) {
  const paddlePositionRatioY = isNaN(leftPaddleY / previousCanvasHeight)
    ? 0.5
    : leftPaddleY / previousCanvasHeight;
  leftPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

export function updateRightPaddlePosition(previousCanvasHeight, canvas) {
  const paddlePositionRatioY = isNaN(rightPaddleY / previousCanvasHeight)
    ? 0.5
    : rightPaddleY / previousCanvasHeight;
  rightPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

export function updatePaddleSize(canvas) {
  paddleWidth = canvas.width * 0.015;
  paddleHeight = canvas.height * 0.2;
}

export function updatePaddleSpeed(canvas) {
  paddleDy = canvas.height * 0.015;
}
