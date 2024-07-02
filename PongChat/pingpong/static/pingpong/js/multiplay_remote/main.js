import {
  keyDownHandlerRight,
  keyUpHandlerRight,
  keyDownHandlerLeft,
  keyUpHandlerLeft,
  upPressedRight,
  downPressedRight,
  upPressedLeft,
  downPressedLeft,
} from "./key_handle.js";

import {
  drawLeftPaddle,
  drawRightPaddle,
  moveLeftPaddle,
  moveRightPaddle,
  updatePaddleElement,
  updateLeftPaddlePositionFromRatio,
  updateRightPaddlePositionFromRatio,
} from "./paddle.js";

import {
  drawBall,
  moveBall,
  initializeBallElement,
  updateBallElement,
  updateBallFromRemote,
} from "./ball.js";

import {
  startCountdown,
  clearCanvas,
  drawCenterLine,
  drawCountdown,
  drawScores,
  drawName,
  countdownActive,
  gamePaused,
} from "./ui.js";

import { updateScoreFromRemote, judgeGameFinish } from "./score.js";

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
window.gameSocket = null;
let player_position = null;

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
    drawName(player_position);

    // move objects
    if (!gamePaused) {
      moveBall(window.gameSocket, player_position);
      moveLeftPaddle(upPressedLeft, downPressedLeft, canvas, window.gameSocket);
      moveRightPaddle(
        upPressedRight,
        downPressedRight,
        canvas,
        window.gameSocket
      );
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

export function initializeGame(gameId) {
  window.gameSocket = new WebSocket(
    `ws://${window.location.host}/ws/game/${gameId}/`
  );
  console.log(`WebSocket URL: ws://${window.location.host}/ws/game/${gameId}/`);

  window.gameSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "player_position") {
      if (data.position === "left") {
        console.log("left");
        player_position = "left";
        document.addEventListener("keydown", keyDownHandlerLeft, false);
        document.addEventListener("keyup", keyUpHandlerLeft, false);
      } else {
        console.log("right");
        player_position = "right";
        document.addEventListener("keydown", keyDownHandlerRight, false);
        document.addEventListener("keyup", keyUpHandlerRight, false);
      }
    }

    if (data.type === "paddle_update") {
      if (data.player_position === "left") {
        updateLeftPaddlePositionFromRatio(data.paddle_position_ratio);
        drawLeftPaddle(ctx);
      } else {
        updateRightPaddlePositionFromRatio(data.paddle_position_ratio);
        drawRightPaddle(ctx, canvas);
      }
    }

    if (data.type === "ball_update") {
      updateBallFromRemote(data);
    }

    if (data.type === "score_update") {
      updateScoreFromRemote(data);
      console.log("Score updated");
      drawScores();
      judgeGameFinish(window.gameSocket);
    }

    if (data.type === "score_update_error") {
      console.log(data.error);
    }
  };

  window.gameSocket.onopen = function (event) {
    console.log("Connected to websocket");
  };

  window.gameSocket.onclose = function (event) {
    console.error("Disconnected from websocket");
  };

  window.gameSocket.onerror = function (event) {
    console.error("Error in websocket");
  };

  initialize();
  startCountdown();

  // resize event
  window.addEventListener("resize", onResize, false);

  requestAnimationFrame(draw);
}
