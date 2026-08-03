---
name: llm-wiki-maintain
description: Keep indexes, catalog, and source manifest up to date over time.
---

# LLM Wiki — Maintain Skill

Use this skill periodically, or whenever asked to "clean up / rebuild the wiki."

## Steps

1. `python scripts/wiki_tool.py doctor` — check folder structure, Python version, catalog and manifest presence, note counts.
2. `python scripts/wiki_tool.py build` — regenerate `Wiki/catalog.jsonl`, `Wiki/index.md`, and per-folder `index.md` files. Never hand-edit these generated files — re-run `build` instead.
3. `python scripts/wiki_tool.py source-delta` — list Raw sources not yet represented in the manifest; ingest or explicitly skip them.
4. `python scripts/wiki_tool.py source-coverage` — check which sources are covered by which notes; look for sources with thin (single-note) coverage that might deserve more compiled notes.
5. Look for notes stuck at `status: seed` for a long time — either expand them or leave a log entry explaining why they're intentionally thin.
6. Run the full maintenance gate (`doctor`, `build`, `lint`, `source-lint`, `audit_public.py`) before committing any maintenance changes.
