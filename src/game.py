from .assets import AssetManager
from .audio import AudioManager
from .hosts import HOSTS, next_host_index, host_color
from .hud import Hud
from .physics import first_tile, rect_hits_blocking_tile, tiles_touched_by_rect
from .player import Player
from .room import Room
from .settings import (
    FPS,
    GRAVITY,
    GRID_HEIGHT,
    GRID_WIDTH,
    MAX_FALL_SPEED,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
    hex_color,
)
from .tiles import CRACKED, EXIT, HAZARD, PORE_GAP, SOFT, TILE_ASSETS


class Game:
    def __init__(self, pygame):
        self.pygame = pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Loamwake")
        self.clock = pygame.time.Clock()
        self.assets = AssetManager(pygame)
        self.assets.load()
        self.audio = AudioManager(pygame)
        self.audio.load()
        self.hud = Hud(pygame)
        self.title_font = pygame.font.SysFont(["Georgia", "Times New Roman"], 54)
        self.win_font = pygame.font.SysFont(["Georgia", "Times New Roman"], 72)
        self.info_font = pygame.font.SysFont(["Verdana", "Arial"], 28)
        self.host_index = 0
        self.room_index = 0
        self.room = Room(self.room_index)
        self.player = Player(*self.room.spawn_position())
        self.win = False
        self.win_sound_played = False

    @property
    def host(self):
        return HOSTS[self.host_index]

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    running = False
                elif event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_ESCAPE:
                        running = False
                    elif self.win and event.key == self.pygame.K_RETURN:
                        self.restart_game()
                    elif not self.win and event.key == self.pygame.K_r:
                        self.restart_room()
                    elif not self.win and event.key == self.pygame.K_SPACE:
                        self.handle_space()

            if not self.win:
                self.update(dt)
                self.draw()
            else:
                self.draw_win()
            self.pygame.display.flip()

    def restart_game(self):
        self.host_index = 0
        self.room_index = 0
        self.room = Room(0)
        self.player.reset_to(self.room.spawn_position())
        self.win = False
        self.win_sound_played = False

    def restart_room(self):
        self.room.reset_terrain()
        self.player.reset_to(self.room.spawn_position())

    def handle_space(self):
        if self.host.name == "Springtail":
            direction = self.player.facing
            if self.player.dash_cooldown <= 0 and direction:
                self.dash(direction)
                self.player.dash_cooldown = 1.0
                self.audio.play("dash")
        elif self.host.name == "Dung Beetle" and self.player.grounded:
            self.player.velocity_y = -20.0
            self.player.grounded = False
            self.audio.play("jump")

    def update(self, dt):
        self.room.update_pulses(dt)
        self.player.dash_cooldown = max(0.0, self.player.dash_cooldown - dt)
        keys = self.pygame.key.get_pressed()
        direction = self.input_direction(keys)
        if direction:
            self.player.facing = direction

        if self.host.name == "Earthworm" and keys[self.pygame.K_DOWN]:
            self.worm_dig(direction)

        self.move_horizontal(direction * self.host.speed)
        self.apply_vertical_motion()
        self.resolve_hazards(dt)
        self.check_exit()

    def input_direction(self, keys):
        left = keys[self.pygame.K_LEFT] or keys[self.pygame.K_a]
        right = keys[self.pygame.K_RIGHT] or keys[self.pygame.K_d]
        if left and not right:
            return -1
        if right and not left:
            return 1
        return 0

    def move_horizontal(self, amount):
        if amount == 0:
            return
        self.player.x += amount
        if rect_hits_blocking_tile(self.player.make_rect(self.pygame), self.room, self.host.name):
            step = -1 if amount > 0 else 1
            while rect_hits_blocking_tile(self.player.make_rect(self.pygame), self.room, self.host.name):
                self.player.x += step

    def apply_vertical_motion(self):
        self.player.velocity_y = min(MAX_FALL_SPEED, self.player.velocity_y + GRAVITY)
        self.player.y += self.player.velocity_y
        rect = self.player.make_rect(self.pygame)
        if rect_hits_blocking_tile(rect, self.room, self.host.name):
            moving_down = self.player.velocity_y >= 0
            step = -1 if moving_down else 1
            while rect_hits_blocking_tile(self.player.make_rect(self.pygame), self.room, self.host.name):
                self.player.y += step
            if moving_down:
                self.break_cracked_tiles_underfoot()
            self.player.velocity_y = 0.0
            self.player.grounded = moving_down
        else:
            self.player.grounded = False

    def dash(self, direction):
        distance = 300
        step = 12 * direction
        moved = 0
        while abs(moved) < distance:
            self.player.x += step
            moved += step
            if rect_hits_blocking_tile(self.player.make_rect(self.pygame), self.room, self.host.name):
                self.player.x -= step
                break

    def worm_dig(self, direction):
        rect = self.player.make_rect(self.pygame)
        targets = []
        if direction < 0:
            targets.append((rect.left - 2, rect.centery))
        elif direction > 0:
            targets.append((rect.right + 2, rect.centery))
        targets.append((rect.centerx, rect.bottom + 2))
        dug = False
        for x, y in targets:
            point = self.room.world_to_tile(x, y)
            dug = self.room.dig_soft_tile(point.col, point.row) or dug
        if dug:
            self.audio.play("dig")

    def break_cracked_tiles_underfoot(self):
        if self.host.name != "Dung Beetle":
            return
        rect = self.player.make_rect(self.pygame)
        probe = self.pygame.Rect(rect.left + 2, rect.bottom, rect.width - 4, 4)
        broke = False
        for col, row in tiles_touched_by_rect(probe):
            if self.room.tile_at(col, row) == CRACKED:
                self.room.set_tile(col, row, ".")
                broke = True
        if broke:
            self.audio.play("crack")

    def resolve_hazards(self, dt):
        rect = self.player.make_rect(self.pygame)
        touching_hazard = first_tile(rect, self.room, lambda tile: tile == HAZARD)
        if not touching_hazard:
            self.player.hazard_contact_time = 0.0
            return
        if self.host.name == "Earthworm":
            self.player.hazard_contact_time += dt
            if self.player.hazard_contact_time < 2.0:
                return
        self.kill_player()

    def kill_player(self):
        rect = self.player.make_rect(self.pygame)
        self.audio.play("death")
        reset = self.room.record_death(self.host.name, rect.centerx, rect.centery)
        self.audio.play("morph")
        self.host_index = next_host_index(self.host_index)
        if reset:
            self.player.reset_to(self.room.spawn_position())
        else:
            self.player.reset_to(self.room.spawn_position())

    def check_exit(self):
        rect = self.player.make_rect(self.pygame)
        if not first_tile(rect, self.room, lambda tile: tile == EXIT):
            return
        self.audio.play("exit")
        self.room_index += 1
        if self.room_index >= 3:
            self.win = True
            if not self.win_sound_played:
                self.audio.play("win")
                self.win_sound_played = True
            return
        self.room = Room(self.room_index)
        self.player.reset_to(self.room.spawn_position())

    def draw(self):
        self.draw_background()
        self.draw_tiles()
        self.draw_pulses()
        self.draw_player()
        self.hud.draw(
            self.screen,
            self.host,
            self.room.deaths_in_room,
            self.player.dash_cooldown,
            self.player.hazard_contact_time,
        )

    def draw_background(self):
        image = self.assets.get(f"room_{self.room_index}")
        if image:
            self.screen.blit(image, (0, 0))
        else:
            self.screen.fill(hex_color("deep_loam"))
            self.draw_root_lines()

    def draw_root_lines(self):
        pygame = self.pygame
        color = hex_color("root_amber")
        for offset in (80, 230, 490, 760, 1010):
            pygame.draw.line(self.screen, color, (offset, 0), (offset + 160, GRID_HEIGHT * TILE_SIZE), 2)

    def draw_tiles(self):
        pygame = self.pygame
        for row, values in enumerate(self.room.grid):
            for col, tile in enumerate(values):
                if tile in (".", "P"):
                    continue
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                asset_name = TILE_ASSETS.get(tile)
                image = self.assets.get(asset_name) if asset_name else None
                if image:
                    self.screen.blit(image, rect)
                else:
                    self.draw_fallback_tile(tile, rect)

    def draw_fallback_tile(self, tile, rect):
        pygame = self.pygame
        if tile == "X":
            pygame.draw.rect(self.screen, hex_color("beetle_umber"), rect)
            pygame.draw.rect(self.screen, hex_color("deep_loam"), rect, 2)
        elif tile == CRACKED:
            pygame.draw.rect(self.screen, hex_color("root_amber"), rect)
            pygame.draw.line(self.screen, hex_color("deep_loam"), rect.topleft, rect.bottomright, 3)
            pygame.draw.line(self.screen, hex_color("deep_loam"), rect.midtop, rect.midleft, 2)
        elif tile == PORE_GAP:
            pygame.draw.rect(self.screen, hex_color("pore_mist"), rect)
            pygame.draw.ellipse(self.screen, hex_color("deep_loam"), rect.inflate(-16, -22))
        elif tile == SOFT:
            pygame.draw.rect(self.screen, hex_color("deep_loam"), rect)
            pygame.draw.circle(self.screen, hex_color("worm_rose"), rect.center, 16, 2)
        elif tile == HAZARD:
            pygame.draw.rect(self.screen, hex_color("deep_loam"), rect)
            pygame.draw.circle(self.screen, hex_color("fungal_green"), rect.center, 22)
            pygame.draw.circle(self.screen, hex_color("pore_mist"), rect.center, 7)
        elif tile == EXIT:
            pulse = 5 + int(4 * abs(self.pygame.time.get_ticks() % 800 - 400) / 400)
            pygame.draw.rect(self.screen, hex_color("deep_loam"), rect)
            pygame.draw.circle(self.screen, hex_color("mycelium_glow"), rect.center, 19 + pulse, 3)
            pygame.draw.circle(self.screen, hex_color("mycelium_glow"), rect.center, 10)

    def draw_pulses(self):
        pygame = self.pygame
        for pulse in self.room.pulses:
            age = pulse["age"]
            radius = int(20 + age * 180)
            alpha = max(0, int(190 * (1.0 - age / 0.5)))
            layer = pygame.Surface((SCREEN_WIDTH, GRID_HEIGHT * TILE_SIZE), pygame.SRCALPHA)
            color = (*hex_color("mycelium_glow"), alpha)
            pygame.draw.circle(layer, color, (int(pulse["x"]), int(pulse["y"])), radius, 3)
            self.screen.blit(layer, (0, 0))

    def draw_player(self):
        rect = self.player.make_rect(self.pygame)
        image = self.assets.get(self.host.asset_name)
        if image:
            self.screen.blit(image, image.get_rect(center=rect.center))
        else:
            self.pygame.draw.rect(self.screen, host_color(self.host), rect, border_radius=8)
            self.pygame.draw.rect(self.screen, hex_color("deep_loam"), rect, 2, border_radius=8)

    def draw_win(self):
        image = self.assets.get("win_screen")
        if image:
            self.screen.blit(image, (0, 0))
        else:
            self.screen.fill(hex_color("deep_loam"))
            self.draw_root_lines()
        overlay = self.pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), self.pygame.SRCALPHA)
        overlay.fill((42, 27, 18, 155))
        self.screen.blit(overlay, (0, 0))
        self.center_text("You restored the soil.", self.win_font, hex_color("mycelium_glow"), 278)
        self.center_text("Press Enter to restart", self.info_font, hex_color("pore_mist"), 370)

    def center_text(self, text, font, color, y):
        label = font.render(text, True, color)
        shadow = font.render(text, True, hex_color("deep_loam"))
        x = (SCREEN_WIDTH - label.get_width()) // 2
        self.screen.blit(shadow, (x + 3, y + 3))
        self.screen.blit(label, (x, y))
