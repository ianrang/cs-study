---
title: "정보보안기사 실기 29회 2025년 2회 복원"
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
  - "https://jaesung.tistory.com/91"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 7
provenance: inferred
summary: "2025년 2회 정보보안기사 실기 29회 복원 문항을 동일 구조로 정리하고 공식 출제범위 및 기존 노트로 교차 검증한 문서."
evergreen: false
---

# 정보보안기사 실기 29회 2025년 2회 복원

## Scope
- This is a paraphrased reconstruction of the explicit 29th practical restoration post.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | PAM module type 설명에서 인증, 계정 유효성, 세션 전후 처리에 해당하는 type을 묻는 문항. | auth, account, session | round-1 Linux PAM notes list auth/account/password/session. |
| 2 | short | Windows에서 권한 설정, 보안 기능, 대용량 파일을 지원하는 대표 파일 시스템. | NTFS | Windows system security scope and common OS knowledge. |
| 3 | short | 중간 서버나 제3자가 통신 내용을 복호화하지 못하게 송신자-수신자 사이를 보호하는 방식. | 종단 간 암호화(E2EE) | Cryptographic communication concept; stable. |
| 4 | short | PC 에이전트와 네트워크 센서로 문서 유출을 탐지·차단하는 정보보호 솔루션. | DLP | round-1 security solutions notes classify DLP as information leakage prevention. |
| 5 | short | 고정 버퍼에 크기 검증 없이 복사할 때 발생하는 취약점과 위험 함수. | 버퍼 오버플로우, strcpy() | KCA criteria includes Buffer overflow; C unsafe copy function is standard. |
| 6 | short | Linux 계정 패스워드 해시를 일반 사용자가 직접 볼 수 없도록 저장하는 파일. | /etc/shadow | round-1 Linux notes distinguish passwd and shadow. |
| 7 | short | DNS의 기본 전송계층 프로토콜, 반복 질의 부하 완화 저장 방식, 유지 기간. | UDP, DNS 캐싱, TTL | DNS operation and application security scope align. |
| 8 | short | 웹 서버에 업로드되어 원격 파일 조회·명령 실행에 악용되는 악성 스크립트. | 웹셸(Web Shell) | Web application/file upload attack scope. |
| 9 | short | 위험분석 접근법: 기준 수준 일괄 적용, 자산·위협·취약성 상세 분석, 고위험 영역 상세와 나머지 기준선 조합. | 기준선 접근법, 상세 위험분석, 복합 접근법 | round-1 risk assessment notes match baseline/detail/combined approaches. |
| 10 | short | 전기통신설비와 컴퓨터 기술로 정보를 수집·가공·저장·검색·송수신하는 체계. | 정보통신망 | Legal/management terminology in KCA criteria. |
| 11 | short | Apache Options 설정에서 디렉터리 리스팅 제거를 위해 삭제할 옵션. | Indexes | Web server hardening concept. |
| 12 | short | 사용자가 실행한 명령 이력을 시간순으로 확인하는 Linux accounting 명령. | lastcomm | round-1 Linux log command table maps process accounting pacct to lastcomm. |
| 13 | essay | 인증서 고정의 목적, 핵심 요소 3가지, 우회 방법 2가지를 설명하는 문항. | 특정 인증서/공개키를 앱에 고정해 MITM을 줄인다. 핵심은 고정값, 검증 로직, 실패 처리. 우회는 런타임 후킹, 리패키징/재서명 등이 있다. | Mobile/TLS security topic; answer matches common certificate pinning model. |
| 14 | essay | 파일 업로드 취약점에서 우회 기법과 공격 성공 조건을 설명하는 문항. | MIME/Content-Type만 검사하면 변조로 우회 가능. 업로드 경로에서 서버 스크립트가 실행되고 URL 호출이 가능해야 웹셸 공격이 성립한다. | KCA application vulnerability scope includes file upload and web shell. |
| 15 | essay | 네트워크 보안관제 구성요소 3가지와 역할을 설명하는 문항. | 에이전트는 로그 수집·전송, 정보수집 서버는 수집·저장·처리, 통합관제 시스템은 분석·이벤트 대응 지원. | round-1 monitoring/SIEM notes cover log collection and security monitoring components. |
| 16 | essay | ISMS-P 관점의 식별 위험 처리 방법 4가지를 쓰는 문항. | 위험 수용, 위험 감소, 위험 전가, 위험 회피. | KCA criteria and round-1 risk notes match the four risk treatment strategies. |
| 17 | practical | Windows 이벤트 로그 최대 크기 산정과 설정 경로를 계산·서술하는 문항. | 500바이트 × 1,000건/일 × 30일 = 15,000,000바이트. 이벤트 뷰어에서 해당 로그 속성의 최대 로그 크기를 설정한다. | Windows event log management appears in practical criteria. |
| 18 | practical | 회사 외부 공개 장소와 사내 출입통제구역 CCTV 설치 시 개인정보처리자 조치를 구분하는 문항. | 공개 장소는 설치 목적·장소·촬영 범위·시간·관리책임자 연락처 등을 안내해야 한다. 비공개 장소는 정보주체 동의 등 적법 근거와 보호조치를 확보한다. | Legal answer needs current law check before operational use; concept aligns with 개인정보보호법 CCTV regime. |

## Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for technical items; medium for legal CCTV details because statutory wording must be rechecked against the current law at use time.
- Known normalization: item 12 is treated as process accounting history, not shell history; this matches `lastcomm` but requires accounting to be enabled.
