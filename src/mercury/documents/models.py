from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DocumentType(StrEnum):
    """Supported categories of financial documents."""

    EARNINGS_RELEASE = "earnings_release"
    SEC_FILING = "sec_filing"
    NEWS = "news"
    TRANSCRIPT = "transcript"


class FinancialDocument(BaseModel):
    """Standard structure used for every financial document."""

    document_id: str = Field(min_length=1)
    document_type: DocumentType
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    source: str = Field(min_length=1)
    source_url: str | None = None
    published_at: datetime
    symbols: list[str] = Field(default_factory=list)