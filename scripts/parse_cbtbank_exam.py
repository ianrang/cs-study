#!/usr/bin/env python3
"""Parse cbtbank.kr exam HTML into structured markdown (stdlib only)."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

SUBJECT_MAP = {
    1: "1과목 시스템 보안",
    2: "2과목 네트워크 보안",
    3: "3과목 애플리케이션 보안",
    4: "4과목 정보보안 일반",
    5: "5과목 정보보안 관리 및 법규",
}


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_exam(html_content: str) -> list[dict]:
    questions: list[dict] = []
    box_pattern = re.compile(
        r'<div[^>]*class="[^"]*exam-box[^"]*"[^>]*question-num="(\d+)"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*<div tabindex="0" class="col-12',
        re.DOTALL,
    )
    # Fallback: split by exam-box markers
    parts = re.split(
        r'<div tabindex="0" class="col-12 col-sm-12 col-md-6 exam-box[^"]*"[^>]*question-num="(\d+)"',
        html_content,
    )
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            num = int(parts[i])
            chunk = parts[i + 1]
            title_m = re.search(
                r'<p class="exam-title"><span class="exam-number">\d+</span>\.\s*(.*?)</p>',
                chunk,
                re.DOTALL,
            )
            ol_m = re.search(
                r'<ol class="circlednumbers" correct="(\d)">(.*?)</ol>',
                chunk,
                re.DOTALL,
            )
            if not title_m or not ol_m:
                continue
            title = clean_text(re.sub(r"<[^>]+>", " ", title_m.group(1)))
            answer = int(ol_m.group(1))
            choices = [
                clean_text(re.sub(r"<[^>]+>", " ", li))
                for li in re.findall(r"<li[^>]*>(.*?)</li>", ol_m.group(2), re.DOTALL)
            ]
            questions.append(
                {"num": num, "title": title, "choices": choices, "answer": answer}
            )
    questions.sort(key=lambda q: q["num"])
    return questions


def to_markdown(
    questions: list[dict],
    *,
    exam_title: str,
    exam_date: str,
    source_url: str,
) -> str:
    lines = [
        f"# {exam_title}",
        "",
        "| 항목 | 내용 |",
        "|------|------|",
        f"| 시험일 | {exam_date} |",
        f"| 출처 | {source_url} |",
        f"| 문항 수 | {len(questions)} |",
        f"| 복원 방식 | cbtbank HTML 파싱 (원문 그대로) |",
        "",
    ]

    current_subject = 0
    for q in questions:
        subject = (q["num"] - 1) // 20 + 1
        if subject != current_subject:
            current_subject = subject
            lines.extend(["", f"## {SUBJECT_MAP[subject]}", ""])

        lines.append(f"### {q['num']}. {q['title']}")
        lines.append("")
        for i, choice in enumerate(q["choices"], start=1):
            lines.append(f"{i}. {choice}")
        if q["answer"]:
            lines.append("")
            lines.append(f"**정답**: {q['answer']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    html_content = args.html_file.read_text(encoding="utf-8", errors="ignore")
    questions = parse_exam(html_content)
    if len(questions) != 100:
        print(f"warning: expected 100 questions, got {len(questions)}", file=sys.stderr)

    md = to_markdown(
        questions,
        exam_title=args.title,
        exam_date=args.date,
        source_url=args.source,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md, encoding="utf-8")
    print(f"wrote {args.output} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
