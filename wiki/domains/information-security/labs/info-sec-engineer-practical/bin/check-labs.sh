#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

for script in "$ROOT_DIR"/bin/*.sh "$ROOT_DIR"/labs/*/run.sh; do
  [ -f "$script" ] || continue
  sh -n "$script"
  printf 'syntax ok: %s\n' "${script#$ROOT_DIR/}"
done

printf 'All lab scripts passed shell syntax checks.\n'
