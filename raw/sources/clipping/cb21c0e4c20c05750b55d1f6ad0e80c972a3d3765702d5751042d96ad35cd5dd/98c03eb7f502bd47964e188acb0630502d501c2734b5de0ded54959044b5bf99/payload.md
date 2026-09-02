---
title: "정보보안기사 실기 기출 패턴 기반 통합 학습·실습 로드맵"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, study-roadmap, hands-on-lab, exam-pattern]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "../index.md"
  - "../05-analysis/frequency-analysis.md"
  - "../05-analysis/recurrence-analysis.md"
  - "../05-analysis/pattern-analysis.md"
  - "learning-priority-and-prediction-validity-2026-02.md"
  - "../04-mapping/item-reference-map.md"
  - "../02-references/reference-source-index.md"
  - "../02-references/exam-criteria-and-reference-catalog.md"
  - "study-strategy-2026-02.md"
  - "integrated-study-guide-2026-02.md"
  - "hands-on-lab-feasibility-deep-research.md"
  - "<local-user-home>/study/information-security/AI 요약.pdf"
  - "<local-user-home>/study/information-security/정보보안기사+핵심전략+1.3.pdf-20260622004728.pdf"
source_count: 13
provenance: inferred
summary: "정보보안기사 실기 1~31회 기출 패턴, 최근성, KCA 출제기준, 공식·준공식 레퍼런스, 현재 학습 PDF를 교차해 논리적 학습 순서와 독립 재사용 가능한 테스트베드 구성을 함께 제시한 실행 로드맵."
evergreen: false
---

# 정보보안기사 실기 기출 패턴 기반 통합 학습·실습 로드맵

## 결론
과하지 않다. 지금 필요한 것은 단순 실습환경이 아니라 `기출 패턴 -> 출제기준/레퍼런스 -> 논리적 학습 묶음 -> 안전한 실습 -> 답안 작성`으로 이어지는 학습 체계다.

현재 데이터 기준으로는 특정 문제가 그대로 나올 것을 기대하면 안 된다. 대신 같은 개념이 `단답형`, `설정값`, `로그 해석`, `공격 판단근거`, `대응방안`, `법규 적용 상황`으로 바뀌어 나오는 패턴을 학습해야 한다.

이 문서의 원칙은 다음이다.

1. 기출 문항은 문구 암기가 아니라 개념·패턴·답안 키워드로 학습한다.
2. PDF는 1차 기준이 아니라 보조 교재로 사용한다.
3. 공식 출제기준과 패칭된 레퍼런스가 우선이다.
4. 실습은 로컬·사설망·일회용 환경에서만 수행한다.
5. 외부 시스템, 호스트 OS 설정, 개인 작업환경, 기존 코드에는 영향을 주지 않는다.

## 근거 계층
| 우선순위 | 근거 | 사용 방식 |
|---:|---|---|
| 1 | `REF-KCA-INFOSEC-PRACTICAL-CRITERIA` | 출제 범위의 최상위 기준. 모든 학습 묶음은 이 기준 안에 있어야 한다. |
| 2 | 1~31회 회차별 복원 문서와 빈도·패턴 분석 | 실제 반복된 개념과 최근성 판단에 사용한다. 공식 원문 문구로 단정하지 않는다. |
| 3 | `item-reference-map.md`, `reference-source-index.md` | 최근 23~30회 문항을 KCA 기준과 보조 레퍼런스에 연결한다. |
| 4 | 패칭된 공공·공식 문서 | 개인정보, ISMS-P, KISA 취약점 가이드, 시큐어코딩 등 직접 근거가 있는 항목을 확인한다. |
| 5 | `AI 요약.pdf`, `정보보안기사+핵심전략+1.3.pdf` | 개념 이해, 빠른 복습, 답안 작성 방식 참고용이다. 충돌 시 로컬 기출 분석과 공식 레퍼런스를 우선한다. |

## 학습 순서
학습은 과목 순서가 아니라 사고 흐름 순서로 진행한다.

