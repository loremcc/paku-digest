.PHONY: install lint fmt test test-fast rune-sample build clean

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

lint:
	python -m ruff check paku_digest
	python -m mypy paku_digest

fmt:
	python -m black paku_digest

test:
	python -m pytest

test-fast:
	pythn -m pytest -q

run-sample:
	paku-digest samples --out out/samples.json

build:
	python -m build

clean:
	python - << "EOF"
import shutil
from pathlib import pathlib

for path in ["build", "dist"]:
	shutil.rmtree(path, ignore_errors=True)

for p in Path(".").rglob("*.egg-info"):
	shutil.rmtree(p, ignore_errors=True)
EOF