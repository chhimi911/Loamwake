# Loamwake Codex Handoff

This package tells Codex to build the full playable game in one continuous run.

## What Loamwake Is

**Loamwake** is a fixed-room ecological puzzle platformer made in Python 3.11 with Pygame.

The player cycles through three soil creatures by dying:

1. Springtail
2. Dung Beetle
3. Earthworm

Death is not just failure. Death reshapes the room and creates the path for the next creature.

## What Changed From the Earlier Direction

This is **not** a side-scrolling platformer.

It keeps the original mechanics, but changes the format into a **single-screen / fixed-room puzzle platformer** with illustrated soil chambers.

Codex should build the entire thing without stopping for approval.

## Files Included

```text
loamwake-codex-handoff/
├── README_START_HERE.md
├── spec.md
├── DESIGN.md
├── ASSET_GENERATION.md
├── AGENTS.md
├── TASKS.md
├── CODEX_PROMPT.md
└── .env.example
```

## How to Use with Codex Desktop

1. Download this zip.
2. Unzip it.
3. Open the folder in Codex Desktop.
4. Open `CODEX_PROMPT.md`.
5. Paste the contents into Codex.
6. Let Codex build the full game in one run.

## What Not To Do Yet

Do not set up GitHub first.

Do not ask Codex to polish the art before the game works.

Do not add enemies, upgrades, procedural maps, save files, or complex animation until the MVP is playable.

## One Next Action

Open `CODEX_PROMPT.md` and paste it into Codex.
