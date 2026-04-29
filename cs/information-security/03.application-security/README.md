# 3과목. 어플리케이션 보안

> 정보보안기사 필기 3과목. 출제기준 KCA 2023.1.1 ~ 2026.12.31, 20문제.
> 인터넷 응용 서비스(FTP·메일·Web/App·DNS·DB) 의 동작 원리와 보안 기법, 전자상거래 보안 프로토콜·인증 기술, 어플리케이션 보안 취약점과 시큐어 코딩(개발 보안) 까지 다룬다.

## 1. 출제기준 매핑

| 주요항목 | 세부항목 | 세세항목 | 작성 파일 |
|---|---|---|---|
| 1. 인터넷 응용 보안 | 1) FTP 보안 | FTP 개념 / FTP 서비스 운영 / FTP 공격 유형 / FTP 보안기술 | 02 |
| | 2) 메일 보안 | 메일 개념 / 메일 서비스 운영 / 메일 서비스 공격유형(스팸 메일·악성 메일·웜 등) 과 대책 / 메일 보안 기술 | 03 |
| | 3) Web/App 보안 | Web/App 개념 / Web/App 운영 / Web/App 장애 분석 및 대응 / Web/App 공격 유형 / Web/App 보안 기술 | 04·05·06 |
| | 4) DNS 보안 | DNS 개념 / DNS 서비스 운영 / DNS 공격유형 / DNS 보안 기술 | 01 |
| | 5) DB 보안 | DB 보안 개념 / DB 공격 유형 / DB 보안 기술 | 07 |
| 2. 전자 상거래 보안 | 1) 전자상거래 보안 기술 | 전자지불 수단별 보안요소 / 전자상거래 보안 프로토콜 / 전자상거래 인증기술 / 무선플랫폼에서의 전자상거래 보안 | 08 |
| 3. 어플리케이션 보안 취약점 | 1) 어플리케이션 보안취약점 대응 | 어플리케이션 보안취약점 유형 / 어플리케이션 보안 취약점 대응 기술 | 05 |
| | 2) 어플리케이션 개발 보안 | 소프트웨어 개발 보안 개념 및 요구사항 / 소스코드 개발 보안(Secure Coding) / 개발보안 툴 | 09 |

## 2. 파일 구성

