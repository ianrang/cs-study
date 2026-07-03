---
title: "정보보안기사 실기 28회 2025년 1회 복원"
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
  - "https://jaesung.tistory.com/90"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 7
provenance: inferred
summary: "2025년 1회 정보보안기사 실기 28회 복원 문항을 단답형·서술형·실무형 동일 구조로 정리한 검증본."
evergreen: false
---

# 정보보안기사 실기 28회 2025년 1회 복원

## Scope
- Source classification: Jaesung category pages 1-8 contained three explicit practical exam restoration posts: 28th, 29th, 30th.
- This file is a paraphrased reconstruction, not a verbatim copy of the blog post.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Smurf 공격에서 공격자가 브로드캐스트 주소로 보내는 패킷과 피해자에게 집중되는 응답 패킷 유형을 묻는 문항. | 브로드캐스트 패킷, ICMP 패킷 | KCA criteria includes DoS/DDoS attack types; round-1 network attack notes match Smurf reflection pattern. |
| 2 | short | 서버가 사용자의 요청을 대신 처리하면서 내부망 자원에 접근하게 되는 웹 공격 유형. | SSRF | KCA application vulnerability scope includes server-side request forgery style web vulnerabilities. |
| 3 | short | 포트에 수동 할당하는 VLAN, MAC/인증 기반 자동 할당 VLAN, Cisco VLAN 확인 명령을 순서대로 묻는 문항. | 정적 VLAN, 동적 VLAN, show vlan | KCA network device/security operation scope covers network equipment configuration checks. |
| 4 | short | XSS 상황에서 JavaScript의 쿠키 접근을 막는 쿠키 보안 속성. | HttpOnly | Application security cookie/session control concept; answer is conceptually stable. |
| 5 | short | HTTP 헤더 인젝션에서 헤더 경계를 조작하는 개행 문자 두 종류. | CR, LF | HTTP header injection relies on CRLF sequence. |
| 6 | short | Lockheed Martin이 APT 공격 단계를 7단계로 모델링한 분석 체계. | 사이버 킬 체인 | APT response and incident-analysis topic within KCA practical criteria. |
| 7 | short | Linux에서 열린 파일과 파일을 사용하는 프로세스를 확인하는 명령. | lsof | round-1 Linux logging/operation notes and practical scope cover system status commands. |
| 8 | short | Linux 로그인 실패 기록 btmp를 확인하는 명령. | lastb | round-1 Linux log command table maps btmp to lastb. |
| 9 | short | 정보자산 중요도 기준의 CIA 중 빠진 요소와 이를 바탕으로 자산을 분류하는 행위. | 가용성, 그룹핑 | round-1 risk assessment notes cover asset classification by confidentiality, integrity, availability. |
| 10 | short | 위험분석의 방법·범위·예산·인력과 위험대응 활동을 정하는 계획 문서. | 위험관리계획 | KCA criteria includes risk-analysis planning and risk treatment planning. |
| 11 | short | ISMS-P 물리보안 관점의 보호대책 예시 세 가지. | 보호구역/통제구역 지정, 출입권한 관리, 접근통제 | KISA ISMS-P physical security controls align; blog answer wording was normalized to control names. |
| 12 | short | 모바일 앱의 특정 화면·기능으로 직접 이동시키는 링크 기술. | Deep link | Mobile/app security topic; source wording used DeepLink. |
| 13 | essay | Shell의 역할과 주요 기능 2가지를 설명하는 문항. | 운영체제와 사용자 사이의 명령 인터페이스이며, 명령 해석·커널 전달·환경 설정·스크립트 자동화 등을 수행한다. | OS basics in KCA practical criteria and round-1 Linux notes support the answer. |
| 14 | essay | IPsec의 개념, 동작 모드, 제공 방식 두 가지를 설명하는 문항. | IP 계층 보안 프로토콜. 모드는 전송/터널, 방식은 AH/ESP. | KCA criteria explicitly mentions TCP, UDP, SSL/TLS, IPSec protocols. |
| 15 | essay | 정보자산 중요도 산정의 의미와 기준 세 가지를 설명하는 문항. | 자산 가치를 평가해 관리 우선순위를 정하는 것. 기준은 기밀성·무결성·가용성. | round-1 risk assessment notes define asset value and CIA criteria. |
| 16 | essay | Windows NetBIOS 바인딩 활성화 위험과 보호대책을 쓰는 문항. | 공유자원 노출·비인가 접근 위험. 불필요한 NetBIOS over TCP/IP 비활성화와 인터페이스 고급 설정 점검. | Windows/server hardening scope in KCA practical criteria covers service and share exposure. |
| 17 | practical | Oracle DB 접근 권한과 감사 설정이 미흡할 때의 문제와 대응을 쓰는 문항. | 과도한 권한은 유출·무단 변경을 유발한다. 최소권한 역할 부여, 객체별 감사, 중요정보 암호화/TDE 적용. | KCA practical criteria includes DB security, DB object access control, encryption, and log monitoring. |
| 18 | practical | Telnet 및 FTP 서비스 운영 배너를 보고 취약점과 전환 방안을 쓰는 문항. | Telnet/FTP는 평문 전송으로 인증정보 노출 위험. SSH, SFTP 또는 FTPS로 대체하고 불필요 서비스 중지. | KCA criteria includes service-specific logs and server/network security; answer is standard hardening guidance. |

## Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for item count and answer topics; medium for exact original wording because KCA does not publish official practical question text.
- Known normalization: item 11 was normalized from broad wording to ISMS-P physical security control terminology.
