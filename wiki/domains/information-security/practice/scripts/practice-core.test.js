"use strict";

const assert = require("node:assert/strict");
const test = require("node:test");

global.window = globalThis;
require("../practice-core.js");

test("theme preference cycle is independent of the system theme", () => {
  const { nextThemePreference } = window.PRACTICE_CORE;
  let preference = null;
  const states = [];

  for (let index = 0; index < 4; index += 1) {
    states.push(preference);
    preference = nextThemePreference(preference);
  }

  assert.deepEqual(states, [null, "dark", "light", null]);
});

test("invalid theme preference safely returns to the system-to-dark transition", () => {
  assert.equal(window.PRACTICE_CORE.nextThemePreference("invalid"), "dark");
  assert.equal(window.PRACTICE_CORE.isThemePreference("dark"), true);
  assert.equal(window.PRACTICE_CORE.isThemePreference(null), false);
});

test("attempted progress is normalized to one presentation state", () => {
  const { normalizeProgressRecord } = window.PRACTICE_CORE;
  assert.deepEqual(normalizeProgressRecord({ lastResult: "attempted" }), {
    attemptCount: 0,
    lastResult: "attempted",
    masteryStatus: "attempted",
    essayKeywordScore: null,
    updatedAt: null
  });
  assert.equal(normalizeProgressRecord({ lastResult: "attempted", masteryStatus: "review" }).masteryStatus, "attempted");
});

test("past-exam badge requires both a reconstructed prompt and a round source", () => {
  const { isReconstructedPastExam } = window.PRACTICE_CORE;
  const roundRef = { path: "datasets/info-sec-engineer-practical-past-exams/01-rounds/2026-01-practical-31.md" };

  assert.equal(isReconstructedPastExam({ sourceRefs: [roundRef] }), false);
  assert.equal(isReconstructedPastExam({ examPrompt: [{ type: "text", content: "문제" }], sourceRefs: [] }), false);
  assert.equal(isReconstructedPastExam({ examPrompt: [{ type: "text", content: "문제" }], sourceRefs: [roundRef] }), true);
});

test("essay keyword terms keep English commands and abbreviations at token boundaries", () => {
  const { matchesKeywordTerm } = window.PRACTICE_CORE;

  assert.equal(matchesKeywordTerm("wtmp lastb lastlog lastcomm", "w"), false);
  assert.equal(matchesKeywordTerm("wtmp lastb lastlog lastcomm", "last"), false);
  assert.equal(matchesKeywordTerm("who와 last를 확인한다", "who"), true);
  assert.equal(matchesKeywordTerm("who와 last를 확인한다", "last"), true);
  assert.equal(matchesKeywordTerm("설정 파일 변조를 방지한다", "설정 파일 변조"), true);
});

test("question ordering places filtered prerequisites before dependent questions", () => {
  const { orderByPrerequisites } = window.PRACTICE_CORE;
  const questions = [
    { id: "essay", prerequisites: ["order"] },
    { id: "order", prerequisites: ["cloze"] },
    { id: "cloze", prerequisites: [] }
  ];

  assert.deepEqual(orderByPrerequisites(questions).map((question) => question.id), ["cloze", "order", "essay"]);
});
