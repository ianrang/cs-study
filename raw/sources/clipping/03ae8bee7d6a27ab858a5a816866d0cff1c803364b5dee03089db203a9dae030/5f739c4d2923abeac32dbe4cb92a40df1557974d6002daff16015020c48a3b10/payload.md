---
title: "정보보안기사 실기 복원 101~513번 기술 정확성 전수 검증"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, verification]
status: active
date_created: 2026-07-17
date_updated: 2026-07-17
source_paths:
  - "first-100-content-review-2026-07-16.md"
  - "prompt-completeness-cross-verify-report.md"
  - "round-file-pdf-exhaustive-cross-verify-report.md"
  - "../01-rounds/2016-01-practical-07.md"
  - "../01-rounds/2016-02-practical-08.md"
  - "../01-rounds/2017-01-practical-09.md"
  - "../01-rounds/2017-02-practical-10.md"
  - "../01-rounds/2018-01-practical-11.md"
  - "../01-rounds/2018-02-practical-12.md"
  - "../01-rounds/2019-01-practical-13.md"
  - "../01-rounds/2019-02-practical-14.md"
  - "../01-rounds/2020-01-practical-15.md"
  - "../01-rounds/2020-02-practical-16.md"
  - "../01-rounds/2021-01-practical-17.md"
  - "../01-rounds/2021-02-practical-18.md"
  - "../01-rounds/2022-01-practical-19.md"
  - "../01-rounds/2022-02-practical-20.md"
  - "../01-rounds/2022-04-practical-21.md"
  - "../01-rounds/2023-01-practical-22.md"
  - "../01-rounds/2023-02-practical-23.md"
  - "../01-rounds/2023-04-practical-24.md"
  - "../01-rounds/2024-01-practical-25.md"
  - "../01-rounds/2024-02-practical-26.md"
  - "../01-rounds/2024-04-practical-27.md"
  - "../01-rounds/2025-01-practical-28.md"
  - "../01-rounds/2025-02-practical-29.md"
  - "../01-rounds/2025-04-practical-30.md"
  - "../01-rounds/2026-01-practical-31.md"
source_count: 28
provenance: inferred
summary: "P1-T1의 후반 범위(R07-Q06~R31-Q18) 413문항을 원본 회차 MD 기준으로 기술 정확성, 독립 풀이성, 시대·제품 경계, 복원 한계를 전수 판정한 감사 기록. KCA 공식 원문을 주장하지 않는다."
evergreen: false
---

# 정보보안기사 실기 복원 101~513번 기술 정확성 전수 검증

## Scope and Boundary

- 대상은 R07-Q06부터 R31-Q18까지 413문항이다. [1~100번 검증](first-100-content-review-2026-07-16.md)과 합치면 31회차 513문항 전부를 덮는다.
- 회차 MD는 비공식 복원 SoT이고, 이 보고서는 KCA 공식 시험지 문구·표·보기를 복원하거나 공식 정답이라고 주장하지 않는다.
- 표기의 `OK`는 현재 복원 범위에서 기술적 모순을 확인하지 못했다는 뜻이다. `TIME`은 시험 당시 법령·제품·프로토콜 세대에 한정된다. `LIMITED`는 원문 표·보기·산식·벤더/버전 전제가 없어 정답을 확정할 수 없다는 뜻이다.

## Evidence Codes

각 판정의 대괄호 코드는 아래 URL 또는 해당 회차 MD `source_paths`의 복원 URL을 뜻한다. `S`는 기술 정답의 공식 승격이 아니라 원본 복원 경계만 확인한 경우다.

