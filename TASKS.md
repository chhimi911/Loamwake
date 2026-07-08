# TASKS.md

## Build Goal

Build Loamwake as a complete, playable local Pygame prototype in one continuous run.

## Phase 1: Setup

- [ ] Inspect the folder.
- [ ] Read required docs silently.
- [ ] Create `requirements.txt`.
- [ ] Create source folder structure.
- [ ] Create tests folder.
- [ ] Create `README.md`.
- [ ] Keep `.env.example`.

## Phase 2: Core Window and Loop

- [ ] Create 1280x720 Pygame window.
- [ ] Target 60 FPS.
- [ ] Add game state management.
- [ ] Add quit handling.
- [ ] Add restart handling.

## Phase 3: Levels and Tiles

- [ ] Add three room grids to `levels.py`.
- [ ] Validate rectangular levels.
- [ ] Parse spawn and exit.
- [ ] Implement tile constants.
- [ ] Render tile grid.
- [ ] Use 64px tiles.
- [ ] Keep HUD area at bottom.

## Phase 4: Assets

- [ ] Create asset folder structure.
- [ ] Add asset loader.
- [ ] Load images when present.
- [ ] Resize assets safely.
- [ ] Use rectangle fallback if image missing.
- [ ] If Codex image generation is available, generate assets from `ASSET_GENERATION.md`.
- [ ] Do not block playable build on assets.

## Phase 5: Hosts and Movement

- [ ] Add host data model.
- [ ] Add fixed rotation: Springtail → Dung Beetle → Earthworm → Springtail.
- [ ] Add Springtail movement.
- [ ] Add Springtail horizontal dash: 300px burst, 1s cooldown.
- [ ] Add Springtail `G` passability.
- [ ] Add Beetle movement.
- [ ] Add Beetle high jump.
- [ ] Add Beetle `C` landing break.
- [ ] Add Earthworm movement.
- [ ] Add Earthworm down + direction tunneling through `S`.
- [ ] Add Earthworm no-jump/no-dash rules.

## Phase 6: Collision and Physics

- [ ] Implement grid-based collision.
- [ ] Keep collision readable and commented.
- [ ] Support host-specific blocking rules.
- [ ] Prevent player from leaving room bounds.
- [ ] Apply gravity where needed.
- [ ] Keep Springtail and Earthworm grounded/no-jump behavior clear.

## Phase 7: Hazards and Death

- [ ] Detect hazard contact.
- [ ] Earthworm has 2 seconds of continuous hazard immunity.
- [ ] Other hosts die on hazard contact.
- [ ] Add death sound.
- [ ] Add respawn at `P`.
- [ ] Rotate host after death.

## Phase 8: Death-Morph Terrain

- [ ] Convert 3x3 tile area centered on death point.
- [ ] Springtail corpse creates empty tiles.
- [ ] Beetle corpse creates solid tiles.
- [ ] Earthworm corpse creates soft soil tiles.
- [ ] Persist corpse terrain within the room.
- [ ] Add soil memory pulse visual.
- [ ] Add morph sound.

## Phase 9: Three-Death Reset

- [ ] Track deaths in current room.
- [ ] At three deaths, reset room terrain to original.
- [ ] Keep host rotation continuing.
- [ ] Reset deaths-in-room to zero.
- [ ] Keep room index unchanged.

## Phase 10: Progression and Win

- [ ] Detect exit contact.
- [ ] Load next room.
- [ ] Reset room death count on room entry.
- [ ] After Room 3, show win screen.
- [ ] Add Enter-to-restart on win screen.
- [ ] Add win sound.

## Phase 11: HUD and UX

- [ ] Show current host name.
- [ ] Show deaths-in-room count.
- [ ] Show basic controls.
- [ ] Show dash cooldown feedback for Springtail.
- [ ] Show Earthworm hazard grace feedback if practical.
- [ ] Keep HUD readable.

## Phase 12: Sounds

- [ ] Generate or create simple WAV files if missing.
- [ ] Add dash, jump, dig, crack, death, morph, exit, and win sounds.
- [ ] Make audio optional/graceful if mixer fails.

## Phase 13: Tests

- [ ] Test level rectangularity.
- [ ] Test one spawn and one exit per level.
- [ ] Test host rotation.
- [ ] Test corpse terrain mutation.
- [ ] Test three-death room reset.
- [ ] Run `python -m compileall src`.
- [ ] Run `python -m pytest`.

## Phase 14: README and Final Report

- [ ] Update `README.md`.
- [ ] Include install steps.
- [ ] Include run command.
- [ ] Include controls.
- [ ] Include troubleshooting.
- [ ] List changed files.
- [ ] List commands run.
- [ ] List known limits.
