from pathlib import Path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_WIDTH = 20
GRID_HEIGHT = 10
TILE_SIZE = 64
HUD_HEIGHT = 80
FPS = 60

PLAYER_WIDTH = 38
PLAYER_HEIGHT = 48
GRAVITY = 0.85
MAX_FALL_SPEED = 18

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT_DIR / "assets"

COLORS = {
    "deep_loam": "#2A1B12",
    "root_amber": "#C8843A",
    "mycelium_glow": "#E8D98A",
    "pore_mist": "#BFC7C2",
    "spring_cyan": "#33D6D2",
    "beetle_umber": "#6B3F1D",
    "worm_rose": "#D978A0",
    "fungal_green": "#4F8A3D",
}


def hex_color(name):
    value = COLORS[name].lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))
