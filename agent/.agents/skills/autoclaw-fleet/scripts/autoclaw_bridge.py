#!/usr/bin/env python3
"""Run tasks on a two-node OpenClaw/AutoClaw Gateway fleet."""

from __future__ import annotations

import argparse
import concurrent.futures
import dataclasses
import datetime as dt
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Callable
from urllib import error, parse, request


DEFAULT_TARGETS = ("publish", "login-reply")
DEFAULT_GATEWAY_URLS = {
    "publish": "http://172.16.16.2:18790",
    "login-reply": "http://172.16.16.3:18789",
}
TRUTHY = {"1", "true", "yes", "on"}


class BridgeError(RuntimeError):
    pass


@dataclasses.dataclass(frozen=True)
class Target:
    name: str
    gateway_url: str
    http_url: str
    token: str
    token_source: str
    model: str
    agent_id: str | None


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def env_prefix(name: str) -> str:
    return "AUTOCLAW_" + re.sub(r"[^A-Za-z0-9]", "_", name).upper()


def configured_target_names() -> list[str]:
    raw = os.environ.get("AUTOCLAW_TARGETS", ",".join(DEFAULT_TARGETS))
    names = [part.strip() for part in raw.split(",") if part.strip()]
    if not names:
        raise BridgeError("AUTOCLAW_TARGETS is empty")
    if len(set(names)) != len(names):
        raise BridgeError("AUTOCLAW_TARGETS contains duplicate names")
    return names


def selected_target_names(value: str) -> list[str]:
    configured = configured_target_names()
    requested = configured if value == "all" else [part.strip() for part in value.split(",") if part.strip()]
    unknown = [name for name in requested if name not in configured]
    if unknown:
        raise BridgeError(f"unknown target(s): {', '.join(unknown)}")
    return requested


def allow_insecure_transport() -> bool:
    return os.environ.get("AUTOCLAW_ALLOW_INSECURE_HTTP", "").lower() in TRUTHY


def is_loopback(hostname: str | None) -> bool:
    return hostname in {"127.0.0.1", "::1", "localhost"}


def normalize_gateway_url(name: str, value: str, *, enforce_secure: bool) -> tuple[str, str]:
    gateway_url = value.strip().rstrip("/")
    parsed = parse.urlparse(gateway_url)
    if parsed.scheme not in {"ws", "wss", "http", "https"} or not parsed.hostname:
        raise BridgeError(f"gateway URL for {name} must use ws(s) or http(s)")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise BridgeError(f"gateway URL for {name} must not contain credentials, a query, or a fragment")
    if parsed.path not in {"", "/"}:
        raise BridgeError(f"gateway URL for {name} must not contain an API path")
    insecure = parsed.scheme in {"ws", "http"} and not is_loopback(parsed.hostname)
    if insecure and enforce_secure and not allow_insecure_transport():
        raise BridgeError(
            f"refusing full-operator credential over plaintext transport for {name}; use WSS/HTTPS, "
            "an SSH/VPN loopback tunnel, or explicitly set AUTOCLAW_ALLOW_INSECURE_HTTP=1"
        )
    http_scheme = "https" if parsed.scheme in {"wss", "https"} else "http"
    http_url = parse.urlunparse((http_scheme, parsed.netloc, "", "", "", ""))
    return gateway_url, http_url.rstrip("/")


def read_token_file(path: Path) -> str:
    try:
        mode = path.stat().st_mode & 0o777
    except OSError as exc:
        raise BridgeError(f"cannot stat token file {path}: {exc}") from exc
    if mode & 0o077:
        raise BridgeError(f"token file {path} must not be accessible by group/others (use chmod 600)")
    return path.read_text(encoding="utf-8").strip()


