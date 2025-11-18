# paku-digest

OCR and document-extraction pipeline that **digests** images and PDFs
into structured text and metadata.

`paku-digest` is designed as a personal project built with:
modular architecture, `.env`, configuration, typed CLI, and
a plugin-based OCR engine system (stub for now, Paddle/Chandra later).

------------------------------------------------------------------------

## Overview

`paku-digest`:

-   Processes images or directories.
-   Applies an OCR pipeline (engine → normalization → structuring).
-   Produces structured JSON ready for further ingestion or processing.

Current capabilities: - **Stub OCR Engine** to validate architecture and
flow. - Typer-based CLI (`paku-digest`). - Singleton `AppContext`
managing config, logger, and OCR engines. - Pydantic models for
`Document`, `OcrResult`, `OcrBlock`, etc.

Future: - PaddleOCR integration. - Chandra OCR (local or API via
vLLM). - Routing strategies, benchmarking, multiple output formats.

------------------------------------------------------------------------

## Features

-   Unified CLI (`paku-digest`).
-   Centralized config via `.env` → `AppConfig`.
-   Singleton `AppContext` with OCR engine registry.
-   Pydantic models for strong typing.
-   Modular pipeline system (`digest` pipeline).
-   Extensible architecture for new OCR engines.

------------------------------------------------------------------------

## Architecture

High-level pipeline:

    CLI (Typer)
       ↓
    pipelines.digest_pipeline.run_digest()
       ↓
    AppContext (singleton)
       - AppConfig
       - logger
       - ocr_engines registry
       ↓
    OCR Engine (Stub for now)
       ↓
    Pydantic models
       ↓
    JSON output

------------------------------------------------------------------------

## Project Layout

    paku-digest/
    ├─ paku_digest/
    │ ├─ init.py
    │ ├─ cli.py                 # Typer CLI (paku-digest ...)
    │ ├─ config.py              # AppConfig loader (.env → dataclass)
    │ ├─ context.py             # AppContext singleton (config, logger, engines)
    │ ├─ logging_utils.py       # Centralized logger setup
    │ ├─ models.py              # Pydantic models (Document, OcrResult, ...)
    │ └─ pipelines/
    │ ├─ init.py
    │ └─ digest_pipeline.py
    │
    ├─ samples/                 # Local sample dataset for development & OCR tests
    │ ├─ raw/                   # Unmodified screenshots, photos, scans
    │ │ ├─ img01.png
    │ │ ├─ img02.jpg
    │ │ └─ ...
    │ │
    │ ├─ curated/               # Hand-picked curated samples for benchmarking
    │ │ ├─ forms/
    │ │ ├─ documents/
    │ │ ├─ anime_text/          # Anime screenshots containing text (OCR hard cases)
    │ │ └─ noisy/               # Blurry/low-light/glare samples
    │ │
    │ ├─ expected/              # Ground-truth JSON used for regression testing
    │ │ ├─ img01.json
    │ │ ├─ invoice_01.json
    │ │ └─ ...
    │ │
    │ ├─ notes.md               # Observations / OCR failures to revisit
    │ └─ README.md              # Documentation of the samples folder
    │
    ├─ .env                     # Local configuration (not committed)
    ├─ .env.example             # Environment template
    ├─ Makefile                 # Dev shortcuts (lint/test/build)
    ├─ pyproject.toml           # Build system, dependencies, metadata
    ├─ README.md
    └─ LICENSE

------------------------------------------------------------------------

## Installation

### Create and activate venv

    python -m venv .venv

Windows:

    .venv\Scripts\activate

Linux/macOS:

    source .venv/bin/activate

### Install dependencies

    python -m pip install --upgrade pip
    python -m pip install -e ".[dev]"

------------------------------------------------------------------------

## Configuration

Use `.env` in root:

    PAKU_ENV=local
    PAKU_LOG_LEVEL=INFO
    PAKU_DEFAULT_OCR=stub
    PAKU_WORKDIR=.
    PAKU_PADDLE_LANG=en

Copy from template:

    cp .env.example .env

------------------------------------------------------------------------

## Usage

### Show configuration

    paku-digest config

### Run OCR digest pipeline

    paku-digest digest samples --out out/samples.json

------------------------------------------------------------------------

## Development

### Lint/format

    python -m ruff check paku_digest
    python -m mypy paku_digest
    python -m black paku_digest

### Tests

    python -m pytest

------------------------------------------------------------------------

## Roadmap

-   Formal OCR interface (`OCREngine`).
-   PaddleOCR integration.
-   Chandra OCR (local/API).
-   Routing strategies (light/heavy/auto).
-   Benchmark suite.
-   Multi-format output (json/jsonl/txt).

------------------------------------------------------------------------

## License

Apache License 2.0.
