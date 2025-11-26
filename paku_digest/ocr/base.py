from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import OcrResult


class OCREngine(ABC):
    """Base interface for all OCR engines used by paku-digest."""

    @abstractmethod
    def name(self) -> str:
        """Unique engine name (e.g. 'stub', 'paddle', 'chandra-api')."""
        raise NotImplementedError
    
    @abstractmethod
    def extract(self, path: Path) -> OcrResult:
        """Run OCR on a single image file and return a unified OcrResult."""
        raise NotImplementedError

    def kind(self) -> str:
        """
        Engine kind of routing: 'light' or 'heavy'.

        Default is 'light'. Heavy engines are more accurate but slower or more
        expensive
        """
        return "light"
    
    def is_healthy(self) -> bool:
        """Best-effort health indicator for routing."""
        return True