from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class NewsItem:
    source: str
    title: str
    summary: str
    url: str
    published_at: datetime | None
    source_weight: float = 1.0

    @property
    def text(self) -> str:
        return f"{self.title}. {self.summary}".strip()


@dataclass(slots=True)
class SentimentResult:
    item: NewsItem
    raw_score: float
    normalized_score: float
    confidence: float


@dataclass(slots=True)
class DailyMarketSentiment:
    timestamp: datetime
    score: float
    label: str
    sample_size: int
    details: list[SentimentResult]
