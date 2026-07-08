import {
  GRID_HEIGHT,
  GRID_WIDTH,
  HOSTS,
  LEVELS,
  MAX_FALL_SPEED,
  SCREEN_HEIGHT,
  SCREEN_WIDTH,
  TILE_SIZE,
  TILES,
  createGameState,
  createRoom,
  deathTileFor,
  digSoftTile,
  firstTileInRect,
  playerRect,
  recordDeath,
  rectHitsBlockingTile,
  resetPlayerToSpawn,
  resetRoomTerrain,
  spawnPosition,
  tileAt,
  tilesTouchedByRect,
  updatePulses,
  worldToTile
} from "./game-core.mjs";

const canvas = document.querySelector("#game");
const ctx = canvas.getContext("2d");

const colors = {
  deepLoam: "#2A1B12",
  rootAmber: "#C8843A",
  myceliumGlow: "#E8D98A",
  poreMist: "#BFC7C2",
  springCyan: "#33D6D2",
  beetleUmber: "#6B3F1D",
  wormRose: "#D978A0",
  fungalGreen: "#4F8A3D"
};

const keys = new Set();
const virtualKeys = new Set();
const sounds = new Map();
let audioUnlocked = false;
let state = createGameState();
let lastTime = performance.now();

for (const name of ["dash", "jump", "dig", "crack", "death", "morph", "exit", "win"]) {
  const audio = new Audio(`/assets/sounds/${name}.wav`);
  audio.preload = "auto";
  sounds.set(name, audio);
}

window.addEventListener("keydown", (event) => {
  unlockAudio();
  keys.add(event.code);
  if (event.code === "Space") {
    event.preventDefault();
    handleAction();
  }
  if (event.code === "KeyR") {
    restartRoom();
  }
  if (event.code === "Enter" && state.win) {
    restartGame();
  }
});

window.addEventListener("keyup", (event) => {
  keys.delete(event.code);
});

for (const button of document.querySelectorAll("[data-hold]")) {
  const key = button.dataset.hold;
  const start = (event) => {
    event.preventDefault();
    unlockAudio();
    virtualKeys.add(key);
  };
  const end = (event) => {
    event.preventDefault();
    virtualKeys.delete(key);
  };
  button.addEventListener("pointerdown", start);
  button.addEventListener("pointerup", end);
  button.addEventListener("pointercancel", end);
  button.addEventListener("pointerleave", end);
}

for (const button of document.querySelectorAll("[data-tap]")) {
  button.addEventListener("click", () => {
    unlockAudio();
    if (button.dataset.tap === "space") handleAction();
    if (button.dataset.tap === "reset") restartRoom();
  });
}

function unlockAudio() {
  audioUnlocked = true;
}

function playSound(name) {
  if (!audioUnlocked) return;
  const source = sounds.get(name);
  if (!source) return;
  const audio = source.cloneNode();
  audio.volume = 0.35;
  audio.play().catch(() => {});
}

function loop(now) {
  const dt = Math.min(0.05, (now - lastTime) / 1000);
  lastTime = now;
  if (!state.win) update(dt);
  draw();
  requestAnimationFrame(loop);
}

function restartGame() {
  state = createGameState();
}

function restartRoom() {
  resetRoomTerrain(state.room);
  resetPlayerToSpawn(state);
}

function host() {
  return HOSTS[state.hostIndex];
}

function inputDirection() {
  const left = keys.has("ArrowLeft") || keys.has("KeyA") || virtualKeys.has("left");
  const right = keys.has("ArrowRight") || keys.has("KeyD") || virtualKeys.has("right");
  if (left && !right) return -1;
  if (right && !left) return 1;
  return 0;
}

function isDownHeld() {
  return keys.has("ArrowDown") || keys.has("KeyS") || virtualKeys.has("down");
}

