import {
  canvas,
  ctx,
  previousCanvasHeight,
  previousCanvasWidth,
} from "./main.js";
import { incrementRightScore, incrementLeftScore } from "./score.js";

import {
  paddleWidth,
  paddleHeight,
  leftPaddleY,
  rightPaddleY,
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

function initializeBallSpeed() {
  ballDx = canvas.width * 0.01;
  ballDy = canvas.width * 0.0005;
}

export function moveBall(gameSocket) {
  if (ballX + ballDx < paddleWidth * 2) {
    if (ballY > leftPaddleY && ballY < leftPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (leftPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
      sendBallPosition(gameSocket);
    } else {
      // Game Over
      incrementRightScore(gameSocket);
    }
  } else if (ballX + ballDx > canvas.width - paddleWidth * 2) {
    if (ballY > rightPaddleY && ballY < rightPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (rightPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
      sendBallPosition(gameSocket);
    } else {
      // Game Over
      incrementLeftScore(gameSocket);
    }
  }

  if (
    ballY + ballDy > canvas.height - ballRadius ||
    ballY + ballDy < ballRadius
  ) {
    ballDy = -ballDy;
    sendBallPosition(gameSocket);
  }

  ballX += ballDx;
  ballY += ballDy;

  if (Math.random() < 0.05) {
    sendBallPosition(gameSocket);
  }
}

function sendBallPosition(gameSocket) {
  gameSocket.send(
    JSON.stringify({
      type: "update_ball",
      ball_position_ratio_x: ballX / canvas.width,
      ball_position_ratio_y: ballY / canvas.height,
      ball_position_ratio_dx: ballDx / canvas.width,
      ball_position_ratio_dy: ballDy / canvas.height,
    }),
  );
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

export function updateBallFromRemote(data) {
  ballX = data.ball_position_ratio_x * canvas.width;
  ballY = data.ball_position_ratio_y * canvas.height;
  ballDx = data.ball_position_ratio_dx * canvas.width;
  ballDy = data.ball_position_ratio_dy * canvas.height;
}
