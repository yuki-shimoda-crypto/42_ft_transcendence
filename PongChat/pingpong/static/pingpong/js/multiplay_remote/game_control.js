import { pauseGame, resumeGame, showRestartButton } from "./ui.js";
import { initialize } from "./main.js";

export function gameOver(message, gameSocket) {
  pauseGame();
  gameSocket.send(
    JSON.stringify({
      type: "end_game",
    })
  );
  showRestartButton(message);
}

export function resetGame() {
  pauseGame();
  setTimeout(() => {
    initialize();
    resumeGame();
  }, 500);
}
