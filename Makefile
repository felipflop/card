PY := /usr/bin/python3

.PHONY: setup coil check

# venv must see the system pcbnew/wx that ship with KiCad
setup:
	uv venv --python $(PY) --system-site-packages --allow-existing
	uv sync

coil:
	uv run tools/coil_gen.py -o hardware/libs/card.pretty

check:
	uv run python -c "import pcbnew, wx; print('pcbnew', pcbnew.Version())"
	uv run kibot --version
