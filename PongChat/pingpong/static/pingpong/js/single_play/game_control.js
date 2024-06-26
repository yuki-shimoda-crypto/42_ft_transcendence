import { pauseGame, resumeGame, showRestartButton } from "./ui.js";
import { initialize } from "./main.js";

export function gameOver(message) {
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
