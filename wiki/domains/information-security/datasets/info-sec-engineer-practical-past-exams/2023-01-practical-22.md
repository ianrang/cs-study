---
title: "정보보안기사 실기 22회 2023년 1회 실기 복원"
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
  - "https://nhustler.tistory.com/34"
  - "https://nhustler.tistory.com/35"
  - "https://blog.naver.com/stereok2/223148136930"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 22회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 22회 2023년 1회 실기 복원

## Scope
- Exam mapping: 2023년 1회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 거리 벡터, 링크 상태, Cisco 하이브리드 라우팅 프로토콜. | RIP, OSPF, EIGRP | source-derived; Naver cross-checked; official wording unverified |
| 2 | short | Unix 로그 파일명. | lastlog, sulog, acct 등 문항 조건에 맞는 로그 파일 | source-derived; Naver cross-checked; exact blank wording unverified |
| 3 | short | `/etc/passwd` 계정 속성 필드. | 계정명, 패스워드 자리, UID, GID, 설명, 홈 디렉터리, 로그인 셸 | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | HTTP 응답 분할에 쓰이는 개행문자. | CRLF 또는 `%0d%0a` | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | PHP 파일 삽입 취약점 관련 `php.ini` 설정. | `allow_url_fopen`, `allow_url_include` 등 원격 파일 포함 관련 설정 | source-derived; Naver cross-checked; exact blank wording unverified |
| 6 | short | Snort threshold type. | limit, threshold, both 중 조건에 맞는 threshold type | source-derived; Naver cross-checked; exact rule wording unverified |
| 7 | short | ARP request 주소 관련 문제. | ARP request는 브로드캐스트 MAC을 사용해 대상 IP의 MAC 주소를 질의 | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | DNS 프로토콜 기본 특성. | 주로 UDP/53을 사용하고 zone transfer 등은 TCP/53을 사용 | source-derived; Naver cross-checked; exact prompt wording unverified |
| 9 | short | SW 개발보안 점검 방법. | 블랙박스 테스트, 화이트박스 테스트 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | DBMS 조회 질의문 보안약점 대응. | PreparedStatement 또는 매개변수화 질의 사용 | source-derived; Naver cross-checked; official wording unverified |
| 11 | short | 개인정보 안전성 확보조치 기준상 접속기록 보관. | 개인정보처리시스템 접속기록 보관·점검, 위변조 방지, 보관기간 준수 | source-derived; Naver cross-checked; current-law wording needs check |
| 12 | short | 위험 관리에서 보호대책 후 남는 위험. | 잔여위험 | source-derived; Naver cross-checked; official wording unverified |
| 13 | essay | 모바일 기기 보안 기술 설명. | MDM은 단말 정책·앱·분실통제를 관리하고, 컨테이너화는 업무/개인 영역을 분리하며, 모바일 가상화는 격리된 실행환경을 제공 | source-derived; Naver cross-checked; official wording unverified |
| 14 | essay | 기준선 접근법과 상세 위험분석의 정의·장단점. | 기준선은 빠르고 표준화되나 과소/과대보호 위험이 있고, 상세 위험분석은 정확하지만 비용과 시간이 크다 | source-derived; Naver cross-checked; official wording unverified |
| 15 | essay | Cookie 보안 설정 값 의미. | Secure는 HTTPS 전송 제한, HttpOnly는 스크립트 접근 제한, Expires는 만료시각 지정 | source-derived; Naver cross-checked; official wording unverified |
| 16 | essay | DNS 증폭공격에 쓰이는 IP 공격기법과 이유. | 출발지 IP spoofing을 이용해 피해자 IP로 대량 응답이 향하게 하며, 작은 질의 대비 큰 응답으로 증폭 효과를 얻음 | source-derived; Naver cross-checked; official wording unverified |
| 17 | practical | SQL Injection 취약점명, 판단 사유, 조치 방안. | SQL Injection. 입력값이 쿼리 구조를 바꿀 수 있으면 취약하며 입력검증, PreparedStatement, 최소권한, 오류노출 제한으로 조치 | source-derived; Naver cross-checked; official wording unverified |
| 18 | practical | 개인정보의 기술적·관리적 보호조치. | 내부관리계획, 접근권한 관리, 접근통제, 암호화, 접속기록 보관·점검, 악성프로그램 방지, 물리적 안전조치 등 | source-derived; Naver cross-checked; current-law wording needs check |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
