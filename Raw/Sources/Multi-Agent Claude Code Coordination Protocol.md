---
Title: "Multi-Agent Claude Code Coordination Protocol"
Author: "Doston Yusupov"
Reference: "C:\\Users\\user\\CLAUDE.md (project instructions)"
ContentType:
  - "markdown"
Created: 2026-08-03
Processed: true
tags:
  - "source"
---

# Multi-Agent Claude Code Coordination Protocol

Captured from the project's `CLAUDE.md`, which configures 3 parallel Claude Code terminals working on the same repo.

## Terminal roles

- T1, T2 — Developers: implement tasks assigned by the Planner.
- P — Planner: plans, dispatches, reviews, and approves; never writes code.

Coordination is enforced by three artifacts at the repo root: `active_tasks.md` (kanban), `active_files.md` (file locks), and `.multi-agent/config.json` (settings). The kanban and lock files are gitignored (live state); the config is committed so the team shares settings on clone.

## File-lock protocol (mandatory before every edit)

1. Read `active_files.md`.
2. If the target path is locked by another terminal and the timestamp is fresher than 15 minutes, wait 30s and re-check, looping until the lock disappears.
3. If locked but older than the TTL: it's stale — warn the user before clearing, per project policy.
4. If not listed: append `- <path> → T<N> @ <ISO-timestamp>` (developers) or `- <path> → P @ <ISO-timestamp>` (planner), then proceed.
5. Edit.
6. Remove your line from `active_files.md` immediately when done.

Read-only operations (`Read`, `Grep`, `git status`, `git diff`) do not need a lock.

## Shared kanban (`active_tasks.md`)

Four sections in order: 🟢 IN PROGRESS/TODO → 🟡 AWAITING REVIEW → 🟠 BLOCKED → ✅ DONE.

- Planner writes new tasks into TODO with full file lists, acceptance criteria, and an assignee.
- Developer picks up a task, locks files, implements, runs verification, moves it to AWAITING REVIEW with a status note.
- Developers STOP at AWAITING REVIEW — no commit until the user relays Planner approval.
- After approval: pull-rebase → stage specific files → commit → push → move to DONE with commit hash.

## Approval gate

Developers must stop at AWAITING REVIEW and wait for the user to relay the Planner's approval (`approved <TASK-ID>`) before running `git add`/`commit`/`push`. The Planner independently re-runs build/tests and exercises the change before approving — a developer's "verified locally" note is not sufficient on its own.

## Git workflow — Variant B (single integration branch)

All developers commit directly to `main`; there are no per-task feature branches, since the Planner approval gate plays the code-review role. Before committing an approved task: `git fetch && git pull --rebase origin main`, stage only the specific changed files (never `git add -A`), commit, then `git push origin main`. Releases are cut from `main` and tagged.

## Commit format

Conventional Commits — `<type>(<scope>): <description>`, imperative subject under ~72 chars, with a body when the change isn't self-explanatory.
