"""共用工具：HTTP 请求 + 本地缓存 + schema 检查。"""

from __future__ import annotations

import json
import os
import re
import sys
import time

# 防御：本目录存在与标准库同名的 calendar.py。直接运行本目录脚本时
# sys.path[0] 指向本目录，标准库链 (urllib→http→email→calendar)
# 触发的 `import calendar` 会误命中本地 calendar.py，而后者又
# `from _common import ...`，在 _common 尚未初始化完成时形成循环导入。
# 故在触发该链路 (import urllib.request) 之前，按标准库绝对路径锁定 calendar。
# 契约：任何脚本必须先 `from _common import ...` 再触发 urllib/http/email 导入，
# 否则本防御失效（防御只在 _common 首次 import 时执行一次）。
if "calendar" not in sys.modules:
    try:
        import importlib.util as _ilu

        _cal_path = os.path.join(os.path.dirname(os.__file__), "calendar.py")
        if os.path.isfile(_cal_path):
            _spec = _ilu.spec_from_file_location("calendar", _cal_path)
            _cal_mod = _ilu.module_from_spec(_spec)
            sys.modules["calendar"] = _cal_mod
            try:
                _spec.loader.exec_module(_cal_mod)
            except Exception:
                del sys.modules["calendar"]  # 不留半初始化模块
                raise
    except Exception as _e:  # frozen/zipimport 等异常环境：提示但不阻断
        print(f"WARNING: 标准库 calendar 预加载失败（{_e}）", file=sys.stderr)

import urllib.error  # noqa: E402
import urllib.request  # noqa: E402

BASE_URL = "https://hhxg.top/static/data"
CACHE_DIR = os.path.expanduser("~/.cache/hhxg-market")
SUPPORTED_SCHEMA = 3
HEADERS = {
    "User-Agent": "hhxg-skill/1.0",
    "X-Skill-Client": "clawhub",
}
_WS_RE = re.compile(r"\s+")


def fetch_json(path, cache_name=None):
    """获取 JSON 数据，网络抖动自动重试一次，失败时用本地缓存兜底。

    Returns (data, from_cache) 元组。
    """
    url = f"{BASE_URL}/{path}"
    cache_file = os.path.join(CACHE_DIR, cache_name) if cache_name else None

    last_err = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if cache_file:
                _save_cache(cache_file, data)
            return data, False
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise RuntimeError(
                    "数据接口不存在 (404)，请升级技能：\n"
                    "  cd ~/.claude/skills/hhxg-market && git pull"
                )
            # 5xx 等服务端错误：有缓存先降级（带提示），无缓存报错
            cached = _load_cache(cache_file) if cache_file else None
            if cached:
                return cached, True
            raise RuntimeError(f"服务端错误 HTTP {e.code}，请稍后重试")
        except (ValueError, UnicodeDecodeError):
            # 响应非法（含 JSONDecodeError 与残缺部署吐 HTML 的形态）：
            # 不写缓存；读侧有旧缓存则降级（stderr 会提示是缓存数据）
            cached = _load_cache(cache_file) if cache_file else None
            if cached:
                return cached, True
            raise RuntimeError("数据格式异常，服务端可能在维护，请稍后重试")
        except OSError as e:
            # URLError / TimeoutError / ConnectionError / SSLError /
            # IncompleteRead 等网络层异常均为 OSError 谱系
            last_err = e
            if attempt == 0:
                time.sleep(1)

    # 两次都失败，尝试缓存兜底
    if cache_file:
        cached = _load_cache(cache_file)
        if cached:
            return cached, True
    raise RuntimeError(
        "网络不可用，且无本地缓存。请稍后重试或直接访问 https://hhxg.top"
    )


def as_dicts(value):
    """把可能为 null / 混入非 dict 元素的列表安全归一为 dict 列表。

    上游 KB JSON 的容器字段可能显式为 null（区别于缺键），
    渲染层统一经此归一后再迭代，避免 traceback 泄露给用户。
    """
    if not isinstance(value, list):
        return []
    return [x for x in value if isinstance(x, dict)]


def md_inline(value, limit=None):
    """外部文本 → 单行安全 markdown：折叠空白、转义结构字符、可选截断。

    数据源含第三方提交文本（董秘问答/题材名等），换行可伪造标题与
    指令块、竖线会打乱表格列，统一经此消毒后再进入 markdown 输出。
    """
    text = _WS_RE.sub(" ", str(value or "")).strip()
    text = text.replace("|", "｜").replace("`", "'")
    if limit and len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def check_schema(data):
    """schema 版本检查。"""
    meta = data.get("meta", {})
    ver = meta.get("schema_version", SUPPORTED_SCHEMA)
    if ver > SUPPORTED_SCHEMA:
        print(
            f"WARNING: 数据格式已更新 (v{ver})，当前技能支持 v{SUPPORTED_SCHEMA}，建议升级：\n"
            "  cd ~/.claude/skills/hhxg-market && git pull\n",
            file=sys.stderr,
        )


def print_cache_hint(from_cache, date_str):
    """缓存兜底时输出提示。"""
    if from_cache:
        print(
            f"NOTE: 网络不可用，以下为本地缓存数据（{date_str}）\n",
            file=sys.stderr,
        )


def run_main(sections, default="all"):
    """通用 main 入口：解析 args、fetch、输出。"""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}

    if flags & {"-h", "--help"}:
        import __main__

        print((__main__.__doc__ or "").strip())
        sys.exit(0)
    unknown = flags - {"--json"}
    if unknown:
        print(
            "未知参数: {}（支持 --json / -h）".format(", ".join(sorted(unknown))),
            file=sys.stderr,
        )
        sys.exit(1)
    use_json = "--json" in flags

    section = args[0] if args else default
    if section not in sections:
        print(f"未知板块: {section}", file=sys.stderr)
        print("可选: {}".format(", ".join(sections)), file=sys.stderr)
        sys.exit(1)

    return section, args[1:], use_json


def _save_cache(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except OSError:
        pass


def _load_cache(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
