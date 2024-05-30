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
let ballRadius, x, y, dx, dy;
let paddleWidth, paddleHeight, leftPaddleY, rightPaddleY, paddleDy;
let previousCanvasWidth, previousCanvasHeight;
let upPressed = false;
let downPressed = false;
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

  updatePaddleSize();
  updateLeftPaddlePosition();
  updateRightPaddlePosition();
  updatePaddleSpeed();
}

function initializeBallPosition() {
  x = canvas.width / 2;
  y = canvas.height / 2;
}

function getRandomDirection() {
  return Math.random() < 0.5 ? 1 : -1;
}

function initializeBallSpeed() {
  const angle = Math.random() * 2 * Math.PI;
  dx = canvas.width * 0.01 * getRandomDirection();
  dy = canvas.height * 0.01 * Math.sin(angle);
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
  const ballPositionRatioX = isNaN(x / previousCanvasWidth)
    ? 0.5
    : x / previousCanvasWidth;
  const ballPositionRatioY = isNaN(y / previousCanvasHeight)
    ? 0.5
    : y / previousCanvasHeight;

  x = canvas.width * ballPositionRatioX;
  y = canvas.height * ballPositionRatioY;
}

function updateBallSize() {
  ballRadius = Math.min(canvas.width, canvas.height) * 0.05;
}

function updateBallSpeed() {
  dx = canvas.width * 0.01;
  dy = canvas.height * 0.01;
}

function updateLeftPaddlePosition() {
  const paddlePositionRatioY = isNaN(leftPaddleY / previousCanvasHeight)
    ? 0.5
    : leftPaddleY / previousCanvasHeight;
  leftPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

function updateRightPaddlePosition() {
  const paddlePositionRatioY = isNaN(rightPaddleY / previousCanvasHeight)
    ? 0.5
    : rightPaddleY / previousCanvasHeight;
  rightPaddleY = (canvas.height - paddleHeight) * paddlePositionRatioY;
}

function updatePaddleSize() {
  paddleWidth = canvas.width * 0.015;
  paddleHeight = canvas.height * 0.2;
}

function updatePaddleSpeed() {
  paddleDy = canvas.height * 0.015;
}

function keyDownHandler(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressed = true;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressed = true;
  }
}

function keyUpHandler(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressed = false;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressed = false;
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

function drawBall() {
  ctx.beginPath();
  ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
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

  for (let y = radius; y < canvas.height; y += radius * 4) {
    ctx.moveTo(canvas.width / 2, y);
    ctx.arc(canvas.width / 2, y, radius, 0, Math.PI * 2);
  }

  ctx.fill();
  ctx.closePath();
}

function drawRoundedRect(x, y, width, height, radius) {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
}

function drawLeftPaddle() {
  const radius = paddleWidth;
  drawRoundedRect(
    paddleWidth,
    leftPaddleY,
    paddleWidth,
    paddleHeight,
    radius / 2,
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
}

function drawRightPaddle() {
  const radius = paddleWidth;
  drawRoundedRect(
    canvas.width - paddleWidth * 2,
    rightPaddleY,
    paddleWidth,
    paddleHeight,
    radius / 2,
  );
  ctx.fillStyle = "#0095DD";
  ctx.fill();
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
  const gameOverMessage = document.getElementById("gameOverMessage");
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
  if (x + dx < paddleWidth * 2) {
    if (y > leftPaddleY && y < leftPaddleY + paddleHeight) {
      dx = -dx;
      const hitPosition =
        (y - (leftPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      dy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてdyを変更
    } else {
      // Game Over
      cpuScore++;
      if (cpuScore >= winningScore) {
        gameOver("CPU wins!");
      } else {
        resetGame();
      }
    }
  } else if (x + dx > canvas.width - paddleWidth * 2) {
    if (y > rightPaddleY && y < rightPaddleY + paddleHeight) {
      dx = -dx;
      const hitPosition =
        (y - (rightPaddleY + paddleHeight / 2)) / (paddleHeight / 2);
      dy = hitPosition * (canvas.height * 0.02); // 中央からの距離に応じてdyを変更
    } else {
      // Game Over
      playerScore++;
      if (playerScore >= winningScore) {
        gameOver("Player wins!");
      } else {
        resetGame();
      }
    }
  }

  if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
    dy = -dy;
  }

  x += dx;
  y += dy;
}

function moveLeftPaddle() {
  if (upPressed && leftPaddleY > 0) {
    leftPaddleY -= paddleDy;
  } else if (downPressed && leftPaddleY < canvas.height - paddleHeight) {
    leftPaddleY += paddleDy;
  }
}

function moveRightPaddle() {
  const diff = y - (rightPaddleY + paddleHeight / 2);
  if (Math.abs(diff) > paddleDy && Math.random() < 0.8) {
    let direction = 1;
    if (Math.random() < 0.1) {
      direction = -1;
    }

    if (y < rightPaddleY + paddleHeight / 2 && rightPaddleY > 0) {
      rightPaddleY -= paddleDy * direction;
    } else if (
      y > rightPaddleY + paddleHeight / 2 &&
      rightPaddleY < canvas.height - paddleHeight
    ) {
      rightPaddleY += paddleDy * direction;
    }
  }
}

function draw() {
  clearCanvas();

  if (countdownActive) {
    drawCountdown();
  } else {
    // draw objects
    drawBall();
    drawCenterLine();
    drawLeftPaddle();
    drawRightPaddle();
    drawScores();

    // move objects
    if (!gamePaused) {
      moveBall();
      moveLeftPaddle();
      moveRightPaddle();
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

  updatePaddleSize();
  updateLeftPaddlePosition();
  updateRightPaddlePosition();
  updatePaddleSpeed();
}

initialize();
startCountdown();

// resize event
window.addEventListener("resize", onResize, false);

// keybord event
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

requestAnimationFrame(draw);
