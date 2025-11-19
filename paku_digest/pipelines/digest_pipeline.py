from __future__ import annotations

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


def run_digest(
    input_path: Path,
    ocr_engine_name: str | None = None,
) -> List[Document]:
    """
    Main digest pipeline:
    - resolves the OCR engine (from arg or config)
    - discovers input images
    - runs OCR on each
    - returns a list of Document models
    """
    ctx = AppContext.instance()
    cfg = ctx.config
    log = ctx.logger

    engine_name = ocr_engine_name or cfg.default_ocr
    engine = ctx.get_ocr(engine_name)

    paths = discover_images(input_path)
    documents: list[Document] = []

    for p in paths:
        log.info(f"[digest] Processing {p}")
        ocr_result = engine.extract(p)  # returns OcrResult
        doc = Document(path=p, ocr=ocr_result)
        documents.append(doc)

    return documents
