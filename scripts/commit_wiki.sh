#!/usr/bin/env bash
# commit_wiki.sh — wiki/ 변경 commit 시 author=swan-bot + subject [wiki-bot] prefix 자동 적용.
# Panel A C5c 결정. cs/, development/ 등 read-only 영역 변경 거부.
#
# 사용:
#   bash scripts/commit_wiki.sh "feat(wiki): ingest mixtral paper"
#
# 또는 alias:
#   alias wcommit='bash $(git rev-parse --show-toplevel)/scripts/commit_wiki.sh'
#
# git config 영구 설정 (옵션 — 한 번만):
#   git config user.email "bot@kurnell.local"

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

SUBJECT="${1:-}"
if [[ -z "$SUBJECT" ]]; then
  echo "Usage: $0 <commit subject>" >&2
  exit 2
fi

# Subject prefix 강제
if [[ "$SUBJECT" != "["*"]"* ]]; then
  SUBJECT="[wiki-bot] $SUBJECT"
fi

# Stage 분석 — read-only 영역 변경 차단
READONLY_DIRS=(cs/ development/ coding-test/ lang/ tools/)
STAGED_FILES=$(git diff --cached --name-only)

if [[ -z "$STAGED_FILES" ]]; then
  echo "ERROR: staged 변경 없음. 'git add' 먼저." >&2
  exit 1
fi

VIOLATIONS=()
for file in $STAGED_FILES; do
  for ro_dir in "${READONLY_DIRS[@]}"; do
    if [[ "$file" == "$ro_dir"* ]]; then
      VIOLATIONS+=("$file (in $ro_dir)")
    fi
  done
done

if (( ${#VIOLATIONS[@]} > 0 )); then
  echo "ERROR: LLM write scope 위반 — read-only 영역에 staged 변경:" >&2
  printf '  - %s\n' "${VIOLATIONS[@]}" >&2
  echo "" >&2
  echo "read-only 영역 (cs/, development/, coding-test/, lang/, tools/) 은" >&2
  echo "사람 직접 commit 으로만 변경 가능 (swan author, 별도 commit)." >&2
  exit 1
fi

# Commit — author 만 swan-bot, email 은 git config 그대로
GIT_AUTHOR="swan-bot <bot@kurnell.local>"

git -c "user.name=swan-bot" -c "user.email=bot@kurnell.local" \
  commit -m "$SUBJECT" --author="$GIT_AUTHOR"

echo "" >&2
echo "✓ wiki/ commit 완료. author=swan-bot, subject prefix=[wiki-bot]" >&2
