---
title: "정보보안기사 실기 19회 2022년 1회 실기 복원"
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
  - "https://nhustler.tistory.com/40"
  - "https://nhustler.tistory.com/41"
  - "https://blog.naver.com/stereok2/222723288429"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 19회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 19회 2022년 1회 실기 복원

## Scope
- Exam mapping: 2022년 1회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 위험관리 3요소의 빈칸을 채우는 문제. | 자산, 위협, 취약점 | source-derived; Naver cross-checked; official wording unverified |
| 2 | short | 네트워크 진입 시 단말과 사용자를 인증하고 취약점 점검·통제를 수행하는 솔루션. | NAC(Network Access Control) | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | 공유자원 동시 접근 순서에 따른 비정상 결과를 악용하는 공격기법. | Race Condition 공격 | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | victim MAC 주소를 위조해 해당 IP로 가는 데이터를 중간에서 가로채는 공격. | ARP Spoofing | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | 패킷 기반 IDS와 서버 설치형 IDS 유형 구분. | 네트워크 기반 IDS, 호스트 기반 IDS | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | BCP 수립 시 업무 중요도, RTO, RPO를 결정하는 절차. | BIA(Business Impact Analysis, 업무영향도 분석) | source-derived; Naver cross-checked; official wording unverified |
| 7 | short | Apache 정상 접속 로그, 에러 로그, 로그 경로 설정 파일. | access log, error log, httpd.conf | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | 필 짐머만이 개발한 공개 이메일 보안 기술. | PGP(Pretty Good Privacy) | source-derived; Naver cross-checked; official wording unverified |
| 9 | short | 위험평가에서 CIA 관점으로 산정하는 자산 평가 값. | 자산 중요도 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | 이미 연결된 세션을 가로채는 공격 기법. | 세션 하이재킹 | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | setuid, setgid, sticky bit가 설정된 파일·디렉터리 권한 의미. | setuid는 소유자 권한 실행, setgid는 그룹 권한 실행, sticky bit는 공용 디렉터리에서 소유자/root 외 삭제 제한 | source-derived; Naver cross-checked; official wording unverified |
| 12 | essay | 공공기관 개인정보처리방침 포함 사항과 공개 방법. | 처리 목적·보유기간·제3자 제공·파기·위탁·정보주체 권리·책임자 연락처 등과 홈페이지/사업장 게시/관보·신문/간행물/계약서 고지 | source-derived; Naver cross-checked; legal wording needs current-law check |
| 13 | essay | promiscuous mode 의미, 가능한 공격, 대응 방법. | NIC가 목적지가 아닌 패킷도 수신하는 모드이며 스니핑이 가능하다. 암호화 통신, promisc 해제, 스위치 운용 등으로 대응 | source-derived; Naver cross-checked; official wording unverified |
| 14 | practical | 구성도와 자산목록을 보고 자산 식별 문제점과 보안 취약 문제점을 설명. | 개발 서버 누락 같은 자산 식별 누락과 중복 호스트명/노후 OS 등 보안 취약점을 지적 | source-derived; Naver cross-checked; exact asset list wording unverified |
| 15 | practical | 파일 업로드 취약점 대응을 위한 `.htaccess` 설정 의미 설명. | 실행 차단, 특정 확장자 제한, MIME/Handler 제거 등 업로드 파일 실행 방지 설정 | source-derived; Naver cross-checked; exact directive wording unverified |
| 16 | practical | 위험평가에서 자산 중요도 평가 목적, 우려사항, 가능성, 위험분석기법 적용. | CIA 기반 중요도 산정으로 통제 우선순위를 정하고 우려사항·발생가능성을 반영해 위험도와 대응 우선순위를 결정 | source-derived; Naver cross-checked; exact scenario wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
