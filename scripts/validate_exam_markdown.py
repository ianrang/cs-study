#!/usr/bin/env python3
"""Validate restored information-security exam markdown files.

This validator is intentionally strict for final `기출문제.md` files:
100 numbered questions, 4 choices per question, one answer field per question,
and 5 subject headings. Candidate/reconstruction notes should fail this check
until they are promoted to final exam documents.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SUBJECT_RE = re.compile(r"^## \d과목 ", re.M)
QUESTION_RE = re.compile(r"^### (\d+)\. ", re.M)
ANSWER_RE = re.compile(r"^\*\*정답\*\*:\s*(.+)$", re.M)
CHOICE_RE = re.compile(r"^([1-4])\. ", re.M)
FENCE_RE = re.compile(r"```.*?```", re.S)


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("", text)


def question_blocks(text: str) -> list[tuple[int, str]]:
    stripped = strip_fenced_code(text)
    blocks: list[tuple[int, str]] = []
    for match in re.finditer(r"^### (\d+)\. .*?(?=^### \d+\. |\Z)", stripped, re.M | re.S):
        blocks.append((int(match.group(1)), match.group(0)))
    return blocks


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    questions = [int(m.group(1)) for m in QUESTION_RE.finditer(strip_fenced_code(text))]
    missing = [n for n in range(1, 101) if n not in questions]
    duplicates = sorted({n for n in questions if questions.count(n) > 1})

    if len(questions) != 100:
        errors.append(f"expected 100 questions, found {len(questions)}")
    if missing:
        errors.append(f"missing questions: {missing}")
    if duplicates:
        errors.append(f"duplicate questions: {duplicates}")

    subject_count = len(SUBJECT_RE.findall(text))
    if subject_count != 5:
        errors.append(f"expected 5 subject headings, found {subject_count}")

    for num, block in question_blocks(text):
        choices = CHOICE_RE.findall(block)
        answers = ANSWER_RE.findall(block)
        if choices != ["1", "2", "3", "4"]:
            errors.append(f"question {num}: expected choices 1..4, found {choices}")
        if len(answers) != 1:
            errors.append(f"question {num}: expected one answer field, found {len(answers)}")
        elif not re.fullmatch(r"[1-4](?:\s*,\s*[1-4])*", answers[0].strip()):
            errors.append(f"question {num}: invalid answer format {answers[0]!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    failed = False
    for path in args.paths:
        errors = validate_file(path)
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
