from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from typing import Iterable, Literal

from ..models import Document

ExportFormat = Literal["json", "jsonl", "txt", "csv"]


def export_documents_to_string(
    documents: Iterable[Document],
    fmt: ExportFormat,
) -> str:
    """
    Render a collection of Document models into a text representation
    in the given format.

    Supported formats:
    - json   : pretty JSON array
    - jsonl  : one JSON object per line
    - txt    : one line per document (anime title/url per line style)
    - csv    : tabular export (one row per document)
    """
    docs_list = list(documents)

    # ---------- JSON ----------
    if fmt == "json":
        payload = [d.model_dump(mode="json") for d in docs_list]
        return json.dumps(payload, ensure_ascii=False, indent=2)

    # ---------- JSONL ----------
    if fmt == "jsonl":
        lines = []
        for d in docs_list:
            payload = d.model_dump(mode="json")
            lines.append(json.dumps(payload, ensure_ascii=False))
        return "\n".join(lines) + ("\n" if lines else "")

    # ---------- TXT ----------
    if fmt == "txt":
        lines = []
        for d in docs_list:
            raw_text = ""
            if d.ocr and d.ocr.raw_text is not None:
                raw_text = str(d.ocr.raw_text)
            raw_text = " ".join(raw_text.split())
            if raw_text:
                lines.append(raw_text)
        return "\n".join(lines) + ("\n" if lines else "")

    # ---------- CSV ----------
    if fmt == "csv":
        import csv

        buf = StringIO()
        writer = csv.writer(buf)

        header = ["path", "engine", "language", "raw_text"]
        writer.writerow(header)

        for d in docs_list:
            engine = d.ocr.engine if d.ocr is not None else ""
            language = d.ocr.language if (d.ocr is not None and d.ocr.language is not None) else ""
            raw_text = ""
            if d.ocr and d.ocr.raw_text is not None:
                raw_text = str(d.ocr.raw_text)
            writer.writerow([str(d.path), engine, language, raw_text])

        return buf.getvalue()


def export_documents_to_file(
    documents: Iterable[Document],
    fmt: ExportFormat,
    out_path: Path,
) -> None:
    """
    Export documents into a file in the given format.
    """
    text = export_documents_to_string(documents, fmt=fmt)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
