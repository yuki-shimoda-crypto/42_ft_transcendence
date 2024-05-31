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
} from "./paddle.js";

import {
  drawBall,
  moveBall,
  updateBallPosition,
  updateBallSize,
  updateBallSpeed,
  initializeBallPosition,
  initializeBallSpeed,
  ballY,
} from "./ball.js";

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
let previousCanvasWidth, previousCanvasHeight;

// Score
export let playerScore = 0;
export let cpuScore = 0;
export const winningScore = 11;

// Countdown
let countdown = 3;
let countdownActive = true;
let gamePaused = false;

function initialize() {
  updateCanvasSize();

  updateBallSize(canvas);
  initializeBallPosition(canvas);
  initializeBallSpeed(canvas);

  updatePaddleSize(canvas);
  updateLeftPaddlePosition(previousCanvasHeight, canvas);
  updateRightPaddlePosition(previousCanvasHeight, canvas);
  updatePaddleSpeed(canvas);
}

export function incrementCpuScore() {
  cpuScore++;
}

export function incrementPlayerScore() {
  playerScore++;
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

function drawCenterLine() {
  const lineWidth = canvas.width * 0.01;
  const radius = lineWidth * 0.7;

  ctx.beginPath();
  ctx.setLineDash([]);
  ctx.fillStyle = "#0095DD";

  for (let y = radius; y < canvas.height; y += radius * 4) {
    ctx.moveTo(canvas.width / 2, y);
    ctx.arc(canvas.width / 2, y, radius, 0, Math.PI * 2);
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

export function gameOver(message) {
  gamePaused = true;
  showRestartButton(message);
}

export function resetGame() {
  gamePaused = true;
  setTimeout(() => {
    initialize();
    gamePaused = false;
  }, 500);
}

function draw() {
  clearCanvas();

  if (countdownActive) {
    drawCountdown();
  } else {
    // draw objects
    drawBall(ctx);
    drawCenterLine();
    drawLeftPaddle(ctx);
    drawRightPaddle(ctx, canvas);
    drawScores();

    // move objects
    if (!gamePaused) {
      moveBall(canvas);
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

  updateBallSize(canvas);
  updateBallPosition(canvas, previousCanvasWidth, previousCanvasHeight);
  updateBallSpeed(canvas);

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
