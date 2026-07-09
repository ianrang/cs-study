---
title: "Lab 02 Service Config Expected Observations"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, expected-observations, service-config]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "questions.md"
source_count: 1
provenance: inferred
summary: "Service config Lab 질문의 기대 관찰값."
evergreen: false
---

# Expected Observations

| Question | Expected |
|---|---|
| Q1 | `Options Indexes` enables directory listing. Use `Options -Indexes` or remove `Indexes`. |
| Q2 | TRACE can expose request data and is usually disabled with `TraceEnable Off`. |
| Q3 | Zone transfer to `any` can expose internal DNS records. Restrict it to trusted secondary DNS IPs. |
| Q4 | `RELAY` permits mail relay for listed hosts. `REJECT` denies the listed domain or host. |
| Q5 | Disable unnecessary services, set `only_from`, `no_access`, finite `instances`, and access time limits. |
