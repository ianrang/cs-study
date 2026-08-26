---
title: 정보보안기사 실기 복원 1~100번 기술 정확성 교차검증
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
- verification
date_created: '2026-07-16'
date_updated: '2026-07-16'
source_paths:
- raw/sources/clipping/7a3822b1f191e2ec3be5f8754373ee7e4c492d4ac6ffb5973e823d4594ad1159/0a799ff8f1da6ce002869d29bf9f431d858b4db1b6e5b18e6b146f06007387fb/manifest.json
summary: 기출 복원 1~100번을 문항별로 검토해 확인된 기술 오류를 정정하고, 원문 복원 한계와 현행성 한계를 분리한 감사 기록.
---

## Overview











# 정보보안기사 실기 복원 1~100번 기술 정확성 교차검증

### Scope
- 대상은 1~100번(R01 전항, R02 전항, R03 전항, R04 전항, R05 전항, R06 전항, R07 1~5번)이다.
- 회차 MD는 비공식 기출 복원 SoT이며, 이 문서는 KCA 공식 원문을 대체하거나 공식 문구 일치를 주장하지 않는다.
- 정정은 기술 표준·공식 제품 문서·OWASP·CVE Program과 수학적으로 결정되는 라우팅 계산을 기준으로 했다.

### Verdict
- 문항 수·ID·MD에서 파생한 JSON의 일대일 보존은 유지한다.
- 문항별 판정은 아래 표에 기록했다. 법령·버전·당시 기준 문항은 현행성 주의로 분리했다.
- 총 21개 회차 행에 기술 정정 또는 독립 풀이를 위한 표현 보완을 반영했다. 이 중 핵심 기술 오답·과장에 해당한 13개는 표준·공식 문서 또는 결정적 계산으로 정정했다.
- 2026-07-17 PDF 대조에서 R06-Q01의 TCP Open/Half-Open 스캔 조건과 A~E 레이블을 확인해, 기존 복원 한계를 해소했다. PDF는 블로그 편집본이며 KCA 공식 원문으로 승격하지 않는다.

### Item-by-item Disposition
표기: `OK` 현재 유지, `TIME` 당시 법령·버전/환경 주의, `WORDING` 표현 보완, `FIXED` 기술 정정 반영, `LIMITED` 복원 한계.

| range | item dispositions |
|---|---|
| 1~16 | 1 OK, 2 OK, 3 TIME, 4 OK, 5 WORDING, 6 FIXED, 7 OK, 8 OK, 9 TIME, 10 OK, 11 FIXED, 12 OK, 13 OK, 14 TIME, 15 OK, 16 OK |
| 17~31 | 17 OK, 18 FIXED, 19 OK, 20 FIXED, 21 OK, 22 OK, 23 OK, 24 OK, 25 OK, 26 OK, 27 OK, 28 OK, 29 OK, 30 TIME, 31 FIXED |
| 32~47 | 32 OK, 33 OK, 34 OK, 35 OK, 36 OK, 37 OK, 38 OK, 39 TIME, 40 OK, 41 OK, 42 OK, 43 WORDING, 44 WORDING, 45 FIXED, 46 OK, 47 TIME |
| 48~63 | 48 FIXED, 49 OK, 50 TIME, 51 OK, 52 OK, 53 OK, 54 OK, 55 OK, 56 FIXED, 57 OK, 58 OK, 59 OK, 60 TIME, 61 OK, 62 OK, 63 OK |
| 64~79 | 64 FIXED, 65 OK, 66 OK, 67 OK, 68 OK, 69 OK, 70 FIXED, 71 WORDING, 72 OK, 73 OK, 74 OK, 75 TIME, 76 FIXED, 77 OK, 78 FIXED, 79 FIXED |
| 80~95 | 80 FIXED, 81 FIXED, 82 FIXED, 83 FIXED, 84 TIME, 85 TIME, 86 OK, 87 OK, 88 TIME, 89 OK, 90 OK, 91 OK, 92 OK, 93 WORDING, 94 OK, 95 FIXED |
| 96~100 | 96 OK, 97 OK, 98 FIXED, 99 FIXED, 100 FIXED |

