EMPTY = "."
SOLID = "X"
CRACKED = "C"
PORE_GAP = "G"
SOFT = "S"
HAZARD = "H"
SPAWN = "P"
EXIT = "E"

MUTABLE_TILES = {EMPTY, SOLID, CRACKED, PORE_GAP, SOFT, HAZARD}

TILE_ASSETS = {
    SOLID: "solid_soil",
    CRACKED: "cracked_soil",
    PORE_GAP: "pore_gap",
    SOFT: "soft_soil",
    HAZARD: "hazard",
    EXIT: "exit_node",
}


def blocks_host(tile, host_name):
    """Return whether a tile blocks the named host's collision box."""
    if tile in (EMPTY, SPAWN, EXIT, HAZARD):
        return False
    if tile == PORE_GAP:
        return host_name != "Springtail"
    return tile in {SOLID, CRACKED, SOFT}


def death_tile_for(host_name):
    if host_name == "Springtail":
        return EMPTY
    if host_name == "Dung Beetle":
        return SOLID
    if host_name == "Earthworm":
        return SOFT
    raise ValueError(f"Unknown host: {host_name}")
