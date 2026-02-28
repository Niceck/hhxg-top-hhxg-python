# hhxg — A 股日报快照 SDK

> 零配置、类型安全、AI 原生的 A 股市场数据 Python SDK

[![PyPI](https://img.shields.io/pypi/v/hhxg?color=blue)](https://pypi.org/project/hhxg/)
[![Python](https://img.shields.io/pypi/pyversions/hhxg)](https://pypi.org/project/hhxg/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/hhxg-top/hhxg-python/actions/workflows/ci.yml/badge.svg)](https://github.com/hhxg-top/hhxg-python/actions)

---

## 为什么选 hhxg？

| 特性 | tushare | akshare | **hhxg** |
|------|---------|---------|----------|
| 需要注册 | 是（Token） | 否 | **否** |
| 需要配置 | 是 | 否 | **否** |
| 返回类型 | DataFrame | DataFrame | **Pydantic 模型** |
| 类型提示 | 无 | 无 | **完整类型安全** |
| AI 友好 | 否 | 否 | **MCP + GPT + SDK** |
| 数据范围 | 全量历史 | 全量历史 | **日报快照** |

**hhxg 的定位**：不追求全量历史数据，专注于**每日市场快照**——赚钱效应、热门题材、资金流向、连板天梯、游资龙虎榜、焦点新闻，一个函数调用获取全部。

---

## 30 秒上手

```bash
pip install hhxg
```

```python
import hhxg

snapshot = hhxg.get_snapshot()
print(f"赚钱效应: {snapshot.market.sentiment_index}%")
print(f"最高连板: {snapshot.ladder.top_streak.name} {snapshot.ladder.max_streak}板")
```

输出：

```
赚钱效应: 61.8%
最高连板: 豫能控股 7板
```

---

## 完整 API

| 函数 | 返回类型 | 说明 |
|------|----------|------|
| `get_snapshot()` | `Snapshot` | 完整日报快照 |
| `get_market()` | `Market` | 市场赚钱效应、涨跌分布 |
| `get_hot_themes()` | `list[HotTheme]` | 热门题材及龙头股 |
| `get_sectors()` | `list[SectorGroup]` | 行业/板块资金流向 |
| `get_ladder()` | `LadderDetail` | 连板天梯（含晋级率） |
| `get_hotmoney()` | `Hotmoney` | 游资龙虎榜（含席位明细） |
| `get_news()` | `list[NewsItem]` | 焦点新闻 |

所有函数零配置、开箱即用，返回 Pydantic 模型，IDE 自动补全。

---

## 数据内容

每日快照涵盖：

- **市场赚钱效应** — 情绪指数、涨跌家数分布、结构差值
- **热门题材** — TOP 题材及涨停数、净流入、龙头股
- **行业/板块资金** — 强势/弱势板块、净流入排名、领涨股
- **连板天梯** — 各级连板股票、晋级率、地域/概念分布
- **游资龙虎榜** — 净买入 TOP、知名游资席位操作明细
- **焦点新闻** — 市场焦点 + 宏观新闻
- **AI 摘要** — 一句话概括当日市场

---

## 搭配 Pandas

```python
import hhxg
import pandas as pd

themes = hhxg.get_hot_themes()
df = pd.DataFrame([
    {"题材": t.name, "涨停数": t.limitup_count, "净流入(亿)": t.net_yi}
    for t in themes
])
print(df.to_string(index=False))
```

```
     题材  涨停数  净流入(亿)
 绿色电力    16     0.22
     风电    16     8.17
小金属概念    15    19.38
昨日高振幅    14    30.84
 最近多板    13    13.80
     核电    11     4.18
```

---

## 高级用法

### 自定义客户端

```python
from hhxg import HhxgClient

client = HhxgClient(
    base_url="https://your-mirror.com/snapshot.json",
    timeout=30.0,
)
snapshot = client.get_snapshot()
```

### 强制刷新缓存

```python
from hhxg import HhxgClient

client = HhxgClient()
snapshot = client.get_snapshot(force=True)  # 跳过内存缓存
```

---

## MCP Server — AI 工具直接调用

安装 MCP 依赖：

```bash
pip install hhxg[mcp]
```

### Claude Desktop

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "hhxg": {
      "command": "hhxg-mcp"
    }
  }
}
```

### Cursor

在 Cursor Settings > MCP 中添加：

```json
{
  "mcpServers": {
    "hhxg": {
      "command": "hhxg-mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add hhxg hhxg-mcp
```

### 可用 MCP 工具

| 工具 | 说明 |
|------|------|
| `get_snapshot` | 完整日报快照（最全面） |
| `get_market` | 市场赚钱效应、涨跌分布 |
| `get_hot_themes` | 热门题材及龙头股 |
| `get_sectors` | 行业/板块资金流向 |
| `get_ladder` | 连板天梯 |
| `get_hotmoney` | 游资龙虎榜 |
| `get_news` | 焦点新闻 |

配置完成后，直接对 AI 说「今天 A 股怎么样」「哪些题材最热」即可。

---

## AI 生态联动

hhxg 是[恢恢量化](https://hhxg.top) AI 生态的一部分：

| 接入方式 | 适用场景 | 状态 |
|----------|----------|------|
| **Python SDK**（本项目） | 量化研究、数据分析 | ✅ 可用 |
| **MCP Server**（本项目） | Claude Desktop / Cursor / Claude Code | ✅ 可用 |
| **GPT Action** | ChatGPT 自定义 GPT | 🚧 开发中 |

---

## 数据来源

数据由 [恢恢量化](https://hhxg.top) 每日盘后更新，覆盖 5000+ 只 A 股。

> 数据仅供研究参考，不构成投资建议。

---

## 更多功能

SDK 提供每日市场快照数据。如需以下高级功能，请访问 [hhxg.top](https://hhxg.top)：

- 可视化图表与趋势分析
- AI 多因子选股工具
- ETF 资金流向筛选
- 历史数据回溯
- AI 智能问答

---

## License

[MIT](LICENSE) &copy; [恢恢量化](https://hhxg.top)
