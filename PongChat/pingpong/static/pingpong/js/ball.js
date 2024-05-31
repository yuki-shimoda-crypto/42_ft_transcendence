import {
  cpuScore,
  playerScore,
  winningScore,
  gameOver,
  resetGame,
  incrementCpuScore,
  incrementPlayerScore,
} from "./script.js";

import {
  paddleWidth,
  paddleHeight,
  leftPaddleY,
  rightPaddleY,
} from "./paddle.js";

export let ballY;
let ballRadius, ballX, ballDx, ballDy;

export function drawBall(ctx) {
  ctx.beginPath();
  ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

export function initializeBallPosition(canvas) {
  ballX = canvas.width / 2;
  ballY = canvas.height / 2;
}

function getRandomDirection() {
  return Math.random() < 0.5 ? 1 : -1;
}

export function initializeBallSpeed(canvas) {
  const angle = Math.random() * 2 * Math.PI;
  ballDx = canvas.width * 0.01 * getRandomDirection();
  ballDy = canvas.height * 0.01 * Math.sin(angle);
}

export function moveBall(canvas) {
  if (ballX + ballDx < paddleWidth * 2) {
    if (ballY > leftPaddleY && ballY < leftPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (leftPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else {
      // Game Over
      incrementCpuScore();
      if (cpuScore >= winningScore) {
        gameOver("CPU wins! Better luck next time.");
      } else {
        resetGame();
      }
    }
  } else if (ballX + ballDx > canvas.width - paddleWidth * 2) {
    if (ballY > rightPaddleY && ballY < rightPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (rightPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else {
      // Game Over
      incrementPlayerScore();
      if (playerScore >= winningScore) {
        gameOver("Congratulations! You win!");
      } else {
        resetGame();
      }
    }
  }

  if (
    ballY + ballDy > canvas.height - ballRadius ||
    ballY + ballDy < ballRadius
  ) {
    ballDy = -ballDy;
  }

  ballX += ballDx;
  ballY += ballDy;
}

export function updateBallPosition(
  canvas,
  previousCanvasWidth,
  previousCanvasHeight,
) {
  const ballPositionRatioX = isNaN(ballX / previousCanvasWidth)
    ? 0.5
    : ballX / previousCanvasWidth;
  const ballPositionRatioY = isNaN(ballY / previousCanvasHeight)
    ? 0.5
    : ballY / previousCanvasHeight;

  ballX = canvas.width * ballPositionRatioX;
  ballY = canvas.height * ballPositionRatioY;
}

export function updateBallSize(canvas) {
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05;
}

export function updateBallSpeed(canvas) {
  ballDx = canvas.width * 0.01;
  ballDy = canvas.height * 0.01;
}
