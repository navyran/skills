---
name: prompt-harness-architect
description: Design system prompts for app or website chatbots, multimodal document/image review, and production LLM harnesses; use for context structure, response prefill, conversation history, uncertainty rules, and evals.
---

# Prompt Harness Architect

Use this skill to design prompts as production harnesses, not one-off chatbot messages. Keep the output practical: a revised prompt or harness, a short rationale, and eval cases when the task has real behavioral risk.

## Workflow

### 1. Contract

Define the task before writing the prompt:

- Who the model helps.
- What job the model must do.
- What it must not do.
- What success looks like.
- Whether the answer is for a human, an API, a database, or another agent.
- What uncertainty behavior is required.

Set the epistemic tone explicitly: stay factual, calibrate confidence, and do not guess when the evidence is unclear.

For high-stakes or ambiguous tasks, explicitly tell the model when to refuse, ask for missing information, escalate to a human, or say it cannot determine the answer.

### 2. Structure

Separate the prompt into stable context, dynamic input, runtime controls, and output requirements.

Stable context includes schemas, policies, rubrics, examples, product rules, domain definitions, artifact structure or layout, artifact purpose, interpretation rules, expected languages, field meanings, and human-input quirks such as circles, scribbles, partial marks, or imperfect handwriting. It is usually the best candidate for prompt caching when the runtime supports caching.

Dynamic input includes the user's request, current document, retrieved snippets, images, current tool results, and conversation state.

When the runtime supports separate messages, put durable context in system or developer instructions and pass changing content as user or runtime input.

Use labeled sections with Markdown headings or semantic XML-style tags that say what is inside. Prefer one clear structure over clever prose.

For a fill-in scaffold, read `references/prompt-harness-template.md`.

### 3. Steer

Add only the steering the task actually needs:

- Procedure order: tell the model what to inspect first, compare second, and conclude last. For multiple evidence sources, inspect the structured or reliable source before ambiguous freeform material, then reconcile them.
- Evidence rules: require factual claims to be grounded in provided input when useful.
- Examples: add few-shot, structured, multimodal, or human-labeled examples for hard, ambiguous, or repeatedly failing cases. When visual examples matter, attach or encode them in the format the runtime supports.
- Conversation state: for chatbots, include relevant recent turns, user preferences, summarized state, and important tool results in the harness context. Do not blindly append the full conversation forever.
- Final reminders: restate the few constraints that matter most near the end, then tell the model to perform the task.

### 4. Format

Choose the output shape based on the consumer:

- Human reader: concise prose or Markdown.
- API/database: strict JSON schema.
- XML parser: tagged final block.
- Mixed use: short human summary plus a strict structured block.

If the runtime supports response prefill, use it as a separate lever from output instructions: `{` for JSON objects, `[` for JSON arrays, or a tag such as `<final_verdict>` when the application only needs a final block.

Decide what intermediate analysis belongs in the visible answer. Detailed inspection can improve accuracy, but the final output may need only concise findings or a structured verdict.

For runtime-specific capability notes, read `references/harness-runtime-notes.md`.

### 5. Evaluate

Create eval cases before calling the prompt good:

- Happy path.
- Ambiguous input.
- Missing information.
- Unreadable or low-quality input.
- Conflicting evidence.
- Irrelevant or adversarial input.
- Output-format compliance.
- Conversation-history or stale-context case for chatbots.
- Known prior failures.

Iterate empirically: run a simple prompt, inspect the concrete failure, add the missing context, order, examples, or output controls, rerun, and turn the failure into an eval case.

When reasoning traces, extended thinking, scratchpads, logs, or prior model outputs are available, use them as diagnostic material. Find where the model misunderstood, skipped evidence, guessed, or used the wrong order; then convert that observation into clearer instructions, examples, references, or eval cases. Do not expose hidden reasoning to end users.

For an eval template, read `references/eval-case-template.md`.

## Expected Output

When improving a prompt, usually return:

1. A short diagnosis of the current prompt.
2. A revised prompt or harness.
3. Key design choices, briefly.
4. Eval cases for the revised harness.
5. Any unresolved ambiguity or missing domain context.

For small prompt edits, skip the long explanation and provide the revised prompt directly.

## Source Notes

This skill is original synthesis inspired by public prompting guidance and production prompt-harness patterns. For provenance and attribution guidance, read `references/source-notes.md`.
