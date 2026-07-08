from dataclasses import dataclass

from .settings import PLAYER_HEIGHT, PLAYER_WIDTH


@dataclass
class Player:
    x: float
    y: float
    velocity_y: float = 0.0
    grounded: bool = False
    facing: int = 1
    dash_cooldown: float = 0.0
    hazard_contact_time: float = 0.0

    def make_rect(self, pygame):
        return pygame.Rect(round(self.x), round(self.y), PLAYER_WIDTH, PLAYER_HEIGHT)

    def reset_to(self, position):
        self.x, self.y = position
        self.velocity_y = 0.0
        self.grounded = False
        self.hazard_contact_time = 0.0
