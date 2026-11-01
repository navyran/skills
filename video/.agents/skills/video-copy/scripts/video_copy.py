#!/usr/bin/env python3
"""Run the internal video-copy workflow through remote app APIs."""

from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.request import urlretrieve

requests: Any = None


SKILL_DIR = Path(__file__).resolve().parents[1]
PROMPT_SOURCE_DIR = SKILL_DIR / "assets" / "prompts"

# Internal deployment values are centralized here. Override with
# VIDEO_COPY_API_BASE_URL / VIDEO_COPY_API_KEY when testing another deployment.
INTERNAL_API_BASE_URL = "http://121.36.14.67:5176"
INTERNAL_API_KEY = "cvk_01_JMMeZHbm5jHj_AoN9wUjnneXijobcCxw"

ENDPOINTS = {
    "health": "/v1/health",
    "files": "/v1/files",
    "video_analysis": "/v1/video-analyses",
    "image_gen": "/v1/images",
    "text_generation": "/v1/text-generations",
    "video_gen": "/v1/video-generations",
}

STEP_ORDER = ("analysis", "frames", "character", "background", "prompt", "video")
PROMPT_FILES = {
    "analysis": "01_video_analysis.md",
    "character": "02_character_card.md",
    "background": "03_background_image.md",
    "prompt": "04_scene_video_prompt.md",
    "video": "05_scene_video_generation.md",
}
PROMPT_EXPORT_FILES = {
    "analysis": "01_video_analysis.md",
    "character": "02_character_card.md",
    "background": "03_background_image.md",
    "scene_prompt": "04_scene_video_prompt.md",
    "video_wrapper": "05_scene_video_generation.md",
}
PROMPT_KEY_ALIASES = {
    "prompt": "scene_prompt",
    "video": "video_wrapper",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
MAX_PRODUCT_IMAGES = 5
MAX_VIDEO_REFERENCE_IMAGES = 9
DEFAULT_VIDEO_WORKERS = 3


def now_id() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def get_requests() -> Any:
    global requests
    if requests is None:
        try:
            import requests as requests_module
        except ImportError as exc:
            raise RuntimeError("Remote API steps require the requests package.") from exc
        requests = requests_module
    return requests


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return value.strip("._") or "file"


def api_base_url() -> str:
    value = os.environ.get("VIDEO_COPY_API_BASE_URL") or INTERNAL_API_BASE_URL
    if not value:
        raise RuntimeError("Internal video-copy API base URL is not configured in the skill.")
    return value.rstrip("/")


def api_key() -> str:
    return os.environ.get("VIDEO_COPY_API_KEY") or INTERNAL_API_KEY


def api_url(name: str) -> str:
    return f"{api_base_url()}{ENDPOINTS[name]}"


def auth_headers() -> dict[str, str]:
    key = api_key()
    return {"Authorization": f"Bearer {key}"} if key else {}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: ("<redacted>" if str(key).lower() in {"authorization", "api_key", "token"} else redact(item))
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str) and value.startswith("data:") and ";base64," in value:
        prefix, b64 = value.split(",", 1)
        return f"{prefix},<{len(b64)} chars>"
    return value


def render_template(template: str, context: dict[str, Any]) -> str:
    def replace(match: re.Match) -> str:
        key = match.group(1).strip()
        value = context.get(key, "")
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)

    return re.sub(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}", replace, template)


def copy_input_file(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / safe_name(src.name)
    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)
    return dst


def collect_product_images(paths: list[str], run_dir: Path) -> list[str]:
    image_dir = run_dir / "product" / "images"
    candidates: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            children = [child for child in sorted(path.iterdir()) if child.suffix.lower() in IMAGE_EXTENSIONS]
        elif path.exists():
            children = [path]
        else:
            raise FileNotFoundError(f"Product image not found: {raw}")
        for child in children:
            resolved = child.resolve()
            if resolved not in seen:
                candidates.append(child)
                seen.add(resolved)

    copied: list[str] = []
    for image in candidates[:MAX_PRODUCT_IMAGES]:
        copied.append(str(copy_input_file(image, image_dir)))
    return copied


