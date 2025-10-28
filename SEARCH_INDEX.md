# Search index schema

The Hugo build now emits language-specific search payloads for Algolia and other
external consumers. Each build produces two JSON files at the project root:

- `public/index.zh-cn.json` — Chinese content only
- `public/index.en.json` — English content only

These files contain flattened page and heading records for their respective
languages. They replace the previous single-language payload and can be uploaded
independently to Algolia indices (`index.zh-cn`, `index.en`).

## Record structure

Every object in the search index exposes the following fields:

| Field       | Type     | Description |
|-------------|----------|-------------|
| `objectID`  | string   | Stable identifier derived from the page permalink. Heading records append positional suffixes so they remain unique. |
| `uri`       | string   | Page URL (or anchored URL for headings). Honors the `absoluteURL` flag configured in `params.search`. |
| `title`     | string   | Page title. |
| `content`   | string   | Snippet of the page or heading contents, stripped of HTML. |
| `date`      | string   | Publication date formatted with `params.dateFormat`. |
| `lang`      | string   | Language code (`.Language.Lang`, e.g. `zh-cn`, `en`). |
| `section`   | string   | Section inferred from `.Section`, falling back to `.Type`. |
| `type`      | string   | Page type (`.Type`). Mirrors `section` when no explicit type exists. |
| `categories`| array    | Normalized list of category terms (empty array when unset). |
| `tags`      | array    | Normalized list of tag terms (empty array when unset). |
| `series`    | array    | Normalized list of series terms (empty array when unset). |

The root-level page record also carries a `content` snippet sourced from the
page description, while heading records reuse the same metadata with anchor
specific URLs.

## Consumption notes

- Update Algolia index settings to point to `index.zh-cn` and `index.en`.
- Existing `objectID` values remain stable for each language, so incremental
  updates continue to work as before.
- Fuse.js consumers can continue to read the JSON payloads directly; the array
  structure and field names remain backward compatible with the previous single
  language index while adding the new metadata columns described above.
