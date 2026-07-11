---
title: "Lab 01 Linux Hardening"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab, linux-hardening]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "../../README.md"
source_count: 1
provenance: inferred
summary: "Linux/Unix 계정 파일, 로그, 권한, 명령어를 시험 답안 형태로 해석하는 독립 Lab."
evergreen: false
---

# Lab 01. Linux Hardening

## Objective
Linux/Unix 계정 파일, 로그, 권한, 명령어를 시험 답안 형태로 해석한다.

## Exam Pattern
- `/etc/passwd`, `/etc/shadow` 필드 의미
- `$1$`, `$5$`, `$6$` 해시 식별자
- `utmp`, `wtmp`, `btmp`, `lastlog`, `lastcomm`, `lsof`
- SUID, SGID, sticky bit, world-writable, umask

## Run
```bash
sh ./run.sh
```

Generated files stay under `.sandbox/`.

## Forbidden
- Do not read or modify host `/etc/passwd` or `/etc/shadow`.
- Do not create host users.
- Do not change host SSH, PAM, or shell profile settings.
