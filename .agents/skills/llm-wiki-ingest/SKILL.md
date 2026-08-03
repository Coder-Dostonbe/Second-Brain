---
name: llm-wiki-ingest
description: Compile a Raw source into linked, traceable Wiki notes.
---

# LLM Wiki — Ingest Skill

Use this skill whenever a new file appears in `Raw/Sources/`, or the user asks to "add this to my wiki / second brain."

## Steps

1. Confirm the source file exists under `Raw/Sources/` with valid frontmatter (see `Schema/frontmatter-schema.md`). If missing, create it from `_templates/source-note.md` first.
2. Run `python scripts/wiki_tool.py search-catalog --query "<likely topic>"` to find existing related Wiki notes before creating new ones.
3. For each reusable claim worth keeping, create or update a note in the matching `Wiki/` subfolder using the template from `_templates/` that matches the tag (`topic`, `concept`, `entity`, `project`, `log`).
4. Add the Raw source's path to that note's `sources` list and update `source_count` to match.
5. Never copy large verbatim blocks from the source — compile, don't duplicate. Keep notes short and reusable.
6. Never state a claim in a Wiki note that isn't backed by the Raw source(s) listed in `sources`.
7. After compiling, run:
   ```bash
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-scan --update --accept-covered
   python scripts/wiki_tool.py source-lint
   ```
8. If the ingest meaningfully changed the Wiki, append a log entry:
   ```bash
   python scripts/wiki_tool.py log --title "Ingested <source>" --details "<one line on what was compiled>"
   ```
