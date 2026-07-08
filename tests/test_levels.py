from src.hosts import HOSTS, next_host_index
from src.levels import LEVELS, validate_level
from src.settings import GRID_HEIGHT, GRID_WIDTH
from src.tiles import EXIT, SPAWN


def test_levels_are_rectangular_and_expected_size():
    for rows in LEVELS:
        validate_level(rows)
        assert len(rows) == GRID_HEIGHT
        assert all(len(row) == GRID_WIDTH for row in rows)


def test_levels_have_one_spawn_and_exit():
    for rows in LEVELS:
        flat = "".join(rows)
        assert flat.count(SPAWN) == 1
        assert flat.count(EXIT) == 1


def test_host_rotation_order():
    names = []
    index = 0
    for _ in range(5):
        names.append(HOSTS[index].name)
        index = next_host_index(index)
    assert names == [
        "Springtail",
        "Dung Beetle",
        "Earthworm",
        "Springtail",
        "Dung Beetle",
    ]
