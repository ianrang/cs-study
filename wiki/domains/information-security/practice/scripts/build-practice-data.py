#!/usr/bin/env python3
"""Validate practice JSON sources and generate browser-loadable practice-data.js."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PRACTICE_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = PRACTICE_ROOT.parent
DATA_ROOT = PRACTICE_ROOT / "data"
SCHEMA_PATH = PRACTICE_ROOT / "schemas" / "question-bank.schema.json"
OUTPUT_PATH = PRACTICE_ROOT / "practice-data.js"
ALLOWED_STATUSES = {"official", "source-derived", "inferred"}
ALLOWED_MATCH_POLICIES = {"case-insensitive", "exact"}
HANDLER_GRADING = {"short": "auto", "cloze": "auto", "order": "auto", "essay": "self"}
ALLOWED_QUESTION_KINDS = {"predicted"}
ALLOWED_BLOCK_TYPES = {"text", "code"}
ALLOWED_TOPIC_STATUSES = {"active", "future"}
ALLOWED_LEARNING_PATH_STATUSES = {"active", "future"}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path.relative_to(VAULT_ROOT)}: {error}") from error


def validate_source_ref(ref: object, question_id: str, errors: list[str]) -> None:
    if not isinstance(ref, dict):
        errors.append(f"{question_id}: sourceRefs item must be an object")
        return
    path = ref.get("path")
    line = ref.get("line")
    status = ref.get("status")
    excerpt = ref.get("excerpt")
    if not isinstance(path, str) or not path:
        errors.append(f"{question_id}: sourceRefs.path is required")
        return
    source_path = VAULT_ROOT / path
    if not source_path.is_file():
        errors.append(f"{question_id}: source path does not exist: {path}")
    elif not isinstance(line, int) or line < 1 or line > len(source_path.read_text(encoding="utf-8").splitlines()):
        errors.append(f"{question_id}: source line is outside {path}: {line}")
    else:
        source_line = source_path.read_text(encoding="utf-8").splitlines()[line - 1].strip()
        if not isinstance(excerpt, str) or len(excerpt.strip()) < 3:
            errors.append(f"{question_id}: sourceRefs.excerpt must identify the supported source text")
        elif not source_line or source_line.startswith("```") or excerpt not in source_line:
            errors.append(f"{question_id}: source excerpt does not match a meaningful source line: {path}:{line}")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{question_id}: invalid source status: {status}")


def has_non_empty_strings(value: object) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate_content_blocks(blocks: object, field: str, question_id: str, errors: list[str]) -> None:
    if not isinstance(blocks, list) or not blocks:
        errors.append(f"{question_id}: {field} must be a non-empty block array")
        return
    for index, block in enumerate(blocks, start=1):
        if not isinstance(block, dict) or block.get("type") not in ALLOWED_BLOCK_TYPES or not isinstance(block.get("content"), str) or not block["content"].strip():
            errors.append(f"{question_id}: {field} block {index} requires type(text/code) and non-empty content")


def validate_answer(question: dict[str, object], handler: str | None, errors: list[str]) -> None:
    question_id = str(question.get("id", "<missing id>"))
    stage = question.get("stage")
    answer = question.get("answer")
    if not isinstance(answer, dict):
        errors.append(f"{question_id}: answer must be an object")
        return
    if handler not in HANDLER_GRADING:
        errors.append(f"{question_id}: stage handler is unsupported")
        return
    if answer.get("type") != handler:
        errors.append(f"{question_id}: answer.type must be {handler}")
    if handler == "short":
        if answer.get("matchPolicy") not in ALLOWED_MATCH_POLICIES:
            errors.append(f"{question_id}: short/decision requires matchPolicy")
        accepted = answer.get("accepted")
        if not has_non_empty_strings(accepted):
            errors.append(f"{question_id}: short/decision requires non-empty accepted strings")
        if answer.get("inputLabel") is not None and (not isinstance(answer.get("inputLabel"), str) or not answer["inputLabel"].strip()):
            errors.append(f"{question_id}: short inputLabel must be a non-empty string when supplied")
    elif handler == "cloze":
        if answer.get("matchPolicy") not in ALLOWED_MATCH_POLICIES:
            errors.append(f"{question_id}: cloze requires matchPolicy")
        blanks = answer.get("blanks")
        if not isinstance(blanks, list) or not blanks:
            errors.append(f"{question_id}: cloze requires blanks")
            return
        blank_ids: set[str] = set()
        for blank in blanks:
            if not isinstance(blank, dict) or not isinstance(blank.get("id"), str) or not blank["id"].strip() or not isinstance(blank.get("label"), str) or not blank["label"].strip():
                errors.append(f"{question_id}: cloze blank requires non-empty id and label")
                continue
            blank_id = blank["id"]
            if blank_id in blank_ids:
                errors.append(f"{question_id}: duplicate cloze blank id {blank_id}")
            blank_ids.add(blank_id)
            accepted = blank.get("accepted")
            if not has_non_empty_strings(accepted):
                errors.append(f"{question_id}: blank {blank_id} requires accepted strings")
    elif handler == "order":
        items = answer.get("items")
        expected = answer.get("expected")
        if not isinstance(items, list) or not isinstance(expected, list) or not items:
            errors.append(f"{question_id}: order requires items and expected")
            return
        item_ids = [item.get("id") for item in items if isinstance(item, dict)]
        if len(item_ids) != len(items) or len(set(item_ids)) != len(items) or len(expected) != len(items) or len(set(expected)) != len(expected) or set(item_ids) != set(expected):
            errors.append(f"{question_id}: order item ids and expected must be the same unique set")
        if not all(isinstance(item, dict) and isinstance(item.get("id"), str) and item["id"].strip() and isinstance(item.get("label"), str) and item["label"].strip() for item in items):
            errors.append(f"{question_id}: each order item requires non-empty id and label")
    elif handler == "essay":
        model_answer = answer.get("modelAnswer")
        keyword_groups = answer.get("keywordGroups")
        deduction_risks = answer.get("deductionRisks")
        if not isinstance(model_answer, list) or not model_answer or not isinstance(keyword_groups, list) or not keyword_groups or not isinstance(deduction_risks, list) or not deduction_risks:
            errors.append(f"{question_id}: essay requires modelAnswer, keywordGroups, and deductionRisks")
            return
        if not has_non_empty_strings(model_answer) or not has_non_empty_strings(deduction_risks):
            errors.append(f"{question_id}: essay modelAnswer and deductionRisks require non-empty strings")
        for group in keyword_groups:
            if not isinstance(group, dict) or not isinstance(group.get("label"), str) or not group["label"].strip() or not isinstance(group.get("terms"), list) or not group["terms"] or not all(isinstance(term, str) and term.strip() for term in group["terms"]):
                errors.append(f"{question_id}: each keywordGroup requires label and non-empty terms")


def validate_question_provenance(question: dict[str, object], errors: list[str]) -> None:
    question_id = str(question.get("id", "<missing id>"))
    question_kind = question.get("questionKind")
    if question_kind is not None and question_kind not in ALLOWED_QUESTION_KINDS:
        errors.append(f"{question_id}: invalid questionKind: {question_kind}")
    refs = question.get("sourceRefs")
    if question_kind == "predicted" and (not isinstance(refs, list) or not any(
        isinstance(ref, dict) and "/08-prediction/" in str(ref.get("path", "")) for ref in refs
    )):
        errors.append(f"{question_id}: predicted question requires an 08-prediction sourceRef")
    if question_kind == "predicted" and (not isinstance(refs, list) or not any(
        isinstance(ref, dict) and "/05-analysis/" in str(ref.get("path", "")) for ref in refs
    )):
        errors.append(f"{question_id}: predicted question requires a 05-analysis sourceRef")
    exam_prompt = question.get("examPrompt")
    if exam_prompt is not None:
        validate_content_blocks(exam_prompt, "examPrompt", question_id, errors)


def validate_pack_contract(schema: dict[str, object], pack: dict[str, object], errors: list[str]) -> None:
    pack_id = str(pack.get("packId", "<missing packId>"))
    for field in schema.get("required", []):
        if field not in pack:
            errors.append(f"{pack_id}: schema required field is missing: {field}")
    if not isinstance(pack.get("version"), int) or int(pack.get("version", 0)) < 1:
        errors.append(f"{pack_id}: version must be an integer >= 1")
    if not isinstance(pack.get("packId"), str) or not pack["packId"].replace("-", "").isalnum() or pack["packId"].lower() != pack["packId"]:
        errors.append(f"{pack_id}: packId must be lowercase kebab-case")


def validate(curriculum: dict[str, object], packs: list[dict[str, object]], schema: dict[str, object]) -> list[str]:
    errors: list[str] = []
    required_question_fields = schema.get("properties", {}).get("questions", {}).get("items", {}).get("required", [])
    stages = curriculum.get("stages")
    if not isinstance(stages, list) or not stages:
        return ["curriculum: stages must be a non-empty array"]
    stage_ids = [stage.get("id") for stage in stages if isinstance(stage, dict)]
    if len(stage_ids) != len(stages) or len(set(stage_ids)) != len(stages):
        errors.append("curriculum: stage ids must be unique")
    for stage in stages:
        if not isinstance(stage, dict) or not isinstance(stage.get("id"), str) or not stage["id"].strip() or not isinstance(stage.get("label"), str) or not stage["label"].strip() or stage.get("handler") not in HANDLER_GRADING or stage.get("grading") != HANDLER_GRADING.get(stage.get("handler")):
            errors.append("curriculum: each stage requires id, label, supported handler, and matching grading")
    stage_id_set = set(stage_ids)
    stage_handler_by_id = {stage["id"]: stage["handler"] for stage in stages if isinstance(stage, dict) and stage.get("id") in stage_id_set and stage.get("handler") in HANDLER_GRADING}
    learning_paths = curriculum.get("learningPaths")
    if not isinstance(learning_paths, list) or not learning_paths:
        errors.append("curriculum: learningPaths must be a non-empty array")
        learning_paths = []
    learning_path_ids = [path.get("id") for path in learning_paths if isinstance(path, dict)]
    if len(learning_path_ids) != len(learning_paths) or len(set(learning_path_ids)) != len(learning_paths):
        errors.append("curriculum: learningPath ids must be unique")
    learning_path_id_set = set(learning_path_ids)
    for path in learning_paths:
        if not isinstance(path, dict) or not isinstance(path.get("id"), str) or not path["id"].strip() or not isinstance(path.get("title"), str) or not path["title"].strip() or path.get("status") not in ALLOWED_LEARNING_PATH_STATUSES:
            errors.append("curriculum: each learningPath requires id, title, and supported status")

    topics = curriculum.get("topics")
    if not isinstance(topics, list):
        return ["curriculum: topics must be an array"]
    topic_ids = [topic.get("id") for topic in topics if isinstance(topic, dict)]
    if len(topic_ids) != len(topics) or len(set(topic_ids)) != len(topics):
        errors.append("curriculum: topic ids must be unique")
    topic_id_set = set(topic_ids)
    for topic in topics:
        if not isinstance(topic, dict):
            errors.append("curriculum: each topic must be an object")
            continue
        if not isinstance(topic.get("id"), str) or not topic["id"].strip() or not isinstance(topic.get("title"), str) or not topic["title"].strip() or topic.get("status") not in ALLOWED_TOPIC_STATUSES:
            errors.append("curriculum: each topic requires id, title, and supported status")
        if topic.get("status") == "active":
            if topic.get("learningPath") not in learning_path_id_set:
                errors.append(f"curriculum: active topic has invalid learningPath: {topic.get('id')}")
            if not isinstance(topic.get("sourceChapter"), str) or not topic["sourceChapter"].strip() or not isinstance(topic.get("sourceSection"), str) or not topic["sourceSection"].strip():
                errors.append(f"curriculum: active topic requires sourceChapter and sourceSection: {topic.get('id')}")
        for prerequisite in topic.get("prerequisites", []):
            if prerequisite not in topic_id_set or prerequisite == topic.get("id"):
                errors.append(f"curriculum: invalid prerequisite {prerequisite} for {topic.get('id')}")

    question_ids: set[str] = set()
    questions_by_id: dict[str, dict[str, object]] = {}
    topic_question_count = {topic_id: 0 for topic_id in topic_id_set}
    for pack in packs:
        validate_pack_contract(schema, pack, errors)
        questions = pack.get("questions")
        if not isinstance(questions, list) or not questions:
            errors.append(f"{pack.get('packId', '<missing pack>')}: questions must be a non-empty array")
            continue
        for question in questions:
            if not isinstance(question, dict):
                errors.append("question must be an object")
                continue
            for field in required_question_fields:
                if field not in question:
                    errors.append(f"question: schema required field is missing: {field}")
            question_id = question.get("id")
            if not isinstance(question_id, str) or not question_id:
                errors.append("question id is required")
                continue
            if question_id in question_ids:
                errors.append(f"duplicate question id: {question_id}")
            question_ids.add(question_id)
            questions_by_id[question_id] = question
            if question.get("curriculumId") not in topic_id_set:
                errors.append(f"{question_id}: unknown curriculumId {question.get('curriculumId')}")
            else:
                topic_question_count[str(question["curriculumId"])] += 1
            if question.get("stage") not in stage_id_set:
                errors.append(f"{question_id}: invalid stage {question.get('stage')}")
            if not isinstance(question.get("title"), str) or not question["title"].strip():
                errors.append(f"{question_id}: title is required")
            validate_content_blocks(question.get("prompt"), "prompt", question_id, errors)
            validate_content_blocks(question.get("explanation"), "explanation", question_id, errors)
            if not has_non_empty_strings(question.get("tags")):
                errors.append(f"{question_id}: tags require non-empty strings")
            if not isinstance(question.get("prerequisites"), list) or not all(isinstance(item, str) for item in question.get("prerequisites", [])):
                errors.append(f"{question_id}: prerequisites must be a string array")
            refs = question.get("sourceRefs")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{question_id}: sourceRefs are required")
            else:
                for ref in refs:
                    validate_source_ref(ref, question_id, errors)
            validate_question_provenance(question, errors)
            validate_answer(question, stage_handler_by_id.get(question.get("stage")), errors)

    for question_id, question in questions_by_id.items():
        for prerequisite in question.get("prerequisites", []):
            if prerequisite == question_id or prerequisite not in questions_by_id:
                errors.append(f"{question_id}: invalid question prerequisite {prerequisite}")
                continue
            prerequisite_topic = questions_by_id[prerequisite].get("curriculumId")
            question_topic = question.get("curriculumId")
            if prerequisite_topic != question_topic and prerequisite_topic not in topic_by_prerequisite_lineage(curriculum, question_topic):
                errors.append(f"{question_id}: prerequisite {prerequisite} is outside its curriculum lineage")
    validate_question_prerequisite_cycles(questions_by_id, errors)

    for topic in topics:
        if isinstance(topic, dict) and topic.get("status") == "active" and topic_question_count.get(topic.get("id"), 0) == 0:
            errors.append(f"active topic has no question: {topic.get('id')}")
    return errors


def topic_by_prerequisite_lineage(curriculum: dict[str, object], topic_id: object) -> set[object]:
    topic_map = {topic.get("id"): topic for topic in curriculum.get("topics", []) if isinstance(topic, dict)}
    lineage: set[object] = set()
    pending = list(topic_map.get(topic_id, {}).get("prerequisites", []))
    while pending:
        prerequisite = pending.pop()
        if prerequisite in lineage:
            continue
        lineage.add(prerequisite)
        pending.extend(topic_map.get(prerequisite, {}).get("prerequisites", []))
    return lineage


def validate_question_prerequisite_cycles(questions_by_id: dict[str, dict[str, object]], errors: list[str]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(question_id: str) -> None:
        if question_id in visited:
            return
        if question_id in visiting:
            errors.append(f"question prerequisites contain a cycle at {question_id}")
            return
        visiting.add(question_id)
        for prerequisite in questions_by_id[question_id].get("prerequisites", []):
            if prerequisite in questions_by_id:
                visit(prerequisite)
        visiting.remove(question_id)
        visited.add(question_id)

    for question_id in questions_by_id:
        visit(question_id)


def build_payload(curriculum: dict[str, object], packs: list[dict[str, object]]) -> dict[str, object]:
    questions = [question for pack in packs for question in pack["questions"]]
    return {"version": 1, "curriculum": curriculum, "questions": questions}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated data is stale")
    args = parser.parse_args()

    try:
        curriculum = load_json(DATA_ROOT / "curriculum.json")
        pack_paths = sorted((DATA_ROOT / "question-packs").glob("*.json"))
        if not pack_paths:
            raise ValueError("no question packs found")
        packs = [load_json(path) for path in pack_paths]
        schema = load_json(SCHEMA_PATH)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if not isinstance(curriculum, dict) or not isinstance(schema, dict) or not all(isinstance(pack, dict) for pack in packs):
        print("content roots must be JSON objects", file=sys.stderr)
        return 1
    errors = validate(curriculum, packs, schema)
    if errors:
        print("question bank validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1

    payload = build_payload(curriculum, packs)
    generated = "// Generated by scripts/build-practice-data.py. Do not edit directly.\n"
    generated += "window.PRACTICE_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    if args.check:
        if not OUTPUT_PATH.is_file() or OUTPUT_PATH.read_text(encoding="utf-8") != generated:
            print("practice-data.js is missing or stale; run python3 scripts/build-practice-data.py", file=sys.stderr)
            return 1
        print("question bank validation passed; generated data is current")
        return 0
    OUTPUT_PATH.write_text(generated, encoding="utf-8")
    print(f"validated {len(payload['questions'])} questions and generated {OUTPUT_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
