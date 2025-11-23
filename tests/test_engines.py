from pathlib import Path

from paku_digest.context import AppContext
from paku_digest.models import Document, OcrResult


def test_stub_engine_registered():
    ctx = AppContext.instance()
    engines = ctx.list_ocr_engines()
    assert "stub" in engines
    stub = engines["stub"]
    assert stub.name() == "stub"


def test_stub_engine_extract_returns_ocrresult(tmp_path: Path):
    # create a dummy file to simulate an image
    img = tmp_path / "dummy.png"
    img.write_bytes(b"not-a-real-image")

    ctx = AppContext.instance()
    stub = ctx.get_ocr("stub")
    result = stub.extract(img)

    assert isinstance(result, OcrResult)
    assert result.engine == "stub"
    assert "dummy.png" in result.raw_text


def test_digest_pipeline_runs_with_stub(tmp_path: Path):
    from paku_digest.pipelines.digest_pipeline import run_digest

    img = tmp_path / "dummy.png"
    img.write_bytes(b"fake")

    docs = run_digest(input_path=tmp_path, ocr_engine_name="stub")
    assert len(docs) == 1
    doc = docs[0]
    assert isinstance(doc, Document)
    assert doc.path.name == "dummy.png"
    assert doc.ocr is not None
    assert doc.ocr.engine == "stub"
