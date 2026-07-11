#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
LAB_ROOT="$ROOT_DIR/labs"

usage() {
  printf 'Usage: %s all|LAB_ID\n' "$0"
}

clean_one() {
  lab="$1"
  dir="$LAB_ROOT/$lab"
  if [ ! -d "$dir" ]; then
    printf 'Unknown lab: %s\n' "$lab" >&2
    exit 1
  fi
  sandbox="$dir/.sandbox"
  case "$sandbox" in
    "$LAB_ROOT"/*/.sandbox) rm -rf "$sandbox" ;;
    *) printf 'Refusing unsafe cleanup path: %s\n' "$sandbox" >&2; exit 1 ;;
  esac
  printf 'Cleaned %s\n' "$lab"
}

if [ "${1:-}" = "" ]; then
  usage
  exit 1
fi

if [ "$1" = "all" ]; then
  for dir in "$LAB_ROOT"/*; do
    [ -d "$dir" ] || continue
    clean_one "$(basename "$dir")"
  done
else
  clean_one "$1"
fi
