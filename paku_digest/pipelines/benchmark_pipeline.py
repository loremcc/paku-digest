from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Dict, List, Optional

from ..context import AppContext
from ..ocr.base import OCREngine
from .digest_pipeline import discover_images


@dataclass
class EngineRunStats:
    name: str
    kind: str
    runs: List[dict]
    total_ms: float
    avg_ms: float
    ok_count: int
    error_count: int


def _benchmark_one_engine(
    engine: OCREngine,
    paths: List[Path],
    log,
) -> EngineRunStats:
    runs: List[dict] = []
    total_ms = 0.0
    ok_count = 0
    error_count = 0

    for p in paths:
        log.info(f"[benchmark] Engine '{engine.name()}' on {p}")
        start = perf_counter()
        error: Optional[str] = None
        ok = True

        try:
            engine.extract(p)
        except Exception as exc:  # noqa: BLE001
            ok = False
            error = str(exc)
            log.error(f"[benchmark] Error with engine '{engine.name()}' on {p}: {exc}")
        elapsed_ms = (perf_counter() - start) * 1000.0

        total_ms += elapsed_ms
        if ok:
            ok_count += 1
        else:
            error_count += 1

        runs.append(
            {
                "path": str(p),
                "elapsed_ms": elapsed_ms,
                "ok": ok,
                "error": error,
            }
        )

    avg_ms = total_ms / len(paths) if paths else 0.0

    return EngineRunStats(
        name=engine.name(),
        kind=engine.kind(),
        runs=runs,
        total_ms=total_ms,
        avg_ms=avg_ms,
        ok_count=ok_count,
        error_count=error_count,
    )


def run_benchmark(
    input_path: Path,
    engine_names: Optional[List[str]] = None,
) -> dict:
    """
    Benchmark pipeline:

    - discovers images under input_path
    - runs each selected engine on all images
    - records per-image timings and aggregate stats
    - returns a JSON-serializable dict
    """
    ctx = AppContext.instance()
    log = ctx.logger

    paths = discover_images(input_path)
    if not paths:
        log.warning(f"[benchmark] No images found under {input_path}")
        return {
            "input_root": str(input_path),
            "num_images": 0,
            "engines": [],
        }

    # Select engines
    engines: Dict[str, OCREngine] = ctx.list_ocr_engines()
    if engine_names:
        # Filter to requested names only
        engines = {
            name: eng
            for name, eng in engines.items()
            if name in engine_names
        }

    if not engines:
        raise RuntimeError(
            "No OCR engines available for benchmark "
            f"(requested: {engine_names!r})."
        )

    engine_stats: List[dict] = []
    for name, engine in engines.items():
        stats = _benchmark_one_engine(engine, paths, log)
        engine_stats.append(
            {
                "name": stats.name,
                "kind": stats.kind,
                "total_ms": stats.total_ms,
                "avg_ms": stats.avg_ms,
                "ok_count": stats.ok_count,
                "error_count": stats.error_count,
                "runs": stats.runs,
            }
        )

    result = {
        "input_root": str(input_path),
        "num_images": len(paths),
        "engines": engine_stats,
    }
    return result
