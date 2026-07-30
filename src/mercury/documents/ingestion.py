import hashlib
import json
from pathlib import Path

from pydantic import ValidationError

from mercury.documents.models import (
    FinancialDocument,
    RawFinancialDocument,
)


class DocumentIngestionError(Exception):
    """Raised when a document cannot be ingested."""


def normalize_whitespace(text: str) -> str:
    """Replace repeated spaces and line breaks with single spaces."""

    return " ".join(text.split())


def normalize_symbols(symbols: list[str]) -> list[str]:
    """Uppercase, remove blanks, remove duplicates, and sort symbols."""

    normalized = {
        symbol.strip().upper()
        for symbol in symbols
        if symbol.strip()
    }

    return sorted(normalized)


def create_document_id(document: RawFinancialDocument) -> str:
    """Create a repeatable ID from the document's important content."""

    identity_data = {
        "document_type": document.document_type.value,
        "title": document.title,
        "body": document.body,
        "source": document.source,
        "published_at": document.published_at.isoformat(),
    }

    serialized = json.dumps(
        identity_data,
        sort_keys=True,
        ensure_ascii=False,
    )

    digest = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()[:20]

    return f"{document.document_type.value}-{digest}"


def load_raw_document(file_path: Path) -> RawFinancialDocument:
    """Read and validate a raw JSON document."""

    try:
        raw_text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise DocumentIngestionError(
            f"Document file not found: {file_path}"
        ) from exc
    except OSError as exc:
        raise DocumentIngestionError(
            f"Could not read document file: {file_path}"
        ) from exc

    try:
        raw_data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise DocumentIngestionError(
            f"Invalid JSON in file {file_path}: {exc.msg}"
        ) from exc

    try:
        return RawFinancialDocument.model_validate(raw_data)
    except ValidationError as exc:
        raise DocumentIngestionError(
            f"Document validation failed: {exc}"
        ) from exc


def standardize_document(
    raw_document: RawFinancialDocument,
) -> FinancialDocument:
    """Clean a raw document and convert it into Mercury's format."""

    cleaned_document = RawFinancialDocument(
        document_type=raw_document.document_type,
        title=normalize_whitespace(raw_document.title),
        body=normalize_whitespace(raw_document.body),
        source=normalize_whitespace(raw_document.source),
        source_url=(
            raw_document.source_url.strip()
            if raw_document.source_url
            else None
        ),
        published_at=raw_document.published_at,
        symbols=normalize_symbols(raw_document.symbols),
    )

    document_id = create_document_id(cleaned_document)

    return FinancialDocument(
        document_id=document_id,
        document_type=cleaned_document.document_type,
        title=cleaned_document.title,
        body=cleaned_document.body,
        source=cleaned_document.source,
        source_url=cleaned_document.source_url,
        published_at=cleaned_document.published_at,
        symbols=cleaned_document.symbols,
    )


def save_document(
    document: FinancialDocument,
    output_directory: Path,
) -> Path:
    """Save a standardized document as JSON."""

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory / f"{document.document_id}.json"
    )

    output_path.write_text(
        document.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )

    return output_path


def ingest_document(
    input_path: Path,
    output_directory: Path,
) -> Path:
    """Run the complete ingestion pipeline."""

    raw_document = load_raw_document(input_path)
    standardized_document = standardize_document(raw_document)

    return save_document(
        standardized_document,
        output_directory,
    )