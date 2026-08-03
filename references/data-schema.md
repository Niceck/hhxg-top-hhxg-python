# 数据结构说明

所有数据基于 `https://hhxg.top/static/data/` 下的 JSON 文件。

---

## 一、日报快照（fetch_snapshot.py）

URL: `assistant/skill_snapshot.json`

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `meta` | object | `{schema_version, generated_at}` |
| `date` | string | 数据日期，如 `"2026-02-28"` |
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
| `comparison` | object? | 较昨日变化（可选） |
| `signals_count` | object? | 量化工具钩子（可选） |
| `links` | array | 工具页链接 |

### ai_summary

| 字段 | 说明 |
|------|------|
| `market_state` | 一句话行情总结 |
| `focus_direction` | 资金方向 |
| `theme_focus` | 题材聚焦 |
| `hotmoney_state` | 游资动态 |
| `news_highlight` | 焦点新闻摘要 |
| `cta` | 行动号召文案 |

### market

| 字段 | 说明 |
|------|------|
| `date` | 数据日期 |
| `sentiment_index` | 赚钱效应指数 (0-100) |
| `sentiment_label` | 情绪标签: 强/中/弱 |
| `limit_up` | 涨停家数 |
| `fried` | 炸板数 |
| `limit_down` | 跌停家数 |
| `struct_diff` | 结构差值 |
| `promotion_rate` | 晋级率 |
| `total` | 个股总数 |
| `buckets` | 涨跌分布 `[{name, count, prev, dir}]`，`prev` 为昨日同区间数量，`dir` 为 `"up"` / `"down"` / `""` |

### hot_themes 元素

| 字段 | 说明 |
|------|------|
| `name` | 题材名称 |
| `limitup_count` | 涨停数 |
| `net_yi` | 净流入(亿) |
| `top_stocks` | 龙头股 `[{name, net_yi}]`，`net_yi` 为该股游资净买入(亿) |

### sectors 元素 (SectorGroup)

| 字段 | 说明 |
|------|------|
| `label` | 分组标签（如"行业"、"概念"） |
| `strong` | 强势板块 `[SectorItem]` |
| `weak` | 弱势板块 `[SectorItem]` |

SectorItem: `{name, net_yi, leader, bias_pct}`

### ladder（概览）

| 字段 | 说明 |
|------|------|
| `total_limit_up` | 涨停总数 |
| `max_streak` | 最高连板数 |
| `top_streak` | 最高连板股 `{name, code, industry}` |

### ladder_detail（详情）

| 字段 | 说明 |
|------|------|
| `levels` | 各级连板 `[{boards, count, stocks}]` |
| `lb_rates_map` | 晋级率 `{"2": "9.6%", "3": "60.0%", ...}`，key 为起始板数字符串 |
| `area_counts` | 地域分布 `{name: count, ...}` |
| `concept_counts` | 概念分布 `{name: count, ...}` |

levels.stocks 元素: `{name, code, industry, area, concept}`

### hotmoney

| 字段 | 说明 |
|------|------|
| `date` | 数据日期 |
| `total_net_yi` | 龙虎榜总净买入(亿) |
| `top_net_buy` | 净买入 TOP `[{name, net_yi, ratio_pct}]` |
| `seats` | 知名游资 `[{name, stocks}]` |

seats.stocks 元素: `{name, net_yi}`

### focus_news / macro_news 元素

| 字段 | 说明 |
|------|------|
| `t` | 时间 ISO 格式 `2026-02-28T15:30:00` |
| `cat` | 分类标签 |
| `title` | 标题 |

### comparison（较昨日变化）

当服务端有近 2 日数据时生成，否则为 null。

| 字段 | 说明 |
|------|------|
| `yesterday` | 昨日数据 `{limit_up, sentiment_index, fried}` |
| `trend_label` | 趋势判断文案（如"近7日高位区间"） |
| `trend_url` | 趋势图链接 |

### signals_count（量化工具钩子）

当服务端有选股审计数据时生成，否则为 null。

