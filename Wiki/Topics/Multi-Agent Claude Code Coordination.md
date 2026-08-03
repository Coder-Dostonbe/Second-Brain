---
tags:
  - "topic"
topics: []
status: seed
created: 2026-08-03
updated: 2026-08-03
sources:
  - "Raw/Sources/Multi-Agent Claude Code Coordination Protocol.md"
source_count: 1
aliases:
  - "Multi-Agent Coordination"
---

# Multi-Agent Claude Code Coordination

## Overview

Running several Claude Code terminals on one repo needs an explicit protocol, or two agents will edit the same file or commit conflicting work. The setup used in this project splits terminals into **Developer** (T1, T2) and **Planner** (P) roles, coordinated through three shared artifacts at the repo root: a kanban (`active_tasks.md`), a file-lock ledger (`active_files.md`), and a committed settings file (`.multi-agent/config.json`).

## Key concepts

- [[File Lock Protocol]]
- [[Planner Approval Gate]]

## Open questions

- How should the stale-lock TTL (15 minutes) be tuned for slower, longer-running tasks?
