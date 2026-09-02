import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const practiceRoot = resolve(import.meta.dirname, "..");
const appSource = readFileSync(resolve(practiceRoot, "app.js"), "utf8");
const formatterStart = appSource.indexOf("  function escapeHtml");
const formatterEnd = appSource.indexOf("  function loadProgress");

if (formatterStart < 0 || formatterEnd < 0) {
  throw new Error("past-exam formatter boundaries not found in app.js");
}

// app.js intentionally remains a browser IIFE. Evaluate only the two pure
// formatting helpers so this test exercises the production implementation.
const { formatPastExamText, formatPastExamRoundLabel } = Function(
  `${appSource.slice(formatterStart, formatterEnd)}\nreturn { formatPastExamText, formatPastExamRoundLabel };`
)();

const pastExams = JSON.parse(
  readFileSync(resolve(practiceRoot, "data/generated/past-exams.json"), "utf8")
);
const items = pastExams.rounds.flatMap((round) => round.items);
const byId = (id) => items.find((item) => item.id === id);
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const topLevelLabels = (value) => [
  ...String(value).matchAll(/(?:^|<br>|\s)(?:\(([A-Z가-힣]|\d{1,2})\)(?::|\s)|([A-Z가-힣])\s*:)/g),
].map((match) => match[1] || match[2]);

const legacyItem = byId("R01-Q04");
const explicitItem = byId("R07-Q02");
const snortItem = byId("R07-Q04");
const referenceItem = byId("R08-Q06");

assert(legacyItem, "R01-Q04 must exist");
assert(explicitItem, "R07-Q02 must exist");
assert(snortItem, "R07-Q04 must exist");
assert(referenceItem, "R08-Q06 must exist");
assert(
  formatPastExamRoundLabel({ year: "2016", session: "01", roundId: "R07" }) === "2016년 1회 · R07",
  "past-exam round identity must use the shared year/session/round formatter"
);
assert(
  formatPastExamText(legacyItem.answer) === "(A) lastlog<br>(B) sulog<br>(C) loginlog",
  "legacy A : / B : / C : answer labels must render as labeled lines"
);
assert(
  (formatPastExamText(legacyItem.prompt).match(/<br>/g) || []).length >= 3,
  "legacy prompt labels must render as separate lines"
);
assert(
  formatPastExamText(explicitItem.answer).includes("(C) `JMP ESP`"),
  "R07-Q02 must preserve JMP ESP as the third answer"
);
assert(
  !formatPastExamText("<img src=x onerror=alert(1)>").includes("<img"),
  "source text must be HTML-escaped before presentation markers are rendered"
);
assert(
  formatPastExamText(snortItem.prompt).includes('class="exam-code-block" data-language="snort"'),
  "actual Snort reconstruction must render through the generic code-block component"
);
assert(
  formatPastExamText(referenceItem.prompt).includes('class="exam-reference-block"'),
  "actual TCP flow reconstruction must render through the generic reference-block component"
);
const escapedCodeBlock = formatPastExamText("{{code:html}}<img src=x>\\nvalue{{/code}}");
assert(
  escapedCodeBlock.includes("&lt;img src=x&gt;\nvalue") && !escapedCodeBlock.includes("<img src=x>"),
  "code-block content must remain HTML-escaped while preserving explicit line breaks"
);

for (const item of items) {
  if (topLevelLabels(item.prompt).length > 1) {
    assert(
      formatPastExamText(item.prompt).includes("<br>"),
      `${item.id} multi-slot prompt must render as separate lines`
    );
  }
  if (topLevelLabels(item.answer).length > 1) {
    assert(
      formatPastExamText(item.answer).includes("<br>"),
      `${item.id} multi-slot answer must render as separate lines`
    );
  }
}

console.log("past-exam rendering contract passed");
