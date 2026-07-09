---
title: "Lab 01 Linux Hardening Cleanup"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, cleanup, linux-hardening]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "README.md"
source_count: 1
provenance: inferred
summary: "Linux hardening Lab 산출물 정리 절차."
evergreen: false
---

# Cleanup

From `labs/info-sec-engineer-practical`:

```bash
./bin/clean-lab.sh 01-linux-hardening
```

The cleanup command removes only:

```text
labs/01-linux-hardening/.sandbox/
```
