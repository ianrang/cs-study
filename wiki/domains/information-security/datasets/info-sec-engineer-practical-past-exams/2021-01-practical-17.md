---
title: "정보보안기사 실기 17회 2021년 1회 실기 복원"
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
  - "https://blog.naver.com/stereok2/222396448808"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 17회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 17회 2021년 1회 실기 복원

## Scope
- Exam mapping: 2021년 1회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 로그인 인증 우회 공격 기법 | Pass the Hash | Naver answer cross-check; exact official wording unverified |
| 2 | short | DNS 캐시 변조 공격 | DNS Cache Poisoning | Naver answer cross-check; exact official wording unverified |
| 3 | short | 사이버 킬 체인 프레임워크 | MITRE ATT&CK | Naver answer cross-check; exact official wording unverified |
| 4 | short | 로그인 자격증명 대입 공격 | Credential Stuffing | Naver answer cross-check; exact official wording unverified |
| 5 | short | 보안취약점 분석 기준 | CVSS | Naver answer cross-check; exact official wording unverified |
| 6 | short | 침해사고 대응 7단계 중 해당 단계 | 초기 대응 | Naver answer cross-check; exact official wording unverified |
| 7 | short | 정보보호 법규 용어 | 내부관리계획, 전자적 침해행위, 정보보호 사전점검 | Naver answer cross-check; exact official wording unverified |
| 8 | short | 주요정보통신기반시설 관련 법규 용어 | 정보통신망, 정보보호시스템, 정보통신기반시설 | Naver answer cross-check; exact official wording unverified |
| 9 | short | ISO 27005 위험관리 절차 | 위험식별, 위험분석, 위험수준평가 | Naver answer cross-check; exact official wording unverified |
| 10 | short | 개인정보 안전성 확보조치 기준 | 접속일시, 처리한 정보주체 정보, 내부관리계획 | Naver answer cross-check; exact official wording unverified |
| 11 | essay | 개인정보보호법상 가명정보와 익명정보 | 가명처리는 추가정보 없이는 특정 개인을 알아볼 수 없게 처리하는 것이며, 가명정보는 통계작성·과학적 연구·공익적 기록보존 등에 활용 가능하고 익명정보는 더 이상 개인을 식별할 수 없는 정보다 | Naver answer cross-check; exact official wording unverified |
| 12 | essay | NAC 물리적 구성방법 | Inline 방식과 Out-of-band 방식 | Naver answer cross-check; exact official wording unverified |
| 13 | essay | 정보보호최고책임자의 역할 및 책임 | 정보보호 정책·계획 수립, 위험관리, 보안조직 운영, 보안사고 대응, 교육·점검 등 CISO 책임 사항 기술 | Naver answer cross-check; exact official wording unverified |
| 14 | essay | 웹 원격명령실행 공격 성공 여부와 대응 | Unicode 취약점 기반 원격명령실행 시도이나 404 등으로 실패한 것으로 판단하며, 패치·입력 필터링·화이트리스트·웹/IIS 구성 분리·IPS 탐지로 대응한다 | Naver answer cross-check; exact official wording unverified |
| 15 | essay | Snort 룰 해석 | msg는 경고 메시지, content:"GET"은 HTTP GET 탐지, content:"USER"와 !content:"anonymous"는 익명 아닌 FTP USER 조건, \|00\| depth 1은 첫 바이트 NULL 조건을 의미한다 | Naver answer cross-check; exact official wording unverified |
| 16 | essay | Apache 설정 문제점과 대응방안 | Indexes로 디렉터리 인덱싱이 가능하고 FollowSymLinks로 심볼릭 링크 경유 접근이 가능하다. Indexes/FollowSymLinks 제거 또는 -Indexes/-FollowSymLinks, 필요 시 AllowOverride 설정으로 대응한다 | Naver answer cross-check; exact official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and must be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
