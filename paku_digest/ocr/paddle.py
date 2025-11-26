from __future__ import annotations

from pathlib import Path
from typing import Any, List

import importlib.util

from .base import OCREngine
from ..config import AppConfig
from ..models import OcrResult, OcrBlock, BoundingBox


class PaddleOCREngine(OCREngine):
    """
    Local OCR engine based on PaddleOCR.

    This engine is only available if the 'paddleocr' package is installed
    (typically via the 'ocr' extra or requirements-ocr.txt).
    """

    def __init__(self, config: AppConfig, logger) -> None:
        self._config = config
        self._logger = logger

        # Lazy, safe import: non rompe il progetto se paddleocr non è installato
        if importlib.util.find_spec("paddleocr") is None:
            raise RuntimeError(
                "PaddleOCR is not installed. "
                "Install it via the 'ocr' extra or requirements-ocr.txt "
                "e.g. `pip install -e .[ocr]`."
            )

        from paddleocr import PaddleOCR  # type: ignore[import]

        self._ocr = PaddleOCR(
            use_angle_cls=True,
            lang=self._config.paddle_lang,
            show_log=False,
        )

    def name(self) -> str:
        return "paddle"
    
    def kind(self) -> str:
        return "heavy"
    
    def extract(self, path: Path) -> OcrResult:
        self._logger.info(f"[paddle] OCR on {path}")
        result = self._ocr.ocr(str(path), cls=True)

        blocks: List[OcrBlock] = []
        raw_lines: List[str] = []

        if not result:
            return OcrResult(
                engine=self.name(),
                raw_text="",
                blocks=[],
                language=self._config.paddle_lang,
                meta={"source": str(path), "note": "no text detected"},
            )

        # PaddleOCR structure: result[0] is list of lines
        for line in result[0]:
            # line[0] = box, line[1] = (text, confidence)
            box = line[0]
            text, conf = line[1]

            x_coords = [p[0] for p in box]
            y_coords = [p[1] for p in box]

            bbox = BoundingBox(
                x=int(min(x_coords)),
                y=int(min(y_coords)),
                width=int(max(x_coords) - min(x_coords)),
                height=int(max(y_coords) - min(y_coords)),
            )

            blocks.append(
                OcrBlock(
                    text=text,
                    confidence=float(conf),
                    bbox=bbox,
                    type="line",
                )
            )
            raw_lines.append(text)

        return OcrResult(
            engine=self.name(),
            raw_text="\n".join(raw_lines),
            blocks=blocks,
            language=self._config.paddle_lang,
            meta={"source": str(path)},
        )
