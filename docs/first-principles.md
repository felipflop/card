# First principles

Before picking parts, I try to write down what physics and the requirements force, with numbers. Every decision record should trace back to a section here. If a decision can't, it's taste, and I say so.

The numbers come from datasheets (cited) or from the arithmetic shown. Anything I haven't measured yet is marked as an estimate.

## 1. What the card has to do

Stripped down, the card has five jobs. Everything else is optional.

1. Open a link on any phone with no app, iPhones included. That means ISO/IEC 14443-A and an NDEF record, because that's what iOS reads in the background.
2. Prove a tap is genuine, so a copied card is detectable.
3. Work with no battery.
4. Fit a wallet: as close to the ISO/IEC 7810 ID-1 card (85.60 × 53.98 × 0.76 mm) as the parts allow.
5. Look finished: no visible components, no silkscreen, nothing that reads as a bare PCB.

Jobs 1 and 2 pick the chip family (sections 2 and 3). Job 3 sets the energy budget (section 4). Job 4 sets the thickness budget (section 5). Job 5 sets the optics and the palette (sections 6 and 7).

## 2. The antenna is an LC tank

A passive tag is powered and read through a resonant LC circuit tuned to the reader's 13.56 MHz carrier:

f₀ = 1 / (2π √(L·C))

C is the tag's input capacitance plus the coil and layout parasitics. For the NTAG X DNA that's 18.4 pF typical (datasheet Rev 3.2, Table 282), and I allow 2.5 pF of parasitics, so C ≈ 20.9 pF. Solving for L:

- 13.56 MHz needs L = 6.59 µH.
- 14.0 MHz needs L = 6.18 µH.

The coil should sit slightly above 13.56 MHz before lamination, because both the trim capacitor and the dielectric skin can only pull the frequency down, never up.

The biggest coil that fits the card captures the most flux, so the coil runs around the perimeter. `tools/coil_gen.py` uses the planar spiral formula from NXP AN11276. It keeps trace and gap equal, because the coil is visible on the front and even stripes look deliberate, and solves their width for the target frequency. With 18.4 pF and an untuned target of 14.0 MHz it picks 6 turns of 0.39 mm stripes: L ≈ 6.19 µH, f₀ ≈ 13.99 MHz, Rdc ≈ 3.7 Ω on half-ounce flex copper.

**How precise does the tuning have to be?** Less than I first thought. The tag isn't just a capacitor: the datasheet also gives 1.5 kΩ of parallel input resistance at the start of operation (Table 282), which is the condition that sets read range. At 14 MHz the coil's reactance is X = ωL ≈ 540 Ω, so the loaded quality factor is

Q ≈ R / X = 1500 / 540 ≈ 2.7

The coil's own copper loss barely registers. Even with 18 µm copper its Q is about 150, which looks like an 81 kΩ resistor in parallel with the chip's 1.5 kΩ. A tank with Q ≈ 2.7 is about 5 MHz wide, and its response at a detuning Δf is 1 / √(1 + (2QΔf/f)²):

| Detuning | Response |
|---|---|
| 0.1 MHz | 99.9% |
| 0.3 MHz | 99.3% |
| 0.5 MHz | 98.0% |
| 1.0 MHz | 92.6% |

So the lamination shift of a few hundred kHz costs about 1%, and copper thickness is free to choose for other reasons. The trim cap stays as a DNP footprint for measuring, not because the card depends on it. When the tag is harvesting it loads the coil harder, which lowers Q and widens the band further.

*Correction, 2026-11-22.* The first version of the generator assumed 17 pF, which put the coil at 13.58 MHz with the real 18.4 pF, and I listed that as an open problem. The Q calculation above shows it would have cost under 1%. I regenerated the coil anyway, since aiming above 13.56 MHz costs nothing.

## 3. Proving a tap is genuine needs a secret that can't be read out

A static URL or UID can be copied. To make a copy detectable, every tap has to produce something only the original chip could compute: a counter plus a MAC or signature under a key that never leaves the chip. That rules out plain NTAG21x tags and points at SUN messages (AES-CMAC over a counter), plus an ECC signature for originality. The NTAG X DNA does both in one die, which is [decision 0001](decisions/0001-use-ntag-x-dna-for-the-tag.md).

## 4. Energy: what the field gives and what light costs

**Supply.** The tag can deliver at most 10 mW from GPIO1 (datasheet Rev 3.2, Table 281), and only while a phone is held there. A real phone at a few centimetres gives less; I'll measure it.

**Voltage window.** The tag's VCC has an absolute maximum of 2.0 V (Table 273) and should avoid 1.55–1.62 V (Table 274). The MCU needs at least 1.62 V. That leaves a window of a few hundred millivolts, so the rail is 1.8 V ([0003](decisions/0003-run-the-board-at-1v8.md)).

**Load.** An LED costs P = Vf × I. A red LED at 1 mA and 1.8 V is 1.8 mW. Charlieplexing lights one LED at a time, so twelve LEDs cost the same average power as one LED that's always on, whatever pattern they show.

**Storage.** Energy in a capacitor is E = ½CV². Only the part between 1.8 V and the MCU's 1.62 V floor is usable:

E = ½ C (1.8² − 1.62²) = 0.31 × C

