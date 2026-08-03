---
tags:
  - "concept"
topics:
  - "Multi-Agent Claude Code Coordination"
status: seed
created: 2026-08-03
updated: 2026-08-03
sources:
  - "Raw/Sources/Multi-Agent Claude Code Coordination Protocol.md"
source_count: 1
aliases:
  - "approval gate"
---

# Planner Approval Gate

## Definition

A hard stop in the workflow: once a Developer terminal moves a task to "AWAITING REVIEW" on the shared kanban, it must not `git add`/`commit`/`push` until the user relays that the Planner has approved it (`approved <TASK-ID>`). The Planner independently re-runs the build/tests and exercises the change — a developer's own "verified locally" note doesn't skip this.

## Why it matters

This plays the role a code-review step would play in a normal PR-based workflow, but for a single-branch model (see [[Multi-Agent Claude Code Coordination]]) where everyone commits straight to `main`. Without an independent re-check, a developer's local "it works" claim is the only gate, and duplicated/conflicting work across T1 and T2 wouldn't be caught before landing on `main`.

## Related

- [[Multi-Agent Claude Code Coordination]]
- [[File Lock Protocol]]
