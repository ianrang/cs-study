---
title: "정보보안기사 실기 2026년 2회 대비 3주 학습 전략"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, study-strategy]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "frequency-analysis.md"
  - "recurrence-analysis.md"
  - "pattern-analysis.md"
  - "significance-review.md"
  - "session-slot-pattern-analysis.md"
  - "item-reference-map.md"
source_count: 6
provenance: inferred
summary: "정보보안기사 실기 2026년 2회차를 약 3주 남긴 상황에서 60점 이상 합격을 목표로 한 압축 학습 로드맵과 답안 전략."
evergreen: false
---

# 정보보안기사 실기 2026년 2회 대비 3주 학습 전략

## Verdict
- 3주 남은 상태에서도 60점 이상 목표는 가능하다.
- 조건은 기출 원문 암기가 아니라 `문제 → 개념 → 답안 키워드 → 설정/명령/대응방안`으로 묶어 반복하는 것이다.
- 모든 범위를 균등하게 공부하면 위험하다. 반복 상위 개념과 최근 23~30회 강세 축에 집중해야 한다.
- 2026년 2회차는 2회 슬롯 경향상 시스템/관리/서비스 설정을 약간 더 높게 잡되, 슬롯 패턴은 보조 가중치로만 사용한다.

## Passing Strategy
| target | action |
|---|---|
| 안정권 60점 | 단답형 반복 개념을 빠르게 맞히고, 서술형/실무형은 키워드 부분점수를 확보한다. |
| 시간 배분 | 1주차 개념 압축, 2주차 기출 회전, 3주차 예상문제와 오답 고정. |
| 답안 원칙 | 정의만 쓰지 말고 `판단근거 + 핵심 키워드 + 대응/설정`을 붙인다. |
| 버릴 범위 | 저빈도 특수 표준·벤더 용어는 마지막에 본다. 단 medium 4개는 용어만 확인한다. |

## Three-Week Roadmap
| period | goal | daily output |
|---|---|---|
| D-21~D-15 | 반복 개념 1회독 | 상위 10개 concept group별 단답 카드와 서술 키워드 작성 |
| D-14~D-8 | 기출 23~30회 집중 회전 | 회차당 오답표, 명령/설정/법규 키워드 보강 |
| D-7~D-4 | 예상문제 실전 답안 | 예상문제 36개를 제한 시간 안에 작성하고 채점 키워드 누락 확인 |
| D-3~D-1 | 암기표 고정 | Linux/Windows/Apache/DNS/SNMP/IPSec/위험관리/개인정보 키워드만 반복 |
| 시험 당일 | 부분점수 확보 | 모르는 문제도 개념명, 위험, 대응, 설정값 중 아는 키워드를 쓴다. |

## Priority Topics
| priority | topic | must know |
|---:|---|---|
| 1 | 위험관리/위험평가 | 자산·위협·취약점, 위험수용/감소/전가/회피, 기준선/상세/복합, BIA, ALE/SLE/ARO |
| 2 | 접근통제/권한관리 | DAC/MAC/RBAC, PAM auth/account/session, 패스워드 정책, 최소권한, IAM/EAM |
| 3 | 서비스 보안설정 | Apache/IIS, DNS zone, SNMP community/v3, NTP monlist, SMTP relay, DB 권한·감사 |
| 4 | 리눅스/유닉스 | `/etc/passwd`, `/etc/shadow`, `/proc`, utmp/wtmp/btmp/lastlog, `lastb`, `lsof`, `lastcomm`, setuid/setgid/sticky, xinetd, iptables |
| 5 | 웹 취약점/시큐어코딩 | SQL Injection, XSS, SSRF, XXE, 파일 업로드, PreparedStatement, CRLF, request smuggling |
| 6 | 네트워크/프로토콜 | IPSec AH/ESP/IKE, ARP spoofing, VLAN, DNS, SNMP, TCP scan, DRDoS |
| 7 | 개인정보/ISMS-P/법규 | 안전성 확보조치, 접근권한 관리, 접속기록, 영상정보처리기기, 위탁 공개, CISO |
| 8 | 관제/탐지/포렌식 | IDS/IPS, HIDS/NIDS, Snort, 오탐/미탐, SIEM/SOAR, APT/Kill Chain, 포렌식 원칙 |
| 9 | 최근 확장 | DLP, MDM/BYOD, deep link, E2EE, credential stuffing, zero-day |

## Daily Routine
| block | time | work |
|---|---:|---|
| 암기 | 40m | 단답형 키워드 50개를 쓰면서 확인 |
| 이해 | 60m | concept group 1~2개를 정의·구성요소·대응방안으로 정리 |
| 기출 | 90m | 최근 회차 1개 또는 예상문제 6개 풀이 |
| 오답 | 40m | 틀린 문제를 `개념-답안키워드-실수원인`으로 재작성 |
| 회고 | 10m | 다음 날 암기표에 누락 키워드 추가 |

## Answer Templates
| type | template |
|---|---|
| 개념 설명 | `정의 → 목적/효과 → 대표 구성요소 또는 예시` |
| 공격 분석 | `공격명 → 판단근거 → 영향 → 대응방안 2~3개` |
| 설정/명령 | `파일/명령/지시자 → 의미 → 보안상 이유` |
| 법규/관리 | `적용 주체 → 요구사항 → 보관/점검/통제 기준` |
| 위험관리 | `자산/위협/취약점 → 위험 산정/평가 → 대응전략` |

## Minimum Passing Checklist
- 위험관리 4대 대응, 위험분석 방법, BIA/ALE/SLE/ARO를 설명할 수 있다.
- DAC/MAC/RBAC와 PAM 모듈을 구분할 수 있다.
- Linux 로그 파일과 계정 파일, 주요 명령을 쓸 수 있다.
- SQL Injection/XSS/SSRF/XXE/파일업로드 대응을 서술할 수 있다.
- IPSec AH/ESP/IKE와 전송/터널 모드를 구분할 수 있다.
- DNS/SNMP/VLAN/NTP/Apache 설정형 문제에 대응할 수 있다.
- 개인정보 안전성 확보조치의 접근권한·접속기록·암호화·접근통제 키워드를 쓸 수 있다.

## Risk Control
| risk | mitigation |
|---|---|
| 남은 시간이 짧음 | 저빈도 주제를 깊게 파지 말고 반복 상위 개념군에 집중한다. |
| 서술형 공백 | 완전한 문장보다 채점 키워드 3~5개를 먼저 쓴다. |
| 설정 명령 혼동 | 파일명·명령어·지시자를 따로 암기하지 말고 문제 상황과 같이 묶는다. |
| 법령 최신성 | 법령 세부 조문보다 안전성 확보조치·ISMS-P 통제 키워드 중심으로 정리한다. |