| 단계 | 묶음 | 이유 |
|---:|---|---|
| 0 | 답안 템플릿과 공통 배경 | 실기 답안은 키워드만 아는 것보다 구조화가 중요하다. |
| 1 | 위험관리·접근통제·법규 기초 | 관리/법규는 전체 최다이고 다른 과목의 판단근거가 된다. |
| 2 | Linux/Unix·Windows 계정·로그·권한 | 최근 시스템 보안 비중이 높고 단답 점수화가 쉽다. |
| 3 | 서비스 보안설정 | 최근 KCA 세부항목 최다 축이다. Apache, DNS, SNMP, NTP, SMTP, DB를 같이 묶는다. |
| 4 | 네트워크 프로토콜·장비·공격 | DNS/SNMP/VLAN/IPSec/ARP/ICMP/iptables/ACL은 함께 변형된다. |
| 5 | 웹 취약점·시큐어코딩 | XSS, CSRF, SQLi, SSRF, 파일 업로드, CRLF는 판단근거와 대응까지 써야 한다. |
| 6 | 관제·Snort·로그·침해사고 | Snort 룰, HIDS/NIDS, SIEM, 포렌식, PCAP 해석을 묶어 훈련한다. |
| 7 | 암호통신·DB·모바일·DR 보강 | IPSec/TLS/DB/MDM/BCP는 고득점 분기와 최근 변형 대비용이다. |

## 답안 템플릿
모든 단원은 아래 3단 구조로 답안을 만든다.

`무엇인가 -> 왜 문제인가/왜 필요한가 -> 어떻게 설정·탐지·대응하는가`

| 문제 유형 | 답안 구조 |
|---|---|
| 개념형 | 정의 -> 목적 -> 구성요소/예시 |
| 공격형 | 공격명 -> 판단근거 -> 대응방안 |
| 설정형 | 설정값/파일 -> 보안 의미 -> 권장 조치 |
| 로그형 | 로그 필드/증거 -> 의심 행위 -> 확인·차단·보존 |
| 법규형 | 적용 주체 -> 의무/요건 -> 기록·보관·통지·점검 |
| 비교형 | 비교 대상 -> 차이 기준 -> 적용 상황 |

## PDF 사용 규칙
| 자료 | 현재 역할 | 사용법 | 주의 |
|---|---|---|---|
| `AI 요약.pdf` | 개념 이해용 1차 읽기 자료 | 새 단원을 시작할 때 전체 구조를 잡는다. 표와 명령어는 암기표로 옮긴다. | 요약본 특성상 과포함·단순화 가능성이 있다. 기출 빈도와 레퍼런스로 걸러야 한다. |
| `정보보안기사+핵심전략+1.3.pdf` | 킬러토픽과 답안 전략 | 중요도 판단, 서술형 표현, 최근 5년 기출 관점을 참고한다. | 저자 전략서이므로 공식 출제기준 자체가 아니다. |
| Part.1~5 문제풀이 PDF | 문제 적용 훈련 | 해당 묶음 학습 후 같은 축의 문제만 골라 푼다. | 과목 순서대로 처음부터 읽으면 반복 개념 연결이 약해진다. |
| 1~28회 기출 PDF | 회차 교차검증 | 오답이 생겼을 때 회차 파일과 함께 확인한다. | thodi-lab/blog-source 편집본이며 KCA 공식 원문 보장은 아니다. |

PDF는 `읽기 -> 기출 매핑 확인 -> 레퍼런스 확인 -> 답안 작성 -> 실습 관찰` 순서로만 사용한다. PDF를 먼저 완독하고 외우는 방식은 우선순위가 흐려진다.

## 학습 묶음 0. 공통 배경과 답안 작성
### 학습 내용
- CIA: 기밀성, 무결성, 가용성
- 식별, 인증, 인가, 감사
- OSI/TCP/IP, 포트, TCP flag, UDP/ICMP
- HTTP request/response, method, header, cookie
- 로그의 의미: 주체, 시간, 행위, 결과, 출처
- 보안 설정 답안의 공통 구조: 제한, 비활성화, 최소권한, 로그, 최신화

### 변형 패턴
| 기출 형태 | 변형 가능성 |
|---|---|
| CIA 단답 | 위험평가, 자산 중요도, 개인정보 안전성 원칙으로 확장 |
| 인증/인가 단답 | PAM, 접근통제 모델, 개인정보 접근권한 관리로 확장 |
| TCP flag 단답 | SYN scan, half-open, iptables, Snort 룰로 확장 |
| HTTP header 단답 | CRLF, Cache-Control, Cookie flag, URL Rewrite로 확장 |

