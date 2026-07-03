---
title: "정보보안기사 실기 2026년 2회 예상문제"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, predicted-questions]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "frequency-analysis.md"
  - "recurrence-analysis.md"
  - "pattern-analysis.md"
  - "significance-review.md"
  - "session-slot-pattern-analysis.md"
  - "study-strategy-2026-02.md"
  - "item-reference-map.md"
source_count: 7
provenance: inferred
summary: "기출 빈도·최근성·출제기준 연결·회차 슬롯 경향을 근거로 작성한 정보보안기사 실기 2026년 2회 예상문제와 채점 키워드."
evergreen: false
---

# 정보보안기사 실기 2026년 2회 예상문제

## Scope
- 본 문서는 실제 출제를 보장하지 않는다.
- 예상 근거는 1~30회 복원본의 반복 개념, 최근 23~30회 출제기준 연결, 2회 슬롯 보조 가중치다.
- 공식 PDF 원문 미대조 상태이므로 예상문제는 공식 문구 재현이 아니라 개념·유형 기반 학습 문제다.

## Short Answer
| no | predicted question | answer key | basis | confidence |
|---:|---|---|---|---|
| 1 | 위험분석에서 자산, 위협, 취약점의 관계를 설명하고 위험을 산정할 때 고려하는 요소를 쓰시오. | 자산 가치, 위협 가능성, 취약점, 영향도, 위험도 | 위험관리/위험평가 79건 | high |
| 2 | 위험 대응 전략 4가지를 쓰고 각각의 의미를 간략히 설명하시오. | 수용, 감소, 회피, 전가 | 전 회차 반복 | high |
| 3 | 기준선 접근법, 상세 위험분석, 복합 접근법의 차이를 쓰시오. | 기본 보호대책 일괄 적용 / 자산별 상세 분석 / 고위험은 상세, 나머지는 기준선 | 위험평가 반복 | high |
| 4 | DAC, MAC, RBAC의 접근통제 기준을 각각 쓰시오. | 사용자 재량 / 보안등급·정책 강제 / 역할 기반 | 접근통제 반복 | high |
| 5 | PAM 모듈 중 `auth`, `account`, `session`의 역할을 쓰시오. | 인증 / 계정 권한·상태 확인 / 세션 설정·관리 | 최근 시스템 보안 | high |
| 6 | Linux 로그인 실패 기록 파일과 이를 확인하는 명령을 쓰시오. | `btmp`, `lastb` | 리눅스 로그·명령 최근성 | high |
| 7 | Linux에서 열린 파일과 해당 파일을 사용하는 프로세스를 확인하는 명령을 쓰시오. | `lsof` | 최근 28회 출제 | high |
| 8 | `/etc/shadow` 파일에서 `$1$`, `$5$`, `$6$`이 의미하는 해시 알고리즘을 쓰시오. | MD5, SHA-256, SHA-512 | OS 계정 파일 반복 | high |
| 9 | setuid, setgid, sticky bit의 의미를 쓰시오. | 소유자 권한 실행, 그룹 권한 실행, 공용 디렉터리 삭제 제한 | Unix 권한 반복 | high |
| 10 | SQL Injection 방어를 위해 PreparedStatement가 효과적인 이유를 설명하시오. | SQL 구조와 파라미터를 분리하고 바인딩해 입력값이 쿼리 구조를 바꾸지 못함 | 시큐어코딩 반복 | high |
| 11 | HTTP Response Splitting에 사용되는 개행 문자 2가지를 쓰시오. | CR `%0D`, LF `%0A` | CRLF 보강 문항 | high |
| 12 | SSRF 취약점의 원리와 주요 대응 방안을 쓰시오. | 서버가 사용자 입력 URL로 내부망 요청 수행; allowlist, 내부 IP 차단, URL 검증 | 최근 웹 취약점 | high |
| 13 | IPSec의 AH와 ESP가 제공하는 보안 기능 차이를 쓰시오. | AH: 인증·무결성, ESP: 기밀성·인증·무결성 | IPSec 반복 | high |
| 14 | SNMP 보안 설정 3가지를 쓰시오. | community string 변경, SNMPv3 사용, ACL 제한, RO 권한 사용 | SNMP 반복 | high |
| 15 | NTP monlist 악용 DDoS 대응 방안 2가지를 쓰시오. | 4.2.8 이상 업그레이드, `disable monitor`, ACL/방화벽/속도제한 | 최근 서비스 설정 | high |
| 16 | 개인정보처리시스템 접근권한 관리 기준 3가지를 쓰시오. | 권한 부여·변경·말소, 내역 보관, 계정 공유 금지, 최소권한 | 개인정보/ISMS-P 반복 | high |
| 17 | HIDS와 NIDS의 차이를 쓰시오. | 호스트 로그·파일·프로세스 감시 / 네트워크 패킷·트래픽 감시 | IDS/IPS 반복 | high |
| 18 | DLP가 보호하는 데이터 상태 3가지를 쓰시오. | data in use, data in motion, data at rest | 최근 DLP 출제 | medium-high |

