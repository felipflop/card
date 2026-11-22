# 0004. Ship the MCU in WSON-8 first, keep the WCSP footprint

Status: Accepted, 2026-11-22

Derived from: [first principles](../first-principles.md) §5 Thickness

## Context

The plan called for the MSPM0C1104 in its 8-ball WCSP (YCJ, 0.86 × 1.60 mm, 0.35 mm tall). On 2026-11-21 TI showed it out of stock and sold only on 12,000-piece reels, and LCSC doesn't list it. DigiKey, Mouser, Newark and Arrow blocked automated checks, so they still need a manual look. The other 8-pin packages share the same pinout. The WSON-8 (DSG, 2 × 2 × 0.8 mm) had 3,011 at LCSC.

## Decision

Design around the WSON-8 (MSPM0C1104SDSGR) for prototype 1. The YCJ footprint is in the library with its pads numbered like the WSON (B1=1, B2=2, D2=3 and so on) and the WSON's exposed pad numbered 3 (VSS), so swapping packages is a footprint change with no schematic edit.

## Consequences

- Parts I can actually buy, in a package that's easier to rework.
- 0.8 mm is taller than the 0.43 mm stiffener. The MCU island needs a deeper pocket, or a thicker stiffener locally, or it lives on the rigid build. The tag (up to 0.525 mm) already overshoots too, so pocket depth gets settled at layout either way.
- If TI starts selling the WCSP on a cut or custom reel, moving to it costs nothing in the schematic.