def initialize_run(args: argparse.Namespace) -> Path:
    run_dir = Path(args.workdir or f"video-copy-{now_id()}").resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    if not args.video:
        raise ValueError("--video is required for init")
    video = Path(args.video).expanduser()
    if not video.exists():
        raise FileNotFoundError(f"Target video not found: {args.video}")
    video_path = copy_input_file(video, run_dir / "inputs")

    product_dir = run_dir / "product"
    product_dir.mkdir(parents=True, exist_ok=True)
    if args.product_file:
        product_text = read_text(Path(args.product_file).expanduser())
    else:
        product_text = args.product_description or ""
    if not product_text.strip():
        raise ValueError("Provide --product-file or --product-description")
    write_text(product_dir / "product.md", product_text)

    product_images = collect_product_images(args.product_images or [], run_dir)
    if not product_images:
        raise ValueError("Provide at least one --product-image path or directory")

    prompt_dir = run_dir / "prompts"
    prompt_dir.mkdir(exist_ok=True)
    for src in sorted(PROMPT_SOURCE_DIR.glob("*.md")):
        dst = prompt_dir / src.name
        if not dst.exists():
            shutil.copy2(src, dst)

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_video": str(video_path),
        "product_description": str(product_dir / "product.md"),
        "product_images": product_images,
        "steps": {},
        "api_endpoints": ENDPOINTS,
    }
    write_json(run_dir / "manifest.json", manifest)
    return run_dir


