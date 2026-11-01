#!/usr/bin/env python3
"""校验脱敏博客文章的基础结构、代码围栏和本地图片链接。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


IMAGE_PATTERN = re.compile(r"!\[[^\]]*]\(([^)]+)\)")
INTERNAL_IP_PATTERN = re.compile(
    r"(?<!\d)(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
    r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?!\d)"
)
LONG_ID_PATTERN = re.compile(r"(?<!\d)\d{12,}(?!\d)")
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(?:password|passwd|token|secret|access[_ -]?key|authorization)"
    r"\s*[:=]\s*[^\s\"']+"
)


def parse_args() -> argparse.Namespace:
    """解析校验参数。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path, help="待校验 Markdown 文章")
    parser.add_argument(
        "--deny",
        action="append",
        default=[],
        help="禁止出现的非机密业务标识，可重复传入",
    )
    return parser.parse_args()


def resolve_local_image(article: Path, raw_target: str) -> Path | None:
    """解析 Markdown 图片目标；远程和 data URL 不做本地存在性检查。"""
    target = raw_target.strip().strip("<>")
    if " " in target:
        target = target.split(" ", 1)[0]
    parsed = urlsplit(target)
    if parsed.scheme in {"http", "https", "data"}:
        return None
    local_path = Path(unquote(parsed.path))
    if not local_path.is_absolute():
        local_path = article.parent / local_path
    return local_path.resolve()


def collect_issues(
    article: Path,
    text: str,
    deny_terms: list[str],
) -> tuple[list[str], list[str]]:
    """收集阻断错误和需要人工复核的警告。"""
    errors: list[str] = []
    warnings: list[str] = []
    lines = text.splitlines()

    if article.suffix.lower() != ".md":
        errors.append("文章扩展名不是 .md")
    if not text.strip():
        errors.append("文章为空")
    if not any(line.startswith("# ") for line in lines):
        errors.append("缺少一级标题")
    if "{{" in text or "}}" in text or "[TODO" in text:
        errors.append("文章仍包含模板占位符或 TODO")

    trailing_lines = [
        str(index)
        for index, line in enumerate(lines, 1)
        if line.rstrip() != line
    ]
    if trailing_lines:
        errors.append(f"存在尾随空格，行号：{', '.join(trailing_lines[:10])}")

    backtick_fence = chr(96) * 3
    has_mermaid = any(
        line.strip().casefold() in {"~~~mermaid", f"{backtick_fence}mermaid"}
        for line in lines
    )
    if has_mermaid:
        errors.append("检测到 Mermaid 代码块，请生成 PNG/WebP 并替换后再发布")

    fence_count = sum(
        1
        for line in lines
        if line.startswith(backtick_fence) or line.startswith("~~~")
    )
    if fence_count % 2:
        errors.append("Markdown 代码围栏数量不是偶数")

    for raw_target in IMAGE_PATTERN.findall(text):
        image_path = resolve_local_image(article, raw_target)
        if image_path is not None and not image_path.is_file():
            errors.append(f"本地图片不存在：{raw_target}")

    lowered = text.casefold()
    for term in deny_terms:
        normalized = term.strip()
        if normalized and normalized.casefold() in lowered:
            errors.append(f"命中禁止业务标识：{normalized}")

    if INTERNAL_IP_PATTERN.search(text):
        errors.append("检测到内网 IPv4 地址")
    if SECRET_ASSIGNMENT_PATTERN.search(text):
        errors.append("检测到疑似明文凭证赋值")
    if LONG_ID_PATTERN.search(text):
        warnings.append("检测到 12 位以上连续数字，请人工确认是否为业务标识")

    return errors, warnings


def main() -> int:
    """执行文章校验并返回适合自动化调用的退出码。"""
    args = parse_args()
    article = args.article.expanduser().resolve()
    if not article.is_file():
        print(f"[ERROR] 文章不存在：{article}", file=sys.stderr)
        return 1

    text = article.read_text(encoding="utf-8")
    errors, warnings = collect_issues(article, text, args.deny)

    for warning in warnings:
        print(f"[WARN] {warning}")
    for error in errors:
        print(f"[ERROR] {error}", file=sys.stderr)

    if errors:
        print(
            f"[FAILED] {len(errors)} 个错误，{len(warnings)} 个警告",
            file=sys.stderr,
        )
        return 1

    print(f"[OK] {article}")
    print(f"[OK] {len(text.splitlines())} 行，{len(warnings)} 个警告")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