| Storage | Usable energy | One LED at 0.5 mA (0.85 mW) | One LED at 0.1 mA (0.17 mW) |
|---|---|---|---|
| MLCC bank as fitted, 54 µF | 17 µJ | 20 ms | 98 ms |
| MLCC bank with C5, 76 µF | 23 µJ | 28 ms | 138 ms |
| CAP-XX thin supercap, 40 mF, 4.5 → 1.8 V via a regulator | 340 mJ | about 6 min | about 33 min |

**Open problem.** The plan promised a fade of 0.3–1 s from an MLCC bank. Physics says the bank gives tens of milliseconds at useful brightness, before MLCC DC-bias derating makes it worse. A visible fade needs either very low current at the end of the fade or a real store like the 0.4 mm supercap. I'll measure the fade on prototype 1 before deciding.

## 5. Thickness: the tallest part sets the card

The card is a stack. Pockets in the stiffener hold the parts, so the stiffener has to be at least as thick as the tallest part:

| Layer | Thickness |
|---|---|
| Flex (polyimide, copper, mask) | 0.11 mm |
| Adhesive | 0.06 mm (0.025 mm with OCA) |
| Stiffener ≥ tallest part | see below |
| Back skin | 0.08 mm |

Tallest parts: the tag at 0.525 mm max (SOT2127-1), 0402 capacitors at 0.55 mm max, the WSON MCU at 0.8 mm max. The LEDs are 0.2 mm.

- With the tag as the tallest part, the stack is 0.11 + 0.06 + 0.525 + 0.08 = **0.78 mm**. ISO's 0.76 mm is only reachable with OCA instead of 467MP, or by finding a thinner tag package.
- The 0402 bank capacitors (0.55 mm) and the WSON (0.8 mm, giving **1.05 mm** at that island) both break the budget.

**Open problem.** The plan's 0.43 mm stiffener was never going to work with these parts. Either the bank moves to 0201 capacitors (0.33 mm) and the MCU goes back to the WCSP (0.35 mm), or the card accepts about 0.8 mm. Pocket depth gets decided at layout with these numbers.

## 6. Light: what the eye sees and how the engraving glows

**Brightness per watt depends on colour.** The eye's sensitivity, the CIE V(λ) curve, peaks at 555 nm. Relative values: 586 nm yellow ≈ 0.81, 605 nm amber ≈ 0.57, 626 nm red ≈ 0.31, 527 nm green ≈ 0.82, 470 nm blue ≈ 0.09. For the same optical power, a yellow LED looks about 2.6 times brighter than a red one. ROHM's own numbers agree in direction: 7.6 mcd at 1 mA for the 586 nm SML-P11YT against 4.0 mcd for the 626 nm SML-P11VT. That's why the gold LED in [0008](decisions/0008-raise-the-rail-to-2v0-for-gold-leds.md) is also the efficient one.

**Light gets trapped in clear plastic.** Light inside a material of index n hitting its surface at more than the critical angle θc = arcsin(1/n) reflects back in completely. For epoxy (n ≈ 1.5) θc ≈ 41.8°; for polycarbonate (n ≈ 1.59) θc ≈ 39.1°. A Lambertian LED embedded face down in the slab sends a fraction cos²θc of its light beyond that angle: about 56–60%. That light runs along the epoxy and skin until something scatters it out, and the laser-engraved micro-voids do exactly that. It's the physics behind the edge-lit engraving in [0006](decisions/0006-light-the-back-and-the-engraving.md), and why the engraving needs the laser's foaming setting, which leaves light-scattering voids. The carbonising setting leaves dark marks that won't glow.

## 7. Colour: what makes metal look expensive

This part is perception rather than physics, so it's weaker evidence. Gold is a warm, yellow-orange reflector. Next to warm neutrals it reads as gold; next to cool blue-blacks or blue-whites the contrast pushes it toward brass. Cold light sources next to it do the same. A light that matches the metal's hue makes the card read as one material. That's the reasoning behind [0007](decisions/0007-use-the-noir-or-palette.md), and I'll check it against physical samples before committing.

## 8. Fine pitch: why the board needs via-in-pad

The tag's balls are on a 0.35 mm pitch with 0.20 mm pads, which leaves 0.15 mm between pads. One trace between two pads at 3 mil needs 3 × 0.076 = 0.23 mm (trace plus two gaps). So no trace fits between balls. The outer ring of twelve balls can route straight out. The four inner balls (B2, B3 and C3 are VSS, C2 is VCC) need vias in their pads, filled and capped. That's the first-principles reason the plan calls for HDI with VIPPO.

## Open problems found here

| # | Problem | Section | Next step |
|---|---|---|---|
| 1 | Coil tuned too low for the 18.4 pF typical tag capacitance | 2 | Done 2026-11-22: regenerated for 13.99 MHz. Loaded Q ≈ 2.7 means it only cost about 1% |
| 2 | MLCC bank fades in tens of ms, not 0.3–1 s | 4 | Measure on prototype 1; consider the 0.4 mm supercap |
| 3 | 0.76 mm ISO thickness not reachable with these parts | 5 | Decide at layout: 0201 bank and WCSP MCU, or accept about 0.8 mm |
