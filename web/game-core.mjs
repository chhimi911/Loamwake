export const SCREEN_WIDTH = 1280;
export const SCREEN_HEIGHT = 720;
export const GRID_WIDTH = 20;
export const GRID_HEIGHT = 10;
export const TILE_SIZE = 64;
export const PLAYER_WIDTH = 38;
export const PLAYER_HEIGHT = 48;
export const GRAVITY = 0.85;
export const MAX_FALL_SPEED = 18;

export const TILES = {
  EMPTY: ".",
  SOLID: "X",
  CRACKED: "C",
  PORE: "G",
  SOFT: "S",
  HAZARD: "H",
  SPAWN: "P",
  EXIT: "E"
};

export const LEVELS = [
  [
    "XXXXXXXXXXXXXXXXXXXX",
    "X..................X",
    "X.....G.......XXX..X",
    "X.P...G.......X.E..X",
    "XXXX..G..XXX..X.XXXX",
    "X.....G....C..X....X",
    "X..XXXXXXX.C..XXXX.X",
    "X..S.......C.......X",
    "X..S..HHH..X..HHH..X",
    "XXXXXXXXXXXXXXXXXXXX"
  ],
  [
    "XXXXXXXXXXXXXXXXXXXX",
    "X.P........G.......X",
    "XXXXXXCXXXXGXXXX...X",
    "X.....C....G...X.E.X",
    "X..H..C........X.XXX",
    "X..XXXXXXXXSSSSX...X",
    "X..........S...XXX.X",
    "X...HHHH...S.......X",
    "X..XXXXXX..S..HH...X",
    "XXXXXXXXXXXXXXXXXXXX"
  ],
  [
    "XXXXXXXXXXXXXXXXXXXX",
    "X.P..............E.X",
    "XXXX..G..XXXXXXXXX.X",
    "X.....G........X...X",
    "X..C..G..HHHH..X.C.X",
    "X..C..XXXXXXXX.X.C.X",
    "X..C...........X...X",
    "X..XXXX..SSSS..XXX.X",
    "X.....H..S..H......X",
    "XXXXXXXXXXXXXXXXXXXX"
  ]
];

export const HOSTS = [
  { name: "Springtail", speed: 8, color: "#33D6D2" },
  { name: "Dung Beetle", speed: 3, color: "#6B3F1D" },
  { name: "Earthworm", speed: 4, color: "#D978A0" }
];

export function validateLevels() {
  for (const rows of LEVELS) {
    if (rows.length !== GRID_HEIGHT) {
      throw new Error("Every room must have 10 rows.");
    }
    if (rows.some((row) => row.length !== GRID_WIDTH)) {
      throw new Error("Every room row must have 20 columns.");
    }
    const flat = rows.join("");
    if (flat.split(TILES.SPAWN).length - 1 !== 1) {
      throw new Error("Every room needs exactly one spawn.");
    }
    if (flat.split(TILES.EXIT).length - 1 !== 1) {
      throw new Error("Every room needs exactly one exit.");
    }
  }
}

export function nextHostIndex(index) {
  return (index + 1) % HOSTS.length;
}

export function deathTileFor(hostName) {
  if (hostName === "Springtail") return TILES.EMPTY;
  if (hostName === "Dung Beetle") return TILES.SOLID;
  if (hostName === "Earthworm") return TILES.SOFT;
  throw new Error(`Unknown host ${hostName}`);
}

export function blocksHost(tile, hostName) {
  if (tile === null) return true;
  if ([TILES.EMPTY, TILES.SPAWN, TILES.EXIT, TILES.HAZARD].includes(tile)) {
    return false;
  }
  if (tile === TILES.PORE) {
    return hostName !== "Springtail";
  }
  return [TILES.SOLID, TILES.CRACKED, TILES.SOFT].includes(tile);
}

export function createRoom(index) {
  const originalRows = LEVELS[index];
  const grid = originalRows.map((row) => row.split(""));
  return {
    index,
    originalRows,
    grid,
    spawn: findTile(grid, TILES.SPAWN),
    exit: findTile(grid, TILES.EXIT),
    deathsInRoom: 0,
    pulses: []
  };
}

export function createGameState() {
  validateLevels();
  const room = createRoom(0);
  return {
    roomIndex: 0,
    hostIndex: 0,
    room,
    player: createPlayer(room),
    win: false,
    winPlayed: false
  };
}

export function createPlayer(room) {
  const position = spawnPosition(room);
  return {
    x: position.x,
    y: position.y,
    vy: 0,
    grounded: false,
    facing: 1,
    dashCooldown: 0,
    hazardContactTime: 0
  };
}