| 파일 | 주제 | 출제기준 매핑 | 통합자료 매핑(line) | 3과목.txt 매핑(line) |
|---|---|---|---|---|
| `01.dns-dhcp-snmp.md` | DNS 개념·질의 과정 / 네임서버 구성·존 파일 / DNS 레코드 / DNS 도구(nslookup·dig·whois) / DNS Spoofing·Cache Poisoning / DNSSEC / Bind DNS 보안(재귀적 질의·존 전송 제한) / DHCP 동작·Starvation Attack / SNMP(Manager-Agent·MIB·SMI·Community String·v1/v2/v3·USM·VACM) | 1.4 DNS 보안 + 보강(DHCP·SNMP) | 3008 ~ 3238 | 1 ~ 175, 318 ~ 410 |
| `02.ftp-security.md` | FTP 능동 모드·수동 모드 / 제어채널·데이터채널 / FTP Bounce Attack / TFTP·익명 FTP 공격 / ftpusers·user_list·tcp_wrappers / SFTP(SSH)·FTPS(SSL/TLS) | 1.1 FTP 보안 | 3240 ~ 3314 | 257 ~ 317 |
| `03.mail-security.md` | MUA·MTA·MDA·MRA 구조 / SMTP·POP3·IMAP·SMTPS·POP3S·IMAPS / 메일 큐·사용자 메일함 / SMTP 봉투·메시지·릴레이 / sendmail 구성·access 파일 / 이메일 인증 SPF·DKIM·DMARC / Received·Received-SPF·Authentication-Results 헤더 / 스팸메일 방지(Procmail·Sanitizer·Inflex·SpamAssassin) / S/MIME·OpenPGP | 1.2 메일 보안 | 3316 ~ 3469 | 952 ~ 1109 |
| `04.http-and-web-client.md` | HTTP 1.0/1.1/2/3 / 요청·응답 메시지 구조 / 주요 메소드(GET·POST·HEAD·PUT·DELETE·OPTIONS·TRACE·CONNECT) / 상태코드(1xx ~ 5xx) / 상태 유지(쿠키·세션) / 쿠키 보안 속성(HttpOnly·Secure·SameSite·Expires) / 웹 브라우저 보안 영역 / HTTPS·HSTS | 1.3 Web/App 보안(개념·운영) | 3471 ~ 3570 | 176 ~ 256 |
| `05.web-app-attacks.md` | SQL Injection(Form·Union·Stored Procedure·Mass·Error-Based·Blind) / XSS(Stored·Reflected·DOM-Based) / CSRF / SSRF / OS Command Injection / 파일 업로드·다운로드·경로 조작·파일 삽입(LFI·RFI) / URL·파라미터 변조 / 불충분한 세션 관리 / 정보누출 / HTTP 응답 분할 / XXE Injection / Xpath/Xquery Injection / 악성 컨텐츠 / 불충분한 인증·인가 / 취약한 패스워드 복구 / 자동화 공격(CAPTCHA) / 데이터 평문전송 / 쿠키 변조 / OWASP Top 10·CWE Top 25 매핑 | 1.3 Web/App 공격 유형 + 3.1 어플리케이션 보안취약점 | 3573 ~ 4097 | 417 ~ 750 |
| `06.web-server-hardening.md` | 개발 보안 관리 원칙 / 디렉터리 리스팅 / 심볼릭 링크 사용 설정 / 웹 서비스 메소드 제한(LimitExcept) / 관리자 페이지 노출 / 위치공개·백업파일 / 검색엔진(robots.txt) / 웹 서비스 최소 권한 사용자 / 웹 서비스 정보 숨김(ServerTokens·ServerSignature) / httpd.conf 주요 지시자 / 웹 로그 분석(NCSA CLF·ELF·W3C ELF) / 보안서버 구축(SSL/TLS 인증서·OpenSSL·Cipher Suite) | 1.3 Web/App 보안 기술·장애 분석 + 보안서버 | 4099 ~ 4373 | 751 ~ 951 |
| `07.db-security.md` | 트랜잭션 ACID(원자성·일관성·격리성·영속성) / SQL 분류(DML·DDL·DCL·TCL) / 뷰 기반 접근통제 / SQL 기반 접근통제(GRANT·REVOKE·DENY) / 데이터베이스 보안 위협(집성·추론) / 보안 통제(접근통제·추론통제·흐름통제) / 데이터베이스 암호화(컬럼: API·Plug-in·Hybrid / 블록: TDE·파일 암호화) / MySQL DBMS 취약점 점검 | 1.5 DB 보안 | 4374 ~ 4502 | 1110 ~ 1180 |
| `08.electronic-commerce-security.md` | **Tier 1**: 전자지불 시스템 분류(전자화폐·신용카드 기반·계좌이체 기반·전자수표) / SET 프로토콜(이중 서명·인증서·5단계) / SSL·TLS 기반 안전결제(4과목 cross-ref) / 3-D Secure 1·2 (EMVCo) / **Tier 2**: 전자상거래 인증기술(OTP·PKI·공인인증서·I-PIN·FIDO2 간략) / 무선플랫폼 전자상거래 보안(WPKI·WTLS) / **Tier 3**: PCI DSS v4·전자금융감독규정·전자서명법 cross-ref / EMV·NFC·OAuth 2.0·OIDC·FIDO2 (4과목 cross-ref) | 2.1 전자상거래 보안 | (없음, 외부 보강 100%) | (없음) |
| `09.secure-development.md` | (1) 소프트웨어 개발 보안 개념: Secure SDLC 5단계 + 단계별 보안 활동 + Traditional SDLC 비교 / (2) KISA SW 개발보안 가이드 7대 보안약점(입력 데이터 검증·보안 기능·시간 및 상태·에러 처리·코드 오류·캡슐화·API 오용) + 각 카테고리 대표 사례 + 05 단원 cross-ref / (3) OWASP Top 10 ↔ KISA 7대 / CWE Top 25 ↔ KISA 7대 매핑표 / (4) 개발 보안 도구: SAST·DAST·IAST·SCA·RASP 분류표(동작 시점·장단점·대표 도구) | 3.2 어플리케이션 개발 보안 | (4099 ~ 4111 일부) | (751 ~ 761 일부) + 외부 보강 |

