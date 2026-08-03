# Naming Conventions

## Files

- Use `Title Case With Spaces.md` for note filenames — Obsidian wikilinks read naturally this way (`[[Retrieval Augmented Generation]]`).
- Raw sources: name after the source's title, not a generic "source-1.md". If a stable slug is needed for scripting, keep the human title as the file's `Title` frontmatter.
- Avoid special characters that break wikilinks or file systems: `# ^ [ ] | : \ / ? " < > *`.

## Folders

- `Wiki/Topics/` — broad subject areas that group multiple concepts (e.g. `Retrieval Augmented Generation.md`).
- `Wiki/Concepts/` — a single idea, technique, or definition (e.g. `Chunking Strategy.md`).
- `Wiki/Entities/` — a specific person, product, organization, or tool (e.g. `Obsidian.md`).
- `Wiki/Projects/` — an ongoing effort with a goal and status (e.g. `Second Brain Setup.md`).
- `Wiki/Logs/` — dated changelog-style entries of what changed and why.

## Aliases and links

- Use `aliases` in frontmatter for alternate names rather than duplicate notes.
- Prefer linking `[[Note Name]]` over duplicating content across notes.

## Wiki note tag ↔ folder mapping

The tag in frontmatter must match the folder the note lives in:

| tag | folder |
|---|---|
| `topic` | `Wiki/Topics/` |
| `concept` | `Wiki/Concepts/` |
| `entity` | `Wiki/Entities/` |
| `project` | `Wiki/Projects/` |
| `log` | `Wiki/Logs/` |

`lint` checks this mapping.
