#!/usr/bin/env python3
"""安全推送 Git 分支并通过 Codeup GitLab V4 API 创建合并请求。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


def _run_git(*args: str) -> str:
    """执行只读或普通推送 Git 命令，并返回去除空白的标准输出。"""
    completed = subprocess.run(["git", *args], text=True, capture_output=True, check=False)
    if completed.returncode:
        message = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise RuntimeError(message)
    return completed.stdout.strip()


def _current_branch() -> str:
    """拒绝 detached HEAD，确保 MR 的源分支可稳定推送。"""
    branch = _run_git("branch", "--show-current")
    if not branch:
        raise RuntimeError("当前处于 detached HEAD，无法创建合并请求")
    return branch


def _require_clean_worktree() -> None:
    """阻止把未提交或未跟踪的文件误发布到远端。"""
    if _run_git("status", "--porcelain"):
        raise RuntimeError("工作区不干净；请先提交、暂存或处理本地改动")


def _request_json(base_url: str, project_id: str, token: str, method: str, path: str, data: dict[str, str] | None = None) -> Any:
    """调用 Codeup GitLab V4 API，错误信息不包含认证头或请求体。"""
    url = f"{base_url.rstrip('/')}/api/v4/projects/{quote(project_id, safe='')}{path}"
    body = urlencode(data).encode("utf-8") if data else None
    headers = {"PRIVATE-TOKEN": token}
    if body:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = Request(url, data=body, method=method, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Codeup API 请求失败（HTTP {exc.code}）") from exc
    except URLError as exc:
        raise RuntimeError(f"无法连接 Codeup API：{exc.reason}") from exc


def _description(args: argparse.Namespace) -> str:
    """从互斥的内联参数或文件读取合并请求说明。"""
    if args.description_file:
        return Path(args.description_file).read_text(encoding="utf-8")
    return args.description or ""


def _open_merge_request(base_url: str, project_id: str, token: str, source: str, target: str) -> dict[str, Any] | None:
    """先复用同源同目标的开放 MR，避免重复提交审查请求。"""
    query = urlencode({"state": "opened", "source_branch": source, "target_branch": target})
    items = _request_json(base_url, project_id, token, "GET", f"/merge_requests?{query}")
    return items[0] if isinstance(items, list) and items else None


def _parse_args() -> argparse.Namespace:
    """解析发布所需参数，令牌和项目 ID 优先从环境读取。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", default=os.environ.get("CODEUP_PROJECT_ID"))
    parser.add_argument("--target-branch", required=True)
    parser.add_argument("--source-branch")
    parser.add_argument("--title")
    parser.add_argument("--description")
    parser.add_argument("--description-file")
    parser.add_argument("--base-url", default=os.environ.get("CODEUP_BASE_URL", "https://codeup.aliyun.com"))
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--confirm", action="store_true", help="确认执行 git push 和 Codeup API 写操作")
    args = parser.parse_args()
    if not args.project_id:
        parser.error("缺少 --project-id 或 CODEUP_PROJECT_ID")
    if args.description and args.description_file:
        parser.error("--description 与 --description-file 只能选择一个")
    return args


def main() -> int:
    """执行预检查；只有显式确认才推送并创建外部合并请求。"""
    args = _parse_args()
    _require_clean_worktree()
    source = args.source_branch or _current_branch()
    if source == args.target_branch:
        raise RuntimeError("源分支与目标分支不能相同")
    _run_git("remote", "get-url", args.remote)
    title = args.title or _run_git("log", "-1", "--format=%s")
    if not title:
        raise RuntimeError("缺少合并请求标题")
    plan = {"project_id": args.project_id, "source_branch": source, "target_branch": args.target_branch, "title": title}
    if not args.confirm:
        print(json.dumps({"mode": "preflight", "would_push": True, "would_create_merge_request": True, **plan}, ensure_ascii=False))
        return 0
    token = os.environ.get("CODEUP_PRIVATE_TOKEN")
    if not token:
        raise RuntimeError("缺少 CODEUP_PRIVATE_TOKEN")
    _run_git("push", "--set-upstream", args.remote, source)
    existing = _open_merge_request(args.base_url, args.project_id, token, source, args.target_branch)
    if existing:
        print(json.dumps({"created": False, "iid": existing.get("iid"), "web_url": existing.get("web_url"), **plan}, ensure_ascii=False))
        return 0
    created = _request_json(args.base_url, args.project_id, token, "POST", "/merge_requests", {
        "source_branch": source,
        "target_branch": args.target_branch,
        "title": title,
        "description": _description(args),
    })
    print(json.dumps({"created": True, "iid": created.get("iid"), "web_url": created.get("web_url"), **plan}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        raise SystemExit(1)