function handleAction() {
  if (state.win) {
    restartGame();
    return;
  }
  const currentHost = host();
  if (currentHost.name === "Springtail" && state.player.dashCooldown <= 0) {
    dash(state.player.facing || 1);
    state.player.dashCooldown = 1;
    playSound("dash");
  }
  if (currentHost.name === "Dung Beetle" && state.player.grounded) {
    state.player.vy = -20;
    state.player.grounded = false;
    playSound("jump");
  }
}

function update(dt) {
  updatePulses(state.room, dt);
  state.player.dashCooldown = Math.max(0, state.player.dashCooldown - dt);
  const direction = inputDirection();
  if (direction) state.player.facing = direction;
  if (host().name === "Earthworm" && isDownHeld()) {
    wormDig(direction);
  }
  moveHorizontal(direction * host().speed);
  applyVerticalMotion();
  resolveHazards(dt);
  checkExit();
}

function moveHorizontal(amount) {
  if (amount === 0) return;
  state.player.x += amount;
  if (rectHitsBlockingTile(playerRect(state.player), state.room, host().name)) {
    const step = amount > 0 ? -1 : 1;
    let guard = 80;
    while (guard > 0 && rectHitsBlockingTile(playerRect(state.player), state.room, host().name)) {
      state.player.x += step;
      guard -= 1;
    }
  }
}

function applyVerticalMotion() {
  state.player.vy = Math.min(MAX_FALL_SPEED, state.player.vy + 0.85);
  state.player.y += state.player.vy;
  if (rectHitsBlockingTile(playerRect(state.player), state.room, host().name)) {
    const movingDown = state.player.vy >= 0;
    const step = movingDown ? -1 : 1;
    let guard = 90;
    while (guard > 0 && rectHitsBlockingTile(playerRect(state.player), state.room, host().name)) {
      state.player.y += step;
      guard -= 1;
    }
    if (movingDown) {
      breakCrackedTilesUnderfoot();
    }
    state.player.vy = 0;
    state.player.grounded = movingDown;
  } else {
    state.player.grounded = false;
  }
}

function dash(direction) {
  const step = direction * 12;
  let moved = 0;
  while (Math.abs(moved) < 300) {
    state.player.x += step;
    moved += step;
    if (rectHitsBlockingTile(playerRect(state.player), state.room, host().name)) {
      state.player.x -= step;
      break;
    }
  }
}

function wormDig(direction) {
  const rect = playerRect(state.player);
  const targets = [{ x: rect.x + rect.width / 2, y: rect.y + rect.height + 2 }];
  if (direction < 0) targets.push({ x: rect.x - 2, y: rect.y + rect.height / 2 });
  if (direction > 0) targets.push({ x: rect.x + rect.width + 2, y: rect.y + rect.height / 2 });
  let dug = false;
  for (const target of targets) {
    const point = worldToTile(target.x, target.y);
    dug = digSoftTile(state.room, point.col, point.row) || dug;
  }
  if (dug) playSound("dig");
}

function breakCrackedTilesUnderfoot() {
  if (host().name !== "Dung Beetle") return;
  const rect = playerRect(state.player);
  const probe = { x: rect.x + 2, y: rect.y + rect.height, width: rect.width - 4, height: 4 };
  let broke = false;
  for (const { col, row } of tilesTouchedByRect(probe)) {
    if (tileAt(state.room, col, row) === TILES.CRACKED) {
      state.room.grid[row][col] = TILES.EMPTY;
      broke = true;
    }
  }
  if (broke) playSound("crack");
}

function resolveHazards(dt) {
  const touching = firstTileInRect(playerRect(state.player), state.room, (tile) => tile === TILES.HAZARD);
  if (!touching) {
    state.player.hazardContactTime = 0;
    return;
  }
  if (host().name === "Earthworm") {
    state.player.hazardContactTime += dt;
    if (state.player.hazardContactTime < 2) return;
  }
  playSound("death");
  recordDeath(state);
  playSound("morph");
}