## Essay / Practical
| no | predicted question | scoring points | basis | confidence |
|---:|---|---|---|---|
| 19 | Apache에서 디렉터리 리스팅이 가능한 설정을 확인했다. 위험과 대응 설정을 설명하시오. | `Options Indexes` 위험, 파일 목록 노출, `-Indexes` 또는 제거, 접근통제 | 서비스 보안설정 최다 | high |
| 20 | DNS master/slave zone 설정에서 zone transfer를 제한해야 하는 이유와 설정 방향을 설명하시오. | zone 정보 유출, `allow-transfer`, slave IP 제한, 외부 AXFR 차단 | DNS 반복 | high |
| 21 | Snort 룰에서 `msg`, `content`, `nocase`, `threshold` 또는 `detection_filter`의 의미를 설명하시오. | 경고 메시지, 페이로드 탐지 문자열, 대소문자 무시, 임계 탐지 | Snort 반복 | medium-high |
| 22 | ARP Spoofing 공격의 원리, 영향, 대응 방안을 설명하시오. | 위조 ARP reply, MAC cache 변조, MITM/sniffing, 정적 ARP, ARP inspection, 암호화 | 네트워크 공격 반복 | high |
| 23 | XSS 공격의 원리와 대응 방안을 Stored/Reflected/DOM 관점에서 설명하시오. | 스크립트 삽입, 쿠키 탈취, 입력검증, 출력 인코딩, CSP, HttpOnly | 웹 취약점 반복 | high |
| 24 | 파일 업로드 취약점으로 웹셸이 실행되는 조건과 대응 방안을 설명하시오. | 확장자/MIME 검증 우회, 실행 경로 저장, 실행권한 제거, 난수 파일명, 웹루트 외부 저장 | 파일 업로드 반복 | high |
| 25 | DR 사이트 유형 4가지와 RTO 관점의 차이를 설명하시오. | mirror, hot, warm, cold; 자원 동기화 수준과 복구시간 차이 | BCP/DR 반복 | medium-high |
| 26 | 개인정보 접속기록 관리에서 기록해야 할 항목과 보관·점검의 목적을 설명하시오. | 접속자, 일시, 처리 내역, 접속지, 월 1회 점검, 이상행위 탐지, 보관 | 개인정보 안전성 확보조치 | high |
| 27 | Linux 계정 보안을 점검할 때 `/etc/passwd`, `/etc/shadow`, `login.defs`에서 확인할 항목을 설명하시오. | 권한, 해시 저장, 잠금/만료/최소길이, root 소유, 패스워드 정책 | 2회 슬롯 시스템 가중 | high |
| 28 | VLAN의 보안 목적과 포트 기반/MAC 기반/프로토콜 기반 VLAN의 차이를 설명하시오. | 논리 분리, broadcast domain 축소, 포트 할당, MAC 등록, 프로토콜별 분리 | VLAN 반복 | high |
| 29 | APT 공격을 단계적으로 분석하는 체계를 쓰고, 탐지/대응 관점에서 설명하시오. | Cyber Kill Chain 또는 ATT&CK, 정찰·침투·명령제어·목표달성, 로그/EDR/관제 대응 | Kill Chain medium 주의 | medium |
| 30 | DB 감사 설정과 감사 로그 외부 저장이 필요한 이유를 설명하시오. | audit 설정, 권한 오남용 추적, 무결성, 관리자 변조 방지, 외부 전송/보관 | DB/감사 최근성 | medium-high |

## Practical Scenario
| no | scenario | scoring points | basis | confidence |
|---:|---|---|---|---|
| 31 | 웹 로그에 `GET /search?q=' or '1'='1` 형태가 보인다. 공격명, 판단근거, 대응 방안을 쓰시오. | SQL Injection, 항상 참 조건, PreparedStatement, 입력검증, 오류 메시지 제한, WAF | SQL Injection 반복 | high |
| 32 | 서버가 큰 `Content-Length` 요청을 오래 유지하며 1바이트씩 전송받고 있다. 공격명과 대응을 쓰시오. | Slow HTTP POST/RUDY, 연결 점유, timeout, body size 제한, 동시연결 제한 | Slow HTTP 반복 | high |
| 33 | DNS 응답 트래픽이 피해자에게 대량 유입된다. 공격 원리와 네트워크 대응을 쓰시오. | DNS Amplification DRDoS, 출발지 위조, 공개 DNS, recursion 제한, BCP38/uRPF, rate limit | DRDoS 반복 | high |
| 34 | `xinetd` 설정에서 특정 대역만 허용하고 동시접속 수와 접속시간을 제한해야 한다. 사용할 설정 항목을 쓰시오. | `only_from`, `no_access`, `instances`, `access_time` | xinetd 최근 실무 | high |
| 35 | Oracle DB 감사 로그가 DB 내부에만 저장된다. 문제점과 개선 방안을 쓰시오. | 관리자 변조 가능성, 무결성 저하, 외부 로그 서버, 접근통제, 정기 점검 | DB 감사 최근성 | medium-high |
| 36 | 모바일 앱에서 특정 화면으로 바로 이동하는 링크가 인증 없이 민감 기능을 호출한다. 관련 기술과 대응을 쓰시오. | deep link, 인증/인가 검증, URL scheme 검증, 민감 기능 재인증 | 모바일 최근 확장 | medium |

## Must-Memorize Answer Keys
| topic | keys |
|---|---|
| 위험대응 | 수용, 감소, 회피, 전가 |
| 접근통제 | DAC, MAC, RBAC |
| PAM | auth, account, password, session |
| Linux logs | utmp, wtmp, btmp, lastlog, xferlog |
| Linux commands | lastb, lsof, lastcomm, find, chmod, iptables |
| IPSec | AH, ESP, IKE, transport mode, tunnel mode |
| Web secure coding | input validation, output encoding, PreparedStatement, upload validation |
| HTTP | CR, LF, OPTIONS, Cookie Secure/HttpOnly, Cache-Control |
| IDS/IPS | HIDS, NIDS, false positive, false negative, Snort rule |
| DR | mirror, hot, warm, cold, RTO, RPO |