| code | ground |
|---|---|
| S | 해당 회차 MD의 `source_paths`에 보존된 비공식 복원 원천; KCA 공식 원문 미확보 |
| P | [RFC 4301 IPsec security architecture](https://www.rfc-editor.org/rfc/rfc4301.html) |
| H | [RFC 9111 HTTP caching](https://www.rfc-editor.org/rfc/rfc9111.html) |
| T | [RFC 8446 TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html) |
| W | [Wireshark DNS display-filter reference](https://www.wireshark.org/docs/dfref/d/dns.html) |
| N | [Netfilter iptables limit and ICMP guidance](https://netfilter.org/documentation/HOWTO/packet-filtering-HOWTO-7.html) |
| R | [Netfilter length-match semantics](https://netfilter.org/documentation/HOWTO/netfilter-extensions-HOWTO-3.html) |
| SN | [Snort offset/depth/distance/within guide](https://docs.snort.org/rules/options/payload/oddw) |
| D | [BIND 9 allow-transfer reference](https://bind9.readthedocs.io/en/latest/reference.html#allow-transfer) |
| G | [MITRE CAPEC-125 Slow HTTP DoS](https://capec.mitre.org/data/definitions/125.html) |
| UR | [RFC 3704 ingress filtering/uRPF](https://www.rfc-editor.org/rfc/rfc3704.html) |
| M | [MySQL bind_address reference](https://dev.mysql.com/doc/refman/9.1/en/server-system-variables.html) |
| PH | [PHP URL include configuration](https://www.php.net/manual/en/filesystem.configuration.php) |
| A | [Apache core configuration reference](https://httpd.apache.org/docs/2.4/mod/core.html) |
| O | [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) |
| SS | [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) |
| X | [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) |
| C | [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) |
| U | [Microsoft UAC elevation behavior](https://learn.microsoft.com/en-au/windows/security/application-security/application-control/user-account-control/how-it-works) |
| WL | [Microsoft HTTP Server API error logging](https://learn.microsoft.com/en-us/windows/win32/http/configuring-http-server-api-error-logging) and [Microsoft DHCP troubleshooting](https://learn.microsoft.com/es-es/troubleshoot/windows-server/networking/troubleshoot-dhcp-guidance) |
| K | [NIST cryptographic hash-function glossary](https://csrc.nist.gov/glossary/term/cryptographic_hash_function) |
| L | [대한민국 국가법령정보센터](https://www.law.go.kr) — 현행법 확인용; 과거 회차 정답의 무단 치환 근거가 아님 |
| I | [MITRE ATT&CK](https://attack.mitre.org) 또는 [CVE Program](https://www.cve.org) 등 해당 제품·공격의 공개 1차 자료 |
| PC | 현재 보유한 1~28회 문제·답 PDF 편집본의 동일 문항 대조. 제작자가 Tistory/Naver 블로그를 출처로 밝힌 비공식 편집본이며 KCA 공식 원문이 아니다. 파일·해시·한계는 [PDF source cross-verify report](pdf-source-cross-verify-report.md)에 보존한다. |
| KRN | [Linux kernel printk documentation](https://docs.kernel.org/core-api/printk-basics.html) 및 [kernel timestamp format](https://docs.kernel.org/admin-guide/kernel-parameters.html) |
| SQ | [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) 및 [Blind SQL Injection](https://owasp.org/www-community/attacks/Blind_SQL_Injection) |
| F | [RFC 959 File Transfer Protocol](https://www.rfc-editor.org/rfc/rfc959.html) |
| RR | [RFC 903 Reverse Address Resolution Protocol](https://www.rfc-editor.org/rfc/rfc903.html) |
| NT | [NTP 4.2.8-series `ntp.conf` reference](https://www.ntp.org/documentation/4.2.8-series/ntp.conf/) |
| MS | [Microsoft `net session` reference](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh750729%28v%3Dws.11%29) |
| IU | [Microsoft IIS URL Rewrite outbound-rules guide](https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/creating-outbound-rules-for-url-rewrite-module) |
| LC | [lastcomm(1)](https://man7.org/linux/man-pages/man1/lastcomm.1.html) |
| TCP | [RFC 9293 Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293.html) |
| UPI | 사용자가 제공한 2026-07-17 사진 3장. 회차·번호는 원본과 다를 수 있는 비공식 학습 자료이므로, 일치하는 문항의 표·보기·질문 구조를 보강하는 용도로만 사용하며 KCA 공식 원문은 아니다. |

## Item Dispositions

문항별 배열은 `Rxx` 행의 `Q01`부터 순서대로 해당 문항 ID를 뜻한다. 예: `R07` 행의 첫 값은 `R07-Q06`이다. 판정 자체의 이유는 다음과 같다: `OK`는 인용 근거와 대조해 기술 모순을 찾지 못함, `TIME`은 시험 당시 법령·제품·표준 세대에 묶여 현행값으로 치환하지 않음, `WORDING`은 핵심어는 유지하면서 충분조건 단정·환경 일반화를 제거함, `FIXED`는 아래 개별 사유의 확정 오류를 최소 수정함, `LIMITED`는 표·보기·산식 등 결정 자료가 없어 답을 만들지 않음이다. 모든 항목의 근거 URL은 대괄호 코드로 연결한다.

| round / item range | ordered dispositions and grounds |
|---|---|
| R07 / Q06–Q16 | Q06 OK[W]; Q07 OK[I]; Q08 OK[I]; Q09 OK[S]; Q10 TIME[L]; Q11 OK[N]; Q12 FIXED[S]; Q13 TIME[L]; Q14 FIXED[PC]; Q15 FIXED[H]; Q16 OK[I] |
| R08 / Q01–Q16 | Q01 FIXED[M]; Q02 TIME[L]; Q03 TIME[S]; Q04 OK[S]; Q05 OK[S]; Q06 FIXED[PC]; Q07 OK[S]; Q08 FIXED[PC]; Q09 TIME[L]; Q10 FIXED[PC]; Q11 OK[P]; Q12 OK[O]; Q13 WORDING[PC]; Q14 OK[I]; Q15 FIXED[S]; Q16 TIME[L] |
| R09 / Q01–Q16 | Q01 OK[S]; Q02 OK[N]; Q03 OK[S]; Q04 OK[A]; Q05 OK[S]; Q06 TIME[L]; Q07 FIXED[T]; Q08 FIXED[S]; Q09 OK[S]; Q10 OK[S]; Q11 TIME[L]; Q12 TIME[S]; Q13 TIME[S]; Q14 OK[S]; Q15 TIME[L]; Q16 FIXED[N] |
| R10 / Q01–Q16 | Q01 WORDING[I]; Q02 FIXED[F]; Q03 OK[S]; Q04 OK[S]; Q05 OK[S]; Q06 TIME[L]; Q07 OK[S]; Q08 TIME[L]; Q09 TIME[L]; Q10 OK[S]; Q11 OK[I]; Q12 TIME[L]; Q13 FIXED[N]; Q14 FIXED[UPI,TCP]; Q15 OK[N]; Q16 FIXED[S] |
| R11 / Q01–Q15 | Q01 OK[U]; Q02 OK[S]; Q03 WORDING[P]; Q04 OK[D]; Q05 FIXED[G]; Q06 TIME[L]; Q07 FIXED[S]; Q08 TIME[L]; Q09 OK[S]; Q10 OK[I]; Q11 WORDING[S]; Q12 TIME[L]; Q13 TIME[L]; Q14 OK[O]; Q15 OK[SN] |
| R12 / Q01–Q16 | Q01 OK[I]; Q02 FIXED[P]; Q03 OK[H]; Q04 OK[S]; Q05 OK[S]; Q06 OK[S]; Q07 TIME[L]; Q08 WORDING[S]; Q09 OK[S]; Q10 WORDING[S]; Q11 WORDING[S]; Q12 OK[S]; Q13 OK[SN]; Q14 OK[S]; Q15 FIXED[R]; Q16 FIXED[L] |
| R13 / Q01–Q15 | Q01 OK[S]; Q02 OK[S]; Q03 OK[S]; Q04 OK[I]; Q05 TIME[S]; Q06 OK[O]; Q07 FIXED[S]; Q08 OK[S]; Q09 OK[S]; Q10 OK[S]; Q11 FIXED[A]; Q12 FIXED[S]; Q13 FIXED[P]; Q14 OK[SN]; Q15 FIXED[S] |
| R14 / Q01–Q16 | Q01 OK[S]; Q02 OK[S]; Q03 WORDING[P]; Q04 OK[U]; Q05 TIME[L]; Q06 TIME[S]; Q07 FIXED[S]; Q08 OK[A]; Q09 TIME[L]; Q10 TIME[L]; Q11 TIME[S]; Q12 OK[S]; Q13 OK[S]; Q14 OK[S]; Q15 WORDING[A]; Q16 FIXED[SN] |
| R15 / Q01–Q16 | Q01 OK[O]; Q02 OK[S]; Q03 OK[S]; Q04 OK[I]; Q05 TIME[L]; Q06 TIME[L]; Q07 OK[T]; Q08 TIME[L]; Q09 OK[S]; Q10 OK[S]; Q11 FIXED[P]; Q12 FIXED[PC]; Q13 TIME[L]; Q14 FIXED[S]; Q15 OK[H]; Q16 TIME[PC,L] |
| R16 / Q01–Q16 | Q01 WORDING[S]; Q02 OK[L]; Q03 OK[S]; Q04 OK[S]; Q05 OK[I]; Q06 FIXED[T]; Q07 FIXED[PC]; Q08 WORDING[S]; Q09 OK[S]; Q10 OK[T]; Q11 OK[H]; Q12 WORDING[S]; Q13 FIXED[S]; Q14 OK[O]; Q15 FIXED[PC]; Q16 TIME[L] |
| R17 / Q01–Q16 | Q01 OK[I]; Q02 OK[I]; Q03 FIXED[I]; Q04 OK[I]; Q05 OK[I]; Q06 WORDING[S]; Q07 TIME[L]; Q08 TIME[L]; Q09 OK[S]; Q10 TIME[L]; Q11 OK[L]; Q12 FIXED[S]; Q13 TIME[L]; Q14 FIXED[I]; Q15 FIXED[PC,SN]; Q16 FIXED[A] |
| R18 / Q01–Q16 | Q01 OK[I]; Q02 OK[I]; Q03 OK[O]; Q04 OK[U]; Q05 OK[S]; Q06 OK[S]; Q07 OK[I]; Q08 WORDING[S]; Q09 FIXED[G]; Q10 FIXED[S]; Q11 OK[O]; Q12 FIXED[UR]; Q13 OK[N]; Q14 FIXED[T]; Q15 TIME[S]; Q16 FIXED[S] |
| R19 / Q01–Q16 | Q01 OK[S]; Q02 OK[I]; Q03 OK[S]; Q04 OK[I]; Q05 WORDING[S]; Q06 OK[S]; Q07 TIME[A]; Q08 FIXED[S]; Q09 OK[S]; Q10 OK[I]; Q11 OK[S]; Q12 TIME[L]; Q13 WORDING[S]; Q14 FIXED[S]; Q15 FIXED[A]; Q16 FIXED[PC] |
| R20 / Q01–Q16 | Q01 OK[H]; Q02 FIXED[S]; Q03 OK[S]; Q04 OK[S]; Q05 OK[S]; Q06 OK[P]; Q07 OK[I]; Q08 OK[A]; Q09 OK[I]; Q10 TIME[L]; Q11 TIME[L]; Q12 WORDING[S]; Q13 OK[SN]; Q14 FIXED[S]; Q15 FIXED[PC,N]; Q16 FIXED[S] |
| R21 / Q01–Q16 | Q01 OK[S]; Q02 OK[S]; Q03 FIXED[S]; Q04 WORDING[S]; Q05 OK[I]; Q06 FIXED[PC]; Q07 WORDING[P]; Q08 FIXED[S]; Q09 FIXED[S]; Q10 OK[A]; Q11 OK[S]; Q12 WORDING[S]; Q13 TIME[L]; Q14 FIXED[N]; Q15 OK[S]; Q16 FIXED[D] |
| R22 / Q01–Q18 | Q01 FIXED[S]; Q02 TIME[S]; Q03 OK[S]; Q04 OK[H]; Q05 FIXED[PH]; Q06 OK[SN]; Q07 OK[N]; Q08 OK[S]; Q09 OK[O]; Q10 OK[O]; Q11 TIME[L]; Q12 FIXED[S]; Q13 OK[U]; Q14 OK[S]; Q15 OK[H]; Q16 OK[N]; Q17 OK[O]; Q18 TIME[L] |
| R23 / Q01–Q18 | Q01 FIXED[WL]; Q02 FIXED[S]; Q03 OK[S]; Q04 TIME[L]; Q05 FIXED[PC,KRN]; Q06 OK[O]; Q07 OK[S]; Q08 OK[I]; Q09 OK[I]; Q10 OK[I]; Q11 OK[S]; Q12 OK[S]; Q13 WORDING[O]; Q14 WORDING[S]; Q15 WORDING[U]; Q16 FIXED[H]; Q17 TIME[L]; Q18 FIXED[D] |
| R24 / Q01–Q18 | Q01 OK[L]; Q02 OK[S]; Q03 OK[S]; Q04 OK[I]; Q05 OK[S]; Q06 WORDING[S]; Q07 FIXED[S]; Q08 OK[I]; Q09 OK[S]; Q10 OK[H]; Q11 OK[S]; Q12 OK[I]; Q13 FIXED[S]; Q14 TIME[S]; Q15 OK[N]; Q16 OK[S]; Q17 TIME[S]; Q18 FIXED[S] |
| R25 / Q01–Q18 | Q01 TIME[U]; Q02 WORDING[S]; Q03 OK[P]; Q04 OK[I]; Q05 OK[S]; Q06 OK[S]; Q07 OK[U]; Q08 OK[S]; Q09 OK[S]; Q10 FIXED[SS]; Q11 OK[S]; Q12 FIXED[S]; Q13 OK[S]; Q14 FIXED[S]; Q15 OK[S]; Q16 WORDING[S]; Q17 FIXED[S]; Q18 FIXED[S] |
| R26 / Q01–Q18 | Q01 TIME[S]; Q02 OK[N]; Q03 WORDING[S]; Q04 OK[H]; Q05 OK[S]; Q06 OK[O]; Q07 OK[I]; Q08 OK[H]; Q09 OK[O]; Q10 OK[S]; Q11 OK[S]; Q12 OK[S]; Q13 FIXED[U]; Q14 TIME[L]; Q15 FIXED[S]; Q16 OK[O]; Q17 WORDING[PC]; Q18 WORDING[I] |
| R27 / Q01–Q18 | Q01 OK[S]; Q02 OK[RR]; Q03 OK[S]; Q04 TIME[L]; Q05 TIME[S]; Q06 WORDING[I]; Q07 OK[O]; Q08 OK[H]; Q09 TIME[U]; Q10 OK[S]; Q11 OK[S]; Q12 OK[S]; Q13 OK[S]; Q14 TIME[L]; Q15 OK[S]; Q16 WORDING[S]; Q17 FIXED[PC,O]; Q18 WORDING[NT] |
| R28 / Q01–Q18 | Q01 OK[N]; Q02 OK[O]; Q03 WORDING[S]; Q04 OK[H]; Q05 OK[H]; Q06 OK[I]; Q07 WORDING[S]; Q08 OK[S]; Q09 WORDING[S]; Q10 OK[S]; Q11 TIME[L]; Q12 WORDING[S]; Q13 OK[S]; Q14 WORDING[U]; Q15 WORDING[P]; Q16 OK[S]; Q17 TIME[I]; Q18 WORDING[S] |
| R29 / Q01–Q18 | Q01 OK[S]; Q02 OK[U]; Q03 OK[T]; Q04 OK[O]; Q05 WORDING[O]; Q06 OK[S]; Q07 OK[N]; Q08 OK[O]; Q09 OK[S]; Q10 TIME[L]; Q11 OK[A]; Q12 WORDING[LC]; Q13 OK[T]; Q14 WORDING[O]; Q15 WORDING[S]; Q16 OK[S]; Q17 OK[U]; Q18 TIME[L] |
| R30 / Q01–Q18 | Q01 WORDING[S]; Q02 FIXED[P]; Q03 FIXED[MS]; Q04 OK[S]; Q05 OK[S]; Q06 OK[S]; Q07 OK[S]; Q08 FIXED[UPI]; Q09 OK[I]; Q10 OK[U]; Q11 WORDING[S]; Q12 WORDING[S]; Q13 OK[S]; Q14 OK[S]; Q15 WORDING[UPI]; Q16 OK[SN]; Q17 WORDING[S]; Q18 WORDING[O] |
| R31 / Q01–Q18 | Q01 OK[S]; Q02 WORDING[I]; Q03 OK[N]; Q04 OK[I]; Q05 FIXED[WL]; Q06 FIXED[K]; Q07 WORDING[S]; Q08 OK[O]; Q09 OK[S]; Q10 OK[IU]; Q11 TIME[L]; Q12 OK[S]; Q13 TIME[L]; Q14 OK[O]; Q15 TIME[L]; Q16 FIXED[T]; Q17 FIXED[T,X]; Q18 FIXED[C] |

## Item-Specific Correction Reasons

`FIXED` 항목의 변경 사유는 다음과 같다. 각 행의 공식·1차 근거 URL은 위 문항별 판정 표의 코드에 연결한다.

| round | corrected item IDs and reason |
|---|---|
| R07 | Q12: ROI 비율과 순편익을 구분; Q15: `must-revalidate`와 source port 443의 과도한 추론 제거 |
| R08 | Q01: MySQL `bind-address`를 리스닝 주소와 권한 통제로 분리; Q15: `/home/*` glob 범위를 전체 파일 주장으로 일반화하지 않음 |
| R09 | Q07: TLS 1.2 이하 record-version 설명을 TLS 1.3에 일반화하지 않음; Q08: Delphi를 익명 반복 설문으로 정정; Q16: iptables `limit`의 허용/초과 처리 의미 보정 |
| R10 | Q13: DROP/REJECT의 보안 우열 단정을 제거; Q16: promiscuous mode와 단일 로그를 공격 확정 근거로 쓰지 않음 |
| R11 | Q05: Slowloris를 느린 미완성 HTTP 헤더 공격으로 정정; Q07: SNMP Trap/Inform을 주기 보고와 구별 |
| R12 | Q02: ESP 무결성·인증을 SA 선택 사항으로 보정; Q15: `--length 100`의 정확 일치 의미 보정; Q16: 비밀번호 저장을 hash/KDF와 법령 시점으로 분리 |
| R13 | Q07: Delphi 정의 보정; Q11: `AddType`만으로 실행 차단 불가; Q12: IDS/IPS 배치를 정책·운영 조건으로 제한; Q13: AH/ESP 적용 범위 보정; Q15: `robots.txt`를 접근통제로 오인하지 않음 |
| R14 | Q07: CC의 평가 기준/인증 표현 보정; Q16: Snort `offset`/`depth`가 룰과 모순되는 점을 보정 |
| R15 | Q11: ESP 인증 범위의 SA 의존성 보정; Q14: `umask 077`과 `266`의 실제 생성 권한 차이 보정 |
| R16 | Q06: TLS 1-RTT·0-RTT 재개/재전송 한계 보정; Q13: SPF·DKIM·DMARC의 검증 주체와 범위 보정 |
| R17 | Q03: ATT&CK를 고정 선형 Kill Chain 확장으로 보지 않음; Q12: out-of-band NAC의 802.1X/스위치 강제 가능성 반영; Q14: 404만으로 명령 실행 성공을 단정하지 않음; Q16: Apache `/` 허용의 노출 범위 보정 |
| R18 | Q09: Slowloris 설명 보정; Q10: deep link 자체와 검증/인가 부재 위험 분리; Q12: uRPF의 비대칭 경로 조건 반영; Q14: ECDHE-RSA와 SPF/DKIM 역할 보정; Q16: DNS ANY 단일 로그의 DRDoS 확정 금지 |
| R19 | Q08: PGP/PEM의 일반적 보안 우열 단정 제거; Q14: 주어진 자산 목록의 구체적 식별·지원종료 사실 반영; Q15: AddType의 한계 보정 |
| R20 | Q02: Delphi 정의 보정; Q14: Sendmail 빈칸 4개의 실제 값 보정; Q16: 위험 처리 방식을 제목이 아닌 의미로 답하도록 보정 |
| R21 | Q03: 근거 없는 DoA 약어 확장 제거; Q08: Delphi 정의 보정; Q09: `JMP ESP`와 `RET` 제어흐름 구별; Q14: iptables `recent --set` 선행 조건 추가; Q16: DNS transfer와 update 지시자 구별 |
| R22 | Q01: OSPF 변화 갱신과 주기 refresh를 함께 반영; Q05: PHP `allow_url_include` 지시자로 보정; Q12: DoA 확장을 확정 답으로 만들지 않음 |
| R23 | Q01: Windows DHCP/IIS 경로 보정; Q02: System V AMD64 `printf` 인자 레지스터 보정; Q16: HTTP 헤더의 증거 한계 보정; Q18: `zone` 문자열을 `korea.co.kr`으로, 파일명과 transfer/update 지시자를 별도로 보정 |
| R24 | Q07: ISO 31000에 고정 DoA 용어가 있다는 주장 제거; Q13: setgid의 group 상속과 root 권한을 구별; Q18: 올바른 `access_times` 필드명 보정 |
| R25 | Q10: SSRF는 allowlist·DNS/리다이렉트·egress 조건을 함께 검증; Q12: 2015 Gartner UEBA와 SOAR 혼동 보정; Q14: ping 스니핑 탐지의 단일 증거 한계; Q17: multicast MAC과 정적 ARP 전제 보정; Q18: 정적·샌드박스 분석 구분 |
| R26 | Q13: UAC 화면만으로 계정/파일 손상 확정 금지; Q15: promiscuous mode 로그의 대체 원인 반영 |
| R30 | Q02: AH와 ESP 모두 anti-replay sequence number를 가짐 |
| R31 | Q05: IIS/DHCP 로그 경로 보정; Q06: hash는 복호화 가능한 암호화가 아님; Q16: TLS 1.2 RSA와 (EC)DHE/TLS 1.3 경계 보정; Q17: Fiddler/SSLv3/XSS 증거 한계 보정; Q18: CSRF 토큰 생성뿐 아니라 전달·검증 필요 |

## PDF Reconstruction Recovery Audit (2026-07-17)

현재 보유한 1~28회 문제·답 PDF 편집본과 사용자가 제공한 보조 사진을 대조했다. 모두 KCA 공식 시험지나 공식 정답이 아니다. 다만 아래 항목은 기존 MD에 없던 결정 조건을 실제로 제공하므로 `LIMITED`를 해소할 근거가 된다. `PC`의 파일 정체성·해시·출처 한계는 [PDF source cross-verify report](pdf-source-cross-verify-report.md)에 기록한다.

| item ID | disposition | PDF로 확인한 결정 조건 / 반영 사유 | independent-use boundary |
|---|---|---|---|
| R07-Q14 | FIXED | 두 cron 표현식과 여섯 필드 `root` 위치를 확인했다. 첫 표현식은 매시 0분이다. | 실제 crontab 종류·소유자 권한을 별도 확인해야 한다. |
| R08-Q06 | FIXED | 3478/2324 SYN 번호와 A~C의 위치가 확인됐다. | TCP SYN이 sequence space 1을 소비한다는 표준 계산을 적용했다. |
| R08-Q08 | FIXED | UDP, DNS cache, TTL을 묻는 전체 설명이 확인됐다. | UDP는 일반 질의의 기대 답이며 DNS 전체의 유일 전송계층이라는 뜻은 아니다. |
| R08-Q10 | FIXED | 수용·회피·전가 각각의 정의가 확인됐다. | 특정 조직의 위험 승인 기준은 별도다. |
| R08-Q13 | WORDING | 연계보관성의 질문과 수집·이동·분석·보관·제출의 핵심 단계가 확인됐다. | 같은 PDF 답안 안에서 분석/보관 열거 순서가 달라 단일 순서 채점은 하지 않는다. |
| R15-Q12 | FIXED | `/proc/5900/exe`, 복원 명령과 `history`/`cmdline` 선택지가 확인됐다. | 대상 PID의 생존·접근 권한이 필요하다. |
| R15-Q16 | TIME | 신청서 4개 항목과 PDF 편집 답안 4개 지적점을 확인했다. | 개인정보 법령의 적법성은 시험 당시 법령 버전으로 별도 대조한다. |
| R16-Q07 | FIXED | `strace -e trace=open ps \| more`와 목적 문장이 확인됐다. | 실제 컴파일 경로 진단 가능성은 바이너리·심볼 정보에 좌우된다. |
| R16-Q15 | FIXED | B 대책의 ARO=0.25, 감소 ALE=20,000, 비용=4,000을 확인했다. | 효과는 제시된 산식(감소 ALE-운영비) 안에서만 비교한다. |
| R17-Q15 | FIXED | Snort 룰 문자열과 네 개의 질문을 확인했다. | 편집본 룰의 HTTP 문법·오탈자는 정상 룰로 일반화하지 않는다. |
| R19-Q16 | FIXED | 두 위험평가 표와 복합접근법 예시를 확인했다. | 제시 답안은 하나의 분석 예시이며 조직 고유 위험평가를 대체하지 않는다. |
| R20-Q15 | FIXED | (C)가 `no ip directed-broadcast 100`임을 확인했다. | IOS 플랫폼·버전에 따라 ACL 동작 및 명령 지원이 다를 수 있다. |
| R21-Q06 | FIXED | 불완전한 암호화 저장 취약점의 전체 stem과 A~C가 확인됐다. | 이 체크리스트만으로 암호 설계 전체의 안전성을 판정하지 않는다. |
| R23-Q05 | FIXED | syslog 샘플의 A~C 레이블과 `kernel: [시간]` 형식을 확인했다. | 대괄호 수치를 PID로 단정하지 않으며 로그 포맷·경로는 환경 의존이다. |
| R26-Q17 | WORDING | Oracle 예시 권한 4개와 최소화 방법 5개를 확인했다. | 권한명·매개변수는 Oracle 제품/버전에 한정된다. |
| R27-Q17 | FIXED | Java `?`, `prepareStatement`, `setString`, `executeQuery()` 네 빈칸이 확인됐다. | JDBC `PreparedStatement` 문맥에 한정된다. |
| R10-Q14 | FIXED | 사용자 사진에서 TCP 3-way handshake와 4-way termination의 표·각 빈칸 위치를 확인했다. 사진의 예시 순서번호는 다르므로 기존 복원 답 `B=344`, `D=677`으로부터 시작 순서번호 `343`, `676`을 역산해 별도로 유지했다. | TCP SYN/FIN의 sequence-space 소비는 RFC 9293으로 대조했다. 사진은 KCA 공식 원문이 아니다. |
| R30-Q08 | FIXED | 사용자 사진의 실제 문장과 보기는 `대규모 데이터 로그인 자격증명`을 대입해 계정을 탈취하는 행위를 묻고, 보기에서 `크리덴셜 스터핑`을 선택하게 한다. | `무차별 공격기법`은 설명의 분류어이며 `역방향 무차별 대입 공격`을 복수 정답으로 만들지 않는다. 사진은 KCA 공식 원문이 아니다. |
| R30-Q15 | WORDING | 사용자 사진에서 EAM/IAM의 공통 기능 1개, EAM 관리 대상, EAM 문제점 2개, IAM 추가 기능을 각각 묻는 네 요구사항을 확인했다. | 사진에 답안 페이지는 없어 답은 기존 복원 원천과의 공통 핵심어로 제한한다. EAM/IAM 제품별 명칭·범위는 보편 정의로 단정하지 않는다. |

사용자 제공 사진으로 기존 `LIMITED` 세 항목의 결정적인 표·보기·질문 구조를 모두 확인했다. 따라서 이 전수 검증의 `LIMITED`는 **0건**이다. 다만 사진은 회차·번호가 원문과 다를 수 있는 비공식 보조 자료이며, KCA 공식 원문·공식 정답으로 취급하지 않는다.

## TIME Boundary Audit (2026-07-17)

이전 전수 검증의 `TIME` 84개를 다시 읽고, PDF 복원으로 새로 `TIME`이 된 R15-Q16을 포함해 85개를 재분류했다. 이 중 10개는 시간이 아니라 기술 정의·문법·구현 사실이므로 아래의 1차 근거로 `OK`/`FIXED`/`WORDING`으로 전환했다. 따라서 현재 `TIME`은 **75개**다. 법령·인증 체계·제품/배포판 설정은 정확한 시험 시행일 버전 또는 제품 버전이 확인되지 않으면 현행 자료로 추정 치환하지 않았다.

| reassigned item | previous TIME rationale | verified conclusion and primary ground |
|---|---|---|
| R05-Q04 | SQL Injection을 시대 항목으로 묶음 | `OK`: 문자열 결합 SQL 입력이라는 기술 정의는 [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)으로 확인된다. |
| R08-Q14 | 취약 OpenSSL 버전이 과거 사실 | `OK`: CVE-2014-0160의 식별·영향 버전은 [CVE Program](https://www.cve.org/CVERecord?id=CVE-2014-0160)으로 확인되는 역사적 사실이다. |
| R10-Q02 | Active FTP의 역사적 임시 포트 표현 | `FIXED`: 서버 20/tcp와 클라이언트 지정 data port를 [RFC 959](https://www.rfc-editor.org/rfc/rfc959.html)으로 확인했다. `1024` 이상은 원문 복원 답에만 남긴다. |
| R23-Q13 | 업로드 우회 예시가 구형 구현에 의존 | `WORDING`: [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)에 맞춰 Null byte를 레거시 조건부 예시로 한정했다. |
| R27-Q02 | RARP의 레거시 사용 | `OK`: MAC 주소만 아는 호스트의 protocol address 발견이라는 정의는 [RFC 903](https://www.rfc-editor.org/rfc/rfc903.html)으로 확인된다. |
| R27-Q18 | `disable monitor`의 구현/버전 의존 | `WORDING`: [NTP 4.2.8 설정 문서](https://www.ntp.org/documentation/4.2.8-series/ntp.conf/)가 해당 옵션을 확인하므로 지원 버전 한정 표현으로 보정했다. |
| R29-Q12 | process accounting의 설정/경로 의존 | `WORDING`: [lastcomm(1)](https://man7.org/linux/man-pages/man1/lastcomm.1.html)에 따라 process accounting 데이터가 있을 때의 조회 명령임을 명시해 shell history 일반화 제거. |
| R29-Q14 | Null byte 우회의 구형성 | `WORDING`: [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)에 맞춰 NUL 처리 결함이 있는 레거시 구성요소로 한정했다. |
| R30-Q03 | Windows 명령 옵션의 제품성 | `FIXED`: [Microsoft `net session`](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/hh750729%28v%3Dws.11%29)의 문서 구문 `/delete`로 정정했다. |
| R31-Q10 | IIS 모듈의 제품성 | `OK`: [Microsoft IIS URL Rewrite outbound-rules](https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/creating-outbound-rules-for-url-rewrite-module)가 모듈·아웃바운드 규칙을 확인한다. |

남은 75개는 전부 문항별로 아래 셋 중 하나다. 각 ID의 현재 판정과 원천은 위 `Item Dispositions`의 코드로 교차 추적한다.

| retained class | item IDs | why not normalized |
|---|---|---|
| 시험 당시 법령·개인정보·ISMS/ISMS-P·정부 경보/인증 기준 | R01-Q03/Q09/Q14; R02-Q14; R03-Q08/Q16; R06-Q09; R07-Q10/Q13; R08-Q02/Q09/Q16; R09-Q06/Q11/Q15; R10-Q06/Q08/Q09/Q12; R11-Q06/Q08/Q12/Q13; R12-Q07; R14-Q05/Q09/Q10; R15-Q06/Q08/Q13/Q16; R16-Q16; R17-Q07/Q08/Q10/Q13; R19-Q12; R20-Q10/Q11; R21-Q13; R22-Q11/Q18; R23-Q04/Q17; R26-Q14; R27-Q04/Q14; R28-Q11; R29-Q10/Q18; R31-Q11/Q13/Q15 | 현행 법령·인증 항목은 과거 기출의 정답으로 치환할 수 없다. 국가법령정보센터의 [개인정보 영향평가 2016 변경조문](https://www.law.go.kr/LSW/lsSideInfoP.do?chrClsCd=010202&docCls=jo&joBrNo=00&joNo=0035&lsId=&lsiSeq=286175&urlMode=lsScJoRltInfoR)처럼 정확한 시행일 조문이 확보된 개별 항목만 후속 해제 대상이다. |
| OS·배포판·서버·DB·보안제품/설정 | R06-Q05/Q06; R08-Q03; R09-Q12/Q13; R13-Q05; R14-Q06/Q11; R15-Q05; R18-Q15; R19-Q07; R22-Q02; R24-Q14/Q17; R25-Q01; R26-Q01; R27-Q05/Q09; R28-Q17 | 파일 경로·옵션·기본값·지원 여부가 배포판·버전·제품에 의존한다. 원문이 해당 환경을 확정하지 않는 한 하나의 현재 설정을 보편 정답으로 만들지 않는다. |
| 시험 출처가 특정 판본·취약 구현을 전제한 설명/공격 예시 | R04-Q02/Q12; R05-Q11 | OWASP Top 10 판본, 데이터베이스 함수, 악성코드 분석 절차가 원문 보기·제품·시대에 의존한다. 현재 근거로 일반 기술 설명은 가능하지만 누락된 원문 전제를 확정할 수 없다. |

이 표는 `TIME`을 “불확실한 오답”으로 취급하지 않는다. 각 문항은 현재 답의 시험 당시 적합성·환경 종속성·현행 재사용 가능성을 분리한 것이며, **정확한 당시 조문 또는 제품 버전이 새로 확인될 때만** 개별적으로 다시 판정한다.

## Confirmed Corrections

- HTTP cache semantics, source-port inference, TLS record-version scope, PHP remote include controls, Snort cursor semantics, netfilter `limit` and `length` semantics, IPsec ESP/AH coverage, DNS zone transfer controls, and CSRF token validation were corrected using the cited protocol/vendor guidance.
- SQL injection, file upload, XSS, slow HTTP, ARP/promiscuous-mode, uRPF, IDS/IPS/NAC deployment, Windows UAC, and Apache settings were changed only to remove a technically false certainty or a configuration-independent assertion.
- The corrected answers retain the answerable keyword where the reconstructed prompt actually supports one. Where it does not, the report marks the ID `LIMITED` instead of manufacturing packet fields, diagrams, formula inputs, vendor version, or historical legal wording.

## Reconstruction Limits and Time Boundaries

| class | item IDs | reason |
|---|---|---|
| photo-backed reconstructed prompt | R10-Q14; R30-Q08/Q15 | User-provided nonofficial photos supplied the missing TCP table, credential-stuffing choices, and EAM/IAM subquestions. The three are independently usable after reconstruction, but remain explicitly nonofficial and do not establish KCA wording or marking guidance. |
| law, certification, retention, privacy or governance | R07-Q10/Q13; R08-Q02/Q09/Q16; R09-Q06/Q11/Q15; R10-Q06/Q08/Q09/Q12; R11-Q06/Q08/Q12/Q13; R12-Q07/Q16; R15-Q05/Q06/Q08/Q13/Q16; R16-Q16; R17-Q07/Q08/Q10/Q13; R19-Q12; R20-Q10/Q11; R21-Q13; R22-Q11/Q18; R23-Q04/Q17; R25-Q01; R26-Q14; R27-Q04/Q14; R28-Q11; R29-Q10/Q18; R31-Q11/Q13/Q15 | The answer may be appropriate to the exam-time statute/guidance but is not normalized to the current law. Current-law verification must begin with the official law portal [L]. |
| OS/product/version/configuration | R08-Q03/Q14; R09-Q07/Q12/Q13; R10-Q02/Q13/Q16; R11-Q05/Q07; R12-Q15; R14-Q08/Q11/Q15/Q16; R15-Q11/Q14; R18-Q12/Q14; R19-Q07/Q14/Q15; R21-Q14/Q16; R22-Q01/Q02/Q05; R23-Q01/Q02/Q18; R24-Q13/Q18; R25-Q01/Q17; R26-Q01/Q13/Q15/Q18; R27-Q02/Q05/Q18; R30-Q03/Q17; R31-Q05/Q10/Q16/Q17 | A deployment, protocol version, distribution, or product release must be stated. A historical command/path is not a universal operational prescription. |

## P1-T1 Completion Basis

- The preceding first-100 report plus this report contains one disposition for every ID from R01-Q01 through R31-Q18 (513 items).
- All edits were made to round MD SoT only. The prescribed build script regenerated `past-exams.json` and `practice-data.js` while validating 242 learning questions and 513 past-exam items.
- 2026-07-17 validation: `build-practice-data.py --check` passed; `test-practice-contract.py` passed (21 tests); `git diff --check` passed; and `check-local-todo-dag.py todo.md` passed (2 task rows).
- `scripts/lint.py` still reports the pre-existing HIGH 18: missing frontmatter on the nine P1-T2 design documents. It reports no new error from this report or the P1-T1 round changes.
