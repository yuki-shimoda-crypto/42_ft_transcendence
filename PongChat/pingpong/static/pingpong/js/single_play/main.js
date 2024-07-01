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
  updatePaddleElement,
} from "./paddle.js";

import {
  drawBall,
  moveBall,
  initializeBallElement,
  updateBallElement,
  ballY,
} from "./ball.js";

import {
  startCountdown,
  clearCanvas,
  drawCenterLine,
  drawCountdown,
  drawScores,
  countdownActive,
  gamePaused,
} from "./ui.js";

// デュース機能を追加する
// 点数のプログレスバーを追加する
// プレイヤー名を入力して、それを表示する
// 勝利者を表示する
// 最初の画面を作成する

// プレイヤー名を入力するフォームを作成する
// プレイヤー名を入力して、それを表示する
// スタートボタンを作成する
// スタートボタンを押すと、ゲームが始まる

export const canvas = document.querySelector("#myCanvas");
export const ctx = canvas.getContext("2d");
export let previousCanvasWidth, previousCanvasHeight;

export function initialize() {
  updateCanvasSize();
  initializeBallElement();
  updatePaddleElement();
}

function updateCanvasSize() {
  const contentPlaceholder = document.querySelector("#content-placeholder");
  if (!contentPlaceholder) {
    return;
  }

  const windowWidth = contentPlaceholder.clientWidth;
  const windowHeight = window.innerHeight;
  const aspectRatio = 16 / 9; // 16:9

  if (windowWidth / windowHeight > aspectRatio) {
    canvas.width = Math.max(0, windowHeight * aspectRatio);
    canvas.height = windowHeight;
  } else {
    canvas.width = Math.max(0, windowWidth);
    canvas.height = windowWidth / aspectRatio;
  }
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
  updateBallElement();
  updatePaddleElement();
}

initialize();
startCountdown();

// resize event
window.addEventListener("resize", onResize, false);
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

requestAnimationFrame(draw);
