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
} from "./paddle.js";

import {
  drawBall,
  moveBall,
  initializeBallElement,
  updateBallElement,
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
      moveLeftPaddle(upPressedLeft, downPressedLeft, canvas);
      moveRightPaddle(upPressedRight, downPressedRight, canvas);
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
  const gameSocket = new WebSocket(
    `ws://${window.location.host}/ws/game/${gameId}/`
  );
  console.log(`WebSocket URL: ws://${window.location.host}/ws/game/${gameId}/`);

  gameSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "player_position") {
      // if (data.player === "left") {
      //   updatePaddleElement(data.player, data.position);
      // } else if (data.player === "right") {
      //   updatePaddleElement(data.player, data.position);
      // }
      if (data.position === "left") {
        console.log("left");
        // updatePaddleElement("left", data.y);
      } else {
        console.log("right");
        // updatePaddleElement("right", data.y);
      }
    }
  };

  gameSocket.onopen = function (event) {
    console.log("Connected to websocket");
  };

  gameSocket.onclose = function (event) {
    console.error("Disconnected from websocket");
  };

  gameSocket.onerror = function (event) {
    console.error("Error in websocket");
  };

  initialize();
  startCountdown();

  // resize event
  window.addEventListener("resize", onResize, false);
  document.addEventListener("keydown", keyDownHandlerRight, false);
  document.addEventListener("keyup", keyUpHandlerRight, false);
  document.addEventListener("keydown", keyDownHandlerLeft, false);
  document.addEventListener("keyup", keyUpHandlerLeft, false);

  requestAnimationFrame(draw);
}
