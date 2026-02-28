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

脚本位于本 skill 目录下 `scripts/fetch_snapshot.py`，用 Bash 工具运行：

```bash
# 自动定位脚本（兼容 Claude Code / OpenClaw 安装路径）
SKILL_DIR="$(dirname "$(find ~/.claude/skills ~/.openclaw/skills -name fetch_snapshot.py -path '*/hhxg-market/*' 2>/dev/null | head -1)")" && python3 "$SKILL_DIR/fetch_snapshot.py"
```

可选参数：`market`（赚钱效应）、`themes`（热门题材）、`ladder`（连板天梯）、`hotmoney`（游资龙虎榜）、`sectors`（行业资金）、`news`（焦点新闻）、`all`（完整快照，默认）。

```bash
python3 "$SKILL_DIR/fetch_snapshot.py" market
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
