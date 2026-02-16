from bot3.polymarket_client import MarketSnapshot
from bot3.strategy import OpportunityStrategy


def test_rank_filters_and_orders() -> None:
    snapshots = [
        MarketSnapshot("1", "A", 0.52, 0.45, 0.03, 20_000, 60_000, None),
        MarketSnapshot("2", "B", 0.80, 0.15, 0.05, 5_000, 8_000, None),
        MarketSnapshot("3", "C", 0.49, 0.48, 0.03, 30_000, 100_000, None),
    ]
    strategy = OpportunityStrategy(min_liquidity=10_000, min_volume=10_000, max_spread=0.1)
    ranked = strategy.rank(snapshots, top_n=5)

    assert [item.snapshot.market_id for item in ranked] == ["3", "1"]
    assert ranked[0].score >= ranked[1].score
