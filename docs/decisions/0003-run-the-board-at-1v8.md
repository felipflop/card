# 0003. Run the board from a 1.8 V rail

Status: Accepted, 2026-11-22

Derived from: [first principles](../first-principles.md) §4 Energy (voltage window)

## Context

The tag's VCC absolute maximum is 2.0 V (datasheet Rev 3.2, Table 273), and its VCC has to be powered for I2C to work. Its harvest output offers 1.8 V or 2.0 V targets. The datasheet also says to avoid holding VCC between 1.55 and 1.62 V. The MSPM0C1104 runs from 1.62 V to 3.6 V.

## Decision

One 1.8 V rail from GPIO1 feeds the tag's VCC, the MCU and the LEDs, with 100 nF at the tag and 10 µF at the MCU as the datasheets ask.

## Consequences

- No regulator or level shifting anywhere.
- Only red LEDs light directly. Red AlGaInP is specified at 1.8 V for 1 mA, so in practice the LEDs run at a few hundred µA and PWM sets brightness.
- During the fade-out the rail passes through the 1.55–1.62 V zone the tag dislikes. The field is gone by then, so a tag reset there does no harm.
- [0008](0008-raise-the-rail-to-2v0-for-gold-leds.md) proposes moving the MCU and LEDs to 2.0 V to fit gold LEDs.
