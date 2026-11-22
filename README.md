# card

A thin PCB business card that opens a webpage when you tap it with a phone

## Status

- [x] Coil generator and footprint
- [x] Schematic
- [x] Coil 
- [ ] Layout
- [ ] Firmware
- [ ] Web side
- [ ] Prototype 1

## Build

Needs KiCad 10 and [uv](https://docs.astral.sh/uv/).

```
make setup   # Python venv that can see KiCad's pcbnew
make erc     # electrical rules check; fails on any violation
make docs    # schematic SVGs and PDF into hardware/renders (not tracked)
make coil    # regenerate the coil footprint
```

## Design notes

- [First principles](docs/first-principles.md): the numbers physics sets before any part gets picked, from coil tuning to thickness. This is where I found three problems in my original plan.
- [Decisions](docs/decisions/): one page per design choice, what I picked and what it costs.
- [Research](docs/research/): stock checks, LED colours, thin solar cells.

## Layout

```
hardware/          KiCad 10 project (card, nfc, mcu_leds); libs/ holds every symbol and footprint
tools/coil_gen.py  NFC coil footprint generator
docs/              design notes
```

## License

MIT, see [LICENSE](LICENSE).
