from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from mercury.documents.models import DocumentType, FinancialDocument


def test_create_valid_financial_document() -> None:
    document = FinancialDocument(
        document_id="nvda-2025-q1-earnings",
        document_type=DocumentType.EARNINGS_RELEASE,
        title="NVIDIA Announces Quarterly Results",
        body="NVIDIA reported quarterly revenue growth.",
        source="NVIDIA Investor Relations",
        source_url="https://example.com/nvda-results",
        published_at=datetime(
            2025,
            5,
            28,
            20,
            0,
            tzinfo=timezone.utc,
        ),
        symbols=["NVDA"],
    )

    assert document.document_id == "nvda-2025-q1-earnings"
    assert document.document_type == DocumentType.EARNINGS_RELEASE
    assert document.symbols == ["NVDA"]


def test_document_rejects_empty_body() -> None:
    with pytest.raises(ValidationError):
        FinancialDocument(
            document_id="invalid-document",
            document_type=DocumentType.NEWS,
            title="Example title",
            body="",
            source="Example source",
            published_at=datetime.now(timezone.utc),
            symbols=["NVDA"],
        )