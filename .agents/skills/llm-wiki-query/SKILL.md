---
name: llm-wiki-query
description: Answer a question from the compiled Wiki before reading broad Raw context.
---

# LLM Wiki — Query Skill

Use this skill whenever the user asks a question that this vault might already have knowledge about.

## Steps

1. Start with `Wiki/index.md` for orientation.
2. Search the catalog rather than grepping the whole vault:
   ```bash
   python scripts/wiki_tool.py search-catalog --query "user's topic"
   ```
3. Open only the most relevant Wiki notes returned.
4. Answer using those notes. Cite the compiled note (and its `sources`) in your answer.
5. Only open files under `Raw/Sources/` directly when:
   - the compiled note is `status: seed` and clearly too thin, or
   - the user explicitly asks to see the original source / verify a claim.
6. If nothing in the catalog is relevant, say so plainly rather than improvising an answer as if it came from the Wiki — offer to ingest a new source instead.
