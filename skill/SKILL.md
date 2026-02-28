---
name: hhxg-market
description: A 股日报快照 — 每日盘后获取赚钱效应、热门题材、连板天梯、游资龙虎榜等实时市场数据，零配置无需安装任何依赖。
tools: ["Bash", "WebFetch"]
---

# A 股日报快照（恢恢量化）

## 概述

零配置获取 A 股每日市场快照数据，数据源自 [恢恢量化](https://hhxg.top)，每个交易日盘后（约 20:00）更新。

**无需安装任何 Python 包**，直接通过 HTTP 获取 JSON 数据即可。

## 数据获取

### 方式 1：WebFetch（推荐）

直接用 WebFetch 工具获取并解析：

```
WebFetch: https://hhxg.top/static/data/assistant/skill_snapshot.json
```

### 方式 2：curl + python3

```bash
curl -s https://hhxg.top/static/data/assistant/skill_snapshot.json | python3 -m json.tool
```

### 方式 3：使用脚本获取格式化输出

```bash
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py
```

可选参数：
```bash
# 只看市场赚钱效应
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py market

# 只看热门题材
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py themes

# 只看连板天梯
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py ladder

# 只看游资龙虎榜
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py hotmoney

# 只看行业资金
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py sectors

# 只看焦点新闻
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py news

# 完整快照（默认）
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py all
```

## 数据更新时间

- 交易日盘后约 **20:00** 更新
- 非交易日（周末、节假日）数据保持为上一个交易日
- 数据中的 `date` 字段标识数据日期

## 使用场景

用户问到以下问题时，自动调用此 skill：
- "今天 A 股怎么样" / "大盘怎么样"
- "A 股日报" / "盘后复盘"
- "热门题材" / "连板天梯" / "龙虎榜"
- "行业资金流向" / "焦点新闻" / "赚钱效应"

## Scripts

- [获取日报快照](scripts/fetch_snapshot.py) — 零依赖 Python 脚本，直接获取并格式化输出

## References

- [数据结构说明](references/data-schema.md) — JSON 字段详解