function checkExit() {
  const touching = firstTileInRect(playerRect(state.player), state.room, (tile) => tile === TILES.EXIT);
  if (!touching) return;
  playSound("exit");
  state.roomIndex += 1;
  if (state.roomIndex >= LEVELS.length) {
    state.win = true;
    if (!state.winPlayed) {
      state.winPlayed = true;
      playSound("win");
    }
    return;
  }
  state.room = createRoom(state.roomIndex);
  resetPlayerToSpawn(state);
}

function draw() {
  if (state.win) {
    drawWin();
    return;
  }
  drawBackground();
  drawTiles();
  drawPulses();
  drawPlayer();
  drawHud();
}

function drawBackground() {
  ctx.fillStyle = colors.deepLoam;
  ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  ctx.save();
  ctx.globalAlpha = 0.35;
  ctx.strokeStyle = colors.rootAmber;
  ctx.lineWidth = 3;
  for (const offset of [80, 230, 490, 760, 1010]) {
    ctx.beginPath();
    ctx.moveTo(offset, 0);
    ctx.bezierCurveTo(offset + 75, 180, offset - 40, 420, offset + 160, GRID_HEIGHT * TILE_SIZE);
    ctx.stroke();
  }
  ctx.restore();
}

function drawTiles() {
  for (let row = 0; row < GRID_HEIGHT; row += 1) {
    for (let col = 0; col < GRID_WIDTH; col += 1) {
      const tile = state.room.grid[row][col];
      if (tile === TILES.EMPTY || tile === TILES.SPAWN) continue;
      drawTile(tile, col * TILE_SIZE, row * TILE_SIZE);
    }
  }
}

