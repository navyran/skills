---
name: video-copy
description: Use this internal skill to copy a promotional video for a new product by calling the remote video_analysis, image_gen, text_generation, and video_gen APIs. Use when a PM or operator provides a source promo video plus new product description/images and wants editable prompt templates, saved requests/responses, generated character/background assets, and separate scene-level result clips.
---

# Video Copy

## Purpose

Run the internal video-copy pipeline for PM prompt iteration. The source video is analyzed, reusable or scene-level assets are generated, scene prompts are written, and each scene is generated as a separate video clip.

The API base URL/key are internal skill configuration. Do not ask the user for API credentials. The runner defaults to the deployed internal API at `http://121.36.14.67:5176` with a built-in bearer key; override with `VIDEO_COPY_API_BASE_URL` / `VIDEO_COPY_API_KEY` only when testing a different internal deployment.

## Inputs

Required user inputs:

- Source promo video file.
- Product description, either a Markdown/text file or plain text.
- One or more product images, either files or a directory. The runner uses at most 5 product images, in sorted input order, to keep Seedance references focused.

No prompt input is required before the first run. Default prompts are copied into the run folder and can be edited later.

## First Run

Use the runner script:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py init \
  --video ./source.mp4 \
  --product-file ./product.md \
  --product-image ./product_images
```

The command prints the run directory. Then run:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py run \
  --workdir ./video-copy-YYYYMMDD-HHMMSS
```

Scene video generation runs in parallel by default with 3 workers. Adjust it when needed:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py run \
  --workdir ./video-copy-YYYYMMDD-HHMMSS \
  --from-step video \
  --video-workers 5
```

If this skill is being used from a copied workspace package instead of an installed skill, use that package's `scripts/video_copy.py` path.

## Run Folder

Each run stores all inputs and outputs under the current working directory:

```text
video-copy-YYYYMMDD-HHMMSS/
├── inputs/
├── product/
│   ├── product.md
│   └── images/
├── prompts/
├── requests/
├── responses/
├── outputs/
├── assets/
│   ├── characters/
│   └── backgrounds/
├── scenes/
│   └── scene_001/
│       ├── scene.json
│       ├── source_frame.jpg
│       ├── character_card.png
│       ├── background.png
│       ├── video_prompt.md
│       ├── video_gen_request.json
│       ├── video_gen_response.json
│       └── result.mp4
└── manifest.json
```

Every API request and response is saved. Every editable prompt is in `prompts/`.

## Workflow

1. `analysis`: call `POST /v1/video-analyses` with `prompts/01_video_analysis.md`.
2. `frames`: extract representative midpoint frames for each analyzed scene.
3. `character`: call `POST /v1/files` and `POST /v1/images` for global or per-scene character cards based on `analysis.asset_plan.character_generation.scope`.
4. `background`: call `POST /v1/files` and `POST /v1/images` for global or per-scene backgrounds based on `analysis.asset_plan.background_generation.scope`.
5. `prompt`: call `POST /v1/text-generations` to create `scene_*/video_prompt.md`.
6. `video`: call `POST /v1/video-generations`, then poll `GET /v1/video-generations/{task_id}` to create separate scene clips. Scenes are submitted and polled in parallel unless `--video-workers 1` is used.

The analysis prompt asks for `asset_plan`, `characters`, `backgrounds`, and scene timing fields. If the API response omits asset scope, the runner falls back to per-scene generation.

## PM Prompt Iteration

To improve results, edit files in `prompts/`, then rerun from the affected step:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py run \
  --workdir ./video-copy-YYYYMMDD-HHMMSS \
  --from-step background
```

For one scene only:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py run-scene \
  --workdir ./video-copy-YYYYMMDD-HHMMSS \
  --scene 3 \
  --from-step prompt
```

Valid full-run `--from-step` values:

```text
analysis, frames, character, background, prompt, video
```

Valid scene-only `--from-step` values:

```text
prompt, video
```

## Output Review

List scene outputs:

```bash
python ~/.codex/skills/video-copy/scripts/video_copy.py list \
  --workdir ./video-copy-YYYYMMDD-HHMMSS
```

Final clips are saved as:

```text
scenes/scene_001/result.mp4
scenes/scene_002/result.mp4
...
```

## Implementation Notes

- The runner keeps internal API configuration in `scripts/video_copy.py`.
- Patch only `INTERNAL_API_BASE_URL`, `INTERNAL_API_KEY`, and `ENDPOINTS` if the internal deployment URL or route contract changes.
- The runner sends local files through `/v1/files` multipart upload and stores sanitized request records.
- At most 5 product images are passed to prompt generation and video generation.
- Seedance prompts use Chinese defaults and follow the documented multimodal-reference pattern: explicit image order binding, subject/action/environment/camera/style/quality/constraint structure, storyboard order for complex scenes, and one main camera movement per shot.
- `/v1/images` currently returns a server-side output path. The runner records that path and passes it back to `/v1/video-generations`; generated image binaries may not be downloadable into the local run folder unless the API later returns a URL or data URI.
