# Thin solar for a battery-free card

NFC gives up to 10 mW, but only during a tap. A thin solar cell gives a few hundred µW for as long as there's light. Stored, that lets the tag run from VCC and signal an arriving phone on GPIO2, so the LEDs could light on every tap instead of only from the app.

## Cells that fit the stack

Indoor output per cm², scaled linearly to 500 lux from each source's own figure:

| Technology | Example | Thickness | As quoted | Scaled to 500 lx | Fits? |
|---|---|---|---|---|---|
| Flexible amorphous Si | PowerFilm LL200 | 0.22 mm | 0.13–0.29 mW per module at 200 lx | (per-module) | Yes |
| Amorphous Si on film | Panasonic Amorton film | ~0.4 mm | 9.0 µW/cm² at 200 lx | ~22 | Tight |
| Organic PV | Epishine LEH3 | ~0.2 mm | 18 µW/cm² at 500 lx | 18 | Yes |
| Organic PV | Dracula LAYER 2.0 | 0.30 mm | ~45 µW/cm² at 1000 lx | ~22 | Yes |
| Flexible perovskite | Lab cells on PET | µm active | 32.5–36% efficiency at 1000 lx | ~49 (est.) | No product |
| Dye-sensitized | Exeger Powerfoyle | 1.3 mm | 37 µA into 3.7 V from 16 cm² at 200 lx | ~21 | Too thick |
| Monocrystalline Si | ANYSOLAR KXOB | 1.2–1.8 mm | 25% cell efficiency (outdoor) | | Too thick |

The perovskite figure is my estimate, taking 1000 lx of white LED light as about 0.3 mW/cm².

## Storage and power management

- MLCC bank: about 17–23 µJ usable between 1.8 V and 1.62 V. Enough for a short fade only.
- CAP-XX thin prismatic supercap: 0.4 mm, 40 mF at 4.5 V, about 340 mJ usable through a regulator.
- PMICs: e-peas AEM10330 (cold start 275 mV / 3 µW, regulated 1.2–3.3 V out), TI BQ25570, Nexperia NEH2000BY. Package heights still to check against the pocket.

## The risk

Every thin cell has a continuous back electrode, and anywhere on the card it sits inside the coil. A conductive sheet there acts like a shorted turn and detunes the antenna. Keep the cell small, prefer series-strip modules (slit back metal), and measure a coupon on a VNA before committing.

## Sources

- [PowerFilm LL200-3.6-75](https://www.powerfilmsolar.com/products/electronic-component-solar-panels/indoor-light-series/ll200-3.6-75)
- [Panasonic Amorton brochure](https://panasonic.net/electricworks/amorton/assets/pdf/Brochures_Amorton_E_2.pdf)
- [Epishine indoor solar cells](https://www.epishine.com/products/indoor-solar-cells)
- [Dracula LAYER 2.0](https://dracula-technologies.com/layer-2-0-organic-photovoltaic-module-for-indoor-energy-harvesting/)
- [Flexible perovskite record on PET](https://www.nanowerk.com/nanotechnology-news2/newsid=63500.php)
- [Exeger Powerfoyle brief](https://armkeil.blob.core.windows.net/developer/Files/pdf/ai-ecosystem-catalogue/ARM2112_137AEPSolutionsBrief-ExegerX2_SB1_IoT.pdf)
- [ANYSOLAR presentation](https://anysolar.biz/wp-content/uploads/dp/dd/ANYSOLAR_PRESENTATION_2022.pdf)
- [CAP-XX thin supercaps](https://www.astutegroup.com/services/franchise-electronics/franchise-lines/cap-xx/)
- [e-peas AEM10330](https://e-peas.com/product/aem10330/)
- [Nexperia NEH2000BY](https://www.nexperia.com/product/NEH2000BY)
