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
  - "file locking"
---

# File Lock Protocol

## Definition

A mandatory check-before-edit rule for multi-agent repos: before touching any file, a terminal reads a shared lock ledger, waits out any fresh lock held by another terminal, claims the file with its own timestamped entry, edits, then removes its entry when done. Read-only operations (`Read`, `Grep`, `git status`, `git diff`) are exempt.

## Why it matters

Without it, two Claude Code terminals editing the same file concurrently silently overwrite each other's work. The 15-minute TTL on locks also guards against a crashed or abandoned terminal permanently blocking a file — but a stale lock should be *cleared with a warning*, not silently ignored, since the "abandoned" terminal might just be slow.

## Related

- [[Multi-Agent Claude Code Coordination]]
- [[Planner Approval Gate]]
