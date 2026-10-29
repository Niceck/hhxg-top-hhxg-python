# Changelog

## v1.2.2 (2026-10-29)

- **news.py 快讯改读每小时滚动的 `https://hhxg.top/api/news`**：站点静态 `news/n0.json` 现在一天只随全站构建更新 3 次，盘中最多落后约 6 小时；接口失败、返回结构不对或要超过 50 条时自动回落静态文件，stderr 会提示。
- **`_common.fetch_json`** 接受 `https://hhxg.top/` 下的绝对地址（其他域名拒绝），相对路径行为不变。

## v1.2.1 (2026-10-28)

- **strategy.py `presets`**：不再显示当日命中数与覆盖率检查（当日命中仅会员可见），改为「策略 / 阶段 / 回溯胜率」表，附回溯研究页链接（公开回溯统计每周更新）；`references/data-schema.md` 同步——`jiuzhuan` / `multi_factor` / `emotion_sync` 恒为 `null`，`summary` 只剩 `preset_total`。
- **更新时间口径**：README / SKILL.md / fetch_snapshot.py / openapi.yaml 统一为「交易日 20:22 起更新，预计 20:30 前完成（北京时间）」；两融数据为交易日上午约 09:05 更新上一交易日。
- **openapi.yaml 1.1.0 → 1.3.0**：与站点公开的 https://hhxg.top/openapi.yaml 一致，新增付费数据 API（`/api/data/index` 目录、`/api/data/{scope}` Bearer token，Max 权益）与 `x-pricing` 套餐目录；原 4 个公开端点不变。

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
