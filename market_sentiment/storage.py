from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import DailyMarketSentiment


class JsonlStorage:
    def __init__(self, path: str = "data/sentiment_history.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, snapshot: DailyMarketSentiment) -> None:
        payload = asdict(snapshot)
        payload["timestamp"] = snapshot.timestamp.isoformat()

        # simplify nested datetime serialization
        for item in payload.get("details", []):
            pub = item["item"].get("published_at")
            item["item"]["published_at"] = pub.isoformat() if pub else None

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
