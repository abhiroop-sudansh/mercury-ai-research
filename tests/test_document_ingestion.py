import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from mercury.documents.ingestion import (
    DocumentIngestionError,
    create_document_id,
    ingest_document,
    normalize_symbols,
    normalize_whitespace,
    standardize_document,
)
from mercury.documents.models import (
    DocumentType,
    RawFinancialDocument,
)


def create_raw_document() -> RawFinancialDocument:
    return RawFinancialDocument(
        document_type=DocumentType.EARNINGS_RELEASE,
        title="  NVIDIA   Quarterly Results  ",
        body="Revenue increased.\n\n  Guidance improved.",
        source="  NVIDIA Investor Relations ",
        source_url="https://example.com/results",
        published_at=datetime(
            2025,
            5,
            28,
            20,
            0,
            tzinfo=timezone.utc,
        ),
        symbols=["nvda", " NVDA ", "amd", ""],
    )


def test_normalize_whitespace() -> None:
    result = normalize_whitespace(
        "Revenue   increased.\n\nGuidance improved."
    )

    assert result == "Revenue increased. Guidance improved."


def test_normalize_symbols() -> None:
    result = normalize_symbols(
        ["nvda", " NVDA ", "amd", ""]
    )

    assert result == ["AMD", "NVDA"]


def test_same_document_generates_same_id() -> None:
    raw_document = create_raw_document()

    first_id = create_document_id(raw_document)
    second_id = create_document_id(raw_document)

    assert first_id == second_id


def test_standardize_document() -> None:
    document = standardize_document(
        create_raw_document()
    )

    assert document.title == "NVIDIA Quarterly Results"
    assert document.body == (
        "Revenue increased. Guidance improved."
    )
    assert document.source == "NVIDIA Investor Relations"
    assert document.symbols == ["AMD", "NVDA"]
    assert document.document_id.startswith(
        "earnings_release-"
    )


def test_ingest_document_saves_json(
    tmp_path: Path,
) -> None:
    input_path = tmp_path / "raw.json"
    output_directory = tmp_path / "processed"

    raw_data = {
        "document_type": "news",
        "title": "Example article",
        "body": "Example financial news body.",
        "source": "Example News",
        "published_at": "2025-05-28T20:00:00Z",
        "symbols": ["NVDA"],
    }

    input_path.write_text(
        json.dumps(raw_data),
        encoding="utf-8",
    )

    output_path = ingest_document(
        input_path=input_path,
        output_directory=output_directory,
    )

    assert output_path.exists()

    saved_data = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    assert saved_data["title"] == "Example article"
    assert saved_data["symbols"] == ["NVDA"]
    assert saved_data["document_id"].startswith("news-")


def test_missing_file_raises_error(
    tmp_path: Path,
) -> None:
    missing_path = tmp_path / "missing.json"

    with pytest.raises(DocumentIngestionError):
        ingest_document(
            input_path=missing_path,
            output_directory=tmp_path / "processed",
        )