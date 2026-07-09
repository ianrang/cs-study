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
date_updated: 2026-07-06
source_paths:
  - "https://blog.naver.com/stereok2/224308597646"
  - "https://jaesung.tistory.com/91"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 8
provenance: inferred
summary: "2025년 2회 정보보안기사 실기 29회 복원 문항을 동일 구조로 정리하고 공식 출제범위 및 기존 노트로 교차 검증한 문서. Naver category post was added as a cross-check source."
evergreen: false
---

# 정보보안기사 실기 29회 2025년 2회 복원

## Scope
- This is a paraphrased reconstruction of the explicit 29th practical restoration posts from Naver and Jaesung-derived sources.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Linux PAM 모듈 유형의 빈칸을 채우시오. (A): 사용자에게 비밀번호 등 인증 정보를 요청하고 입력값이 맞는지 검사하는 모듈 유형. (B): 명시된 계정이 현재 조건에서 유효한 인증 목표인지 검사하며 계정 접근 통제와 정책을 관리하는 모듈 유형. `password`: 사용자가 비밀번호를 변경할 수 있도록 비밀번호 갱신을 관장하는 모듈 유형. (C): 사용자가 인증을 받기 전·후에 수행해야 할 일을 정의하는 모듈 유형. | A : auth B : account C : session | Jaesung source text cross-check; source answer order restored |
| 2 | short | Windows에서 권한 설정, 보안 기능, 대용량 파일을 지원하는 대표 파일 시스템. | NTFS | Windows system security scope and common OS knowledge. |
| 3 | short | 중간 서버나 제3자가 통신 내용을 복호화하지 못하게 송신자-수신자 사이를 보호하는 방식. | 종단 간 암호화(E2EE) | Cryptographic communication concept; stable. |
| 4 | short | PC 에이전트와 네트워크 센서로 문서 유출을 탐지·차단하는 정보보호 솔루션. | DLP | round-1 security solutions notes classify DLP as information leakage prevention. |
| 5 | short | 고정 버퍼에 크기 검증 없이 복사할 때 발생하는 취약점과 위험 함수. | 버퍼 오버플로우, strcpy() | KCA criteria includes Buffer overflow; C unsafe copy function is standard. |
| 6 | short | Linux 계정 패스워드 해시를 일반 사용자가 직접 볼 수 없도록 저장하는 파일. | /etc/shadow | round-1 Linux notes distinguish passwd and shadow. |
| 7 | short | DNS의 전송계층 프로토콜, 반복 질의 부하 완화 저장 방식, 유지 기간. | UDP 또는 TCP, DNS 캐시(Cache), TTL | Naver answer cross-check; 일반 질의는 UDP가 기본이나 큰 응답·존 전송 등은 TCP를 사용한다. |
| 8 | short | 웹 서버에 업로드되어 원격 파일 조회·명령 실행에 악용되는 악성 스크립트. | 웹셸(Web Shell) | Web application/file upload attack scope. |
| 9 | short | 위험분석 접근법: 기준 수준 일괄 적용, 자산·위협·취약성 상세 분석, 고위험 영역 상세와 나머지 기준선 조합. | 기준선 접근법, 상세 위험분석, 복합 접근법 | round-1 risk assessment notes match baseline/detail/combined approaches. |
| 10 | short | 전기통신설비와 컴퓨터 기술로 정보를 수집·가공·저장·검색·송수신하는 체계. | 정보통신망 | Legal/management terminology in KCA criteria. |
| 11 | short | Apache Options 설정에서 디렉터리 리스팅 제거를 위해 삭제할 옵션. | Indexes | Web server hardening concept. |
| 12 | short | 사용자가 실행한 명령 이력을 시간순으로 확인하는 Linux accounting 명령. | lastcomm | round-1 Linux log command table maps process accounting pacct to lastcomm. |
| 13 | essay | 모바일 앱의 인증서 고정에 대해 답하시오. (A) 인증서 고정이 무엇이며 어떤 취약점을 막기 위한 기술인지 설명하시오. (B) 인증서 고정의 핵심 요소 3가지를 쓰시오. (C) 인증서 고정 우회 방법 2가지를 쓰시오. | 서버 인증서 또는 공개키를 앱에 저장하고 TLS 연결 시 서버 인증서와 비교해 MITM을 줄이는 기법이다. 핵심 요소는 인증서/공개키 저장, 인증서 검증, 인증서 교체·갱신 관리다. 우회는 런타임 후킹과 앱 변조·리패키징이 대표적이다 | Jaesung source text cross-check; Mobile/TLS security topic. |
| 14 | essay | 파일 업로드 취약점에 대해 답하시오. (A) 어떤 취약점이 존재하는가? (B) 업로드 로직 우회 기법을 쓰시오. (C) 해당 취약점을 이용한 공격이 성공하기 위한 조건을 쓰시오. | 실행 파일 업로드로 정보 탈취·명령 실행이 가능하다. 우회는 Content-Type 변조, 대소문자·이중 확장자, Null byte 삽입 등이 있다. 공격 성공 조건은 필터 우회, 업로드 제한 미적용, 업로드 파일의 URL 호출·서버 실행 가능 상태다 | Jaesung source text cross-check; KCA application vulnerability scope includes file upload and web shell. |
| 15 | essay | 네트워크 보안관제 구성요소 3가지와 각각의 역할을 설명하시오. 구성요소는 에이전트, 정보수집 서버, 통합관제용 시스템 관점에서 작성한다. | 에이전트는 로그 수집·전송, 정보수집 서버는 수집·저장·처리, 통합관제 시스템은 분석·이벤트 대응 지원. | Jaesung source text cross-check; round-1 monitoring/SIEM notes cover log collection and security monitoring components. |
| 16 | essay | ISMS-P에서 식별된 위험 처리 방법 4가지를 쓰고 각각의 의미를 설명하시오. | 위험 수용, 위험 감소, 위험 전가, 위험 회피. | Jaesung source text cross-check; KCA criteria and round-1 risk notes match the four risk treatment strategies. |
| 17 | practical | Windows 이벤트 로그 최대 크기 설정에 대해 답하시오. 단일 이벤트 최대 크기 500바이트, 하루 이벤트 발생량 1,000개, 보관 기간 30일일 때 (가) 최대 이벤트 로그 크기 계산식, (나) 계산값, (다) 최대 이벤트 로그 크기 설정 경로를 쓰시오. | 500바이트 × 1,000건/일 × 30일 = 15,000,000바이트. 이벤트 뷰어에서 해당 로그 속성의 최대 로그 크기를 설정한다. | Jaesung source text cross-check; Windows event log management appears in practical criteria. |
| 18 | practical | CCTV 설치 시 개인정보처리자가 해야 할 조치를 회사 사옥 외부 공개 장소와 사내 출입통제구역 내부 관점으로 구분해 쓰시오. | 공개 장소 고정형 영상정보처리기기는 법정 사유가 있을 때 설치하고 안내판에 설치 목적·장소, 촬영 범위·시간, 관리책임자 연락처, 위탁 시 수탁자 정보를 기재한다. 녹음과 목적 외 임의 조작을 금지하고 운영·관리 방침과 안전성 확보조치를 마련한다. 비공개 장소는 법 제15조 기반 개인정보 수집으로 보아 정보주체 동의 등 적법 근거를 확보하고 공개 장소 보호조치를 준용한다 | Jaesung source text cross-check; legal wording needs current-law check before operational use. |

## Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for technical items; medium for legal CCTV details because statutory wording must be rechecked against the current law at use time.
- Known normalization: item 12 is treated as process accounting history, not shell history; this matches `lastcomm` but requires accounting to be enabled. Item 7 preserves Naver's `UDP 또는 TCP` answer with the usual DNS-use nuance.
