# A 股日报快照数据结构

数据 URL: `https://hhxg.top/static/data/assistant/skill_snapshot.json`

## 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `meta` | object | 版本信息 (`schema_version`, `generated_at`) |
| `date` | string | 数据日期，如 `"2026-02-27"` |
| `disclaimer` | string | 免责声明 |
| `ai_summary` | object | AI 一句话摘要 |
| `market` | object | 市场赚钱效应 |
| `hot_themes` | array | 热门题材列表 |
| `sectors` | array | 行业/板块资金流向 |
| `ladder` | object | 连板天梯概览 |
| `ladder_detail` | object | 连板天梯详情 |
| `hotmoney` | object | 游资龙虎榜 |
| `focus_news` | array | 焦点新闻 |
| `macro_news` | array | 宏观新闻 |
| `links` | array | 工具页链接 |

## market 对象

| 字段 | 说明 |
|------|------|
| `sentiment_index` | 赚钱效应指数 (0-100) |
| `sentiment_label` | 情绪标签: 强/中/弱 |
| `limit_up` | 涨停家数 |
| `broken_board` | 炸板数 |
| `limit_down` | 跌停家数 |
| `structure_diff` | 结构差值 |
| `buckets` | 涨跌分布数组 `[{label, count}]` |

## hot_themes 数组元素

| 字段 | 说明 |
|------|------|
| `name` | 题材名称 |
| `limitup_count` | 涨停数 |
| `net_yi` | 净流入(亿) |
| `top_stocks` | 龙头股 `[{name, code, change_pct}]` |

## sectors 数组元素 (SectorGroup)

| 字段 | 说明 |
|------|------|
| `label` | 分组标签 (如"行业"、"概念") |
| `strong` | 强势板块 `[SectorItem]` |
| `weak` | 弱势板块 `[SectorItem]` |

SectorItem: `{name, change_pct, top_stock, deviation}`

## ladder / ladder_detail

**ladder** (概览):
| 字段 | 说明 |
|------|------|
| `max_streak` | 最高连板数 |
| `top_streak` | 最高连板股 `{name, code}` |

**ladder_detail** (详情):
| 字段 | 说明 |
|------|------|
| `levels` | 各级连板 `[{label, stocks: [{name, code, theme}]}]` |
| `lb_rates_map` | 晋级率 `{"2进3": "33%", ...}` |
| `area_counts` | 地域分布 `[{name, count}]` |
| `concept_counts` | 概念分布 `[{name, count}]` |

## hotmoney 对象

| 字段 | 说明 |
|------|------|
| `top_buy` | 净买入 TOP `[{stock: {name,code,change_pct}, net_wan}]` |
| `seats` | 知名游资 `[{name, stocks: [{name,code,direction}]}]` |

## news 数组元素

| 字段 | 说明 |
|------|------|
| `title` | 标题 |
| `summary` | 摘要 |
| `time` | 时间 |
| `source` | 来源 |
