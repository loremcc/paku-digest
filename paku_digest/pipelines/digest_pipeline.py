from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List

from ..context import AppContext
from ..models import Document


def discover_images(root: Path) -> List[Path]:
    """
    Discover supported image files starting from a file or directory.

    - If `root` is a file, returns [root].
    - If `root` is a directory, recursively scans for image extensions.
    """
    if root.is_file():
        return [root]

    exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
    return [p for p in root.rglob("*") if p.suffix.lower() in exts]


def _process_one(path: Path, engine, log) -> Document:
    """
    Process a single image with the given engine and return a Document.
    Isolated so it can be used both sequentially and in parallel.
    """
    log.info(f"[digest] Processing {Path} with engine '{engine.name()}")
    ocr_result = engine.extract(path)
    return Document(path=path, ocr=ocr_result)


def run_digest(
    input_path: Path,
    ocr_engine_name: str | None = None,
    workers: int | None = None,
) -> List[Document]:
    """
    Main digest pipeline v2:

    - resolves the OCR engine (name or strategy)
    - discovers input images
    - processes them sequentially or in parallel (ThreadPool)
    - returns a list of Document models
    """
    ctx = AppContext.instance()
    cfg = ctx.config
    log = ctx.logger

    key = ocr_engine_name or cfg.default_ocr  # engine name or strategy
    engine = ctx.resolve_engine(key)

    paths = discover_images(input_path)
    if not paths:
        log.warning(f"[digest] No images found under {input_path}")
        return []

    max_workers = workers or cfg.max_workers
    if max_workers < 1:
        max_workers = 1

    # Sequential path
    if max_workers == 1:
        docs: list[Document] = []
        for p in paths:
            docs.append(_process_one(p, engine, log))
        return docs

    # Parallel path using ThreadPoolExecutor
    log.info(f"[digest] Running with {max_workers} workers over {len(paths)} files")

    docs: list[Document] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        future_map = {ex.submit(_process_one, p, engine, log): p for p in paths}
        for fut in as_completed(future_map):
            p = future_map[fut]
            try:
                doc = fut.result()
            except Exception as exc:  # noqa: BLE001
                log.error(f"[digest] Error processing {p}: {exc}")
                continue
            docs.append(doc)

    return docs
