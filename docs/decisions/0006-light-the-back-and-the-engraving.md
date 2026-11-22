# 0006. Light the back skin and the engraving, not the front

Status: Accepted, 2026-11-22

Derived from: [first principles](../first-principles.md) §5 Thickness, §6 Light

## Context

The plan called for reverse-mount LEDs firing through the substrate. Real reverse-mount parts (Kingbright APTR3216SURCK, for example) are 1.05 mm thick and push their lens through a hole in the board, so on 0.11 mm flex they would stand about 0.9 mm proud of the gold front. Side-view LEDs were the other route, but the APA1606 is 1.2 mm tall. I compared eight placements before choosing.

## Decision

All twelve LEDs are ROHM SML-P11VT (red, 1.0 × 0.6 × 0.2 mm, Vf 1.8 V at 1 mA), on the back, in two roles:

- Back glow: some face out through the clear pocket epoxy and the polycarbonate skin.
- Edge-lit engraving: others sit face down in a clear channel routed in the stiffener. About half their light falls outside the critical angle and stays trapped in the epoxy and skin until it reaches the laser-engraved micro-voids, so the engraving itself glows.

Electrically they're identical. The layout decides which LED does which job.

## Consequences

- The gold front stays flat and untouched.
- One LED part number for both effects.
- The engraving has to use the laser setting that leaves light, scattering micro-voids, not the one that darkens the plastic.
- A printed dot under each channel LED hides the direct hotspot.
- The channel route and the epoxy-to-skin bond (index-matched) become layout and process items.