export function spawnPosition(room) {
  return {
    x: room.spawn.col * TILE_SIZE + 13,
    y: room.spawn.row * TILE_SIZE + 8
  };
}

export function resetPlayerToSpawn(state) {
  state.player = createPlayer(state.room);
}

export function resetRoomTerrain(room) {
  room.grid = room.originalRows.map((row) => row.split(""));
  room.spawn = findTile(room.grid, TILES.SPAWN);
  room.exit = findTile(room.grid, TILES.EXIT);
  room.deathsInRoom = 0;
  room.pulses = [];
}

export function findTile(grid, target) {
  for (let row = 0; row < grid.length; row += 1) {
    for (let col = 0; col < grid[row].length; col += 1) {
      if (grid[row][col] === target) {
        return { col, row };
      }
    }
  }
  throw new Error(`Tile ${target} not found.`);
}

export function tileAt(room, col, row) {
  if (col < 0 || col >= GRID_WIDTH || row < 0 || row >= GRID_HEIGHT) {
    return null;
  }
  return room.grid[row][col];
}

export function setTile(room, col, row, tile) {
  if (col >= 0 && col < GRID_WIDTH && row >= 0 && row < GRID_HEIGHT) {
    room.grid[row][col] = tile;
  }
}

export function worldToTile(x, y) {
  return {
    col: Math.floor(x / TILE_SIZE),
    row: Math.floor(y / TILE_SIZE)
  };
}

export function mutateDeathArea(room, hostName, x, y) {
  const center = worldToTile(x, y);
  const tile = deathTileFor(hostName);
  for (let row = center.row - 1; row <= center.row + 1; row += 1) {
    for (let col = center.col - 1; col <= center.col + 1; col += 1) {
      const current = tileAt(room, col, row);
      if ([TILES.EMPTY, TILES.SOLID, TILES.CRACKED, TILES.PORE, TILES.SOFT, TILES.HAZARD].includes(current)) {
        setTile(room, col, row, tile);
      }
    }
  }
  room.pulses.push({ x, y, age: 0, hostName });
}

export function recordDeath(state) {
  const host = HOSTS[state.hostIndex];
  const rect = playerRect(state.player);
  mutateDeathArea(state.room, host.name, rect.x + rect.width / 2, rect.y + rect.height / 2);
  state.room.deathsInRoom += 1;
  state.hostIndex = nextHostIndex(state.hostIndex);
  if (state.room.deathsInRoom >= 3) {
    resetRoomTerrain(state.room);
  }
  resetPlayerToSpawn(state);
}

export function playerRect(player) {
  return {
    x: Math.round(player.x),
    y: Math.round(player.y),
    width: PLAYER_WIDTH,
    height: PLAYER_HEIGHT
  };
}

export function tilesTouchedByRect(rect) {
  const left = Math.max(0, Math.floor(rect.x / TILE_SIZE));
  const right = Math.min(GRID_WIDTH - 1, Math.floor((rect.x + rect.width - 1) / TILE_SIZE));
  const top = Math.max(0, Math.floor(rect.y / TILE_SIZE));
  const bottom = Math.min(GRID_HEIGHT - 1, Math.floor((rect.y + rect.height - 1) / TILE_SIZE));
  const result = [];
  for (let row = top; row <= bottom; row += 1) {
    for (let col = left; col <= right; col += 1) {
      result.push({ col, row });
    }
  }
  return result;
}

export function rectHitsBlockingTile(rect, room, hostName) {
  if (rect.x < 0 || rect.x + rect.width > GRID_WIDTH * TILE_SIZE) return true;
  if (rect.y < 0 || rect.y + rect.height > GRID_HEIGHT * TILE_SIZE) return true;
  return tilesTouchedByRect(rect).some(({ col, row }) => blocksHost(tileAt(room, col, row), hostName));
}

export function firstTileInRect(rect, room, predicate) {
  return tilesTouchedByRect(rect).find(({ col, row }) => predicate(tileAt(room, col, row))) || null;
}

export function digSoftTile(room, col, row) {
  if (tileAt(room, col, row) === TILES.SOFT) {
    setTile(room, col, row, TILES.EMPTY);
    return true;
  }
  return false;
}

export function updatePulses(room, dt) {
  for (const pulse of room.pulses) {
    pulse.age += dt;
  }
  room.pulses = room.pulses.filter((pulse) => pulse.age <= 0.5);
}
