#!/usr/bin/env python3
"""Resolve China A-share stock code/name to normalized ticker candidates.

No third-party dependencies. Uses public suggestion endpoints only for name
lookup. Returns JSON by default so Codex can consume it reliably.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any


EASTMONEY_TOKEN = "D43BF722C8E33B9C85D1B1C2E75F7E64"


def _suffix_for_code(code: str, market_hint: str = "") -> str | None:
    hint = (market_hint or "").lower()
    if hint in {"sh", "sha", "sse"} or "沪" in market_hint or hint.startswith("1."):
        return ".SS"
    if hint in {"sz", "sza", "szse"} or "深" in market_hint or hint.startswith("0."):
        return ".SZ"

    if code.startswith(("600", "601", "603", "605", "688", "689")):
        return ".SS"
    if code.startswith(("000", "001", "002", "003", "300", "301")):
        return ".SZ"
    return None


def _exchange_for_suffix(suffix: str | None) -> str:
    return {
        ".SS": "上海证券交易所",
        ".SZ": "深圳证券交易所",
    }.get(suffix or "", "待确认")


def _candidate(code: str, name: str = "", suffix: str | None = None, source: str = "", raw: dict[str, Any] | None = None) -> dict[str, Any]:
    suffix = suffix or _suffix_for_code(code)
    return {
        "code": code,
        "name": name,
        "exchange": _exchange_for_suffix(suffix),
        "suffix": suffix,
        "yahoo_ticker": f"{code}{suffix}" if suffix else None,
        "source": source,
        "raw": raw or {},
    }


def _fetch(url: str, encoding: str = "utf-8") -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    # Some local Python installs lack an up-to-date CA bundle. This public
    # endpoint is used only for symbol suggestion, not for sensitive data.
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        return resp.read().decode(encoding, errors="ignore")


def _resolve_code(query: str) -> list[dict[str, Any]]:
    upper = query.strip().upper()
    m = re.fullmatch(r"(\d{6})(?:\.(SS|SZ))?", upper)
    if not m:
        return []
    code, suffix_part = m.group(1), m.group(2)
    suffix = f".{suffix_part}" if suffix_part else _suffix_for_code(code)
    return [_candidate(code=code, suffix=suffix, source="code-rule")]


def _resolve_eastmoney(query: str) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query.strip())
    url = (
        "https://searchapi.eastmoney.com/api/suggest/get"
        f"?input={encoded}&type=14&token={EASTMONEY_TOKEN}"
    )
    text = _fetch(url)
    data = json.loads(text)
    rows = data.get("QuotationCodeTable", {}).get("Data") or []
    out = []
    for row in rows:
        code = str(row.get("Code") or "").strip()
        if not re.fullmatch(r"\d{6}", code):
            continue
        if row.get("Classify") and row.get("Classify") != "AStock":
            continue
        sec_type = str(row.get("SecurityTypeName") or "")
        quote_id = str(row.get("QuoteID") or "")
        suffix = _suffix_for_code(code, sec_type) or _suffix_for_code(code, quote_id)
        out.append(_candidate(
            code=code,
            name=str(row.get("Name") or ""),
            suffix=suffix,
            source="eastmoney",
            raw={
                "SecurityTypeName": row.get("SecurityTypeName"),
                "QuoteID": row.get("QuoteID"),
                "PinYin": row.get("PinYin"),
            },
        ))
    return out


def _resolve_sina(query: str) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query.strip())
    url = f"https://suggest3.sinajs.cn/suggest/type=11,12,13,14,15&key={encoded}&name=suggestdata"
    text = _fetch(url, encoding="gbk")
    m = re.search(r'"(.*)"', text, re.S)
    if not m:
        return []
    payload = m.group(1)
    out = []
    for item in payload.split(";"):
        fields = item.split(",")
        if len(fields) < 4:
            continue
        name, _type, code, symbol = fields[:4]
        if not re.fullmatch(r"\d{6}", code):
            continue
        symbol_lower = symbol.lower()
        hint = "sh" if symbol_lower.startswith("sh") else "sz" if symbol_lower.startswith("sz") else ""
        suffix = _suffix_for_code(code, hint)
        out.append(_candidate(
            code=code,
            name=name,
            suffix=suffix,
            source="sina",
            raw={"symbol": symbol, "type": _type},
        ))
    return out


def _dedupe(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    out = []
    for c in candidates:
        key = (c.get("code"), c.get("suffix"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def resolve(query: str) -> dict[str, Any]:
    query = query.strip()
    if not query:
        return {"query": query, "status": "error", "error": "empty query", "candidates": []}

    candidates = _resolve_code(query)
    errors = []

    if not candidates:
        try:
            candidates.extend(_resolve_eastmoney(query))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"eastmoney: {exc}")
        if not candidates:
            try:
                candidates.extend(_resolve_sina(query))
            except Exception as exc:  # noqa: BLE001
                errors.append(f"sina: {exc}")

    candidates = _dedupe(candidates)
    status = "ok" if candidates else "not_found"
    result = {"query": query, "status": status, "candidates": candidates}
    if errors:
        result["errors"] = errors
    return result


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="A-share code, Yahoo ticker, or Chinese stock name")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args(argv)

    result = resolve(args.query)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["status"] != "ok":
            print(f"未找到: {result['query']}")
            if result.get("errors"):
                print("; ".join(result["errors"]))
            return 1
        for c in result["candidates"]:
            print(f"{c['name'] or result['query']} {c['code']} {c['exchange']} {c.get('yahoo_ticker') or 'suffix待确认'} [{c['source']}]")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
