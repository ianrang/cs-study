---
title: "정보보안기사 실기 문항-출제기준-참고문서 매핑"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-references, mapping]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "reference-source-index.md"
  - "exam-criteria-and-reference-catalog.md"
  - "subject-type-classification-detail.md"
  - "2023-02-practical-23.md"
  - "2023-04-practical-24.md"
  - "2024-01-practical-25.md"
  - "2024-02-practical-26.md"
  - "2024-04-practical-27.md"
  - "2025-01-practical-28.md"
  - "2025-02-practical-29.md"
  - "2025-04-practical-30.md"
source_count: 11
provenance: inferred
summary: "최근 23~30회 정보보안기사 실기 복원 문항을 KCA 실기 출제기준 세부항목과 패칭된 참고문서 ref_id에 연결한 1차 매핑."
evergreen: false
---

# 정보보안기사 실기 문항-출제기준-참고문서 매핑

## Scope
- 이 문서는 문항별 근거 연결의 SSOT이다.
- 현재 범위는 23회~29회 Naver 블로그 복원본과 30회 기존 wiki 복원본을 기준으로 정리한 최근 23회~30회 144개 문항이다.
- 문항 원문 전체는 회차별 복원 문서가 SSOT이므로 이 문서에는 반복하지 않는다.
- `REF-KCA-INFOSEC-PRACTICAL-CRITERIA`는 모든 행의 1차 기준이다. 다른 ref_id는 보조 참고문서로만 연결하며, `KCA가 해당 문서를 참고했다`고 단정하지 않는다.
- `official page confirmed` 상태의 ref_id는 공식 URL을 확인했지만 raw/source 원문 저장은 아직 하지 않은 보조 원천이다.
- 2026-07-03 2차 보강에서는 IETF RFC, NIST CSRC glossary/SP, GNU manual, OWASP community attack page, 국가법령정보센터 현행 법령 페이지를 공식 페이지 확인 상태로 추가했다. 해당 원천도 KCA 공식 참고문헌으로 단정하지 않고 보조 원천으로만 쓴다.

## Mapping

