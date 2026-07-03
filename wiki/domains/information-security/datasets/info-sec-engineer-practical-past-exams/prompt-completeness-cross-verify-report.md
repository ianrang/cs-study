---
title: "정보보안기사 실기 기출 문항 설명 완전성 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, prompt-completeness, verification]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "2013-01-practical-01.md"
  - "2013-02-practical-02.md"
  - "2014-01-practical-03.md"
  - "2014-02-practical-04.md"
  - "2015-01-practical-05.md"
  - "2015-02-practical-06.md"
  - "2016-01-practical-07.md"
  - "2016-02-practical-08.md"
  - "2017-01-practical-09.md"
  - "2017-02-practical-10.md"
  - "2018-01-practical-11.md"
  - "2018-02-practical-12.md"
  - "2019-01-practical-13.md"
  - "2022-04-practical-21.md"
source_count: 14
provenance: inferred
summary: "회차별 기출 복원표에서 설명이 빠진 지시문을 탐지하고, 접근 가능한 복원 원천 기준으로 문항 조건·구분 기준·답안 정합성을 보강한 교차검증 결과."
evergreen: false
---

# 정보보안기사 실기 기출 문항 설명 완전성 교차검증 리포트

## Verdict
- Prompt completeness: pass within accessible reconstruction scope. 기계 스캔으로 탐지한 설명 누락·과압축 후보 48건 중 실제 보강 대상은 회차 파일에 반영했다.
- Logic consistency: pass. 보강된 지시문은 기존 답안과 모순되지 않도록 공격 조건, 법령·관리 기준, 프로토콜 기능, 파일·로그 의미를 답안 단위와 맞췄다.
- Accuracy boundary: scoped. 공식 PDF 비밀번호가 없어 공식 원문 문구 일치까지는 주장하지 않는다.
- Known source limit: resolved. 사용자 제공 원천 이미지로 남아 있던 설명 본문 누락 2건을 대조해 회차 파일에 반영했다.

## Finding Summary
| severity | count | status |
|---|---:|---|
| HIGH | 0 | resolved |
| MEDIUM | 0 | resolved or false positive |
| KNOWN_LIMITED | 0 | resolved |

## Corrected Scope
| file | corrected item scope |
|---|---|
| `2013-01-practical-01.md` | 위험평가, NMS, 보안정책 문서체계, 개인정보 처리자/취급자/처리시스템 지시문 보강 |
| `2013-02-practical-02.md` | ingress/egress/blackhole, FTP 계열 공격, TCP Wrapper, Smurf, switch jamming 지시문 보강 |
| `2014-01-practical-03.md` | SYN flooding, ISMS, XSS, Teardrop 지시문 보강 |
| `2014-02-practical-04.md` | 웹 프록시 도구, IDS 오탐/미탐 지시문 보강 |
| `2015-01-practical-05.md` | journaling, CVE, 개인정보 안전성 확보조치, 업로드/SQL injection, CIA/BIA 지시문 보강 |
| `2015-02-practical-06.md` | 예방 통제·물리적 접근 통제·논리적 접근 통제 구분 보강 |
| `2016-01-practical-07.md` | dropper/injector, webshell, cyber kill chain, 내부관리계획 지시문 보강 |
| `2016-02-practical-08.md` | `/proc` 지시문 보강 |
| `2017-01-practical-09.md` | hosts 파일, Delphi method 지시문 보강 |
| `2017-02-practical-10.md` | DR 사이트 유형 문제의 A/B/C 설명을 사용자 제공 원천 이미지로 대조해 보강 |
| `2018-01-practical-11.md` | BitLocker, Slow HTTP Header, supply-chain attack 지시문 보강 |
| `2018-02-practical-12.md` | Malvertising, CR/LF 기반 HTTP 응답 분할 지시문 보강 |
| `2019-01-practical-13.md` | ARP spoofing, ISAC, Memcached DDoS, `login.defs`, baseline approach, BCP 지시문 보강 |
| `2022-04-practical-21.md` | IPSec/AH/ESP 빈칸 문제를 독립 복원 원천으로 교차 확인해 보강 |
| `2025-01-practical-28.md` | Shell 역할·주요 기능 문항의 메타 표현을 시험 지시문 형태로 정규화 |

## Remaining Tracked Limit
No prompt-completeness known-limited item remains after user-provided source image cross-check.

## False Positives
| file | no | reason |
|---|---:|---|
| `2024-01-practical-25.md` | 12 | SOAR 설명 bullet이 이미 포함되어 있어 설명 누락 아님 |
| `2024-04-practical-27.md` | 5 | `utmp`, `wtmp`, `lastlog`별 로그 설명이 이미 포함되어 있어 설명 누락 아님 |

## Method
- Parsed all same-directory `*-practical-*.md` reconstruction tables.
- Flagged vague prompt patterns such as `다음에서 설명하는`, `다음 설명`, `다음 빈칸`, `빈칸`, `보기`, `(A)` when no usable condition text was present.
- Cross-checked accessible web reconstruction sources where available.
- Cross-checked user-provided source images for `2017-02-practical-10.md` #7 and `2018-02-practical-12.md` #3.
- Preserved source limits rather than inventing official wording when reconstruction sources lacked the original description body.
