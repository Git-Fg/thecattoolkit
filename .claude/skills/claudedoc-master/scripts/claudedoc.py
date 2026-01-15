#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class Entry:
    slug: str
    title: str
    url: str
    tags: List[str]


def _skill_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _catalog_path() -> str:
    return os.path.join(_skill_root(), "catalog.json")


def _load_catalog() -> Dict[str, Any]:
    path = _catalog_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"catalog.json not found at: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _entries() -> List[Entry]:
    catalog = _load_catalog()
    entries = []
    for raw in catalog.get("entries", []):
        entries.append(
            Entry(
                slug=str(raw.get("slug", "")).strip(),
                title=str(raw.get("title", "")).strip(),
                url=str(raw.get("url", "")).strip(),
                tags=list(raw.get("tags", [])),
            )
        )
    return [e for e in entries if e.slug and e.title and e.url]


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def _fuzzy_score(haystack: str, query: str) -> float:
    if not query:
        return 0.0
    if query in haystack:
        return 1.0 + (len(query) / len(haystack))
    return difflib.SequenceMatcher(None, haystack, query).ratio()


def _score_entry(entry: Entry, query: str) -> float:
    q = _normalize(query)
    if not q:
        return 0.0
    slug_score = _fuzzy_score(_normalize(entry.slug), q) * 5.0
    title_score = _fuzzy_score(_normalize(entry.title), q) * 3.0
    tags_score = max([_fuzzy_score(_normalize(t), q) for t in entry.tags] + [0.0]) * 2.0
    return slug_score + title_score + tags_score


def _find_entry_by_slug(slug: str) -> Optional[Entry]:
    for entry in _entries():
        if entry.slug == slug:
            return entry
    return None


def _get_url(url_or_slug: str) -> Optional[str]:
    if url_or_slug.startswith(("http://", "https://")):
        return url_or_slug
    entry = _find_entry_by_slug(url_or_slug)
    return entry.url if entry else None


def cmd_search(query: str, limit: int = 5):
    ents = _entries()
    scored = [(e, _score_entry(e, query)) for e in ents]
    scored = [x for x in scored if x[1] > 0.5]
    scored.sort(key=lambda x: x[1], reverse=True)
    results = scored[:limit]
    if not results:
        print(f"No documentation found for: {query}", file=sys.stderr)
        return
    for entry, score in results:
        tags_str = ", ".join(entry.tags)
        print(f"- **{entry.slug}**: [{entry.title}]({entry.url}) — _{tags_str}_")


def cmd_read(url_or_slug: str):
    url = _get_url(url_or_slug)
    if not url:
        print(f"Error: URL or slug not found: {url_or_slug}", file=sys.stderr)
        return 1
    try:
        result = subprocess.run(
            ["curl", "-s", "-L", url],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("Error: curl not found. Please install curl.", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Claude Documentation Link Resolver"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (fuzzy search) or URL/slug (with --read)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of search results (default: 5)",
    )
    parser.add_argument(
        "--read",
        action="store_true",
        help="Read content from URL or slug using curl",
    )

    args = parser.parse_args()

    try:
        if not args.query:
            parser.print_help()
            return 1
        if args.read:
            return cmd_read(args.query)
        else:
            cmd_search(args.query, args.limit)
            return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
