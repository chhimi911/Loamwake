# CODEX_PROMPT.md

## Goal

Build the full Loamwake MVP: a complete, playable fixed-room ecological puzzle platformer in Python 3.11 with Pygame, original three-host mechanics, death rotation, corpse terrain mutation, room progression, sounds, and Codex-generated or fallback visual assets.

## Context

- Inspect this folder first.
- Read `AGENTS.md`, `spec.md`, `DESIGN.md`, `ASSET_GENERATION.md`, and `TASKS.md` silently.
- Do not print their contents.
- `AGENTS.md` is the operating authority.
- `spec.md` defines the game.
- `DESIGN.md` defines the visual direction.
- `ASSET_GENERATION.md` defines generated asset prompts.
- `TASKS.md` defines the build order.

## Constraints

- Build all phases in one continuous run. Do not stop for approval between milestones.
- This is not a side-scrolling camera game. Build a fixed-room puzzle platformer.
- Keep the original mechanics:
  - Springtail dash and pore-gap passability.
  - Dung Beetle high jump and cracked-tile break.
  - Earthworm tunneling and hazard grace.
  - Death-only host rotation.
  - 3x3 corpse terrain mutation.
  - Three-death room reset.
- Use Python 3.11 and Pygame.
- Use clearly commented modules.
- Make the game run locally.
- Collision must be tile-grid based.
- Images are visual only.
- If image generation is available, generate the compact Loamwake asset pack from `ASSET_GENERATION.md`.
- If image generation is unavailable or fails, use fallback rectangles and finish the playable game.
- Do not block gameplay on art generation.
- Do not invent credentials.
- Do not add cloud services.
- Do not add GitHub steps.
- Do not modify `spec.md`, `DESIGN.md`, `ASSET_GENERATION.md`, `AGENTS.md`, `TASKS.md`, or `CODEX_PROMPT.md` unless fixing a clear typo that blocks the build.
- If a command fails, read the error, fix the root cause, re-run, and continue until passing or truly blocked.
- Keep progress updates brief. Do not print full logs or full instruction files.

## Done when

- The game runs locally with:

```bash
python -m src.main
```

- All three rooms are playable.
- Springtail, Dung Beetle, and Earthworm work with their distinct mechanics.
- Hazards, death rotation, corpse terrain, room reset, room progression, HUD, sounds, and win screen work.
- Asset images are generated/loaded if possible, and fallback rectangles work if assets are missing.
- Available checks pass:

```bash
python -m compileall src
python -m pytest
```

- `README.md` includes setup, run command, controls, and troubleshooting.
- `.env.example` exists.
- Final report is delivered in this format:

### Build Summary
### Files Changed
### Commands Run
### Checks: Passed / Failed
### Known Limits
### Next Recommended Step
