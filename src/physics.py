from .settings import GRID_HEIGHT, GRID_WIDTH, TILE_SIZE
from .tiles import blocks_host


def tiles_touched_by_rect(rect):
    left = max(0, int(rect.left // TILE_SIZE))
    right = min(GRID_WIDTH - 1, int((rect.right - 1) // TILE_SIZE))
    top = max(0, int(rect.top // TILE_SIZE))
    bottom = min(GRID_HEIGHT - 1, int((rect.bottom - 1) // TILE_SIZE))
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            yield col, row


def rect_hits_blocking_tile(rect, room, host_name):
    """Grid collision: art never decides gameplay, only tile characters do."""
    if rect.left < 0 or rect.right > GRID_WIDTH * TILE_SIZE:
        return True
    if rect.top < 0 or rect.bottom > GRID_HEIGHT * TILE_SIZE:
        return True
    for col, row in tiles_touched_by_rect(rect):
        if blocks_host(room.tile_at(col, row), host_name):
            return True
    return False


def first_tile(rect, room, predicate):
    for col, row in tiles_touched_by_rect(rect):
        if predicate(room.tile_at(col, row)):
            return col, row
    return None
