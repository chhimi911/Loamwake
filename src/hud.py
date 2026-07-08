from .settings import GRID_HEIGHT, HUD_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, hex_color


class Hud:
    def __init__(self, pygame):
        self.pygame = pygame
        self.font = pygame.font.SysFont(["Verdana", "Arial"], 22)
        self.small = pygame.font.SysFont(["Consolas"], 14)

    def draw(self, surface, host, deaths, dash_cooldown, hazard_time):
        pygame = self.pygame
        y = GRID_HEIGHT * TILE_SIZE
        pygame.draw.rect(surface, hex_color("deep_loam"), (0, y, SCREEN_WIDTH, HUD_HEIGHT))
        pygame.draw.line(surface, hex_color("root_amber"), (0, y), (SCREEN_WIDTH, y), 2)

        cooldown = "Ready" if dash_cooldown <= 0 else f"{dash_cooldown:.1f}s"
        grace = ""
        if host.name == "Earthworm" and hazard_time > 0:
            grace = f" | hazard grace {max(0, 2.0 - hazard_time):.1f}s"
        text = (
            f"Host: {host.name} | room deaths: {deaths}/3 | dash: {cooldown}{grace}"
        )
        controls = "Move: arrows/A-D | Space: dash/jump | Down+move: worm dig | R: reset room | Esc: quit"

        self._shadow_text(surface, text, (24, y + 12), host)
        self._shadow_text(surface, controls, (24, y + 44), None, small=True)

    def _shadow_text(self, surface, text, position, host, small=False):
        font = self.small if small else self.font
        color = hex_color(host.color_name) if host else hex_color("pore_mist")
        shadow = font.render(text, True, hex_color("deep_loam"))
        label = font.render(text, True, color)
        surface.blit(shadow, (position[0] + 2, position[1] + 2))
        surface.blit(label, position)
