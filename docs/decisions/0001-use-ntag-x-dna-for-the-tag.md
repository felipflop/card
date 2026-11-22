# 0001. Use the NTAG X DNA in WLCSP for the tag

Status: Accepted, 2026-11-21

Derived from: [first principles](../first-principles.md) §1 What the card has to do, §3 Proving a tap is genuine, §8 Fine pitch

## Context

The card has to open a link on any phone, iPhones included, without an app. It should also prove each tap is genuine, power a small MCU, and be as thin as possible. That means ISO 14443-A with NDEF, some form of signed tap, an energy harvesting output, and an I2C link to the MCU.

The single-chip option, the NHS3152 (tag and Cortex-M0+ in one die), is 6.3 mm², has no crypto, and dates from 2017.

## Decision

NXP NTAG X DNA, part NT4PLDJUK, in the 16-ball WLCSP (1.41 × 1.41 × 0.49 mm, 0.35 mm pitch). It's the only tag I found with ECC signatures, AES SUN messages, energy harvesting on GPIO1, an I2C target, and two GPIOs in one die.

## Consequences

- Each tap returns a signed, counted URL, so copied cards are detectable and every card can be told apart.
- The 0.35 mm pitch needs a fab that can place WLCSP and route 3–3.5 mil.
- Input capacitance is 18.4 pF typical (datasheet Rev 3.2, Table 282), which sets the coil inductance.
- NXP only publishes the SOT2127-1 package drawing; the footprint uses it, and I need to confirm -2 matches when the parts arrive.
- Stock is thin: 21 at LCSC on 2026-11-21. The HVQFN version (NT4PLDJHN2, 0.85 mm tall) is the fallback.
