from __future__ import annotations

from pathlib import Path
import json
import sys

import typer

from typing import List

from .context import AppContext
from .config import AppConfig
from .pipelines.digest_pipeline import run_digest
from .pipelines.benchmark_pipeline import run_benchmark
from .pipelines.compare_pipeline import run_compare
from .pipelines.export_pipeline import export_documents_to_string

app = typer.Typer(help="paku-digest – OCR and document extraction pipeline.")


@app.command()
@app.command()
def digest(
    input_path: Path = typer.Argument(..., help="Input file or directory."),
    ocr: str | None = typer.Option(
        None,
        "--ocr",
        help=(
            "OCR engine or strategy to use. "
            "Engines: stub, paddle, chandra-api. "
            "Strategies: light, heavy, auto. "
            "Defaults to PAKU_DEFAULT_OCR."
        ),
    ),
    workers: int = typer.Option(
        0,
        "--workers",
        help=(
            "Number of parallel workers. "
            "0 = use PAKU_MAX_WORKERS from config; "
            "1 = sequential; >1 = ThreadPool."
        ),
    ),
    format: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json | jsonl | txt | csv (default: json).",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        help="Output file (stdout by default).",
    ),
) -> None:
    if workers <= 0:
        ctx = AppContext.instance()
        resolved_workers = ctx.config.max_workers
    else:
        resolved_workers = workers

    docs = run_digest(
        input_path=input_path,
        ocr_engine_name=ocr,
        workers=resolved_workers,
    )

    fmt = format.lower()
    if fmt not in {"json", "jsonl", "txt", "csv"}:
        raise typer.BadParameter(
            f"Unsupported format: {format!r}. Use one of: json, jsonl, txt, csv.",
            param_hint="--format",
        )

    text = export_documents_to_string(docs, fmt=fmt)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


@app.command()
def config() -> None:
    ctx = AppContext.instance()
    data = {
        "env": ctx.config.env,
        "log_level": ctx.config.log_level,
        "default_ocr": ctx.config.default_ocr,
        "workdir": str(ctx.config.workdir),
        "paddle_lang": ctx.config.paddle_lang,
        "ocr_engines": list(ctx.ocr_engines.keys()),
    }
    print(json.dumps(data, indent=2))


@app.command()
def engines() -> None:
    """List registered OCR engines."""
    ctx = AppContext.instance()
    engines = ctx.list_ocr_engines()
    data = [
        {"name": name, "type": engine.__class__.__name__}
        for name, engine in engines.items()
    ]
    print(json.dumps(data, indent=2))


@app.command()
def env_check() -> None:
    """
    Validate environment configuration and print result.
    """
    try:
        cfg = AppConfig.from_env()
        print("Environment configuration OK:")
        print(cfg)
    except Exception as e:
        print("Configuration error:")
        print(str(e))
        raise typer.Exit(code=1)


@app.command()
def benchmark(
    input_path: Path = typer.Argument(..., help="Input file or directory."),
    engine: List[str] = typer.Option(
        None,
        "--engine",
        "-e",
        help=(
            "OCR engine(s) to benchmark by name (e.g. --engine stub --engine paddle). "
            "If omitted, all registered engines are benchmarked."
        ),
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        help="JSON output file for benchmark results (stdout if omitted).",
    ),
) -> None:
    """
    Benchmark engines over the given dataset and report per-image timings.
    """
    engine_names = engine or None
    result = run_benchmark(input_path=input_path, engine_names=engine_names)
    text = json.dumps(result, ensure_ascii=False, indent=2)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


@app.command()
def compare(
    left: Path = typer.Argument(..., help="Left JSON digest output."),
    right: Path = typer.Argument(..., help="Right JSON digest output."),
    out: Path | None = typer.Option(
        None,
        "--out",
        help="JSON output file for comparison results (stdout if omitted).",
    ),
) -> None:
    """
    Compare two digest outputs (per-path OCR text and similarity).
    """
    result = run_compare(left=left, right=right)
    text = json.dumps(result, ensure_ascii=False, indent=2)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
