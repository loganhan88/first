from __future__ import annotations

from statistics import fmean

from .models import DailyMarketSentiment, SentimentResult


class MarketScorer:
    def __init__(self, score_bands: dict | None = None) -> None:
        self.score_bands = score_bands or {
            "very_bearish": -60,
            "bearish": -20,
            "neutral": 20,
            "bullish": 60,
        }

    def aggregate(self, results: list[SentimentResult]) -> DailyMarketSentiment:
        if not results:
            from datetime import datetime

            return DailyMarketSentiment(
                timestamp=datetime.utcnow(),
                score=0.0,
                label="neutral",
                sample_size=0,
                details=[],
            )

        weighted_scores = [
            r.normalized_score * r.item.source_weight * max(0.1, r.confidence) for r in results
        ]
        overall = fmean(weighted_scores) * 100
        label = self._to_label(overall)

        from datetime import datetime

        return DailyMarketSentiment(
            timestamp=datetime.utcnow(),
            score=round(overall, 2),
            label=label,
            sample_size=len(results),
            details=results,
        )

    def _to_label(self, score: float) -> str:
        if score <= self.score_bands["very_bearish"]:
            return "very_bearish"
        if score <= self.score_bands["bearish"]:
            return "bearish"
        if score < self.score_bands["neutral"]:
            return "neutral"
        if score < self.score_bands["bullish"]:
            return "bullish"
        return "very_bullish"
