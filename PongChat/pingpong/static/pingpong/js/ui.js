import { resetScores, playerScore, cpuScore } from "./score.js";
import { canvas, ctx, initialize } from "./main.js";

// Countdown
let countdown = 3;
export let countdownActive = true;
export let gamePaused = false;

export function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

export function drawCenterLine() {
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

export function drawCountdown() {
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

export function drawScores() {
  const fontSize = canvas.width * 0.2;
  ctx.font = `${fontSize}px Arial`;
  ctx.fillStyle = "rgba(0, 149, 221, 0.5)";

  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(playerScore, canvas.width / 4, canvas.height / 2);
  ctx.fillText(cpuScore, (canvas.width / 4) * 3, canvas.height / 2);
}

export function showRestartButton(message) {
  const gameOverMessage = document.getElementById("game-over-message");
  const gameOverText = document.getElementById("gameOverText");
  const restartButton = document.getElementById("restartButton");

  gameOverText.textContent = message;
  gameOverMessage.classList.remove("d-none");

  restartButton.onclick = () => {
    resetScores();
    gameOverMessage.classList.add("d-none");
    initialize();
    startCountdown();
    resumeGame();
  };
}

export function startCountdown() {
  const interval = setInterval(() => {
    if (countdown === 0) {
      countdownActive = false;
      clearInterval(interval);
    } else {
      countdown--;
    }
  }, 1000);
}

export function pauseGame() {
  gamePaused = true;
}

export function resumeGame() {
  gamePaused = false;
}
