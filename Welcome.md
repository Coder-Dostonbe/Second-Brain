---
tags:
  - "log"
---

# Welcome to your Second Brain (LLM Wiki)

This vault separates **raw material** from **compiled knowledge**:

- `Raw/Sources/` — original material, preserved as-is (articles, transcripts, notes you captured). Never edited into prose here — just captured.
- `Wiki/` — distilled, reusable knowledge compiled from Raw sources, organized into `Topics/`, `Concepts/`, `Entities/`, `Projects/`, `Logs/`.
- `Schema/` — the rules that keep the Wiki honest: frontmatter schema, naming conventions, lint checklist, source manifest.
- `_templates/` — starting frontmatter for every note type.
- `.agents/skills/` — instructions so an AI agent knows how to ingest, query, lint, and maintain this vault.
- `.claude/skills/` — Obsidian-format skills (markdown, bases, canvas) so Claude Code can write valid Obsidian files.
- `scripts/wiki_tool.py` — the only tool that touches `Wiki/catalog.jsonl` and `Schema/source-manifest.jsonl`. Run it before every commit.

## How to use this with an agent

1. Drop new material into `Raw/Sources/` as Markdown.
2. Ask the agent to read `AGENTS.md` and compile it into `Wiki/`.
3. Every compiled note must link back to the Raw source(s) it came from.
4. Before committing, the agent runs `doctor`, `build`, `lint`, `source-scan --update --accept-covered`, `source-lint`, and `audit_public.py`.

Start exploring at [[Wiki/index|Wiki/index.md]] once it exists, or read `AGENTS.md` for the full rulebook.
