from __future__ import annotations

from pathlib import Path

from .base import OCREngine
from ..config import AppConfig
from ..models import OcrResult


class ChandraAPIOCREngine(OCREngine):
    """
    Placeholder for Chandra OCR via API.

    This is designed to work with any OpenAI-compatible endpoint
    (e.g., Chandra, vLLM, llamafile server, OpenAI-style gateway, etc.)
    but is *not configured* until the user sets:

        PAKU_CHANDRA_API_URL
        PAKU_CHANDRA_API_KEY

    in the .env file.

    For now, it simply raises a clear RuntimeError. Later we will fill in:
    - HTTP request (async or sync)
    - model selection & OCR prompt
    - response parsing into OcrResult
    """

    def __init__(self, config: AppConfig, logger) -> None:
        self._config = config
        self._logger = logger

        if not (config.chandra_api_url and config.chandra_api_key):
            raise RuntimeError(
                "ChandraAPIOCREngine not configured.\n"
                "Missing PAKU_CHANDRA_API_URL or PAKU_CHANDRA_API_KEY in .env.\n"
                "Example:\n"
                "    PAKU_CHANDRA_API_URL=http://localhost:8000/v1/\n"
                "    PAKU_CHANDRA_API_KEY=yourkey\n"
            )

        # When configured:
        # self._endpoint = config.chandra_api_url.rstrip("/")
        # self._api_key = config.chandra_api_key

    def name(self) -> str:
        return "chandra-api"

    def extract(self, path: Path) -> OcrResult:
        """
        Placeholder implementation: raises a clear message.

        Once implemented, this method will:
        - send the image as base64 or multipart/form-data
        - receive structured OCR text
        - create and return OcrResult
        """
        raise RuntimeError(
            "ChandraAPIOCREngine.extract() called but the engine is not implemented yet.\n"
            "This is a placeholder. When API configuration and server are ready, "
            "the OCR request logic will be added here."
        )
