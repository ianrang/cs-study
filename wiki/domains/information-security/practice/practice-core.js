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

  function isReconstructedPastExam(question) {
    return Array.isArray(question?.examPrompt)
      && question.examPrompt.length > 0
      && Array.isArray(question?.sourceRefs)
      && question.sourceRefs.some((ref) => typeof ref?.path === "string"
        && ref.path.includes("datasets/info-sec-engineer-practical-past-exams/01-rounds/"));
  }

  function normalizeKeywordText(value) {
    return String(value ?? "").trim().toLocaleLowerCase().replace(/\s+/g, " ");
  }

  function matchesKeywordTerm(response, term) {
    const normalizedResponse = normalizeKeywordText(response);
    const normalizedTerm = normalizeKeywordText(term);
    if (!normalizedTerm) return false;

    // English commands and abbreviations must be whole tokens. Otherwise, for
    // example, `last` incorrectly satisfies `lastb`, and `w` satisfies `wtmp`.
    if (/^[a-z0-9_]+$/.test(normalizedTerm)) {
      return new RegExp(`(^|[^a-z0-9_])${normalizedTerm}($|[^a-z0-9_])`, "i").test(normalizedResponse);
    }
    return normalizedResponse.includes(normalizedTerm);
  }

  function orderByPrerequisites(items) {
    const itemById = new Map(items.map((item) => [item.id, item]));
    const ordered = [];
    const visited = new Set();
    const visiting = new Set();

    function visit(item) {
      if (visited.has(item.id) || visiting.has(item.id)) return;
      visiting.add(item.id);
      (item.prerequisites || []).forEach((prerequisiteId) => {
        const prerequisite = itemById.get(prerequisiteId);
        if (prerequisite) visit(prerequisite);
      });
      visiting.delete(item.id);
      visited.add(item.id);
      ordered.push(item);
    }

    items.forEach(visit);
    return ordered;
  }

  window.PRACTICE_CORE = Object.freeze({
    isThemePreference,
    nextThemePreference,
    normalizeProgressRecord,
    isReconstructedPastExam,
    matchesKeywordTerm,
    orderByPrerequisites
  });
})();