def read_keychain_token(name: str) -> str:
    security = shutil.which("security")
    if not security:
        return ""
    result = subprocess.run(
        [security, "find-generic-password", "-a", name, "-s", "autoclaw-fleet", "-w"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def resolve_token(name: str) -> tuple[str, str]:
    prefix = env_prefix(name)
    env_token = os.environ.get(prefix + "_TOKEN", "").strip()
    if env_token:
        return env_token, "environment"
    token_file = os.environ.get(prefix + "_TOKEN_FILE", "").strip()
    if token_file:
        token = read_token_file(Path(token_file).expanduser())
        return token, "file"
    keychain_token = read_keychain_token(name)
    if keychain_token:
        return keychain_token, "macos-keychain"
    return "", "missing"


def load_target(name: str, require_token: bool = True) -> Target:
    prefix = env_prefix(name)
    raw_url = os.environ.get(prefix + "_URL", DEFAULT_GATEWAY_URLS.get(name, ""))
    if not raw_url:
        raise BridgeError(f"{prefix}_URL is not set")
    gateway_url, http_url = normalize_gateway_url(name, raw_url, enforce_secure=require_token)
    token, token_source = resolve_token(name)
    if require_token and not token:
        raise BridgeError(
            f"no token for {name}; set {prefix}_TOKEN, {prefix}_TOKEN_FILE, "
            f"or macOS Keychain service autoclaw-fleet/account {name}"
        )
    agent_id = os.environ.get(prefix + "_AGENT_ID", "").strip() or None
    model = os.environ.get(prefix + "_MODEL", "").strip()
    if not model:
        model = f"openclaw/{agent_id}" if agent_id else "openclaw"
    return Target(name, gateway_url, http_url, token, token_source, model, agent_id)


def request_json(
    target: Target,
    path: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    authenticated: bool = True,
    timeout: float = 15,
) -> Any:
    headers = {"Accept": "application/json"}
    if authenticated:
        if not target.token:
            raise BridgeError(f"token is required for {target.name}")
        headers["Authorization"] = f"Bearer {target.token}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = request.Request(target.http_url + path, data=data, headers=headers, method=method)
    hostname = parse.urlparse(target.http_url).hostname
    try:
        private_target = bool(hostname and ipaddress.ip_address(hostname).is_private)
    except ValueError:
        private_target = False
    opener = request.build_opener(request.ProxyHandler({})) if private_target else request.build_opener()
    try:
        with opener.open(req, timeout=timeout) as response:
            raw = response.read()
    except error.HTTPError as exc:
        detail = exc.read(1500).decode("utf-8", errors="replace").strip()
        hint = ""
        if exc.code == 404 and path.startswith("/v1/"):
            hint = "; enable gateway.http.endpoints.chatCompletions.enabled on the Gateway"
        raise BridgeError(f"HTTP {exc.code} from {target.name}: {detail or exc.reason}{hint}") from exc
    except error.URLError as exc:
        raise BridgeError(f"cannot reach {target.name}: {exc.reason}") from exc
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BridgeError(f"invalid JSON response from {target.name}") from exc


def run_parallel(targets: list[Target], operation: Callable[[Target], Any]) -> tuple[dict[str, Any], bool]:
    results: dict[str, Any] = {}
    failed = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(targets)) as pool:
        futures = {pool.submit(operation, target): target for target in targets}
        for future in concurrent.futures.as_completed(futures):
            target = futures[future]
            try:
                results[target.name] = {"ok": True, "data": future.result()}
            except Exception as exc:  # Preserve the healthy peer's result.
                failed = True
                results[target.name] = {"ok": False, "error": str(exc)}
    return {target.name: results[target.name] for target in targets}, failed


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def load_selected(value: str, require_token: bool = True) -> list[Target]:
    return [load_target(name, require_token=require_token) for name in selected_target_names(value)]


def command_config(_: argparse.Namespace) -> int:
    rows: dict[str, Any] = {}
    for name in configured_target_names():
        prefix = env_prefix(name)
        token, token_source = resolve_token(name)
        rows[name] = {
            "gateway_url": os.environ.get(prefix + "_URL", DEFAULT_GATEWAY_URLS.get(name)) or None,
            "token_configured": bool(token),
            "token_source": token_source,
            "model": os.environ.get(prefix + "_MODEL") or (
                f"openclaw/{os.environ[prefix + '_AGENT_ID']}"
                if os.environ.get(prefix + "_AGENT_ID")
                else "openclaw"
            ),
            "agent_id": os.environ.get(prefix + "_AGENT_ID") or None,
        }
    print_json({"targets": rows})
    return 0


def command_health(args: argparse.Namespace) -> int:
    targets = load_selected(args.target, require_token=False)
    results, failed = run_parallel(
        targets,
        lambda target: request_json(target, "/healthz", authenticated=False, timeout=args.timeout),
    )
    print_json({"operation": "health", "targets": results})
    return 1 if failed else 0


def command_status(args: argparse.Namespace) -> int:
    targets = load_selected(args.target)
    results, failed = run_parallel(
        targets,
        lambda target: request_json(target, "/v1/models", timeout=args.timeout),
    )
    print_json({"operation": "status", "targets": results})
    return 1 if failed else 0


def read_prompt(args: argparse.Namespace) -> str:
    prompt = Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else args.prompt
    if not prompt or not prompt.strip():
        raise BridgeError("prompt must not be empty")
    return prompt.strip()


def dispatch_one(
    target: Target,
    prompt: str,
    task_id: str,
    session: str | None,
    timeout: float,
    max_completion_tokens: int | None,
) -> Any:
    body: dict[str, Any] = {
        "model": target.model,
        "user": session or f"codex:{task_id}",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    if max_completion_tokens is not None:
        body["max_completion_tokens"] = max_completion_tokens
    return request_json(target, "/v1/chat/completions", method="POST", body=body, timeout=timeout)


def dispatch_sync(spec: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    targets = [load_target(name) for name in spec["target_names"]]
    return run_parallel(
        targets,
        lambda target: dispatch_one(
            target,
            spec["prompt"],
            spec["task_id"],
            spec.get("session"),
            float(spec["timeout"]),
            spec.get("max_completion_tokens"),
        ),
    )


def jobs_root() -> Path:
    configured = os.environ.get("AUTOCLAW_JOB_DIR", "").strip()
    root = Path(configured).expanduser() if configured else Path.home() / ".codex" / "autoclaw-fleet" / "jobs"
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    return root


def write_private_json(path: Path, value: Any) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def spawn_background(spec: dict[str, Any]) -> dict[str, Any]:
    job_id = f"job-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    job_dir = jobs_root() / job_id
    job_dir.mkdir(mode=0o700)
    log_fd = os.open(job_dir / "worker.log", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    process = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "_background", "--job-id", job_id],
        stdin=subprocess.PIPE,
        stdout=log_fd,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    os.close(log_fd)
    meta = {
        "job_id": job_id,
        "task_id": spec["task_id"],
        "targets": spec["target_names"],
        "pid": process.pid,
        "state": "running",
        "started_at": utc_now(),
    }
    write_private_json(job_dir / "meta.json", meta)
    assert process.stdin is not None
    process.stdin.write(json.dumps(spec, ensure_ascii=False).encode("utf-8"))
    process.stdin.close()
    return meta


def command_dispatch(args: argparse.Namespace) -> int:
    target_names = selected_target_names(args.target)
    task_id = args.task_id or f"codex-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    spec = {
        "target_names": target_names,
        "prompt": read_prompt(args),
        "task_id": task_id,
        "session": args.session,
        "timeout": args.timeout,
        "max_completion_tokens": args.max_completion_tokens,
    }
    if args.background:
        meta = spawn_background(spec)
        print_json({"operation": "dispatch", "background": True, **meta})
        return 0
    results, failed = dispatch_sync(spec)
    print_json({"operation": "dispatch", "background": False, "task_id": task_id, "targets": results})
    return 1 if failed else 0


def process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def command_job(args: argparse.Namespace) -> int:
    job_dir = jobs_root() / args.job_id
    meta_path = job_dir / "meta.json"
    if not meta_path.exists():
        raise BridgeError(f"unknown job id: {args.job_id}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    result_path = job_dir / "result.json"
    if result_path.exists():
        result = json.loads(result_path.read_text(encoding="utf-8"))
        print_json({"meta": meta, "result": result})
        return 1 if result.get("failed") else 0
    state = "running" if process_exists(int(meta["pid"])) else "worker-exited-without-result"
    print_json({"meta": meta, "state": state})
    return 0 if state == "running" else 1


def command_background(args: argparse.Namespace) -> int:
    job_dir = jobs_root() / args.job_id
    spec = json.load(sys.stdin)
    results, failed = dispatch_sync(spec)
    result = {
        "job_id": args.job_id,
        "task_id": spec["task_id"],
        "finished_at": utc_now(),
        "failed": failed,
        "targets": results,
    }
    write_private_json(job_dir / "result.json", result)
    meta_path = job_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["state"] = "failed" if failed else "complete"
        meta["finished_at"] = result["finished_at"]
        write_private_json(meta_path, meta)
    print_json({"ok": not failed, "job_id": args.job_id})
    return 1 if failed else 0


def add_target_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", default="all", help="target name, comma-separated names, or all")


def add_timeout_argument(parser: argparse.ArgumentParser, default: float) -> None:
    parser.add_argument("--timeout", type=float, default=default, help="timeout in seconds")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    config_parser = subparsers.add_parser("config", help="show redacted target configuration")
    config_parser.set_defaults(func=command_config)

    health_parser = subparsers.add_parser("health", help="check Gateway HTTP liveness")
    add_target_argument(health_parser)
    add_timeout_argument(health_parser, 10)
    health_parser.set_defaults(func=command_health)

    status_parser = subparsers.add_parser("status", help="verify auth and OpenAI-compatible endpoint")
    add_target_argument(status_parser)
    add_timeout_argument(status_parser, 15)
    status_parser.set_defaults(func=command_status)

    dispatch_parser = subparsers.add_parser("dispatch", help="run an agent task")
    add_target_argument(dispatch_parser)
    prompt_group = dispatch_parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file")
    dispatch_parser.add_argument("--task-id")
    dispatch_parser.add_argument("--session", help="stable OpenClaw conversation identifier")
    dispatch_parser.add_argument("--background", action="store_true", help="run the HTTP request in a detached local worker")
    dispatch_parser.add_argument("--max-completion-tokens", type=int)
    add_timeout_argument(dispatch_parser, 1800)
    dispatch_parser.set_defaults(func=command_dispatch)

    job_parser = subparsers.add_parser("job", help="show a background job result")
    job_parser.add_argument("--job-id", required=True)
    job_parser.set_defaults(func=command_job)

    return parser


def main() -> int:
    try:
        if len(sys.argv) == 4 and sys.argv[1:3] == ["_background", "--job-id"]:
            return command_background(argparse.Namespace(job_id=sys.argv[3]))
        args = build_parser().parse_args()
        if hasattr(args, "timeout") and args.timeout <= 0:
            raise BridgeError("--timeout must be positive")
        if hasattr(args, "max_completion_tokens") and args.max_completion_tokens is not None:
            if args.max_completion_tokens <= 0:
                raise BridgeError("--max-completion-tokens must be positive")
        return int(args.func(args))
    except (BridgeError, OSError, ValueError, json.JSONDecodeError) as exc:
        print_json({"ok": False, "error": str(exc)})
        return 2


if __name__ == "__main__":
    sys.exit(main())