def work_context(run_dir: Path, extra: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    manifest = load_json(run_dir / "manifest.json", {})
    analysis = load_json(run_dir / "outputs" / "analysis.json", {})
    product_images = manifest.get("product_images", [])[:MAX_PRODUCT_IMAGES]
    last_product_ref = len(product_images) + 2
    product_reference_range = "无产品参考图" if not product_images else (
        "图片3" if last_product_ref == 3 else f"图片3-图片{last_product_ref}"
    )
    context = {
        "run_dir": str(run_dir),
        "source_video": manifest.get("source_video", ""),
        "product_description": read_text(Path(manifest["product_description"])) if manifest.get("product_description") else "",
        "product_images": product_images,
        "product_reference_range": product_reference_range,
        "analysis_json": analysis,
    }
    if extra:
        context.update(extra)
    return context


def post_json(name: str, payload: dict[str, Any], record_path: Path) -> dict[str, Any]:
    record_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(record_path, {"endpoint": name, "url": api_url(name), "payload": redact(payload)})
    client = get_requests()
    response = client.post(
        api_url(name),
        headers={"Content-Type": "application/json", **auth_headers()},
        json=payload,
        timeout=300,
    )
    return parse_response(name, response)


def post_form_file(
    name: str,
    *,
    data: dict[str, Any],
    files: dict[str, Path],
    record_path: Path,
) -> dict[str, Any]:
    record_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(
        record_path,
        {
            "endpoint": name,
            "url": api_url(name),
            "data": redact(data),
            "files": {field: str(path) for field, path in files.items()},
        },
    )

    opened = []
    try:
        multipart = {}
        for field, path in files.items():
            mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
            handle = open(path, "rb")
            opened.append(handle)
            multipart[field] = (path.name, handle, mime)
        client = get_requests()
        response = client.post(
            api_url(name),
            headers=auth_headers(),
            data=data,
            files=multipart,
            timeout=300,
        )
    finally:
        for handle in opened:
            handle.close()
    return parse_response(name, response)


def get_json(name: str, suffix: str = "", params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    client = get_requests()
    response = client.get(
        f"{api_url(name)}{suffix}",
        headers=auth_headers(),
        params=params or {},
        timeout=120,
    )
    return parse_response(name, response)


def parse_response(name: str, response: requests.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        data = {"status_code": response.status_code, "text": response.text}
    if response.status_code >= 400:
        raise RuntimeError(f"{name} failed: HTTP {response.status_code}: {str(data)[:500]}")
    return data


def upload_asset(path: Path, asset_type: str, record_path: Path) -> dict[str, Any]:
    return post_form_file(
        "files",
        data={"asset_type": asset_type},
        files={"file": path},
        record_path=record_path,
    )


def product_urls(run_dir: Path, asset_type: str) -> list[str]:
    manifest = load_json(run_dir / "manifest.json")
    cache_key = f"product_{asset_type}_urls"
    if manifest.get(cache_key):
        return manifest[cache_key][:MAX_PRODUCT_IMAGES]

    urls = []
    for index, image in enumerate(manifest.get("product_images", [])[:MAX_PRODUCT_IMAGES], start=1):
        result = upload_asset(
            Path(image),
            asset_type,
            run_dir / "requests" / f"upload_product_{index}_{asset_type}.json",
        )
        write_json(run_dir / "responses" / f"upload_product_{index}_{asset_type}.json", result)
        urls.append(result["url"])

    manifest[cache_key] = urls
    manifest["product_images"] = manifest.get("product_images", [])[:MAX_PRODUCT_IMAGES]
    write_json(run_dir / "manifest.json", manifest)
    return urls


def response_image_url(data: dict[str, Any]) -> str:
    for key in ("image_url", "url", "output_url"):
        value = data.get(key)
        if isinstance(value, str):
            return value
    if isinstance(data.get("data"), list) and data["data"]:
        item = data["data"][0] or {}
        return item.get("url") or item.get("b64_json") or ""
    return data.get("path", "")


def response_video_url(data: dict[str, Any]) -> str:
    content = data.get("content") if isinstance(data.get("content"), dict) else {}
    for value in (content.get("video_url"), data.get("video_url"), data.get("url"), data.get("output_url")):
        if isinstance(value, str) and value:
            return value
    return ""


def poll_video_task(task_id: str, response_path: Path, interval: int = 15, timeout: int = 900) -> dict[str, Any]:
    start = time.time()
    last = {}
    while True:
        result = get_json("video_gen", suffix=f"/{task_id}")
        write_json(response_path, result)
        last = result
        status = result.get("status")
        if status == "succeeded":
            return result
        if status in {"failed", "expired"}:
            raise RuntimeError(f"Video task {task_id} ended with status={status}: {result}")
        if time.time() - start > timeout:
            raise TimeoutError(f"Video task {task_id} did not finish within {timeout}s. Last response: {last}")
        time.sleep(interval)


def save_remote_or_b64(value: str, output_path: Path) -> Optional[Path]:
    if not value:
        return None
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if value.startswith("data:") and ";base64," in value:
        b64 = value.split(",", 1)[1]
        output_path.write_bytes(base64.b64decode(b64))
        return output_path
    if re.match(r"^[A-Za-z0-9+/=\s]{100,}$", value):
        output_path.write_bytes(base64.b64decode(re.sub(r"\s+", "", value)))
        return output_path
    if value.startswith(("http://", "https://")):
        urlretrieve(value, output_path)
        return output_path
    local = Path(value)
    if local.exists():
        shutil.copy2(local, output_path)
        return output_path
    return None


def parse_scenes(analysis: dict[str, Any]) -> list[dict[str, Any]]:
    scenes = analysis.get("scenes") or analysis.get("shots") or []
    if not isinstance(scenes, list) or not scenes:
        raise RuntimeError("Video analysis response did not include scenes/shots.")
    normalized = []
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            continue
        item = dict(scene)
        item.setdefault("scene_index", index)
        start, end = scene_bounds(item)
        item["start_seconds"] = start
        item["end_seconds"] = end
        normalized.append(item)
    if not normalized:
        raise RuntimeError("No usable scene objects found in analysis response.")
    return normalized


def scene_bounds(scene: dict[str, Any]) -> tuple[float, float]:
    if "start_seconds" in scene and "end_seconds" in scene:
        return float(scene["start_seconds"]), float(scene["end_seconds"])
    if isinstance(scene.get("t"), list) and len(scene["t"]) >= 2:
        return float(scene["t"][0]), float(scene["t"][1])
    text = str(scene.get("time_range", ""))
    nums = re.findall(r"(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if len(nums) >= 2:
        vals = []
        for h, m, s in nums[:2]:
            vals.append(int(h) * 3600 + int(m) * 60 + float(s))
        return vals[0], vals[1]
    raise RuntimeError(f"Scene lacks guaranteed timing fields: {scene}")


def step_analysis(run_dir: Path) -> None:
    prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["analysis"]), work_context(run_dir))
    video_path = Path(load_json(run_dir / "manifest.json")["source_video"])
    data = post_form_file(
        "video_analysis",
        data={
            "prompt": prompt,
            "model": "gemini-3.5-flash",
            "max_tokens": "24000",
            "temperature": "0.1",
        },
        files={"video": video_path},
        record_path=run_dir / "requests" / "01_video_analysis.json",
    )
    write_json(run_dir / "responses" / "01_video_analysis.json", data)
    write_json(run_dir / "outputs" / "analysis.json", data)

    scenes = parse_scenes(data)
    for scene in scenes:
        scene_dir = run_dir / "scenes" / f"scene_{int(scene['scene_index']):03d}"
        write_json(scene_dir / "scene.json", scene)


def extract_frame(video_path: Path, seconds: float, output_path: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-ss",
                f"{max(0.0, seconds):.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                "-q:v",
                "2",
                str(output_path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0 and output_path.exists():
            return

    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("Frame extraction requires opencv-python or opencv-python-headless.") from exc
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open source video: {video_path}")
    try:
        cap.set(cv2.CAP_PROP_POS_MSEC, max(0.0, seconds) * 1000)
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError(f"Cannot extract frame at {seconds:.2f}s")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), frame)
    finally:
        cap.release()


def step_frames(run_dir: Path) -> None:
    manifest = load_json(run_dir / "manifest.json")
    video_path = Path(manifest["source_video"])
    for scene_path in sorted((run_dir / "scenes").glob("scene_*/scene.json")):
        scene = load_json(scene_path)
        start, end = scene_bounds(scene)
        extract_frame(video_path, (start + end) / 2, scene_path.parent / "source_frame.jpg")


def asset_scope(analysis: dict[str, Any], kind: str) -> str:
    plan = analysis.get("asset_plan") or {}
    section = plan.get(f"{kind}_generation") or {}
    scope = section.get("scope")
    if scope in {"global", "per_scene", "none"}:
        return scope
    return "per_scene"


def scene_dirs(run_dir: Path) -> list[Path]:
    return sorted(path.parent for path in (run_dir / "scenes").glob("scene_*/scene.json"))


def step_character(run_dir: Path) -> None:
    analysis = load_json(run_dir / "outputs" / "analysis.json")
    scope = asset_scope(analysis, "character")
    if scope == "none":
        return
    targets = [run_dir / "assets" / "characters" / "character_global"] if scope == "global" else scene_dirs(run_dir)
    for target in targets:
        if scope == "global":
            scene = {"scope": "global", "scenes": [load_json(d / "scene.json") for d in scene_dirs(run_dir)]}
            ref_frame = scene_dirs(run_dir)[0] / "source_frame.jpg"
            output_path = target.with_suffix(".png")
            req_path = run_dir / "requests" / "02_character_card_global.json"
            resp_path = run_dir / "responses" / "02_character_card_global.json"
        else:
            scene = load_json(target / "scene.json")
            ref_frame = target / "source_frame.jpg"
            output_path = target / "character_card.png"
            req_path = target / "character_card_request.json"
            resp_path = target / "character_card_response.json"
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["character"]), work_context(run_dir, {"scene_json": scene}))
        ref_upload = upload_asset(ref_frame, "image_data_uri", req_path.with_name(f"{req_path.stem}_source_frame_upload.json"))
        write_json(resp_path.with_name(f"{resp_path.stem}_source_frame_upload.json"), ref_upload)
        payload = {
            "prompt": prompt,
            "interface_type": "Nanoblana(gemini3-pro)",
            "image_urls": [ref_upload["url"], *product_urls(run_dir, "image_data_uri")],
        }
        data = post_json("image_gen", payload, req_path)
        write_json(resp_path, data)
        save_remote_or_b64(response_image_url(data), output_path)


