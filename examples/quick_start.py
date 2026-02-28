"""Quick start: 3 lines to get A-share market data."""

import hhxg

snapshot = hhxg.get_snapshot()
print(f"日期: {snapshot.date}")
print(f"赚钱效应: {snapshot.market.sentiment_index}% ({snapshot.market.sentiment_label})")
print(f"涨停: {snapshot.market.limit_up}  炸板: {snapshot.market.fried}")
print(f"\n热门题材:")
for theme in snapshot.hot_themes[:5]:
    leaders = ", ".join(s.name for s in theme.top_stocks[:2])
    print(f"  {theme.name} — 涨停 {theme.limitup_count} 家 | 龙头: {leaders}")
