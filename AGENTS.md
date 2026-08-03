# AGENTS.md — Rules for any agent working in this vault

This vault is an **LLM Wiki**: a second brain built for both humans and AI agents to query reliably.

## The three layers

- **`Raw/Sources/`** — source material, not compiled notes. Treat every file here as evidence, not as something to present directly as "the answer." Never rewrite a Raw source into prose; only add/append new sources here.
- **`Wiki/`** — the only place reusable knowledge should be written. Organized into `Topics/`, `Concepts/`, `Entities/`, `Projects/`, `Logs/`.
- **`Schema/`** — the rules and machine-readable manifests that keep the Wiki honest.

## Hard rules

1. Treat `Raw/Sources/` as source material, not as compiled notes.
2. Write reusable knowledge only under `Wiki/`.
3. Keep every compiled note linked to one or more Raw sources via its `sources` frontmatter field.
4. Search `Wiki/catalog.jsonl` before opening broad Raw context — don't re-read all of `Raw/` for every question.
5. Run `build`, `lint`, and source checks before commits (see Maintenance Gate below).
6. Do not invent citations or create unsupported claims. If a claim isn't backed by a Raw source, don't compile it into the Wiki as fact.

## Compiled note tags

Every note in `Wiki/` must use exactly one of these tags: `topic`, `concept`, `entity`, `project`, `log`.

See `Schema/frontmatter-schema.md` for the exact frontmatter shape and `Schema/naming-conventions.md` for file naming.

## Ingest workflow (new source arrives)

1. Put cleaned Markdown in `Raw/Sources/` using `_templates/source-note.md`.
2. Run `python scripts/wiki_tool.py search-catalog --query "..."` for likely related topics already in the Wiki.
3. Open only the most relevant existing compiled Wiki notes — don't re-derive everything from scratch.
4. Create or update focused notes in `Wiki/` using the matching template in `_templates/`.
5. Add the Raw source path to each note's `sources` list and keep `source_count` accurate.
6. Run:
   ```bash
   python scripts/wiki_tool.py build
   python scripts/wiki_tool.py lint
   python scripts/wiki_tool.py source-scan --update --accept-covered
   python scripts/wiki_tool.py source-lint
   ```
7. Add a log entry (`python scripts/wiki_tool.py log --title "..." --details "..."`) if the ingest meaningfully changed the Wiki.

## Query workflow (answering a question)

1. Start with `Wiki/index.md`.
2. Search the catalog: `python scripts/wiki_tool.py search-catalog --query "user topic"`.
3. Open the most relevant Wiki notes.
4. Open Raw sources only when the compiled note is insufficient or the user asks for source-level verification.
5. Cite the compiled note and Raw source when the answer depends on source material.

## Maintenance gate (run before every meaningful commit)

```bash
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

After ingesting a source, also run:

```bash
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
```

See `Schema/command-reference.md` for full command docs and `Schema/lint-checklist.md` for what lint actually checks.

## Obsidian formatting

When writing or editing any note in this vault, follow Obsidian Flavored Markdown conventions (wikilinks `[[Note Name]]`, callouts, properties) — see the skills under `.claude/skills/` (installed from kepano/obsidian-skills) for the exact syntax rules.
