# DESIGN.md

## Design Direction

Loamwake should feel like a playable soil cross-section diorama: compacted earth, root veins, pore tunnels, fungal hazard growth, and small creatures moving through a living underground chamber.

## Banned Defaults

Do not use:

- Generic arcade tile look
- Default Pygame primary colors except fallback debugging rectangles
- Neon cyberpunk palette
- Space, cave, dungeon, or fantasy castle visuals
- Smooth plastic UI
- Purple gradient effects
- Random stock platformer sprites
- Art where the tiles are hard to read

If the game could be reskinned as a generic platformer without changing layout, it is wrong.

## Typography

Pygame does not need web fonts.

Use built-in system fonts by fallback priority:

- Display/UI title face: `Georgia`, fallback `Times New Roman`, fallback Pygame default
- HUD/body face: `Verdana`, fallback `Arial`, fallback Pygame default
- Utility/mono face: `Consolas`, fallback Pygame default

Type sizes:

- Tiny: 14px
- HUD: 22px
- Label: 28px
- Title: 54px
- Win title: 72px

Use title font only for game title and win message. Use HUD/body font for everything else.

## Color Palette

Use these exact colors for fallback rectangles, HUD, overlays, and generated-asset color guidance.

| Name | Hex | Use |
|---|---|---|
| Deep Loam | `#2A1B12` | background soil darkness, primary dark text shadow |
| Root Amber | `#C8843A` | cracked soil, warm highlights |
| Mycelium Glow | `#E8D98A` | exit node, win glow, focus highlights |
| Pore Mist | `#BFC7C2` | pore gaps, light tunnel edges |
| Spring Cyan | `#33D6D2` | Springtail fallback and UI accent |
| Beetle Umber | `#6B3F1D` | Dung Beetle fallback and solid earth |
| Worm Rose | `#D978A0` | Earthworm fallback and soft-body UI |
| Fungal Green | `#4F8A3D` | hazards |

Do not introduce additional UI colors unless needed for alpha overlays. Every fallback gameplay element must use this palette.

## Tile Visual Rules

- Solid soil: dark chunky clods using Deep Loam and Beetle Umber.
- Cracked soil: Root Amber with visible fractures.
- Pore gap: pale Pore Mist tunnel with hollow center.
- Soft soil: darker loose crumb texture with Worm Rose undertone.
- Hazard: Fungal Green mold bloom, spores, or toxic patch.
- Exit: Mycelium Glow root node or fungal gate.

## Signature Element

Each death triggers a **soil memory pulse**: a quick expanding ring at the death point, then the 3x3 corpse terrain appears with a visible overlay for 500ms.

This is the one memorable visual effect. Keep other effects restrained.

## Layout and Spacing

- Window: 1280x720.
- Grid: 20 columns x 10 rows.
- Tile size: 64px.
- Grid area: 1280x640.
- HUD area: bottom 80px.
- HUD padding: 24px.
- UI spacing scale: 8 / 16 / 24 / 40px.
- Borders: 2px where needed.
- Radius: 0px for tiles; 8px for UI panels.
- Shadows: text shadow only, no soft-card UI.

## Motion

- 60 FPS target.
- Allowed: Springtail dash streak, Beetle landing shake, Earthworm digging dust, death soil memory pulse, exit glow pulse.
- Not allowed: camera scrolling, parallax, long cinematic transitions, or busy particles that obscure tiles.

## Sound Direction

Use short, readable sounds:

- Springtail dash: dry snap.
- Beetle jump/landing: low thud.
- Dig: soft granular scrape.
- Crack: brittle crumble.
- Death: muted soil pulse.
- Morph: low organic bloom.
- Exit: warm fungal chime.
- Win: short restored-soil chord.

If real/generated audio is unavailable, create simple procedural `.wav` tones.

## Done Criteria for Design

- The game reads as an underground soil chamber.
- All gameplay tiles are visually distinguishable.
- Fallback rectangles use the palette above.
- Image assets load when present.
- Missing assets do not crash the game.
- Soil memory pulse exists.
- HUD is readable at 1280x720.