> 통합자료 line 4503 이후의 "어플리케이션 응용" 영역(클라우드 컴퓨팅·블록체인·사물 인터넷) 은 사용자 결정에 따라 1과목·5과목 영역으로 이관 대상이며, 3과목 범위 밖이다.
> 출제기준 1.4 (DNS 보안) 과 함께 통합자료가 같은 "어플리케이션 기본" 으로 묶어 둔 DHCP·SNMP 도 01 단원에서 함께 다루되, 출제기준에 명시된 1.4 DNS 보안 항목과 보강 항목(DHCP·SNMP) 은 §0 들어가며 에서 명시 분리한다. SNMP 는 실기 출제기준 "1.4 보안장비 및 네트워크 장비별 보안특성 파악하기" 에 직접 명시되어 있어 시험 대비상 출제 가능성 보강 학습 대상이다.
> 출제기준 1.3 Web/App 보안 은 분량이 매우 크므로(통합자료 약 900줄 + 3과목.txt 약 770줄) 04(개념·운영) / 05(공격 유형) / 06(보안 기술·운영) 세 단원으로 분할한다. 출제기준 3.1 어플리케이션 보안취약점 영역은 05 와 통합 작성한다(출제기준 매핑상 동일 취약점 카테고리이므로 분할 시 중복 발생). 05 단원 내부는 OWASP Top 10 (2021) 카테고리 + 통합자료 취약점 카테고리 매핑 구조로 작성한다.
> 출제기준 2.1 전자상거래 보안 과 3.2 어플리케이션 개발 보안 은 통합자료에 거의 부재하므로 1차 출처 외부 보강이 필수이며, 작성 시 [외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §C 를 1차로 사용한다.
> 08 단원은 기출 비중에 비례한 3-Tier 우선순위(Tier 1: SET·SSL/TLS·3DS / Tier 2: 전자상거래 인증·무선플랫폼 / Tier 3: PCI DSS·법령) 로 작성하며, FIDO·OAuth·OIDC 는 4과목 (인증) 과 중복되므로 cross-ref 처리한다.
> 09 단원은 학습 효율을 위해 KISA SW 개발보안 가이드의 47개 점검 항목 전수가 아닌 7대 보안약점 카테고리 + 대표 사례 + OWASP/CWE 매핑 구조로 작성한다.

## 3. 학습 가이드

### 학습 순서 (권장)

1. **01 → 02 → 03** (네트워크 응용 서비스 1부): DNS·DHCP·SNMP → FTP → 메일 — 어플리케이션 계층 프로토콜의 동작 원리와 평문 전송의 한계, 인증·암호화 보강 기술을 함께 학습한다.
2. **04 → 05 → 06** (Web/App 3부작): HTTP·쿠키·세션 → 웹 어플리케이션 공격 → 웹 서버 운영 보안 — 출제 비중이 가장 큰 영역. 04 의 메시지 구조와 상태 유지 기술이 05 의 공격 메커니즘을 이해하는 토대.
3. **07** (DB 보안): SQL Injection 의 방어 측면(05) 과 연결지어 학습.
4. **08** (전자상거래): 4과목 (암호학·인증) 의 PKI·전자서명·OTP 와 cross-ref 로 학습.
5. **09** (개발 보안): 05 의 취약점을 코드 레벨에서 어떻게 예방하는지 SDLC 관점으로 정리.

### 우선순위 (출제 빈도 기준)

- 🔴 최상: 05(웹 공격·SQLi·XSS·CSRF·File Upload), 03(SPF·DKIM·DMARC), 01(DNS Spoofing·Cache Poisoning·DNSSEC), 06(httpd.conf·SSL/TLS·웹 로그) — 분량·기출 비중 모두 높음
- 🟠 상: 02(FTP 능동·수동), 04(쿠키 보안 속성·HTTP 메소드), 07(DB 암호화 방식·접근통제)
- 🟡 중: 08(전자상거래 프로토콜·SET·3DS), 09(시큐어 코딩·SAST/DAST·CWE Top 25)

### 외부 보강 필요 영역 (통합자료에 없음 / 빈약)

이 영역은 작성 시 [외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §2 의 출처를 1차 사용한다.

| 파일 | 보강 범위 | 1차 출처 |
|---|---|---|
| 01 | DNSSEC RR(RRSIG·DNSKEY·DS·NSEC·NSEC3) / DoH·DoT / SNMPv3 USM·VACM 세부 / DHCP Option 82(Relay Agent) | RFC 1034·1035 (DNS), RFC 4033 ~ 4035 (DNSSEC), RFC 8484 (DoH), RFC 7858 (DoT), RFC 3411 ~ 3416 (SNMPv3), RFC 3046 (DHCP Option 82), KISA DNSSEC 운영 가이드 |
| 02 | FTP Security Extension (RFC 2228) / FTP over TLS 모드(Explicit·Implicit) / SFTP 와 FTPS 차이 / FTP Extended Passive (RFC 2428) | RFC 959 (FTP), RFC 2228, RFC 2428, RFC 4217 (FTP over TLS), IETF SECSH 워킹그룹 자료(SFTP 드래프트) |
| 03 | SMTP·IMAP·POP3 표준 정의 / DKIM 서명 알고리즘(RSA·Ed25519) / DMARC `p=` 정책(none/quarantine/reject) / S/MIME·OpenPGP 인증서 / MTA-STS·TLS-RPT | RFC 5321 (SMTP), RFC 5322 (IMF), RFC 1939 (POP3), RFC 9051 (IMAP4rev2), RFC 7208 (SPF), RFC 6376 (DKIM), RFC 7489 (DMARC), RFC 8460 (TLS-RPT), RFC 8461 (MTA-STS), RFC 8551 (S/MIME 4.0), RFC 4880 (OpenPGP), KISA 이메일 보안 가이드 |
| 04 | HTTP Semantics 표준 / 쿠키 RFC / SameSite 속성·CSP·HSTS / HTTP/2·HTTP/3 차이 | RFC 9110 (HTTP Semantics), RFC 9111 (HTTP Caching), RFC 9112 (HTTP/1.1), RFC 9113 (HTTP/2), RFC 9114 (HTTP/3), RFC 6265 (HTTP Cookies), RFC 6797 (HSTS), W3C CSP Level 3 |
| 05 | OWASP Top 10 (2021) 카테고리 정의 / OWASP API Security Top 10 (2023) / CWE Top 25 (2023) / OWASP Cheat Sheet (XSS·CSRF·SSRF·SQLi·File Upload·XXE) / OWASP ASVS 4.0 검증 항목 | OWASP Foundation 공식 문서, MITRE CWE Top 25, OWASP Cheat Sheet Series, OWASP ASVS 4.0 |
| 06 | Apache HTTP Server 공식 디렉티브 정의 / NIST 웹 서버 보안 가이드 / OWASP Secure Headers Project / TLS 1.3 권장 Cipher Suite (KCMVP·NIST) | NIST SP 800-44 v2 (Public Web Servers), NIST SP 800-95 (Web Services Security), Apache HTTP Server Documentation, OWASP Secure Headers Project, KISA TLS 보안 가이드 |
| 07 | NIST 데이터베이스 보안 가이드 / TDE 표준 동작(Oracle·SQL Server·MySQL) / DB 접근 제어(RBAC·MAC·DAC) / SQL Injection 방어 표준 | NIST SP 800-53 Rev. 5 (AC·SC·IA), OWASP Database Security Cheat Sheet, ISO/IEC 27001:2022, KISA DB 암호화 가이드 |
| 08 | **Tier 1 출처**: SET 프로토콜 (시험 기출 빈출, 사실상 사장된 표준이지만 학습 필수) / SSL·TLS 기반 결제 / 3-D Secure 1·2 / 전자지불 시스템 분류 — **Tier 2 출처**: PCI DSS v4 / 전자금융감독규정 / WPKI·WTLS — **Tier 3 출처**: EMV·FIDO·OAuth·OIDC (4과목 cross-ref) | PCI Security Standards Council (PCI DSS v4.0.1, 2024), EMVCo 3DS Protocol Specification 2.x, EMV Specifications v4.4, W3C Web Authentication Level 2, RFC 6749 (OAuth 2.0), OpenID Connect Core 1.0, [전자서명법] (국가법령정보센터), KISA 전자금융감독규정 / 전자상거래 보안 가이드, ISO/IEC 7813 (Magnetic Stripe) |
| 09 | (1) Secure SDLC 5단계·단계별 활동 / (2) KISA 7대 보안약점 카테고리 정의·대표 사례 / (3) OWASP Top 10 ↔ KISA 7대 / CWE Top 25 ↔ KISA 7대 매핑 / (4) SAST·DAST·IAST·SCA·RASP 분류 — **47개 점검 항목 전수 ❌** (학습 효율 우선) | NIST SP 800-218 (SSDF v1.1, 2022), OWASP SAMM 2.0, OWASP ASVS 4.0, KISA SW 개발보안 가이드(전자정부 SW 개발·운영자 가이드, 2017), MITRE CWE Top 25 (2023), NIST SP 800-204 (Microservices Security) |

## 4. 작성 원칙 (3과목 적용)

[외부자료 검증 체크리스트](../docs/외부자료-검증체크리스트.md) §3 을 따른다. 3과목 추가 사항:

1. **누락 금지**: 위 매핑표의 통합자료·3과목.txt 라인 범위를 반드시 빠짐없이 흡수한다.
2. **추론 금지**: 양쪽 원본에 없는 내용은 외부 자료 1차 출처를 각주로 명시한 경우에만 추가한다. "아마/보통은/것으로 보인다/것으로 추정/자주 인용/자주 출제" 등 단정·추론 표현 금지.
3. **충돌 시 우선순위**: 출제기준 → 통합자료(체계적 표) → 3과목.txt(보충 사례)
4. **OCR 보정 명시**: 명백한 OCR 결함은 citation box(`> *원본 표기 보정*: ...`) 로 보정하며, 수치·플래그·식별자(예: 53/udp, 53/tcp, 21/tcp, 25/tcp, 110/tcp, 143/tcp, allow_url_fopen 등) 는 보정하지 않는다.
5. **표·명령어·예시 보존**: 통합자료의 표 구조와 3과목.txt 의 명령 예시(예: `dig @네임서버 도메인`, `ipconfig /flushdns`, `makemap hash /etc/mail/access`, `<LimitExcept GET POST>`) 는 학습 가치가 높으므로 원본 표기 그대로 유지한다.
6. **서술 원칙 (1·2 과목 정착)**: 각 H2/H3 단위로 "**정의(인용 박스) → 도입 단락(서술형) → 본문 → 표/예시 → 시험 포인트**" 흐름을 따른다. 표만으로 구성된 영역 금지 — 분류·체계·개념의 의미를 서술적으로 풀이하는 도입 단락 필수(2과목 06·08 단원에서 정착된 회귀 방지 패턴).
7. **외부 보강 출처 각주화**: 위 §3 외부 보강 영역은 모두 1차 출처(NIST·RFC·OWASP·MITRE·PCI SSC·EMVCo·W3C·KISA·국가법령정보센터 등) 를 각주로 명시한다. 위키피디아·민간 학원 자료는 1차 출처로 사용하지 않는다.
8. **cross-ref 정확성**: 1·2 과목 단원 및 3과목 단원 간 cross-ref 는 참조 대상 파일의 자체 §번호와 정확히 일치시킨다(H2 = `§N`, H3 = `§N-M`). 동일 파일 내부에서는 anchor 링크를 사용한다.
9. **표준 정의 약화**: 표준이 명시적으로 정의하지 않는 영역(예: NIST·RFC 가 직접 정의하지 않는 운용 사례) 은 "표준 정의" 가 아닌 "용어 사용 사례·운용 사례" 로 약화 표현한다.
10. **외부 보강 단정 표현 금지**: RFC 섹션 번호, NIST 문서 부제목, 표준 발표 연도, OWASP Top 10 카테고리, PCI DSS 버전 등은 작성 시점에 출처를 직접 확인하고 추측하지 않는다.

## 5. 참고 자료

- 출제기준 PDF: [`docs/info-sec-engineer-criteria-2023-2026.pdf`](../docs/info-sec-engineer-criteria-2023-2026.pdf)
- 외부자료 검증 체크리스트: [`docs/외부자료-검증체크리스트.md`](../docs/외부자료-검증체크리스트.md)
- 원본 자료: [`src/3과목.txt`](../src/3과목.txt) (1 ~ 1226), [`src/정보보안기사 정리_260214.txt`](../src/정보보안기사%20정리_260214.txt) (line 3007 ~ 4503 의 어플리케이션 챕터. 이 외 line 1394 ~ 3005 의 네트워크 챕터는 2과목으로, line 4549 ~ 4582 의 SecaaS·line 4638 ~ 5947 의 침해사고 분석 및 대응은 2과목으로, 어플리케이션 응용 안의 클라우드/블록체인/IoT 는 1·5과목으로 이관)