### 실습
실습보다 답안 템플릿 훈련이 우선이다. 모든 단원에서 3단 답안을 3문장 이하로 작성한다.

## 학습 묶음 1. 위험관리·접근통제·법규 기초
### 왜 먼저 하는가
위험관리/위험평가는 반복 개념군 최상위이고, 접근통제/권한관리는 시스템·개인정보·ISMS-P와 연결된다. 관리/법규는 전체 과목 비중도 가장 높다.

### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| 위험 구성 | 자산, 위협, 취약점, 가능성, 영향, 위험도 |
| 위험분석 | 정량, 정성, 기준선, 상세, 복합, 델파이 |
| 위험대응 | 수용, 감소, 회피, 전가 |
| 업무연속성 | BIA, BCP, DRP, RTO, RPO, hot/warm/cold/mirror site |
| 접근통제 | DAC, MAC, RBAC, BLP, Biba, 최소권한 |
| 인증·권한 | 식별, 인증, 인가, 감사, MFA, PAM |
| 개인정보 | 접근권한 관리, 접속기록, 암호화, 접근통제, 유출 대응 |
| ISMS-P | 관리체계 수립 및 운영, 보호대책 요구사항, 개인정보 처리 단계 |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 용어 단답 | 위험수용, 위험전가, BIA, RTO/RPO |
| 단계 빈칸 | 위험분석 -> 위험평가 -> 대책선정 |
| 상황 판단 | 자산 중요도와 우려사항을 보고 위험평가 |
| 법규 적용 | 개인정보 접근권한, 접속기록, CISO, IDC, 생체정보 보호 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 같은 출제범위 안에서 확장 가능한 내용 |
|---|---|
| 개인정보 안전성 확보조치 | 접근권한 부여·변경·말소, 접속기록 보관·점검, 암호화, 접속통제, 개인정보처리시스템 보호 |
| 개인정보보호법/CCTV | 영상정보처리기기, 처리 근거, 안내판, 보관·파기, 접근권한 |
| 정보통신망법 | CISO, 정보통신서비스 제공자, 집적정보통신시설(IDC), 보호조치 |
| ISMS-P | 정책 수립, 자산관리, 접근통제, 로그, 물리보안, 개인정보 생명주기 |

법령·고시 숫자와 조문은 바뀔 수 있다. 시험 직전에는 `reference-source-index.md`에 있는 공식 법령·고시 원천 또는 현행 공식 페이지로 다시 확인한다.

### 독립 실습
법규 자체는 실습보다 사례형 답안 훈련이 적합하다.

| 실습 | 방법 |
|---|---|
| 위험평가 표 작성 | 가상의 자산 5개를 만들고 CIA, 위협, 취약점, 가능성, 영향, 대응전략을 적는다. |
| 개인정보 처리 흐름 점검 | 수집, 저장, 이용, 제공, 파기 단계별로 필요한 보호조치를 표로 쓴다. |
| 접근권한 점검표 | 사용자, 역할, 권한, 승인자, 변경일, 말소일, 로그 점검 여부를 만든다. |

## 학습 묶음 2. Linux/Unix·Windows 계정·로그·권한
### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| 계정 파일 | `/etc/passwd`, `/etc/shadow`, `/etc/group`, `login.defs` |
| shadow 해시 | `$1$` MD5, `$5$` SHA-256, `$6$` SHA-512 |
| 로그 | `utmp`, `wtmp`, `btmp`, `lastlog`, `/var/log/messages` |
| 명령 | `last`, `lastb`, `lastlog`, `lastcomm`, `lsof`, `find`, `chmod`, `chattr`, `lsattr` |
| 권한 | SUID, SGID, sticky bit, umask, world-writable |
| 접근제어 | `/etc/securetty`, SSH root login, PAM, wheel group |
| Windows | SAM, SID, NTLM, IIS/DHCP 로그 경로, `net session`, `net share` |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 파일명 단답 | `/etc/shadow`, `btmp`, `lastlog`, `securetty` |
| 명령어 단답 | `lastb`, `lastcomm`, `lsof`, `find -perm` |
| 권한 해석 | SUID/SGID/sticky bit 의미와 위험 |
| 설정 보완 | root 직접 로그인 차단, 세션 타임아웃, 패스워드 정책 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| `/etc/passwd`와 `/etc/shadow` | 해시 식별자, shadow 필드, 패스워드 만료 정책, 권한 |
| 로그인 로그 | 실패 로그인 추적, 현재 로그인, 마지막 로그인, 실행 명령 추적 |
| 파일 권한 | 특수권한 탐지, world-writable 탐지, immutable 속성, umask |
| Windows 명령 | 공유 목록, 원격 세션, 로그 경로, 권한 상승 통제 |

