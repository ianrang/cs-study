---
title: "Lab 05 IDS Log Triage Expected Observations"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, expected-observations, ids, log-triage]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "questions.md"
source_count: 1
provenance: inferred
summary: "IDS log triage Lab 질문의 기대 관찰값."
evergreen: false
---

# Expected Observations

| Question | Expected |
|---|---|
| Q1 | `msg` labels alert, `content` matches payload, `nocase` ignores case, `depth` limits search range, `threshold` controls alert frequency, `sid` identifies rule. |
| Q2 | Repeated HTTP GET request pattern from a source within a short time window. |
| Q3 | Broad rules inspect irrelevant traffic and may classify normal traffic as malicious. |
| Q4 | SIEM correlates IDS alert source/destination with web logs, time, URL, status, and user agent. |
| Q5 | A good answer includes evidence, impact/risk, containment, log preservation, and tuning or blocking action. |
