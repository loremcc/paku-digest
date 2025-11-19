from __future__ import annotations

from pathlib import Path

from .base import OCREngine
from ..config import AppConfig
from ..models import OcrResult


class StubOCREngine(OCREngine):
    """Simple fake OCR engine used for development and architecture validation."""

    def __init__(self, config: AppConfig, logger) -> None:
        self._config = config
        self._logger = logger

    def name(self) -> str:
        return "stub"

    def extract(self, path: Path) -> OcrResult:
        self._logger.info(f"[stub] OCR on {path}")
        return OcrResult(
            engine=self.name(),
            raw_text=f"[stub text for {path.name}]",
            blocks=[],
            language=None,
            meta={
                "note": "stub engine, replace with real OCR",
                "path": str(path),
                "env": self._config.env,
            },
        )
