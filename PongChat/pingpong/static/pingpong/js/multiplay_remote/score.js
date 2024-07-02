import { gameOver, resetGame } from "./game_control.js";
// Score
export let playerScore = 0;
export let cpuScore = 0;
export const winningScore = 11;

export function updateScoreFromRemote(data) {
  playerScore = data.score1;
  cpuScore = data.score2;
}

export function incrementRightScore(gameSocket) {
  console.log("incrementCpuScore");
  const sendCpuScore = cpuScore + 1;
  gameSocket.send(
    JSON.stringify({
      type: "update_score",
      score1: playerScore,
      score2: sendCpuScore,
    })
  );
}

export function incrementLeftScore(gameSocket) {
  console.log("incrementPlayerScore");
  const sendPlayerScore = playerScore + 1;
  gameSocket.send(
    JSON.stringify({
      type: "update_score",
      score1: sendPlayerScore,
      score2: cpuScore,
    })
  );
}

export function resetScores() {
  playerScore = 0;
  cpuScore = 0;
}

export function judgeGameFinish(gameSocket) {
  if (cpuScore >= winningScore) {
    gameOver("Congratulations! Right win!", gameSocket);
  } else if (playerScore >= winningScore) {
    gameOver("Congratulations! Left win!", gameSocket);
  } else {
    resetGame();
  }
}
