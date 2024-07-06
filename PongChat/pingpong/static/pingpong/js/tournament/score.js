// Score
export let playerScore = 0;
export let cpuScore = 0;
export const winningScore = 1;

export function incrementCpuScore() {
  cpuScore++;
}

export function incrementPlayerScore() {
  playerScore++;
}

export function resetScores() {
  playerScore = 0;
  cpuScore = 0;
}
