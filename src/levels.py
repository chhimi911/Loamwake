from .settings import GRID_HEIGHT, GRID_WIDTH
from .tiles import EXIT, SPAWN

LEVELS = [
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
        "XXXXXXXXXXXXXXXXXXXX",
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
        "XXXXXXXXXXXXXXXXXXXX",
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
        "XXXXXXXXXXXXXXXXXXXX",
    ],
]


def validate_level(raw_rows):
    """Check the text-grid rules before a room is loaded."""
    if len(raw_rows) != GRID_HEIGHT:
        raise ValueError(f"Expected {GRID_HEIGHT} rows, found {len(raw_rows)}")
    if any(len(row) != GRID_WIDTH for row in raw_rows):
        raise ValueError("Every level row must be 20 tiles wide")
    flat = "".join(raw_rows)
    if flat.count(SPAWN) != 1:
        raise ValueError("Each level needs exactly one spawn tile")
    if flat.count(EXIT) != 1:
        raise ValueError("Each level needs exactly one exit tile")


def validate_all_levels():
    for rows in LEVELS:
        validate_level(rows)
