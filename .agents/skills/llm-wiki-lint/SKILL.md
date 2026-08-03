---
name: llm-wiki-lint
description: Validate the Wiki's frontmatter, tags, and source links before a commit.
---

# LLM Wiki — Lint Skill

Use this skill before any commit that touches `Wiki/`, `Raw/Sources/`, or `Schema/`.

## Steps

1. Run:
   ```bash
   python scripts/wiki_tool.py doctor
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-lint
   python scripts/audit_public.py
   ```
2. If `lint` reports a bad tag, mismatched folder, or `source_count` mismatch, fix the specific note's frontmatter — don't relax the check.
3. If `source-lint` reports a source marked `Processed: true` with no coverage, either compile a Wiki note for it or set `Processed: false` — don't fake coverage.
4. If `audit_public.py` fails, remove the offending secret/path/private key from the file and from git history if already committed, before proceeding.
5. Re-run the full sequence until everything passes. See `Schema/lint-checklist.md` for the exact checklist being enforced.