| 字段 | 说明 |
|------|------|
| `jiuzhuan` | 九转信号命中数 |
| `multi_factor` | 多因子评分>80 命中数 |
| `emotion_sync` | 情绪共振信号命中数 |
| `volatility_alert` | 异动预警数 |
| `free_day` | 免费日提示（如"每周一"） |
| `xuangu_url` | 选股工具链接 |
| `backtest_url` | 策略回溯链接 |

---

## 二、A 股日历（calendar.py）

### 交易日

URL: `calendar/trading_days_2026.json`

类型: `string[]` — 日期字符串数组 `["2026-01-02", "2026-01-03", ...]`

### 解禁 / 业绩预告

URL: `calendar/unlock_202603.json` / `calendar/earnings_202603.json`

```json
{
  "events": [
    {
      "date": "2026-03-05",
      "label": "事件标题",
      "description": "详细描述",
      "top_companies": [{"name": "公司名", "value": "金额"}]
    }
  ]
}
```

### 期货交割日

URL: `calendar/delivery_2026.json`

结构同上 `{events: [...]}`，无 `top_companies` 字段。

---

## 三、融资融券（margin.py）

URL: `assistant/recent_margin_7d.json`

| 字段 | 说明 |
|------|------|
| `window` | `{start, end}` 数据区间 |
| `market` | 市场总览 |
| `top` | 个股排名 |

### market

| 字段 | 说明 |
|------|------|
| `daily_totals` | 每日余额 `[{date, rzye_yi, rqye_yi}]` |
| `delta_rzye_yi` | 7 日融资变化(亿) |
| `delta_rqye_yi` | 7 日融券变化(亿) |

### top

| 字段 | 说明 |
|------|------|
| `increase_rzye` | 融资净买入 TOP `[TopItem]` |
| `decrease_rzye` | 融资净卖出 TOP `[TopItem]` |

TopItem: `{name, latest_rzye_yi, delta_rzye_yi, delta_pct}`

---

## 四、实时快讯（news.py）

URL: `news/n0.json`

类型: `array` — 新闻条目数组（按时间倒序）。

| 字段 | 说明 |
|------|------|
| `t` | 时间 ISO 格式 |
| `cat` | 分类标签 |
| `title` | 标题 |

---

## 五、北向资金（northbound.py）

