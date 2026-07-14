(() => {
  "use strict";

  const data = window.PRACTICE_DATA;
  const core = window.PRACTICE_CORE;
  const storageKey = "info-security-practice-progress-v1";
  const root = document.documentElement;
  const themeStorageKey = root.dataset.themeStorageKey;
  const systemThemeQuery = window.matchMedia?.("(prefers-color-scheme: dark)");
  let storageAvailable = true;
  const state = {
    learningPath: "all",
    source: "all",
    topic: "all",
    stage: "all",
    reviewOnly: false,
    practiceMode: "learning",
    index: 0,
    feedback: null,
    orderDrafts: {},
    essayDrafts: {},
    draggedOrderItemId: null,
    focusRequest: null,
    progress: loadProgress(),
    themePreference: loadThemePreference()
  };
  const elements = {
    learningPath: document.querySelector("#learning-path-filter"),
    source: document.querySelector("#source-filter"),
    topic: document.querySelector("#topic-filter"),
    stage: document.querySelector("#stage-filter"),
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

  if (!data || !data.curriculum || !Array.isArray(data.curriculum.learningPaths) || !Array.isArray(data.curriculum.stages) || !Array.isArray(data.curriculum.topics) || !Array.isArray(data.questions) || !core) {
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

  function loadProgress() {
    try {
      const stored = localStorage.getItem(storageKey);
      if (!stored) return {};
      const parsed = JSON.parse(stored);
      if (!parsed || parsed.schemaVersion !== 1 || !parsed.records || typeof parsed.records !== "object") return {};
      const knownQuestionIds = new Set((data?.questions || []).map((question) => question.id));
      return Object.fromEntries(Object.entries(parsed.records)
        .filter(([id]) => knownQuestionIds.has(id))
        .map(([id, record]) => [id, core.normalizeProgressRecord(record)])
        .filter(([, record]) => record !== null));
    } catch {
      storageAvailable = false;
      return {};
    }
  }

  function saveProgress() {
    try {
      localStorage.setItem(storageKey, JSON.stringify({ schemaVersion: 1, records: state.progress }));
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
    return data.questions.filter((question) => {
      const topic = topicById.get(question.curriculumId);
      const learningPathMatches = state.learningPath === "all" || topic.learningPath === state.learningPath;
      const sourceMatches = state.source === "all" || `${topic.sourceChapter}:${topic.sourceSection}` === state.source;
      const topicMatches = state.topic === "all" || question.curriculumId === state.topic;
      const activeMatches = topic.status === "active";
      const stageMatches = state.stage === "all" || question.stage === state.stage;
      const record = state.progress[question.id];
      const reviewMatches = !state.reviewOnly || record?.lastResult === "incorrect" || record?.lastResult === "self-review";
      return activeMatches && learningPathMatches && sourceMatches && topicMatches && stageMatches && reviewMatches;
    });
  }

  function getCurrentQuestion() {
    const questions = getFilteredQuestions();
    if (!questions.length) return null;
    state.index = Math.max(0, Math.min(state.index, questions.length - 1));
    return questions[state.index];
  }

  function sourceBadge(status) {
    const label = status === "source-derived" ? "복원·파생 근거" : status === "inferred" ? "학습용 추론" : "공식 근거";
    return `<span class="badge badge-${escapeHtml(status)}">${label}</span>`;
  }

  function questionOriginBadge(question) {
    if (question.questionKind === "predicted") return '<span class="badge badge-predicted">예상 문제 · 분석 근거</span>';
    if (question.sourceRefs.some((ref) => ref.path.includes("datasets/info-sec-engineer-practical-past-exams/01-rounds/"))) {
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
      matched: group.terms.some((term) => normalizedResponse.includes(normalize(term)))
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

  function sourcesMarkup(question) {
    const refs = question.sourceRefs.map((ref) => `<li><code>${escapeHtml(ref.path)}:${escapeHtml(ref.line)}</code> · ${escapeHtml(ref.status)}<br /><span>확인 문구: ${escapeHtml(ref.excerpt)}</span></li>`).join("");
    return `<details><summary>근거와 검증 상태</summary><ul class="source-list">${refs}</ul></details>`;
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

  function progressBadges(question) {
    const record = state.progress[question.id];
    if (!record) return "";
    const attempted = record.masteryStatus === "attempted" ? '<span class="badge badge-attempted">풀이함</span>' : "";
    const mastery = record.masteryStatus === "mastered" ? '<span class="badge badge-mastered">정답 완료</span>' : "";
    const review = record.lastResult === "incorrect" || record.lastResult === "self-review" ? '<span class="badge badge-review">복습 필요</span>' : "";
    return attempted || mastery || review ? `${attempted}${mastery}${review}` : "";
  }

  function questionStatus(question) {
    const record = state.progress[question.id];
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
    const records = Object.values(state.progress);
    elements.statTotal.textContent = data.questions.length;
    elements.statComplete.textContent = records.length;
    elements.statMastered.textContent = records.filter((record) => record.masteryStatus === "mastered").length;
    elements.statReview.textContent = records.filter((record) => record.lastResult === "incorrect" || record.lastResult === "self-review").length;
    elements.statFiltered.textContent = getFilteredQuestions().length;
  }

  function renderStorageNotice() {
    elements.storageNotice.hidden = storageAvailable;
  }

  function renderFilterSummary() {
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

  function render() {
    const questions = getFilteredQuestions();
    renderStats();
    renderFilterSummary();
    renderPracticeMode();
    renderThemeToggle();
    renderStorageNotice();
    elements.previous.disabled = !questions.length || state.index === 0;
    elements.next.disabled = !questions.length || state.index >= questions.length - 1;
    if (!questions.length) {
      elements.position.textContent = "문항 0 / 0";
      elements.navigator.replaceChildren();
      elements.card.replaceChildren(document.querySelector("#empty-template").content.cloneNode(true));
      return;
    }
    const question = getCurrentQuestion();
    elements.position.textContent = `문항 ${state.index + 1} / ${questions.length}`;
    renderQuestionNavigator(questions);
    renderQuestion(question);
  }

  function resetProgress(scope) {
    const message = scope === "all"
      ? "전체 진행도를 초기화할까요?"
      : scope === "question"
        ? "이 문항의 진행도를 초기화할까요?"
        : "현재 선택 범위의 진행도를 초기화할까요?";
    if (!window.confirm(message)) return;
    const question = getCurrentQuestion();
    if (scope === "all") {
      state.progress = {};
      state.orderDrafts = {};
      state.essayDrafts = {};
    } else {
      const ids = scope === "question"
        ? new Set(question ? [question.id] : [])
        : new Set(getFilteredQuestions().map((filteredQuestion) => filteredQuestion.id));
      Object.keys(state.progress).forEach((id) => { if (ids.has(id)) delete state.progress[id]; });
      Object.keys(state.orderDrafts).forEach((id) => { if (ids.has(id)) delete state.orderDrafts[id]; });
      Object.keys(state.essayDrafts).forEach((id) => { if (ids.has(id)) delete state.essayDrafts[id]; });
    }
    saveProgress();
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
    const future = data.curriculum.topics.filter((topic) => topic.status === "future");
    elements.futureTopics.innerHTML = future.map((topic) => `<li>${escapeHtml(formatTopicLabel(topic))}</li>`).join("");
    elements.learningPath.addEventListener("change", () => { state.learningPath = elements.learningPath.value; state.index = 0; state.feedback = null; render(); });
    elements.source.addEventListener("change", () => { state.source = elements.source.value; state.index = 0; state.feedback = null; render(); });
    elements.topic.addEventListener("change", () => { state.topic = elements.topic.value; state.index = 0; state.feedback = null; render(); });
    elements.stage.addEventListener("change", () => { state.stage = elements.stage.value; state.index = 0; state.feedback = null; render(); });
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
      state.reviewOnly = false;
      elements.learningPath.value = "all";
      elements.source.value = "all";
      elements.topic.value = "all";
      elements.stage.value = "all";
      elements.review.checked = false;
      state.index = 0;
      state.feedback = null;
      render();
    });
    elements.previous.addEventListener("click", () => { state.index -= 1; state.feedback = null; render(); });
    elements.next.addEventListener("click", () => { state.index += 1; state.feedback = null; render(); });
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
