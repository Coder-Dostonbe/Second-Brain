# Command Reference — `scripts/wiki_tool.py`

Run from the vault root. Requires Python 3.8+, standard library only (no `pip install` needed).

```bash
python scripts/wiki_tool.py <command> [options]
```

| command | mutates? | purpose |
|---|---|---|
| `doctor` | no | Health check: required folders, Python version, catalog/manifest presence, note counts. |
| `build` | yes | Regenerate `Wiki/catalog.jsonl`, `Wiki/index.md`, and per-folder `index.md` files from the current notes. |
| `lint` | no | Validate compiled Wiki note frontmatter: allowed tag, tag↔folder match, `source_count` == `len(sources)`, source links exist, dates present. |
| `source-scan` | no (see `--update`) | List Raw sources with their live coverage (which Wiki notes cite them). |
| `source-scan --update` | yes | Also write `Schema/source-manifest.jsonl`. |
| `source-scan --update --accept-covered` | yes | Additionally flip a source's `Processed` field to `true` once a Wiki note covers it. |
| `source-lint` | no | Validate Raw source frontmatter (`Title`, `Reference`, `Created`, `Processed`, `tags`) and fail if a source is marked `Processed: true` with no manifest coverage. |
| `source-delta` | no | List Raw sources with no Wiki note coverage yet. |
| `source-coverage` | no | Show which Wiki notes cover each Raw source. |
| `search-catalog --query "text"` | no | Case-insensitive search over `Wiki/catalog.jsonl` (title, path, tag, topics). |
| `log --title "..." --details "..."` | yes | Append a timestamped entry to `Wiki/log.md`. |

## Typical sequences

**Maintenance gate** (before every meaningful commit):

```bash
python scripts/wiki_tool.py doctor
python scripts/wiki_tool.py build
python scripts/wiki_tool.py lint
python scripts/wiki_tool.py source-lint
python scripts/audit_public.py
```

**After ingesting a new source:**

```bash
python scripts/wiki_tool.py source-scan --update --accept-covered
python scripts/wiki_tool.py source-lint
```

## Git hook

`scripts/install_hooks.sh` sets `git config core.hooksPath .githooks`, so `.githooks/pre-commit` (build → lint → source-lint → audit_public) runs automatically on every commit. Run it once per clone:

```bash
sh scripts/install_hooks.sh
```
