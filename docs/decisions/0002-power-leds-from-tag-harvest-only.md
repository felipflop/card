# 0002. Power the LEDs from the tag's harvest output only

Status: Accepted, 2026-11-22

Derived from: [first principles](../first-principles.md) §4 Energy

## Context

The NTAG X DNA can output harvested power on GPIO1, but it comes up disabled after every power-on reset. It only turns on when the reader sends a ManageGPIO SET command (datasheet Rev 3.2, section 6.14). A phone doing a plain NDEF read, which is what an iPhone does in the background, never sends that command.

The alternatives were a second coil with its own rectifier, which costs coil area, couples with the main coil and may cut read range, or a DNP footprint for one.

## Decision

Use the tag's harvest output as the only power source. The App Clip and an Android page send ManageGPIO SET to light the LEDs; a plain tap still opens the link with a signed URL.

## Consequences

- Best read range and the simplest RF: one coil, tuned once.
- A first tap from an iPhone without the App Clip shows no light. That's the biggest weakness of the card right now.
- Firmware has to set InRushTarget and the backpower bit so the tag keeps talking while it's harvesting.
- Stored energy plus the tag's GPIO2 field notification could light the LEDs on every tap later. That needs storage and a spare MCU pin, so it's a revision 2 question (see the solar notes in research).
