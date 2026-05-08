#!/usr/bin/env python3
"""
Sync public Obsidian notes → Hugo content/posts/

Rules:
  - Only copies notes that have `public: true` in YAML front matter
    OR the tag "public" in their tags list.
  - Converts [[Wiki Links]] to Hugo-style markdown links.
  - If the linked note is not public, renders a broken-link span instead.
  - Computes backlinks and injects them into each note's front matter.
  - Reads OBSIDIAN_PATH from .env (or the environment).
"""

import os
import re
import sys
import shutil
import yaml
from pathlib import Path
from typing import Optional

# ── Config ────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).parent
REPO_ROOT   = SCRIPT_DIR.parent
CONTENT_DIR = REPO_ROOT / "content" / "posts"
ENV_FILE    = REPO_ROOT / ".env"

def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env

env = load_env()
OBSIDIAN_PATH = Path(os.environ.get("OBSIDIAN_PATH") or env.get("OBSIDIAN_PATH", ""))

if not OBSIDIAN_PATH or not OBSIDIAN_PATH.exists():
    print(f"ERROR: Obsidian vault not found at '{OBSIDIAN_PATH}'")
    print("Set OBSIDIAN_PATH in .env or as an environment variable.")
    sys.exit(1)

# ── Helpers ───────────────────────────────────────────────────
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE     = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def slugify(title: str) -> str:
    """Convert a note title to a URL slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def parse_note(path: Path) -> tuple[dict, str]:
    """Return (front_matter_dict, body_markdown)."""
    raw = path.read_text(encoding="utf-8")
    m   = FRONT_MATTER_RE.match(raw)
    if m:
        fm   = yaml.safe_load(m.group(1)) or {}
        body = raw[m.end():]
    else:
        fm   = {}
        body = raw
    return fm, body


def is_public(fm: dict) -> bool:
    """True if the note should be published."""
    if fm.get("public") is True:
        return True
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return "public" in [str(t).lower().strip() for t in tags]


def note_title(path: Path) -> str:
    """Use the filename stem as the note title (Obsidian convention)."""
    return path.stem


# ── Pass 1: collect all public notes ──────────────────────────
print(f"Scanning vault: {OBSIDIAN_PATH}")
all_notes: dict[str, Path] = {}    # title → path
public_notes: dict[str, Path] = {} # title → path

for md_file in OBSIDIAN_PATH.rglob("*.md"):
    title = note_title(md_file)
    all_notes[title] = md_file
    fm, _ = parse_note(md_file)
    if is_public(fm):
        public_notes[title] = md_file

print(f"Found {len(all_notes)} notes total, {len(public_notes)} public.")

# ── Pass 2: compute backlinks ──────────────────────────────────
# backlinks[title] = list of public titles that link TO it
backlinks: dict[str, list[str]] = {t: [] for t in public_notes}

for src_title, src_path in public_notes.items():
    _, body = parse_note(src_path)
    for m in WIKILINK_RE.finditer(body):
        target = m.group(1).strip()
        if target in public_notes and target != src_title:
            backlinks.setdefault(target, [])
            if src_title not in backlinks[target]:
                backlinks[target].append(src_title)

# ── Pass 3: write Hugo content ─────────────────────────────────
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

# Remove stale posts (notes that were un-published)
existing_slugs = {f.stem for f in CONTENT_DIR.glob("*.md") if f.name != "_index.md"}
new_slugs = {slugify(t) for t in public_notes}
for stale in existing_slugs - new_slugs:
    stale_path = CONTENT_DIR / f"{stale}.md"
    stale_path.unlink()
    print(f"  Removed stale: {stale}.md")


def convert_wikilinks(body: str, public_set: set[str]) -> str:
    """Replace [[Link]] with Hugo markdown links or broken-link spans."""
    def replace(m: re.Match) -> str:
        target  = m.group(1).strip()
        display = (m.group(2) or target).strip()
        if target in public_set:
            slug = slugify(target)
            return f"[{display}](/posts/{slug}/)"
        else:
            return f'<span class="broken-link" title="This note is not public">{display}</span>'
    return WIKILINK_RE.sub(replace, body)


public_titles = set(public_notes.keys())
written = 0

for title, src_path in public_notes.items():
    fm, body = parse_note(src_path)
    slug     = slugify(title)

    # Ensure Hugo-required front matter fields
    fm.setdefault("title", title)
    fm.setdefault("draft", False)
    fm.pop("public", None)  # remove our custom flag

    # Inject backlinks as Hugo-readable paths
    note_backlinks = [f"/posts/{slugify(t)}/" for t in backlinks.get(title, [])]
    if note_backlinks:
        fm["backlinks"] = note_backlinks
    else:
        fm.pop("backlinks", None)

    # Convert wiki-links
    converted_body = convert_wikilinks(body, public_titles)

    # Serialise front matter back to YAML
    fm_yaml = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
    output  = f"---\n{fm_yaml}---\n\n{converted_body}"

    dest = CONTENT_DIR / f"{slug}.md"
    dest.write_text(output, encoding="utf-8")
    written += 1

print(f"Written {written} posts to {CONTENT_DIR}")

# Ensure _index.md exists for the section
index_path = CONTENT_DIR / "_index.md"
if not index_path.exists():
    index_path.write_text(
        "---\ntitle: Blog\ndescription: Writing by Giorgenes\n---\n",
        encoding="utf-8",
    )
    print("Created content/posts/_index.md")

print("Sync complete.")
