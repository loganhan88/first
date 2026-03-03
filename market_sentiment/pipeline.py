from __future__ import annotations

import logging
from typing import Iterable

from .analyzer import LexiconSentimentAnalyzer
from .collectors import RSSCollector
from .config import load_config
from .models import NewsItem, SentimentResult
from .scorer import MarketScorer
from .storage import JsonlStorage


logger = logging.getLogger(__name__)


class SentimentPipeline:
    def __init__(self, config_path: str = "config/sources.yaml") -> None:
        self.config = load_config(config_path)
        self.collector = RSSCollector(
            max_articles_per_source=int(self.config.get("max_articles_per_source", 30))
        )
        self.analyzer = LexiconSentimentAnalyzer()
        self.scorer = MarketScorer(score_bands=self.config.get("score_bands"))
        self.storage = JsonlStorage()

    def run_once(self):
        news_items = self._collect_all_sources(self.config["sources"])
        results: list[SentimentResult] = []

        for item in news_items:
            normalized, confidence = self.analyzer.score(item.text)
            results.append(
                SentimentResult(
                    item=item,
                    raw_score=normalized,
                    normalized_score=normalized,
                    confidence=confidence,
                )
            )

        daily = self.scorer.aggregate(results)
        self.storage.save(daily)

        logger.info(
            "Sentiment computed: score=%s label=%s samples=%s",
            daily.score,
            daily.label,
            daily.sample_size,
        )
        return daily

    def _collect_all_sources(self, sources: Iterable[dict]) -> list[NewsItem]:
        collected: list[NewsItem] = []
        for source in sources:
            if source.get("type") != "rss":
                logger.warning("Skip source '%s': unsupported type", source.get("name"))
                continue

            try:
                items = self.collector.collect(source)
                collected.extend(items)
                logger.info("Collected %s items from %s", len(items), source.get("name"))
            except Exception as exc:
                logger.exception("Failed collecting source %s: %s", source.get("name"), exc)

        return collected
