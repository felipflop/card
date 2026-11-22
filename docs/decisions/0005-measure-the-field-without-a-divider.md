# 0005. Measure field strength with the internal supply monitor, no divider

Status: Accepted, 2026-11-22

Derived from: [first principles](../first-principles.md) §4 Energy

## Context

The original plan had a resistor divider into the ADC for a field-strength meter. But the harvest output holds its 1.8 V target until the field can't keep up, so a divider on the rail would read a flat 1.8 V almost all the time. Sampling the antenna directly needs a diode, and the low-capacitance Schottky I looked at (BAT24-02LS) is rated for only 4 V reverse, about what the antenna swings to. The MSPM0C1104 also has an internal VDD/3 supply-monitor channel. Every MCU pin is already in use.

## Decision

No divider. Firmware raises the LED duty until VDD, read on the internal supply monitor, starts to sag. The duty where it sags tracks how much power the field delivers.

## Consequences

- No parts, no extra load on the antenna, and the freed pin becomes a fourth charlieplex line: 12 LEDs instead of 6.
- The reading is relative, not calibrated in A/m. That's fine for a light show and for "move the phone here" guidance.
- It needs firmware tuning on real phones.
