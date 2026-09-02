(() => {
  "use strict";

  const data = window.PRACTICE_DATA;
  const core = window.PRACTICE_CORE;
  const storageKey = "info-security-practice-progress-v1";
  const pastExamStorageKey = "info-security-past-exam-progress-v1";
  const root = document.documentElement;
  const themeStorageKey = root.dataset.themeStorageKey;
  const systemThemeQuery = window.matchMedia?.("(prefers-color-scheme: dark)");
  const pastExamItems = Array.isArray(data?.pastExams?.rounds)
    ? data.pastExams.rounds.flatMap((round) => round.items.map((item) => ({ ...item, roundId: round.roundId, year: round.year, session: round.session })))
    : [];
  let storageAvailable = true;
  const state = {
    contentKind: "learning",
    learningPath: "all",
    source: "all",
    topic: "all",
    stage: "all",
    reviewOnly: false,
    practiceMode: "learning",
    pastYear: "all",
    pastRound: "all",
    pastType: "all",
    index: 0,
    feedback: null,
    orderDrafts: {},
    essayDrafts: {},
    draggedOrderItemId: null,
    focusRequest: null,
    progress: loadProgress(),
    pastProgress: loadPastExamProgress(),
    pastDrafts: {},
    themePreference: loadThemePreference()
  };
  const elements = {
    contentKind: document.querySelector("#content-kind-filter"),
    learningPath: document.querySelector("#learning-path-filter"),
    source: document.querySelector("#source-filter"),
    topic: document.querySelector("#topic-filter"),
    stage: document.querySelector("#stage-filter"),
    pastYear: document.querySelector("#past-year-filter"),
    pastRound: document.querySelector("#past-round-filter"),
    pastType: document.querySelector("#past-type-filter"),
    pastYearGroup: document.querySelector("#past-year-filter-group"),
    pastRoundGroup: document.querySelector("#past-round-filter-group"),
    pastTypeGroup: document.querySelector("#past-type-filter-group"),
    review: document.querySelector("#review-filter"),
    resetFilters: document.querySelector("#reset-filters"),
    filterSummary: document.querySelector("#filter-summary"),
    practiceMode: document.querySelector("#practice-mode-control"),
    themeToggle: document.querySelector("#theme-toggle"),
    themeToggleLabel: document.querySelector("#theme-toggle-label"),
    themeCurrent: document.querySelector("#theme-current"),
    card: document.querySelector("#question-card"),
    position: document.querySelector("#question-position"),
    navigator: document.querySelector("#question-navigator"),
    previous: document.querySelector("#previous-question"),
    next: document.querySelector("#next-question"),
    quickNavigation: document.querySelector("#quick-question-navigation"),
    quickPrevious: document.querySelector("#quick-previous-question"),
    quickPosition: document.querySelector("#quick-question-position"),
    quickNext: document.querySelector("#quick-next-question"),
    resetTopic: document.querySelector("#reset-topic"),
    resetAll: document.querySelector("#reset-all"),
    storageNotice: document.querySelector("#storage-notice"),
    futureTopics: document.querySelector("#future-topic-list"),
    statTotal: document.querySelector("#stat-total"),
    statComplete: document.querySelector("#stat-complete"),
    statMastered: document.querySelector("#stat-mastered"),
    statReview: document.querySelector("#stat-review"),
    statFiltered: document.querySelector("#stat-filtered")
  };

  if (!data || !data.curriculum || !Array.isArray(data.curriculum.learningPaths) || !Array.isArray(data.curriculum.stages) || !Array.isArray(data.curriculum.topics) || !Array.isArray(data.questions) || !Array.isArray(data.pastExams?.rounds) || !core) {
    elements.card.innerHTML = "<p>학습 데이터 또는 필수 앱 코드가 없습니다. <code>python3 scripts/build-practice-data.py</code>를 실행하고 파일 구성을 확인하세요.</p>";
    return;
  }

  const activeTopics = data.curriculum.topics.filter((topic) => topic.status === "active");
  const topicById = new Map(data.curriculum.topics.map((topic) => [topic.id, topic]));
  const stageById = new Map(data.curriculum.stages.map((stage) => [stage.id, stage]));

  function formatTopicLabel(topic) {
    const source = topic.sourceChapter && topic.sourceSection
      ? `${topic.sourceChapter}장 · ${topic.sourceSection} · `
      : "";
    return `${source}${topic.title}`;
  }

  function normalize(value, matchPolicy = "case-insensitive") {
    const raw = String(value ?? "");
    return matchPolicy === "exact" ? raw : raw.trim().toLocaleLowerCase().replace(/\s+/g, " ");
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // This is the only formatter for the source-derived year/session/round
  // identity. Both learning and exam modes consume the same label.
  function formatPastExamRoundLabel(item) {
    return `${item.year}년 ${Number(item.session)}회 · ${item.roundId}`;
  }

  const displayBlockPattern = /\{\{(code|reference)(?::([a-z0-9]+(?:-[a-z0-9]+)*))?\}\}([\s\S]*?)\{\{\/\1\}\}/g;

  function formatPastExamInline(value) {
    // Escape all source text first so a reconstructed item can never inject
    // HTML. Only the explicit source marker and legacy top-level answer labels
    // receive presentational line breaks after that escaping step.
    const escaped = escapeHtml(value).replaceAll("&lt;br&gt;", "<br>");
    const normalizedLegacyLabels = escaped.replace(
      /(^|<br>|\s)([A-Z가-힣])\s*:/g,
      "$1($2)"
    );
    return normalizedLegacyLabels.replace(
      /\s(?=\((?:[A-Z가-힣]|\d{1,2})\)(?::|\s))/g,
      "<br>"
    );
  }

  function formatPastExamBlockContent(value) {
    return escapeHtml(value)
      .replaceAll("\\n", "\n")
      .replaceAll("&lt;br&gt;", "\n");
  }

  function renderPastExamDisplayBlock(kind, language, content) {
    if (kind === "code") {
      const normalizedLanguage = language || "text";
      const label = language ? "보기 · " + language : "보기 · 코드";
      return '<section class="exam-code-block" data-language="' + escapeHtml(normalizedLanguage) + '" aria-label="' + escapeHtml(label) + '"><div class="exam-block-label">' + escapeHtml(label) + '</div><pre><code>' + formatPastExamBlockContent(content) + '</code></pre></section>';
    }
    return '<aside class="exam-reference-block" aria-label="보기"><div class="exam-block-label">보기</div><div class="exam-reference-content">' + formatPastExamBlockContent(content) + "</div></aside>";
  }

  function formatPastExamText(value) {
    const text = String(value ?? "");
    let cursor = 0;
    let rendered = "";
    for (const match of text.matchAll(displayBlockPattern)) {
      rendered += formatPastExamInline(text.slice(cursor, match.index));
      rendered += renderPastExamDisplayBlock(match[1], match[2], match[3]);
      cursor = match.index + match[0].length;
    }
    return rendered + formatPastExamInline(text.slice(cursor));
  }

  function loadProgress() {
    return loadProgressFor(storageKey, data.questions.map((question) => question.id));
  }

  function loadPastExamProgress() {
    return loadProgressFor(pastExamStorageKey, pastExamItems.map((item) => item.id));
  }

  function loadProgressFor(key, knownIds) {
    try {
      const stored = localStorage.getItem(key);
      if (!stored) return {};
      const parsed = JSON.parse(stored);
      if (!parsed || parsed.schemaVersion !== 1 || !parsed.records || typeof parsed.records !== "object") return {};
      const knownItemIds = new Set(knownIds);
      return Object.fromEntries(Object.entries(parsed.records)
        .filter(([id]) => knownItemIds.has(id))
        .map(([id, record]) => [id, core.normalizeProgressRecord(record)])
        .filter(([, record]) => record !== null));
    } catch {
      storageAvailable = false;
      return {};
    }
  }

  function saveProgress() {
    return saveProgressFor(storageKey, state.progress);
  }

  function savePastExamProgress() {
    return saveProgressFor(pastExamStorageKey, state.pastProgress);
  }

  function saveProgressFor(key, progress) {
    try {
      localStorage.setItem(key, JSON.stringify({ schemaVersion: 1, records: progress }));
      return true;
    } catch {
      storageAvailable = false;
      return false;
    }
  }

  function loadThemePreference() {
    if (!themeStorageKey) return null;
    try {
      const preference = localStorage.getItem(themeStorageKey);
      return core.isThemePreference(preference) ? preference : null;
    } catch {
      return null;
    }
  }

  function saveThemePreference() {
    if (!themeStorageKey) return;
    try {
      if (state.themePreference) localStorage.setItem(themeStorageKey, state.themePreference);
      else localStorage.removeItem(themeStorageKey);
    } catch {}
  }

  function getResolvedTheme() {
    return state.themePreference || (systemThemeQuery?.matches ? "dark" : "light");
  }

  function renderThemeToggle() {
    if (state.themePreference) root.dataset.theme = state.themePreference;
    else delete root.dataset.theme;
    const isDark = getResolvedTheme() === "dark";
    const nextPreference = core.nextThemePreference(state.themePreference);
    const actionLabel = nextPreference
      ? `${nextPreference === "dark" ? "다크" : "라이트"} 모드 사용`
      : "시스템 테마 사용";
    const currentLabel = state.themePreference
      ? `현재 테마: ${state.themePreference === "dark" ? "다크 모드" : "라이트 모드"}`
      : `현재 테마: 시스템 설정(${isDark ? "다크 모드" : "라이트 모드"})`;
    elements.themeToggle.setAttribute("aria-label", actionLabel);
    elements.themeToggleLabel.textContent = actionLabel;
    elements.themeCurrent.textContent = currentLabel;
  }

  function toggleTheme() {
    state.themePreference = core.nextThemePreference(state.themePreference);
    saveThemePreference();
    renderThemeToggle();
  }

  function syncSystemThemeLabel() {
    if (!state.themePreference) renderThemeToggle();
  }

  function getFilteredQuestions() {
    return core.orderByPrerequisites(data.questions.filter((question) => {
      const topic = topicById.get(question.curriculumId);
      const learningPathMatches = state.learningPath === "all" || topic.learningPath === state.learningPath;
      const sourceMatches = state.source === "all" || `${topic.sourceChapter}:${topic.sourceSection}` === state.source;
      const topicMatches = state.topic === "all" || question.curriculumId === state.topic;
      const activeMatches = topic.status === "active";
      const stageMatches = state.stage === "all" || question.stage === state.stage;
      const record = state.progress[question.id];
      const reviewMatches = !state.reviewOnly || record?.lastResult === "incorrect" || record?.lastResult === "self-review";
      return activeMatches && learningPathMatches && sourceMatches && topicMatches && stageMatches && reviewMatches;
    }));
  }

  function getCurrentQuestion() {
    const questions = getFilteredQuestions();
    if (!questions.length) return null;
    state.index = Math.max(0, Math.min(state.index, questions.length - 1));
    return questions[state.index];
  }

  function getFilteredPastExamItems() {
    return pastExamItems.filter((item) => {
      const yearMatches = state.pastYear === "all" || item.year === state.pastYear;
      const roundMatches = state.pastRound === "all" || item.roundId === state.pastRound;
      const typeMatches = state.pastType === "all" || item.type === state.pastType;
      const record = state.pastProgress[item.id];
      const reviewMatches = !state.reviewOnly || record?.lastResult === "self-review";
      return yearMatches && roundMatches && typeMatches && reviewMatches;
    });
  }

  function getActiveItems() {
    return state.contentKind === "past-exam" ? getFilteredPastExamItems() : getFilteredQuestions();
  }

  function getCurrentPastExamItem() {
    const items = getFilteredPastExamItems();
    if (!items.length) return null;
    state.index = Math.max(0, Math.min(state.index, items.length - 1));
    return items[state.index];
  }

  function getCurrentItem() {
    return state.contentKind === "past-exam" ? getCurrentPastExamItem() : getCurrentQuestion();
  }

  function sourceBadge(status) {
    const label = status === "source-derived" ? "복원·파생 근거" : status === "inferred" ? "학습용 추론" : "공식 근거";
    return `<span class="badge badge-${escapeHtml(status)}">${label}</span>`;
  }

  function formatPastExamMeta(item, isExamMode) {
    const modeBadge = isExamMode ? '<span class="badge badge-active">실전 모드</span>' : "";
    return `<span class="badge">${escapeHtml(formatPastExamRoundLabel(item))}</span><span class="badge">${escapeHtml(item.type)}</span><span class="badge badge-past-exam">기출 복원 · 파생 근거</span>${sourceBadge(item.status)}${modeBadge}${progressBadges(item)}`;
  }

  function questionOriginBadge(question) {
    if (question.questionKind === "predicted") return '<span class="badge badge-predicted">예상 문제 · 분석 근거</span>';
    if (core.isReconstructedPastExam(question)) {
      return '<span class="badge badge-past-exam">기출 기반 · 복원 문항</span>';
    }
    return '<span class="badge badge-study">학습 문제</span>';
  }

  function renderBlocks(blocks) {
    return blocks.map((block) => block.type === "code"
      ? `<pre><code>${escapeHtml(block.content)}</code></pre>`
      : `<p>${escapeHtml(block.content)}</p>`).join("");
  }

  function renderShortInput(question) {
    const label = state.practiceMode === "exam" ? "정답" : question.answer.inputLabel || "정답";
    return `<div class="answer-field"><label for="answer-main">${escapeHtml(label)}</label><input id="answer-main" type="text" autocomplete="off" /></div>`;
  }

  function renderClozeInput(question) {
    return `<div class="cloze-grid">${question.answer.blanks.map((blank) => `
      <div class="answer-field"><label for="answer-${escapeHtml(blank.id)}">(${escapeHtml(blank.id)}) ${state.practiceMode === "exam" ? "" : escapeHtml(blank.label)}</label>
      <input id="answer-${escapeHtml(blank.id)}" type="text" autocomplete="off" /></div>`).join("")}</div>`;
  }

  function renderOrderInput(question) {
    const current = state.orderDrafts[question.id] || question.answer.items.map((item) => item.id);
    state.orderDrafts[question.id] = current;
    const labels = new Map(question.answer.items.map((item) => [item.id, item.label]));
    return `<ol class="order-list" id="order-list">${current.map((itemId, index) => `
      <li class="order-item" draggable="true" tabindex="0" data-order-item-id="${escapeHtml(itemId)}" data-order-index="${index}" aria-label="${index + 1}번 ${escapeHtml(labels.get(itemId))}. Alt 또는 Option과 위·아래 화살표로 이동"><span class="drag-handle" aria-hidden="true">⠿</span><span class="order-index">${index + 1}</span><span class="order-label">${escapeHtml(labels.get(itemId))}</span></li>`).join("")}</ol><p class="order-help">항목을 드래그해 순서를 바꾸세요. 키보드에서는 항목에 초점을 둔 뒤 Alt(맥에서는 Option)+위·아래 화살표를 사용합니다.</p>`;
  }

  function renderEssayInput(question) {
    return `<div class="answer-field"><label for="answer-essay">답안 작성</label><textarea id="answer-essay" placeholder="한두 문장으로 직접 답안을 작성하세요.">${escapeHtml(state.essayDrafts[question.id] || "")}</textarea></div>`;
  }

  function gradeShort(question) {
    const response = document.querySelector("#answer-main")?.value || "";
    return { correct: question.answer.accepted.some((value) => normalize(value, question.answer.matchPolicy) === normalize(response, question.answer.matchPolicy)) };
  }

  function gradeCloze(question) {
    const correct = question.answer.blanks.every((blank) => {
      const response = document.querySelector(`#answer-${CSS.escape(blank.id)}`)?.value || "";
      return blank.accepted.some((value) => normalize(value, question.answer.matchPolicy) === normalize(response, question.answer.matchPolicy));
    });
    return { correct };
  }

  function gradeOrder(question) {
    const current = state.orderDrafts[question.id] || [];
    return { correct: current.length === question.answer.expected.length && current.every((itemId, index) => itemId === question.answer.expected[index]) };
  }

  function scoreEssay(question) {
    const response = document.querySelector("#answer-essay")?.value || "";
    state.essayDrafts[question.id] = response;
    const normalizedResponse = normalize(response);
    const groups = question.answer.keywordGroups.map((group) => ({
      label: group.label,
      matched: group.terms.some((term) => core.matchesKeywordTerm(normalizedResponse, term))
    }));
    const matchedCount = groups.filter((group) => group.matched).length;
    return { correct: null, keywordScore: Math.round((matchedCount / groups.length) * 100), groups };
  }

  const stageHandlers = {
    short: { renderInput: renderShortInput, grade: gradeShort, answerSummary: (question) => question.answer.accepted[0] },
    cloze: { renderInput: renderClozeInput, grade: gradeCloze, answerSummary: (question) => question.answer.blanks.map((blank) => `(${blank.id}) ${blank.accepted[0]}`).join(" · ") },
    order: { renderInput: renderOrderInput, grade: gradeOrder, answerSummary: (question) => question.answer.expected.map((itemId, index) => `${index + 1}. ${question.answer.items.find((item) => item.id === itemId).label}`).join(" → ") },
    essay: { renderInput: renderEssayInput, grade: scoreEssay, answerSummary: () => "모범 답안과 핵심 키워드를 확인하세요." }
  };

  function handlerFor(question) {
    return stageHandlers[stageById.get(question.stage).handler];
  }

  function sourcesMarkupFromRefs(sourceRefs) {
    const refs = sourceRefs.map((ref) => `<li><code>${escapeHtml(ref.path)}:${escapeHtml(ref.line)}</code> · ${escapeHtml(ref.status)}<br /><span>확인 문구: ${escapeHtml(ref.excerpt)}</span></li>`).join("");
    return `<details><summary>근거와 검증 상태</summary><ul class="source-list">${refs}</ul></details>`;
  }

  function sourcesMarkup(question) {
    return sourcesMarkupFromRefs(question.sourceRefs);
  }

  function feedbackMarkup(question, result) {
    const isSelfGraded = stageById.get(question.stage).grading === "self";
    const feedbackClass = isSelfGraded ? "feedback-self" : result.correct ? "feedback-correct" : "feedback-incorrect";
    const heading = isSelfGraded ? "모범 답안과 채점 기준" : result.correct ? "정답입니다" : "다시 확인해 보세요";
    const model = isSelfGraded
      ? `<div><h3>모범 답안</h3><ol class="model-answer">${question.answer.modelAnswer.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ol></div>
         <div><h3>핵심 키워드 충족률</h3><p class="keyword-score"><strong>${result.keywordScore}%</strong> · 키워드 일치 수준이며, 답안의 논리적 정확성을 자동 판정하지 않습니다.</p><ul class="keyword-groups">${result.groups.map((group) => `<li class="${group.matched ? "keyword-matched" : "keyword-missing"}">${escapeHtml(group.label)} · ${group.matched ? "확인" : "누락"}</li>`).join("")}</ul></div>
         <div><h3>감점 위험</h3><ul class="deduction-list">${question.answer.deductionRisks.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></div>`
      : `<div><h3>정답</h3><p>${escapeHtml(handlerFor(question).answerSummary(question))}</p></div>`;
    const selfActions = isSelfGraded ? `<div class="action-row"><button class="button button-primary" type="button" data-self-result="self-understood">이해함</button><button class="button button-danger" type="button" data-self-result="self-review">복습 필요</button></div>` : "";
    return `<section class="feedback ${feedbackClass}"><div class="feedback-head" tabindex="-1">${heading}</div><div class="feedback-body">${model}<div><h3>해설</h3>${renderBlocks(question.explanation)}</div>${selfActions}${sourcesMarkup(question)}</div></section>`;
  }

  function transitionProgress(previous, result, keywordScore = null, countAttempt = true) {
    const masteryStatus = result === "correct" || result === "self-understood"
      ? "mastered"
      : result === "attempted"
        ? "attempted"
      : result === "self-review"
        ? "review"
        : previous.masteryStatus === "mastered" ? "mastered" : "review";
    return {
      attemptCount: previous.attemptCount + (countAttempt ? 1 : 0),
      lastResult: result,
      masteryStatus,
      essayKeywordScore: keywordScore,
      updatedAt: new Date().toISOString()
    };
  }

  function recordResult(question, result, keywordScore = null, countAttempt = true) {
    const previous = state.progress[question.id] || { attemptCount: 0 };
    state.progress[question.id] = transitionProgress(previous, result, keywordScore, countAttempt);
    saveProgress();
  }

  function recordPastExamResult(item, result, countAttempt = true) {
    const previous = state.pastProgress[item.id] || { attemptCount: 0 };
    state.pastProgress[item.id] = transitionProgress(previous, result, null, countAttempt);
    savePastExamProgress();
  }

  function moveOrderItem(question, index, direction) {
    const current = [...(state.orderDrafts[question.id] || question.answer.items.map((item) => item.id))];
    const nextIndex = index + direction;
    if (nextIndex < 0 || nextIndex >= current.length) return;
    [current[index], current[nextIndex]] = [current[nextIndex], current[index]];
    state.orderDrafts[question.id] = current;
    state.focusRequest = { questionId: question.id, target: "order-item", itemId: current[nextIndex] };
    render();
  }

  function moveOrderItemBefore(question, itemId, targetId) {
    if (itemId === targetId) return;
    const current = [...(state.orderDrafts[question.id] || question.answer.items.map((item) => item.id))];
    const fromIndex = current.indexOf(itemId);
    const targetIndex = current.indexOf(targetId);
    if (fromIndex < 0 || targetIndex < 0) return;
    current.splice(fromIndex, 1);
    current.splice(current.indexOf(targetId), 0, itemId);
    state.orderDrafts[question.id] = current;
    state.focusRequest = { questionId: question.id, target: "order-item", itemId };
    render();
  }

  function currentProgress() {
    return state.contentKind === "past-exam" ? state.pastProgress : state.progress;
  }

  function progressBadges(item) {
    const record = currentProgress()[item.id];
    if (!record) return "";
    const attempted = record.masteryStatus === "attempted" ? '<span class="badge badge-attempted">풀이함</span>' : "";
    const mastery = record.masteryStatus === "mastered" ? '<span class="badge badge-mastered">정답 완료</span>' : "";
    const review = record.lastResult === "incorrect" || record.lastResult === "self-review" ? '<span class="badge badge-review">복습 필요</span>' : "";
    return attempted || mastery || review ? `${attempted}${mastery}${review}` : "";
  }

  function questionStatus(item) {
    const record = currentProgress()[item.id];
    if (!record) return { id: "unseen", label: "미풀이" };
    if (record.lastResult === "incorrect" || record.lastResult === "self-review") return { id: "review", label: "복습 필요" };
    if (record.masteryStatus === "mastered") return { id: "mastered", label: "정답 완료" };
    return { id: "attempted", label: "풀이함" };
  }

  function renderQuestionNavigator(questions) {
    elements.navigator.innerHTML = questions.map((question, index) => {
      const status = questionStatus(question);
      const current = index === state.index;
      return `<button class="question-step question-step-${status.id}" type="button" data-question-index="${index}" aria-label="문항 ${index + 1}: ${status.label}"${current ? ' aria-current="step"' : ""}>${index + 1}</button>`;
    }).join("");
    elements.navigator.querySelectorAll("[data-question-index]").forEach((button) => button.addEventListener("click", () => {
      state.index = Number(button.dataset.questionIndex);
      state.feedback = null;
      render();
    }));
  }

  function restoreRequestedFocus(question) {
    const request = state.focusRequest;
    if (!request || request.questionId !== question.id) return;
    state.focusRequest = null;
    const target = request.target === "feedback"
      ? elements.card.querySelector(".feedback-head")
      : [...elements.card.querySelectorAll("[data-order-item-id]")].find((item) => item.dataset.orderItemId === request.itemId);
    target?.focus();
  }

  function renderQuestion(question) {
    const topic = topicById.get(question.curriculumId);
    const stage = stageById.get(question.stage);
    const handler = handlerFor(question);
    const refStatus = question.sourceRefs[0]?.status || "inferred";
    const prompt = state.practiceMode === "exam" && question.examPrompt ? question.examPrompt : question.prompt;
    const isExamMode = state.practiceMode === "exam";
    const meta = isExamMode
      ? `<span class="badge badge-active">실전 모드</span>${progressBadges(question)}`
      : `<span class="badge">${escapeHtml(topic.title)}</span><span class="badge">${escapeHtml(stage.label)}</span>${questionOriginBadge(question)}${sourceBadge(refStatus)}${progressBadges(question)}`;
    const actionLabel = stage.grading === "self" ? "모범 답안·채점 기준 보기" : "정답 확인";
    elements.card.innerHTML = `
      <div class="question-meta">${meta}</div>
      <h2 class="question-title">${isExamMode ? "실전 문항" : escapeHtml(question.title)}</h2>
      <div class="prompt">${renderBlocks(prompt)}</div>
      <div class="answer-area">${handler.renderInput(question)}</div>
      <div class="action-row"><button id="submit-answer" class="button button-primary" type="button">${actionLabel}</button><button id="clear-answer" class="button button-quiet" type="button">답 지우기</button><button id="reset-current-question" class="button button-quiet" type="button">이 문항 상태 초기화</button></div>
      ${state.feedback?.questionId === question.id ? feedbackMarkup(question, state.feedback) : ""}`;

    const submitAnswer = () => {
      const result = handler.grade(question);
      if (stage.grading === "self") {
        recordResult(question, "attempted", result.keywordScore);
        state.feedback = { questionId: question.id, ...result };
        state.focusRequest = { questionId: question.id, target: "feedback" };
        render();
        return;
      }
      recordResult(question, result.correct ? "correct" : "incorrect");
      state.feedback = { questionId: question.id, correct: result.correct };
      state.focusRequest = { questionId: question.id, target: "feedback" };
      render();
    };
    elements.card.querySelector("#submit-answer").addEventListener("click", submitAnswer);
    bindAnswerKeyboard(question, stage, submitAnswer);
    elements.card.querySelector("#clear-answer").addEventListener("click", () => {
      if (stage.handler === "order") state.orderDrafts[question.id] = question.answer.items.map((item) => item.id);
      if (stage.grading === "self") delete state.essayDrafts[question.id];
      state.feedback = null;
      render();
    });
    elements.card.querySelector("#reset-current-question").addEventListener("click", () => resetProgress("question"));
    elements.card.querySelectorAll("[data-order-item-id]").forEach((item) => {
      item.addEventListener("keydown", (event) => {
        if (!event.altKey || !["ArrowUp", "ArrowDown"].includes(event.key)) return;
        event.preventDefault();
        moveOrderItem(question, Number(item.dataset.orderIndex), event.key === "ArrowUp" ? -1 : 1);
      });
      item.addEventListener("dragstart", (event) => {
        state.draggedOrderItemId = item.dataset.orderItemId;
        item.classList.add("order-dragging");
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", state.draggedOrderItemId);
      });
      item.addEventListener("dragover", (event) => {
        event.preventDefault();
        if (item.dataset.orderItemId !== state.draggedOrderItemId) item.classList.add("order-drop-target");
      });
      item.addEventListener("dragleave", () => item.classList.remove("order-drop-target"));
      item.addEventListener("drop", (event) => {
        event.preventDefault();
        const itemId = event.dataTransfer.getData("text/plain") || state.draggedOrderItemId;
        moveOrderItemBefore(question, itemId, item.dataset.orderItemId);
      });
      item.addEventListener("dragend", () => {
        state.draggedOrderItemId = null;
        elements.card.querySelectorAll("[data-order-item-id]").forEach((candidate) => candidate.classList.remove("order-dragging", "order-drop-target"));
      });
    });
    elements.card.querySelectorAll("[data-self-result]").forEach((button) => button.addEventListener("click", () => {
      recordResult(question, button.dataset.selfResult, state.feedback?.keywordScore ?? null, false);
      state.feedback = { ...state.feedback, questionId: question.id, correct: null };
      state.focusRequest = { questionId: question.id, target: "feedback" };
      render();
    }));
    restoreRequestedFocus(question);
  }

  function renderPastExamItem(item) {
    const isExamMode = state.practiceMode === "exam";
    const feedback = state.feedback?.questionId === item.id
      ? `<section class="feedback feedback-self"><div class="feedback-head" tabindex="-1">복원 답안과 검증 문구</div><div class="feedback-body"><div><h3>복원 답안</h3><div class="past-exam-text">${formatPastExamText(item.answer)}</div></div><div><h3>검증 문구</h3><p>${escapeHtml(item.verification)}</p></div><div class="action-row"><button class="button button-primary" type="button" data-past-result="self-understood">정답 완료</button><button class="button button-danger" type="button" data-past-result="self-review">복습 필요</button></div>${sourcesMarkupFromRefs([item.sourceRef])}</div></section>`
      : "";
    const meta = formatPastExamMeta(item, isExamMode);
    elements.card.innerHTML = `
      <div class="question-meta">${meta}</div>
      <h2 class="question-title">기출 복원 문항</h2>
      <div class="prompt past-exam-text">${formatPastExamText(item.prompt)}</div>
      <div class="answer-area"><div class="answer-field"><label for="past-exam-answer">답안 작성</label><textarea id="past-exam-answer" placeholder="답안을 직접 작성한 뒤 복원 답안을 확인하세요.">${escapeHtml(state.pastDrafts[item.id] || "")}</textarea></div></div>
      <div class="action-row"><button id="reveal-past-exam-answer" class="button button-primary" type="button">복원 답안 보기</button><button id="clear-past-exam-answer" class="button button-quiet" type="button">답 지우기</button><button id="reset-current-question" class="button button-quiet" type="button">이 문항 상태 초기화</button></div>
      ${feedback}`;

    elements.card.querySelector("#reveal-past-exam-answer").addEventListener("click", () => {
      state.pastDrafts[item.id] = elements.card.querySelector("#past-exam-answer")?.value || "";
      recordPastExamResult(item, "attempted");
      state.feedback = { questionId: item.id, correct: null };
      state.focusRequest = { questionId: item.id, target: "feedback" };
      render();
    });
    elements.card.querySelector("#clear-past-exam-answer").addEventListener("click", () => {
      delete state.pastDrafts[item.id];
      state.feedback = null;
      render();
    });
    elements.card.querySelector("#reset-current-question").addEventListener("click", () => resetProgress("question"));
    elements.card.querySelectorAll("[data-past-result]").forEach((button) => button.addEventListener("click", () => {
      recordPastExamResult(item, button.dataset.pastResult, false);
      state.feedback = { questionId: item.id, correct: null };
      state.focusRequest = { questionId: item.id, target: "feedback" };
      render();
    }));
    restoreRequestedFocus(item);
  }

  function bindAnswerKeyboard(question, stage, submitAnswer) {
    if (stage.handler === "short") {
      elements.card.querySelector("#answer-main")?.addEventListener("keydown", (event) => {
        if (event.key !== "Enter" || event.isComposing) return;
        event.preventDefault();
        submitAnswer();
      });
      return;
    }
    if (stage.handler !== "cloze") return;
    const inputs = [...elements.card.querySelectorAll(".cloze-grid input")];
    inputs.forEach((input, index) => input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" || event.isComposing) return;
      event.preventDefault();
      const nextInput = inputs[index + 1];
      if (nextInput) {
        nextInput.focus();
        return;
      }
      submitAnswer();
    }));
  }

  function renderStats() {
    const items = getActiveItems();
    const records = Object.values(currentProgress());
    elements.statTotal.textContent = state.contentKind === "past-exam" ? pastExamItems.length : data.questions.length;
    elements.statComplete.textContent = records.length;
    elements.statMastered.textContent = records.filter((record) => record.masteryStatus === "mastered").length;
    elements.statReview.textContent = records.filter((record) => record.lastResult === "incorrect" || record.lastResult === "self-review").length;
    elements.statFiltered.textContent = items.length;
  }

  function renderStorageNotice() {
    elements.storageNotice.hidden = storageAvailable;
  }

  function renderFilterSummary() {
    if (state.contentKind === "past-exam") {
      const labels = ["기출 복원"];
      if (state.pastYear !== "all") labels.push(elements.pastYear.selectedOptions[0]?.textContent);
      if (state.pastRound !== "all") labels.push(elements.pastRound.selectedOptions[0]?.textContent);
      if (state.pastType !== "all") labels.push(elements.pastType.selectedOptions[0]?.textContent);
      if (state.reviewOnly) labels.push("복습 필요");
      elements.filterSummary.textContent = labels.join(" · ");
      return;
    }
    const labels = [];
    if (state.learningPath !== "all") labels.push(elements.learningPath.selectedOptions[0]?.textContent);
    if (state.source !== "all") labels.push(elements.source.selectedOptions[0]?.textContent);
    if (state.topic !== "all") labels.push(elements.topic.selectedOptions[0]?.textContent);
    if (state.stage !== "all") labels.push(elements.stage.selectedOptions[0]?.textContent);
    if (state.reviewOnly) labels.push("복습 필요");
    elements.filterSummary.textContent = labels.length ? `선택됨 · ${labels.join(" · ")}` : "전체 학습 범위";
  }

  function renderPracticeMode() {
    elements.practiceMode.querySelectorAll("[data-practice-mode]").forEach((button) => {
      const selected = button.dataset.practiceMode === state.practiceMode;
      button.setAttribute("aria-pressed", String(selected));
    });
  }

  function renderContentKindFilters() {
    const isPastExam = state.contentKind === "past-exam";
    [elements.pastYearGroup, elements.pastRoundGroup, elements.pastTypeGroup].forEach((element) => { element.hidden = !isPastExam; });
    [elements.learningPath, elements.source, elements.topic, elements.stage].forEach((element) => { element.closest(".filter-group").hidden = isPastExam; });
    elements.futureTopics.closest(".future-topics").hidden = isPastExam;
    elements.contentKind.value = state.contentKind;
    elements.resetAll.textContent = isPastExam ? "기출 복원 전체 진행도 초기화" : "학습 문항 전체 진행도 초기화";
  }

  function navigateQuestion(direction) {
    const questions = getActiveItems();
    const nextIndex = Math.max(0, Math.min(state.index + direction, questions.length - 1));
    if (!questions.length || nextIndex === state.index) return;
    state.index = nextIndex;
    state.feedback = null;
    render();
  }

  function renderQuestionNavigation(questions) {
    const previousDisabled = !questions.length || state.index === 0;
    const nextDisabled = !questions.length || state.index >= questions.length - 1;
    elements.previous.disabled = previousDisabled;
    elements.next.disabled = nextDisabled;
    elements.quickNavigation.hidden = !questions.length;
    elements.quickPrevious.disabled = previousDisabled;
    elements.quickNext.disabled = nextDisabled;
    elements.quickPosition.textContent = `문항 ${questions.length ? state.index + 1 : 0} / ${questions.length}`;
  }

  function render() {
    const questions = getActiveItems();
    renderStats();
    renderFilterSummary();
    renderPracticeMode();
    renderContentKindFilters();
    renderThemeToggle();
    renderStorageNotice();
    renderQuestionNavigation(questions);
    if (!questions.length) {
      elements.position.textContent = "문항 0 / 0";
      elements.navigator.replaceChildren();
      elements.card.replaceChildren(document.querySelector("#empty-template").content.cloneNode(true));
      return;
    }
    const question = getCurrentItem();
    elements.position.textContent = `문항 ${state.index + 1} / ${questions.length}`;
    renderQuestionNavigator(questions);
    if (state.contentKind === "past-exam") renderPastExamItem(question);
    else renderQuestion(question);
  }

  function resetProgress(scope) {
    const message = scope === "all"
      ? `${state.contentKind === "past-exam" ? "기출 복원" : "학습 문항"} 전체 진행도를 초기화할까요?`
      : scope === "question"
        ? "이 문항의 진행도를 초기화할까요?"
        : "현재 선택 범위의 진행도를 초기화할까요?";
    if (!window.confirm(message)) return;
    const question = getCurrentItem();
    const progress = currentProgress();
    if (scope === "all") {
      if (state.contentKind === "past-exam") {
        state.pastProgress = {};
        state.pastDrafts = {};
      } else {
        state.progress = {};
        state.orderDrafts = {};
        state.essayDrafts = {};
      }
    } else {
      const ids = scope === "question"
        ? new Set(question ? [question.id] : [])
        : new Set(getActiveItems().map((filteredQuestion) => filteredQuestion.id));
      Object.keys(progress).forEach((id) => { if (ids.has(id)) delete progress[id]; });
      if (state.contentKind === "past-exam") Object.keys(state.pastDrafts).forEach((id) => { if (ids.has(id)) delete state.pastDrafts[id]; });
      else {
        Object.keys(state.orderDrafts).forEach((id) => { if (ids.has(id)) delete state.orderDrafts[id]; });
        Object.keys(state.essayDrafts).forEach((id) => { if (ids.has(id)) delete state.essayDrafts[id]; });
      }
    }
    if (state.contentKind === "past-exam") savePastExamProgress();
    else saveProgress();
    state.feedback = null;
    render();
  }

  function initializeFilters() {
    const activePaths = data.curriculum.learningPaths.filter((path) => path.status === "active");
    const sourceGroups = [...new Map(activeTopics.map((topic) => [`${topic.sourceChapter}:${topic.sourceSection}`, topic])).values()];
    elements.learningPath.innerHTML = `<option value="all">현재 학습 경로 전체</option>${activePaths.map((path) => `<option value="${escapeHtml(path.id)}">${escapeHtml(path.title)}</option>`).join("")}`;
    elements.source.innerHTML = `<option value="all">현재 원본 범위 전체</option>${sourceGroups.map((topic) => `<option value="${escapeHtml(`${topic.sourceChapter}:${topic.sourceSection}`)}">${escapeHtml(`${topic.sourceChapter}장 · ${topic.sourceSection}`)}</option>`).join("")}`;
    elements.topic.innerHTML = `<option value="all">현재 세부 주제 전체</option>${activeTopics.map((topic) => `<option value="${escapeHtml(topic.id)}">${escapeHtml(formatTopicLabel(topic))}</option>`).join("")}`;
    elements.stage.innerHTML = `<option value="all">전체 단계</option>${[...stageById.entries()].map(([id, stage]) => `<option value="${escapeHtml(id)}">${escapeHtml(stage.label)}</option>`).join("")}`;
    const years = [...new Set(data.pastExams.rounds.map((round) => round.year))].sort();
    elements.pastYear.innerHTML = `<option value="all">전체 연도</option>${years.map((year) => `<option value="${escapeHtml(year)}">${escapeHtml(`${year}년`)}</option>`).join("")}`;
    elements.pastRound.innerHTML = `<option value="all">전체 회차</option>${data.pastExams.rounds.map((round) => `<option value="${escapeHtml(round.roundId)}">${escapeHtml(`${round.roundId} · ${round.year}년 ${Number(round.session)}회`)}</option>`).join("")}`;
    elements.pastType.innerHTML = '<option value="all">전체 유형</option><option value="short">단답</option><option value="essay">서술</option><option value="practical">실무형</option>';
    const future = data.curriculum.topics.filter((topic) => topic.status === "future");
    elements.futureTopics.innerHTML = future.map((topic) => `<li>${escapeHtml(formatTopicLabel(topic))}</li>`).join("");
    elements.learningPath.addEventListener("change", () => { state.learningPath = elements.learningPath.value; state.index = 0; state.feedback = null; render(); });
    elements.source.addEventListener("change", () => { state.source = elements.source.value; state.index = 0; state.feedback = null; render(); });
    elements.topic.addEventListener("change", () => { state.topic = elements.topic.value; state.index = 0; state.feedback = null; render(); });
    elements.stage.addEventListener("change", () => { state.stage = elements.stage.value; state.index = 0; state.feedback = null; render(); });
    elements.contentKind.addEventListener("change", () => { state.contentKind = elements.contentKind.value; state.index = 0; state.feedback = null; render(); });
    elements.pastYear.addEventListener("change", () => { state.pastYear = elements.pastYear.value; state.index = 0; state.feedback = null; render(); });
    elements.pastRound.addEventListener("change", () => { state.pastRound = elements.pastRound.value; state.index = 0; state.feedback = null; render(); });
    elements.pastType.addEventListener("change", () => { state.pastType = elements.pastType.value; state.index = 0; state.feedback = null; render(); });
    elements.review.addEventListener("change", () => { state.reviewOnly = elements.review.checked; state.index = 0; state.feedback = null; render(); });
    elements.practiceMode.querySelectorAll("[data-practice-mode]").forEach((button) => button.addEventListener("click", () => {
      state.practiceMode = button.dataset.practiceMode;
      state.feedback = null;
      render();
    }));
    elements.themeToggle.addEventListener("click", toggleTheme);
    elements.resetFilters.addEventListener("click", () => {
      state.learningPath = "all";
      state.source = "all";
      state.topic = "all";
      state.stage = "all";
      state.pastYear = "all";
      state.pastRound = "all";
      state.pastType = "all";
      state.reviewOnly = false;
      elements.learningPath.value = "all";
      elements.source.value = "all";
      elements.topic.value = "all";
      elements.stage.value = "all";
      elements.pastYear.value = "all";
      elements.pastRound.value = "all";
      elements.pastType.value = "all";
      elements.review.checked = false;
      state.index = 0;
      state.feedback = null;
      render();
    });
    elements.previous.addEventListener("click", () => navigateQuestion(-1));
    elements.next.addEventListener("click", () => navigateQuestion(1));
    elements.quickPrevious.addEventListener("click", () => navigateQuestion(-1));
    elements.quickNext.addEventListener("click", () => navigateQuestion(1));
    elements.resetTopic.addEventListener("click", () => resetProgress("topic"));
    elements.resetAll.addEventListener("click", () => resetProgress("all"));
    document.addEventListener("keydown", (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
        event.preventDefault();
        elements.card.querySelector("#submit-answer")?.click();
      }
    });
    if (systemThemeQuery?.addEventListener) systemThemeQuery.addEventListener("change", syncSystemThemeLabel);
    else systemThemeQuery?.addListener?.(syncSystemThemeLabel);
  }

  initializeFilters();
  render();
})();
