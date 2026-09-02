#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LAB_ROOT="$ROOT_DIR/labs"

usage() {
  printf 'Usage: %s all|LAB_ID\n' "$0"
  printf 'Example: %s 01-linux-hardening\n' "$0"
}

run_one() {
  lab="$1"
  script="$LAB_ROOT/$lab/run.sh"
  if [ ! -f "$script" ]; then
    printf 'Unknown lab: %s\n' "$lab" >&2
    exit 1
  fi
  printf '\n== Running %s ==\n' "$lab"
  (cd "$LAB_ROOT/$lab" && sh ./run.sh)
}

if [ "${1:-}" = "" ]; then
  usage
  exit 1
fi

if [ "$1" = "all" ]; then
  for dir in "$LAB_ROOT"/*; do
    [ -d "$dir" ] || continue
    run_one "$(basename "$dir")"
  done
else
  run_one "$1"
fi
