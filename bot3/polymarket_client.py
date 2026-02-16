from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable
import json
from urllib.parse import urlencode
from urllib.request import urlopen


@dataclass
class MarketSnapshot:
    market_id: str
    question: str
    yes_price: float
    no_price: float
    spread: float
    volume: float
    liquidity: float
    end_date_iso: str | None


class PolymarketClient:
    """简单的 Polymarket Gamma API 客户端。"""

    def __init__(self, base_url: str = "https://gamma-api.polymarket.com") -> None:
        self.base_url = base_url.rstrip("/")

    def get_markets(self, *, limit: int = 50, active: bool = True, closed: bool = False) -> list[dict[str, Any]]:
        params = {
            "limit": limit,
            "active": str(active).lower(),
            "closed": str(closed).lower(),
        }
        url = f"{self.base_url}/markets?{urlencode(params)}"
        with urlopen(url, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        if not isinstance(payload, list):
            return []
        return payload

    def build_snapshots(self, markets: Iterable[dict[str, Any]]) -> list[MarketSnapshot]:
        snapshots: list[MarketSnapshot] = []
        for market in markets:
            yes_price = _to_float(market.get("outcomePrices", [0, 0]), index=0)
            no_price = _to_float(market.get("outcomePrices", [0, 0]), index=1)
            spread = abs(1 - (yes_price + no_price))
            snapshots.append(
                MarketSnapshot(
                    market_id=str(market.get("id", "")),
                    question=str(market.get("question", "")),
                    yes_price=yes_price,
                    no_price=no_price,
                    spread=spread,
                    volume=float(market.get("volume", 0) or 0),
                    liquidity=float(market.get("liquidity", 0) or 0),
                    end_date_iso=market.get("endDate"),
                )
            )
        return snapshots


def _to_float(value: Any, *, index: int) -> float:
    if isinstance(value, list) and index < len(value):
        try:
            return float(value[index])
        except (TypeError, ValueError):
            return 0.0
    return 0.0
