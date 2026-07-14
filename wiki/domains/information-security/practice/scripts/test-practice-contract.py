#!/usr/bin/env python3
"""Regression tests for the practice content contract."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


PRACTICE_ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = PRACTICE_ROOT / "scripts" / "build-practice-data.py"
SPEC = importlib.util.spec_from_file_location("build_practice_data", BUILD_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load build-practice-data.py")
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)


class PracticeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curriculum = BUILD.load_json(PRACTICE_ROOT / "data" / "curriculum.json")
        self.packs = [BUILD.load_json(path) for path in sorted((PRACTICE_ROOT / "data" / "question-packs").glob("*.json"))]
        self.schema = BUILD.load_json(PRACTICE_ROOT / "schemas" / "question-bank.schema.json")

    def validate(self, curriculum: object | None = None, packs: object | None = None) -> list[str]:
        return BUILD.validate(
            copy.deepcopy(self.curriculum if curriculum is None else curriculum),
            copy.deepcopy(self.packs if packs is None else packs),
            copy.deepcopy(self.schema),
        )

    def test_current_sources_satisfy_the_contract(self) -> None:
        self.assertEqual(self.validate(), [])

    def test_missing_learning_paths_is_rejected_before_the_ui_can_initialize(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        del curriculum["learningPaths"]
        self.assertIn("curriculum: learningPaths must be a non-empty array", self.validate(curriculum=curriculum))

    def test_active_topic_with_an_unknown_learning_path_is_rejected(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        next(topic for topic in curriculum["topics"] if topic["status"] == "active")["learningPath"] = "missing-path"
        self.assertTrue(any("active topic has invalid learningPath" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_learning_path_id_is_reported_without_raising(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["learningPaths"][0]["id"] = []
        self.assertTrue(any("learningPath ids must be unique" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_stage_and_topic_ids_are_reported_without_raising(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["stages"][0]["id"] = []
        self.assertTrue(any("stage ids must be unique" in error for error in self.validate(curriculum=curriculum)))

        curriculum = copy.deepcopy(self.curriculum)
        curriculum["topics"][0]["id"] = []
        self.assertTrue(any("topic ids must be unique" in error for error in self.validate(curriculum=curriculum)))

    def test_malformed_order_item_id_is_reported_without_raising(self) -> None:
        packs = copy.deepcopy(self.packs)
        order_question = next(question for pack in packs for question in pack["questions"] if question["stage"] == "order")
        order_question["answer"]["items"][0]["id"] = []
        self.assertTrue(any("order item ids and expected must be the same unique set" in error for error in self.validate(packs=packs)))

    def test_malformed_question_prerequisite_is_reported_without_raising(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"][0]["prerequisites"] = [[]]
        self.assertTrue(any("prerequisites must be a string array" in error for error in self.validate(packs=packs)))

    def test_invalid_content_block_is_rejected_before_rendering(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"][0]["prompt"] = [{"type": "unsupported", "content": ""}]
        self.assertTrue(any("prompt block 1 requires type(text/code) and non-empty content" in error for error in self.validate(packs=packs)))

    def test_empty_question_pack_is_rejected(self) -> None:
        packs = copy.deepcopy(self.packs)
        packs[0]["questions"] = []
        self.assertTrue(any("questions must be a non-empty array" in error for error in self.validate(packs=packs)))


if __name__ == "__main__":
    unittest.main()
