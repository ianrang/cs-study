---
title: 정보보안기사 실기 5회 2015년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/ac3e046dc97ab6c77a06ca1d4787f4cb524efb02a1e87ab955e6974a7ba7a4f5/28b9b40ff0fa19bae22af74668ca6b35c4283043a967f88dbf72399838d3ccd2/manifest.json
summary: 정보보안기사 실기 5회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 5회 2015년 1회 실기 복원

### Scope
- Exam mapping: 2015년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 리눅스 파일 시스템에서 ext3부터 지원하며, 파일 시스템의 메타데이터·변경 기록을 남겨 갑작스러운 종료 등으로 손상될 때 일관성 복구에 사용하는 기능의 명칭을 쓰시오. | 저널링(Journaling) | source-derived from Information Security Tistory; 2026-07-16 technical wording correction: journaling is not command-execution logging |
| 2 | short | 여러 기관이 보안 취약점을 일관성 없이 표현하던 문제를 줄이기 위해, 특정 취약점을 공통으로 지칭하고 공유하도록 만든 표준화된 취약점 코드 체계의 명칭을 쓰시오. | CVE(Common Vulnerabilities and Exposures) | source-derived from Information Security Tistory; answer block present |
| 3 | short | FTP 서버에서 TCP 연결 대기 큐(Backlog Queue)가 가득 차 있고 다수의 `SYN_RECEIVED` 상태 연결이 유지되며 정상 사용자의 FTP 접속이 불가능하다. 어떤 유형의 공격인지 쓰시오. | TCP SYN Flooding 공격 | source-derived from Information Security Tistory; prompt condition restored |
| 4 | short | 웹 서버 로그 `"GET /login.php?id%3D%27user%27%20and%20pw%3D%271%27%20or%201%3D1 HTTP/1.1" 200 3926`에서 확인되는 공격의 명칭을 쓰시오. | SQL Injection 공격 (URL 디코딩: `id='user' and pw='1' or 1=1` 형태의 SQL 조건 삽입) | [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) cross-check; source-derived log restored. |
| 5 | short | 개인정보의 기술적·관리적 보호조치 기준에서 권한 부여·변경·말소 이력 보관 기간, 개인정보취급자 접속기록 정기 확인 주기, 시스템 이상 확인 등을 위한 접속기록 보존 기간의 빈칸 (A), (B), (C)를 채우시오. | A : 3년 B : 월 1회 C : 1년 | source-derived from Information Security Tistory; PDF compilation cross-check corrected 2026-07-06 |
| 6 | short | 다음 공격의 명칭을 각각 쓰시오.<br>(A) 실행 가능한 스크립트 파일을 서버에 업로드하여 원격 제어에 악용하는 공격<br>(B) 입력 인자에 질의문을 삽입하여 데이터베이스 질의문을 조작하는 공격 | (A) 파일 업로드 공격(웹셸 업로드)<br>(B) SQL Injection 공격 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: two answer slots are explicitly mapped; exact official wording unavailable |
| 7 | short | 원격 파일 인클루드 취약점의 빈칸을 채우시오. `system()`, `exec()` 같은 운영체제 명령어 실행 함수가 포함된 외부 파일을 include하면 명령어 삽입 공격이 가능하다. 방지를 위해 (1) 코드에 (A) 문이 존재하는지 검증하고, (2) PHP의 경우 원격 URL을 `include`/`require`로 삽입하지 않도록 설정 파일 (B)의 `allow_url_include=(C)`로 변경한다. | A : include/require B : php.ini C : off | source-derived from Information Security Tistory; 2026-07-16 technical correction: allow_url_include directly controls remote include/require; allow_url_fopen=off is broader defense in depth |
| 8 | short | 위험 평가 설명의 빈칸을 채우시오. 정보자산에 대한 잠재적·알려진 (A)과 (B)으로 나타날 수 있는 조직 피해와 현재 통제의 실패 가능성 및 영향을 평가할 때 (C)을 포함해야 한다. | A : 취약점(Vulnerability) B : 위협(Threat) C : 목표 위험 수준 | source-derived from Information Security Tistory; prompt descriptions restored |
| 9 | short | 위험 관리 기법 중 위험을 인지하였으나 별도의 통제를 수행하지 않고 그대로 받아들이며 진행하는 방식의 명칭을 쓰시오. | 위험 수용(Risk Acceptance) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 정보보안의 세 가지 목적 중 기밀성 외의 두 요소와, 업무연속성계획(BCP) 수립 시 재해·장애로 업무가 중단될 경우의 영향을 분석하여 업무 중요도·복구 우선순위 및 RTO/RPO를 결정하는 절차의 빈칸 (A), (B), (C)를 채우시오. | A : 무결성(Integrity) B : 가용성(Availability) C : 업무영향분석(BIA, Business Impact Analysis) | source-derived from Information Security Tistory; 2026-07-18 prompt restoration: BCP, business-disruption impact, priority, and recovery-objective signals added so C uniquely identifies BIA rather than risk analysis; recurring BIA pattern cross-checked against R19-Q06 and NIST SP 800-34 Rev. 1; exact official wording unavailable |
| 11 | essay | 사용자가 변조된 웹 사이트에 접속하자, 삽입된 iframe·자바스크립트·리다이렉트 코드가 브라우저를 여러 경유지로 자동 이동시켰다. 최종 사이트는 사용자의 브라우저 또는 플러그인 취약점을 악용해 악성코드를 내려받아 실행시켰다. (1) 이 공격 기법의 명칭을 쓰시오. (2) 사용자의 PC에서 실제 악성코드 실행·감염이 일어나는 단계와 위치를 쓰시오. (3) 이 사건을 분석하기 위한 정적 분석 방법과 동적 분석 방법을 각각 한 가지씩 서술하시오. | (1) Drive-by Download(드라이브 바이 다운로드) 공격 (2) 4단계의 최종 유포 사이트에서 브라우저·플러그인 취약점이 악용되어 악성코드가 실행·감염된다. (3) 정적 분석: 악성 파일·스크립트를 실행하지 않고 iframe·자바스크립트·리다이렉트 코드, DOM 구조, 문자열·URL 등을 분석한다. 동적 분석: 격리된 샌드박스에서 실행하여 프로세스·파일·레지스트리 변경 및 네트워크 연결·백도어 행위를 관찰한다. | source-derived from Information Security Tistory; 2026-07-18 prompt restoration: answer-leaking attack title removed and three answer parts made explicit; staged browser-exploit behavior cross-checked against MITRE ATT&CK T1189; exact official wording unavailable |
| 12 | essay | 정보통신기반보호법 제16조에 따라 정보공유·분석센터(ISAC)가 수행하는 역할을 각각 서술하시오.<br>(1) 취약점·침해 요인과 대응 방안 정보 제공<br>(2) 침해사고 실시간 경보·분석 체계 운영 | (1) 취약점 및 침해 요인과 그 대응 방안에 관한 정보 제공<br>(2) 침해사고 발생 시 실시간 경보·분석 체계 운영 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: two requested answer slots are explicit; statutory answer remains source-derived |
| 13 | essay | 특정 웹 페이지에 실행 가능한 스크립트를 삽입하여 페이지 방문자의 개인정보나 쿠키 정보를 탈취하는 공격에 답하시오.<br>(1) 공격 명칭<br>(2) 핵심 대응 방안 | (1) XSS(Cross Site Scripting)<br>(2) 신뢰하지 않는 데이터를 출력 위치(HTML, 속성, JavaScript, URL)에 맞게 컨텍스트별 인코딩한다. 프레임워크의 기본 출력 인코딩을 우선 사용하고, 입력 검증·CSP·HttpOnly·WAF는 보조 통제로 적용한다. | source-derived from Information Security Tistory; 2026-07-16 technical correction: input filtering or HttpOnly alone does not prevent XSS |
| 14 | essay | 악성코드 분석 결과에서 확인된 행위를 각각 서술하시오.<br>(1) `a.bat`, `msnsrv.exe`, `wassa.exe` 생성<br>(2) 시스템 기동 시 자동 실행 레지스트리 추가<br>(3) Hidden 파일 보이기 설정 해제<br>(4) `cmd.exe` 관련 레지스트리 삭제<br>(5) 커맨드 쉘 실행 시 `msnsrv.exe` 실행 레지스트리 추가<br>(6) Windows 방화벽 TCP 9070 허용 | (1) a.bat, msnsrv.exe, wassa.exe 파일을 생성한다.<br>(2) 시스템 기동 시 자동 실행되도록 레지스트리에 값을 추가한다.<br>(3) 탐색기에서 Hidden(숨김) 속성의 파일 보이기 설정을 해제한다.<br>(4) 커맨드 쉘 cmd.exe를 레지스트리에서 삭제한다.<br>(5) 커맨드 쉘 실행 시 msnsrv.exe가 실행되도록 레지스트리에 추가한다.<br>(6) Windows 방화벽에서 TCP 9070번 포트를 허용하도록 설정한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: six analysis artifacts and answer slots are explicitly mapped; source provides summarized behavior evidence rather than original raw artifacts; exact official wording unavailable |
| 15 | essay | Apache 웹 서버 `192.168.0.10`의 `/backup/`에 접근했더니 `HTTP/1.1 200 OK`와 함께 `Index of /backup/`, `db-backup.sql`, `config.php` 등 디렉터리 내 파일 목록이 표시되었다. (1) 취약점 유형, (2) 취약한 대상, (3) 정보 노출 여부와 판단 근거, (4) Apache 주 설정 파일의 해당 `<Directory>` 구간에 적용할 대응 설정을 각각 서술하시오. | (1) 디렉터리 리스팅(Directory Listing, AutoIndex) 설정 취약점 (2) Apache 웹 서버 `192.168.0.10`의 `/backup/` 디렉터리 설정 (3) 파일명·경로 등 정보가 노출되었다. HTTP 200 OK만으로는 목록 노출을 단정할 수 없지만, `Index of /backup/`와 실제 파일 목록이 함께 출력되었으므로 자동 디렉터리 목록이 제공된 것이다. (4) 해당 디렉터리에 적용되는 Apache 주 설정의 `<Directory>` 구간에서 `Options -Indexes`를 설정하고, 설정 검증 후 httpd를 재적용한다. | source-derived from Information Security Tistory; 2026-07-18 prompt restoration: observable directory-listing evidence and Apache-specific mitigation added; `Options -Indexes` cross-checked against Apache HTTP Server documentation; exact official wording unavailable |
| 16 | essay | 다음 AXFR 결과를 보고 답하시오.<br>`dig @NS1.abc.COM def.com axfr` → `Transfer failed`<br>`dig @NS2.abc.COM def.com axfr` → SOA, MX, A 레코드 등 존 정보 출력<br>(1) 1차 네임서버의 Zone Transfer 상태 해석<br>(2) 2차 네임서버에서 Zone Transfer 허용 시 보안 위협<br>(3) 대응책 | (1) NS1에 대한 해당 AXFR 요청은 실패했지만, 이 결과만으로 차단 설정 여부나 안전성을 단정할 수는 없다. 설정·로그로 허용 대상을 확인해야 한다.<br>(2) 비인가 Zone Transfer가 허용되면 호스트명·레코드·네트워크 구조가 노출되어 정찰에 악용될 수 있다.<br>(3) Zone Transfer가 필요하지 않은 경우 비활성화하고, 필요한 경우 신뢰할 수 있는 Secondary DNS 서버 IP에 대해서만 Zone Transfer를 허용하도록 설정한다. | source-derived from Information Security Tistory; 2026-07-16 technical correction: Transfer failed alone does not prove a secure configuration |

### Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.

## Schema / Composition

## Usage

## Limitations / Biases

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|


## Relations

| type | target | notes |
|---|---|---|


## Sources

- `raw/sources/clipping/ac3e046dc97ab6c77a06ca1d4787f4cb524efb02a1e87ab955e6974a7ba7a4f5/28b9b40ff0fa19bae22af74668ca6b35c4283043a967f88dbf72399838d3ccd2/manifest.json`
