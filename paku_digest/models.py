from __future__ import annotations

from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class OcrBlock(BaseModel):
    text:str
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: Optional[BoundingBox] = None
    type: Literal["line", "word", "paragraph"] = "line"


class OcrResult(BaseModel):
    engine: str
    raw_text: str
    blocks: List[OcrBlock] = Field(default_factory=list)
    language: Optional[str] = None
    meta: dict = Field(default_factory=dict)


class Document(BaseModel):
    path: Path
    ocr: Optional[OcrResult] = None
