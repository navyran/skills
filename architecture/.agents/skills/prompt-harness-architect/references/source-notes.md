# Source Notes

This skill is original synthesis. It was initially inspired by an Anthropic prompting 101 transcript about building a prompt iteratively for a multimodal review workflow.

Do not redistribute the raw transcript unless the license clearly allows it. Public repo content should use paraphrase, attribution, and independent examples.

## Distilled Principles

- Prompt engineering is iterative and empirical.
- Start with task context and role.
- Set factual, confidence-calibrated tone so the model does not guess when evidence is unclear.
- Separate stable context from dynamic input.
- Put durable context in system or developer instructions when available, while passing changing content separately.
- Describe stable artifact structure, purpose, interpretation rules, and likely human-input quirks before asking the model to interpret filled-in data.
- Structure prompt sections clearly with semantic labels.
- Tell the model what order to inspect evidence, especially when one source is more structured than another.
- Tell the model to abstain when input is unreadable or too low-quality to support a claim.
- Use structured, multimodal, or human-labeled examples for hard or ambiguous cases; attach or encode visual inputs in the runtime-supported format.
- For user-facing chatbots, include relevant conversation history or summaries as context.
- Repeat critical constraints near the end, then tell the model to perform the task.
- Specify the final output format.
- Decide how much intermediate analysis should be visible to the user or downstream system.
- Use response prefill when a runtime supports it.
- Test with deterministic settings and enough output budget while debugging prompt behavior.
- Use reasoning traces or prior model outputs to diagnose missing instructions, then encode the fix in the prompt harness.

## Originality Guidance

Strengthen this skill with:

- Public prompting docs from multiple providers.
- Personal production lessons from shipped AI apps.
- Non-insurance examples such as support triage, document extraction, research review, internal tooling, and structured data cleanup.
- Eval cases that show how the workflow behaves, not just how it is described.
