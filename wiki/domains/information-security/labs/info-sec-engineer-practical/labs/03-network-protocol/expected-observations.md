---
title: "Lab 03 Network Protocol Expected Observations"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, expected-observations, network-protocol]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "questions.md"
source_count: 1
provenance: inferred
summary: "Network protocol Lab 질문의 기대 관찰값."
evergreen: false
---

# Expected Observations

| Question | Expected |
|---|---|
| Q1 | It is TCP half-open/SYN scan. 25 open, 443 closed, 110 filtered/no response. |
| Q2 | Yes. Gateway IP has a MAC different from the expected MAC and shared with another host. |
| Q3 | OUTPUT chain, ICMP protocol, echo request type 8, DROP action. |
| Q4 | Spoofed source causes reflected responses toward a victim; ANY can produce large responses. |
| Q5 | Mention source validation, directed broadcast disable, open resolver restriction, ACL/uRPF/rate limiting. |
