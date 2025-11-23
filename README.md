# paku-digest

OCR and document-extraction pipeline that **digests** images and PDFs into structured text and metadata.

`paku-digest` is a modular, enterprise‑grade personal project designed with:
- typed configuration via `.env`
- a singleton `AppContext`
- Pydantic models
- Typer CLI
- a plug‑in OCR engine system (`stub`, optional `paddle`, optional `chandra-api`)

---

## Overview

`paku-digest`:

- Processes images or entire directories  
- Applies a pluggable OCR engine (stub → paddle → chandra)  
- Normalizes output into structured `Document` models  
- Exports clean JSON suitable for ingestion or pipelines  

### Current capabilities
- **Stub OCR Engine** (architecture validation)
- Typer-based CLI (`paku-digest`)
- Singleton `AppContext` (config + logger + OCR registry)
- Unified OCR models: `Document`, `OcrResult`, `OcrBlock`, `BoundingBox`
- Clean project layout + `.env` configuration + Makefile

### Upcoming (Phase 2.x)
- PaddleOCR (local inference)
- Chandra OCR (OpenAI-compatible API)
- Benchmarking pipelines
- Regression tests
- Multi-format export (txt, jsonl)
- Advanced routing strategies

---

## Features

- Unified CLI  
- Centralized configuration  
- Strong typing via Pydantic  
- Modular OCR engine registry  
- Reproducible environment  
- High extensibility for OCR engines and pipelines  

---

## Architecture

High-level pipeline:

```
CLI (Typer)
   ↓
pipelines.digest_pipeline.run_digest()
   ↓
AppContext (singleton)
   - AppConfig
   - logger
   - ocr_engines registry
   ↓
OCR Engine (stub / paddle / chandra-api)
   ↓
Pydantic models
   ↓
JSON output
```

---

## Project Layout

```
paku-digest/
├─ paku_digest/
│  ├─ __init__.py
│  ├─ cli.py                 # Typer CLI (paku-digest ...)
│  ├─ config.py              # AppConfig loader + validation
│  ├─ context.py             # AppContext singleton (config, logger, engines)
│  ├─ logging_utils.py       # Centralized logger setup
│  ├─ models.py              # Document, OcrResult, OcrBlock,...
│  ├─ ocr/                   # OCR engines (stub, paddle, chandra-api)
│  │   ├─ base.py            # OCREngine interface
│  │   ├─ stub.py            # Stub engine
│  │   ├─ paddle.py          # PaddleOCR (optional, future)
│  │   └─ chandra_api.py     # Chandra OCR (placeholder)
│  └─ pipelines/
│      ├─ __init__.py
│      └─ digest_pipeline.py
│
├─ samples/                  # Empty dataset structure (intentionally clean)
│  ├─ raw/
│  ├─ curated/
│  ├─ expected/
│  ├─ notes.md
│  └─ README.md
│
├─ .env                      # Local configuration (ignored)
├─ .env.example              # Environment template
├─ Makefile
├─ pyproject.toml
├─ ROADMAP.md
├─ CONTRIBUTING.md
├─ README.md                 # This file
└─ LICENSE
```

---

## Installation

### Create and activate venv

```
python -m venv .venv
```

Windows:

```
.venv\Scripts\activate
```

Linux/macOS:

```
source .venv/bin/activate
```

### Install dependencies

```
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

---

## Configuration

Use `.env` in root:

```
PAKU_ENV=local
PAKU_LOG_LEVEL=INFO
PAKU_DEFAULT_OCR=stub
PAKU_WORKDIR=.
PAKU_PADDLE_LANG=en

# Optional — Chandra (OpenAI-compatible API)
PAKU_CHANDRA_API_URL=
PAKU_CHANDRA_API_KEY=
```

Copy template:

```
cp .env.example .env
```

---

## Usage

### Show configuration

```
paku-digest config
```

### Validate environment

```
paku-digest env-check
```

### List available OCR engines

```
paku-digest engines
```

### Run OCR digest pipeline

```
paku-digest digest samples --out out/samples.json
```

---

## Development

### Lint/format

```
python -m ruff check paku_digest
python -m mypy paku_digest
python -m black paku_digest
```

### Tests

```
python -m pytest
```

---

## Roadmap

See the full project roadmap:  
[ROADMAP.md](./ROADMAP.md)

---

## License

Apache License 2.0.
