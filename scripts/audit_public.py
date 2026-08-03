#!/usr/bin/env python3
"""Fail fast on secrets, machine-local paths, private keys, or plugin/cache state before a commit."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IGNORED_DIR_PARTS = {".git", ".obsidian"}

SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key material"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+]{16,}"), "likely secret assignment"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub personal access token"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "likely API secret key"),
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s\"']+"),
    re.compile(r"/home/[^/\s\"']+"),
    re.compile(r"/Users/[^/\s\"']+"),
]

BAD_STAGED_PATH_PARTS = [
    "/.obsidian/plugins/",
    "/.obsidian/cache/",
    "\\.obsidian\\plugins\\",
    "\\.obsidian\\cache\\",
]


def iter_tracked_files(root):
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in IGNORED_DIR_PARTS for part in p.parts):
            continue
        yield p


SELF_PATH = Path(__file__).resolve()


def main():
    problems = []

    for p in iter_tracked_files(ROOT):
        if p.resolve() == SELF_PATH:
            continue  # this file's own pattern source text would flag itself
        rel = p.relative_to(ROOT).as_posix()

        for part in BAD_STAGED_PATH_PARTS:
            if part.replace("\\", "/") in ("/" + rel):
                problems.append(f"{rel}: plugin/cache state should not be committed")

        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue  # binary or unreadable file, skip content scan

        for pattern, label in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"{rel}: possible {label}")

        for pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                problems.append(f"{rel}: machine-local absolute path leaked into a tracked file")
                break

    if problems:
        print("audit_public: FAILED")
        for p in sorted(set(problems)):
            print(f"  - {p}")
        return 1

    print("audit_public: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
