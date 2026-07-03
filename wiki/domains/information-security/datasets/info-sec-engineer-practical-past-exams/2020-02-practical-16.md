---
title: "정보보안기사 실기 16회 2020년 2회 실기 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "https://blog.naver.com/stereok2/222191200052"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 16회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 16회 2020년 2회 실기 복원

## Scope
- Exam mapping: 2020년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | /etc/shadow 파일 해시 알고리즘 식별자 | 1=MD5, 5=SHA-256, 6=SHA-512 | Naver answer cross-check; exact official wording unverified |
| 2 | short | 정보보호최고책임자 | CISO | Naver answer cross-check; exact official wording unverified |
| 3 | short | 정보보호정책 | Policy, 정보보호정책 | Naver answer cross-check; exact official wording unverified |
| 4 | short | 무선랜 보안 표준별 암호 기술 | WEP=RC4, WPA=TKIP, WPA2=AES/CCMP | Naver answer cross-check; exact official wording unverified |
| 5 | short | 엔드포인트 위협 대응 솔루션 | EDR(Endpoint Detection and Response) | Naver answer cross-check; exact official wording unverified |
| 6 | short | TLS 1.3 암호화 기능 | 1-RTT와 0-RTT 지원 | Naver answer cross-check; exact official wording unverified |
| 7 | short | 시스템콜 확인 명령 | strace | Naver answer cross-check; exact official wording unverified |
| 8 | short | 위협정보 수집·분석·대응 시스템 | TMS(Threat Management System) | Naver answer cross-check; exact official wording unverified |
| 9 | short | 위험관리 구성요소 | 위협, 자산, 감소 | Naver answer cross-check; exact official wording unverified |
| 10 | short | UDP 기반 보안 프로토콜 | DTLS | Naver answer cross-check; exact official wording unverified |
| 11 | essay | 쿠키 보안 속성 | Secure는 TLS 연결에서만 쿠키를 전송해 스니핑을 줄이고, HttpOnly는 JavaScript 접근을 막아 XSS 기반 쿠키 탈취를 줄인다 | Naver answer cross-check; exact official wording unverified |
| 12 | essay | 디지털 포렌식 원칙 | 정당성, 재현성, 신속성, 연계보관성, 무결성 중 요구 개수 기술 | Naver answer cross-check; exact official wording unverified |
| 13 | essay | 이메일 보안(SPF, DKIM, DMARC) | SPF는 발신 IP를 DNS TXT 정책으로 검증하고, DKIM은 개인키 서명과 DNS 공개키로 무결성을 확인하며, DMARC는 SPF/DKIM 결과 기반 처리 정책을 제공한다 | Naver answer cross-check; exact official wording unverified |
| 14 | essay | OWASP Top 10 XXE 공격원리와 실행 결과 | XXE는 XML 외부 엔터티를 악용해 파일 노출·SSRF 등을 유발하며, 반복 엔터티 확장으로 Billion Laughs DoS가 가능하다 | Naver answer cross-check; exact official wording unverified |
| 15 | essay | 정량적 위험 평가와 보호대책 선정 | A: SLE 20,000, ALE 10,000, 효과 13,000. B: SLE 80,000, ALE 20,000, 효과 16,000. 효과가 큰 B를 선정한다 | Naver answer cross-check; exact official wording unverified |
| 16 | essay | 개인정보흐름표 문제점 4가지 | 주민등록번호 수집 법령 근거 부재, 안전하지 않은 MD5 사용, 주민번호 평문 전송, 영구보관으로 파기주기 부재 | Naver answer cross-check; exact official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and must be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
