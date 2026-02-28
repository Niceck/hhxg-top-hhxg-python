# hhxg-market — A 股日报快照 Skill

> Claude Code 技能：零配置获取 A 股每日市场数据 — 赚钱效应、热门题材、连板天梯、游资龙虎榜、焦点新闻

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 什么是 hhxg-market？

一个 [Claude Code](https://claude.ai/code) 技能（Skill），安装后对 AI 说「今天 A 股怎么样」就能获取完整的盘后日报数据。

**无需注册、无需 Token、无需安装 Python 包**，仅需 Python 3 标准库。

数据由 [恢恢量化](https://hhxg.top) 每个交易日 **20:00**前更新，覆盖A股多因子策略。

---

## 安装（一键复制）

```bash
git clone --depth 1 https://github.com/Niceck/hhxg-top-hhxg-python.git ~/.claude/skills/hhxg-market
```

---

## 使用方式

### 在 Claude Code 中对话

安装后重启 Claude Code，直接对话：

```
你：今天 A 股怎么样？
你：热门题材有哪些？
你：连板天梯
你：龙虎榜游资动向
你：行业资金流向
你：/hhxg-market
```

### 触发词

| 类别 | 触发词 |
|------|--------|
| 大盘 | 今天 A 股怎么样、大盘怎么样 |
| 日报 | A 股日报、盘后复盘 |
| 数据 | 热门题材、连板天梯、龙虎榜 |
| 资金 | 行业资金流向、焦点新闻、赚钱效应 |

### 终端独立使用

不依赖 Claude Code，直接在终端运行：

```bash
# 完整快照
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py

# 只看特定板块
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py market   # 赚钱效应
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py themes   # 热门题材
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py ladder   # 连板天梯
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py hotmoney # 游资龙虎榜
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py sectors  # 行业资金
python3 ~/.claude/skills/hhxg-market/skill/scripts/fetch_snapshot.py news     # 焦点新闻
```

---

## 数据内容

| 板块 | 内容 |
|------|------|
| 市场赚钱效应 | 情绪指数、涨跌家数分布、涨停/炸板/跌停、结构差值、晋级率 |
| 热门题材 | TOP 题材排行、涨停数、净流入、龙头股 |
| 行业资金 | 强势/弱势板块、净流入排名、领涨股、偏离度 |
| 连板天梯 | 各级连板股票、晋级率、地域分布、概念分布 |
| 游资龙虎榜 | 净买入 TOP、知名游资席位（赵老哥、炒股养家等）操作明细 |
| 焦点新闻 | 市场焦点 + 宏观新闻 |

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
    ├── SKILL.md                # Skill 定义文件
    ├── scripts/
    │   └── fetch_snapshot.py   # 零依赖获取脚本（仅用 Python 3 标准库）
    └── references/
        └── data-schema.md      # JSON 数据结构说明
```

---

## 数据来源

数据由 [恢恢量化](https://hhxg.top) 每日盘后更新，覆盖 5000+ 只 A 股。

> 数据仅供研究参考，不构成投资建议。

如需可视化图表、AI 选股、历史回溯等高级功能，请访问 [hhxg.top](https://hhxg.top)。

---

## License

[MIT](LICENSE) &copy; [恢恢量化](https://hhxg.top)
