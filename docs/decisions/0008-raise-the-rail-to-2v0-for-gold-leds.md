# 0008. Raise the LED rail to 2.0 V for gold LEDs

Status: Proposed, 2026-11-22

Derived from: [first principles](../first-principles.md) §4 Energy, §6 Light

## Context

[0007](0007-use-the-noir-or-palette.md) wants light that matches the ENIG. The closest LED is the ROHM SML-P11YT (586 nm, same 0.2 mm package as the red), which needs 1.9 V at 1 mA. It's also about twice as efficient as the red for the same perceived brightness (7.6 vs 4.0 mcd at 1 mA). The rail is 1.8 V ([0003](0003-run-the-board-at-1v8.md)).

Two ways up:

1. Set the tag's harvest output to its 2.0 V target (datasheet Rev 3.2, Table 24, DefaultTarget 0x11–0x1F). Run the MCU and LEDs from 2.0 V, and feed the tag's own VCC through a small Schottky so it sees about 1.75–1.85 V.
2. Add a charge pump: two capacitors, a diode and one MCU pin, which needs the 20-pin MCU package.

## Decision

Proposed: option 1 for prototype 1, option 2 for revision 2.

## Consequences

- One diode and a firmware setting; no new pins.
- Only about 0.1 V of headroom, so the yellow runs at a few hundred µA. Visible, but dim until the charge pump arrives.
- I2C pull-ups stay on the tag's VCC side. The MCU's I2C pins are open-drain and read 1.8 V levels fine from a 2.0 V supply.
- Before ordering, I have to check the diode's drop keeps the tag's VCC above 1.62 V at its lowest current.
