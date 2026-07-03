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
  - "https://blog.naver.com/stereok2/224130288134"
  - "https://jaesung.tistory.com/90"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 8
provenance: inferred
summary: "2025년 1회 정보보안기사 실기 28회 복원 문항을 단답형·서술형·실무형 동일 구조로 정리한 검증본. Naver category post was added as a cross-check source."
evergreen: false
---

# 정보보안기사 실기 28회 2025년 1회 복원

## Scope
- Source classification: Naver category post and Jaesung category pages contained explicit practical exam restoration posts for this round.
- This file is a paraphrased reconstruction, not a verbatim copy of the blog post.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 반사 서버를 경유해 대량의 ICMP echo reply를 피해자에게 보내는 공격과, 반사 서버 악용 방지를 위해 차단할 패킷. | Smurf, Directed Broadcast, ICMP echo request | Naver answer cross-check; KCA criteria includes DoS/DDoS attack types. |
| 2 | short | 서버가 사용자의 요청을 대신 처리하면서 내부망 자원에 접근하게 되는 웹 공격 유형. | SSRF | KCA application vulnerability scope includes server-side request forgery style web vulnerabilities. |
| 3 | short | 포트에 수동 할당하는 VLAN, MAC/인증 기반 자동 할당 VLAN, Cisco VLAN 확인 명령을 순서대로 묻는 문항. | 정적 VLAN, 동적 VLAN, show vlan | KCA network device/security operation scope covers network equipment configuration checks. |
| 4 | short | XSS 상황에서 JavaScript의 쿠키 접근을 막는 쿠키 보안 속성. | HttpOnly | Application security cookie/session control concept; answer is conceptually stable. |
| 5 | short | HTTP 헤더 인젝션에서 헤더 경계를 조작하는 개행 문자 두 종류. | CR, LF | HTTP header injection relies on CRLF sequence. |
| 6 | short | Lockheed Martin이 APT 공격 단계를 7단계로 모델링한 분석 체계. | 사이버 킬 체인 | APT response and incident-analysis topic within KCA practical criteria. |
| 7 | short | Linux에서 열린 파일과 파일을 사용하는 프로세스를 확인하는 명령. | lsof | round-1 Linux logging/operation notes and practical scope cover system status commands. |
| 8 | short | Linux 로그인 실패 기록 btmp를 확인하는 명령. | lastb | round-1 Linux log command table maps btmp to lastb. |
| 9 | short | 정보자산 중요도 기준의 CIA 중 빠진 요소와 이를 바탕으로 자산을 분류하는 행위. | 가용성, 그룹핑 | round-1 risk assessment notes cover asset classification by confidentiality, integrity, availability. |
| 10 | short | 위험분석의 방법·범위·예산·인력과 위험대응 활동을 정하는 계획 문서. | 위험관리계획 | KCA criteria includes risk-analysis planning and risk treatment planning. |
| 11 | short | ISMS-P 물리보안 관점의 보호대책 예시 세 가지. | 보호구역 지정, 출입통제, 정보시스템 보호, 보호설비 운영, 보호구역 내 작업 통제, 반출입 기기 통제, 업무환경 보안 중 3개 | Naver answer cross-check; KISA ISMS-P physical security controls align. |
| 12 | short | 모바일 앱의 특정 화면·기능으로 직접 이동시키는 링크 기술. | Deep link | Mobile/app security topic; source wording used DeepLink. |
| 13 | essay | Shell의 역할과 주요 기능 2가지를 설명하시오. | 운영체제와 사용자 사이의 명령 인터페이스이며, 명령 해석·커널 전달·환경 설정·스크립트 자동화 등을 수행한다. | OS basics in KCA practical criteria and round-1 Linux notes support the answer. |
| 14 | essay | Windows NetBIOS 바인딩 활성화 위험과 ncpa.cpl 기반 보안 설정 방법. | 인터넷 연결 Windows에서 NetBIOS over TCP/IP가 활성화되면 원격 공유자원 접근 위험이 있다. ncpa.cpl에서 네트워크 어댑터 속성 > TCP/IP 고급 > WINS 탭에서 NetBIOS over TCP/IP 사용 안 함을 선택한다 | Naver answer cross-check; Windows/server hardening scope covers service and share exposure. |
| 15 | essay | IPsec의 정의와 보안 모드 두 가지. | 네트워크/IP 계층에서 IP 패킷 단위 인증(AH), 암호화(ESP), 키관리(IKE)를 수행하는 프로토콜이다. 터널모드는 새 IP 헤더를 추가해 패킷 전체를 보호하고, 전송모드는 원 IP 헤더 외 데이터 부분을 보호한다 | Naver answer cross-check; KCA criteria explicitly mentions IPSec protocols. |
| 16 | essay | 정보자산 중요도 산정의 개념과 필수 기준 3가지. | 자산이 조직에 주는 가치와 손실 영향을 평가해 보호 우선순위를 정하는 절차다. 해당 자산의 기밀성, 무결성, 가용성 등급을 평가해 중요도를 산정한다 | Naver answer cross-check; round-1 risk assessment notes define asset value and CIA criteria. |
| 17 | practical | Oracle DB 감사 로그 설정 결과를 해석하고 감사 로그 저장 방식과 외부 저장 이유를 설명하는 문항. | audit_file_dest는 OS 감사 로그 저장 경로, audit_sys_operations=FALSE는 SYS 계정 감사 미수행, audit_syslog_level은 syslog 전송 등급, audit_trail=NONE은 감사 로그 미저장을 의미한다. SYS.AUD$에 저장하려면 audit_trail을 DB로 변경한다. 외부 저장은 DB 장악 시 로그 위변조를 줄이고 SIEM 연계와 신뢰 가능한 증거 확보에 유리하다 | Naver answer cross-check; DBMS audit configuration and log monitoring topic. |
| 18 | practical | Telnet 및 FTP 접속 배너와 root 로그인을 보고 취약점과 대응 방안을 설명하는 문항. | Telnet/FTP 평문 서비스, OS·커널·데몬 버전 배너 노출, root 직접 로그인 허용이 취약점이다. Telnet은 SSH로, FTP는 SFTP/FTPS로 대체하고 root 직접 로그인을 차단하며, issue.net·vsftpd 배너 설정 등으로 상세 버전 노출을 제거한다 | Naver answer cross-check; service-specific hardening guidance. |

## Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for item count and answer topics; medium for exact original wording because KCA does not publish official practical question text.
- Known normalization: item 11 was normalized to ISMS-P physical security control terminology. Items 14~16 follow the Naver post order: NetBIOS, IPsec, asset importance.
