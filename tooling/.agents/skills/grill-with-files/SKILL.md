---
name: grill-with-files
description: Stress-test a plan against the files it touches — open the workbooks, data, PDFs, and folder, and resolve every question the files can answer by looking instead of asking. Use when you're about to do real work in your filing system (reorganizing files, building or editing a workbook, extracting from PDFs, transforming data) and want the plan interrogated against what's on disk before you start. Triggers — "grill me on this before I start", "poke holes in my approach to this workbook/folder", "stress-test this plan against what's in the files", "interrogate this against the folder", grill-with-files. Prefer over plain grill-me whenever the plan touches files Claude can open; prefer /folder-explore or /workbook-explore (or the audit skills) when you want the files inspected or reported on rather than a plan interrogated.
---

A plan interrogation that works from your words alone has to ask you about everything. But when the plan is about work in your filing system, half the answers are already on disk: the workbook knows its own sheet names, the folder knows its own naming rule, a recording's transcript knows what was said. So the one rule that drives this skill:

> **If the files can answer it, look — don't ask.** Spend your questions only on what the files can't settle: your intent, your judgment calls, and decisions not yet made.

## Run a grilling session

Run a `/grilling` session to interrogate the plan. What makes it *file-grounded*: you've read the files first (below), so each recommended answer **cites what backs it** — *"pull from the master timeline — the rules doc names it the source of truth"* — instead of guessing.

## Read before you ask

Do a **light recon first** so the opening question lands on something real, then open more as specific questions demand — skim structure, don't ingest everything. List the folder (naming patterns, version-y duplicates, subfolders); for a workbook, note its sheets, where tables start, and whether it carries an Instructions / Agent / Audit Log sheet; for data, the headers and row count; for a PDF or recording, whether it's real text/a transcript or a scan — then read only the part that matters.

Prioritize the layer that says **how to work here** — it's where plans live or die. In a light setup that's a README and the folder's naming convention. In a mature one it's a cluster: a rules/agent doc ("never overwrite the originals"), naming and routing conventions (which kind of file belongs where), task SOPs, an inventory of what's present vs. missing, and a session log of prior decisions ("we deleted that — don't recreate it"; "this file's facts are stale"). In a workbook that same layer lives in its sheets — an **Instructions sheet** (how it works), an **Agent sheet** (conventions, gotchas, DO-NOT-EDITs, open decisions), and the **Audit Log** (the session log: what prior tasks decided, retired, or flagged stale). A plan that contradicts any of these is already broken; it just doesn't know yet. These aren't universal — don't assume them — but when they exist, read them first.

## Grill with what you find

Turn what you read into pressure on the plan:

- **Conflict with a convention or a logged decision** — surface it, make me reconcile. *"Everything here is date-prefixed `YYYY-MM-DD`; your plan emits `report_final` — break the rule or rename?"* *"The session log retired that sheet as the source of truth — why is the plan still keying off it?"*
- **Fuzzy file or scope reference** — pin it to reality. *"'The Q3 file' — there are three; `Q3 FINAL v2.xlsx` is newest. That one?"* *"'Clean up the folder' — this level only, or recursively into the subfolders?"*
- **Edge case the files will actually throw** — invent the specific one. *"This download may be a re-export of something already filed — dedupe-check first, or assume it's new?"* *"The PDF is scanned, not text — OCR it, or does the plan silently extract nothing?"* *"That Velixo pull may have silently returned blank or stale — refresh-and-check first, or build on whatever's cached?"*
- **Claim vs. contents** — when I assert how something works, check the file and surface the gap. *"You said totals are row 50; row 50 is blank and 47 holds the total — which drives the formula?"*
- **A number with nothing to reconcile against** — make me name what it ties out to. *"This roll-up feeds the board deck — what control total must it match, and where does that total live?"*

## Finish with a grounded brief

You **read, you don't edit** — getting the plan right *before* any work is the whole point; acting on it is downstream. When we reach shared understanding, write a tight brief and stop:

```
## Grounded plan brief
Goal: <one line>
Resolved: <each decision + the file/convention that grounds it>
Assumptions: <inferred from the files; confirm>
Open / blocked: <what the files couldn't settle>
Scope: <what this won't touch>
```

It's shaped to drop into a planning flow — the decisions feed the steps, "Open" becomes open questions, "Scope" becomes out-of-scope. So **offer the handoff; don't take it**: *"Hand this to /folder-plan or /workbook-plan, save it as a note in the folder, or leave it here?"* Default to leaving it in chat.

One exception leads with a different destination: **when the interrogation surfaced a multi-session feature** — many units, spanning sessions, the kind of thing that wants a spec and independent tickets — lead the offer with handing the brief to `/to-spec` **now, in this window**. `/to-spec` never interviews; the grilling that just happened *is* its interview, so the grill must precede it in-context — leave the brief for a later session and the chain breaks. A signal to surface, not a gate: on the common single-unit path the offer above stays exactly as shipped.

*(Reach for grill-me instead when there are no files to open; for /folder-explore or /workbook-explore (or the audit skills) when you want the files inspected and reported on, not your plan interrogated.)*
