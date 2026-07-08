import math
import wave
from array import array

from .settings import ASSET_DIR

SOUND_SPECS = {
    "dash": (740, 0.08),
    "jump": (180, 0.11),
    "dig": (120, 0.13),
    "crack": (95, 0.12),
    "death": (70, 0.22),
    "morph": (155, 0.28),
    "exit": (520, 0.16),
    "win": (392, 0.45),
}


def ensure_sound_files():
    """Create tiny procedural WAV files so audio assets exist without downloads."""
    sound_dir = ASSET_DIR / "sounds"
    sound_dir.mkdir(parents=True, exist_ok=True)
    for name, (frequency, duration) in SOUND_SPECS.items():
        path = sound_dir / f"{name}.wav"
        if path.exists():
            continue
        samples = array("h")
        sample_rate = 22050
        count = int(sample_rate * duration)
        for index in range(count):
            fade = 1.0 - (index / max(1, count))
            value = int(11000 * fade * math.sin(2 * math.pi * frequency * index / sample_rate))
            samples.append(value)
        with wave.open(str(path), "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(sample_rate)
            file.writeframes(samples.tobytes())


class AudioManager:
    def __init__(self, pygame):
        self.pygame = pygame
        self.enabled = False
        self.sounds = {}

    def load(self):
        ensure_sound_files()
        try:
            if not self.pygame.mixer.get_init():
                self.pygame.mixer.init()
            self.enabled = True
        except self.pygame.error as error:
            print(f"Audio unavailable, continuing silently: {error}")
            return
        for name in SOUND_SPECS:
            path = ASSET_DIR / "sounds" / f"{name}.wav"
            try:
                self.sounds[name] = self.pygame.mixer.Sound(str(path))
            except self.pygame.error:
                self.sounds[name] = None

    def play(self, name):
        sound = self.sounds.get(name)
        if self.enabled and sound:
            sound.play()
