import {
  keyDownHandler,
  keyUpHandler,
  upPressed,
  downPressed,
} from "./key_handle.js";
import {
  drawLeftPaddle,
  drawRightPaddle,
  moveLeftPaddle,
  moveRightPaddle,
  updateLeftPaddlePosition,
  updatePaddleSize,
  updatePaddleSpeed,
  updateRightPaddlePosition,
  paddleWidth,
  paddleHeight,
  leftPaddleY,
  rightPaddleY,
} from "./paddle.js";

// デュース機能を追加する
//　点数のプログレスバーを追加する
// プレイヤー名を入力して、それを表示する
// 勝利者を表示する

// 最初の画面を作成する
// プレイヤー名を入力するフォームを作成する
// プレイヤー名を入力して、それを表示する
// スタートボタンを作成する
// スタートボタンを押すと、ゲームが始まる

const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
let ballRadius, ballX, ballY, ballDx, ballDy;
let previousCanvasWidth, previousCanvasHeight;

// Score
let playerScore = 0;
let cpuScore = 0;

// Countdown
let countdown = 3;
let countdownActive = true;
let gamePaused = false;
const winningScore = 11;

function initialize() {
  updateCanvasSize();

  updateBallSize();
  initializeBallPosition();
  initializeBallSpeed();

  updatePaddleSize(canvas);
  updateLeftPaddlePosition(previousCanvasHeight, canvas);
  updateRightPaddlePosition(previousCanvasHeight, canvas);
  updatePaddleSpeed(canvas);
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
  ballDx = canvas.width * 0.01;
  ballDy = canvas.height * 0.01;
}

function drawCountdown() {
  const fontSize = canvas.width * 0.2;
  ctx.font = `${fontSize}px Arial`;
  ctx.fillStyle = "rgba(0, 149, 221, 0.5)";

  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  if (countdown === 0) {
    ctx.fillText("Start!", canvas.width / 2, canvas.height / 2);
  } else {
    ctx.fillText(countdown, canvas.width / 2, canvas.height / 2);
  }
}

function drawBall() {
  ctx.beginPath();
  ctx.arc(ballX, ballY, ballRadius, 0, Math.PI * 2);
  ctx.fillStyle = "#0095DD";
  ctx.fill();
  ctx.closePath();
}

function drawCenterLine() {
  const lineWidth = canvas.width * 0.01;
  const radius = lineWidth * 0.7;

  ctx.beginPath();
  ctx.setLineDash([]);
  ctx.fillStyle = "#0095DD";

  for (let ballY = radius; ballY < canvas.height; ballY += radius * 4) {
    ctx.moveTo(canvas.width / 2, ballY);
    ctx.arc(canvas.width / 2, ballY, radius, 0, Math.PI * 2);
  }

  ctx.fill();
  ctx.closePath();
}

function drawScores() {
  const fontSize = canvas.width * 0.2;
  ctx.font = `${fontSize}px Arial`;
  ctx.fillStyle = "rgba(0, 149, 221, 0.5)";

  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(playerScore, canvas.width / 4, canvas.height / 2);
  ctx.fillText(cpuScore, (canvas.width / 4) * 3, canvas.height / 2);
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function startCountdown() {
  const interval = setInterval(() => {
    if (countdown === 0) {
      countdownActive = false;
      clearInterval(interval);
    } else {
      countdown--;
    }
  }, 1000);
}

function showRestartButton(message) {
  const gameOverMessage = document.getElementById("game-over-message");
  const gameOverText = document.getElementById("gameOverText");
  const restartButton = document.getElementById("restartButton");

  gameOverText.textContent = message;
  gameOverMessage.classList.remove("d-none");

  restartButton.onclick = () => {
    playerScore = 0;
    cpuScore = 0;
    gameOverMessage.classList.add("d-none");
    initialize();
    startCountdown();
    gamePaused = false;
  };
}

function gameOver(message) {
  gamePaused = true;
  showRestartButton(message);
}

function resetGame() {
  gamePaused = true;
  setTimeout(() => {
    initialize();
    gamePaused = false;
  }, 500);
}

function moveBall() {
  if (ballX + ballDx < paddleWidth * 2) {
    if (ballY > leftPaddleY && ballY < leftPaddleY + paddleHeight) {
      ballDx = -ballDx;
      const hitPosition =
        (ballY - (leftPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      ballDy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてballDyを変更
    } else {
      // Game Over
      cpuScore++;
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
      playerScore++;
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

function draw() {
  clearCanvas();

  if (countdownActive) {
    drawCountdown();
  } else {
    // draw objects
    drawBall();
    drawCenterLine();
    drawLeftPaddle(ctx);
    drawRightPaddle(ctx, canvas);
    drawScores();

    // move objects
    if (!gamePaused) {
      moveBall();
      moveLeftPaddle(upPressed, downPressed, canvas);
      moveRightPaddle(ballY, canvas);
    }
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

  updatePaddleSize(canvas);
  updateLeftPaddlePosition(previousCanvasHeight, canvas);
  updateRightPaddlePosition(previousCanvasHeight, canvas);
  updatePaddleSpeed(canvas);
}

initialize();
startCountdown();

// resize event
window.addEventListener("resize", onResize, false);

// keybord event
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

requestAnimationFrame(draw);
