from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import OcrResult


class OCREngine(ABC):
    """Base interface for all OCR engines used by paku-digest."""

    @abstractmethod
    def name(self) -> str:
        """Human-readble, unique engine name (e.g. 'stub', 'paddle', 'chandra-api')"""
        raise NotImplementedError
    
    @abstractmethod
    def extract(self, path: Path) -> OcrResult:
        """
        Run OCR on a single image file and return a unified OcrResult.

        Implementations must:
        - not mutate the input path
        - return a fully-populated OcrResult (engine, raw_text, blocks, meta, ...)
        """
        raise NotImplementedError
