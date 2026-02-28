# hhxg — A 股日报快照

> 零配置获取 A 股每日市场数据 — 赚钱效应、热门题材、连板天梯、游资龙虎榜、焦点新闻

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CI](https://github.com/Niceck/hhxg-top-hhxg-python/actions/workflows/ci.yml/badge.svg)](https://github.com/Niceck/hhxg-top-hhxg-python/actions)
[![Daily Update](https://github.com/Niceck/hhxg-top-hhxg-python/actions/workflows/daily-snapshot.yml/badge.svg)](https://github.com/Niceck/hhxg-top-hhxg-python/actions)

---

## 三种使用方式

| 方式 | 适用场景 | 需要安装 |
|------|----------|----------|
| **Claude Code Skill** | Claude Code / 小龙虾 CLI | 无需安装 |
| **Python SDK** | 量化研究、数据分析 | `pip install hhxg` |
| **MCP Server** | Claude Desktop / Cursor | `pip install hhxg[mcp]` |

---

## 方式一：Claude Code Skill（推荐）

**零安装，复制即用。**

### 安装

```bash
# 复制 skill 到 Claude Code skills 目录
mkdir -p ~/.claude/skills/hhxg-market/scripts ~/.claude/skills/hhxg-market/references
curl -sL https://raw.githubusercontent.com/Niceck/hhxg-top-hhxg-python/main/skill/SKILL.md \
  -o ~/.claude/skills/hhxg-market/SKILL.md
curl -sL https://raw.githubusercontent.com/Niceck/hhxg-top-hhxg-python/main/skill/scripts/fetch_snapshot.py \
  -o ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py
curl -sL https://raw.githubusercontent.com/Niceck/hhxg-top-hhxg-python/main/skill/references/data-schema.md \
  -o ~/.claude/skills/hhxg-market/references/data-schema.md
curl -sL https://raw.githubusercontent.com/Niceck/hhxg-top-hhxg-python/main/skill/references/scheduled-fetch.md \
  -o ~/.claude/skills/hhxg-market/references/scheduled-fetch.md
chmod +x ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py
```

### 使用

安装后重启 Claude Code，直接对话即可：

```
你：今天 A 股怎么样？
你：热门题材有哪些？
你：连板天梯
你：龙虎榜游资动向
你：/hhxg-market
```

### 触发词

以下关键词会自动触发 skill：

| 类别 | 触发词 |
|------|--------|
| 大盘 | 今天 A 股怎么样、今天市场如何、大盘怎么样 |
| 日报 | A 股日报、A 股复盘、盘后复盘、盘后总结 |
| 情绪 | 市场情绪、赚钱效应、涨跌分布 |
| 题材 | 热门题材、热门概念、主线题材 |
| 连板 | 连板天梯、最高连板、涨停板、连板股 |
| 游资 | 龙虎榜、游资动向、游资席位、知名游资 |
| 资金 | 行业资金流向、板块资金、强势板块、弱势板块 |
| 新闻 | 焦点新闻、市场新闻、今日要闻 |
| 速览 | 股市快报、股市速递、市场快照、每日快报 |

### 独立使用脚本

不依赖 Claude Code，直接在终端运行（仅需 Python 3，无第三方依赖）：

```bash
# 完整快照
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py

# 只看特定板块
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py market   # 赚钱效应
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py themes   # 热门题材
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py ladder   # 连板天梯
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py hotmoney # 游资龙虎榜
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py sectors  # 行业资金
python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py news     # 焦点新闻
```

### 定时获取（每日 20:00）

**macOS launchd：**

```bash
cat > ~/Library/LaunchAgents/com.hhxg.snapshot.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hhxg.snapshot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>20</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/hhxg-snapshot.log</string>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.hhxg.snapshot.plist
```

**cron：**

```bash
(crontab -l 2>/dev/null; echo "0 20 * * 1-5 /usr/bin/python3 ~/.claude/skills/hhxg-market/scripts/fetch_snapshot.py > /tmp/hhxg-snapshot.log 2>&1") | crontab -
```

---

## 方式二：Python SDK

```bash
pip install hhxg
```

```python
import hhxg

snapshot = hhxg.get_snapshot()
print(f"赚钱效应: {snapshot.market.sentiment_index}%")
print(f"最高连板: {snapshot.ladder.top_streak.name} {snapshot.ladder.max_streak}板")
```

完整 API：

| 函数 | 返回类型 | 说明 |
|------|----------|------|
| `get_snapshot()` | `Snapshot` | 完整日报快照 |
| `get_market()` | `Market` | 市场赚钱效应、涨跌分布 |
| `get_hot_themes()` | `list[HotTheme]` | 热门题材及龙头股 |
| `get_sectors()` | `list[SectorGroup]` | 行业/板块资金流向 |
| `get_ladder()` | `LadderDetail` | 连板天梯（含晋级率） |
| `get_hotmoney()` | `Hotmoney` | 游资龙虎榜（含席位明细） |
| `get_news()` | `list[NewsItem]` | 焦点新闻 |

搭配 Pandas：

```python
import hhxg, pandas as pd

themes = hhxg.get_hot_themes()
df = pd.DataFrame([
    {"题材": t.name, "涨停数": t.limitup_count, "净流入(亿)": t.net_yi}
    for t in themes
])
print(df.to_string(index=False))
```

---

## 方式三：MCP Server

```bash
pip install hhxg[mcp]
```

**Claude Desktop** — 编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{ "mcpServers": { "hhxg": { "command": "hhxg-mcp" } } }
```

**Cursor** — Settings > MCP 添加同上配置。

**Claude Code：**

```bash
claude mcp add hhxg hhxg-mcp
```

配置完成后直接说「今天 A 股怎么样」即可。

---

## 数据内容

每日快照涵盖 5000+ 只 A 股，交易日盘后 **20:00** 更新：

| 板块 | 内容 |
|------|------|
| 市场赚钱效应 | 情绪指数、涨跌家数分布、涨停/炸板/跌停、结构差值 |
| 热门题材 | TOP 题材排行、涨停数、净流入、龙头股 |
| 行业资金 | 强势/弱势板块、净流入排名、领涨股、偏离度 |
| 连板天梯 | 各级连板股票、晋级率、地域分布、概念分布 |
| 游资龙虎榜 | 净买入 TOP、知名游资席位操作明细 |
| 焦点新闻 | 市场焦点 + 宏观新闻 |

---

## 数据来源

数据由 [恢恢量化](https://hhxg.top) 每日盘后更新。

> 数据仅供研究参考，不构成投资建议。

如需可视化图表、AI 选股、历史回溯等高级功能，请访问 [hhxg.top](https://hhxg.top)。

---

## License

[MIT](LICENSE) &copy; [恢恢量化](https://hhxg.top)
