---
title: "정보보안기사 실기 기출 문항 설명 완전성 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, prompt-completeness, verification]
status: active
date_created: 2026-07-03
date_updated: 2026-07-17
source_paths:
  - "../01-rounds/2013-01-practical-01.md"
  - "../01-rounds/2013-02-practical-02.md"
  - "../01-rounds/2014-01-practical-03.md"
  - "../01-rounds/2014-02-practical-04.md"
  - "../01-rounds/2015-01-practical-05.md"
  - "../01-rounds/2015-02-practical-06.md"
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
source_count: 31
provenance: inferred
summary: "회차별 기출 복원표에서 설명이 빠진 지시문을 탐지하고, 접근 가능한 복원 원천 기준으로 문항 조건·구분 기준·답안 정합성을 보강한 교차검증 결과. 31회는 사용자 제공 원천으로 추가했고, 32회는 검증된 복원 원천 부재로 생성하지 않는다."
evergreen: false
---

# 정보보안기사 실기 기출 문항 설명 완전성 교차검증 리포트

## Verdict
- Prompt completeness: 2026-07-17 현재 보유한 1~28회 문제·답 PDF 편집본 대조로 R06-Q01의 TCP 스캔 A~E 패킷 흐름을 확인해 standalone 풀이 가능하게 복원했다. PDF는 블로그 원천을 명시한 비공식 편집본이며 KCA 공식 원문으로 승격하지 않는다. 세부 판정은 [101~513 content review](101-513-content-review-2026-07-17.md#pdf-reconstruction-recovery-audit-2026-07-17)를 따른다.
- 32회 requested sweep: blocked by source quality, not by local editing. 접근 가능한 공개 자료와 로컬 파일에는 정보보안기사 실기 32회 실제 복원 원천이 없었고, 확인된 32회 관련 Jaesung 글은 "AI 예상 문제"이므로 기출 복원 파일로 승격하지 않는다.
- Logic consistency: pass for answer-topic mapping and standalone practice within the available reconstruction sources. 21회 6·8·9번, 22회 5·10번처럼 기존 답안이 다른 개념으로 수렴하던 항목은 원천 기준으로 정정했다.
- Accuracy boundary: scoped. 1~28회 thodi-lab/blog-source PDF 편집본은 비밀번호 해제 후 대조했지만, KCA 공식 시험 원문 문구와 1:1 일치한다고 주장하지 않는다. 29회는 공개 블로그 복원 원천 기준이다. 이번 세션에 사용자가 제공한 사진으로 R30-Q08의 보기와 R30-Q15의 네 요구사항을 보강했으며, 현재 파일 목록에서 30회 PDF를 재확인하지 못한 사실과는 구분한다. 31회는 사용자 제공 HTML 표와 4번 이미지 원천 기준이다.
- Known source limit: active. PDF 편집본 자체가 `13~28회 온계절님 블로그`, `1~12회 information-security.tistory.com` 출처를 표기하므로 공식 원문 보증 근거가 아니라 패키지형 교차검증 보강 근거로 사용한다.

## Finding Summary
| severity | count | status |
|---|---:|---|
| HIGH | 0 | no newly discovered source-answer topic contradiction in this pass |
| MEDIUM | 0 | 2026-07-17 PDF 대조로 기존 R06-Q01 패킷 흐름 누락을 해소 |
| KNOWN_LIMITED | 0 | 사용자 제공 사진으로 R10-Q14의 TCP 표, R30-Q08의 보기, R30-Q15의 네 요구사항을 보강해 독립 풀이 한계를 해소 |
| SOURCE_BOUNDARY | 1 | 31회 is based on a user-provided HTML table rather than an official KCA release |
| PHOTO_BOUNDARY | 3 | R10-Q14, R30-Q08, R30-Q15는 사용자 제공 비공식 사진을 보조 복원 근거로 사용하며 KCA 공식 원문·정답은 아님 |
| SOURCE_LIMIT | 11 | standalone prompt reconstructed from answer block because source body is image-only |
| OCR_VISUAL | 26 | image prompt restored after local image download, OCR attempt, and visual inspection |
| NAVER_RECON | 16 | prompt restored from Naver analysis/reconstruction text and later checked against thodi-lab/blog-source PDF where in 1~28 scope |
| PDF_COMPILATION_CHECK | 1 | 1~28회 단답형·서술형 problem/problem+answer PDF unlocked and text-extracted; not an official KCA source |
| OCR_NA | 10 | 21~30 source images were representative/stock/title images; problem bodies were text, so no OCR restoration target remained |
| BLOCKED_SOURCE_GAP | 1 | 32회 verified practical restoration source absent; expected-question or prep-summary pages are excluded |

## Completeness Rule
| rule | pass condition | fail condition |
|---|---|---|
| 단답형/개념형 | 설명 문장만으로 답안 후보가 1개로 수렴한다. | "다음 설명"이라고만 되어 있고 실제 설명이 없다. |
| 로그/패킷형 | 로그, 패킷, 명령 결과, HTTP 요청, ARP 테이블 등 판단 자료가 prompt 안에 있다. | 답안은 로그/패킷 세부값을 근거로 하지만 prompt에 판단 자료가 없다. |
| 코드/설정형 | 코드, 설정 파일, 룰, 명령 출력의 핵심 행이 prompt 안에 있다. | "다음 룰", "다음 설정"이라고만 되어 있고 핵심 행이 없다. |
| 그림/표 기반 | 그림·표의 의미가 텍스트로 재구성되어 있다. | 그림·표가 없으면 문제 풀이 경로가 재현되지 않는다. |
| 답안 정합성 | 답안이 prompt에 있는 근거에서 도출된다. | 답안에만 근거가 있고 prompt에는 해당 근거가 없다. |

## Context-Dependent Incomplete Items
21~31회차 범위에서 2026-07-16 strict scan은 standalone-blocking prompt 누락을 찾지 못했다. 이후 PDF·사진·기술 정확성 보강으로 R06-Q01, R10-Q14, R30-Q08·Q15의 결정 조건을 보강했다. 따라서 전체 1~31회차에 남은 독립 풀이 불가 문항은 없다. 21~28회는 thodi-lab/blog-source PDF 편집본과 대조한 범위이고, KCA 공식 원문 문구 일치 검증은 여전히 주장하지 않는다. 29회는 Naver/Jaesung 복원 원천이고, 30회는 이전 PDF 대조 기록·이번 세션의 파일 미확인 상태·사용자 제공 사진을 구분해 추적한다.

## Corrected Scope
| file | corrected item scope |
|---|---|
| `2013-01-practical-01.md` | 위험평가, NMS, 보안정책 문서체계, 개인정보 처리자/취급자/처리시스템 지시문 보강 |
| `2013-02-practical-02.md` | ingress/egress/blackhole, FTP 계열 공격, TCP Wrapper, Smurf, switch jamming 지시문 보강 |
| `2014-01-practical-03.md` | SYN flooding, ISMS, XSS, Teardrop 지시문 보강 |
| `2014-02-practical-04.md` | 웹 프록시 도구, IDS 오탐/미탐 지시문 보강 |
| `2015-01-practical-05.md` | journaling, CVE, 개인정보 안전성 확보조치, 업로드/SQL injection, CIA/BIA 지시문 보강 |
| `2015-02-practical-06.md` | 예방 통제·물리적 접근 통제·논리적 접근 통제 구분 보강 |
| `2016-01-practical-07.md` | dropper/injector, webshell, cyber kill chain, 내부관리계획 지시문 보강 |
| `2016-02-practical-08.md` | `/proc` 지시문 보강 |
| `2017-01-practical-09.md` | hosts 파일, Delphi method 지시문 보강 |
| `2017-02-practical-10.md` | DR 사이트 유형 문제의 A/B/C 설명을 사용자 제공 원천 이미지로 대조해 보강 |
| `2018-01-practical-11.md` | BitLocker, Slow HTTP Header, supply-chain attack 지시문 보강 |
| `2018-02-practical-12.md` | IPSec, CR/LF 기반 HTTP 응답 분할, DB 보안 위협, logrotate, 접속기록, 위험 산식, CC, DR 사이트, Linux/NTP 명령 지시문 보강 |
| `2019-01-practical-13.md` | IDS/IPS 탐지 방식, 웹 취약점 분석 방법, 위험분석 방법론, `.htaccess`, IDS/IPS 배치, IPSec, Snort, `robots.txt` 지시문 보강 |
| `2019-02-practical-14.md` | 접근통제, ARP, IPSec, DDE, 경보단계, Linux 로그, 법률명, ISMS-P, `/etc/shadow`, MAC, TCP ACK Scan, Apache, Snort 지시문 보강 |
| `2020-01-practical-15.md` | XSS, Suricata, 접속기록 보관, ISMS-P, VPN, ESP 터널모드, `/proc` 백도어, 백업 권한, Slow HTTP POST, 교통카드 개인정보 안내문 조건 보강 |
| `2020-02-practical-16.md` | CISO, 무선랜 암호, EDR, TLS 1.3, `strace`, TMS, 쿠키 보안, 포렌식 원칙, 메일 보안, XXE, 위험평가 조건 보강 |
| `2021-01-practical-17.md` | 법령 용어, ISO 27005, 접속기록 정의, 웹로그 원격명령실행, Snort, Apache 설정 지시문 보강 |
| `2021-02-practical-18.md` | WPA2, YARA, SW 취약점, DGA, 위험분석 절차, Prepared Statement, DRDoS, Tiny Fragment, 이메일 로그, Linux 보안, DNS 증폭 로그 지시문 보강 |
| `2022-01-practical-19.md` | 위험구성요소, NAC, Race Condition, ARP Spoofing, IDS 유형, BIA/RTO/RPO, Apache 로그·설정, PGP/PEM, 자산 중요도, 세션 하이재킹, 특수비트 권한, 개인정보처리방침, Promiscuous mode 로그, 자산목록, `.htaccess`, 위험평가서 지시문 보강 |
| `2022-02-practical-20.md` | HTTP OPTIONS, 위험분석 방법, 접근통제, IDS 오탐/미탐, Apache Indexes, 개인정보 수집 가능 사유, Snort FTP, Sendmail, 라우터, 위험대응 지시문 보강 |
| `2022-04-practical-21.md` | Sendmail, SNMP, 위험허용, BCP, 암호화 저장 점검, 위험분석 방법론, exploit code, IDS, DR, iptables, ALE, DNS zone 설정 조건 보강 |
| `2023-01-practical-22.md` | 라우팅 프로토콜, Unix 로그, `/etc/passwd`, HTTP Response Splitting, PHP 파일 삽입, Snort threshold, ARP, DNS, DBMS 질의문, 개인정보 접속기록, 위험관리, BYOD, Cookie 설정, DNS 증폭, SQL Injection 로그, 개인정보 안전성 확보조치 조건 보강 |
| `2023-04-practical-24.md` | PIPC/KISA 개인정보영향평가 위험도 산정 공식의 `(C)=2` 근거 확인, DB 암호화 방식 문장 잘림 보정, Apache 로그 경로 표기 보정, xinetd CIDR 표기 보정, rsh/rlogin/rexec 원격접속 파일 보안, iptables chain/rule, SNMP 보안설정, Unix 계열별 패스워드 길이 설정의 prompt/answer 분리 |
| `2024-01-practical-25.md` | 기밀성 등급, IDS 대응 행위, ARP 캐시 공격 판단 및 정적 ARP 조치의 prompt/answer 분리 |
| `2024-02-practical-26.md` | UAC, Promiscuous mode, XSS, DB 권한 최소화의 prompt/answer 분리 |
| `2024-04-practical-27.md` | SW 취약점 A/B/C 답안 정정, 정보보호 방침·실행계획, 미러사이트, NTP DDoS 대응의 prompt/answer 분리 |
| `2025-01-practical-28.md` | Smurf, SSRF, VLAN, HttpOnly, CR/LF, Cyber Kill Chain, `lsof`, `lastb`, 자산 중요도, 위험관리계획, ISMS-P 물리보호, Deep Link, Shell, NetBIOS, IPSec, 자산 중요도 기준, Oracle audit, Telnet/FTP 점검 결과 조건 보강 |
| `2025-02-practical-29.md` | Naver/Jaesung 복원 원천 기준으로 PAM, Certificate Pinning, 파일 업로드 취약점, 보안관제 구성요소, ISMS-P 위험처리, Windows 이벤트 로그 용량, CCTV 보호구역 조건 보강 |
| `2025-04-practical-30.md` | 사용자 제공 PDF와 Jaesung 복원 원천 기준으로 `/etc/shadow`, 디지털 포렌식, BYOD, 자산·위협·취약성 관계, EAM/IAM, Snort 룰, SQL Injection 조건 보강 |
| `2026-01-practical-31.md` | 사용자 제공 HTML 표 기준으로 18문항 생성, 4번 이미지 문항은 링크 이미지 다운로드 후 육안 확인으로 prompt 복원 |

## 2026-07-04 Restored Context
| file | restored item scope | source basis |
|---|---|---|
| `2015-01-practical-05.md` | 15번 디렉터리 리스팅 결과, 16번 DNS Zone Transfer 결과를 prompt에 반영 | Information Security Tistory text body |
| `2018-01-practical-11.md` | 14번 Blind SQL Injection URL 조건과 출력 결과를 prompt에 반영 | Information Security Tistory text body |
| `2019-01-practical-13.md` | 11번 `.htaccess`, 14번 Snort 룰, 15번 `robots.txt` 설정 조건을 prompt에 반영 | Information Security Tistory text body |
| `2023-02-practical-23.md` | 13번 PHP 업로드 코드·우회·성공조건, 16번 HTTP Request의 Referer/Cache-Control 헤더를 prompt에 반영 | it-utopia Tistory text body and Naver cross-check status |
| `2013-02-practical-02.md` | 12번 Snort GET Flooding 룰, 15번 IIS URL 기반 SQL Injection 로그 조건을 prompt에 반영 | Information Security Tistory text body |
| `2014-01-practical-03.md` | 12번 Cache-Control 패킷 조건, 14번 IPSec VPN/NAT/AH 상황, 15번 HTTP GET Flooding 상황을 prompt에 반영 | Information Security Tistory text body |
| `2014-02-practical-04.md` | 11번 VPN 프로토콜·IPSec 모드 조건, 14번 Snort PCRE 룰 조건을 prompt에 반영 | Information Security Tistory text body |
| `2015-02-practical-06.md` | 3번 DNS ANY 질의/ACL 조건, 16번 ARP 테이블 조건을 prompt에 반영 | Information Security Tistory text body |
| `2016-01-practical-07.md` | 2번 exploit 용어 조건, 15번 HTTP Request 패킷 조건을 prompt에 반영 | Information Security Tistory text body |
| `2017-01-practical-09.md` | 5번 tcpdump 단편화 행, 12번 xinetd 설정값, 13번 ndd 명령, 16번 SYN Flooding/iptables 조건을 prompt에 반영 | Information Security Tistory text body |
| `2017-02-practical-10.md` | 15번 ICMP Echo Request 브로드캐스트 공격 조건을 prompt에 반영 | Information Security Tistory text body |
| `2018-02-practical-12.md` | 13번 HTTP GET Flooding 탐지 Snort 룰 조건을 prompt에 반영 | Information Security Tistory text body |

## 2026-07-06 Strict Standalone Restored Context
| file | restored item scope | source basis |
|---|---|---|
| `2013-01-practical-01.md` | 3번 개인정보 내부관리계획 항목 목록, 4번 Solaris 로그 파일 설명, 6번 SIEM 기능 설명, 7번 IDS 유형 설명, 8번 Linux 로그 파일 설명, 10번 자산관리 절차 조건, 11번 권한 행, 15번 Cisco 명령 빈칸, 16번 ARP 테이블을 prompt에 반영 | Information Security Tistory text body |
| `2015-02-practical-06.md` | 2번 SNMPv3 보안 매개변수 표, 4번 라우팅 테이블과 목적지 IP, 5번 Unix 명령 목록, 6번 OS 목록, 7번 ISMS 순서, 8번 위험분석 용어 설명, 9번 내부관리계획 항목 목록, 14번 SQL 쿼리, 15번 Slow HTTP Header 패킷 조건을 prompt에 반영 | Information Security Tistory text body |
| `2013-02-practical-02.md` | 2번 위험분석 방법론 설명, 4번 정보보호 정책 요소 설명, 5번 Tripwire/Nessus 설명, 7번 CIA 설명, 10번 위험구성요소 설명을 prompt에 반영 | Information Security Tistory text body |
| `2014-01-practical-03.md` | 1번 Diffie-Hellman 공개값·비밀값·전송값, 2번 HeartBleed 조건, 4번 접근통제 정책 설명, 5번 Snort 룰, 8번 ISMS 관리절차 보기, 10번 위험대응 설명을 prompt에 반영 | Information Security Tistory text body |
| `2014-02-practical-04.md` | 1번 CVE 예시, 2번 OWASP 설명, 4~5번 위험분석·위험관리 설명, 8번 스캔 보기, 9번 Telnet 조건, 10번 C 코드, 15번 WPA 옵션 문항, 16번 위험계산 조건을 prompt에 반영 | Information Security Tistory text body |
| `2015-01-practical-05.md` | 3번 FTP SYN Flooding 현상, 4번 웹 로그, 7번 RFI 설정 조건, 8번 위험평가 설명, 11번 Drive-by-download 단계, 14번 악성코드 변경 목록을 prompt에 반영 | Information Security Tistory text body plus answer-block-derived change list |
| `2016-01-practical-07.md` | 1번 PE 섹션 설명, 3번 DNS 설정 설명, 4번 Snort 룰, 5번 Dropper/Injector 설명, 9번 통제 분류 설명, 12번 위험수치 문항, 14번 crontab 항목, 16번 Bash/ShellShock 문항을 prompt에 반영 | Information Security Tistory text body; 12/14/16 source body is image-only and reconstructed from answer block |
| `2016-02-practical-08.md` | 1번 MySQL 설정값, 2번 ISMS 대책 항목 목록, 3번 WEP 설명, 5번 정보보호 목표 순서, 6번 TCP 3-way 수치, 7번 setuid 함수 호출, 11번 IPSec 구성도, 15번 crontab 요구사항을 prompt에 반영 | Information Security Tistory text body; 6 source body is image-only and reconstructed from answer block |
| `2017-01-practical-09.md` | 2번 Smurf 과정, 3번 버퍼오버플로우 설명, 6번 법 조항 빈칸, 7번 SSL/TLS 순서, 9번 CC 설명, 14번 FTP Active Mode 문항을 prompt에 반영 | Information Security Tistory text body |
| `2017-02-practical-10.md` | 2번 FTP Active 모드 포트 조건, 4번 VLAN 목적, 6번 주요정보통신기반시설 지정 고려사항, 8번 개인정보 안전성 확보조치 정의, 10번 위험관리 설명, 11번 버퍼오버플로우 방어기법, 13번 iptables DROP/REJECT, 16번 Promiscuous Mode 문항을 prompt에 반영 | Information Security Tistory text body where available; image-only items reconstructed from answer block |
| `2018-01-practical-11.md` | 2번 DB 보안 접근통제 설명, 3번 VPN/IPSec 설명, 7번 SNMP 포트·보고 방식, 8번 정보통신망법 보관·점검 기준, 9번 위험분석 계산식, 11번 포트 스캔 패킷 흐름, 13번 여행사 개인정보 약관, 15번 Snort 룰 조건을 prompt에 반영 | Information Security Tistory image assets downloaded; Tesseract OCR attempted; visual inspection used for final transcription |

## 2026-07-06 OCR/Visual Image Restored Context
| file | no | image content restored | OCR note |
|---|---:|---|---|
| `2018-01-practical-11.md` | 2 | DB 접근 통제, 추론 통제, 흐름 통제 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 3 | IPSec, AH, ESP 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 7 | SNMP UDP 161, Event Reporting, UDP 162 조건 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 8 | 5년, 월 1회, 6개월 보관·점검 기준 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 9 | `SLE = AV × (A)`, `ALE = SLE × (B)` 계산식 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 11 | TCP 25 SYN/SYN-ACK/RST, TCP 443 SYN/RST, TCP 110 SYN/no response scan flow | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 13 | 여행자 멤버십·이벤트 업체 제공, 탈퇴 시까지, 주민등록번호 포함 수집항목, 동의거부 문구 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-01-practical-11.md` | 15 | Telnet 23, alert, `Dangerous`, first 14 bytes, `anonymous` condition | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 2 | IPSec 계층, AH 51, ESP 50 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 3 | CR/LF 기반 HTTP 응답 분할 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 4 | 집성, 추론, 데이터 디들링 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 5 | logrotate `weekly`, `size 1M`, `create`, `compress` 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 7 | 접속기록 정의의 개인정보처리시스템, 수행업무, 전자적 기록 조건 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 8 | `위험 = 자산 × 위협 × 취약성 - 정보보호 대책` 산식 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 9 | EAL, PP, ST 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 10 | Mirror, Cold, Hot, Warm site 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 14 | `last`, `lsattr`, `chattr -i` 명령 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2018-02-practical-12.md` | 15 | `ntp -version`, `disable monlist`, `ntpdc -c monlist`, `iptables` 명령 조건 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 3 | IDS/IPS pattern/misuse, anomaly, false positive 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 6 | Black-box, white-box 웹 취약점 분석 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 7 | 확률 분포법, 델파이법 설명 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 11 | `.htaccess` `FilesMatch` 및 `AddType` 설정 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 12 | IPS inline, IDS mirroring 배치 사유 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 13 | AH/ESP 모드별 인증·암호화 구간 및 IKE 물음 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 14 | Heartbleed 탐지 Snort 룰 조건 | local `tesseract -l kor+eng` attempted; visual transcription used |
| `2019-01-practical-13.md` | 15 | `robots.txt` user-agent, allow, disallow 설정 | local `tesseract -l kor+eng` attempted; visual transcription used |

## 2026-07-06 Naver Reconstruction Restored Context
Naver PostView HTML 본문에서 텍스트를 추출해 14~20회차의 주제명-only prompt를 독립 풀이 가능한 조건형 prompt로 보강했다. 단, Naver 원천은 공식 시험지가 아니라 분석/복원 글이며 18회차와 20회차 글에는 실제 문제와 100% 동일하지 않을 수 있다는 취지의 주석이 있어 공식 원문 일치 보증 근거로 사용하지 않는다.

| file | restored item scope | source basis |
|---|---|---|
| `2019-02-practical-14.md` | 1~16번 접근통제, ARP, IPSec, DDE, 경보단계, 로그, 법률, ISMS-P, 계정/Shadow, MAC, TCP ACK Scan, Apache, Snort 조건 보강 | Naver PostView text extraction |
| `2020-01-practical-15.md` | 1, 5, 6, 8, 10~16번 XSS, Suricata, 접속기록, ISMS-P, VPN, ESP, `/proc`, 비밀번호, 백업 권한, Slow HTTP POST, 교통카드 개인정보 조건 보강 | Naver PostView text extraction |
| `2020-02-practical-16.md` | 2~15번 CISO, 정책, 무선랜, EDR, TLS 1.3, `strace`, TMS, 위험모델, 쿠키, 포렌식, 메일 보안, XML/XXE, 위험평가 조건 보강 | Naver PostView text extraction |
| `2021-01-practical-17.md` | 2~10, 14~16번 DNS, MITRE ATT&CK, Credential Stuffing, CVSS, 침해사고 대응, 법령 용어, ISO 27005, 웹로그, Snort, Apache 설정 조건 보강 | Naver PostView text extraction |
| `2021-02-practical-18.md` | 1~16번 WPA2, YARA, SW 취약점, 위험관리, DGA, Prepared Statement, DRDoS, Tiny Fragment, 이메일 로그, Linux 보안, DNS 증폭 조건 보강 | Naver PostView text extraction |
| `2022-01-practical-19.md` | 11~16번 특수비트, 개인정보처리방침, Promiscuous 로그, 구성도/자산목록, `.htaccess`, 위험평가서 조건 보강 | Naver PostView text extraction plus nhustler source listing |
| `2022-02-practical-20.md` | 1~5, 7~8, 11~16번 HTTP Method, 위험분석, 접근통제, IDS, Apache, Snort, Sendmail, router, 위험대응 조건 보강 | Naver PostView text extraction plus nhustler source listing |

## 2026-07-06 21~30 Cross-Verification
21~30회차는 Naver PostView 텍스트, direct web reconstruction, Jaesung restoration, 로컬 출제기준/학습 노트를 함께 대조했다. 이전 검증 기록에는 사용자 제공 30회 PDF 텍스트 추출 대조가 남아 있으나, 이번 세션에서는 해당 파일을 재확인하지 못했다. 이 범위의 Naver 글에는 본문 문항이 HTML 텍스트로 노출되어 있었고, 첨부 이미지는 대표/스톡 이미지로 확인되어 OCR 복원 대상 문제 이미지가 없었다. Jaesung 28~30회 이미지는 제목 배너 계열이며 본문 문항은 HTML 텍스트였다.

| file | reviewed source basis | action |
|---|---|---|
| `2022-04-practical-21.md` | Naver `stereok2/222985383781`, nhustler listing | 1~16번 중 기존 요약형·오답수렴 항목을 빈칸·명령·조건형 prompt로 보강 |
| `2023-01-practical-22.md` | Naver `stereok2/223148136930`, nhustler listing | 1~12번 단답형의 실제 설명·빈칸 조건 보강, PHP/DBMS 항목 답안 정정 |
| `2023-02-practical-23.md` | direct web reconstruction, Naver `stereok2/223202583456` | 기존 18문항 구조가 Naver 주제·답안 흐름과 일치함을 재확인 |
| `2023-04-practical-24.md` | direct web reconstruction, Naver `stereok2/223403908181` | 14~17번에서 prompt에 섞인 답안 조각을 answer로 분리 |
| `2024-01-practical-25.md` | direct web reconstruction, Naver `stereok2/223481498564` | 15~17번에서 prompt/answer 분리 및 ARP 판단 조건 정규화 |
| `2024-02-practical-26.md` | direct web reconstruction, Naver `stereok2/223603394618` | 13, 15~17번에서 UAC·promiscuous·XSS·DB 권한 문항 구조 정규화 |
| `2024-04-practical-27.md` | direct web reconstruction, Naver `stereok2/223762794914` | 7번 A/B/C 답안 정합성 수정, 14·16·18번 prompt/answer 분리 |
| `2025-01-practical-28.md` | Naver `stereok2/224130288134`, Jaesung 90, local criteria/notes | 18문항 독립 풀이 가능 상태 확인; Jaesung은 AI 복원 보조 원천으로만 사용 |
| `2025-02-practical-29.md` | Naver `stereok2/224308597646`, Jaesung 91, local criteria/notes | 18문항 독립 풀이 가능 상태 확인; 법령/CCTV 항목은 현행 법령 재확인 필요 |
| `2025-04-practical-30.md` | user-provided 30회 PDF, Jaesung 92, local criteria/notes | 18문항 독립 풀이 가능 상태 확인; 사용자 제공 PDF로 답안 상세 보강 |

## 2026-07-06 PDF Compilation Cross-Check
사용자 제공 비밀번호로 `/Users/ian/study/information-security/기출/`의 1~28회 단답형·서술형 문제/문제+답 PDF 4개를 해제하고 `pdftotext -raw` 추출을 수행했다. PDF 표기 출처는 13~28회 온계절님 블로그, 1~12회 Information Security Tistory, 제작 thodi-lab이므로 공식 KCA 원문이 아니라 편집본 교차검증 원천이다.

| range | PDF result | decision |
|---|---|---|
| 1~13 | many topics found but automatic text match is weak because local prompts are reconstructed/paraphrased and PDF is a sequential problem-bank compilation | keep source limits; use manual screen-level PDF check for high-impact items |
| 14~27 | automatic and manual checks generally align with local Naver/direct reconstruction rows | use PDF compilation as additional cross-check evidence |
| 28 | automatic scores are weak, but PDF end section manually confirms Smurf, SSRF, VLAN, HttpOnly, CR/LF, Cyber Kill Chain, `lsof`, `lastb`, asset importance, risk-management plan, physical controls, deep link, Shell, NetBIOS, IPSec, Oracle audit, Telnet/FTP items | keep 28회 item count and answer-topic confidence |
| 29~30 | outside provided PDF range | keep previous Naver/Jaesung source boundary |

## 2026-07-06 21~30 OCR Finding
21~30회차 검증 중 이미지 OCR이 필요한 문제 본문 이미지는 발견하지 못했다. Naver `aPostImageFileSizeInfo`에는 각 글의 대표/스톡 이미지가 1~2개 등록되어 있었고, 문제 본문은 HTML 텍스트에서 추출되었다. Jaesung 28~30회 글의 상단 이미지는 "정보보안기사 실기 문제 복원"류 제목 배너로 확인했으며, 본문 문항은 HTML 텍스트였다.

| range | image status | OCR decision |
|---|---|---|
| 21~27 | Naver representative/stock images; direct reconstruction text available where used | OCR not applicable for problem reconstruction |
| 28~29 | Naver representative images plus Jaesung title banner; problem body in HTML text | OCR not applicable for problem reconstruction |
| 30 | Jaesung title banner; problem body in HTML text | OCR not applicable; source reliability tracked as AI reconstruction limit |

## 2026-07-07 31 Source Update and 32 Source Sweep
31회차는 사용자 제공 문제·정답 HTML 표와 4번 이미지 문항을 기준으로 `2026-01-practical-31.md`를 생성했다. 32회차는 실제 기출 복원 문항 파일을 만들지 않는다. 현재 확인 가능한 공개 원천은 시험 복원글이 아니라 대비 요약, 후기, 예상문제, 다른 자격 종목 글로 분류되며, 문제 본문 이미지 OCR 대상도 확인되지 않았다.

| target | local status | external sweep result | OCR decision | decision |
|---|---|---|---|---|
| 31회 / 2026년 1회 | `2026-01-practical-31.md` created | user-provided 문제·정답 HTML table supplied on 2026-07-07 | item 4 linked image downloaded and visually inspected | include in past-exam dataset with user-provided source boundary |
| 32회 / 2026년 2회 추정 | no `*-practical-32.md` file | Jaesung `/99` is titled as a 32회 AI expected-question post, not a past-exam restoration; Naver search results did not expose a verified 기사 실기 32회 복원글 | no verified problem image source found | exclude from past-exam dataset; keep only as future prediction material if used elsewhere |

Checked source classes: local `datasets/info-sec-engineer-practical-past-exams/*practical*.md`, Jaesung Tistory category and posts `/93`, `/94`, `/95`, `/99`, stereok2 Naver blog main/search pages, Naver search result pages for 31회, 32회, 2026년 1회, 2026년 2회, 26년 1회, 26년 2회, and the user-provided 31회 HTML table.

## 2026-07-06 Image-Only Source Limits
아래 항목은 현재 접근 가능한 HTML 본문에는 이미지 링크만 있고 텍스트 원문이 없다. 답안 블록과 회차 문맥으로 독립 풀이 가능한 prompt는 복구했지만, 이미지 안의 정확한 원문 문구·도식과 1:1 일치한다고 주장하지 않는다.

| file | no | restored basis |
|---|---:|---|
| `2016-01-practical-07.md` | 12 | answer block identifies SLE, SLE formula, ARO, ROI prompt slots |
| `2016-01-practical-07.md` | 14 | answer block identifies two crontab behaviors |
| `2016-01-practical-07.md` | 16 | answer block identifies ShellShock cause and reverse-shell concept |
| `2016-02-practical-08.md` | 6 | answer block identifies TCP sequence/ack numbers |
| `2017-02-practical-10.md` | 2 | answer block identifies FTP Active mode and port blanks |
| `2017-02-practical-10.md` | 4 | answer block identifies VLAN objective blanks |
| `2017-02-practical-10.md` | 6 | answer block identifies infrastructure designation blanks |
| `2017-02-practical-10.md` | 10 | answer block identifies risk-management blanks |
| `2017-02-practical-10.md` | 11 | answer block identifies canary and ASLR subquestions |
| `2017-02-practical-10.md` | 13 | answer block identifies DROP/REJECT subquestions |
| `2017-02-practical-10.md` | 16 | answer block identifies Promiscuous Mode subquestions |

## 2026-07-06 Strict Meta-Prompt Sweep
1~31회차 전체 회차 파일을 대상으로 "문항 주제만 있고 판단 자료가 없는 prompt"를 다시 검색했다. 이 sweep은 정답 키워드가 맞는지보다, 학습자가 `reconstructed prompt`만 읽고 문제를 풀 수 있는지를 우선 기준으로 삼았다.

| check | result | interpretation |
|---|---:|---|
| generic/meta prompt pattern scan | 0 remaining matches | `문항.`, `묻는 문항`, `쓰는 문항`, `계산·서술하는 문항`, 단독 `설명.`, 단독 `기술.`류의 placeholder prompt가 남아 있지 않다. |
| low-detail reconstructed prompt scan | 0 remaining candidates | 짧은 요약형 prompt 중 답안 근거 없이 주제명만 남은 항목을 찾지 못했다. |
| password literal scan | 0 remaining matches | PDF 해제용 비밀번호 문자열을 dataset 문서에 저장하지 않았다. |
| latest manual correction sweep | completed | `2020-02` 16번, `2021-01` 12~13번, `2022-01` 1~10번, `2023-01` 4번·11~18번, `2025-01` 1~18번, `2025-02` 1번·13~18번, `2025-04` 1번·6번·13~16번·18번을 추가 보강했다. |

The strict sweep result means current local files have no additional detectable standalone-blocking prompt gaps under the available reconstruction sources. The 2026-07-17 PDF supplement resolved R06-Q01, and the user-provided photo supplement resolved the TCP table of R10-Q14 plus the decisive wording of R30-Q08 and R30-Q15. It does not mean KCA official wording, punctuation, table layout, or image layout has been fully recovered.

## Strict Completeness Gate
회차 파일의 `reconstructed prompt`는 답안 주제 요약이 아니라 독립 풀이 가능한 문제 조건이어야 한다. 따라서 아래 요소가 원천에 있으면 prompt에 보존한다.

| source element | required prompt representation |
|---|---|
| 표 | 열·행의 판단값 또는 동등한 key-value 목록 |
| 그림 | 풀이에 필요한 노드, 흐름, 주소, 권한, 상태값의 텍스트 재구성 |
| 로그·패킷 | 공격 판단에 필요한 IP, 포트, 헤더, 페이로드, 상태값 |
| 명령·설정 | 빈칸 주변 명령, 옵션, 설정 키, 출력값 |
| 법/관리 항목 목록 | 답안이 수렴되는 항목명과 조건 목록 |

## Remaining Tracked Limit
21~31회차에는 strict scan 기준 standalone-blocking prompt 누락을 남기지 않았다. 전체 1~31회차의 남은 한계에는 KCA 공식 원문 미검증, Naver/PDF 편집본과 사용자 제공 사진의 비공식성, 31회차의 사용자 제공 HTML 표 원천 경계, 32회차의 verified reconstruction source 부재가 포함된다.

## False Positives
| file | no | reason |
|---|---:|---|
| `2024-01-practical-25.md` | 12 | SOAR 설명 bullet이 이미 포함되어 있어 설명 누락 아님 |
| `2024-04-practical-27.md` | 5 | `utmp`, `wtmp`, `lastlog`별 로그 설명이 이미 포함되어 있어 설명 누락 아님 |

## Method
- Parsed all same-directory `*-practical-*.md` reconstruction tables.
- Flagged vague prompt patterns such as `다음에서 설명하는`, `다음 설명`, `다음 빈칸`, `빈칸`, `보기`, `(A)` when no usable condition text was present.
- Reclassified prompts that contain `다음 ... 물음에 답하시오`, `다음 ... 결과`, `다음 ... 로그`, `다음 ... 룰`, `다음 ... 설정` as context-dependent when the actual log/rule/config/result body is absent.
- Cross-checked accessible web reconstruction sources where available.
- Cross-checked unlocked 1~28회 thodi-lab/blog-source PDF compilation where available.
- Searched 31~32회 candidate sources separately; 31회 was later supplied by the user as a problem-answer HTML table, while 32회 expected-question/prep-summary pages remain rejected as past-exam evidence.
- Cross-checked user-provided source images for `2017-02-practical-10.md` #7 and `2018-02-practical-12.md` #3.
- Preserved source limits rather than inventing official wording when reconstruction sources lacked the original description body.
