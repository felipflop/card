# LED colours

All ROHM PICOLED parts (1.0 × 0.6 mm). Same target brightness for every row: 4 mcd, which is what the red SML-P11VT gives at 1 mA. mcd is already weighted by the eye's sensitivity, so equal mcd means roughly equal perceived brightness.

AlGaInP figures are from the SML-P11x datasheet at 1 mA. ROHM only specifies the InGaN parts (green, blue, white) at 5 mA, so those rows are scaled down to 1 mA and marked as estimates.

| Colour | Part | Wavelength | Vf | mcd/mA | Current for 4 mcd | LED power | From a 1.8 V rail? |
|---|---|---|---|---|---|---|---|
| Red | SML-P11VT | 626 nm | 1.8 V | 4.0 | 1.0 mA | 1.8 mW | Barely |
| Red, lower bin | SML-P11UT | 621 nm | 1.8 V | 2.5 | 1.6 mA | 2.9 mW | Barely |
| Amber | SML-P11DT | 605 nm | 1.9 V | 7.3 | 0.55 mA | 1.0 mW | No |
| Yellow (gold) | SML-P11YT | 586 nm | 1.9 V | 7.6 | 0.53 mA | 1.0 mW | No |
| Yellow-green | SML-P11MT | 569 nm | 1.9 V | 2.1 | 1.9 mA | 3.6 mW | No |
| Green | SMLP13EC8T | 527 nm | ~2.7 V (est.) | ~22 (est.) | ~0.18 mA | ~0.5 mW | No |
| Blue | SMLP13BC8T | 470 nm | ~2.8 V (est.) | ~5 (est.) | ~0.8 mA | ~2.2 mW | No |
| White | SMLP13WBC9W | phosphor | ~2.8 V (est.) | ~30 (est.) | ~0.13 mA | ~0.4 mW | No |

Why yellow beats red per watt: the eye's V(λ) curve is about 0.81 at 586 nm and 0.31 at 626 nm (see [first principles §6](../first-principles.md#6-light-what-the-eye-sees-and-how-the-engraving-glows)).

Ways above 1.8 V: the tag's 2.0 V harvest target ([0008](../decisions/0008-raise-the-rail-to-2v0-for-gold-leds.md)), or a charge pump on a spare MCU pin.

Sources: [SML-P11x datasheet](https://fscdn.rohm.com/en/products/databook/datasheet/opto/led/chip_mono/sml-p11-e.pdf), [SML-P12x/P13x datasheet](https://fscdn.rohm.com/en/products/databook/datasheet/opto/led/chip_mono/sml-p1-e.pdf).