def step_background(run_dir: Path) -> None:
    analysis = load_json(run_dir / "outputs" / "analysis.json")
    scope = asset_scope(analysis, "background")
    targets = [run_dir / "assets" / "backgrounds" / "background_global"] if scope == "global" else scene_dirs(run_dir)
    for target in targets:
        if scope == "global":
            scene = {"scope": "global", "scenes": [load_json(d / "scene.json") for d in scene_dirs(run_dir)]}
            ref_frame = scene_dirs(run_dir)[0] / "source_frame.jpg"
            output_path = target.with_suffix(".png")
            req_path = run_dir / "requests" / "03_background_global.json"
            resp_path = run_dir / "responses" / "03_background_global.json"
        else:
            scene = load_json(target / "scene.json")
            ref_frame = target / "source_frame.jpg"
            output_path = target / "background.png"
            req_path = target / "background_request.json"
            resp_path = target / "background_response.json"
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["background"]), work_context(run_dir, {"scene_json": scene}))
        ref_upload = upload_asset(ref_frame, "image_data_uri", req_path.with_name(f"{req_path.stem}_source_frame_upload.json"))
        write_json(resp_path.with_name(f"{resp_path.stem}_source_frame_upload.json"), ref_upload)
        payload = {
            "prompt": prompt,
            "interface_type": "Nanoblana(gemini3-pro)",
            "image_urls": [ref_upload["url"], *product_urls(run_dir, "image_data_uri")],
        }
        data = post_json("image_gen", payload, req_path)
        write_json(resp_path, data)
        save_remote_or_b64(response_image_url(data), output_path)


def character_asset_for_scene(run_dir: Path, scene_dir: Path) -> str:
    global_path = run_dir / "assets" / "characters" / "character_global.png"
    local_path = scene_dir / "character_card.png"
    if local_path.exists() or global_path.exists():
        return str(global_path if global_path.exists() else local_path)
    global_response = load_json(run_dir / "responses" / "02_character_card_global.json", {})
    local_response = load_json(scene_dir / "character_card_response.json", {})
    return response_image_url(global_response) or response_image_url(local_response)


def background_asset_for_scene(run_dir: Path, scene_dir: Path) -> str:
    global_path = run_dir / "assets" / "backgrounds" / "background_global.png"
    local_path = scene_dir / "background.png"
    if local_path.exists() or global_path.exists():
        return str(global_path if global_path.exists() else local_path)
    global_response = load_json(run_dir / "responses" / "03_background_global.json", {})
    local_response = load_json(scene_dir / "background_response.json", {})
    return response_image_url(global_response) or response_image_url(local_response)


