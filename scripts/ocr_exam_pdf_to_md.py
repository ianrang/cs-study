#!/usr/bin/env python3
"""OCR scanned exam PDF pages and emit markdown (verbatim OCR, no inference)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SUBJECT_MAP = {
    1: "1과목 시스템 보안",
    2: "2과목 네트워크 보안",
    3: "3과목 애플리케이션 보안",
    4: "4과목 정보보안 일반",
    5: "5과목 정보보안 관리 및 법규",
}


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _pillow_crop():
    import sys

    pip_dir = Path(__file__).resolve().parents[1] / ".tmp" / "pip"
    if pip_dir.exists():
        sys.path.insert(0, str(pip_dir))
    from PIL import Image  # type: ignore

    return Image


def ocr_pages(
    pdf: Path, workdir: Path, dpi: int = 400, split_columns: bool = True
) -> list[Path]:
    workdir.mkdir(parents=True, exist_ok=True)
    prefix = workdir / "page"
    run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(prefix)])
    txts: list[Path] = []
    Image = _pillow_crop() if split_columns else None
    for png in sorted(workdir.glob("page-*.png")):
        targets = [png]
        if split_columns and Image is not None:
            im = Image.open(png)
            w, h = im.size
            targets = []
            for side, box in [("L", (0, 0, w // 2, h)), ("R", (w // 2, 0, w, h))]:
                crop_path = workdir / f"{png.stem}-{side}.png"
                im.crop(box).save(crop_path)
                targets.append(crop_path)
        for target in targets:
            out = target.with_suffix(".txt")
            run(
                [
                    "tesseract",
                    str(target),
                    str(out.with_suffix("")),
                    "-l",
                    "kor+eng",
                    "--psm",
                    "6",
                ]
            )
            txts.append(out)
    return txts


def normalize_ocr_question_markers(raw: str) -> str:
    """Fix common OCR misreads of question numbers without inventing content."""
    raw = re.sub(r"\r", "", raw)
    # Known OCR glitches from Baba Yetu 2023 4회 scans (verified in combined-ocr.txt)
    raw = re.sub(r"(?m)^835,", "35.", raw)
    raw = re.sub(r"(?m)^883\.", "83.", raw)
    # "1 첨입" without dot before Korean question stem
    raw = re.sub(r"(?m)^(\d{1,3})\s+(?=[가-힣])", r"\1. ", raw)
    return raw


def _is_garbage_question(title: str) -> bool:
    t = title.strip()
    if not t or len(t) < 8:
        return True
    if t.startswith("<?xml"):
        return True
    if re.fullmatch(r"[\W\d\s]+", t):
        return True
    return False


def parse_questions(raw: str) -> list[dict]:
    """Best-effort split on question numbers; keeps OCR text as-is."""
    raw = normalize_ocr_question_markers(raw)
    chunks = re.split(r"(?<=\n)(?=\d{1,3}\.\s*)", raw)
    questions: list[dict] = []
    for chunk in chunks:
        m = re.match(r"(\d{1,3})\.\s*(.*)", chunk.strip(), re.DOTALL)
        if not m:
            continue
        num = int(m.group(1))
        if num < 1 or num > 100:
            continue
        body = m.group(2).strip()
        lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
        title_lines: list[str] = []
        choices: list[str] = []
        for ln in lines:
            if re.match(r"^[@①②③④⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾]|^\(\d\)|^[①②③④]", ln):
                choices.append(re.sub(r"^[@]\s*", "", ln))
            elif not choices:
                title_lines.append(ln)
            else:
                choices.append(ln)
        if _is_garbage_question(" ".join(title_lines)):
            continue
        questions.append(
            {
                "num": num,
                "title": " ".join(title_lines),
                "choices": choices,
            }
        )
    # dedupe by num keeping longest
    by_num: dict[int, dict] = {}
    for q in questions:
        prev = by_num.get(q["num"])
        if not prev or len(q["title"]) + len("".join(q["choices"])) > len(
            prev["title"]
        ) + len("".join(prev["choices"])):
            by_num[q["num"]] = q
    return [by_num[k] for k in sorted(by_num)]


def to_markdown(
    questions: list[dict],
    *,
    title: str,
    exam_date: str,
    source: str,
    raw_path: Path,
    answers: dict[int, int] | None = None,
) -> str:
    lines = [
        f"# {title}",
        "",
        "| 항목 | 내용 |",
        "|------|------|",
        f"| 시험일 | {exam_date} |",
        f"| 출처 | {source} |",
        f"| 복원 방식 | Baba Yetu PDF 스캔 → Tesseract OCR (원문 OCR 그대로, 추론·보기 보완 없음) |",
        f"| OCR 원문 | `{raw_path}` |",
        f"| 파싱 문항 수 | {len(questions)} / 100 |",
        "",
        "> OCR 2단 PDF 특성상 문항·보기 분리가 불완전할 수 있다. `[미파싱]` 구간은 OCR 원문 파일을 대조할 것.",
        "",
    ]
    parsed_nums = {q["num"] for q in questions}
    current_subject = 0
    for num in range(1, 101):
        subject = (num - 1) // 20 + 1
        if subject != current_subject:
            current_subject = subject
            lines.extend(["", f"## {SUBJECT_MAP[subject]}", ""])
        if num not in parsed_nums:
            lines.extend([f"### {num}. [미파싱 — OCR 원문 대조 필요]", ""])
            continue
        q = next(x for x in questions if x["num"] == num)
        lines.append(f"### {num}. {q['title']}")
        lines.append("")
        if q["choices"]:
            for i, c in enumerate(q["choices"], start=1):
                lines.append(f"{i}. {c}")
        else:
            lines.append("*(보기 OCR 미분리 — 원문 PDF/OCR 대조)*")
        if answers and num in answers:
            lines.append("")
            lines.append(f"**정답**: {answers[num]}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def load_comcbt_answers(path: Path | None) -> dict[int, int] | None:
    if not path or not path.exists():
        return None
    answers: dict[int, int] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            n, a = int(parts[0]), int(parts[1])
            if 1 <= n <= 100 and 1 <= a <= 4:
                answers[n] = a
    return answers or None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--answers-file")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    workdir = Path(args.workdir)
    txt_files = ocr_pages(pdf, workdir)
    raw = "\n\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in txt_files)
    raw_path = workdir / "combined-ocr.txt"
    raw_path.write_text(raw, encoding="utf-8")
    questions = parse_questions(raw)
    answers = load_comcbt_answers(
        Path(args.answers_file) if args.answers_file else None
    )
    md = to_markdown(
        questions,
        title=args.title,
        exam_date=args.date,
        source=args.source,
        raw_path=raw_path,
        answers=answers,
    )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out} parsed={len(questions)}", file=sys.stderr)


if __name__ == "__main__":
    main()
