from __future__ import annotations

import json
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class CompareResult:
    path: str
    left_text: Optional[str]
    right_text: Optional[str]
    exact_equal: bool
    similarity: float
    left_missing: bool
    right_missing: bool


def _load_documents(path: Path) -> Dict[str, Any]:
    """
    Load a digest JSON output and index by document path.

    Expected format (current digest output):
        [
            {
                "path": "...",
                "ocr": { "raw_text": "...", ... }
            },
            ...
        ]
    Returns: { path_str -> document_dict }
    """
    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of documents in {path}, got {type(data)}")

    by_path: Dict[str, Any] = {}
    for item in data:
        p = item.get("path")
        if not p:
            continue
        by_path[str(p)] = item
    return by_path


def _extract_text(doc: Optional[dict]) -> Optional[str]:
    if not doc:
        return None
    ocr = doc.get("ocr")
    if not isinstance(ocr, dict):
        return None
    text = ocr.get("raw_text")
    if text is None:
        return None
    return str(text)


def _similarity(a: str, b: str) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def run_compare(left: Path, right: Path) -> dict:
    """
    Compare two digest JSON outputs.

    For each path in the union of both sides:
    - extract OCR raw_text
    - compute exact equality
    - compute similarity ratio [0, 1]
    - mark missing on left/right

    Returns a JSON-serializable dict with:
    - summary (counts, averages)
    - per_path results
    """
    left_docs = _load_documents(left)
    right_docs = _load_documents(right)

    all_paths = sorted(set(left_docs.keys()) | set(right_docs.keys()))

    results: List[CompareResult] = []

    for p in all_paths:
        ldoc = left_docs.get(p)
        rdoc = right_docs.get(p)

        ltext = _extract_text(ldoc)
        rtext = _extract_text(rdoc)

        left_missing = ldoc is None
        right_missing = rdoc is None

        if ltext is None and rtext is None:
            sim = 1.0
            exact = True
        else:
            sim = _similarity(ltext or "", rtext or "")
            exact = (ltext == rtext)

        results.append(
            CompareResult(
                path=p,
                left_text=ltext,
                right_text=rtext,
                exact_equal=exact,
                similarity=sim,
                left_missing=left_missing,
                right_missing=right_missing,
            )
        )

    # Summary statistics
    total = len(results)
    exact_count = sum(1 for r in results if r.exact_equal)
    sim_sum = sum(r.similarity for r in results)
    avg_similarity = sim_sum / total if total else 0.0

    high_similar = sum(1 for r in results if r.similarity >= 0.9)
    left_only = sum(1 for r in results if r.left_missing and not r.right_missing)
    right_only = sum(1 for r in results if r.right_missing and not r.left_missing)

    return {
        "left_source": str(left),
        "right_source": str(right),
        "total_paths": total,
        "exact_equal_count": exact_count,
        "avg_similarity": avg_similarity,
        "high_similarity_count": high_similar,
        "left_only_count": left_only,
        "right_only_count": right_only,
        "per_path": [
            {
                "path": r.path,
                "exact_equal": r.exact_equal,
                "similarity": r.similarity,
                "left_missing": r.left_missing,
                "right_missing": r.right_missing,
                "left_text": r.left_text,
                "right_text": r.right_text,
            }
            for r in results
        ],
    }
