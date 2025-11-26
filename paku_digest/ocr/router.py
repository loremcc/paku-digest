from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .base import OCREngine


@dataclass
class EngineRouter:
    """
    Routing logic for OCR engines.

    Supports strategies:
    - 'light'  → prefer light engines
    - 'heavy'  → prefer heavy engines
    - 'auto'   → prefer heavy if healthy, fallback to light
    """

    engines: Dict[str, OCREngine]

    def _select_by_kind(self, kind: str) -> OCREngine | None:
        """
        Return the first healthy engine of the given kind, or None.
        kind: 'light' | 'heavy'
        """
        candidates = [
            e
            for e in self.engines.values()
            if e.kind() == kind and e.is_healthy()
        ]
        if not candidates:
            return None
        return candidates[0]

    def select(self, strategy: str) -> OCREngine:
        """
        Select an engine based on a routing strategy:
        - 'light'
        - 'heavy'
        - 'auto'
        """
        strategy = strategy.lower()

        if strategy == "light":
            engine = self._select_by_kind("light")
            if engine is not None:
                return engine
            engine = self._select_by_kind("heavy")
            if engine is not None:
                return engine
            raise RuntimeError("No OCR engines available for strategy 'light'.")

        if strategy == "heavy":
            engine = self._select_by_kind("heavy")
            if engine is not None:
                return engine
            engine = self._select_by_kind("light")
            if engine is not None:
                return engine
            raise RuntimeError("No OCR engines available for strategy 'heavy'.")

        if strategy == "auto":
            heavy = self._select_by_kind("heavy")
            if heavy is not None:
                return heavy
            light = self._select_by_kind("light")
            if light is not None:
                return light
            raise RuntimeError("No OCR engines available for strategy 'auto'.")

        raise ValueError(f"Unknown routing strategy: {strategy!r}")
