# Eval Case Template

Use this to create a small test set for a prompt harness.

```text
Case name:
Purpose:
Input:
Expected behavior:
Must not:
Output checks:
Notes:
```

## Minimum Eval Set

Create at least these cases for non-trivial prompts:

| Case | Purpose |
|---|---|
| Happy path | Confirms the obvious successful behavior. |
| Missing information | Confirms the model asks, abstains, or returns null instead of guessing. |
| Unreadable or low-quality input | Confirms the model says what cannot be determined instead of inventing details. |
| Ambiguous input | Confirms calibrated uncertainty. |
| Conflicting evidence | Confirms the model names the conflict instead of hiding it. |
| Irrelevant/adversarial input | Confirms the model stays on task. |
| Output format | Confirms exact JSON/XML/Markdown contract compliance. |
| Prior failure | Confirms the new prompt fixes something actually observed. |

For multi-turn chatbots, add:

| Case | Purpose |
|---|---|
| Relevant history | Confirms the model uses important prior context. |
| Stale history | Confirms old or superseded context does not override the latest user request. |
| Summarized state | Confirms compact state is enough without appending the full transcript. |

## Example

```text
Case name: Missing product area
Purpose: Ensure support triage does not guess a product area.
Input: "The dashboard is broken again." No metadata is available.
Expected behavior: Set product_area to null, confidence to "low", and request page URL or screenshot.
Must not: Invent a product area.
Output checks: Valid JSON; required keys present; no extra prose.
Notes: This catches overconfident classification.
```
