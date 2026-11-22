# 0007. Use the Noir Or palette

Status: Proposed, 2026-11-22

Derived from: [first principles](../first-principles.md) §7 Colour

## Context

The card has four visible materials and one light: the front mask, the ENIG gold, the back skin, the engraving, and the LED glow. I compared five palettes on six layouts in [card-studio.html](../explorations/card-studio.html): Noir Or, Midnight, Graphite, Ivoire and Kapton.

What I learned doing it: gold only looks rich next to warm neutrals; next to blue-black or blue-white it looks brassy. Cold light (blue, white, green) next to warm metal looks cheap. More than one glow colour starts to look like a gadget.

## Decision

Noir Or: warm matte black mask, ENIG, smoked black matte polycarbonate skin, warm grey foamed engraving, and gold-coloured light. The gold is the only gloss on the card.

## Consequences

- Monochrome gold on black: the light matches the metal, so the card reads as one material.
- All of it is standard: matte black LPI mask and smoked PC skins are stock items.
- Gold light needs a 586 nm yellow LED, which doesn't light from the 1.8 V rail. That's [0008](0008-raise-the-rail-to-2v0-for-gold-leds.md).
- The white colorway from the plan becomes Ivoire: warm white, with amber light, since gold light is too weak on a light skin.