### 독립 테스트베드
| 원칙 | 내용 |
|---|---|
| 환경 | throwaway Linux 컨테이너 또는 VM |
| 금지 | 호스트 `/etc`, 호스트 사용자, 실제 SSH 설정 변경 금지 |
| 저장 | 실습 파일은 컨테이너 내부 또는 `/private/tmp/infosec-lab` 같은 일회용 디렉터리 |
| 재사용 | 실습 종료 후 컨테이너 삭제 또는 VM snapshot 복원 |

### 실습 체크리스트
1. 테스트 계정 2개를 만들고 `/etc/passwd`, `/etc/shadow` 필드 의미를 확인한다.
2. 로그인 실패 로그 샘플을 만들거나 제공된 샘플로 `lastb` 의미를 확인한다.
3. SUID/SGID/sticky bit가 표시되는 파일 목록을 만들고 권한 문자열을 해석한다.
4. `find`로 world-writable 파일을 찾는 명령을 작성한다.
5. `lsof`로 프로세스가 연 파일을 확인한다.
6. 결과를 `파일/명령 -> 보안 의미 -> 조치` 형식으로 정리한다.

## 학습 묶음 3. 서비스 보안설정
### 핵심 학습 내용
| 서비스 | 학습 내용 |
|---|---|
| Apache/IIS | `Options -Indexes`, `TraceEnable Off`, HTTP method, URL Rewrite, 로그 |
| DNS/BIND | master/slave, zone transfer, `allow-transfer`, recursion, TTL/cache |
| SNMP | community string, SNMPv3, read-only, ACL, 161/162 |
| NTP | monlist, amplification, version, ACL, rate limit |
| SMTP | open relay, sendmail access DB, relay 제한 |
| DB | 권한, 감사, 외부 로그 저장, 암호화, 마스킹 |
| xinetd | `disable`, `only_from`, `no_access`, `instances`, `access_time` |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 설정값 빈칸 | `allow-transfer`, `disable`, `access.db`, `Options -Indexes` |
| 취약 설정 설명 | zone transfer 허용, open relay, 디렉터리 리스팅 |
| 대응 방안 | 접근 IP 제한, 최신 버전, 로그 외부 보관, 평문 서비스 대체 |
| 실무형 | 설정 파일 일부를 보고 문제점과 조치 쓰기 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| DNS zone transfer | authoritative/recursive 구분, cache poisoning, DNS spoofing, DRDoS |
| Apache/IIS | 불필요 method 제한, HTTP 헤더 제거, 쿠키 속성, 로그 경로 |
| DB 감사 | audit 설정, SYS 감사, 외부 로그, 최소권한 |
| SMTP relay | sendmail 설정, access DB, 인증 릴레이, 스팸 악용 |

### 독립 테스트베드
| Lab | 구성 | 관찰값 |
|---|---|---|
| Apache | Apache 컨테이너 1개 | directory listing, `.htaccess`, HTTP method, access/error log |
| DNS | BIND primary/secondary 컨테이너 2개 | zone transfer 허용/차단, TTL/cache |
| Mail 설정 읽기 | 실제 메일 발송 없이 샘플 설정 파일 | relay 허용/차단 규칙 해석 |
| DB 감사 | SQLite/PostgreSQL toy DB 또는 설정 샘플 | 권한과 감사 로그 개념 확인 |

외부 포트는 기본적으로 `127.0.0.1`에만 바인딩한다. DNS 실습은 Docker 내부 네트워크에서만 수행한다.

