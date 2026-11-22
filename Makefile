PY := /usr/bin/python3
SCH := hardware/card.kicad_sch

.PHONY: setup coil check erc docs

# venv must see the system pcbnew/wx that ship with KiCad
setup:
	uv venv --python $(PY) --system-site-packages --allow-existing
	uv sync

coil:
	uv run tools/coil_gen.py -o hardware/libs/card.pretty

check:
	uv run python -c "import pcbnew, wx; print('pcbnew', pcbnew.Version())"
	uv run kibot --version

erc:
	kicad-cli sch erc --severity-all --exit-code-violations -o /dev/stdout $(SCH)

# schematic renders, kept out of git
docs:
	mkdir -p hardware/renders
	kicad-cli sch export svg -o hardware/renders $(SCH)
	kicad-cli sch export pdf -o hardware/renders/schematic.pdf $(SCH)
