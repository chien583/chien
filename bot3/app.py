from __future__ import annotations

import argparse

from bot3.polymarket_client import PolymarketClient
from bot3.strategy import OpportunityStrategy


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="小机器人3：Polymarket 市场机会扫描")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--min-liquidity", type=float, default=5_000)
    parser.add_argument("--min-volume", type=float, default=1_000)
    parser.add_argument("--max-spread", type=float, default=0.25)
    parser.add_argument("--top", type=int, default=10)
    return parser


def main() -> None:
    args = make_parser().parse_args()

    client = PolymarketClient()
    markets = client.get_markets(limit=args.limit)
    snapshots = client.build_snapshots(markets)

    strategy = OpportunityStrategy(
        min_liquidity=args.min_liquidity,
        min_volume=args.min_volume,
        max_spread=args.max_spread,
    )
    opportunities = strategy.rank(snapshots, top_n=args.top)

    if not opportunities:
        print("没有找到符合条件的市场，请放宽筛选条件。")
        return

    print(f"找到 {len(opportunities)} 个候选市场：")
    for idx, opp in enumerate(opportunities, start=1):
        snap = opp.snapshot
        print(
            f"[{idx}] score={opp.score:.4f} | id={snap.market_id} | "
            f"yes={snap.yes_price:.3f} no={snap.no_price:.3f} | {snap.question}"
        )
        print(f"     reason: {opp.reason}")


if __name__ == "__main__":
    main()
