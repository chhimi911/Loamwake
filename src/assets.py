from .settings import ASSET_DIR, TILE_SIZE


class AssetManager:
    """Loads optional PNG assets; callers draw palette fallbacks when missing."""

    def __init__(self, pygame):
        self.pygame = pygame
        self.images = {}

    def load(self):
        specs = {
            "springtail": ("hosts/springtail.png", (44, 48)),
            "beetle": ("hosts/beetle.png", (48, 44)),
            "earthworm": ("hosts/earthworm.png", (50, 32)),
            "solid_soil": ("tiles/solid_soil.png", (TILE_SIZE, TILE_SIZE)),
            "cracked_soil": ("tiles/cracked_soil.png", (TILE_SIZE, TILE_SIZE)),
            "pore_gap": ("tiles/pore_gap.png", (TILE_SIZE, TILE_SIZE)),
            "soft_soil": ("tiles/soft_soil.png", (TILE_SIZE, TILE_SIZE)),
            "hazard": ("tiles/hazard.png", (TILE_SIZE, TILE_SIZE)),
            "exit_node": ("tiles/exit_node.png", (TILE_SIZE, TILE_SIZE)),
            "corpse_overlay": ("tiles/corpse_overlay.png", (TILE_SIZE, TILE_SIZE)),
            "room_0": ("backgrounds/room_01_soil_chamber.png", (1280, 640)),
            "room_1": ("backgrounds/room_02_root_chamber.png", (1280, 640)),
            "room_2": ("backgrounds/room_03_fungal_depths.png", (1280, 640)),
            "win_screen": ("ui/win_screen.png", (1280, 720)),
        }
        for name, (relative_path, size) in specs.items():
            path = ASSET_DIR / relative_path
            if not path.exists():
                self.images[name] = None
                continue
            try:
                image = self.pygame.image.load(str(path)).convert_alpha()
                self.images[name] = self.pygame.transform.smoothscale(image, size)
            except self.pygame.error:
                self.images[name] = None

    def get(self, name):
        return self.images.get(name)
