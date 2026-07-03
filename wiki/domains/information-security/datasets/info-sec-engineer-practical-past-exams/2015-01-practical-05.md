---
title: "정보보안기사 실기 5회 2015년 1회 실기 복원"
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
  - "https://information-security.tistory.com/289"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 5회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 5회 2015년 1회 실기 복원

## Scope
- Exam mapping: 2015년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 리눅스 파일 시스템에서 ext3부터 지원하며, 명령 수행 로그를 남겨 갑작스러운 종료 등으로 파일 시스템이 손상될 때 기존 로그로 복구하는 기능의 명칭을 쓰시오. | 저널링(Journaling) | source-derived from Information Security Tistory; answer block present |
| 2 | short | 여러 기관이 보안 취약점을 일관성 없이 표현하던 문제를 줄이기 위해, 특정 취약점을 공통으로 지칭하고 공유하도록 만든 표준화된 취약점 코드 체계의 명칭을 쓰시오. | CVE(Common Vulnerabilities and Exposures) | source-derived from Information Security Tistory; answer block present |
| 3 | short | FTP 서비스를 운영하는 서버에서 다음과 같은 현상이 확인되었다. 어떤 유형의 공격인지 쓰시오. | TCP SYN Flooding 공격 | source-derived from Information Security Tistory; answer block present |
| 4 | short | 다음 웹 서버 로그에서 확인되는 공격의 명칭을 쓰시오. | SQL Injection 공격 (URL 디코딩: id='user' and pw='1' or 1=1 형태의 SQL 조건 삽입) | source-derived from Information Security Tistory; answer block present |
| 5 | short | 개인정보의 기술적·관리적 보호조치 기준에서 권한 부여·변경·말소 이력 보관 기간, 개인정보취급자 접속기록 정기 확인 주기, 시스템 이상 확인 등을 위한 접속기록 보존 기간의 빈칸 (A), (B), (C)를 채우시오. | A : 5년 B : 월 1회 C : 6개월 | source-derived from Information Security Tistory; answer block present |
| 6 | short | 실행 가능한 스크립트 파일을 서버에 업로드해 원격 제어하는 공격과, 입력 인자에 질의문을 삽입해 데이터베이스 질의문을 조작하는 공격의 명칭을 각각 쓰시오. | A : 파일 업로드 공격(웹쉘 업로드) B : SQL Injection 공격 | source-derived from Information Security Tistory; answer block present |
| 7 | short | 원격 파일 인클루드(Remote File Include) 취약점에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : include/require B : php.ini C : off | source-derived from Information Security Tistory; answer block present |
| 8 | short | 위험 평가와 관련된 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 취약점(Vulnerability) B : 위협(Threat) C : 목표 위험 수준 | source-derived from Information Security Tistory; answer block present |
| 9 | short | 위험 관리 기법 중 위험을 인지하였으나 별도의 통제를 수행하지 않고 그대로 받아들이며 진행하는 방식의 명칭을 쓰시오. | 위험 수용(Risk Acceptance) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 정보보안의 세 가지 목적 중 기밀성 외의 두 요소와, 위험관리계획 수립 시 업무 우선순위 선정 및 보호대책 수준 도출에 사용하는 분석의 빈칸 (A), (B), (C)를 채우시오. | A : 무결성(Integrity) B : 가용성(Availability) C : 업무영향분석(BIA, Business Impact Analysis) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 다음은 드라이브 바이 다운로드(Drive By Download) 공격의 단계이다. 물음에 답하시오. | (1) Drive By Download(드라이브 바이 다운로드) (2) 악성코드 유포 사이트(최종 유포지) (3) 정적 분석 : 룰 엔진 기반의 악성코드 패턴 비교, 악성코드 유포 사이트 페이지의 DOM 구조 검증 동적 분석 : 샌드박스(SandBox) 환경에서 동작 분석, 특정 포트 백도어 생성 여부 모니터링 | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 정보통신기반보호법 제16조에 따라 정보공유·분석센터(ISAC)가 수행하는 역할 2가지를 서술하시오. | (1) 취약점 및 침해 요인과 그 대응 방안에 관한 정보 제공 (2) 침해사고 발생 시 실시간 경보·분석 체계 운영 | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 특정 웹 페이지에 실행 가능한 스크립트를 삽입하여 페이지 방문자의 개인정보나 쿠키 정보를 탈취하는 공격의 명칭과 대응 방안을 서술하시오. | 공격 명칭 : XSS(Cross Site Script) 대응 방안 : 사용자 입력값에 대해 HTML 특수문자(<, >, ", ', & 등)를 엔티티 코드로 인코딩하여 스크립트 실행을 차단한다. 쿠키에 HttpOnly 속성을 적용하여 자바스크립트를 통한 쿠키 접근을 차단한다. 웹 방화벽(WAF)을 적용하여 악성 스크립트 패턴을 탐지·차단한다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 악성코드 동작 분석 결과 다음과 같은 시스템 변경 사항이 발견되었다. 이 악성코드의 동작 6가지를 서술하시오. | (1) a.bat, msnsrv.exe, wassa.exe 파일을 생성한다. (2) 시스템 기동 시 자동 실행되도록 레지스트리에 값을 추가한다. (3) 탐색기에서 Hidden(숨김) 속성의 파일 보이기 설정을 해제한다. (4) 커맨드 쉘 cmd.exe를 레지스트리에서 삭제한다. (5) 커맨드 쉘 실행 시 msnsrv.exe가 실행되도록 레지스트리에 추가한다. (6) Windows 방화벽에서 TCP 9070번 포트를 허용하도록 설정한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음 공격 결과에 관한 물음에 답하시오. | (1) 디렉토리 리스팅(Directory Listing) 취약점 공격 (2) 웹 서버(192.168.0.10) (3) 공격 성공으로 판단된다. HTTP 200 OK 응답 코드는 요청이 정상적으로 처리되었음을 의미하므로, 디렉토리 내 파일 목록이 브라우저에 정상적으로 출력된 것으로 판단할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음은 DNS 서버로 Zone Transfer를 시도한 결과이다. 물음에 답하시오. | (1) 1차 네임서버(NS1)는 Zone Transfer 요청에 응답하지 않아 도메인 정보 탈취에 실패하였다. Zone Transfer가 적절히 차단되어 있는 안전한 상태이다. (2) 공격자가 간단한 명령으로 내부 시스템·네트워크 구조(호스트 목록, IP 대역, 보안 장비 IP 등)를 쉽게 파악할 수 있다. 사내 IP 대역이나 보안 장비 IP가 외부에 노출될 수 있다. Zone Transfer 시도 시 Zone 파일 크기에 따라 과도한 트래픽이 유발되어 서비스 거부(DoS) 공격으로 악용될 수 있다. (3) Zone Transfer가 필요하지 않은 경우 비활성화하고, 필요한 경우 신뢰할 수 있는 Slave DNS 서버 IP에 대해서만 Zone Transfer를 허용하도록 설정한다. | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