| item_id | round | no | criteria_detail | reference_ids | evidence | confidence | notes |
|---|---|---:|---|---|---|---|---|
| R23-Q1 | 23회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Windows IIS/DHCP 로그 경로와 파일명은 운영체제·서비스 로그 위치 지식이다. | high | Naver 교차 확인, 공식 원문 문구는 미검증 |
| R23-Q2 | 23회 | 2 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Linux x86-64 인자 전달 레지스터는 운영체제/시스템 실행 환경 특성이다. | high | 저수준 시스템 지식 |
| R23-Q3 | 23회 | 3 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | PLT/GOT와 동적 링크는 실행 파일 로딩과 런타임 심볼 해석 주제다. | high | 시스템 보안 기초와 연결 |
| R23-Q4 | 23회 | 4 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | ISMS-P 인증 기준 3대 영역은 관리체계·보호대책·개인정보 처리 단계다. | high | ISMS-P 기준과 직접 연결 |
| R23-Q5 | 23회 | 5 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `/var/log/messages`는 Unix/Linux 시스템 로그 파일이다. | high | OS 로그 지식 |
| R23-Q6 | 23회 | 6 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SQL Injection은 웹 입력값이 DB 질의를 변조하는 취약점이다. | high | 시큐어코딩 SQL 삽입 항목과 직접 연결 |
| R23-Q7 | 23회 | 7 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | PAM은 Linux 인증 모듈 체계다. | high | 인증 설정 점검과 연결 |
| R23-Q8 | 23회 | 8 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `hping3`는 TCP/IP 패킷 생성·스캔·공격 테스트 도구다. | high | 패킷/프로토콜 실무 도구 |
| R23-Q9 | 23회 | 9 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Tripwire와 Nessus는 무결성 점검·취약점 점검 도구다. | high | 점검 도구와 이력관리 축 |
| R23-Q10 | 23회 | 10 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NVD-CVE-DETAILS; REF-CWE-TOP-25; REF-FIRST-CVSS | Heartbleed는 OpenSSL 취약점과 영향 범위 판단 주제이며 NVD CVE detail에서 CVE-2014-0160 설명과 CVSS 3.1 점수가 확인된다. | high | 공식 CVE/NVD/CVSS 계열 보조 원천 확인, 공식 시험 원문 문구는 미검증 |
| R23-Q11 | 23회 | 11 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 위험관리 3단계는 위험분석·평가·대응 절차다. | high | 위험평가 직접 연결 |
| R23-Q12 | 23회 | 12 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 정보자산 관리의 구성요소와 보안 목적은 자산 식별·보호대책 선정의 전제다. | high | 자산관리 기본 |
| R23-Q13 | 23회 | 13 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 파일 업로드 취약점은 위험한 형식 파일 업로드와 웹셸 실행 조건을 다룬다. | high | 시큐어코딩 파일 업로드 항목과 연결 |
| R23-Q14 | 23회 | 14 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | TCP flag 조합은 TCP 연결 상태와 스캔/패킷 분석의 기본이다. | high | TCP 키워드 직접 연결 |
| R23-Q15 | 23회 | 15 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | NetBIOS 바인딩 제거는 Windows 네트워크 서비스 노출 완화 설정이다. | high | 기반시설 Windows 점검과 연결 |
| R23-Q16 | 23회 | 16 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-IETF-HTTP-CACHING | Cache-Control 헤더와 캐시 재검증/원본 서버 부하 해석은 RFC 9111의 HTTP cache와 cache control header field 정의로 보조 검증 가능하다. | high | IETF RFC 9111 공식 페이지 확인, 공식 시험 원문 문구는 미검증 |
| R23-Q17 | 23회 | 17 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PRIVACY-SAFETY-MEASURES | 개인정보 안전성 확보조치와 소상공인 적용 예외는 법적 준거성 판단이다. | high | 고시 연결 |
| R23-Q18 | 23회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | DNS master/slave zone 설정은 DNS 서비스 보안·운영 설정이다. | high | DNS 서비스 점검 |
| R24-Q1 | 24회 | 1 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PIPC-PIA-GUIDE | 개인정보영향평가 위험도 산정 공식은 개인정보 영향 분석과 위험평가다. | high | 문항에 PIPC/KISA 안내서 성격 직접 등장 |
| R24-Q2 | 24회 | 2 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | DB 암호화 방식은 DB 서비스 보호 설정이다. | high | DB 보안특성 |
| R24-Q3 | 24회 | 3 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | LAN 스위칭 방식은 네트워크 장비 동작 특성이다. | high | Switch 키워드 연결 |
| R24-Q4 | 24회 | 4 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 무선랜 보안 표준은 무선 프로토콜 보안특성이다. | medium | WPA/WPA2/WPA3 등 세부 표준 문항 원문과 직접 대응하는 공식 원천을 아직 raw/source로 고정하지 않아 보수적 유지 |
| R24-Q5 | 24회 | 5 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | VLAN 할당 방식은 네트워크 장비 분리·운영 설정이다. | high | 기반시설 네트워크 점검과 연결 |
| R24-Q6 | 24회 | 6 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `robots.txt`는 웹 크롤러 접근 제어를 위한 웹 서비스 설정이다. | high | 웹 서비스 설정 |
| R24-Q7 | 24회 | 7 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | ISO 31000 기반 위험평가는 위험관리 절차와 기준 수립 주제다. | high | 위험평가 직접 연결 |
| R24-Q8 | 24회 | 8 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-DLP-GLOSSARY | DLP는 data in use, data in motion, data at rest를 식별·모니터링·보호하는 체계이며 문항의 PC 에이전트와 네트워크 센서 설명은 endpoint/network actions와 연결된다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R24-Q9 | 24회 | 9 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `/proc` 기반 은닉 프로세스 탐지는 Linux 프로세스 점검이다. | high | OS 점검 명령 |
| R24-Q10 | 24회 | 10 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Apache 접근 로그 해석은 웹 로그 분석으로 침입 원인을 파악하는 주제다. | high | 로그분석 직접 연결 |
| R24-Q11 | 24회 | 11 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PRIVACY-SAFETY-MEASURES | 랜덤 라운딩은 PIPC 개인정보 안전성 확보조치 기준 안내서의 가명·익명처리 기술 분류에서 일반 라운딩, 제어 라운딩 등과 함께 명시된 처리 기법이다. | high | 기존 패칭 원천 내부 직접 근거 확인 |
| R24-Q12 | 24회 | 12 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NVD-CVE-DETAILS; REF-CWE-TOP-25; REF-FIRST-CVSS | Log4j 취약점은 취약 버전 식별과 보완 조치 관리 주제이며 NVD CVE detail과 CVSS 기준으로 보조 검증 가능하다. | high | 공식 CVE/NVD/CVSS 계열 보조 원천 확인, 공식 시험 원문 문구는 미검증 |
| R24-Q13 | 24회 | 13 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | 특수비트와 소유자 권한 조정은 Unix 파일 권한 점검이다. | high | Linux/Unix 권한 점검 |
| R24-Q14 | 24회 | 14 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `.rhosts` 신뢰 파일 제거는 원격접속 보안설정 보완이다. | high | Unix 원격접속 점검 |
| R24-Q15 | 24회 | 15 | 네트워크 및 보안장비 설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | IPTables 정책은 방화벽 룰 기반 네트워크 통제 설정이다. | high | Firewall 키워드 연결 |
| R24-Q16 | 24회 | 16 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | SNMP community와 버전 설정은 네트워크 장비 관리 보안이다. | high | SNMP 키워드 직접 연결 |
| R24-Q17 | 24회 | 17 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | OS별 패스워드 최소 길이 설정은 계정 정책 점검이다. | high | login.defs 등 운영체제 설정 |
| R24-Q18 | 24회 | 18 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | xinetd 접근제어와 인스턴스 제한은 Unix 서비스 보안설정이다. | high | 원격 서비스 제한 |
| R25-Q1 | 25회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Windows 기본 그룹 권한은 계정·접근통제 지식이다. | high | Windows 보안특성 |
| R25-Q2 | 25회 | 2 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-TEMPEST-GLOSSARY | TEMPEST는 정보시스템 장비의 비의도 compromising emanations에 대한 조사·통제 개념이며 전자파 방사 정보 유출 위협과 직접 연결된다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R25-Q3 | 25회 | 3 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IPSec 보안 기능은 네트워크 계층 보안 프로토콜 특성이다. | high | IPSec 키워드 직접 연결 |
| R25-Q4 | 25회 | 4 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 세션 하이재킹은 TCP 세션/인증 상태 탈취 공격이다. | high | TCP/IP 공격 특성 |
| R25-Q5 | 25회 | 5 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 예방·탐지·교정 통제는 보호대책 유형 분류다. | high | 관리적 보호대책 연결 |
| R25-Q6 | 25회 | 6 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | 메일 릴레이 제한은 SMTP 서비스 오픈 릴레이 방지 설정이다. | high | 메일 서비스 점검 |
| R25-Q7 | 25회 | 7 | 서비스별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 웹 프록시는 웹 요청 중계·필터링 서비스 특성이다. | high | 웹 서비스 특성 |
| R25-Q8 | 25회 | 8 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 서브넷 마스크 계산은 IP 주소 체계와 네트워크 분할 지식이다. | high | IP 키워드 연결 |
| R25-Q9 | 25회 | 9 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 퍼징은 비정상 입력으로 취약점을 탐지하는 점검 방법이다. | high | 취약점 점검 방법 |
| R25-Q10 | 25회 | 10 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SSRF 방지를 위한 허용/차단 목록은 서버 요청 대상 검증이다. | high | 시큐어코딩 SSRF 항목과 연결 |
| R25-Q11 | 25회 | 11 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 위험 수용·감소·전가·회피는 위험 대응 전략이다. | high | 위험처리 직접 연결 |
| R25-Q12 | 25회 | 12 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-SOAR-GLOSSARY | SOAR는 security orchestration, automation, and response의 공식 약어로 보안관제 자동화·대응 오케스트레이션 문항과 연결된다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R25-Q13 | 25회 | 13 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 소프트웨어 보안약점 분석 산출물은 개발보안 진단·보완 관리와 연결된다. | high | 시큐어코딩 가이드 연결 |
| R25-Q14 | 25회 | 14 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | ping을 이용한 sniffing 탐지는 ICMP/프로미스큐어스 모드 반응 특성이다. | high | ICMP/스니핑 특성 |
| R25-Q15 | 25회 | 15 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 기밀성 등급 구분은 정보자산 분류와 보호수준 산정이다. | high | 자산 중요도 산정 |
| R25-Q16 | 25회 | 16 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IDS 대응 동작은 침입 탐지·알림·차단 운영이다. | high | IDS/관제 연결 |
| R25-Q17 | 25회 | 17 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | ARP redirect/spoofing은 ARP 프로토콜 악용 공격이다. | high | ARP 키워드 직접 연결 |
| R25-Q18 | 25회 | 18 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-MALWARE-INCIDENT-GUIDE | PE 악성코드 분석은 악성코드 침해 예방·대응과 호스트 침해 원인 분석 범위에 속하며 NIST SP 800-83의 malware incident handling 범위로 보조 검증 가능하다. | high | NIST SP 800-83 공식 페이지 확인, PE 포맷 세부 원천은 별도 보강 가능 |
| R26-Q1 | 26회 | 1 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `login.defs` 패스워드 정책은 Linux 계정 보안 설정이다. | high | 운영체제 계정 정책 |
| R26-Q2 | 26회 | 2 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | CSMA/CA와 RTS/CTS는 무선 매체 접근 제어 특성이다. | high | 무선 프로토콜 |
| R26-Q3 | 26회 | 3 | 서비스별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Recursive/Authoritative DNS 구분은 DNS 서비스 동작 특성이다. | high | DNS 서비스 특성 |
| R26-Q4 | 26회 | 4 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE; REF-OWASP-TOP-10-WEB; REF-CWE-444-HTTP-SMUGGLING | HTTP request smuggling은 HTTP 요청/응답 해석 불일치를 악용하는 weakness로 CWE-444 전용 항목과 직접 연결된다. | high | CWE-444 공식 페이지 확인, 공식 시험 원문 문구는 미검증 |
| R26-Q5 | 26회 | 5 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | false positive/negative는 탐지 시스템 정확도 평가 개념이다. | high | IDS/관제 운영 |
| R26-Q6 | 26회 | 6 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | XML 조회 조건의 자료형 검증은 입력값 검증과 보안약점 방지다. | high | 시큐어코딩 입력검증 |
| R26-Q7 | 26회 | 7 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-MITRE-ATTACK | APT는 단계적 침투와 장기 은닉을 전제로 한 침해 분석 주제이며 MITRE ATT&CK는 실제 관찰 기반 공격 전술·기술 knowledge base다. | high | MITRE ATT&CK 공식 보조 원천 확인 |
| R26-Q8 | 26회 | 8 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Slow Read Attack은 HTTP 연결 유지와 응답 수신 지연을 악용하는 DoS다. | high | 웹 서비스 DoS 설정 |
| R26-Q9 | 26회 | 9 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | XSS 유형 구분은 웹 입력·출력 검증 취약점 주제다. | high | 시큐어코딩 XSS 항목 |
| R26-Q10 | 26회 | 10 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | HIDS/NIDS 비교는 침입탐지 시스템 배치와 모니터링 범위다. | high | IDS 관제 |
| R26-Q11 | 26회 | 11 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 위험 구성요소는 자산·위협·취약점·영향을 식별하는 분석 축이다. | high | 위험분석 기본 |
| R26-Q12 | 26회 | 12 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 위험관리 절차와 대응은 위험평가 결과를 처리하는 과정이다. | high | 위험평가 직접 연결 |
| R26-Q13 | 26회 | 13 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Windows UAC 팝업과 관리자 권한 실행은 운영체제 권한 상승 통제다. | high | Windows 접근통제 |
| R26-Q14 | 26회 | 14 | 정보자산 위협 및 취약점 분석 정리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PIPC-PIA-GUIDE | 개인정보 영향평가 고려사항은 개인정보 처리와 위험 분석 범위 식별이다. | high | PIA 안내서 연결 |
| R26-Q15 | 26회 | 15 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | promiscuous 모드 스니핑 탐지는 네트워크 인터페이스와 패킷 수신 특성이다. | high | 스니핑 특성 |
| R26-Q16 | 26회 | 16 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | XSS 정의와 유형은 웹 애플리케이션 입력/출력 보안약점이다. | high | 시큐어코딩 XSS 항목 |
| R26-Q17 | 26회 | 17 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | DB 권한 부여 제한과 접근권한 최소화는 DB 서비스 보안설정 점검이다. | high | DBMS 점검 |
| R26-Q18 | 26회 | 18 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NVD-CVE-DETAILS; REF-CWE-TOP-25; REF-FIRST-CVSS | Heartbleed 보완은 취약 라이브러리 식별과 패치 조치 관리이며 NVD CVE detail에서 영향 버전·취약점 설명·CVSS 기준을 보조 확인할 수 있다. | high | 공식 CVE/NVD/CVSS 계열 보조 원천 확인, 공식 시험 원문 문구는 미검증 |
| R27-Q1 | 27회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | DAC/MAC/RBAC는 접근통제 모델과 권한 관리 방식이다. | high | 인증·접근통제 |
| R27-Q2 | 27회 | 2 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | RARP는 MAC 주소에서 IP 주소를 얻는 네트워크 프로토콜이다. | high | TCP/IP 주소 체계 |
| R27-Q3 | 27회 | 3 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | VLAN 구성 방식은 네트워크 장비 기반 논리 분리 운영이다. | high | VLAN 키워드 연결 |
| R27-Q4 | 27회 | 4 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-LAW-ELECTRONIC-FINANCIAL-TRANSACTION | CISO 지정과 전자금융 분야 책임은 전자금융거래법 현행 법령 페이지로 보조 검증 가능한 법적 준거성 판단이다. | high | 국가법령정보센터 현행 법령 페이지 확인, 조문별 raw/source 저장은 미수행 |
| R27-Q5 | 27회 | 5 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | utmp/wtmp/lastlog는 Unix 로그인 기록 파일이다. | high | OS 로그 파일 |
| R27-Q6 | 27회 | 6 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | FIN/XMAS/Null scan은 TCP flag 기반 스캔 방식이다. | high | TCP 스캔 |
| R27-Q7 | 27회 | 7 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SQL Injection, XSS, OS Command Injection은 웹 입력값 검증 취약점이다. | high | 시큐어코딩 주요 보안약점 |
| R27-Q8 | 27회 | 8 | 서비스별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | HTTP OPTIONS 메서드는 웹 서버가 허용하는 메서드 노출 특성이다. | high | HTTP 서비스 특성 |
| R27-Q9 | 27회 | 9 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Hot Fix와 Update 구분은 운영체제 보안업데이트 특성이다. | high | 보안업데이트 키워드 |
| R27-Q10 | 27회 | 10 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | SNMP agent/manager/MIB는 네트워크 장비 관리 프로토콜 구조다. | high | SNMP 키워드 직접 연결 |
| R27-Q11 | 27회 | 11 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 위험수용은 위험평가 후 선택하는 위험 처리 방식이다. | high | 위험처리 직접 연결 |
| R27-Q12 | 27회 | 12 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | VLAN은 네트워크 분리와 브로드캐스트 도메인 제어 기술이다. | high | VLAN 반복 출제 |
| R27-Q13 | 27회 | 13 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 복합접근법은 기준선/상세 위험분석을 결합하는 위험분석 방법론이다. | high | 위험분석 방법 |
| R27-Q14 | 27회 | 14 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 정보보호조치 지침의 정책·조직·자산관리 항목은 관리체계 보호대책이다. | high | ISMS-P/관리체계 연결 |
| R27-Q15 | 27회 | 15 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Unix 파일 권한 표기는 소유자/그룹/기타 권한 점검이다. | high | 파일 권한 |
| R27-Q16 | 27회 | 16 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-CONTINGENCY-PLANNING | DR site 유형은 contingency planning, resilience, disaster recovery planning 범위의 자산 보호대책이며 NIST SP 800-34로 보조 검증 가능하다. | high | NIST SP 800-34 공식 페이지 확인 |
| R27-Q17 | 27회 | 17 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | PreparedStatement는 SQL Injection을 줄이는 안전한 질의 작성 방식이다. | high | 시큐어코딩 SQL 삽입 대응 |
| R27-Q18 | 27회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | NTP monlist 비활성화와 버전 업그레이드는 NTP 증폭 공격 대응 설정이다. | high | NTP 서비스 점검 |
| R28-Q1 | 28회 | 1 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Smurf는 Directed Broadcast와 ICMP echo request 악용을 차단해야 하는 ICMP 반사형 DoS 유형이다. | high | Naver 답안 기준으로 보강 |
| R28-Q2 | 28회 | 2 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SSRF는 웹 요청이 내부망 자원 접근으로 이어지는 입력 검증 계열 취약점이다. | high | 시큐어코딩 가이드 구현단계 보안약점의 SSRF 항목과 연결 |
| R28-Q3 | 28회 | 3 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | VLAN 할당 방식과 Cisco 확인 명령은 네트워크 장비 보안 운영 지식이다. | high | 기반시설 상세가이드의 네트워크 장비 점검과도 연결 가능 |
| R28-Q4 | 28회 | 4 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | HttpOnly는 XSS 상황에서 쿠키 접근을 제한하는 웹 보안 설정이다. | high | 기존 분류는 네트워크 보안이지만 어플리케이션 보안 연결이 더 강함 |
| R28-Q5 | 28회 | 5 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | HTTP 헤더 인젝션은 CR/LF로 응답 헤더 경계를 조작한다. | high | HTTP 응답분할/헤더 처리 취약점과 연결 |
| R28-Q6 | 28회 | 6 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-MITRE-ATTACK | 사이버 킬 체인은 APT 침해 분석 단계 모델이며 MITRE ATT&CK는 공격 전술·기술 지식베이스로 보조 연결 가능하다. | medium | Kill Chain 자체의 전용 공식 원천을 아직 고정하지 않아 medium 유지 |
| R28-Q7 | 28회 | 7 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `lsof`는 Linux 열린 파일과 프로세스 상태 확인 명령이다. | high | 운영체제 점검 명령 |
| R28-Q8 | 28회 | 8 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `lastb`는 Linux 로그인 실패 기록 확인 명령이다. | high | 인증 로그 점검 |
| R28-Q9 | 28회 | 9 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 정보자산 중요도 산정은 CIA 기준으로 자산을 식별·분류한다. | high | 위험분석 수행준거와 직접 연결 |
| R28-Q10 | 28회 | 10 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 위험관리계획은 위험분석 범위·방법·대응 활동을 정한다. | high | 위험분석 계획 수립 |
| R28-Q11 | 28회 | 11 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 보호구역·출입권한·접근통제는 ISMS-P 물리보안 보호대책이다. | high | ISMS-P 인증기준 안내서 연결 |
| R28-Q12 | 28회 | 12 | 서비스별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-OWASP-MOBILE-TOP-10 | Deep link는 모바일 앱 기능 이동 기술이며 OWASP Mobile Top 10 2024는 unprotected endpoints에 deep link를 향후 고려 후보로 명시한다. | high | OWASP Mobile 공식 보조 원천 확인 |
| R28-Q13 | 28회 | 13 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Shell은 사용자 명령 해석과 커널 전달을 담당한다. | high | 운영체제 기본 보안특성 |
| R28-Q14 | 28회 | 14 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | NetBIOS over TCP/IP 비활성화는 Windows 서비스 노출 완화 설정이다. | high | Naver 답안 순서 기준: 14번 NetBIOS |
| R28-Q15 | 28회 | 15 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IPsec의 AH/ESP/IKE와 터널·전송 모드는 프로토콜별 보안특성이다. | high | Naver 답안 순서 기준: 15번 IPSec |
| R28-Q16 | 28회 | 16 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산 중요도 산정은 보호 대상 식별과 관리 우선순위 산정이다. | high | Naver 답안 순서 기준: 16번 자산 중요도 |
| R28-Q17 | 28회 | 17 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Oracle audit_trail, audit_file_dest, SYS 감사와 외부 로그 저장은 DB 감사 설정 점검 주제다. | high | Naver 답안 기준으로 감사 설정 해석 보강 |
| R28-Q18 | 28회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Telnet/FTP 평문 서비스, 배너 정보 노출, root 직접 로그인 차단은 서비스 취약 설정 보완이다. | high | Naver 답안 기준으로 취약점과 대응 보강 |
| R29-Q1 | 29회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | PAM account/auth/session type은 Linux 인증·계정·세션 체계 지식이다. | high | Naver 답안 순서 기준으로 보강 |
| R29-Q2 | 29회 | 2 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | NTFS는 Windows 권한과 대용량 파일 지원 파일시스템이다. | high | Windows 보안특성 |
| R29-Q3 | 29회 | 3 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-E2EE-GLOSSARY | 종단 간 암호화는 네트워크를 통과하는 데이터 암호화 개념이며 라우팅 정보 노출 가능성까지 포함해 NIST CSRC glossary로 보조 검증 가능하다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R29-Q4 | 29회 | 4 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NIST-DLP-GLOSSARY | DLP는 endpoint actions와 network actions를 포함해 data in use/in motion/at rest를 보호하는 체계이므로 PC 에이전트와 네트워크 센서 설명에 직접 연결된다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R29-Q5 | 29회 | 5 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 버퍼 오버플로우와 `strcpy()`는 메모리 안전 취약점이다. | high | 기존 분류는 관리/법규이나 취약점 보완 연결이 더 강함 |
| R29-Q6 | 29회 | 6 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `/etc/shadow`는 Linux 패스워드 해시 보호 파일이다. | high | 계정/인증 파일 |
| R29-Q7 | 29회 | 7 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | DNS는 UDP 또는 TCP를 사용하며 캐시와 TTL은 질의 부하 완화와 유지 기간 개념이다. | high | Naver 답안 기준으로 UDP/TCP 보강 |
| R29-Q8 | 29회 | 8 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 웹셸은 파일 업로드와 웹 서버 실행 조건에 의해 악용된다. | high | 위험한 형식 파일 업로드 항목과 연결 |
| R29-Q9 | 29회 | 9 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 기준선·상세·복합 접근법은 위험분석 방법론이다. | high | 위험분석 접근법 |
| R29-Q10 | 29회 | 10 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-LAW-NETWORK-ACT | 정보통신망 정의는 정보통신망법 현행 법령 페이지로 보조 검증 가능한 법적 준거성·정보자산 범위 식별 항목이다. | high | 국가법령정보센터 현행 법령 페이지 확인, 조문별 raw/source 저장은 미수행 |
| R29-Q11 | 29회 | 11 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Apache `Options Indexes` 제거는 웹 서버 디렉터리 리스팅 방지 설정이다. | high | WEB/WAS 설정 점검 |
| R29-Q12 | 29회 | 12 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-GNU-ACCOUNTING-UTILITIES | `lastcomm`은 process accounting의 `acct` 기록에서 실행 명령을 나열하는 도구이며 GNU Accounting Utilities manual로 보조 검증 가능하다. | high | GNU manual 공식 페이지 확인, accounting 활성화 조건 주의 |
| R29-Q13 | 29회 | 13 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-OWASP-MOBILE-TOP-10 | 인증서 고정은 TLS/모바일 통신에서 MITM 완화 목적으로 쓰이며 OWASP Mobile Top 10의 insecure communication·binary protection 계열과 보조 연결된다. | high | OWASP Mobile 공식 보조 원천 확인 |
| R29-Q14 | 29회 | 14 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 파일 업로드 우회와 웹셸 실행 조건은 웹 서비스 취약점 보완 주제다. | high | 업로드 파일 검증 항목과 연결 |
| R29-Q15 | 29회 | 15 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 에이전트·정보수집 서버·통합관제 시스템은 보안관제 구성요소다. | high | 정보수집 및 모니터링 직접 연결 |
| R29-Q16 | 29회 | 16 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 위험 수용·감소·전가·회피는 위험 처리 전략이다. | high | ISMS-P 위험관리 연결 |
| R29-Q17 | 29회 | 17 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Windows 이벤트 로그 최대 크기 설정은 로그 보존·운영체제 보안설정이다. | high | 이벤트 로그 점검 |
| R29-Q18 | 29회 | 18 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-LAW-PIPA | CCTV 설치 조치는 개인정보 보호법의 영상정보처리기기·개인정보 처리 법적 근거 검토와 직접 연결된다. | high | 국가법령정보센터 현행 법령 페이지 확인, 조문별 raw/source 저장은 미수행 |
| R30-Q1 | 30회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `/etc/shadow` hash id는 Linux 계정 인증 저장 형식이다. | high | 계정 파일 보안 |
| R30-Q2 | 30회 | 2 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IPsec AH sequence number는 재생 공격 방지에 쓰인다. | high | IPSec 키워드 직접 연결 |
| R30-Q3 | 30회 | 3 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `net session /delete`는 Windows 원격 세션 관리 명령이다. | high | Windows 관리 명령 |
| R30-Q4 | 30회 | 4 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | LAN 스위치 프레임 전송 방식은 네트워크 장비 특성이다. | high | Switch 키워드 연결 |
| R30-Q5 | 30회 | 5 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 델파이 기법은 정성적 위험분석·전문가 합의 기법이다. | high | 위험분석 방법 |
| R30-Q6 | 30회 | 6 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 디지털 포렌식은 침해 증거 수집·보존·분석 절차다. | high | 침입 원인 분석과 대응 |
| R30-Q7 | 30회 | 7 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 물리적·논리적 접근통제는 자산 보호대책 유형이다. | high | ISMS-P 접근통제 연결 |
| R30-Q8 | 30회 | 8 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-OWASP-CREDENTIAL-STUFFING | 유출 자격증명 악용은 탈취된 username/password 쌍을 자동 주입해 계정 접근을 시도하는 credential stuffing과 직접 연결된다. | high | OWASP community attack page 공식 확인, source answer와 엄밀한 용어 차이 주의 |
| R30-Q9 | 30회 | 9 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-NVD-CVE-DETAILS; REF-CWE-TOP-25; REF-NIST-ZERO-DAY-GLOSSARY | 제로데이는 이전에 알려지지 않은 취약점을 악용하는 공격 개념이며 NIST CSRC zero day attack glossary로 전용 보조 검증 가능하다. | high | NIST CSRC glossary 공식 페이지 확인 |
| R30-Q10 | 30회 | 10 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `net share`는 Windows 공유 목록·생성·삭제 명령이다. | high | Windows 공유 관리 |
| R30-Q11 | 30회 | 11 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PRIVACY-SAFETY-MEASURES | DB 개인정보 마스킹은 개인정보처리시스템/DB 보호조치와 연결된다. | medium | 패턴 기반 마스킹·SQL 파싱 기반 마스킹 방식명과 직접 대응하는 공식 원천을 아직 고정하지 않아 보수적 유지 |
| R30-Q12 | 30회 | 12 | 정보자산 위협 및 취약점 분석 정리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산 분석과 취약성 분석은 위험분석 기본 단계다. | high | 위험분석 직접 연결 |
| R30-Q13 | 30회 | 13 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE; REF-OWASP-MOBILE-TOP-10; REF-NIST-MOBILE-DEVICE-SECURITY | MDM·컨테이너화·모바일 가상화는 BYOD/enterprise mobile device lifecycle에서 단말 관리와 격리·보호 전략을 다루는 모바일 보안 기술이며 NIST SP 800-124 Rev. 2의 centralized device management와 enterprise mobility 범위로 보조 검증 가능하다. | high | NIST SP 800-124 Rev. 2 공식 페이지 확인 |
| R30-Q14 | 30회 | 14 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산·위협·취약성 관계는 위험 산정의 기본 모델이다. | high | 위험분석 직접 연결 |
| R30-Q15 | 30회 | 15 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | EAM/IAM은 계정·권한 수명주기와 접근권한 관리 체계다. | medium | ISMS-P 접근권한 관리와는 연결되지만 EAM/IAM 차이 설명은 벤더 용어 차이가 있어 보수적 유지 |
| R30-Q16 | 30회 | 16 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Snort 탐지 룰 조건 정의는 IDS 운영 정확도와 연결된다. | high | IDS/IPS 키워드 직접 연결 |
| R30-Q17 | 30회 | 17 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | TMOUT, securetty, passwd/shadow 권한, world-writable, umask, xinetd는 Linux 보안설정 점검 항목이다. | high | 운영체제 취약점 보완 |
| R30-Q18 | 30회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SQL Injection은 DB 조회 쿼리 입력값 조작 취약점이다. | high | 시큐어코딩 가이드 SQL 삽입 항목과 직접 연결 |

