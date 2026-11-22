# 2026-11-22: Schematic, sourcing, and a lot of reading

## Sourcing

Checked stock for the two chips. The MSPM0C1104 WCSP (S8YCJR) is out of stock at TI and only sold on 12k reels; LCSC carries every other package. DigiKey, Mouser, Newark and Arrow all refused automated lookups, so those still need a manual look. Notes in [research/sourcing-2026-11.md](../research/sourcing-2026-11.md). Result: [0004](../decisions/0004-ship-the-mcu-in-wson-first.md).

## What the datasheets changed

Reading the NTAG X DNA datasheet properly turned up three things the plan had missed:

- VCC absolute max is 2.0 V, so the whole board has to live in a narrow window ([0003](../decisions/0003-run-the-board-at-1v8.md)).
- Harvesting stays off until the reader sends ManageGPIO SET. A plain iPhone tap never does ([0002](../decisions/0002-power-leds-from-tag-harvest-only.md)).
- Input capacitance is 18.4 pF typical, not 17 pF, which detunes the coil I generated yesterday.

On the MCU side, PA0 and PA1 are open-drain only, so they can only be the I2C pins, and PA1 doubles as NRST. That leaves four push-pull pins, which became a 12-LED charlieplex once I dropped the ADC divider ([0005](../decisions/0005-measure-the-field-without-a-divider.md)).

## LEDs

Reverse-mount LEDs turned out to be 1.05 mm thick and need a hole through the board, which would have put bumps on the gold front. I built [led-options.html](../explorations/led-options.html) to compare eight placements and went with back glow plus an edge-lit engraving, both using the 0.2 mm ROHM SML-P11VT ([0006](../decisions/0006-light-the-back-and-the-engraving.md)).

## Schematic

Hierarchical KiCad 10 project in `hardware/`: a root sheet, `nfc` (coil, trim cap, tag, fade bank) and `mcu_leds` (MCU, pull-ups, LED matrix, test pads). All symbols and footprints are in the project library, drawn from the vendor package drawings:

| Footprint | Source |
|---|---|
| NXP WLCSP-16, 0.35 mm | SOT2127-1 outline and reflow footprint (NSMD Ø0.20, mask Ø0.27, paste Ø0.23) |
| TI WSON-8 DSG | DSG0008A land pattern and stencil |
| TI DSBGA-8 YCJ | YCJ0008-C01, SMD pads Ø0.255 under Ø0.18 mask |
| ROHM PICOLED 1006 | SML-P11x land pattern, 0.6 × 0.5 mm pads |

ERC: 0 errors, 0 warnings. The netlist checks out: each LED line carries three anodes and three cathodes, all eight tag VSS balls reach GND, and I2C crosses between the sheets.

An automated schematic review flagged one error, too few MPNs on the BOM, which I fixed. Three of the passive MPNs are confirmed in LCSC's catalogue; the 22 µF bank and the 01005 resistors still need a live check.

## Still open

- LED polarity: ROHM's cathode mark is ambiguous on the drawing. Check on the first assembled board.
- The eval board guide (UG10083) wouldn't download, so the reference capacitor values on VCC and GPIO1 are unconfirmed.
- The three problems in [first principles](../first-principles.md#open-problems-found-here): coil tuning, fade length, and thickness.

## Exploration

Spent the rest of the day on what the card could become. The research is in [research/](../research/), and the two pages I built to think it through are [beyond-the-tap.html](../explorations/beyond-the-tap.html) (19 passive features, ranked) and [card-studio.html](../explorations/card-studio.html) (six layouts, five palettes, LED colours). The palette and the gold LED are proposed in [0007](../decisions/0007-use-the-noir-or-palette.md) and [0008](../decisions/0008-raise-the-rail-to-2v0-for-gold-leds.md).
