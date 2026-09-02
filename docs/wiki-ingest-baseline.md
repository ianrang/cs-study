# Knowledge Pipeline Implementation Baseline

## Scope

- Task: `KNOWLEDGE-PIPELINE-IMPL-001`
- Extractor repository: `007_youtube-script` at `75a9bbd4bf099c69a5529b0ec8c94f5be9a14294`
- Vault repository: `001_cs-study` at `c7c1d919aad0fa1f9ef7713f0577161ab0a1a595`
- Worktrees: isolated `feat/knowledge-pipeline` branches
- Original dirty worktrees: excluded from writes and inventory

## Enumeration Contract

- Repository searches include hidden paths.
- Repository file counts exclude `.git/**`; generated caches and virtual environments are excluded when present.
- Wiki inventory is every `wiki/**/*.md` path in the selected vault commit.
- Content inventory excludes `wiki/templates/**` and root `wiki/index.md`, `wiki/overview.md`, `wiki/log.md`.
- Active inventory additionally excludes every path containing `drafts`, `staging`, or `archive`.
- Basename collision inventory groups all wiki Markdown by filename stem; a group has at least two paths.

## Fixed Counts

| Item | Count |
|---|---:|
| extractor non-network tests | 87 passed |
| vault legacy tests | 47 passed |
| vault legacy lint | HIGH 0, MEDIUM 0 |
| wiki Markdown | 123 |
| wiki content | 114 |
| wiki active under the rule above | 103 |
| duplicate basename groups | 6 |
| files in duplicate groups | 31 |
| required CI workflows | 0 |
| pre-commit configuration | 0 |

The earlier design-review snapshot of 138 wiki Markdown files included paths from the original dirty worktree. It is not the migration input selected by the user-approved isolated-HEAD strategy.

## Basename Collision Inventory

| Stem | Paths |
|---|---:|
| `README` | 9 |
| `architecture` | 2 |
| `cleanup` | 6 |
| `expected-observations` | 6 |
| `index` | 2 |
| `questions` | 6 |

The exact path list is generated again by the sequence 6a no-write planner; this baseline fixes the expected group and file cardinalities without authorizing any rename.

## Cross-repository Contract Fixture

Both repositories contain `tests/fixtures/contracts/canonical-transcript-v1.json` with identical bytes.

| Property | Value |
|---|---|
| byte size | 588 |
| SHA-256 | `2e6978b1d8643ca5ab1884403e5225a3ac2178b0f5af9b4509cfa7d5172f0bf4` |

## Known Entry Conditions

- Extractor reverse hook exists at this baseline.
- Extractor and legacy importer each own a separate `1.0` version string.
- Legacy importer still exposes directory variant selection and `--force` pair replacement.
- Target `knowledge.schema.json`, parser, immutable capture, checker, and migration planner do not exist at this baseline.
- Canonical wiki content remains unchanged until the separately approved sequence 6b apply.
