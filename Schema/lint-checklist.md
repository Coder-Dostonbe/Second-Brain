# Lint Checklist

## `wiki_tool.py lint` (compiled Wiki notes)

- [ ] Frontmatter parses as valid YAML.
- [ ] `tags` contains exactly one of: `topic`, `concept`, `entity`, `project`, `log`.
- [ ] The note's tag matches the folder it lives in (see `naming-conventions.md`).
- [ ] `source_count` equals the length of `sources`.
- [ ] Every path in `sources` points to a file that exists under `Raw/Sources/`.
- [ ] `created` and `updated` are present and look like `YYYY-MM-DD`.

## `wiki_tool.py source-lint` (Raw sources)

- [ ] Frontmatter parses as valid YAML.
- [ ] `Title`, `Reference`, `Created`, `Processed`, and `tags` are present.
- [ ] `tags` includes `"source"`.
- [ ] If `Processed: true`, the source manifest (`Schema/source-manifest.jsonl`) lists at least one covering Wiki note (`covered_by` non-empty). A source marked processed with no coverage is a lint failure.

## `audit_public.py`

- [ ] No obvious secrets (API keys, tokens, passwords) in any tracked file.
- [ ] No machine-local absolute paths (a personal computer's user home directory) leaking into committed notes.
- [ ] No private key material (`BEGIN ... PRIVATE KEY`).
- [ ] No `.obsidian/plugins/`, `.obsidian/cache/`, or `.obsidian/workspace*.json` accidentally staged.

Run all of these via the Maintenance Gate in `AGENTS.md` before every meaningful commit.
