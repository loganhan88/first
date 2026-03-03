from market_sentiment.collectors import RSSCollector


def test_collector_build_item_from_dict_entry():
    collector = RSSCollector(max_articles_per_source=5)
    source = {"name": "Demo", "weight": 1.5}
    entry = {
        "title": "Stocks rally",
        "summary": "<p>profit growth</p>",
        "link": "https://example.com/a",
        "published": "Mon, 02 Mar 2026 10:00:00 GMT",
    }

    item = collector._build_item(source, entry)

    assert item.source == "Demo"
    assert item.source_weight == 1.5
    assert item.title == "Stocks rally"
    assert item.summary == "profit growth"
    assert item.url == "https://example.com/a"
    assert item.published_at is not None