## 학습 묶음 4. 네트워크 프로토콜·장비·공격
### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| TCP/IP | SYN, ACK, FIN, RST, UDP, ICMP, TCP half-open scan |
| ARP/ICMP | ARP spoofing, static ARP, Smurf, ping 기반 스니핑 탐지 |
| DNS | spoofing, cache poisoning, zone transfer, amplification |
| SNMP/VLAN | agent/manager/MIB, community, VLAN 방식, Cisco `show vlan` |
| IPSec/VPN | AH, ESP, IKE, transport/tunnel, anti-replay sequence number |
| 방화벽/ACL | iptables, ingress/egress filtering, uRPF |
| 도구 | `hping3`, `tcpdump`, `nc`는 보조 연결 확인 도구 |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 공격명 식별 | ARP spoofing, Smurf, DNS spoofing, SYN flooding |
| 패킷 근거 | SYN/ACK/RST, ICMP echo, DNS ANY, TTL/cache |
| 설정 대응 | iptables, ACL, directed broadcast 차단, uRPF |
| 장비 특성 | VLAN, SNMP, switch forwarding, router ACL |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| Smurf/DRDoS | spoofed source IP, reflection, amplification, directed broadcast 차단 |
| DNS spoofing | cache poisoning, 빠른 응답, DNSSEC 개념, recursive 제한 |
| IPSec | AH/ESP/IKE, transport/tunnel, replay 방지, 인증·암호화 범위 |
| SNMP | v1/v2c community 위험, v3 보안, MIB 정보 노출 |

### 독립 테스트베드
| 원칙 | 내용 |
|---|---|
| 가능 | network namespace 또는 host-only VM에서 ARP table, routing table, tcpdump 관찰 |
| 제한 | DoS, 증폭, flood는 실제 부하 발생 금지 |
| 대체 | 샘플 PCAP, 합성 로그, 룰 매칭으로 학습 |
| 보조 도구 | `nc`는 localhost 연결 확인과 배너 확인 수준으로 제한 |

### 실습 체크리스트
1. TCP 연결과 종료 패킷 흐름을 PCAP 샘플로 읽는다.
2. ARP table을 보고 gateway MAC 변조 여부를 판단하는 표를 만든다.
3. iptables 규칙을 `체인 -> 프로토콜 -> 매치 조건 -> 타깃`으로 해석한다.
4. DNS zone transfer 허용/차단 결과를 비교한다.
5. SNMP는 실제 장비 대신 샘플 설정과 로그로 community 위험을 해석한다.

## 학습 묶음 5. 웹 취약점·시큐어코딩
### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| SQL Injection | 입력값 조작, PreparedStatement, 파라미터 바인딩 |
| XSS | stored/reflected/DOM, 출력 인코딩, 입력 검증, 쿠키 보호 |
| CSRF | 세션 쿠키 자동 전송, CSRF token, Referer/Origin, 재인증 |
| SSRF | 서버가 내부망/신뢰 리소스에 요청하게 되는 구조 |
| 파일 업로드 | 확장자/MIME 우회, 저장 경로, 실행권한, 웹셸 위험 |
| CRLF/Response Splitting | CR, LF, 헤더 조작, 쿠키/XSS 연계 |
| HTTP 설정 | Cookie `Secure`, `HttpOnly`, `SameSite`, Cache-Control, OPTIONS |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 취약점명 단답 | SQLi, XSS, CSRF, SSRF, 퍼징 |
| 코드 해석 | 취약한 SQL 문자열 연결, CSRF token 코드 |
| 우회 기법 | MIME 변조, 이중확장자, null byte, CRLF |
| 대응방안 | PreparedStatement, 인코딩, 토큰, 화이트리스트, 실행권한 제거 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| XSS | 저장형/반사형/DOM, 쿠키 탈취, CSP, 출력 인코딩 |
| CSRF | token, SameSite, Referer/Origin, 중요 기능 재인증 |
| SSRF | 내부망 접근, metadata endpoint, allowlist, DNS rebinding 주의 |
| 파일 업로드 | 확장자 검증, MIME 신뢰 한계, 저장 위치, 실행 권한, 웹셸 탐지 |

