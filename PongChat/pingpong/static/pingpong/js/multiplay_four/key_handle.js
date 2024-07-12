export let upPressedRight = false;
export let downPressedRight = false;
export let upPressedLeft = false;
export let downPressedLeft = false;
export let upPressedLeftMiddle = false;
export let downPressedLeftMiddle = false;

// Right Paddle
export function keyDownHandlerRight(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressedRight = true;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressedRight = true;
  }
}

export function keyUpHandlerRight(e) {
  if (e.key === "Up" || e.key === "ArrowUp") {
    upPressedRight = false;
  } else if (e.key === "Down" || e.key === "ArrowDown") {
    downPressedRight = false;
  }
}

// Left Paddle
export function keyDownHandlerLeft(e) {
  if (e.key === "w" || e.key === "W") {
    upPressedLeft = true;
  } else if (e.key === "s" || e.key === "S") {
    downPressedLeft = true;
  }
}

export function keyUpHandlerLeft(e) {
  if (e.key === "w" || e.key === "W") {
    upPressedLeft = false;
  } else if (e.key === "s" || e.key === "S") {
    downPressedLeft = false;
  }
}

// LeftMiddle Paddle
export function keyDownHandlerLeftMiddle(e) {
  if (e.key === "e" || e.key === "E") {
    upPressedLeftMiddle = true;
  } else if (e.key === "d" || e.key === "D") {
    downPressedLeftMiddle = true;
  }
}

export function keyUpHandlerLeftMiddle(e) {
  if (e.key === "e" || e.key === "E") {
    upPressedLeftMiddle = false;
  } else if (e.key === "d" || e.key === "D") {
    downPressedLeftMiddle = false;
  }
}