URL: `assistant/recent_northbound_7d.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| `scope` | string | 固定 `"northbound"` |
| `generated_at` | string | 生成时间 |
| `window` | object | `{trading_days, dates, start, end}` |
| `stats` | object | 7 日统计（见下） |
| `series` | array | 每日明细，**按日期降序**（最新在 `[0]`） |

### stats

| 字段 | 说明 |
|------|------|
| `total_inflow_7d_yi` | 7 日北向合计(亿) |
| `avg_daily_yi` | 日均(亿) |
| `max_single_day_yi` / `min_single_day_yi` | 单日最高/最低(亿) |
| `consecutive_inflow_days` | 连续活跃天数 |
| `net_inflow_days` / `net_outflow_days` | 活跃/回落天数 |

### series 元素

`{date, north_in_yi, south_in_yi, hgt_yi, sgt_yi}`

> ⚠️ 口径：2024-08 起接口口径变更，`north_in_yi` 恒为正，仅反映外资成交
> 活跃度，不代表真实净流入方向；`south_in_yi` 为累计存量值，非日度净流入。

---

## 六、题材概念（theme.py）

热度榜 URL: `assistant/recent_theme_latest.json`

| 字段 | 类型 | 说明 |
|------|------|------|
| `latest_date` | string | 数据日期 |
| `items` | array | 题材榜（按游资参与数 → 当日涨停数降序） |

### items 元素

| 字段 | 说明 |
|------|------|
| `name` | 题材/概念名称 |
| `yz` | 游资参与数 |
| `zt` | 当日涨停数 |
| `avg10` | 近 10 日平均涨停数（上游暂未提供，恒为 null，脚本不展示） |
| `ratio` | 涨停占比（0-1 浮点） |

概念链 URL: `assistant/concept_chain_latest.json`

| 字段 | 说明 |
|------|------|
| `stats` | `{total_concepts, total_leaders, total_industries, window_days}` |
| `top.concepts` | TOP 概念 `[{name, limitup_total, active_days, max_lianban}]` |
| `top.leaders` | TOP 龙头 `[{code, name, industry, limitup_days, max_lianban, score}]` |
| `top.concept_to_leaders` | 概念 → 龙头映射（值为龙头对象数组） |
| `top.industry_to_concepts` | 行业 → 概念映射 `{行业: [{name, count}]}` |
| `related` | 概念共现映射 `{概念: [{name, count}]}` |

---

## 七、董秘问答（dongmi.py）

7 日流水 URL: `assistant/recent_dongmi_7d.json`

| 字段 | 说明 |
|------|------|
| `window` | `{trading_days, dates, start, end}` |
| `stats` | `{records, top_names: [{name, count}]}` |
| `counts_by_date` | 每日条数映射 |
| `records` | QA 流水 `[{t, date, name, q, a}]`（Q/A 已截断） |

30 日索引 URL: `assistant/dongmi_full_30d.json`

| 字段 | 说明 |
|------|------|
| `stats` | `{total_records, unique_stocks, date_range}` |
| `top_stocks` | TOP 被问股 `[{股票, 问答数}]` |
| `hot_topics` | 热门话题 `[{话题, 命中数}]` |
| `stock_qa_index` | 按股票聚合的 QA 索引（仅高热度个股） |

---

## 八、量化策略（strategy.py）

策略审计 URL: `xuangu/preset_audit.json`

| 字段 | 说明 |
|------|------|
| `asof_used` | 审计基准日 |
| `universe_size` | 选股宇宙股票数 |
| `summary` | `{preset_total, coverage_pass, coverage_fail}` |
| `presets` | 各策略 `[{key, label, coverage_check, asof_hits, ...}]` |

游资席位 URL: `xuangu/hotmoney_seats.json` — `{席位名: [ts_code, ...]}` 映射。

最新信号 URL: `assistant/recent_strategy_latest.json`

| 字段 | 说明 |
|------|------|
| `latest_strategy_date` | 策略日期 |
| `summary` | `{pending, holding, cleared}` 数量汇总 |
| `pending` | 待开仓 `[{name, date}]` |
| `holding_top` | 持仓盈亏 TOP `[{name, buy_date, pnl}]` |
| `cleared_recent` | 近期清仓 `[{name, buy_date, sell_date, ret}]` |

历史统计 URL: `assistant/strategy_full_stats.json`

| 字段 | 说明 |
|------|------|
| `stats` | `{total, wins, losses, even, win_rate, avg_return, median_return, max_return, min_return}`（`win_rate` 为字符串如 `"33.1%"`） |
| `distribution` | 收益区间分布映射 |
| `monthly` | 月度表现 `[{月份, 笔数, 均值, 胜率}]` |
| `top_winners` / `top_losers` | 历史最佳/最差 `[{股票名称, 买入日期, 清仓日期, 保底收益}]` |
| `recent_30d` | `{笔数, 胜率, 均值}` |

---

## 九、共振 + 风险（resonance.py）

共振信号 URL: `assistant/resonance_latest.json`

| 字段 | 说明 |
|------|------|
| `data_date` | 数据日期 |
| `stats` | `{total, triple_plus, min_categories, by_category, missing_sources}`（`missing_sources` 非空 = 部分数据源缺失，信号可能少报） |
| `signals` | 信号列表（按加权共振分降序，元素含 `hotmoney_seats` 席位数组） |

signals 元素: `{code, name, industry, categories, category_count,
signal_strength, score, details, warnings}`；`categories` 取值
`hotmoney`(龙虎榜) / `strategy`(策略) / `theme`(题材) / `indicator`(指标)。

风险警报 URL: `assistant/recent_risk_alerts_latest.json`

| 字段 | 说明 |
|------|------|
| `stats` | `{total_universe, top_n, amount_p70_yi, counts, total_counts}`；⚠️ `counts` 是 top_n 截断后的榜单长度，**全市场命中数必须用 `total_counts`** |
| `alerts` | 4 桶预警：`crash`(暴跌) / `distribution`(巨量出货) / `nineturn_top_warning`(九转见顶) / `high_turnover_drop`(高换手放量下跌) |

alerts 桶元素: `{code, name, industry, pct, close, vol_ratio, turnover,
amount_yi, nineturn}`
