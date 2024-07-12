import {
  canvas,
  ctx,
  previousCanvasHeight,
  previousCanvasWidth,
} from "./main.js";
import {
  cpuScore,
  playerScore,
  winningScore,
  incrementCpuScore,
  incrementPlayerScore,
} from "./score.js";

import { gameOver, resetGame } from "./game_control.js";

import {
  paddleWidth,
  paddleHeight,
  leftPaddleY,
  leftMiddlePaddleY,
  rightPaddleY,
  rightMiddlePaddleY,
} from "./paddle.js";

export let ballY;
let ballRadius, ballX, ballDx, ballDy;

export function drawBall() {
  ctx.beginPath();
  ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

export function initializeBallElement() {
  updateBallSize();
  initializeBallPosition();
  initializeBallSpeed();
}

function initializeBallPosition() {
  ballX = canvas.width / 2;
  ballY = canvas.height / 2;
}

function getRandomDirection() {
  return Math.random() < 0.5 ? 1 : -1;
}

function initializeBallSpeed() {
  const angle = Math.random() * 2 * Math.PI;
  ballDx = canvas.width * 0.01 * getRandomDirection();
  ballDy = canvas.height * 0.01 * Math.sin(angle);
}

export function moveBall() {
  if (ballX + ballDx < paddleWidth * 2) {
    if (ballY > leftPaddleY && ballY < leftPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (leftPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else if (
      ballY > leftMiddlePaddleY &&
      ballY < leftMiddlePaddleY + paddleHeight
    ) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (leftMiddlePaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else {
      // Game Over
      incrementCpuScore();
      if (cpuScore >= winningScore) {
        gameOver("Congratulations! Right win!");
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
    } else if (
      ballY > rightMiddlePaddleY &&
      ballY < rightMiddlePaddleY + paddleHeight
    ) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (rightMiddlePaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else {
      // Game Over
      incrementPlayerScore();
      if (playerScore >= winningScore) {
        gameOver("Congratulations! Left win!");
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

export function updateBallElement() {
  updateBallSize();
  updateBallPosition();
  updateBallSpeed();
}

function updateBallPosition() {
  const ballPositionRatioX = isNaN(ballX / previousCanvasWidth)
    ? 0.5
    : ballX / previousCanvasWidth;
  const ballPositionRatioY = isNaN(ballY / previousCanvasHeight)
    ? 0.5
    : ballY / previousCanvasHeight;

  ballX = canvas.width * ballPositionRatioX;
  ballY = canvas.height * ballPositionRatioY;
}

function updateBallSize() {
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05;
}

function updateBallSpeed() {
  ballDx = (ballDx * canvas.width) / previousCanvasWidth;
  ballDy = (ballDy * canvas.height) / previousCanvasHeight;
}
