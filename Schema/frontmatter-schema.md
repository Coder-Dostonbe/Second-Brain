# Frontmatter Schema

## Raw source notes (`Raw/Sources/*.md`)

```yaml
---
Title: ""
Author: ""
Reference: ""
ContentType:
  - "markdown"
Created: YYYY-MM-DD
Processed: false
tags:
  - "source"
---
```

- `Title` — human-readable title of the source.
- `Author` — creator of the original material, if known.
- `Reference` — a URL, ISBN, file path, or other stable pointer to the origin. Use `"owned-demo"` for self-authored fixtures.
- `ContentType` — list, usually `["markdown"]`.
- `Created` — ISO date the source was captured into this vault.
- `Processed` — `true` once at least one compiled Wiki note covers this source; otherwise `false`.
- `tags` — must include `"source"`.

## Compiled Wiki notes (`Wiki/**/*.md`)

```yaml
---
tags:
  - "concept"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---
```

- `tags` — exactly one allowed value: `topic`, `concept`, `entity`, `project`, or `log`.
- `topics` — related topic note links (wikilink strings), optional.
- `status` — `seed` (just created, thin), `growing` (actively expanded), or `stable` (mature, rarely changes).
- `created` / `updated` — ISO dates.
- `sources` — list of paths under `Raw/Sources/` this note's claims trace back to. Must be non-empty for any note that makes factual claims.
- `source_count` — must equal `len(sources)`. Checked by `lint`.
- `aliases` — alternate names/wikilink targets for this note.

Both schemas are validated by `python scripts/wiki_tool.py lint` (compiled notes) and `python scripts/wiki_tool.py source-lint` (Raw sources).
