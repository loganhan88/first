from __future__ import annotations

import math
import re


POSITIVE_TERMS = {
    "rally",
    "growth",
    "beat",
    "optimism",
    "surge",
    "bull",
    "profit",
    "recovery",
    "upgrade",
    "strong",
    "上涨",
    "反弹",
    "增长",
    "利好",
    "乐观",
    "牛市",
    "盈利",
}

NEGATIVE_TERMS = {
    "selloff",
    "recession",
    "fear",
    "downgrade",
    "loss",
    "crisis",
    "bear",
    "weak",
    "decline",
    "drop",
    "下跌",
    "衰退",
    "悲观",
    "利空",
    "亏损",
    "暴跌",
    "风险",
}


class LexiconSentimentAnalyzer:
    """轻量级金融情绪分析器（中英双语关键词）。"""

    token_pattern = re.compile(r"[A-Za-z]+|[\u4e00-\u9fff]{1,4}")

    def score(self, text: str) -> tuple[float, float]:
        if not text:
            return 0.0, 0.0

        tokens = [tok.lower() for tok in self.token_pattern.findall(text)]
        if not tokens:
            return 0.0, 0.0

        pos_hits = sum(1 for t in tokens if t in POSITIVE_TERMS)
        neg_hits = sum(1 for t in tokens if t in NEGATIVE_TERMS)

        raw = pos_hits - neg_hits
        magnitude = pos_hits + neg_hits

        if magnitude == 0:
            return 0.0, 0.15

        normalized = math.tanh(raw / max(2, magnitude))
        confidence = min(1.0, 0.3 + magnitude / 10)
        return normalized, confidence
