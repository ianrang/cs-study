(() => {
  "use strict";

  const explicitThemePreferences = Object.freeze(["dark", "light"]);
  const themePreferenceCycle = Object.freeze([null, ...explicitThemePreferences]);
  const progressResults = Object.freeze(["attempted", "correct", "incorrect", "self-understood", "self-review"]);
  const masteryStatuses = Object.freeze(["attempted", "mastered", "review"]);

  function isThemePreference(value) {
    return explicitThemePreferences.includes(value);
  }

  function nextThemePreference(preference) {
    const currentIndex = themePreferenceCycle.indexOf(isThemePreference(preference) ? preference : null);
    return themePreferenceCycle[(currentIndex + 1) % themePreferenceCycle.length];
  }

  function normalizeProgressRecord(record) {
    const lastResult = record?.lastResult;
    if (!progressResults.includes(lastResult)) return null;
    const fallbackStatus = lastResult === "attempted"
      ? "attempted"
      : lastResult === "correct" || lastResult === "self-understood" ? "mastered" : "review";
    const masteryStatus = lastResult === "attempted" ? "attempted" : record?.masteryStatus || fallbackStatus;
    if (!masteryStatuses.includes(masteryStatus)) return null;
    return {
      attemptCount: Number.isInteger(record?.attemptCount) && record.attemptCount >= 0 ? record.attemptCount : 0,
      lastResult,
      masteryStatus,
      essayKeywordScore: Number.isInteger(record?.essayKeywordScore) && record.essayKeywordScore >= 0 && record.essayKeywordScore <= 100 ? record.essayKeywordScore : null,
      updatedAt: record?.updatedAt || null
    };
  }

  window.PRACTICE_CORE = Object.freeze({
    isThemePreference,
    nextThemePreference,
    normalizeProgressRecord
  });
})();
