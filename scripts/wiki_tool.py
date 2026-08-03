#!/usr/bin/env python3
"""Deterministic tooling for the LLM Wiki. Standard library only, no third-party deps."""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ALLOWED_TAGS = {"topic", "concept", "entity", "project", "log"}
FOLDER_FOR_TAG = {
    "topic": "Topics",
    "concept": "Concepts",
    "entity": "Entities",
    "project": "Projects",
    "log": "Logs",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --- minimal frontmatter parsing (stdlib only, no PyYAML) ---------------


def split_frontmatter(text):
    """Return (frontmatter_text, body) or (None, text) if no frontmatter block."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines(keepends=True)
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = "".join(lines[1:i])
            body = "".join(lines[i + 1:])
            return fm, body
    return None, text


def _strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    return s


def parse_simple_yaml(fm_text):
    """Parse the flat key/value + block-list subset of YAML used by this vault's templates."""
    data = {}
    if not fm_text:
        return data
    lines = fm_text.splitlines()
    i, n = 0, len(lines)
    key_re = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")
    item_re = re.compile(r"^\s*-\s*(.*)$")
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = key_re.match(line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            items = []
            j = i + 1
            while j < n and item_re.match(lines[j]):
                items.append(_strip_quotes(item_re.match(lines[j]).group(1)))
                j += 1
            if j > i + 1:
                data[key] = items
                i = j
                continue
            data[key] = None
            i += 1
        elif val == "[]":
            data[key] = []
            i += 1
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [_strip_quotes(x) for x in inner.split(",")] if inner else []
            i += 1
        else:
            data[key] = _strip_quotes(val)
            i += 1
    return data


def update_scalar_field(text, key, new_value):
    """Rewrite a single scalar frontmatter field in place, preserving everything else."""
    fm, body = split_frontmatter(text)
    if fm is None:
        return text
    field_re = re.compile(rf"^{re.escape(key)}:\s*.*$")
    out = []
    replaced = False
    for line in fm.splitlines():
        if not replaced and field_re.match(line):
            out.append(f"{key}: {new_value}")
            replaced = True
        else:
            out.append(line)
    new_fm = "\n".join(out)
    return f"---\n{new_fm}\n---\n{body}" if new_fm else text


def extract_title(body):
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("# ") and not s.startswith("##"):
            return s[2:].strip()
    return None


# --- vault helpers --------------------------------------------------------


def list_raw_sources(root):
    d = root / "Raw" / "Sources"
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.md"))


def iter_wiki_notes(root):
    wiki_dir = root / "Wiki"
    if not wiki_dir.is_dir():
        return
    log_flat = (root / "Wiki" / "log.md").resolve()
    for p in sorted(wiki_dir.rglob("*.md")):
        if p.name.lower() == "index.md":
            continue
        if p.resolve() == log_flat:
            continue
        yield p


def compute_coverage(root):
    """path-under-Raw/Sources -> [wiki note paths that list it in `sources`]"""
    coverage = {}
    for p in iter_wiki_notes(root):
        fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        data = parse_simple_yaml(fm)
        sources = data.get("sources") or []
        rel_note = p.relative_to(root).as_posix()
        for s in sources:
            coverage.setdefault(s, []).append(rel_note)
    return coverage


def load_manifest(root):
    p = root / "Schema" / "source-manifest.jsonl"
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


# --- commands ---------------------------------------------------------


def cmd_doctor(root, args):
    problems = []
    required_dirs = [
        "Raw/Sources", "Raw/Files",
        "Wiki/Topics", "Wiki/Concepts", "Wiki/Entities", "Wiki/Projects", "Wiki/Logs",
        "Schema", "_templates", ".agents/skills", "scripts",
    ]
    for d in required_dirs:
        if not (root / d).is_dir():
            problems.append(f"missing directory: {d}")
    if sys.version_info < (3, 8):
        problems.append("python 3.8+ required")

    catalog = root / "Wiki" / "catalog.jsonl"
    manifest = root / "Schema" / "source-manifest.jsonl"
    sources = list_raw_sources(root)
    notes = list(iter_wiki_notes(root))

    print("LLM Wiki doctor")
    print(f"  python: {sys.version.split()[0]}")
    print(f"  catalog present: {catalog.exists()}")
    print(f"  source manifest present: {manifest.exists()}")
    print(f"  raw sources: {len(sources)}")
    print(f"  wiki notes: {len(notes)}")
    for folder in ("Topics", "Concepts", "Entities", "Projects", "Logs"):
        d = root / "Wiki" / folder
        count = len(list(d.glob("*.md"))) if d.is_dir() else 0
        print(f"    {folder}: {count}")

    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("OK")
    return 0


def cmd_build(root, args):
    notes = list(iter_wiki_notes(root))
    entries = []
    by_folder = {"Topics": [], "Concepts": [], "Entities": [], "Projects": [], "Logs": []}

    for p in notes:
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        data = parse_simple_yaml(fm)
        title = extract_title(body) or p.stem
        tags = data.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        tag = tags[0] if tags else ""
        entry = {
            "path": p.relative_to(root).as_posix(),
            "title": title,
            "tag": tag,
            "topics": data.get("topics") or [],
            "sources": data.get("sources") or [],
            "updated": data.get("updated") or "",
        }
        entries.append(entry)
        folder = p.parent.name
        if folder in by_folder:
            by_folder[folder].append(entry)

    entries.sort(key=lambda e: e["path"])
    catalog_path = root / "Wiki" / "catalog.jsonl"
    with catalog_path.open("w", encoding="utf-8", newline="\n") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    lines = [
        "# Wiki Index", "",
        f"_{len(entries)} compiled notes. Generated by `wiki_tool.py build` — do not hand-edit._", "",
    ]
    for folder in ("Topics", "Concepts", "Entities", "Projects", "Logs"):
        lines.append(f"## {folder}")
        lines.append("")
        for e in sorted(by_folder[folder], key=lambda e: e["title"]):
            lines.append(f"- [[{Path(e['path']).stem}]]")
        lines.append("")
    (root / "Wiki" / "index.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")

    for folder in ("Topics", "Concepts", "Entities", "Projects", "Logs"):
        flines = [f"# {folder} Index", ""]
        for e in sorted(by_folder[folder], key=lambda e: e["title"]):
            flines.append(f"- [[{Path(e['path']).stem}]]")
        (root / "Wiki" / folder / "index.md").write_text("\n".join(flines) + "\n", encoding="utf-8", newline="\n")

    print(f"build: {len(entries)} notes indexed -> Wiki/catalog.jsonl, Wiki/index.md, per-folder index.md")
    return 0


def cmd_lint(root, args):
    errors = []
    for p in iter_wiki_notes(root):
        rel = p.relative_to(root).as_posix()
        fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        data = parse_simple_yaml(fm)

        tags = data.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        valid = [t for t in tags if t in ALLOWED_TAGS]
        if len(tags) != 1 or len(valid) != 1:
            errors.append(f"{rel}: tags must contain exactly one of {sorted(ALLOWED_TAGS)}, got {tags}")
        else:
            expected_folder = FOLDER_FOR_TAG[valid[0]]
            if p.parent.name != expected_folder:
                errors.append(f"{rel}: tag '{valid[0]}' belongs in Wiki/{expected_folder}/, not Wiki/{p.parent.name}/")

        sources = data.get("sources") or []
        if not isinstance(sources, list):
            sources = []
        try:
            source_count = int(data.get("source_count"))
        except (TypeError, ValueError):
            source_count = None
        if source_count != len(sources):
            errors.append(f"{rel}: source_count ({source_count}) != len(sources) ({len(sources)})")
        for s in sources:
            if not (root / s).is_file():
                errors.append(f"{rel}: source link does not exist: {s}")

        for field in ("created", "updated"):
            v = data.get(field)
            if not v or not DATE_RE.match(str(v)):
                errors.append(f"{rel}: '{field}' missing or not YYYY-MM-DD")

    if errors:
        print("lint: FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"lint: OK ({len(list(iter_wiki_notes(root)))} notes)")
    return 0


def cmd_source_scan(root, args):
    coverage = compute_coverage(root)
    sources = list_raw_sources(root)
    manifest = []
    today = date.today().isoformat()

    for p in sources:
        rel = p.relative_to(root).as_posix()
        text = p.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)
        data = parse_simple_yaml(fm)
        title = data.get("Title") or p.stem
        covered_by = coverage.get(rel, [])
        was_processed = bool(data.get("Processed"))
        processed = was_processed or (bool(covered_by) and args.accept_covered)
        manifest.append({
            "path": rel, "title": title, "processed": processed,
            "covered_by": covered_by, "updated": today,
        })
        print(f"{rel}: covered_by={len(covered_by)} processed={processed}")

        if args.update and args.accept_covered and covered_by and not was_processed:
            p.write_text(update_scalar_field(text, "Processed", "true"), encoding="utf-8", newline="\n")

    if args.update:
        manifest.sort(key=lambda e: e["path"])
        manifest_path = root / "Schema" / "source-manifest.jsonl"
        with manifest_path.open("w", encoding="utf-8", newline="\n") as f:
            for e in manifest:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        print(f"source-scan: wrote {len(manifest)} entries -> Schema/source-manifest.jsonl")
    return 0


def cmd_source_lint(root, args):
    errors = []
    manifest_by_path = {m["path"]: m for m in load_manifest(root)}

    for p in list_raw_sources(root):
        rel = p.relative_to(root).as_posix()
        fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        data = parse_simple_yaml(fm)

        for field in ("Title", "Reference", "Created", "Processed"):
            if data.get(field) in (None, ""):
                errors.append(f"{rel}: missing '{field}'")

        tags = data.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        if "source" not in tags:
            errors.append(f"{rel}: tags must include 'source'")

        if data.get("Processed") is True:
            entry = manifest_by_path.get(rel)
            if not entry or not entry.get("covered_by"):
                errors.append(f"{rel}: marked Processed=true but has no Wiki coverage in source manifest")

    if errors:
        print("source-lint: FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"source-lint: OK ({len(list_raw_sources(root))} sources)")
    return 0


def cmd_source_delta(root, args):
    coverage = compute_coverage(root)
    sources = list_raw_sources(root)
    missing = [p.relative_to(root).as_posix() for p in sources
               if not coverage.get(p.relative_to(root).as_posix())]
    if missing:
        print("source-delta: sources with no Wiki coverage yet")
        for m in missing:
            print(f"  - {m}")
    else:
        print("source-delta: every Raw source is covered by at least one Wiki note")
    return 0


def cmd_source_coverage(root, args):
    coverage = compute_coverage(root)
    for p in list_raw_sources(root):
        rel = p.relative_to(root).as_posix()
        covered = coverage.get(rel, [])
        print(f"{rel}: {len(covered)} note(s)")
        for c in covered:
            print(f"  - {c}")
    return 0


def cmd_search_catalog(root, args):
    catalog_path = root / "Wiki" / "catalog.jsonl"
    if not catalog_path.is_file():
        print("search-catalog: no catalog yet, run `build` first")
        return 1
    q = args.query.lower()
    hits = []
    for line in catalog_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        haystack = " ".join([
            entry.get("title", ""), entry.get("path", ""), entry.get("tag", ""),
            " ".join(entry.get("topics") or []),
        ]).lower()
        if q in haystack:
            hits.append(entry)
    if not hits:
        print(f"search-catalog: no matches for '{args.query}'")
        return 0
    for e in hits:
        print(f"{e['tag']:<8} {e['title']}  ({e['path']})")
    return 0


def cmd_log(root, args):
    log_path = root / "Wiki" / "log.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"## {ts} — {args.title}\n\n{args.details}\n\n"
    existing = log_path.read_text(encoding="utf-8") if log_path.is_file() else "# Wiki Log\n\n"
    log_path.write_text(existing + entry, encoding="utf-8", newline="\n")
    print(f"log: appended entry '{args.title}'")
    return 0


def main(argv=None):
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(prog="wiki_tool.py")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")
    sub.add_parser("build")
    sub.add_parser("lint")

    p_scan = sub.add_parser("source-scan")
    p_scan.add_argument("--update", action="store_true")
    p_scan.add_argument("--accept-covered", action="store_true")

    sub.add_parser("source-lint")
    sub.add_parser("source-delta")
    sub.add_parser("source-coverage")

    p_search = sub.add_parser("search-catalog")
    p_search.add_argument("--query", required=True)

    p_log = sub.add_parser("log")
    p_log.add_argument("--title", required=True)
    p_log.add_argument("--details", required=True)

    args = parser.parse_args(argv)
    handlers = {
        "doctor": cmd_doctor,
        "build": cmd_build,
        "lint": cmd_lint,
        "source-scan": cmd_source_scan,
        "source-lint": cmd_source_lint,
        "source-delta": cmd_source_delta,
        "source-coverage": cmd_source_coverage,
        "search-catalog": cmd_search_catalog,
        "log": cmd_log,
    }
    return handlers[args.command](root, args)


if __name__ == "__main__":
    sys.exit(main())
