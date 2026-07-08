from dataclasses import dataclass

from .settings import hex_color


@dataclass(frozen=True)
class Host:
    name: str
    speed: float
    color_name: str
    asset_name: str


SPRINGTAIL = Host("Springtail", 8.0, "spring_cyan", "springtail")
DUNG_BEETLE = Host("Dung Beetle", 3.0, "beetle_umber", "beetle")
EARTHWORM = Host("Earthworm", 4.0, "worm_rose", "earthworm")

HOSTS = (SPRINGTAIL, DUNG_BEETLE, EARTHWORM)


def next_host_index(current_index):
    return (current_index + 1) % len(HOSTS)


def host_color(host):
    return hex_color(host.color_name)
