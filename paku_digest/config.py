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

    @classmethod
    def from_env(cls) -> "AppConfig":
        load_dotenv()

        env = os.getenv("PAKU_ENV", "local")
        log_level = os.getenv("PAKU_LOG_LEVEL", "INFO")
        default_ocr = os.getenv("PAKU_DEFAULT_OCR", "stub")
        workdir = Path(os.getenv("PAKU_WORKDIR", ".")).resolve()
        paddle_lang = os.getenv("PAKU_PADDLE_LANG", "en")

        return cls(
            env=env,
            log_level=log_level,
            default_ocr=default_ocr,
            workdir=workdir,
            paddle_lang=paddle_lang,
        )
    