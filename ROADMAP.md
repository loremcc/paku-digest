# paku-digest --- Roadmap

This roadmap outlines the planned evolution of **paku-digest** from a
stub-based prototype into a full OCR and document-extraction framework.

The roadmap is incremental and structured to enable continuous
development without breaking the architecture.

------------------------------------------------------------------------

## Phase 1 --- Foundation (Current)

**Status: In progress**

-   [x] Project structure and packaging
-   [x] Typer-based CLI
-   [x] `.env` configuration system
-   [x] Singleton `AppContext`
-   [x] Stub OCR Engine (architecture validation)
-   [x] Pydantic document models
-   [x] `digest` pipeline (basic end-to-end working flow)
-   [x] Logging utilities
-   [x] Minimal samples folder infrastructure

------------------------------------------------------------------------

## Phase 2 --- OCR Engine System (Next)

### 2.1 --- Define OCR interface

-   [x] `OCREngine` Protocol / base class
-   [x] Unified OCR output model
-   [x] Engine registry (plug-in style)

### 2.2 --- Implement real engines

-   [x] `PaddleOCREngine` (local inference)
-   [x] `ChandraOCREngine` (local or API)
-   [x] CLI selection: `--ocr paddle` / `--ocr chandra`

### 2.3 --- Engine routing & strategies

-   [ ] Strategy: `light` / `heavy` / `auto`
-   [ ] Performance-aware routing
-   [ ] Engine health-checks

------------------------------------------------------------------------

## Phase 3 --- Pipelines Expansion

-   [ ] `digest` pipeline v2 with parallelism and batching
-   [ ] Benchmark pipeline
-   [ ] Compare pipeline
-   [ ] Multi-format export pipeline

------------------------------------------------------------------------

## Phase 4 --- Dataset and Regression System

### 4.1 --- Samples/Expected dataset

-   [ ] Populate `samples/raw`
-   [ ] Curated benchmark sets
-   [ ] Ground-truth JSON

### 4.2 --- Regression testing

-   [ ] CLI: `paku-digest regression samples/ expected/`
-   [ ] Error diff report
-   [ ] Thresholds and scoring

------------------------------------------------------------------------

## Phase 5 --- Advanced Features

-   [ ] OCR confidence heatmaps
-   [ ] Layout detection
-   [ ] Anime-text-specific heuristics
-   [ ] LM-based OCR post-processing
-   [ ] Notion / API integrations

------------------------------------------------------------------------

## Phase 6 --- Optimization & Distribution

-   [ ] Performance optimization
-   [ ] Docker image
-   [ ] Optional GUI
-   [ ] Plugin specification for third-party engines

------------------------------------------------------------------------

## Vision

A modular, engine-agnostic OCR platform capable of digesting structured
and unstructured visual data with consistent outputs across engines and
formats.
