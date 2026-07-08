import assert from "node:assert/strict";
import {
  HOSTS,
  TILES,
  TILE_SIZE,
  createGameState,
  deathTileFor,
  mutateDeathArea,
  nextHostIndex,
  validateLevels
} from "./game-core.mjs";

function tileCenter(col, row) {
  return {
    x: col * TILE_SIZE + TILE_SIZE / 2,
    y: row * TILE_SIZE + TILE_SIZE / 2
  };
}

validateLevels();

let index = 0;
const names = [];
for (let step = 0; step < 5; step += 1) {
  names.push(HOSTS[index].name);
  index = nextHostIndex(index);
}
assert.deepEqual(names, ["Springtail", "Dung Beetle", "Earthworm", "Springtail", "Dung Beetle"]);

assert.equal(deathTileFor("Springtail"), TILES.EMPTY);
assert.equal(deathTileFor("Dung Beetle"), TILES.SOLID);
assert.equal(deathTileFor("Earthworm"), TILES.SOFT);

for (const [host, expected] of [
  ["Springtail", TILES.EMPTY],
  ["Dung Beetle", TILES.SOLID],
  ["Earthworm", TILES.SOFT]
]) {
  const state = createGameState();
  const point = tileCenter(10, 5);
  mutateDeathArea(state.room, host, point.x, point.y);
  const changed = [];
  for (let row = 4; row <= 6; row += 1) {
    for (let col = 9; col <= 11; col += 1) {
      changed.push(state.room.grid[row][col]);
    }
  }
  assert.deepEqual(new Set(changed), new Set([expected]));
}

console.log("web core tests passed");