### Corrected Items and Grounds
| item | correction | ground |
|---|---|---|
| R01-Q11 | Sticky directory에서는 파일 소유자 또는 디렉터리 소유자가 삭제·이름 변경할 수 있다. | [GNU Coreutils mode structure](https://www.gnu.org/s/coreutils/manual/html_node/Mode-Structure.html) |
| R02-Q02 | 델파이법을 직접 집단토론이 아니라 반복·익명 전문가 의견수렴으로 정정했다. | 위험분석 방법론의 정의 정합성 검토 |
| R02-Q04 | 문서 자체와 최고경영자 승인을 분리했다. | 정책 문구의 논리 관계 검토 |
| R02-Q15 | SQL 특수문자 차단만 제시한 답을 Prepared Statement 중심으로 정정했다. | [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) |
| R03-Q14 | AH 실패의 확정 근거를 NAT에 의한 IP 주소 변경으로 한정하고 SAD 추정을 제거했다. | [RFC 4302](https://www.rfc-editor.org/info/rfc4302/), [RFC 3022](https://www.rfc-editor.org/info/rfc3022/) |
| R04-Q01 | CVE 연도를 발견 연도가 아닌 ID 예약 또는 공개 연도로 정정했다. | [CVE Program](https://www.cve.org/about/Process) |
| R04-Q09 | HTTP OPTIONS 요청의 종료 빈 줄을 명시했다. | [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html) |
| R05-Q01 | 저널링을 명령 실행 로그가 아닌 파일시스템 변경 기록으로 정정했다. | [Linux Kernel ext3 documentation](https://www.kernel.org/doc/html/latest/filesystems/ext3.html) |
| R05-Q04 | URL 디코딩된 조건절이 SQL Injection의 문자열 결합 입력이라는 점을 1차 보안 지침으로 재확인해 TIME 경계를 해제했다. | [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) |
| R05-Q07 | 원격 include/require 차단 설정을 `allow_url_include=Off`로 정정했다. | [PHP Manual](https://www.php.net/manual/en/features.remote-files.php) |
| R05-Q13 | XSS 핵심 대응을 입력 치환이 아닌 출력 위치별 인코딩으로 정정했다. | [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) |
| R05-Q15~16 | 디렉터리 리스팅을 정보노출 취약점으로, AXFR 실패를 안전성 미확정 상태로 정정했다. | [RFC 5936](https://www.rfc-editor.org/info/rfc5936/)은 AXFR 접근 제한과 권한 부여를 별도로 다룬다. |
| R06-Q02~03 | SNMPv3 privacy와 DNS ANY 질의의 보안 의미를 과장 없이 정정했다. | [RFC 3414](https://www.rfc-editor.org/info/rfc3414/) |
| R06-Q04 | `10.0.122.64`의 최장 일치 라우트를 `10.0.64.0/18 -> 10.0.160.3`으로 정정했다. | CIDR 범위와 longest-prefix-match 계산 |
| R06-Q01 | PDF 편집본에서 TCP Open/Half-Open Scan의 A~E 패킷 흐름을 확인해 독립 풀이 가능하게 복원했다. | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html) 및 로컬 1~28회 PDF 편집본 대조 (KCA 공식 원문 아님) |
| R06-Q16 | 같은 MAC만으로 ARP 스푸핑을 단정하지 않도록 조건을 추가했다. | [RFC 1027](https://www.rfc-editor.org/info/rfc1027/)의 Proxy ARP 동작 |
| R07-Q03~05 | Zone 정의를 정정하고, Snort offset/depth 범위와 injector 정의를 정정했다. | [Snort Rule Guide](https://docs.snort.org/rules/options/payload/oddw), [MITRE ATT&CK T1055](https://attack.mitre.org/techniques/T1055/) |

### Limits
- 법령·보관기간·개인정보 영향평가·ISMS 이전 체계·운영체제 경로는 해당 시점 기출 복원값으로 보존한다. 현행 법령 답으로 재사용하려면 별도 법령 대조가 필요하다.
- `source-derived`는 회차 MD에서 JSON이 결정적으로 파생되었음을 뜻한다. KCA 공식 시험지 여부의 승격 표기가 아니다.

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

- `raw/sources/clipping/7a3822b1f191e2ec3be5f8754373ee7e4c492d4ac6ffb5973e823d4594ad1159/0a799ff8f1da6ce002869d29bf9f431d858b4db1b6e5b18e6b146f06007387fb/manifest.json`