### 독립 테스트베드
| Lab | 구성 | 금지 |
|---|---|---|
| WebGoat/Juice Shop | localhost 취약 앱, 브라우저, ZAP | 외부 사이트 스캔 금지 |
| ZAP 관찰 | passive scan, request/response 확인 | 인터넷 대상 active scan 금지 |
| Toy app | 의도적으로 취약한 로컬 앱 | 실사용 서비스 코드 재사용 금지 |

실습 결과는 항상 `취약 입력 -> 서버 반응 -> 보안 영향 -> 대응 코드/설정`으로 정리한다.

## 학습 묶음 6. 관제·Snort·로그·침해사고
### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| IDS/IPS | IDS vs IPS, HIDS vs NIDS, signature/anomaly, FP/FN |
| Snort | rule header, action, protocol, src/dst, port, `msg`, `content`, `nocase`, `depth`, `threshold`, `sid` |
| SIEM/SOAR | 로그 수집, 상관분석, 경보, 자동화 대응 |
| PCAP | TCP flag, HTTP request, DNS query, ICMP, source/destination |
| 포렌식 | 증거 수집, 보존, 분석, 보고, 무결성 |
| 악성코드/APT | Kill Chain, MITRE ATT&CK, 제로데이, 루트킷, 웹셸 |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 룰 해석 | Snort `content`, `nocase`, `depth`, `threshold` 의미 |
| 탐지 품질 | 오탐, 미탐, 룰 부정확성 |
| 로그 판단 | 웹 로그, 시스템 로그, Fiddler, SIEM 설명 |
| 사고대응 | 증거 보존, 분석, 원인 파악, 보완 조치 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| Snort 룰 | HTTP buffer, offset/depth, threshold type, sid/rev |
| SIEM | 수집, 정규화, 상관분석, 대시보드, 알림, 포렌식 지원 |
| APT/Kill Chain | 정찰, 침투, C2, 내부 이동, 목표 달성, 탐지·차단 지점 |
| 포렌식 | 휘발성 우선순위, 해시 무결성, chain of custody |

### 독립 테스트베드
| Lab | 구성 | 관찰값 |
|---|---|---|
| Snort/Suricata offline | 샘플 PCAP + 로컬 룰 | alert 발생 여부, 룰 옵션 의미 |
| Web log triage | Apache 샘플 로그 | 공격 요청, status code, User-Agent, Referer |
| Security Onion eval | 가능하면 별도 VM | PCAP import, alert triage |

Security Onion은 무겁고 x86-64 요구가 있을 수 있으므로, 처음에는 Suricata/Snort offline PCAP 분석으로 시작한다.

## 학습 묶음 7. 암호통신·DB·모바일·DR 보강
### 핵심 학습 내용
| 축 | 반드시 알아야 할 내용 |
|---|---|
| IPSec | AH, ESP, IKE, transport/tunnel, sequence number |
| TLS | ClientHello/ServerHello, 인증서, 공개키, 세션키, 대칭키 |
| 해시/암호 | 해시, salt, 일방향성, 전자서명, PKI |
| DB | DDL/DML/DCL/TCL, GRANT/REVOKE, 감사, 암호화, 마스킹 |
| 데이터보호 | DLP, masking, encryption, access control |
| 모바일 | MDM, containerization, mobile virtualization, BYOD, deep link |
| DR | BCP, DRP, RTO/RPO, hot/warm/cold/mirror |

### 기출 패턴
| 패턴 | 예시 |
|---|---|
| 구성요소 단답 | AH/ESP/IKE, DLP, MDM |
| 비교 서술 | transport/tunnel, MDM/컨테이너화/모바일 가상화 |
| 실무형 | TLS handshake에서 공개키/대칭키 용도 설명 |
| 보수 학습 | DB 마스킹 방식명, EAM/IAM은 벤더 용어 차이 주의 |

### 레퍼런스 확장 후보
| 이미 나온 축 | 확장 가능 내용 |
|---|---|
| TLS handshake | 인증서 검증, 키 교환, 세션키, TLS 1.2/1.3 차이의 큰 개념 |
| DB 감사 | audit destination, SYS 감사, 외부 로그, SIEM 연계 |
| 모바일 보안 | MDM, MAM/MCM/EMM, 인증서 고정, deep link 검증 |
| DR | site 유형, RTO/RPO, BIA와 복구전략 연결 |