## Coverage

| range | mapped_items | high | medium | low |
|---|---:|---:|---:|---:|
| 23회 | 18 | 18 | 0 | 0 |
| 24회 | 18 | 17 | 1 | 0 |
| 25회 | 18 | 18 | 0 | 0 |
| 26회 | 18 | 18 | 0 | 0 |
| 27회 | 18 | 18 | 0 | 0 |
| 28회 | 18 | 17 | 1 | 0 |
| 29회 | 18 | 18 | 0 | 0 |
| 30회 | 18 | 16 | 2 | 0 |
| 합계 | 144 | 140 | 4 | 0 |

## Follow-Up
- 23~27회는 Naver 블로그 기반으로 회차별 복원 문항을 보강하고 같은 스키마로 확장했다. 28~29회도 Naver 카테고리에서 회차별 분석 글이 확인되었고, 30회는 기존 wiki 복원본 기준이다. 공식 PDF 직접 대조는 아직 미검증이다.
- 2026-07-03 1차 보강에서 CVE/NVD/CWE/CVSS/MITRE ATT&CK, OWASP Top 10 Web, OWASP Mobile Top 10 공식 페이지 확인으로 6개 medium 행을 high로 승격했다.
- 2026-07-03 2차 보강에서 IETF RFC, CWE-444, NIST CSRC glossary/SP, GNU manual, OWASP credential stuffing, 국가법령정보센터 현행 법령 페이지 확인으로 16개 medium 행을 high로 승격했다.
- 기존 패칭 원천 재검토에서 PIPC 개인정보 안전성 확보조치 기준 안내서의 `랜덤 라운딩` 직접 근거를 확인해 1개 medium 행을 high로 승격했다.
- 남은 4개 medium 행은 무선랜 세부 표준, Cyber Kill Chain 전용 원천, DB 마스킹 방식명, EAM/IAM 벤더 용어 차이에 대한 직접 공식 원천이 더 필요하므로 보수적으로 유지한다.
