from __future__ import annotations

from pathlib import Path
import json
import sys

import typer

from .context import AppContext
from .config import AppConfig
from .pipelines.digest_pipeline import run_digest

app = typer.Typer(help="paku-digest – OCR and document extraction pipeline.")


@app.command()
def digest(
    input_path: Path = typer.Argument(..., help="File o directory di input."),
    ocr: str | None = typer.Option(
        None, "--ocr", help="OCR engine to use (default: from config)."
    ),
    out: Path | None = typer.Option(
        None, "--out", help="JSON files in output (stdout by default)."
    ),
) -> None:
    docs = run_digest(input_path=input_path, ocr_engine_name=ocr)
    payload = [d.model_dump(mode="json") for d in docs]
    text = json.dumps(payload, ensure_ascii=False, indent=2)

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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