## 독립 테스트베드 아키텍처
### 기본 원칙
| 원칙 | 규칙 |
|---|---|
| 격리 | 모든 실습은 컨테이너, VM, network namespace, `/private/tmp` 하위 일회용 디렉터리에서만 한다. |
| 로컬 바인딩 | 웹 실습 포트는 `127.0.0.1`에만 바인딩한다. |
| 외부 영향 금지 | 인터넷, 회사/학교망, 제3자 IP, 실제 서비스 대상으로 스캔·공격·부하를 발생시키지 않는다. |
| 호스트 보호 | 호스트 `/etc`, SSH, 방화벽, 사용자 계정, 브라우저 기본 프로필을 변경하지 않는다. |
| 재사용 | 실습별 compose/README/checklist를 두고, 데이터는 volume 또는 snapshot으로 초기화한다. |
| 정리 | 실습 종료 후 컨테이너/VM/임시 네트워크/임시 파일 삭제 절차를 실행한다. |

### 실습 묶음

| 실습 묶음 | 학습 범위 |
|---|---|
| Linux hardening | Linux 계정·권한·로그 실습 |
| Service configuration | Apache/BIND/SMTP/xinetd 설정 해석 |
| Network protocol | TCP/ARP/DNS/iptables 증거 해석 |
| Web vulnerability review | 웹 취약점 코드·요청 해석 |
| IDS log triage | Snort/IDS/로그 triage |
| Risk and law tabletop | 위험관리·법규 tabletop |

실행 경로, 샌드박스와 정리 절차는 canonical 지식이 아니라 실행 프로젝트 계약이 소유한다.

### Lab별 산출물 표준
각 Lab은 아래 파일을 가진다.

| 파일 | 내용 |
|---|---|
| `README.md` | 목표, 기출 매핑, 실행 전제, 금지 행동 |
| `compose.yaml` 또는 `run.md` | 컨테이너/VM 실행 방법 |
| `questions.md` | 시험형 질문 |
| `expected-observations.md` | 기대 로그·출력·패킷 |
| `cleanup.md` | 정리 명령과 초기화 방법 |

## 4주 실행 로드맵
기간이 더 짧으면 Week 1~2를 우선하고, Week 3~4는 고득점 보강으로 본다.

| 주차 | 목표 | 학습 묶음 | 실습 |
|---:|---|---|---|
| Week 1 | 점수 기반 만들기 | 공통 배경, 위험관리, 접근통제, Linux 로그·권한 | Linux Hardening, 위험평가 표 |
| Week 2 | 설정·네트워크·웹 핵심 완성 | 서비스 보안설정, DNS/SNMP/VLAN, 웹 취약점 | Apache/BIND, WebGoat/Juice Shop |
| Week 3 | 관제·침해사고·암호통신 보강 | Snort/Suricata, SIEM, IPSec/TLS, DB 감사 | Offline PCAP, Snort/Suricata 룰 |
| Week 4 | 회차형 답안과 오답 회수 | 최근 23~31회, 예상문제, 법규 확장 | 실습 결과 기반 서술형 답안 작성 |

## 일일 루틴
| 블록 | 시간 | 수행 |
|---|---:|---|
| 개념 정리 | 30분 | AI 요약 또는 통합 학습본으로 해당 묶음 개념 읽기 |
| 기출 패턴 확인 | 30분 | 회차 파일, 빈도/패턴 문서에서 같은 개념 변형 확인 |
| 문제 적용 | 60분 | Part PDF 또는 회차 문항을 직접 답안 작성 |
| 실습/관찰 | 40분 | 해당 묶음의 로컬 실습 또는 샘플 로그/PCAP 해석 |
| 오답 회수 | 20분 | 오답을 `개념부족/키워드누락/문장화실패/레퍼런스미확인`으로 분류 |

