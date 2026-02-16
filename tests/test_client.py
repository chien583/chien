from bot3.polymarket_client import PolymarketClient


def test_build_snapshots_handles_invalid_price() -> None:
    client = PolymarketClient()
    markets = [
        {
            "id": "x1",
            "question": "Sample",
            "outcomePrices": ["0.42", "oops"],
            "volume": "1200",
            "liquidity": "34000",
            "endDate": "2026-10-01T00:00:00Z",
        }
    ]

    snapshots = client.build_snapshots(markets)
    assert len(snapshots) == 1
    snap = snapshots[0]
    assert snap.yes_price == 0.42
    assert snap.no_price == 0.0
    assert round(snap.spread, 2) == 0.58
