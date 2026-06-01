#!/usr/bin/env python3
"""Validate information-security exam markdown files.

This validator accepts both complete restored exams and partial restored
question sets. Partial files do not need to expose empty 100-question slots;
they must still keep each captured question auditable.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SUBJECT_RE = re.compile(r"^## (?:\d과목 )?.+", re.M)
QUESTION_RE = re.compile(r"^### (\d+)\. ", re.M)
FENCE_RE = re.compile(r"```.*?```", re.S)
ANSWER_RE = re.compile(r"^\*\*(?:정답|답안)\*\*:?\s*([1-4](?:\s*,\s*[1-4])*)\s*$", re.M)
CHOICE_RE = re.compile(r"^([1-4])\. ", re.M)
BAD_CHOICE_RE = re.compile(r"^[5-9]\. ", re.M)


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def question_blocks(text: str) -> list[tuple[int, str]]:
    stripped = strip_fenced_code(text)
    blocks: list[tuple[int, str]] = []
    for match in re.finditer(r"^### (\d+)\. .*?(?=^### \d+\. |\Z)", stripped, re.M | re.S):
        blocks.append((int(match.group(1)), match.group(0)))
    return blocks


def declared_count(text: str) -> int | None:
    match = re.search(r"^\| (?:문항 수|확보 문항) \| ([0-9]+)(?:\s*/\s*[0-9]+)?문항? \|", text, re.M)
    if match:
        return int(match.group(1))
    return None


def validate_file(path: Path, *, require_complete: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    questions = [int(m.group(1)) for m in QUESTION_RE.finditer(strip_fenced_code(text))]
    duplicates = sorted({n for n in questions if questions.count(n) > 1})

    if not questions:
        errors.append("expected at least 1 question, found 0")
    if require_complete and len(questions) != 100:
        missing = [n for n in range(1, 101) if n not in questions]
        errors.append(f"expected 100 questions, found {len(questions)}")
        if missing:
            errors.append(f"missing questions: {missing}")
    if duplicates:
        errors.append(f"duplicate questions: {duplicates}")

    count = declared_count(text)
    if count is not None and count != len(questions):
        errors.append(f"declared question count {count}, found {len(questions)}")

    subject_count = len(SUBJECT_RE.findall(text))
    if subject_count < 1:
        errors.append("expected at least 1 subject heading")

    for num, block in question_blocks(text):
        choices = CHOICE_RE.findall(block)
        if choices and choices != ["1", "2", "3", "4"]:
            errors.append(f"question {num}: expected choices 1..4, found {choices}")
        bad_choices = BAD_CHOICE_RE.findall(block)
        if bad_choices:
            errors.append(f"question {num}: invalid choice labels {bad_choices}")
        details_count = len(re.findall(r"^<details>", block, re.M))
        answer_count = len(ANSWER_RE.findall(block))
        if details_count != 1:
            errors.append(f"question {num}: expected 1 details block, found {details_count}")
        if answer_count != 1:
            errors.append(f"question {num}: expected 1 answer line, found {answer_count}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.paths:
        errors = validate_file(path, require_complete=args.require_complete)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
