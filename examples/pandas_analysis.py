"""Combine hhxg with pandas for deeper analysis."""

import hhxg

try:
    import pandas as pd
except ImportError:
    raise SystemExit("This example requires pandas: pip install pandas")

snapshot = hhxg.get_snapshot()

# ---- Hot themes → DataFrame ----
themes_data = [
    {
        "题材": t.name,
        "涨停数": t.limitup_count,
        "净流入(亿)": t.net_yi,
        "龙头": t.top_stocks[0].name if t.top_stocks else "",
    }
    for t in snapshot.hot_themes
]
df_themes = pd.DataFrame(themes_data)
print("=== 热门题材 ===")
print(df_themes.to_string(index=False))

# ---- Sector fund flow → DataFrame ----
rows = []
for group in snapshot.sectors:
    for item in group.strong:
        rows.append({"分组": group.label, "方向": "强势", "名称": item.name, "净流入(亿)": item.net_yi})
    for item in group.weak:
        rows.append({"分组": group.label, "方向": "弱势", "名称": item.name, "净流入(亿)": item.net_yi})
df_sectors = pd.DataFrame(rows)
print("\n=== 行业资金流 ===")
print(df_sectors.to_string(index=False))

# ---- Hotmoney top buys ----
if snapshot.hotmoney:
    buys = [
        {"股票": b.name, "净买入(亿)": b.net_yi, "占比%": b.ratio_pct}
        for b in snapshot.hotmoney.top_net_buy
    ]
    df_buys = pd.DataFrame(buys)
    print(f"\n=== 游资净买入 TOP (合计 {snapshot.hotmoney.total_net_yi:.1f} 亿) ===")
    print(df_buys.to_string(index=False))
