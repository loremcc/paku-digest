from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from .config import AppConfig
from .logging_utils import get_logger
from .ocr.base import OCREngine
from .ocr.stub import StubOCREngine
from .ocr.paddle import PaddleOCREngine
from .ocr.chandra_api import ChandraAPIOCREngine
from .ocr.router import EngineRouter


@dataclass
class AppContext:
    """
    Singleton that holds config, logger, and OCR engine registry.
    """
    _instance: ClassVar[Optional["AppContext"]] = None

    config: AppConfig
    logger: object
    ocr_engines: Dict[str, OCREngine]
    router: EngineRouter

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

        # Optional: Paddle
        try:
            paddle_engine = PaddleOCREngine(config=config, logger=logger)
        except RuntimeError as e:
            logger.info(f"[AppContext] PaddleOCREngine not available: {e}")
        else:
            engines[paddle_engine.name()] = paddle_engine

        # Optional: Chandra API
        try:
            chandra_engine = ChandraAPIOCREngine(config=config, logger=logger)
        except RuntimeError as e:
            logger.info(f"[AppContext] ChandraAPIOCREngine not available: {e}")
        else:
            engines[chandra_engine.name()] = chandra_engine

        router = EngineRouter(engines=engines)

        return cls(
            config=config,
            logger=logger,
            ocr_engines=engines,
            router=router,
        )

    def get_ocr(self, name: str) -> OCREngine:
        if name not in self.ocr_engines:
            raise ValueError(
                f"OCR engine not registered: {name}. "
                f"Available: {', '.join(self.ocr_engines.keys())}"
            )
        return self.ocr_engines[name]

    def list_ocr_engines(self) -> Dict[str, OCREngine]:
        return dict(self.ocr_engines)
    
    def resolve_engine(self, name_or_strategy: str) -> OCREngine:
        """
        Resolve either:
        - a concrete engine name (stub, paddle, chandra-api)
        - a routing strategy (light, heavy, auto)
        """
        key = name_or_strategy.lower()
        if key in self.ocr_engines:
            return self.ocr_engines[key]

        if key in {"light", "heavy", "auto"}:
            return self.router.select(key)

        raise ValueError(
            f"Unknown OCR engine or strategy: {name_or_strategy!r}. "
            f"Available engines: {', '.join(self.ocr_engines.keys())}; "
            f"strategies: light, heavy, auto."
        )