function drawTile(tile, x, y) {
  if (tile === TILES.SOLID) {
    ctx.fillStyle = colors.beetleUmber;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = colors.deepLoam;
    ctx.lineWidth = 2;
    ctx.strokeRect(x + 1, y + 1, TILE_SIZE - 2, TILE_SIZE - 2);
    drawSoilPebbles(x, y);
  }
  if (tile === TILES.CRACKED) {
    ctx.fillStyle = colors.rootAmber;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = colors.deepLoam;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x + 15, y + 4);
    ctx.lineTo(x + 30, y + 28);
    ctx.lineTo(x + 22, y + 60);
    ctx.moveTo(x + 31, y + 28);
    ctx.lineTo(x + 55, y + 16);
    ctx.stroke();
  }
  if (tile === TILES.PORE) {
    ctx.fillStyle = colors.poreMist;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.fillStyle = colors.deepLoam;
    ctx.beginPath();
    ctx.ellipse(x + 32, y + 32, 23, 15, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  if (tile === TILES.SOFT) {
    ctx.fillStyle = colors.deepLoam;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = colors.wormRose;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(x + 32, y + 32, 17, 0, Math.PI * 2);
    ctx.stroke();
    drawSoilPebbles(x, y, colors.wormRose);
  }
  if (tile === TILES.HAZARD) {
    ctx.fillStyle = colors.deepLoam;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.fillStyle = colors.fungalGreen;
    ctx.beginPath();
    ctx.arc(x + 32, y + 34, 23, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = colors.poreMist;
    ctx.beginPath();
    ctx.arc(x + 25, y + 26, 4, 0, Math.PI * 2);
    ctx.arc(x + 42, y + 39, 5, 0, Math.PI * 2);
    ctx.fill();
  }
  if (tile === TILES.EXIT) {
    const pulse = 4 + Math.sin(performance.now() / 180) * 4;
    ctx.fillStyle = colors.deepLoam;
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = colors.myceliumGlow;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(x + 32, y + 32, 21 + pulse, 0, Math.PI * 2);
    ctx.stroke();
    ctx.fillStyle = colors.myceliumGlow;
    ctx.beginPath();
    ctx.arc(x + 32, y + 32, 10, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawSoilPebbles(x, y, color = colors.deepLoam) {
  ctx.save();
  ctx.globalAlpha = 0.38;
  ctx.fillStyle = color;
  for (const [px, py] of [[12, 16], [42, 12], [22, 45], [51, 47]]) {
    ctx.beginPath();
    ctx.arc(x + px, y + py, 3, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function drawPulses() {
  for (const pulse of state.room.pulses) {
    const progress = pulse.age / 0.5;
    ctx.save();
    ctx.globalAlpha = Math.max(0, 1 - progress);
    ctx.strokeStyle = colors.myceliumGlow;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(pulse.x, pulse.y, 20 + progress * 100, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }
}

function drawPlayer() {
  const rect = playerRect(state.player);
  const currentHost = host();
  ctx.save();
  ctx.translate(rect.x + rect.width / 2, rect.y + rect.height / 2);
  ctx.scale(state.player.facing < 0 ? -1 : 1, 1);
  ctx.fillStyle = currentHost.color;
  ctx.strokeStyle = colors.deepLoam;
  ctx.lineWidth = 3;
  if (currentHost.name === "Springtail") {
    roundedBody(-18, -17, 36, 34, 12);
    ctx.beginPath();
    ctx.moveTo(-10, 12);
    ctx.lineTo(-22, 24);
    ctx.lineTo(-2, 17);
    ctx.stroke();
  } else if (currentHost.name === "Dung Beetle") {
    roundedBody(-20, -17, 40, 34, 15);
    ctx.beginPath();
    ctx.moveTo(-14, 17);
    ctx.lineTo(-22, 25);
    ctx.moveTo(8, 17);
    ctx.lineTo(18, 25);
    ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.ellipse(0, 2, 24, 14, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    for (let x = -12; x <= 12; x += 8) {
      ctx.beginPath();
      ctx.moveTo(x, -9);
      ctx.lineTo(x + 2, 13);
      ctx.stroke();
    }
  }
  ctx.restore();
}

function roundedBody(x, y, width, height, radius) {
  ctx.beginPath();
  ctx.roundRect(x, y, width, height, radius);
  ctx.fill();
  ctx.stroke();
}

function drawHud() {
  const y = GRID_HEIGHT * TILE_SIZE;
  const currentHost = host();
  ctx.fillStyle = colors.deepLoam;
  ctx.fillRect(0, y, SCREEN_WIDTH, 80);
  ctx.strokeStyle = colors.rootAmber;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(0, y);
  ctx.lineTo(SCREEN_WIDTH, y);
  ctx.stroke();
  const cooldown = state.player.dashCooldown <= 0 ? "Ready" : `${state.player.dashCooldown.toFixed(1)}s`;
  const grace = currentHost.name === "Earthworm" && state.player.hazardContactTime > 0
    ? ` | hazard grace ${Math.max(0, 2 - state.player.hazardContactTime).toFixed(1)}s`
    : "";
  drawText(`Host: ${currentHost.name} | room deaths: ${state.room.deathsInRoom}/3 | dash: ${cooldown}${grace}`, 24, y + 29, "22px Verdana", currentHost.color);
  drawText("Move: arrows/A-D | Space: dash/jump | Down+move: worm dig | R: reset room | Enter: restart win", 24, y + 61, "14px Consolas", colors.poreMist);
}

function drawWin() {
  drawBackground();
  ctx.fillStyle = "rgba(42, 27, 18, 0.72)";
  ctx.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
  drawText("You restored the soil.", 640, 330, "72px Georgia", colors.myceliumGlow, "center");
  drawText("Press Enter to restart", 640, 392, "28px Verdana", colors.poreMist, "center");
}

function drawText(text, x, y, font, fill, align = "left") {
  ctx.font = font;
  ctx.textAlign = align;
  ctx.textBaseline = "middle";
  ctx.fillStyle = colors.deepLoam;
  ctx.fillText(text, x + 2, y + 2);
  ctx.fillStyle = fill;
  ctx.fillText(text, x, y);
}

requestAnimationFrame(loop);
