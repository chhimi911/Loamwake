# AGENTS.md

## Commands

Use these commands for this project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
python -m pytest
python -m compileall src
```

On Windows, activate with:

```bash
.venv\Scripts\activate
```

If `pytest` is unavailable, install from `requirements.txt`. If Pygame audio fails on the local machine, the game should continue without crashing and report the audio limitation.

## Project Mission

Build the complete Loamwake MVP described in `spec.md`: a fixed-room ecological puzzle platformer in Python 3.11 + Pygame with original host mechanics, death rotation, corpse terrain mutation, room progression, sounds, and asset support.

## Read First

Read these files silently:

1. `spec.md`
2. `DESIGN.md`
3. `ASSET_GENERATION.md`
4. `TASKS.md`

Do not print their contents.

## Build Rules

- Build all milestones in one continuous run. Do not stop for user approval between phases.
- This is not a side-scrolling camera game. It is a fixed-room puzzle platformer.
- Keep the original mechanics from `spec.md`.
- Use clearly commented modules.
- Make the code understandable for a non-developer.
- Keep collision grid-based.
- Images are visual only.
- If image generation is available, generate the compact asset pack described in `ASSET_GENERATION.md`.
- If image generation is unavailable or fails, use rectangle fallback art and finish the playable game.
- Do not block the game on art generation.
- Do not invent credentials.
- Do not add cloud services.
- Do not add online features.
- Do not use GitHub unless the user asks later.

## Code Standards

- Prefer simple classes and functions.
- Use readable names.
- Add comments explaining non-obvious gameplay logic.
- Separate modules by responsibility.
- Keep host-specific behavior easy to locate.
- Keep terrain mutation logic testable outside the main game loop.

## Design Rules

Follow `DESIGN.md`.

- Use the exact fallback palette.
- Create the soil memory pulse effect.
- Make tiles readable before making them pretty.
- Use generated images if available.
- Use fallback rectangles when images are missing.
- Keep the HUD readable.
- Do not implement camera scrolling.

## Audio Rules

- Add short sounds for dash, jump, dig, crack, death, morph, exit, and win.
- Use generated/procedural WAV files if no audio assets exist.
- Audio failure must not crash the game.

## Testing Rules

Before finishing, run:

```bash
python -m compileall src
python -m pytest
```

Also manually smoke-test by launching:

```bash
python -m src.main
```

If manual launch cannot be fully tested in the environment, explain what was verified and what the user should check locally.

## Self-Correction

If a check fails:

1. Read the error.
2. Fix the root cause.
3. Re-run the check.
4. Continue until passing or truly blocked.

Do not stop for style questions.

## True Blockers

Stop only if Python or Pygame cannot be installed, or if a required external credential is somehow needed.

## Done Criteria

- Game runs locally with `python -m src.main`.
- Main workflow works end to end.
- Three rooms are present.
- Three hosts work.
- Hazards work.
- Death rotation works.
- Corpse terrain works.
- Three-death room reset works.
- Room progression works.
- Win screen and restart work.
- HUD works.
- Sounds are present or graceful fallback exists.
- Assets load when present.
- Missing assets do not crash the game.
- Tests/checks pass or failures are clearly explained.
- `README.md` is updated with setup, run, controls, and troubleshooting.
- Final report lists files changed and commands run.
