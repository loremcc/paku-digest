from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from .config import AppConfig
from .logging_utils import get_logger
from .ocr.base import OCREngine
from .ocr.stub import StubOCREngine
from .ocr.paddle import PaddleOCREngine
from .ocr.chandra_api import ChandraAPIOCREngine


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

        engines: Dict[str, OCREngine] = {}

        # Always available: stub
        stub_engine = StubOCREngine(config=config, logger=logger)
        engines[stub_engine.name()] = stub_engine

        # Optional: PaddleOCR (only if dependencies installed)
        try:
            paddle_engine = PaddleOCREngine(config=config, logger=logger)
        except RuntimeError as e:
            logger.info(f"[AppContext] PaddleOCREngine not available: {e}")
        else:
            engines[paddle_engine.name()] = paddle_engine

        return cls(config=config, logger=logger, ocr_engines=engines)

        # Optional: Chandra API engine
        try:
            chandra_engine = ChandraAPIOCREngine(config=config, logger=logger)
        except RuntimeError as e:
            logger.info(f"[AppContext] ChandraAPIOCREngine not available: {e}")
        else:
            engines[chandra_engine.name()] = chandra_engine

    def get_ocr(self, name: str) -> OCREngine:
        if name not in self.ocr_engines:
            raise ValueError(
                f"OCR engine not registered: {name}. "
                f"Available: {', '.join(self.ocr_engines.keys())}"
            )
        return self.ocr_engines[name]

    def list_ocr_engines(self) -> Dict[str, OCREngine]:
        return dict(self.ocr_engines)
