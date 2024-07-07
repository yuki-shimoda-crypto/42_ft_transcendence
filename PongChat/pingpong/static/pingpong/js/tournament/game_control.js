import { pauseGame, resumeGame, showRestartButton } from "./ui.js";
import { initialize } from "./main.js";
import { sendWinner } from "./network.js";

export function gameOver(message, winner_id) {
  sendWinner(winner_id);
  pauseGame();
  showRestartButton(message);
}

export function resetGame() {
  pauseGame();
  setTimeout(() => {
    initialize();
    resumeGame();
  }, 500);
}
