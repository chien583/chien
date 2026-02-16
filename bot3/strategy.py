from __future__ import annotations

from dataclasses import dataclass

from bot3.polymarket_client import MarketSnapshot


@dataclass
class ScoredOpportunity:
    snapshot: MarketSnapshot
    score: float
    reason: str


class OpportunityStrategy:
    """基于流动性、成交量、价差筛选可关注市场。"""

    def __init__(
        self,
        *,
        min_liquidity: float = 5_000,
        min_volume: float = 1_000,
        max_spread: float = 0.25,
    ) -> None:
        self.min_liquidity = min_liquidity
        self.min_volume = min_volume
        self.max_spread = max_spread

    def rank(self, snapshots: list[MarketSnapshot], *, top_n: int = 10) -> list[ScoredOpportunity]:
        opportunities: list[ScoredOpportunity] = []
        for snap in snapshots:
            if snap.liquidity < self.min_liquidity:
                continue
            if snap.volume < self.min_volume:
                continue
            if snap.spread > self.max_spread:
                continue

            score = self._score(snap)
            reason = (
                f"liquidity={snap.liquidity:.0f}, volume={snap.volume:.0f}, "
                f"spread={snap.spread:.3f}"
            )
            opportunities.append(ScoredOpportunity(snapshot=snap, score=score, reason=reason))

        return sorted(opportunities, key=lambda x: x.score, reverse=True)[:top_n]

    def _score(self, snap: MarketSnapshot) -> float:
        liquidity_score = min(snap.liquidity / 50_000, 1.0)
        volume_score = min(snap.volume / 20_000, 1.0)
        spread_score = max(0.0, 1 - (snap.spread / max(self.max_spread, 0.01)))
        price_balance = 1 - abs(snap.yes_price - 0.5) * 2
        return round(
            liquidity_score * 0.35
            + volume_score * 0.35
            + spread_score * 0.2
            + price_balance * 0.1,
            4,
        )
