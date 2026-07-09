---
title: "Lab 02 Service Config"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, service-config]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "../../README.md"
source_count: 1
provenance: inferred
summary: "Apache, BIND, SMTP, xinetd 설정 샘플에서 취약 설정과 보완 조치를 찾는 독립 Lab."
evergreen: false
---

# Lab 02. Service Config

## Objective
Apache, BIND, SMTP, xinetd 설정 샘플에서 취약 설정과 보완 조치를 찾는다.

## Exam Pattern
- Apache `Options Indexes`, `TraceEnable`
- DNS zone transfer and `allow-transfer`
- SMTP relay restriction and access database
- xinetd `disable`, `only_from`, `no_access`, `instances`, `access_time`

## Run
```bash
sh ./run.sh
```

Generated files stay under `.sandbox/`.
