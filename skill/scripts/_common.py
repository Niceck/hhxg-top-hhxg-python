"""共用工具：HTTP 请求 + 本地缓存 + schema 检查。"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

BASE_URL = "https://hhxg.top/static/data"
CACHE_DIR = os.path.expanduser("~/.cache/hhxg-market")
SUPPORTED_SCHEMA = 3
HEADERS = {
    "User-Agent": "hhxg-skill/1.0",
    "X-Skill-Client": "clawhub",
}


def fetch_json(path, cache_name=None):
    """获取 JSON 数据，失败时用本地缓存兜底。

    Returns (data, from_cache) 元组。
    """
    url = "%s/%s" % (BASE_URL, path)
    cache_file = os.path.join(CACHE_DIR, cache_name) if cache_name else None

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if cache_file:
            _save_cache(cache_file, data)
        return data, False
    except Exception:
        if cache_file:
            cached = _load_cache(cache_file)
            if cached:
                return cached, True
        raise RuntimeError(
            "数据服务暂时不可用，且无本地缓存。请稍后重试或直接访问 https://hhxg.top"
        )


def check_schema(data):
    """schema 版本检查。"""
    meta = data.get("meta", {})
    ver = meta.get("schema_version", SUPPORTED_SCHEMA)
    if ver > SUPPORTED_SCHEMA:
        print(
            "WARNING: 数据格式已更新 (v%s)，当前技能支持 v%s，建议升级：\n"
            "  cd ~/.claude/skills/hhxg-market && git pull\n" % (ver, SUPPORTED_SCHEMA),
            file=sys.stderr,
        )


def print_cache_hint(from_cache, date_str):
    """缓存兜底时输出提示。"""
    if from_cache:
        print(
            "NOTE: 网络不可用，以下为本地缓存数据（%s）\n" % date_str,
            file=sys.stderr,
        )


def run_main(sections, default="all"):
    """通用 main 入口：解析 args、fetch、输出。"""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    use_json = "--json" in flags

    section = args[0] if args else default
    if section not in sections:
        print("未知板块: %s" % section)
        print("可选: %s" % ", ".join(sections))
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
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
