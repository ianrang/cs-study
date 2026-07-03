---
title: "정보보안기사 실기 18회 2021년 2회 실기 복원"
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
  - "https://blog.naver.com/stereok2/222587717690"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 18회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 18회 2021년 2회 실기 복원

## Scope
- Exam mapping: 2021년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 무선랜 보안 표준 | WPA2 | Naver answer cross-check; exact official wording unverified |
| 2 | short | 악성 파일 분류 툴 | YARA | Naver answer cross-check; exact official wording unverified |
| 3 | short | SW 보안 취약점 | SQL Injection, XSS, OS Command Injection | Naver answer cross-check; exact official wording unverified |
| 4 | short | MS 오피스 프로토콜 | DDE(Dynamic Data Exchange) | Naver answer cross-check; exact official wording unverified |
| 5 | short | 위험관리 3요소 | 자산, 위협, 취약점 | Naver answer cross-check; exact official wording unverified |
| 6 | short | 정보보안 거버넌스 | 조직의 정보보호 목표·전략·책임·통제를 경영 관점에서 수립·관리하는 체계 | Naver answer cross-check; exact official wording unverified |
| 7 | short | 도메인 임시 생성 기법 | DGA(Domain Generation Algorithm) | Naver answer cross-check; exact official wording unverified |
| 8 | short | 위험분석 절차 | 자산식별, 자산 가치 및 의존도 평가 | Naver answer cross-check; exact official wording unverified |
| 9 | short | Slow HTTP Header DoS | Slowloris | Naver answer cross-check; exact official wording unverified |
| 10 | short | 모바일 딥링크 | 앱의 특정 화면·기능으로 직접 이동하게 하는 URI/URL 기반 연결 방식 | Naver answer cross-check; exact official wording unverified |
| 11 | essay | Prepared Statement와 SQL Injection 방어 | SQL과 파라미터를 분리해 미리 컴파일하고 값을 바인딩하므로 입력값이 SQL 구문으로 해석되지 않아 SQL Injection을 방어한다 | Naver answer cross-check; exact official wording unverified |
| 12 | essay | DRDoS 공격원리와 Unicast RPF | 공격자가 피해자 IP로 출발지를 위조해 반사 서버에 요청을 보내고 응답이 피해자에게 집중된다. Unicast RPF는 역방향 경로 검증으로 출발지 위조 패킷을 차단한다 | Naver answer cross-check; exact official wording unverified |
| 13 | essay | 패킷 필터링 방화벽과 Tiny Fragment 공격 | Ingress filtering으로 외부에서 내부 출발지 IP를 가진 패킷을 차단하고, tiny fragment는 TCP 헤더 일부를 뒤쪽 조각으로 밀어 필터 우회를 노린다. 조각 재조립 검사와 stateful inspection으로 대응한다 | Naver answer cross-check; exact official wording unverified |
| 14 | essay | 이메일 보안과 스팸메일 대응 | SPF는 발신 IP를 DNS 정책으로 검증하고 DKIM은 RSA 기반 서명으로 메일 무결성을 확인하며, DMARC는 SPF/DKIM 결과 기반 정책을 적용한다 | Naver answer cross-check; exact official wording unverified |
| 15 | essay | 리눅스 계정 잠금, iptables, /etc/shadow, LimitRequestBody | PAM 설정에서 deny로 잠금 임계값을 설정하고, iptables DROP으로 차단하며, /etc/shadow는 root 소유와 400 권한으로 보호한다. LimitRequestBody는 요청 본문 크기를 제한한다 | Naver answer cross-check; exact official wording unverified |
| 16 | essay | DNS 기반 증폭 공격 | DNS Amplification 기반 DRDoS로 판단한다. 출발지 IP를 피해자로 위조해 공개 DNS 서버에 질의하고, 큰 DNS 응답이 피해자에게 집중되어 트래픽이 증폭된다 | Naver answer cross-check; exact official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and must be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
