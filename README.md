# Loamwake

Loamwake is a fixed-room ecological puzzle platformer. The repo now contains two playable builds:

- A Vercel-ready browser version built with static HTML/CSS/Canvas.
- The original local Python/Pygame prototype.

You rotate through three soil hosts by dying, and each death reshapes the room into new terrain that can open the route forward.

## Web Version for Vercel

The web version is what Vercel should deploy. It does not depend on Pygame or a Python server.

```bash
npm install
npm run build
npm run dev
```

Open:

```text
http://127.0.0.1:4173
```

Vercel uses `vercel.json`, runs `npm run build`, and serves the generated `dist/` folder. This prevents Vercel from treating `src/main.py` as a Python serverless function.

## Python/Pygame Version

Use Python 3.11 or newer for the local desktop prototype.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If your Mac does not have a `python` command, use `python3` for the setup commands.

Run:

```bash
python -m src.main
```

## Controls

- Left/right or A/D: move
- Space as Springtail: dash horizontally
- Space as Dung Beetle: high jump
- Down + left/right as Earthworm: dig soft soil
- R: restart the current room
- Escape: quit
- Enter on the win screen: restart from room 1

## Mechanics

- Springtail is fast, can dash, and can pass through pore gaps.
- Dung Beetle is slow, jumps high, and breaks cracked soil by landing on it.
- Earthworm digs soft soil and survives the first two seconds of continuous hazard contact.
- Death rotates hosts in this order: Springtail, Dung Beetle, Earthworm.
- Each death mutates a 3x3 tile area around the death point.
- Three deaths in one room reset that room's terrain while host rotation continues.

## Assets

Images are optional. A Codex-generated reference sheet is included at `assets/ui/generated_asset_sheet.png`. The runtime loader expects individual PNGs in the folders under `assets/` using the names described in `ASSET_GENERATION.md`. Missing images do not crash the game; Loamwake draws readable fallback rectangles using the design palette.

Procedural WAV files are created automatically in `assets/sounds/` when the game or tests touch the audio system.

## Troubleshooting

- If Pygame is missing, run `pip install -r requirements.txt` inside the virtual environment.
- If audio fails on your machine, the game continues silently and prints the audio limitation.
- If `python -m pytest` is unavailable, install the requirements first.

## Checks

```bash
npm run build
npm run test:web
python -m compileall src
python -m pytest
```
