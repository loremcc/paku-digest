from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Optional, Dict

from .config import AppConfig
from .logging_utils import get_logger
from .models import OcrResult


@dataclass
class AppContext:
    """
    Singleton che contiene config, logger e registry degli OCR engine.
    """
    _instance: ClassVar[Optional["AppContext"]] = None

    config: AppConfig
    logger: object
    ocr_engines: Dict[str, object]

    @classmethod
    def instance(cls) -> "AppContext":
        if cls._instance is None:
            cls._instance = cls._build()
        return cls._instance

    @classmethod
    def _build(cls) -> "AppContext":
        config = AppConfig.from_env()
        logger = get_logger(config)

        class StubEngine:
            def name(self) -> str:
                return "stub"

            def extract(self, path: Path) -> OcrResult:
                logger.info(f"[stub] OCR on {path}")
                return OcrResult(
                    engine=self.name(),
                    raw_text=f"[stub text for {path.name}]",
                    blocks=[],
                    language=None,
                    meta={"note": "stub engine, replace with real OCR"},
                )

        ocr_engines: Dict[str, object] = {
            "stub": StubEngine(),
        }

        return cls(config=config, logger=logger, ocr_engines=ocr_engines)

    def get_ocr(self, name: str) -> object:
        if name not in self.ocr_engines:
            raise ValueError(f"OCR engine not registered: {name}")
        return self.ocr_engines[name]
