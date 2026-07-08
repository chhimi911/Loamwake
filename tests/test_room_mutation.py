from src.room import Room
from src.settings import TILE_SIZE
from src.tiles import EMPTY, SOFT, SOLID


def tile_center(col, row):
    return col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2


def changed_tiles(room, col, row):
    return {
        room.tile_at(x, y)
        for y in range(row - 1, row + 2)
        for x in range(col - 1, col + 2)
    }


def test_springtail_death_makes_empty_tunnel_tiles():
    room = Room(0)
    x, y = tile_center(10, 5)
    room.mutate_death_area("Springtail", x, y)
    assert changed_tiles(room, 10, 5) == {EMPTY}


def test_beetle_death_makes_solid_platform_tiles():
    room = Room(0)
    x, y = tile_center(10, 5)
    room.mutate_death_area("Dung Beetle", x, y)
    assert changed_tiles(room, 10, 5) == {SOLID}


def test_earthworm_death_makes_soft_soil_tiles():
    room = Room(0)
    x, y = tile_center(10, 5)
    room.mutate_death_area("Earthworm", x, y)
    assert changed_tiles(room, 10, 5) == {SOFT}


def test_three_deaths_reset_room_terrain():
    room = Room(0)
    x, y = tile_center(10, 5)
    assert room.record_death("Dung Beetle", x, y) is False
    assert room.deaths_in_room == 1
    assert room.tile_at(10, 5) == SOLID
    assert room.record_death("Earthworm", x, y) is False
    assert room.deaths_in_room == 2
    assert room.record_death("Springtail", x, y) is True
    assert room.deaths_in_room == 0
    assert ["".join(row) for row in room.grid] == room.original_rows
