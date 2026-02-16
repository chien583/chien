# 小机器人3（Polymarket 应用增强版）

这个版本补充了一个可运行的 Polymarket 事件扫描机器人骨架，重点是：

- 通过 Gamma API 拉取市场数据
- 根据「流动性 + 价差 + 成交量」做机会评分
- 输出可读的机会清单，便于后续接入交易执行层

## 快速开始

```bash
python -m bot3.app --limit 30 --min-liquidity 5000 --max-spread 0.25 --min-volume 1000
```

## 功能概览

1. `PolymarketClient`：负责请求公开市场数据。
2. `OpportunityStrategy`：负责过滤与评分。
3. `app.py`：命令行入口，串联抓取与策略分析。

> 说明：当前版本先聚焦「发现机会」。如果要做自动下单，建议在此基础上增加签名、风控和执行模块。
