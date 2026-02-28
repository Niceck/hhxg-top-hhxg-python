# hhxg-market — A 股量化数据助手

> Claude Code / OpenClaw 技能：零配置获取 A 股日报、日历、融资融券、量化选股、实时快讯

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 什么是 hhxg-market？

一个 [Claude Code](https://claude.ai/code) / [OpenClaw](https://github.com/nicepkg/openclaw) 技能（Skill），安装后对 AI 说「今天 A 股怎么样」、「融资融券数据」、「明天是交易日吗」就能获取对应数据。

**无需注册、无需 Token、无需安装 Python 包**，仅需 Python 3 标准库。

数据由 [恢恢量化](https://hhxg.top) 持续更新，覆盖 5000+ 只 A 股。

---

## 安装（一键复制）

**Claude Code：**
```bash
git clone --depth 1 https://github.com/Niceck/hhxg-top-hhxg-python.git ~/.claude/skills/hhxg-market
```

**OpenClaw：**
```bash
git clone --depth 1 https://github.com/Niceck/hhxg-top-hhxg-python.git ~/.openclaw/skills/hhxg-market
```

---

## 功能模块

| 模块 | 脚本 | 数据内容 |
|------|------|----------|
| 日报快照 | `fetch_snapshot.py` | 赚钱效应、热门题材、连板天梯、游资龙虎榜、行业资金、焦点新闻 |
| A 股日历 | `calendar.py` | 交易日查询、限售解禁、业绩预告、期货交割日 |
| 融资融券 | `margin.py` | 近 7 日余额变化、融资净买入/净卖出 TOP |
| 量化选股 | `strategy.py` | 13 策略审计（胜率/覆盖率）、游资席位持仓 |
| 实时快讯 | `news.py` | 财经快讯流（按时间倒序） |

---

## 使用方式

### 在 Claude Code 中对话

```
你：今天 A 股怎么样？
你：热门题材 / 连板天梯 / 龙虎榜
你：明天是交易日吗？
你：融资融券数据
你：量化选股策略
你：最新财经快讯
```

### 触发词

| 类别 | 触发词 |
|------|--------|
| 日报 | 今天 A 股怎么样、大盘怎么样、盘后复盘、赚钱效应 |
| 题材 | 热门题材、连板天梯、龙虎榜、行业资金流向 |
| 日历 | 今天是交易日吗、下周解禁、交割日、业绩预告 |
| 两融 | 融资融券、两融数据、融资净买入 |
| 选股 | 量化选股、选股策略、游资席位 |
| 快讯 | 最新快讯、财经新闻、焦点新闻 |

### 终端独立使用

```bash
# 定位脚本目录（兼容 Claude Code / OpenClaw）
SKILL_DIR=$(dirname "$(find ~/.claude/skills ~/.openclaw/skills -name _common.py -path '*/hhxg-market/*' 2>/dev/null | head -1)")

# 日报快照
python3 "$SKILL_DIR/fetch_snapshot.py"
python3 "$SKILL_DIR/fetch_snapshot.py" market    # 赚钱效应
python3 "$SKILL_DIR/fetch_snapshot.py" themes    # 热门题材

# A 股日历
python3 "$SKILL_DIR/calendar.py"                     # 本周事件
python3 "$SKILL_DIR/calendar.py" trading 2026-03-05  # 交易日查询

# 融资融券
python3 "$SKILL_DIR/margin.py"                       # 完整报告

# 量化选股
python3 "$SKILL_DIR/strategy.py"                     # 策略 + 游资席位

# 实时快讯
python3 "$SKILL_DIR/news.py"                         # 最新 20 条
python3 "$SKILL_DIR/news.py" 50                      # 最新 50 条

# 所有脚本支持 --json 输出原始数据
python3 "$SKILL_DIR/margin.py" --json
```

---

## 输出示例

```
# A 股日报快照 — 2026-02-27

> **赚钱效应 61.8%（强）**
> - **题材**: 绿色电力、风电、小金属概念 等题材活跃
> - **资金**: 小金属、电力、IT服务 方向资金集中
> - **游资**: 游资净买入 41亿，烽火通信领涨

# 本周 A 股日历（2026-02-23 ~ 2026-03-01）

今天 2026-02-28 是交易日
本周交易日: 2026-02-24, 2026-02-25, 2026-02-26, 2026-02-27, 2026-02-28

# 融资融券市场总览（近 7 个交易日）

最新融资余额: 18355 亿 | 7 日变化: +120.5 亿
融资净买入 TOP: 寒武纪 +12.0亿, 芯原股份 +7.8亿 ...
```

---

## 卸载

```bash
rm -rf ~/.claude/skills/hhxg-market
```

---

## 文件结构

```
├── README.md
├── LICENSE
└── skill/
    ├── SKILL.md                  # Skill 定义文件
    ├── scripts/
    │   ├── _common.py            # 共用工具（HTTP、缓存、schema 检查）
    │   ├── fetch_snapshot.py     # 日报快照
    │   ├── calendar.py           # A 股日历
    │   ├── margin.py             # 融资融券
    │   ├── strategy.py           # 量化选股
    │   └── news.py               # 实时快讯
    └── references/
        └── data-schema.md        # JSON 数据结构说明
```

---

## 数据来源

数据由 [恢恢量化](https://hhxg.top) 持续更新，覆盖 5000+ 只 A 股。

> 数据仅供研究参考，不构成投资建议。

如需可视化图表、AI 选股、历史回溯等高级功能，请访问 [hhxg.top](https://hhxg.top)。

---

## License

[MIT](LICENSE) &copy; [恢恢量化](https://hhxg.top)
