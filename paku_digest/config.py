from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class AppConfig:
    env: str
    log_level: str
    default_ocr: str
    workdir: Path
    paddle_lang: str

    # Chandra API (temporary config)
    chandra_api_url: str | None = None
    chandra_api_key: str | None = None

    @classmethod
    def from_env(cls) -> "AppConfig":
        load_dotenv()

        env = os.getenv("PAKU_ENV", "local")
        log_level = os.getenv("PAKU_LOG_LEVEL", "INFO")
        default_ocr = os.getenv("PAKU_DEFAULT_OCR", "stub")
        workdir = Path(os.getenv("PAKU_WORKDIR", ".")).resolve()
        paddle_lang = os.getenv("PAKU_PADDLE_LANG", "en")

        chandra_api_url = os.getenv("PAKU_CHANDRA_API_URL")
        chandra_api_key = os.getenv("PAKU_CHANDRA_API_KEY")

        cfg = cls(
                env=env,
                log_level=log_level,
                default_ocr=default_ocr,
                workdir=workdir,
                paddle_lang=paddle_lang,
                chandra_api_url=chandra_api_url,
                chandra_api_key=chandra_api_key,
            )

        cfg.validate()
        return cfg

        # -----------------------------------------
        # Validation logic
        # -----------------------------------------
        def validate(self) -> None:
            """
            Validate essential environment configuration.
            Raises ValueError with helpful messages on invalid config.
            """

            # Required fields
            if not self.env:
                raise ValueError("Environment variable PAKU_ENV is required.")

            if self.default_ocr not in {"stub", "paddle", "chandra-api"}:
                raise ValueError(
                    f"Invalid PAKU_DEFAULT_OCR='{self.default_ocr}'. "
                    "Must be one of: stub, paddle, chandra-api"
                )

            if not isinstance(self.workdir, Path):
                raise ValueError("PAKU_WORKDIR must be a valid filesystem path.")

            # Optional validation for Chandra
            if self.default_ocr == "chandra-api":
                if not self.chandra_api_url:
                    raise ValueError(
                        "PAKU_CHANDRA_API_URL is required when PAKU_DEFAULT_OCR=chandra-api"
                    )
                if not self.chandra_api_key:
                    raise ValueError(
                        "PAKU_CHANDRA_API_KEY is required when PAKU_DEFAULT_OCR=chandra-api"
                    )