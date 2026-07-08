from dataclasses import dataclass

from .levels import LEVELS, validate_level
from .settings import GRID_HEIGHT, GRID_WIDTH, TILE_SIZE
from .tiles import EMPTY, EXIT, HAZARD, MUTABLE_TILES, SOFT, SPAWN, death_tile_for


@dataclass(frozen=True)
class TilePoint:
    col: int
    row: int


class Room:
    """Mutable room state: terrain changes persist until the room resets."""

    def __init__(self, index):
        self.index = index
        self.original_rows = LEVELS[index]
        validate_level(self.original_rows)
        self.grid = [list(row) for row in self.original_rows]
        self.spawn = self._find(SPAWN)
        self.exit = self._find(EXIT)
        self.deaths_in_room = 0
        self.pulses = []

    def _find(self, tile):
        for row, values in enumerate(self.grid):
            for col, value in enumerate(values):
                if value == tile:
                    return TilePoint(col, row)
        raise ValueError(f"Tile {tile!r} not found")

    def tile_at(self, col, row):
        if col < 0 or col >= GRID_WIDTH or row < 0 or row >= GRID_HEIGHT:
            return None
        return self.grid[row][col]

    def set_tile(self, col, row, tile):
        if 0 <= col < GRID_WIDTH and 0 <= row < GRID_HEIGHT:
            if self.grid[row][col] in MUTABLE_TILES:
                self.grid[row][col] = tile

    def world_to_tile(self, x, y):
        return TilePoint(int(x // TILE_SIZE), int(y // TILE_SIZE))

    def spawn_position(self):
        return (
            self.spawn.col * TILE_SIZE + 13,
            self.spawn.row * TILE_SIZE + 8,
        )

    def mutate_death_area(self, host_name, world_x, world_y):
        """Convert a 3x3 tile area around the death point into corpse terrain."""
        center = self.world_to_tile(world_x, world_y)
        new_tile = death_tile_for(host_name)
        changed = []
        for row in range(center.row - 1, center.row + 2):
            for col in range(center.col - 1, center.col + 2):
                before = self.tile_at(col, row)
                if before in MUTABLE_TILES:
                    self.grid[row][col] = new_tile
                    changed.append(TilePoint(col, row))
        self.pulses.append({"x": world_x, "y": world_y, "age": 0.0, "host": host_name})
        return changed

    def record_death(self, host_name, world_x, world_y):
        self.mutate_death_area(host_name, world_x, world_y)
        self.deaths_in_room += 1
        if self.deaths_in_room >= 3:
            self.reset_terrain()
            return True
        return False

    def reset_terrain(self):
        self.grid = [list(row) for row in self.original_rows]
        self.spawn = self._find(SPAWN)
        self.exit = self._find(EXIT)
        self.deaths_in_room = 0
        self.pulses.clear()

    def dig_soft_tile(self, col, row):
        if self.tile_at(col, row) == SOFT:
            self.grid[row][col] = EMPTY
            return True
        return False

    def update_pulses(self, dt):
        for pulse in self.pulses:
            pulse["age"] += dt
        self.pulses = [pulse for pulse in self.pulses if pulse["age"] <= 0.5]

    def hazard_tiles(self):
        for row, values in enumerate(self.grid):
            for col, value in enumerate(values):
                if value == HAZARD:
                    yield TilePoint(col, row)
