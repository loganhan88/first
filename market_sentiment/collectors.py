from __future__ import annotations

from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from .models import NewsItem

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover
    BeautifulSoup = None

try:
    import feedparser  # type: ignore
except Exception:  # pragma: no cover
    feedparser = None


class RSSCollector:
    def __init__(self, max_articles_per_source: int = 30) -> None:
        self.max_articles_per_source = max_articles_per_source

    def collect(self, source: dict) -> list[NewsItem]:
        if feedparser is not None:
            return self._collect_with_feedparser(source)
        return self._collect_with_stdlib(source)

    def _collect_with_feedparser(self, source: dict) -> list[NewsItem]:
        feed = feedparser.parse(source["url"])
        items: list[NewsItem] = []

        for entry in feed.entries[: self.max_articles_per_source]:
            items.append(self._build_item(source, entry))

        return items

    def _collect_with_stdlib(self, source: dict) -> list[NewsItem]:
        with urlopen(source["url"], timeout=20) as response:
            payload = response.read()

        root = ET.fromstring(payload)
        entries: list[dict[str, Any]] = []

        for item in root.findall("./channel/item")[: self.max_articles_per_source]:
            entries.append(
                {
                    "title": (item.findtext("title") or "").strip(),
                    "summary": item.findtext("description") or "",
                    "link": item.findtext("link") or "",
                    "published": item.findtext("pubDate") or item.findtext("published"),
                    "updated": item.findtext("updated"),
                }
            )

        if not entries:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for item in root.findall("./atom:entry", ns)[: self.max_articles_per_source]:
                summary_node = item.find("atom:summary", ns)
                link_node = item.find("atom:link", ns)
                entries.append(
                    {
                        "title": (item.findtext("atom:title", default="", namespaces=ns) or "").strip(),
                        "summary": summary_node.text if summary_node is not None else "",
                        "link": link_node.attrib.get("href", "") if link_node is not None else "",
                        "published": item.findtext("atom:published", default=None, namespaces=ns),
                        "updated": item.findtext("atom:updated", default=None, namespaces=ns),
                    }
                )

        return [self._build_item(source, entry) for entry in entries]

    def _build_item(self, source: dict, entry: Any) -> NewsItem:
        summary_html = self._entry_get(entry, "summary", "")
        summary = self._html_to_text(summary_html)

        published_raw = self._entry_get(entry, "published") or self._entry_get(entry, "updated")
        published_at = self._parse_datetime(published_raw)

        return NewsItem(
            source=source.get("name", "Unknown"),
            title=self._entry_get(entry, "title", "").strip(),
            summary=summary,
            url=self._entry_get(entry, "link", ""),
            published_at=published_at,
            source_weight=float(source.get("weight", 1.0)),
        )


    @staticmethod
    def _html_to_text(value: str) -> str:
        if not value:
            return ""
        if BeautifulSoup is not None:
            return BeautifulSoup(value, "html.parser").get_text(" ", strip=True)
        # fallback: very lightweight HTML tag strip
        import re

        no_tag = re.sub(r"<[^>]+>", " ", value)
        return re.sub(r"\s+", " ", no_tag).strip()

    @staticmethod
    def _entry_get(entry: Any, key: str, default: str | None = None) -> str:
        if isinstance(entry, dict):
            return entry.get(key, default) or ""
        return entry.get(key, default) or ""

    @staticmethod
    def _parse_datetime(raw: str | None) -> datetime | None:
        if not raw:
            return None
        try:
            return parsedate_to_datetime(raw)
        except Exception:
            return None