## 오답 분류 규칙
| 원인 | 조치 |
|---|---|
| 개념부족 | AI 요약 또는 통합 학습본으로 돌아가 3줄 정의를 작성한다. |
| 키워드누락 | 암기표에 파일명, 명령어, 설정값, 법규 용어를 추가한다. |
| 문장화실패 | 3단 답안 템플릿으로 다시 쓴다. |
| 레퍼런스미확인 | `reference-source-index.md`와 `item-reference-map.md`에서 근거 상태를 확인한다. |
| 실습이해부족 | 해당 Lab의 기대 관찰값을 보고 다시 실행하거나 샘플 로그로 대체한다. |

## 학습 우선순위 결정 규칙
| 조건 | 처리 |
|---|---|
| 반복도 높음 + 최근성 높음 + 레퍼런스 명확 | 반드시 자세히 학습하고 실습까지 한다. |
| 반복도 높음 + 최근성 낮음 | 단답과 기본 서술형으로 압축한다. |
| 최근성 높음 + 반복도 낮음 | 예상 변형 후보로 두되 과도한 깊이는 피한다. |
| 레퍼런스가 medium 또는 벤더 용어 차이 있음 | 공식 용어를 단정하지 않고 비교·주의점 중심으로 학습한다. |
| PDF에만 있고 기출·출제기준 연결이 약함 | 시험 직전 암기 또는 배경지식으로 낮춘다. |

## 개인정보보호법·법규 학습 확장 예시
기출에 특정 조문이나 수치가 나왔다고 그 문항만 외우면 변형에 약하다. 법규는 `주체 -> 의무 -> 증거/기록 -> 점검/통지`로 확장한다.

| 기출 출발점 | 확장 학습 |
|---|---|
| 접근권한 관리 | 권한 부여·변경·말소, 최소권한, 계정 공유 금지, 이력 보관, 정기 점검 |
| 접속기록 | 기록 항목, 보관, 위·변조 방지, 정기 점검, 이상행위 대응 |
| 암호화 | 저장·전송 암호화, 비밀번호 일방향 해시, 개인정보처리시스템 보호 |
| CCTV/영상정보 | 설치 근거, 안내, 접근권한, 보관·파기, 열람 요청 |
| CISO/IDC | 지정·역할·책임, 보호조치, 점검, 시정명령, 보험 또는 피해보상 축 |
| 생체정보 | 비례성, 적법성, 목적제한, 투명성, 안전성, 통제권 보장 |

법규 수치와 시행일은 시험 직전에 공식 법령·고시 원천으로 다시 확인한다. 이 문서는 법률 자문이 아니라 시험 학습 로드맵이다.

## 최종 학습 산출물
시험 전까지 아래 6개 산출물을 직접 만들어야 한다.

| 산출물 | 완료 기준 |
|---|---|
| 반복 개념 암기표 | 위험관리, 접근통제, Linux 명령, 서비스 설정, 웹 취약점, Snort 룰을 한 표로 정리 |
| 법규 적용표 | 개인정보, ISMS-P, 정보통신망법 축을 주체·의무·기록·점검으로 정리 |
| 설정/명령 표 | 파일명, 명령어, 설정값, 보안 의미, 조치를 한 줄로 작성 |
| 로그/PCAP 해석 노트 | 증거, 공격명, 판단근거, 대응방안 구조로 작성 |
| 실습 관찰표 | 각 Lab의 관찰값과 시험형 질문 답안 작성 |
| 오답 회수표 | 오답 원인과 재학습 위치를 연결 |

## 최종 판단
현재 두 PDF만 순서대로 읽는 방식은 효율이 낮다. PDF는 개념 설명과 문제풀이 재료로 쓰고, 실제 학습 순서는 `기출 반복 개념군`, `최근성`, `KCA 출제기준`, `공식 레퍼런스`, `답안 작성 가능성`으로 재배열해야 한다.

가장 먼저 해야 할 일은 Linux/Unix 로그·명령, 위험관리/접근통제, 서비스 보안설정, 웹 취약점, DNS/SNMP/VLAN, Snort/관제를 묶어서 공부하는 것이다. 그 다음 개인정보·ISMS-P·법규를 상황형으로 확장하고, IPSec/TLS/DB/모바일/DR은 고득점 보강으로 붙인다.

독립 테스트베드는 충분히 구성할 수 있다. 다만 실습의 목적은 공격 성공이 아니라 `관찰 가능한 증거를 보고 시험 답안으로 바꾸는 능력`을 만드는 것이다.
