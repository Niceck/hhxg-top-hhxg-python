# Changelog

## v1.2.0 (2026-08-03)

新增 5 个数据模块（脚本 4 → 9），与 [AI 集成页面](https://hhxg.top/skill.html) 宣传能力对齐：

- **northbound.py** — 北向资金：近 7 日沪深港通资金流向（北向/南向/沪股通/深股通），输出自带 2024-08 口径变更说明
- **theme.py** — 题材概念：当日热度榜（游资参与/涨停/占比）+ 近 30 日概念链路（TOP 概念/龙头映射/`related <概念>` 共现查询）
- **dongmi.py** — 董秘问答：7 日 QA 流水 + 30 日 TOP 被问股/热门话题（`topics`）+ 个股查询（`stock <名称>`，30 日索引 miss 自动回退 7 日流水）
- **strategy.py** — 量化策略：策略审计（`presets`，14 策略当日命中）+ 最新信号（`signals`）+ 历史胜率（`stats`）+ 游资席位（`seats`）
- **resonance.py** — 共振 + 风险：跨数据源共振信号（≥2 类确认，含数据源分布）+ 4 类风险预警（暴跌/出货/九转见顶/高换手下跌）

修复：`_common.py` 引入标准库 `calendar` 遮蔽防御（本目录 calendar.py 与标准库同名，部分 Python 版本 urllib 导入链会触发循环导入）；网络异常捕获扩展 TimeoutError / ConnectionError。

文档同步：SKILL.md 触发词与模块说明、README 功能表、references/data-schema.md 补 5 节字段说明。

## v1.1.0

- openapi.yaml：GPT Actions / Dify / Coze 集成支持（4 个公开 REST 端点）

## v1.0.0

- 首发：fetch_snapshot.py（日报快照）、calendar.py（A 股日历）、margin.py（融资融券）、news.py（实时快讯）
