from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime

import feedparser
from bs4 import BeautifulSoup

from .models import NewsItem


class RSSCollector:
    def __init__(self, max_articles_per_source: int = 30) -> None:
        self.max_articles_per_source = max_articles_per_source

    def collect(self, source: dict) -> list[NewsItem]:
        feed = feedparser.parse(source["url"])
        items: list[NewsItem] = []

        for entry in feed.entries[: self.max_articles_per_source]:
            summary_html = entry.get("summary", "")
            summary = BeautifulSoup(summary_html, "html.parser").get_text(" ", strip=True)

            published_raw = entry.get("published") or entry.get("updated")
            published_at = self._parse_datetime(published_raw)

            items.append(
                NewsItem(
                    source=source.get("name", "Unknown"),
                    title=entry.get("title", "").strip(),
                    summary=summary,
                    url=entry.get("link", ""),
                    published_at=published_at,
                    source_weight=float(source.get("weight", 1.0)),
                )
            )

        return items

    @staticmethod
    def _parse_datetime(raw: str | None) -> datetime | None:
        if not raw:
            return None
        try:
            return parsedate_to_datetime(raw)
        except Exception:
            return None
