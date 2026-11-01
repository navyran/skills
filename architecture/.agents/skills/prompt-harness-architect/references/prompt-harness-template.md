# Prompt Harness Template

Use this when creating a new prompt harness or rewriting a rough prompt into production form.

## Compact Template

```text
<task_context>
You are helping [user/persona/team] with [task].
The goal is [success condition].
Do not [forbidden behavior].
Stay factual, calibrate confidence, and do not guess when evidence is unclear.
</task_context>

<stable_reference>
[Schemas, policies, rubrics, examples, product rules, domain definitions, artifact structure or layout, artifact purpose, interpretation rules, field meanings, input quirks.]
</stable_reference>

<dynamic_input>
[User request, document, retrieved context, images or image descriptions, tool result, current conversation state.]
</dynamic_input>

<procedure>
1. Read the stable reference.
2. Inspect the most structured or reliable input first.
3. Inspect ambiguous, freeform, or visual material using that context.
4. Compare facts against the rubric or task criteria.
5. Identify uncertainty, missing information, unreadable inputs, or contradictions.
6. Decide which intermediate findings should be visible.
7. Produce the final answer in the requested format.
</procedure>

<examples>
[Few-shot examples with input, expected output, and brief rationale. Include multimodal or human-labeled examples when useful; attach or encode visual inputs in the runtime-supported format.]
</examples>

<uncertainty_policy>
If the evidence is insufficient, say what cannot be determined.
Do not invent facts or infer beyond the available evidence.
Escalate to a human when the task is high-stakes or ambiguous.
</uncertainty_policy>

<output_format>
[Markdown, JSON schema, XML tags, or mixed human + structured output.]
[Say whether to include concise intermediate findings or only the final structured block.]
</output_format>

<final_reminders>
Use only provided evidence.
Follow the output format exactly.
Keep the final answer concise.
Now perform the task.
</final_reminders>
```

## JSON Output Contract Checklist

When the output must be JSON, specify:

- Required keys.
- Allowed enum values.
- Type of each field.
- Whether null is allowed.
- What to do with unknown or missing values.
- Whether extra keys are forbidden.
- Whether the runtime should prefill `{` or `[` when supported.
- Whether visible intermediate analysis is allowed before the JSON.

## Example Domain: Support Triage

Use a non-insurance example to avoid copying the source transcript's running case.

```text
Task: Classify a support ticket.
Stable context: severity rubric, product area list, escalation rules.
Dynamic input: customer ticket text, account tier, recent incidents, screenshots or attachments.
Procedure: extract facts, map to severity, decide escalation, produce JSON.
Uncertainty policy: if severity depends on unavailable logs, set confidence to "low" and request the missing log.
```
