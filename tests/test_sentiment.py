from market_sentiment.analyzer import LexiconSentimentAnalyzer
from market_sentiment.models import NewsItem, SentimentResult
from market_sentiment.scorer import MarketScorer


def test_analyzer_detects_positive():
    analyzer = LexiconSentimentAnalyzer()
    score, conf = analyzer.score("Stocks rally as growth and profit improve, 市场乐观反弹")
    assert score > 0
    assert conf > 0.3


def test_analyzer_detects_negative():
    analyzer = LexiconSentimentAnalyzer()
    score, conf = analyzer.score("Markets drop amid recession fear and 暴跌风险")
    assert score < 0
    assert conf > 0.3


def test_market_scorer_label():
    scorer = MarketScorer()
    item = NewsItem(
        source="t",
        title="",
        summary="",
        url="",
        published_at=None,
        source_weight=1.0,
    )
    results = [
        SentimentResult(item=item, raw_score=0.0, normalized_score=0.9, confidence=1.0),
        SentimentResult(item=item, raw_score=0.0, normalized_score=0.8, confidence=1.0),
    ]
    daily = scorer.aggregate(results)
    assert daily.score > 60
    assert daily.label == "very_bullish"
