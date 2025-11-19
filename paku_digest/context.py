from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from .config import AppConfig
from .logging_utils import get_logger
from .ocr.base import OCREngine
from .ocr.stub import StubOCREngine


@dataclass
class AppContext:
    """
    Singleton that holds config, logger, and OCR engine registry.
    """
    _instance: ClassVar[Optional["AppContext"]] = None

    config: AppConfig
    logger: object
    ocr_engines: Dict[str, OCREngine]

    @classmethod
    def instance(cls) -> "AppContext":
        if cls._instance is None:
            cls._instance = cls._build()
        return cls._instance

    @classmethod
    def _build(cls) -> "AppContext":
        config = AppConfig.from_env()
        logger = get_logger(config)

        stub_engine = StubOCREngine(config=config, logger=logger)

        ocr_engines: Dict[str, OCREngine] = {
            stub_engine.name(): stub_engine,
            # future:
            # "paddle": PaddleOCREngine(config, logger),
            # "chandra-api": ChandraAPIOCREngine(config, logger),
        }

        return cls(config=config, logger=logger, ocr_engines=ocr_engines)

    def get_ocr(self, name: str) -> OCREngine:
        if name not in self.ocr_engines:
            raise ValueError(f"OCR engine not registered: {name}")
        return self.ocr_engines[name]
