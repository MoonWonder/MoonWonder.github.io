#!/usr/bin/env python3
"""Automate the MoonWonder content migration.

This script materialises the restructuring described in the
"Automate content migration" ticket.  It analyses the existing Hugo content
under ``content/`` together with the canonical taxonomy map stored at
``data/taxonomy-map.yaml`` (and an optional audit report) to plan and execute a
migration.

Usage examples::

    python scripts/migrate_content.py --dry-run
    python scripts/migrate_content.py --apply --log migration.log

``--dry-run`` (the default) produces a textual report without touching the
working tree.  ``--apply`` performs the planned operations, creating ``.bak``
backups before files are modified or moved.

What the migration does:

* Normalises post file names to lowercase kebab-case slugs and converts Markdown
  entries with ``resources`` into leaf bundles (``<slug>/index.md``).
* Removes ``slug`` keys from front matter, canonicalises taxonomy values, and
  injects a stable ``commentID`` so Staticman comment threads survive URL
  changes.
* Relocates life diary entries from ``content/posts/life`` into
  ``content/life/<year>/<slug>/index.md`` bundles, keeping important front
  matter flags intact.
* Migrates the ``content/books`` hierarchy into ``content/series``.
* Rewrites internal links and shortcodes that reference ``/posts`` or
  ``/books`` so they track the new canonical paths (language prefixes are
  preserved automatically).
* Updates helper tooling (``content/posts/config.json``) when files move so
  relative paths remain valid.

The script is intentionally conservative: it reports every action it would take
and only mutates the repository when explicitly asked to ``--apply``.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:  # pragma: no cover - tooling guard
    import yaml
except ImportError as exc:  # pragma: no cover - tooling guard
    print("PyYAML is required to run the migration script", file=sys.stderr)
    raise


SCRIPT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_ROOT.parent
BACKUP_ROOT = PROJECT_ROOT / "migration_backups"

CONTENT_ROOT = Path("content")
POSTS_ROOT = CONTENT_ROOT / "posts"
LIFE_ROOT = CONTENT_ROOT / "life"
BOOKS_ROOT = CONTENT_ROOT / "books"
SERIES_ROOT = CONTENT_ROOT / "series"
TAXONOMY_MAP_PATH = Path("data/taxonomy-map.yaml")
DEFAULT_AUDIT_PATH = Path("data/audit-report.yaml")
FRONT_MATTER_DELIMITER = "---"
MARKDOWN_SUFFIX = ".md"
INDEX_MD = "index.md"

# Regex used to locate internal references we need to rewrite
INTERNAL_URL_PATTERN = re.compile(r"/(?:posts|books)/[^\s)\"'<>]+")


class MigrationError(RuntimeError):
    """Raised when the migration plan cannot be computed."""


@dataclass
class ResourceMove:
    source: Path
    destination: Path


@dataclass
class PagePlan:
    """Represents the plan for a single Markdown page that will move/change."""

    source: Path
    destination: Path
    front_matter: Dict
    body: str
    resource_moves: List[ResourceMove] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    entry_type: str = "post"  # post, life, series
    old_permalink: Optional[str] = None
    new_permalink: Optional[str] = None
    old_relpath: Optional[Path] = None
    new_relpath: Optional[Path] = None

    def summary(self) -> str:
        if self.source == self.destination:
            marker = str(self.source)
        else:
            marker = f"{self.source} → {self.destination}"
        suffix = f" ({'; '.join(self.notes)})" if self.notes else ""
        return f"{self.entry_type}: {marker}{suffix}"


@dataclass
class FileRewrite:
    path: Path
    updated_content: str
    rewrites: List[Tuple[str, str]]


@dataclass
class MigrationPlan:
    pages: List[PagePlan] = field(default_factory=list)
    rewrites: List[FileRewrite] = field(default_factory=list)
    link_rewrites: List[Tuple[Path, str, str]] = field(default_factory=list)
    unknown_taxonomy: Dict[str, Set[str]] = field(
        default_factory=lambda: collections.defaultdict(set)
    )
    slug_registry: Dict[Path, Set[str]] = field(
        default_factory=lambda: collections.defaultdict(set)
    )
    path_mapping: Dict[Path, Path] = field(default_factory=dict)
    obsolete_directories: Set[Path] = field(default_factory=set)

    def ensure_unique_slug(self, parent: Path, slug: str) -> str:
        """Guarantee slug uniqueness within ``parent`` by appending a suffix."""

        used = self.slug_registry[parent]
        candidate = slug
        counter = 2
        while candidate in used:
            candidate = f"{slug}-{counter}"
            counter += 1
        used.add(candidate)
        return candidate

    def add_page(self, page: PagePlan) -> None:
        self.pages.append(page)
        if page.old_relpath and page.new_relpath:
            self.path_mapping[page.old_relpath] = page.new_relpath


@dataclass
class FrontMatter:
    data: Dict
    body: str


def slugify(value: str, *, allow_unicode: bool = False) -> str:
    """Convert arbitrary text into a lowercase kebab-case slug."""

    original = value
    value = str(value or "").strip()
    if not value:
        return hashlib.sha1(original.encode("utf-8")).hexdigest()[:12]
    if not allow_unicode:
        value = unicodedata.normalize("NFKD", value)
        value = value.encode("ascii", "ignore").decode("ascii")
    else:
        value = unicodedata.normalize("NFKC", value)
    value = value.lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s_-]+", "-", value).strip("-")
    if not value:
        return hashlib.sha1(original.encode("utf-8")).hexdigest()[:12]
    return value


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_front_matter(raw: str) -> FrontMatter:
    if not raw.lstrip().startswith(FRONT_MATTER_DELIMITER):
        return FrontMatter({}, raw)

    lines = raw.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_DELIMITER:
        return FrontMatter({}, raw)

    closing_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == FRONT_MATTER_DELIMITER:
            closing_idx = idx
            break
    if closing_idx is None:
        return FrontMatter({}, raw)

    fm_body = "\n".join(lines[1:closing_idx])
    remainder = "\n".join(lines[closing_idx + 1 :])
    data = yaml.safe_load(fm_body) if fm_body.strip() else {}
    if data is None:
        data = {}
    if remainder and not remainder.endswith("\n"):
        remainder += "\n"
    return FrontMatter(data=data, body=remainder)


def render_markdown(front_matter: Dict, body: str) -> str:
    header = yaml.safe_dump(
        front_matter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).rstrip()
    body_section = body.lstrip("\n")
    return f"{FRONT_MATTER_DELIMITER}\n{header}\n{FRONT_MATTER_DELIMITER}\n\n{body_section}"


def backup_path(path: Path) -> Path:
    absolute = path.resolve()
    try:
        relative = absolute.relative_to(PROJECT_ROOT)
    except ValueError:
        relative = Path(absolute.name)
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    target = BACKUP_ROOT / relative
    if absolute.is_dir():
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(absolute, target)
        return target
    target = target.with_suffix(target.suffix + ".bak")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(absolute, target)
    return target


def safe_backup(path: Path) -> None:
    if path.exists():
        backup_path(path)


def load_taxonomy_map(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {"categories": {}, "tags": {}, "series": {}}
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    lookup: Dict[str, Dict[str, str]] = {k: {} for k in ("categories", "tags", "series")}

    def register(section: str, canonical: str, aliases: Iterable[str]) -> None:
        key = _tax_key(canonical)
        lookup[section][key] = canonical
        for alias in aliases or []:
            lookup[section][_tax_key(alias)] = canonical

    for section in lookup:
        entries = raw.get(section)
        if isinstance(entries, dict):
            for canonical, aliases in entries.items():
                if isinstance(aliases, dict):
                    aliases = aliases.get("aliases") or aliases.get("alias") or []
                register(section, canonical, aliases if isinstance(aliases, list) else [aliases])
        elif isinstance(entries, list):
            for item in entries:
                if isinstance(item, dict):
                    register(section, item.get("canonical", ""), item.get("aliases", []))
                elif isinstance(item, str):
                    register(section, item, [])
    return lookup


def _tax_key(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def normalise_taxonomy(
    values: Optional[Sequence[str]],
    lookup: Dict[str, str],
    *,
    plan: MigrationPlan,
    field: str,
) -> List[str]:
    if not values:
        return []
    output: List[str] = []
    seen: Set[str] = set()
    for raw in values:
        key = _tax_key(raw)
        canonical = lookup.get(key)
        if canonical is None:
            canonical = str(raw)
            plan.unknown_taxonomy[field].add(canonical)
        if canonical not in seen:
            seen.add(canonical)
            output.append(canonical)
    return output


def ensure_comment_id(front_matter: Dict, old_permalink: str) -> str:
    existing = front_matter.get("commentID") or front_matter.get("commentId")
    if existing:
        front_matter["commentID"] = str(existing)
        front_matter.pop("commentId", None)
        return str(existing)
    stable = hashlib.sha1(old_permalink.encode("utf-8")).hexdigest()[:16]
    front_matter["commentID"] = stable
    return stable


def compute_permalink(root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(root)
    if rel.name == INDEX_MD:
        rel = rel.parent
    else:
        rel = rel.with_suffix("")
    return "/" + "/".join(rel.parts) + "/"


def clean_front_matter(data: Dict) -> Dict:
    payload = dict(data or {})
    payload.pop("slug", None)
    return payload


def plan_posts(plan: MigrationPlan, taxonomy_lookup: Dict[str, Dict[str, str]], *, content_root: Path) -> None:
    if not POSTS_ROOT.exists():
        return

    for path in sorted(POSTS_ROOT.rglob("*.md")):
        if path.name == INDEX_MD:
            continue
        try:
            path.relative_to(POSTS_ROOT / "life")
            continue  # handled separately
        except ValueError:
            pass

        raw = load_text(path)
        fm = split_front_matter(raw)
        front_matter = clean_front_matter(fm.data)

        slug_source = fm.data.get("slug") or fm.data.get("title") or path.stem
        slug = plan.ensure_unique_slug(path.parent, slugify(slug_source))

        resources = front_matter.get("resources") or []
        needs_bundle = bool(resources)

        if needs_bundle:
            dest_dir = path.parent / slug
            destination = dest_dir / INDEX_MD
        else:
            dest_dir = path.parent
            destination = path.parent / f"{slug}{MARKDOWN_SUFFIX}"

        front_matter["categories"] = normalise_taxonomy(
            front_matter.get("categories"), taxonomy_lookup["categories"], plan=plan, field="categories"
        )
        front_matter["tags"] = normalise_taxonomy(
            front_matter.get("tags"), taxonomy_lookup["tags"], plan=plan, field="tags"
        )
        series_values = front_matter.get("series")
        if isinstance(series_values, str):
            series_values = [series_values]
        front_matter["series"] = normalise_taxonomy(
            series_values, taxonomy_lookup["series"], plan=plan, field="series"
        )

        old_permalink = compute_permalink(content_root, path)
        new_permalink = compute_permalink(content_root, destination)
        ensure_comment_id(front_matter, old_permalink)

        resource_moves: List[ResourceMove] = []
        if needs_bundle:
            for res in resources:
                src_rel = res.get("src")
                if not src_rel:
                    continue
                source_asset = (path.parent / src_rel).resolve()
                target_asset = (dest_dir / Path(src_rel).name).resolve()
                resource_moves.append(ResourceMove(source=source_asset, destination=target_asset))
                res["src"] = Path(src_rel).name

        plan.add_page(
            PagePlan(
                source=path,
                destination=destination,
                front_matter=front_matter,
                body=fm.body,
                resource_moves=resource_moves,
                notes=["bundle" if needs_bundle else "rename"],
                entry_type="post",
                old_permalink=old_permalink,
                new_permalink=new_permalink,
                old_relpath=path.relative_to(content_root),
                new_relpath=destination.relative_to(content_root),
            )
        )


def plan_life(plan: MigrationPlan, taxonomy_lookup: Dict[str, Dict[str, str]], *, content_root: Path) -> None:
    legacy_life = POSTS_ROOT / "life"
    if not legacy_life.exists():
        return

    for path in sorted(legacy_life.rglob("*.md")):
        if path.name == INDEX_MD:
            continue

        raw = load_text(path)
        fm = split_front_matter(raw)
        front_matter = clean_front_matter(fm.data)

        date_value = str(front_matter.get("date", ""))
        year_match = re.match(r"(\d{4})", date_value)
        year = year_match.group(1) if year_match else "undated"

        slug_source = fm.data.get("slug") or fm.data.get("title") or path.stem
        slug = plan.ensure_unique_slug(LIFE_ROOT / year, slugify(slug_source))

        destination_dir = LIFE_ROOT / year / slug
        destination = destination_dir / INDEX_MD

        front_matter["categories"] = normalise_taxonomy(
            front_matter.get("categories"), taxonomy_lookup["categories"], plan=plan, field="categories"
        )
        front_matter["tags"] = normalise_taxonomy(
            front_matter.get("tags"), taxonomy_lookup["tags"], plan=plan, field="tags"
        )
        series_values = front_matter.get("series")
        if isinstance(series_values, str):
            series_values = [series_values]
        front_matter["series"] = normalise_taxonomy(
            series_values, taxonomy_lookup["series"], plan=plan, field="series"
        )

        old_permalink = compute_permalink(content_root, path)
        new_permalink = compute_permalink(content_root, destination)
        ensure_comment_id(front_matter, old_permalink)

        resources = front_matter.get("resources") or []
        resource_moves: List[ResourceMove] = []
        for res in resources:
            src_rel = res.get("src")
            if not src_rel:
                continue
            source_asset = (path.parent / src_rel).resolve()
            target_asset = (destination_dir / Path(src_rel).name).resolve()
            resource_moves.append(ResourceMove(source=source_asset, destination=target_asset))
            res["src"] = Path(src_rel).name

        plan.add_page(
            PagePlan(
                source=path,
                destination=destination,
                front_matter=front_matter,
                body=fm.body,
                resource_moves=resource_moves,
                notes=["life"],
                entry_type="life",
                old_permalink=old_permalink,
                new_permalink=new_permalink,
                old_relpath=path.relative_to(content_root),
                new_relpath=destination.relative_to(content_root),
            )
        )

    plan.obsolete_directories.add(legacy_life)


def plan_books(plan: MigrationPlan, *, content_root: Path) -> None:
    if not BOOKS_ROOT.exists():
        return

    for path in sorted(BOOKS_ROOT.rglob("*.md")):
        raw = load_text(path)
        fm = split_front_matter(raw)
        front_matter = clean_front_matter(fm.data)

        relative = path.relative_to(BOOKS_ROOT)
        destination = SERIES_ROOT / relative

        plan.add_page(
            PagePlan(
                source=path,
                destination=destination,
                front_matter=front_matter,
                body=fm.body,
                notes=["series"],
                entry_type="series",
                old_permalink=compute_permalink(content_root, path),
                new_permalink=compute_permalink(content_root, destination),
                old_relpath=path.relative_to(content_root),
                new_relpath=destination.relative_to(content_root),
            )
        )

    plan.obsolete_directories.add(BOOKS_ROOT)


def build_permalink_map(plan: MigrationPlan) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for page in plan.pages:
        if not page.old_permalink or not page.new_permalink:
            continue
        old = page.old_permalink.rstrip("/")
        new = page.new_permalink.rstrip("/")
        mapping[old] = new
        mapping[old + "/"] = new + "/"
    return mapping


def rewrite_urls(text: str, permalink_map: Dict[str, str]) -> Tuple[str, List[Tuple[str, str]]]:
    if not permalink_map:
        return text, []

    updates: List[Tuple[str, str]] = []
    pieces: List[str] = []
    last_idx = 0

    for match in INTERNAL_URL_PATTERN.finditer(text):
        url = match.group(0)
        base, anchor = _split_anchor(url)
        base, query = _split_query(base)
        candidates = [base, base.rstrip("/"), base + "/", base.rstrip("/") + "/"]
        replacement_base = None
        for candidate in candidates:
            replacement_base = permalink_map.get(candidate)
            if replacement_base:
                break
        if not replacement_base:
            continue
        new_url = replacement_base
        if not base.endswith("/") and replacement_base.endswith("/") and not query and not anchor:
            new_url = replacement_base.rstrip("/")
        if base.endswith("/") and not replacement_base.endswith("/"):
            new_url = replacement_base + "/"
        if query:
            new_url = f"{new_url}?{query}"
        if anchor:
            new_url = f"{new_url}#{anchor}"
        updates.append((url, new_url))
        pieces.append(text[last_idx : match.start()])
        pieces.append(new_url)
        last_idx = match.end()

    if not updates:
        return text, []

    pieces.append(text[last_idx:])
    return "".join(pieces), updates


def _split_anchor(url: str) -> Tuple[str, Optional[str]]:
    if "#" not in url:
        return url, None
    base, fragment = url.split("#", 1)
    return base, fragment


def _split_query(url: str) -> Tuple[str, Optional[str]]:
    if "?" not in url:
        return url, None
    base, query = url.split("?", 1)
    return base, query


def rewrite_links(plan: MigrationPlan, *, content_root: Path) -> None:
    permalink_map = build_permalink_map(plan)
    if not permalink_map:
        return

    planned_sources = {page.source for page in plan.pages}

    for page in plan.pages:
        updated_body, replacements = rewrite_urls(page.body, permalink_map)
        if replacements:
            page.body = updated_body
            for old, new in replacements:
                plan.link_rewrites.append((page.destination, old, new))

    for path in sorted(content_root.rglob("*.md")):
        if path in planned_sources:
            continue
        raw = load_text(path)
        updated, replacements = rewrite_urls(raw, permalink_map)
        if replacements:
            plan.rewrites.append(FileRewrite(path=path, updated_content=updated, rewrites=replacements))
            for old, new in replacements:
                plan.link_rewrites.append((path, old, new))


def update_config_json(plan: MigrationPlan, *, content_root: Path, dry_run: bool) -> None:
    config_path = POSTS_ROOT / "config.json"
    if not config_path.exists():
        return

    try:
        config_data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MigrationError(f"Unable to parse {config_path}: {exc}")

    posts_root = POSTS_ROOT.resolve()
    content_root_resolved = content_root.resolve()

    def remap_path(raw_value: str) -> Tuple[str, bool]:
        candidate = Path(raw_value)
        base = (posts_root / candidate).resolve()
        try:
            rel_to_content = base.relative_to(content_root_resolved)
        except ValueError:
            return raw_value, False
        new_rel = plan.path_mapping.get(rel_to_content)
        if not new_rel:
            return raw_value, False
        new_abs = (content_root_resolved / new_rel).resolve()
        rel_to_posts = os.path.relpath(new_abs, posts_root)
        if not rel_to_posts.startswith("."):
            rel_to_posts = f"./{rel_to_posts}"
        formatted = Path(rel_to_posts).as_posix()
        return formatted, formatted != raw_value

    changed = False
    for section in ("alias", "refrence"):
        block = config_data.get(section)
        if not isinstance(block, dict):
            continue
        updated_block = {}
        for key, value in block.items():
            new_key, key_changed = remap_path(key)
            if isinstance(value, list):
                new_list = []
                list_changed = False
                for item in value:
                    new_item, item_changed = remap_path(item)
                    new_list.append(new_item)
                    list_changed = list_changed or item_changed
                updated_block[new_key] = new_list
                changed = changed or key_changed or list_changed
            else:
                new_value, value_changed = remap_path(str(value))
                updated_block[new_key] = new_value
                changed = changed or key_changed or value_changed
        config_data[section] = updated_block

    if changed:
        payload = json.dumps(config_data, indent=4, sort_keys=True, ensure_ascii=False)
        if not dry_run:
            safe_backup(config_path)
            config_path.write_text(payload + "\n", encoding="utf-8")


def apply_plan(plan: MigrationPlan, *, dry_run: bool) -> None:
    if not plan.pages and not plan.rewrites:
        print("Nothing to do.")
        return

    for page in plan.pages:
        print(page.summary())
        if dry_run:
            continue

        safe_backup(page.source)
        if page.destination.exists() and page.destination != page.source:
            safe_backup(page.destination)

        page.destination.parent.mkdir(parents=True, exist_ok=True)
        write_text(page.destination, render_markdown(page.front_matter, page.body))

        if page.destination != page.source and page.source.exists():
            try:
                page.source.unlink()
            except IsADirectoryError:
                shutil.rmtree(page.source)

        for res in page.resource_moves:
            if not res.source.exists():
                continue
            safe_backup(res.source)
            res.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(res.source), str(res.destination))

    for rewrite in plan.rewrites:
        print(f"rewrite: {rewrite.path}")
        if dry_run:
            continue
        safe_backup(rewrite.path)
        write_text(rewrite.path, rewrite.updated_content)

    if not dry_run:
        for directory in plan.obsolete_directories:
            if directory.exists():
                shutil.rmtree(directory)

    if plan.link_rewrites:
        print("\nLink rewrites performed:")
        for path, old, new in plan.link_rewrites:
            print(f"  {path}: {old} -> {new}")

    if plan.unknown_taxonomy:
        print("\nUnknown taxonomy values detected:")
        for field, values in plan.unknown_taxonomy.items():
            if values:
                joined = ", ".join(sorted(values))
                print(f"  {field}: {joined}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate MoonWonder Hugo content")
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT_PATH, help="Optional audit report (JSON or YAML)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", dest="dry_run", action="store_true", help="Show the planned operations (default)")
    mode.add_argument("--apply", dest="apply", action="store_true", help="Apply the planned operations")
    parser.add_argument("--content-root", type=Path, default=CONTENT_ROOT, help="Content root (defaults to ./content)")
    parser.add_argument("--taxonomy-map", type=Path, default=TAXONOMY_MAP_PATH, help="Taxonomy alias map")
    parser.add_argument("--log", type=Path, help="Optional path to write the migration log")
    return parser.parse_args(argv)


def load_audit(path: Path) -> Dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        if path.suffix in {".yaml", ".yml"}:
            return yaml.safe_load(text) or {}
        return json.loads(text)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise MigrationError(f"Failed to parse audit report at {path}: {exc}")


def write_log(plan: MigrationPlan, audit: Dict, log_path: Path) -> None:
    lines: List[str] = []
    if audit:
        lines.append("# Audit report keys")
        lines.append(", ".join(sorted(audit.keys())))
        lines.append("")

    lines.append("# Planned page operations")
    for page in plan.pages:
        lines.append(f"- {page.summary()}")

    if plan.link_rewrites:
        lines.append("")
        lines.append("# Link rewrites")
        for path, old, new in plan.link_rewrites:
            lines.append(f"- {path}: {old} -> {new}")

    if plan.unknown_taxonomy:
        lines.append("")
        lines.append("# Unknown taxonomy values")
        for field, values in plan.unknown_taxonomy.items():
            if values:
                joined = ", ".join(sorted(values))
                lines.append(f"- {field}: {joined}")

    write_text(log_path, "\n".join(lines) + "\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    dry_run = not args.apply

    taxonomy_lookup = load_taxonomy_map(args.taxonomy_map)
    audit = load_audit(args.audit)
    if audit:
        print(f"Loaded audit report with keys: {', '.join(sorted(audit.keys()))}")

    plan = MigrationPlan()

    plan_posts(plan, taxonomy_lookup, content_root=args.content_root)
    plan_life(plan, taxonomy_lookup, content_root=args.content_root)
    plan_books(plan, content_root=args.content_root)

    rewrite_links(plan, content_root=args.content_root)
    update_config_json(plan, content_root=args.content_root, dry_run=dry_run)

    if args.log:
        write_log(plan, audit, args.log)

    apply_plan(plan, dry_run=dry_run)

    if dry_run:
        print("\nDry run complete. Re-run with --apply to apply the migration.")
    else:
        print("\nMigration completed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
