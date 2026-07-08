# ASSET_GENERATION.md

## Purpose

Use this file if Codex image generation is available. Generate a compact asset pack for Loamwake.

Do not let asset generation block the playable MVP. If image generation fails, keep rectangle fallbacks and finish the game.

## Global Asset Style

All generated images should match this style:

```text
A readable 2D game asset style for a fixed-room ecological puzzle platformer set in soil. Hand-painted soil cross-section diorama, chunky readable shapes, warm loam browns, roots, fungal threads, tiny underground life, clean silhouette, no gore, no text, no watermark, no UI mockup, transparent background for sprites and tiles.
```

## Required Assets

```text
assets/
├── backgrounds/
│   ├── room_01_soil_chamber.png
│   ├── room_02_root_chamber.png
│   └── room_03_fungal_depths.png
├── hosts/
│   ├── springtail.png
│   ├── beetle.png
│   └── earthworm.png
├── tiles/
│   ├── solid_soil.png
│   ├── cracked_soil.png
│   ├── pore_gap.png
│   ├── soft_soil.png
│   ├── hazard.png
│   ├── exit_node.png
│   └── corpse_overlay.png
├── ui/
│   ├── springtail_portrait.png
│   ├── beetle_portrait.png
│   ├── earthworm_portrait.png
│   └── win_screen.png
└── sounds/
```

## Background Prompts

### `assets/backgrounds/room_01_soil_chamber.png`

```text
1280x640 background for a 2D fixed-room soil puzzle platformer. Underground soil cross-section chamber, compacted loam, small pebbles, thin roots, tiny pore tunnels, warm brown palette, hand-painted readable diorama, subtle depth, no text, no characters, no UI, no watermark.
```

### `assets/backgrounds/room_02_root_chamber.png`

```text
1280x640 background for a 2D fixed-room soil puzzle platformer. Underground chamber with larger roots crossing through loam, mycelium threads, compacted soil shelves, gentle amber highlights, hand-painted game background, readable but not busy, no text, no characters, no UI, no watermark.
```

### `assets/backgrounds/room_03_fungal_depths.png`

```text
1280x640 background for a 2D fixed-room soil puzzle platformer. Deeper underground fungal soil chamber, dark loam, glowing mycelium strands, green fungal pockets, root fragments, hand-painted diorama style, readable gameplay backdrop, no text, no characters, no UI, no watermark.
```

## Host Sprite Prompts

Sprites should be transparent PNGs if possible. They must read clearly at about 40x52 pixels in game.

### `assets/hosts/springtail.png`

```text
Transparent PNG sprite, small cyan springtail soil arthropod for a 2D puzzle platformer, side view, clean silhouette, cute but natural, bright cyan body, tiny legs, spring tail hint, no background, no text, no watermark.
```

### `assets/hosts/beetle.png`

```text
Transparent PNG sprite, small brown dung beetle for a 2D puzzle platformer, side view, sturdy rounded body, readable legs, earthen brown shell, strong compact silhouette, no background, no text, no watermark.
```

### `assets/hosts/earthworm.png`

```text
Transparent PNG sprite, small pink earthworm for a 2D puzzle platformer, side view, simple segmented body, readable head direction, soft pink and rose tones, clean silhouette, no background, no text, no watermark.
```

## Tile Sprite Prompts

Tiles should work at 64x64.

### `assets/tiles/solid_soil.png`

```text
64x64 tileable game tile, compact solid soil block, dark loam brown, chunky clods, readable edges, hand-painted 2D game asset, no text, no watermark.
```

### `assets/tiles/cracked_soil.png`

```text
64x64 tileable game tile, cracked tan soil block, visible fracture lines, brittle dry clod texture, readable for breakable platform, hand-painted 2D game asset, no text, no watermark.
```

### `assets/tiles/pore_gap.png`

```text
64x64 game tile, pale porous tunnel gap through soil, light gray hollow pore shape, readable pass-through passage, hand-painted 2D asset, no text, no watermark.
```

### `assets/tiles/soft_soil.png`

```text
64x64 tileable game tile, soft diggable soil, loose crumbly dark brown earth with subtle rose undertone, readable as diggable, hand-painted 2D game asset, no text, no watermark.
```

### `assets/tiles/hazard.png`

```text
64x64 game tile, fungal hazard patch in soil, green mold bloom and small spores, clearly dangerous but not gory, readable 2D game asset, no text, no watermark.
```

### `assets/tiles/exit_node.png`

```text
64x64 game tile, glowing mycelium root node exit, warm yellow fungal light, circular organic doorway symbol, readable goal tile, hand-painted 2D game asset, no text, no watermark.
```

### `assets/tiles/corpse_overlay.png`

```text
64x64 transparent overlay game asset, subtle soil memory mark, organic ring and spores, warm mycelium glow, used where a creature death reshaped terrain, no gore, no text, no watermark.
```

## UI Portrait Prompts

### `assets/ui/springtail_portrait.png`

```text
128x128 portrait icon of a cyan springtail creature, soil game UI style, clean readable face/body, hand-painted, transparent or simple dark loam background, no text, no watermark.
```

### `assets/ui/beetle_portrait.png`

```text
128x128 portrait icon of a brown dung beetle creature, soil game UI style, compact sturdy shape, hand-painted, transparent or simple dark loam background, no text, no watermark.
```

### `assets/ui/earthworm_portrait.png`

```text
128x128 portrait icon of a pink earthworm creature, soil game UI style, soft segmented body, hand-painted, transparent or simple dark loam background, no text, no watermark.
```

### `assets/ui/win_screen.png`

```text
1280x720 win screen illustration for a soil restoration puzzle game. Underground soil chamber restored with healthy roots, glowing mycelium, tiny soil life, warm hopeful loam colors, hand-painted diorama style, no text, no watermark.
```

## Asset Implementation Rules

- Resize images in code to fit game dimensions.
- Collision must always use the tile grid, never pixel-perfect image collision.
- Missing assets must not crash the game.
- If an asset is missing, draw fallback rectangles using `DESIGN.md` palette.
- Keep generated files in `/assets`; do not scatter them through source code.