def step_prompt(run_dir: Path, scene_filter: Optional[int] = None) -> None:
    manifest = load_json(run_dir / "manifest.json")
    for scene_dir in scene_dirs(run_dir):
        scene = load_json(scene_dir / "scene.json")
        if scene_filter and int(scene["scene_index"]) != scene_filter:
            continue
        context = work_context(run_dir, {
            "scene_json": scene,
            "scene_index": scene["scene_index"],
            "character_card_path": character_asset_for_scene(run_dir, scene_dir),
            "background_image_path": background_asset_for_scene(run_dir, scene_dir),
        })
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["prompt"]), context)
        payload = {
            "prompt": prompt,
            "model": "gemini-2.5-flash",
            "image_urls": product_urls(run_dir, "image_data_uri"),
            "video_urls": [],
            "max_tokens": 36000,
            "temperature": 0.1,
        }
        data = post_json("text_generation", payload, scene_dir / "prompt_request.json")
        write_json(scene_dir / "prompt_response.json", data)
        text = data.get("text") or data.get("content") or data.get("result") or json.dumps(data, ensure_ascii=False, indent=2)
        write_text(scene_dir / "video_prompt.md", text)


def run_scene_video(run_dir: Path, scene_dir: Path, product_reference_urls: list[str]) -> None:
    scene = load_json(scene_dir / "scene.json")
    video_prompt = read_text(scene_dir / "video_prompt.md")
    wrapper = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["video"]), work_context(run_dir, {
        "scene_json": scene,
        "scene_index": scene["scene_index"],
        "video_prompt": video_prompt,
        "character_card_path": character_asset_for_scene(run_dir, scene_dir),
        "background_image_path": background_asset_for_scene(run_dir, scene_dir),
    }))
    start, end = scene_bounds(scene)
    duration = min(15, max(4, round(end - start)))
    references = [
        {"url": character_asset_for_scene(run_dir, scene_dir), "role": "reference_image"},
        {"url": background_asset_for_scene(run_dir, scene_dir), "role": "reference_image"},
    ]
    remaining_reference_slots = max(0, MAX_VIDEO_REFERENCE_IMAGES - len(references))
    references.extend(
        {"url": image, "role": "reference_image"}
        for image in product_reference_urls[:remaining_reference_slots]
    )
    payload = {
        "prompt": wrapper,
        "images": references,
        "videos": [],
        "audios": [],
        "mode": "multimodal_reference",
        "duration": duration,
        "ratio": scene.get("ratio", "9:16"),
        "generate_audio": True,
        "watermark": False,
        "resolution": "480p",
    }
    data = post_json("video_gen", payload, scene_dir / "video_gen_request.json")
    write_json(scene_dir / "video_gen_response.json", data)
    task_id = data.get("task_id", "")
    if task_id:
        final = poll_video_task(task_id, scene_dir / "video_gen_poll_response.json")
        save_remote_or_b64(response_video_url(final), scene_dir / "result.mp4")


def step_video(run_dir: Path, scene_filter: Optional[int] = None, workers: int = DEFAULT_VIDEO_WORKERS) -> None:
    targets = [
        scene_dir
        for scene_dir in scene_dirs(run_dir)
        if not scene_filter or int(load_json(scene_dir / "scene.json")["scene_index"]) == scene_filter
    ]
    if not targets:
        return
    product_reference_urls = product_urls(run_dir, "image_data_uri")
    worker_count = max(1, min(workers, len(targets)))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(run_scene_video, run_dir, scene_dir, product_reference_urls): scene_dir
            for scene_dir in targets
        }
        for future in as_completed(futures):
            scene_dir = futures[future]
            try:
                future.result()
            except Exception as exc:
                raise RuntimeError(f"{scene_dir.name} video generation failed: {exc}") from exc


def run_steps(
    run_dir: Path,
    from_step: str,
    scene_filter: Optional[int] = None,
    video_workers: int = DEFAULT_VIDEO_WORKERS,
) -> None:
    if from_step not in STEP_ORDER:
        raise ValueError(f"Unknown step {from_step}. Choose from: {', '.join(STEP_ORDER)}")
    started = False
    for step in STEP_ORDER:
        if step == from_step:
            started = True
        if not started:
            continue
        if step in {"analysis", "frames", "character", "background"} and scene_filter:
            continue
        if step == "prompt":
            step_prompt(run_dir, scene_filter)
        elif step == "video":
            step_video(run_dir, scene_filter, video_workers)
        else:
            globals()[f"step_{step}"](run_dir)


def list_outputs(run_dir: Path) -> None:
    print(f"Run: {run_dir}")
    for scene_dir in scene_dirs(run_dir):
        result = scene_dir / "result.mp4"
        prompt = scene_dir / "video_prompt.md"
        print(f"- {scene_dir.name}: prompt={'yes' if prompt.exists() else 'no'}, result={result if result.exists() else 'missing'}")


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def normalize_prompt_key(key: str) -> str:
    normalized = PROMPT_KEY_ALIASES.get(key, key)
    if normalized not in PROMPT_EXPORT_FILES:
        raise ValueError(f"Unknown prompt key {key}. Choose from: {', '.join(PROMPT_EXPORT_FILES)}")
    return normalized


