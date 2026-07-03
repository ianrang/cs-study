---
title: "정보보안기사 실기 빈도 분석 유의미성 검토"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-analysis, significance]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "frequency-analysis.md"
  - "recurrence-analysis.md"
  - "pattern-analysis.md"
  - "item-reference-map.md"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 빈도·재출제 결과를 최근성, 출제기준 중요도, 근거 신뢰도 관점에서 해석한 유의미성 검토."
evergreen: false
---

# 정보보안기사 실기 빈도 분석 유의미성 검토

## Review Criteria
| criterion | meaning |
|---|---|
| frequency | 1~30회 전체 반복 횟수 |
| recency | 23~30회 최근 출제 강도 |
| transformability | 단답·서술·실무형으로 변형 가능한 정도 |
| source confidence | `item-reference-map.md`의 23~30회 reference confidence |
| exam-scope fit | KCA 실기 출제기준 세부항목과의 직접성 |

## Significant Topics
| rank | topic | significance | reason |
|---:|---|---|---|
| 1 | 위험관리/위험평가 | very high | 전 30회 등장, 최근 25건 탐지, 위험평가 criteria 12건과 직접 연결된다. |
| 2 | 접근통제/권한관리 | very high | 28개 회차에서 반복되고 OS/법규/관리체계를 모두 가로지른다. |
| 3 | 서비스 보안설정 점검 | very high | 23~30회 KCA 세부항목 중 최다 28건이다. 웹/DB/DNS/NTP/메일/Apache 설정으로 변형된다. |
| 4 | 리눅스/유닉스 로그·명령 | high | 최근 23~30회 21건으로 최근성이 강하고 단답 적중 가치가 높다. |
| 5 | 웹 취약점/시큐어코딩 | high | SQL Injection, XSS, SSRF, XXE, 파일 업로드, PreparedStatement 등으로 변형폭이 크다. |
| 6 | DNS/SNMP/VLAN/네트워크장비 | high | 최근 17건이며 네트워크 장비·프로토콜 실무형과 연결된다. |
| 7 | 개인정보/ISMS-P/법규 | high | 전체 56건이나 최근 13건으로 유지형 주제다. 법령 개정성 때문에 최신성 검토가 필요하다. |
| 8 | 악성코드/APT/포렌식 | medium-high | 최근 10건으로 증가 신호가 있으나 개별 원천·용어 정확성 확인이 중요하다. |
| 9 | 무선/모바일 | medium | 전체 빈도는 낮지만 최근 MDM/deep link/무선 표준으로 확장된다. |
| 10 | 데이터베이스/데이터보호 | medium | 빈도는 중간이나 DB 감사·마스킹·DLP가 최근 실무형과 연결된다. |

## Caution Topics
| topic | caution |
|---|---|
| Cyber Kill Chain | `R28-Q6`은 medium confidence로 남아 있어 전용 공식 원천 확보 전까지 근거 강도를 과장하지 않는다. |
| DB 마스킹 방식명 | `R30-Q11`은 개인정보 보호조치와 연결되지만 방식명 직접 원천이 부족하다. |
| EAM/IAM 비교 | `R30-Q15`는 ISMS-P 접근권한 관리와 연결되지만 벤더 용어 차이가 있다. |
| 무선랜 세부 표준 | `R24-Q4`는 KCA 프로토콜 보안특성과 연결되지만 세부 표준 직접 원천이 아직 보강 대상이다. |

## Study Priority Decision
| priority | include in next strategy? | basis |
|---:|---|---|
| 1 | yes | 위험관리/위험평가, 접근통제/권한관리, 서비스 보안설정, 리눅스/유닉스 로그·명령 |
| 2 | yes | 웹 취약점/시큐어코딩, DNS/SNMP/VLAN, 개인정보/ISMS-P/법규 |
| 3 | yes, focused | 악성코드/APT/포렌식, IPSec/VPN/암호통신, DB/데이터보호 |
| 4 | selective | 무선/모바일, 특수 표준·벤더 용어 항목 |

## Limits
- 빈도는 복원본 기준이며 공식 PDF 문구 대조가 아니다.
- 최근 23~30회는 reference confidence가 높지만, 4개 medium 항목은 전략 문서에서 과도한 확신도로 다루지 않는다.
