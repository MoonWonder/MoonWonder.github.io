#!/usr/bin/env python3
"""Content audit utility for MoonWonder's Hugo site."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import frontmatter
import tomlkit
import yaml

# Supported markdown extensions
MARKDOWN_EXTENSIONS = {".md", ".markdown", ".mdown", ".mkd"}

LANGUAGE_SUFFIX_RE = re.compile(r"\.(?P<lang>[a-z]{2}(?:-[a-z]{2})?)\.(?:md|markdown|mdown|mkd)$", re.IGNORECASE)
LANGUAGE_DIR_RE = re.compile(r"^[a-z]{2}(?:-[a-z]{2})?$", re.IGNORECASE)


@dataclass
class Issue:
    """Represents a single audit issue discovered for a file."""

    severity: str
    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "details": sanitize_for_json(self.details),
        }


@dataclass
class FileReport:
    """Describes the audit outcome for a single markdown file."""

    path: Path
    relative_path: str
    language: str
    language_variants: Sequence[str]
    content_type: str
    word_count: int
    prospective_url: Optional[str]
    current_url: Optional[str]
    slug: Optional[str]
    metadata_summary: Dict[str, Any]
    issues: List[Issue] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": str(self.path),
            "relative_path": self.relative_path,
            "language": self.language,
            "language_variants": list(self.language_variants),
            "content_type": self.content_type,
            "word_count": self.word_count,
            "prospective_url": self.prospective_url,
            "current_url": self.current_url,
            "slug": self.slug,
            "metadata": sanitize_for_json(self.metadata_summary),
            "issues": [issue.to_dict() for issue in self.issues],
        }

    @property
    def error_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for issue in self.issues if issue.severity == "WARNING")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Hugo markdown content")
    parser.add_argument(
        "--content-root",
        default="content",
        help="Root directory containing site content (default: content)",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory to write audit reports into (default: reports)",
    )
    parser.add_argument(
        "--json-output",
        help="Override path for JSON report (defaults to reports/content_audit.json)",
    )
    parser.add_argument(
        "--csv-output",
        help="Override path for CSV report (defaults to reports/content_audit.csv)",
    )
    parser.add_argument(
        "--taxonomy-map",
        help="Optional path to a taxonomy canonical map (YAML/TOML/JSON)",
    )
    parser.add_argument(
        "--default-language",
        help="Override default content language from config",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the audit without writing any report files",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors for exit codes",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with a non-zero status code when violations are found",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    content_root = Path(args.content_root).resolve()
    if not content_root.exists():
        print(f"error: content root '{content_root}' does not exist", file=sys.stderr)
        return 2

    reports_dir = Path(args.reports_dir).resolve()
    if args.json_output:
        json_output = Path(args.json_output).resolve()
    else:
        json_output = reports_dir / "content_audit.json"

    if args.csv_output:
        csv_output = Path(args.csv_output).resolve()
    else:
        csv_output = reports_dir / "content_audit.csv"

    project_root = Path(__file__).resolve().parents[1]
    default_language = (
        args.default_language
        or detect_default_language(project_root / "config" / "_default")
        or "en"
    )

    taxonomy_map = load_taxonomy_map(args.taxonomy_map) if args.taxonomy_map else {}

    reports: List[FileReport] = []
    duplicates: Dict[str, List[FileReport]] = {}

    for file_path in sorted(iter_markdown_files(content_root)):
        report = audit_file(
            file_path=file_path,
            content_root=content_root,
            default_language=default_language,
            taxonomy_map=taxonomy_map,
        )
        reports.append(report)
        if report.prospective_url:
            duplicates.setdefault(report.prospective_url, []).append(report)

    register_duplicate_permalinks(duplicates)

    summary = build_summary(reports)

    if not args.dry_run:
        ensure_parent(json_output)
        ensure_parent(csv_output)
        write_json_report(json_output, reports, summary)
        write_csv_report(csv_output, reports)

    print_summary(summary, json_output, csv_output, args.dry_run)

    exit_code = 0
    if args.check:
        has_errors = summary["issues"].get("ERROR", 0) > 0
        has_warnings = summary["issues"].get("WARNING", 0) > 0
        if has_errors or (args.strict and has_warnings):
            exit_code = 1

    return exit_code


def iter_markdown_files(content_root: Path) -> Iterable[Path]:
    for path in content_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in MARKDOWN_EXTENSIONS:
            yield path


def audit_file(
    file_path: Path,
    content_root: Path,
    default_language: str,
    taxonomy_map: Dict[str, Set[str]],
) -> FileReport:
    relative_path = file_path.relative_to(content_root).as_posix()
    issues: List[Issue] = []
    metadata: Dict[str, Any] = {}
    content_body = ""

    try:
        with file_path.open("r", encoding="utf-8") as fh:
            post = frontmatter.load(fh)
        metadata = post.metadata or {}
        content_body = post.content or ""
    except Exception as exc:  # pylint: disable=broad-except
        issues.append(
            Issue(
                severity="ERROR",
                code="frontmatter_parse_error",
                message=f"Failed to parse front matter: {exc}",
            )
        )
        try:
            content_body = file_path.read_text(encoding="utf-8")
        except Exception:  # pragma: no cover - best effort fallback
            content_body = ""
        metadata = {}

    language = detect_language(file_path, metadata, default_language)
    language_variants = sorted(infer_metadata_languages(metadata))
    word_count = compute_word_count(content_body)

    content_type = determine_content_type(relative_path)
    filename = file_path.name
    is_branch_index = filename == "_index.md"
    is_leaf_index = filename == "index.md"

    title_value = metadata.get("title")
    if not has_valid_title(title_value):
        issues.append(
            Issue(
                severity="ERROR",
                code="missing_title",
                message="Title is missing or empty",
            )
        )

    parsed_date = parse_date(metadata.get("date"))
    requires_date = content_type in {"posts", "life"} and not is_branch_index
    if requires_date and not parsed_date:
        issues.append(
            Issue(
                severity="ERROR",
                code="missing_date",
                message="Date is required for this content type",
            )
        )

    taxonomy_summary: Dict[str, List[str]] = {}
    for taxonomy_name in ("tags", "categories"):
        raw_value = metadata.get(taxonomy_name)
        normalized_terms, taxonomy_issues = validate_taxonomy_field(
            taxonomy_name, raw_value, taxonomy_map.get(taxonomy_name)
        )
        taxonomy_summary[taxonomy_name] = normalized_terms
        issues.extend(taxonomy_issues)

    slug_value = metadata.get("slug")
    slug = determine_slug(
        slug_value=slug_value,
        file_path=file_path,
        is_leaf_index=is_leaf_index,
        title_value=title_value,
    )

    if slug_value and content_type in {"posts", "life"}:
        issues.append(
            Issue(
                severity="WARNING",
                code="deprecated_slug",
                message="Slug field is deprecated for posts and life entries",
            )
        )

    current_url = build_current_url(
        relative_path=relative_path,
        is_branch_index=is_branch_index,
        is_leaf_index=is_leaf_index,
    )
    prospective_url, permalink_issue = compute_prospective_url(
        content_type=content_type,
        relative_path=relative_path,
        slug=slug,
        parsed_date=parsed_date,
        is_branch_index=is_branch_index,
    )
    if permalink_issue:
        issues.append(permalink_issue)

    if prospective_url and current_url and prospective_url != current_url:
        issues.append(
            Issue(
                severity="WARNING",
                code="permalink_conflict",
                message="Current path does not match prospective canonical permalink",
                details={"current": current_url, "prospective": prospective_url},
            )
        )

    metadata_summary = {
        "title": title_value,
        "date": parsed_date,
        "lastmod": metadata.get("lastmod"),
        "tags": taxonomy_summary.get("tags"),
        "categories": taxonomy_summary.get("categories"),
        "slug": slug_value,
        "draft": metadata.get("draft"),
    }

    return FileReport(
        path=file_path,
        relative_path=relative_path,
        language=language,
        language_variants=language_variants,
        content_type=content_type,
        word_count=word_count,
        prospective_url=prospective_url,
        current_url=current_url,
        slug=slug,
        metadata_summary=metadata_summary,
        issues=issues,
    )


def determine_content_type(relative_path: str) -> str:
    parts = relative_path.split("/")
    if not parts:
        return "page"
    first = parts[0]
    if first == "posts":
        if len(parts) > 1 and parts[1] == "life":
            return "life"
        return "posts"
    if first == "life":
        return "life"
    return first if len(parts) > 1 else "page"


def has_valid_title(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, dict):
        return any(str(v).strip() for v in value.values())
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return any(str(v).strip() for v in value)
    return bool(str(value).strip())


def parse_date(value: Any) -> Optional[dt.datetime]:
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time.min)
    if isinstance(value, str) and value.strip():
        candidate = value.strip()
        try:
            return dt.datetime.fromisoformat(candidate.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def validate_taxonomy_field(
    taxonomy_name: str,
    value: Any,
    allowed_terms: Optional[Set[str]],
) -> Tuple[List[str], List[Issue]]:
    issues: List[Issue] = []
    normalized: List[str] = []

    if value in (None, ""):
        issues.append(
            Issue(
                severity="ERROR",
                code=f"missing_{taxonomy_name}",
                message=f"{taxonomy_name.title()} field is required and must be a non-empty list",
            )
        )
        return normalized, issues

    if not isinstance(value, (list, tuple, set)):
        issues.append(
            Issue(
                severity="ERROR",
                code=f"invalid_{taxonomy_name}",
                message=f"{taxonomy_name.title()} field must be a list",
            )
        )
        return normalized, issues

    for term in value:
        if term in (None, ""):
            continue
        normalized_term = str(term).strip()
        if not normalized_term:
            continue
        normalized.append(normalized_term)
        if allowed_terms is not None and normalized_term not in allowed_terms:
            issues.append(
                Issue(
                    severity="WARNING",
                    code="unknown_taxonomy_term",
                    message=f"Term '{normalized_term}' is not present in the canonical {taxonomy_name} map",
                    details={"taxonomy": taxonomy_name, "term": normalized_term},
                )
            )

    if not normalized:
        issues.append(
            Issue(
                severity="ERROR",
                code=f"empty_{taxonomy_name}",
                message=f"{taxonomy_name.title()} list must contain at least one value",
            )
        )

    return normalized, issues


def determine_slug(
    slug_value: Any,
    file_path: Path,
    is_leaf_index: bool,
    title_value: Any,
) -> Optional[str]:
    if isinstance(slug_value, str) and slug_value.strip():
        return slugify(slug_value)
    if is_leaf_index:
        return slugify(file_path.parent.name)
    candidate = file_path.stem
    if candidate in {"index", "_index"}:
        candidate = file_path.parent.name
    slug = slugify(candidate)
    if slug:
        return slug
    if isinstance(title_value, str):
        return slugify(title_value)
    if isinstance(title_value, dict):
        for variant in title_value.values():
            if isinstance(variant, str) and variant.strip():
                slug_candidate = slugify(variant)
                if slug_candidate:
                    return slug_candidate
    return None


def build_current_url(
    relative_path: str,
    is_branch_index: bool,
    is_leaf_index: bool,
) -> Optional[str]:
    parts = relative_path.split("/")
    if not parts:
        return None

    if is_branch_index or is_leaf_index:
        parts = parts[:-1]
    else:
        parts[-1] = Path(parts[-1]).stem

    if parts and parts[0] == "posts":
        parts = parts[1:]

    cleaned_parts = [slugify(part) for part in parts if part]
    if not cleaned_parts:
        return "/"
    return "/" + "/".join(cleaned_parts) + "/"


def compute_prospective_url(
    content_type: str,
    relative_path: str,
    slug: Optional[str],
    parsed_date: Optional[dt.datetime],
    is_branch_index: bool,
) -> Tuple[Optional[str], Optional[Issue]]:
    if is_branch_index:
        # Branch bundles represent sections; future canonical handling deferred.
        return None, None

    if not slug:
        return None, Issue(
            severity="ERROR",
            code="missing_slug",
            message="Unable to determine a slug for this document",
        )

    if content_type == "life":
        if not parsed_date:
            return None, Issue(
                severity="ERROR",
                code="missing_date",
                message="Life entries require a valid date to infer canonical permalink",
            )
        year = parsed_date.year
        return f"/life/{year}/{slug}/", None

    if content_type == "posts":
        parts = relative_path.split("/")
        # remove leading 'posts' and filename
        sections = parts[1:-1]
        section_slugs = [slugify(part) for part in sections if part]
        return "/" + "/".join(section_slugs + [slug]) + "/", None

    # default: mirror current structure without filename extension
    current_url = build_current_url(relative_path, False, False)
    return current_url, None


def register_duplicate_permalinks(duplicates: Dict[str, List[FileReport]]) -> None:
    for url, entries in duplicates.items():
        if not url or len(entries) < 2:
            continue
        for report in entries:
            report.issues.append(
                Issue(
                    severity="ERROR",
                    code="duplicate_permalink",
                    message=f"Prospective URL '{url}' is duplicated",
                )
            )


def build_summary(reports: Sequence[FileReport]) -> Dict[str, Any]:
    total_files = len(reports)
    issue_totals: Dict[str, int] = {"ERROR": 0, "WARNING": 0}
    for report in reports:
        issue_totals["ERROR"] += report.error_count
        issue_totals["WARNING"] += report.warning_count
    return {
        "generated_at": dt.datetime.utcnow().isoformat() + "Z",
        "total_files": total_files,
        "issues": issue_totals,
    }


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json_report(path: Path, reports: Sequence[FileReport], summary: Dict[str, Any]) -> None:
    payload = {
        "summary": summary,
        "files": [report.to_dict() for report in reports],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_csv_report(path: Path, reports: Sequence[FileReport]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "relative_path",
                "language",
                "language_variants",
                "content_type",
                "word_count",
                "prospective_url",
                "current_url",
                "slug",
                "issue_severity",
                "issue_code",
                "issue_message",
            ]
        )
        for report in reports:
            if report.issues:
                for issue in report.issues:
                    writer.writerow(
                        [
                            report.relative_path,
                            report.language,
                            ";".join(report.language_variants),
                            report.content_type,
                            report.word_count,
                            report.prospective_url or "",
                            report.current_url or "",
                            report.slug or "",
                            issue.severity,
                            issue.code,
                            issue.message,
                        ]
                    )
            else:
                writer.writerow(
                    [
                        report.relative_path,
                        report.language,
                        ";".join(report.language_variants),
                        report.content_type,
                        report.word_count,
                        report.prospective_url or "",
                        report.current_url or "",
                        report.slug or "",
                        "OK",
                        "",
                        "",
                    ]
                )


def print_summary(summary: Dict[str, Any], json_output: Path, csv_output: Path, dry_run: bool) -> None:
    errors = summary["issues"].get("ERROR", 0)
    warnings = summary["issues"].get("WARNING", 0)
    print(f"Audited {summary['total_files']} markdown files")
    print(f"Errors: {errors}  Warnings: {warnings}")
    if dry_run:
        print("Dry run enabled; reports were not written")
    else:
        print(f"JSON report: {json_output}")
        print(f"CSV report: {csv_output}")


def detect_default_language(config_dir: Path) -> Optional[str]:
    config_file = config_dir / "hugo.toml"
    if not config_file.exists():
        return None
    try:
        content = config_file.read_text(encoding="utf-8")
        data = tomlkit.parse(content)
    except Exception:  # pylint: disable=broad-except
        return None
    default_lang = data.get("defaultContentLanguage")
    if isinstance(default_lang, str) and default_lang.strip():
        return default_lang.strip()
    return None


def load_taxonomy_map(path: str) -> Dict[str, Set[str]]:
    file_path = Path(path).resolve()
    if not file_path.exists():
        print(f"warning: taxonomy map '{file_path}' not found; skipping taxonomy validation")
        return {}

    ext = file_path.suffix.lower()
    try:
        if ext in {".yaml", ".yml"}:
            raw = yaml.safe_load(file_path.read_text(encoding="utf-8"))
        elif ext == ".toml":
            raw = tomlkit.parse(file_path.read_text(encoding="utf-8"))
        elif ext == ".json":
            raw = json.loads(file_path.read_text(encoding="utf-8"))
        else:
            print(f"warning: unsupported taxonomy map format '{ext}'; expected YAML/TOML/JSON")
            return {}
    except Exception as exc:  # pylint: disable=broad-except
        print(f"warning: failed to parse taxonomy map '{file_path}': {exc}")
        return {}

    return normalise_taxonomy_map(raw)


def normalise_taxonomy_map(raw: Any) -> Dict[str, Set[str]]:
    if not isinstance(raw, dict):
        return {}

    result: Dict[str, Set[str]] = {}
    for taxonomy, value in raw.items():
        terms = flatten_terms(value)
        if terms:
            result[str(taxonomy)] = terms
    return result


def flatten_terms(value: Any) -> Set[str]:
    terms: Set[str] = set()
    if value is None:
        return terms
    if isinstance(value, str):
        if value.strip():
            terms.add(value.strip())
        return terms
    if isinstance(value, (list, tuple, set)):
        for item in value:
            terms.update(flatten_terms(item))
        return terms
    if isinstance(value, dict):
        for item in value.values():
            if isinstance(item, str):
                if item.strip():
                    terms.add(item.strip())
                continue
            if isinstance(item, dict):
                for attr in ("canonical", "slug", "name", "value"):
                    attr_value = item.get(attr)
                    if isinstance(attr_value, str) and attr_value.strip():
                        terms.add(attr_value.strip())
                terms.update(flatten_terms(item))
                continue
            terms.update(flatten_terms(item))
        if not terms:
            terms.update(str(k).strip() for k in value.keys() if str(k).strip())
        return terms
    terms.add(str(value))
    return terms


def detect_language(file_path: Path, metadata: Dict[str, Any], default_language: str) -> str:
    for key in ("language", "lang"):
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    languages = metadata.get("languages")
    if isinstance(languages, (list, tuple)):
        for value in languages:
            if isinstance(value, str) and value.strip():
                return value.strip()

    match = LANGUAGE_SUFFIX_RE.search(file_path.name)
    if match:
        return match.group("lang")

    for part in reversed(file_path.parts[:-1]):
        if LANGUAGE_DIR_RE.match(part):
            return part

    return default_language


def infer_metadata_languages(metadata: Dict[str, Any]) -> Set[str]:
    languages: Set[str] = set()
    for key in ("title", "summary", "description"):
        value = metadata.get(key)
        if isinstance(value, dict):
            for lang_code, text in value.items():
                if isinstance(lang_code, str) and isinstance(text, str) and text.strip():
                    languages.add(lang_code.strip())
    return languages


def compute_word_count(text: str) -> int:
    if not text:
        return 0
    latin_tokens = re.findall(r"[A-Za-z0-9']+", text)
    cjk_tokens = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\u3400-\u4dbf\uac00-\ud7af]", text)
    return len(latin_tokens) + len(cjk_tokens)


def slugify(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKD", str(value)).strip()
    if not text:
        return ""
    text = text.replace(" ", "-")
    text = re.sub(r"[\s·]+", "-", text, flags=re.UNICODE)
    text = re.sub(r"[^\w\-]+", "-", text, flags=re.UNICODE)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-_")
    return text.lower()


def sanitize_for_json(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): sanitize_for_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [sanitize_for_json(v) for v in value]
    return str(value)


if __name__ == "__main__":
    sys.exit(main())