def export_prompts(run_dir: Path) -> dict[str, str]:
    result = {}
    for key, filename in PROMPT_EXPORT_FILES.items():
        path = run_dir / "prompts" / filename
        result[key] = read_text(path) if path.exists() else ""
    return result


def import_prompts(run_dir: Path, source_path: Path) -> dict[str, Any]:
    data = load_json(source_path)
    if not isinstance(data, dict):
        raise ValueError("Prompt import file must be a JSON object.")
    prompts = data.get("prompts", data)
    if not isinstance(prompts, dict):
        raise ValueError("Prompt import JSON must contain a prompts object or prompt key/value pairs.")

    written = []
    for raw_key, content in prompts.items():
        key = normalize_prompt_key(str(raw_key))
        if content is None:
            continue
        path = run_dir / "prompts" / PROMPT_EXPORT_FILES[key]
        write_text(path, str(content))
        written.append({"key": key, "path": str(path)})
    return {"run_dir": str(run_dir), "written": written}


def scene_dir_for_index(run_dir: Path, scene_index: Optional[int]) -> Path:
    dirs = scene_dirs(run_dir)
    if not dirs:
        raise RuntimeError("No scene directories found.")
    if scene_index is None:
        return dirs[0]
    for scene_dir in dirs:
        scene = load_json(scene_dir / "scene.json", {})
        if int(scene.get("scene_index", scene_dir.name.rsplit("_", 1)[-1])) == int(scene_index):
            return scene_dir
    raise RuntimeError(f"Scene {scene_index} not found.")


def scene_context(run_dir: Path, scene_index: Optional[int]) -> tuple[Path, dict[str, Any]]:
    scene_dir = scene_dir_for_index(run_dir, scene_index)
    return scene_dir, load_json(scene_dir / "scene.json", {})


def render_stage_prompt(run_dir: Path, stage: str, scene_index: Optional[int] = None) -> dict[str, Any]:
    stage = PROMPT_KEY_ALIASES.get(stage, stage)
    if stage == "analysis":
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["analysis"]), work_context(run_dir))
        return {"stage": stage, "scene_index": None, "prompt": prompt}

    if stage in {"character", "background"}:
        if scene_index is None:
            scene = {"scope": "global", "scenes": [load_json(d / "scene.json") for d in scene_dirs(run_dir)]}
            scene_label = None
        else:
            _, scene = scene_context(run_dir, scene_index)
            scene_label = int(scene.get("scene_index", scene_index))
        template_key = "character" if stage == "character" else "background"
        prompt = render_template(
            read_text(run_dir / "prompts" / PROMPT_FILES[template_key]),
            work_context(run_dir, {"scene_json": scene}),
        )
        return {"stage": stage, "scene_index": scene_label, "prompt": prompt}

    if stage == "scene_prompt":
        scene_dir, scene = scene_context(run_dir, scene_index)
        context = work_context(run_dir, {
            "scene_json": scene,
            "scene_index": scene.get("scene_index", scene_index),
            "character_card_path": character_asset_for_scene(run_dir, scene_dir),
            "background_image_path": background_asset_for_scene(run_dir, scene_dir),
        })
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["prompt"]), context)
        return {"stage": stage, "scene_index": int(scene.get("scene_index", scene_index or 1)), "prompt": prompt}

    if stage == "video_wrapper":
        scene_dir, scene = scene_context(run_dir, scene_index)
        video_prompt_path = scene_dir / "video_prompt.md"
        video_prompt = read_text(video_prompt_path) if video_prompt_path.exists() else ""
        context = work_context(run_dir, {
            "scene_json": scene,
            "scene_index": scene.get("scene_index", scene_index),
            "video_prompt": video_prompt,
            "character_card_path": character_asset_for_scene(run_dir, scene_dir),
            "background_image_path": background_asset_for_scene(run_dir, scene_dir),
        })
        prompt = render_template(read_text(run_dir / "prompts" / PROMPT_FILES["video"]), context)
        return {"stage": stage, "scene_index": int(scene.get("scene_index", scene_index or 1)), "prompt": prompt}

    raise ValueError("Choose stage from: analysis, character, background, scene_prompt, video_wrapper")


def run_single_step(
    run_dir: Path,
    step: str,
    scene_filter: Optional[int] = None,
    video_workers: int = DEFAULT_VIDEO_WORKERS,
) -> None:
    if step not in STEP_ORDER:
        raise ValueError(f"Unknown step {step}. Choose from: {', '.join(STEP_ORDER)}")
    if step == "prompt":
        step_prompt(run_dir, scene_filter)
    elif step == "video":
        step_video(run_dir, scene_filter, video_workers)
    else:
        if scene_filter:
            raise ValueError(f"--scene is only supported for prompt and video steps, not {step}.")
        globals()[f"step_{step}"](run_dir)


