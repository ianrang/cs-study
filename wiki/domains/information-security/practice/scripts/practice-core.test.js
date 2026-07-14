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
