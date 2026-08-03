# Workflow Examples

## Example 1: Ingesting a new article

1. Save the cleaned article Markdown to `Raw/Sources/Streaming Systems Overview.md` using `_templates/source-note.md`, with `Processed: false`.
2. `python scripts/wiki_tool.py search-catalog --query "streaming"` — see if a `Wiki/Topics/Streaming Systems.md` topic already exists.
3. If it exists, open it and add a new subsection or link a new concept note instead of duplicating.
4. Create `Wiki/Concepts/Exactly Once Delivery.md` from `_templates/concept-note.md`, with:
   ```yaml
   sources:
     - "Raw/Sources/Streaming Systems Overview.md"
   source_count: 1
   ```
5. Run the ingest command sequence from `AGENTS.md`.
6. `source-scan --update --accept-covered` flips the source's `Processed` state and records `covered_by` in the manifest.

## Example 2: Answering "what do we know about X?"

1. `python scripts/wiki_tool.py search-catalog --query "X"`.
2. Open the top 1-3 matches from `Wiki/`.
3. Answer from those notes, citing the note and its `sources`.
4. Only open `Raw/Sources/` files directly if the user asks "show me the original" or the compiled note is too thin (`status: seed`).

## Example 3: A Raw source with no coverage yet

1. `python scripts/wiki_tool.py source-delta` lists sources in `Raw/Sources/` not yet in `Schema/source-manifest.jsonl` or not covered by any Wiki note.
2. Compile at least one Wiki note per uncovered source before considering ingestion "done."
3. `source-lint` will fail the build if a source is marked `Processed: true` without `covered_by` entries — this is intentional, it catches false "done" claims.