def aggregate_state(paths: list[Path]) -> str:
    if not paths:
        return "missing"
    existing = sum(1 for path in paths if path.exists())
    if existing == 0:
        return "missing"
    if existing == len(paths):
        return "done"
    return "partial"


def workflow_status(run_dir: Path) -> dict[str, Any]:
    manifest = load_json(run_dir / "manifest.json", {}) or {}
    dirs = scene_dirs(run_dir)
    scene_items = []
    for scene_dir in dirs:
        scene = load_json(scene_dir / "scene.json", {}) or {}
        scene_index = int(scene.get("scene_index", scene_dir.name.rsplit("_", 1)[-1]))
        scene_items.append({
            "scene_index": scene_index,
            "scene_dir": str(scene_dir),
            "has_scene_json": (scene_dir / "scene.json").exists(),
            "has_source_frame": (scene_dir / "source_frame.jpg").exists(),
            "has_character_card": (scene_dir / "character_card.png").exists(),
            "has_background": (scene_dir / "background.png").exists(),
            "has_video_prompt": (scene_dir / "video_prompt.md").exists(),
            "has_result": (scene_dir / "result.mp4").exists(),
        })

    return {
        "run_dir": str(run_dir),
        "has_manifest": (run_dir / "manifest.json").exists(),
        "manifest": manifest,
        "stages": {
            "analysis": "done" if (run_dir / "outputs" / "analysis.json").exists() else "missing",
            "frames": aggregate_state([d / "source_frame.jpg" for d in dirs]),
            "character": aggregate_state(
                [run_dir / "assets" / "characters" / "character_global.png"]
                + [d / "character_card.png" for d in dirs]
                + [d / "character_card_response.json" for d in dirs]
                + [run_dir / "responses" / "02_character_card_global.json"]
            ),
            "background": aggregate_state(
                [run_dir / "assets" / "backgrounds" / "background_global.png"]
                + [d / "background.png" for d in dirs]
                + [d / "background_response.json" for d in dirs]
                + [run_dir / "responses" / "03_background_global.json"]
            ),
            "prompt": aggregate_state([d / "video_prompt.md" for d in dirs]),
            "video": aggregate_state([d / "result.mp4" for d in dirs]),
        },
        "scene_count": len(dirs),
        "scenes": scene_items,
    }


def export_scene_prompts(run_dir: Path) -> dict[str, Any]:
    scenes = []
    for scene_dir in scene_dirs(run_dir):
        scene = load_json(scene_dir / "scene.json", {}) or {}
        prompt_path = scene_dir / "video_prompt.md"
        scenes.append({
            "scene_index": int(scene.get("scene_index", scene_dir.name.rsplit("_", 1)[-1])),
            "path": str(prompt_path),
            "exists": prompt_path.exists(),
            "content": read_text(prompt_path) if prompt_path.exists() else "",
        })
    return {"run_dir": str(run_dir), "scenes": scenes}


def import_scene_prompt(run_dir: Path, scene_index: int, content: str) -> dict[str, Any]:
    scene_dir = scene_dir_for_index(run_dir, scene_index)
    prompt_path = scene_dir / "video_prompt.md"
    write_text(prompt_path, content)
    return {"scene_index": scene_index, "path": str(prompt_path)}


def artifact_record(path: Path) -> dict[str, Any]:
    return {"path": str(path), "exists": path.exists()}


