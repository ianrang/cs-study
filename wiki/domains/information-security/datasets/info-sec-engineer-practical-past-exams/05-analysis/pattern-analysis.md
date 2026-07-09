---
title: "정보보안기사 실기 기출 패턴 분석"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-analysis, pattern]
status: active
date_created: 2026-07-03
date_updated: 2026-07-07
source_paths:
  - "frequency-analysis.md"
  - "recurrence-analysis.md"
  - "../03-classification/subject-type-classification-detail.md"
  - "../04-mapping/item-reference-map.md"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 1~31회 빈도와 반복 개념을 종합해 과목·유형·최근성 관점의 출제 패턴을 정리한 분석."
evergreen: false
---

# 정보보안기사 실기 기출 패턴 분석

## Verdict
- 전체 축은 `정보보안 관리 및 법규`와 `네트워크 보안`이 가장 크다.
- 최근 23~31회에서는 `시스템 보안`이 전체 평균보다 크고, 31회 XSS/CSRF/Fiddler 문항 반영으로 `어플리케이션 보안` 최근 비중도 올라갔다.
- 단답형은 62.0%지만, 고득점 분기점은 반복 개념을 설정·로그·코드·법적 적용 상황으로 서술하는 문항이다.
- 1~28회 thodi-lab/blog-source PDF 편집본은 대조했지만 KCA 공식 원문 문구는 미주장이므로, 분석은 문구 단위가 아니라 개념·유형 단위로 사용한다.

## Pattern Summary
| pattern | evidence | learning impact |
|---|---|---|
| 관리/법규와 네트워크가 전체 58.1% | 관리/법규 156건, 네트워크 142건 | 위험관리·접근통제·프로토콜/장비 보안은 우선 학습 축이다. |
| 최근 시스템 보안 상승 | 23~31회 시스템 보안 34건, 최근 비중 21.0% | Linux/Windows 파일·명령·권한·로그를 단답으로 빠르게 꺼내야 한다. |
| 최근 어플리케이션 보안 재상승 | 23~31회 어플리케이션 보안 33건, 최근 비중 20.4% | XSS, CSRF, 웹 서버 설정, 퍼징, 로그·프록시 도구 기반 문항을 함께 준비해야 한다. |
| 서비스 보안설정이 최근 최다 KCA 축 | 23~30회 `서비스 보안설정 점검과 보완` 28건 | 웹/DB/DNS/NTP/메일/Apache 설정과 취약점 대응을 실무형으로 준비해야 한다. |
| 위험관리 계열은 반복 고정축 | 1~30회 recurrence 기준 79건·30회차 모두 등장, 31회에도 위험관리 단계 문항 추가 | 위험분석 방법론, 위험대응, 자산 중요도, BIA/ALE/SLE는 필수 고정 암기 축이다. |
| 웹 취약점은 변형폭이 큼 | SQL Injection, XSS, SSRF, XXE, 파일 업로드, CRLF, request smuggling | 공격명뿐 아니라 판단근거·대응코드·설정까지 연결해야 한다. |
| 관제/탐지/로그는 단답과 실무형을 오감 | IDS/IPS/Snort/관제 52건, 로그·명령 계열 52건 | Snort 룰, 로그 필드, HIDS/NIDS, 오탐/미탐 구분을 함께 준비해야 한다. |

## Recent Exam Shape
| axis | recent signal, 23~31회 | interpretation |
|---|---:|---|
| 정보보안 관리 및 법규 | 44 | 위험관리, 법령 용어, CISO, 생체인식 보호 원칙이 반복된다. |
| 네트워크 보안 | 41 | IPSec, DNS, ARP, TCP/IP, 무선/모바일 통신과 방화벽 룰이 반복된다. |
| 시스템 보안 | 34 | OS 명령·로그·권한·파일시스템 단답이 반복된다. |
| 어플리케이션 보안 | 33 | XSS, CSRF, SQL Injection, 웹 서버 설정, 퍼징과 프록시 점검이 강화된다. |
| 정보보안 일반 | 10 | 암호·통제·재해복구 등 기본 개념은 낮은 빈도지만 꾸준히 출제된다. |

## Strategy Implications
| implication | basis |
|---|---|
| 1차 학습은 반복 개념군 중심이어야 한다. | 위험관리, 접근통제, 웹/HTTP, 로그/명령, 네트워크 장비가 반복 상위다. |
| 2차 학습은 변형 대응이어야 한다. | 같은 개념이 빈칸, 명령, 로그 해석, 대응방안으로 변형된다. |
| 최근 대비는 시스템 보안, 어플리케이션 보안, 서비스 설정을 같이 올려야 한다. | 최근 23~31회에서 시스템 보안은 여전히 높고, 31회 반영 후 어플리케이션 보안 비중이 상승했다. |
| 예상문제는 단순 정의형보다 "증거 기반 답안"을 포함해야 한다. | 로그·코드·설정·법규 적용 문항이 반복된다. |

## Next Use
- `study-strategy-2026-02.md`에서는 본 문서의 pattern을 학습 순서로 변환한다.
- `predicted-practical-questions-2026-02.md`에서는 반복 개념군별로 단답형/서술형/실무형 예상문제를 분리한다.