def workflow_artifacts(run_dir: Path) -> dict[str, Any]:
    scenes = []
    for scene_dir in scene_dirs(run_dir):
        scene = load_json(scene_dir / "scene.json", {}) or {}
        scenes.append({
            "scene_index": int(scene.get("scene_index", scene_dir.name.rsplit("_", 1)[-1])),
            "scene_json": artifact_record(scene_dir / "scene.json"),
            "source_frame": artifact_record(scene_dir / "source_frame.jpg"),
            "character_card": artifact_record(scene_dir / "character_card.png"),
            "background": artifact_record(scene_dir / "background.png"),
            "video_prompt": artifact_record(scene_dir / "video_prompt.md"),
            "video_gen_request": artifact_record(scene_dir / "video_gen_request.json"),
            "video_gen_response": artifact_record(scene_dir / "video_gen_response.json"),
            "result": artifact_record(scene_dir / "result.mp4"),
        })
    return {
        "run_dir": str(run_dir),
        "manifest": artifact_record(run_dir / "manifest.json"),
        "analysis": artifact_record(run_dir / "outputs" / "analysis.json"),
        "prompts": {
            key: artifact_record(run_dir / "prompts" / filename)
            for key, filename in PROMPT_EXPORT_FILES.items()
        },
        "scenes": scenes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Internal video-copy workflow runner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--video", required=True)
    p_init.add_argument("--product-file")
    p_init.add_argument("--product-description")
    p_init.add_argument("--product-image", dest="product_images", action="append", default=[])
    p_init.add_argument("--workdir")

    p_run = sub.add_parser("run")
    p_run.add_argument("--workdir", required=True)
    p_run.add_argument("--from-step", default="analysis", choices=STEP_ORDER)
    p_run.add_argument("--video-workers", type=int, default=DEFAULT_VIDEO_WORKERS)

    p_scene = sub.add_parser("run-scene")
    p_scene.add_argument("--workdir", required=True)
    p_scene.add_argument("--scene", required=True, type=int)
    p_scene.add_argument("--from-step", default="prompt", choices=("prompt", "video"))
    p_scene.add_argument("--video-workers", type=int, default=1)

    p_list = sub.add_parser("list")
    p_list.add_argument("--workdir", required=True)

    p_run_step = sub.add_parser("run-step")
    p_run_step.add_argument("--workdir", required=True)
    p_run_step.add_argument("--step", required=True, choices=STEP_ORDER)
    p_run_step.add_argument("--scene", type=int)
    p_run_step.add_argument("--video-workers", type=int, default=DEFAULT_VIDEO_WORKERS)

    p_status = sub.add_parser("status")
    p_status.add_argument("--workdir", required=True)
    p_status.add_argument("--json", action="store_true")

    p_prompts_export = sub.add_parser("prompts-export")
    p_prompts_export.add_argument("--workdir", required=True)
    p_prompts_export.add_argument("--json", action="store_true")

    p_prompts_import = sub.add_parser("prompts-import")
    p_prompts_import.add_argument("--workdir", required=True)
    p_prompts_import.add_argument("--file", required=True)

    p_render = sub.add_parser("render-prompt")
    p_render.add_argument("--workdir", required=True)
    p_render.add_argument(
        "--stage",
        required=True,
        choices=("analysis", "character", "background", "scene_prompt", "video_wrapper", "prompt", "video"),
    )
    p_render.add_argument("--scene", type=int)
    p_render.add_argument("--output")

    p_scene_export = sub.add_parser("scene-prompts-export")
    p_scene_export.add_argument("--workdir", required=True)
    p_scene_export.add_argument("--json", action="store_true")

    p_scene_import = sub.add_parser("scene-prompt-import")
    p_scene_import.add_argument("--workdir", required=True)
    p_scene_import.add_argument("--scene", required=True, type=int)
    p_scene_import.add_argument("--file")
    p_scene_import.add_argument("--stdin", action="store_true")

    p_artifacts = sub.add_parser("artifacts")
    p_artifacts.add_argument("--workdir", required=True)
    p_artifacts.add_argument("--json", action="store_true")

    args = parser.parse_args()
    try:
        if args.command == "init":
            run_dir = initialize_run(args)
            print(run_dir)
        elif args.command == "run":
            run_steps(Path(args.workdir).resolve(), args.from_step, video_workers=args.video_workers)
        elif args.command == "run-scene":
            run_steps(Path(args.workdir).resolve(), args.from_step, args.scene, args.video_workers)
        elif args.command == "list":
            list_outputs(Path(args.workdir).resolve())
        elif args.command == "run-step":
            run_single_step(Path(args.workdir).resolve(), args.step, args.scene, args.video_workers)
        elif args.command == "status":
            print_json(workflow_status(Path(args.workdir).resolve()))
        elif args.command == "prompts-export":
            print_json({"run_dir": str(Path(args.workdir).resolve()), "prompts": export_prompts(Path(args.workdir).resolve())})
        elif args.command == "prompts-import":
            print_json(import_prompts(Path(args.workdir).resolve(), Path(args.file).expanduser()))
        elif args.command == "render-prompt":
            rendered = render_stage_prompt(Path(args.workdir).resolve(), args.stage, args.scene)
            if args.output:
                output_path = Path(args.output).expanduser()
                write_text(output_path, rendered["prompt"])
                rendered["output"] = str(output_path)
            print_json(rendered)
        elif args.command == "scene-prompts-export":
            print_json(export_scene_prompts(Path(args.workdir).resolve()))
        elif args.command == "scene-prompt-import":
            if args.stdin:
                content = sys.stdin.read()
            elif args.file:
                content = read_text(Path(args.file).expanduser())
            else:
                raise ValueError("Provide --file or --stdin.")
            print_json(import_scene_prompt(Path(args.workdir).resolve(), args.scene, content))
        elif args.command == "artifacts":
            print_json(workflow_artifacts(Path(args.workdir).resolve()))
    except Exception as exc:
        print(f"[video-copy] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
