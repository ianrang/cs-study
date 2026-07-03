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
  - "2025-01-practical-28.md"
  - "2025-02-practical-29.md"
  - "2025-04-practical-30.md"
source_count: 6
provenance: inferred
summary: "최근 28~30회 정보보안기사 실기 복원 문항을 KCA 실기 출제기준 세부항목과 패칭된 참고문서 ref_id에 연결한 1차 매핑."
evergreen: false
---

# 정보보안기사 실기 문항-출제기준-참고문서 매핑

## Scope
- 이 문서는 문항별 근거 연결의 SSOT이다.
- 현재 범위는 고신뢰 최근 회차인 28회, 29회, 30회 54개 문항이다.
- 문항 원문 전체는 회차별 복원 문서가 SSOT이므로 이 문서에는 반복하지 않는다.
- `REF-KCA-INFOSEC-PRACTICAL-CRITERIA`는 모든 행의 1차 기준이다. 다른 ref_id는 보조 참고문서로만 연결하며, `KCA가 해당 문서를 참고했다`고 단정하지 않는다.

## Mapping

| item_id | round | no | criteria_detail | reference_ids | evidence | confidence | notes |
|---|---|---:|---|---|---|---|---|
| R28-Q1 | 28회 | 1 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Smurf는 ICMP/브로드캐스트 기반 DoS 유형이다. | high | DoS/DDoS 키워드와 직접 연결 |
| R28-Q2 | 28회 | 2 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SSRF는 웹 요청이 내부망 자원 접근으로 이어지는 입력 검증 계열 취약점이다. | high | 시큐어코딩 가이드 구현단계 보안약점의 SSRF 항목과 연결 |
| R28-Q3 | 28회 | 3 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | VLAN 할당 방식과 Cisco 확인 명령은 네트워크 장비 보안 운영 지식이다. | high | 기반시설 상세가이드의 네트워크 장비 점검과도 연결 가능 |
| R28-Q4 | 28회 | 4 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | HttpOnly는 XSS 상황에서 쿠키 접근을 제한하는 웹 보안 설정이다. | high | 기존 분류는 네트워크 보안이지만 어플리케이션 보안 연결이 더 강함 |
| R28-Q5 | 28회 | 5 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | HTTP 헤더 인젝션은 CR/LF로 응답 헤더 경계를 조작한다. | high | HTTP 응답분할/헤더 처리 취약점과 연결 |
| R28-Q6 | 28회 | 6 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 사이버 킬 체인은 APT 침해 분석 단계 모델이다. | medium | KCA 세부항목 직접 키워드는 아니나 침해 원인 분석 축과 연결 |
| R28-Q7 | 28회 | 7 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `lsof`는 Linux 열린 파일과 프로세스 상태 확인 명령이다. | high | 운영체제 점검 명령 |
| R28-Q8 | 28회 | 8 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `lastb`는 Linux 로그인 실패 기록 확인 명령이다. | high | 인증 로그 점검 |
| R28-Q9 | 28회 | 9 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 정보자산 중요도 산정은 CIA 기준으로 자산을 식별·분류한다. | high | 위험분석 수행준거와 직접 연결 |
| R28-Q10 | 28회 | 10 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 위험관리계획은 위험분석 범위·방법·대응 활동을 정한다. | high | 위험분석 계획 수립 |
| R28-Q11 | 28회 | 11 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 보호구역·출입권한·접근통제는 ISMS-P 물리보안 보호대책이다. | high | ISMS-P 인증기준 안내서 연결 |
| R28-Q12 | 28회 | 12 | 서비스별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Deep link는 모바일 앱 기능 이동 기술이다. | medium | 모바일 앱 보안 범위와 연결 |
| R28-Q13 | 28회 | 13 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | Shell은 사용자 명령 해석과 커널 전달을 담당한다. | high | 운영체제 기본 보안특성 |
| R28-Q14 | 28회 | 14 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IPsec의 모드와 AH/ESP는 프로토콜별 보안특성이다. | high | KCA 대표 키워드에 IPSec 명시 |
| R28-Q15 | 28회 | 15 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산 중요도 산정은 보호 대상 식별과 관리 우선순위 산정이다. | high | CIA 기준 연결 |
| R28-Q16 | 28회 | 16 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | NetBIOS over TCP/IP 비활성화는 Windows 서비스 노출 완화 설정이다. | high | 기존 분류는 관리/법규이나 OS 보안설정 연결이 더 강함 |
| R28-Q17 | 28회 | 17 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Oracle DB 권한·감사·암호화는 DB 서비스 보안설정 점검 주제다. | high | DBMS 점검 항목과 연결 |
| R28-Q18 | 28회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Telnet/FTP 평문 서비스 전환은 서비스 취약 설정 보완이다. | high | 기존 분류는 관리/법규이나 서비스 보안 연결이 더 강함 |
| R29-Q1 | 29회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | PAM 모듈 type은 Linux 인증 체계 지식이다. | high | 인증 보안특성 |
| R29-Q2 | 29회 | 2 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | NTFS는 Windows 권한과 대용량 파일 지원 파일시스템이다. | high | Windows 보안특성 |
| R29-Q3 | 29회 | 3 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 종단 간 암호화는 송수신자 사이 통신 보호 개념이다. | medium | 암호 통신 일반 개념 |
| R29-Q4 | 29회 | 4 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | DLP는 PC 에이전트와 네트워크 센서로 정보 유출을 탐지한다. | medium | 보안관제/솔루션 운영 축 |
| R29-Q5 | 29회 | 5 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 버퍼 오버플로우와 `strcpy()`는 메모리 안전 취약점이다. | high | 기존 분류는 관리/법규이나 취약점 보완 연결이 더 강함 |
| R29-Q6 | 29회 | 6 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `/etc/shadow`는 Linux 패스워드 해시 보호 파일이다. | high | 계정/인증 파일 |
| R29-Q7 | 29회 | 7 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | DNS UDP, 캐싱, TTL은 프로토콜 동작 특성이다. | high | DNS 키워드 직접 연결 |
| R29-Q8 | 29회 | 8 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 웹셸은 파일 업로드와 웹 서버 실행 조건에 의해 악용된다. | high | 위험한 형식 파일 업로드 항목과 연결 |
| R29-Q9 | 29회 | 9 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 기준선·상세·복합 접근법은 위험분석 방법론이다. | high | 위험분석 접근법 |
| R29-Q10 | 29회 | 10 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 정보통신망 정의는 법적 준거성·정보자산 범위 식별에 쓰인다. | medium | 최신 법령 확인 필요 |
| R29-Q11 | 29회 | 11 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Apache `Options Indexes` 제거는 웹 서버 디렉터리 리스팅 방지 설정이다. | high | WEB/WAS 설정 점검 |
| R29-Q12 | 29회 | 12 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `lastcomm`은 Linux process accounting 기반 명령 이력 확인이다. | medium | accounting 활성화 조건 주의 |
| R29-Q13 | 29회 | 13 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 인증서 고정은 TLS/모바일 통신에서 MITM 완화 목적으로 쓰인다. | medium | 모바일 구현 세부는 별도 원천 보강 가능 |
| R29-Q14 | 29회 | 14 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | 파일 업로드 우회와 웹셸 실행 조건은 웹 서비스 취약점 보완 주제다. | high | 업로드 파일 검증 항목과 연결 |
| R29-Q15 | 29회 | 15 | 정보수집 및 모니터링 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 에이전트·정보수집 서버·통합관제 시스템은 보안관제 구성요소다. | high | 정보수집 및 모니터링 직접 연결 |
| R29-Q16 | 29회 | 16 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 위험 수용·감소·전가·회피는 위험 처리 전략이다. | high | ISMS-P 위험관리 연결 |
| R29-Q17 | 29회 | 17 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Windows 이벤트 로그 최대 크기 설정은 로그 보존·운영체제 보안설정이다. | high | 이벤트 로그 점검 |
| R29-Q18 | 29회 | 18 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | CCTV 설치 조치는 개인정보 법적 준거성 검토가 필요하다. | medium | 최신 개인정보보호법 조문 확인 필요 |
| R30-Q1 | 30회 | 1 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | `/etc/shadow` hash id는 Linux 계정 인증 저장 형식이다. | high | 계정 파일 보안 |
| R30-Q2 | 30회 | 2 | 프로토콜별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | IPsec AH sequence number는 재생 공격 방지에 쓰인다. | high | IPSec 키워드 직접 연결 |
| R30-Q3 | 30회 | 3 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `net session /delete`는 Windows 원격 세션 관리 명령이다. | high | Windows 관리 명령 |
| R30-Q4 | 30회 | 4 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | LAN 스위치 프레임 전송 방식은 네트워크 장비 특성이다. | high | Switch 키워드 연결 |
| R30-Q5 | 30회 | 5 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 델파이 기법은 정성적 위험분석·전문가 합의 기법이다. | high | 위험분석 방법 |
| R30-Q6 | 30회 | 6 | 로그분석 및 대응 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 디지털 포렌식은 침해 증거 수집·보존·분석 절차다. | high | 침입 원인 분석과 대응 |
| R30-Q7 | 30회 | 7 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | 물리적·논리적 접근통제는 자산 보호대책 유형이다. | high | ISMS-P 접근통제 연결 |
| R30-Q8 | 30회 | 8 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 유출 자격증명 악용은 계정 보안과 인증 취약점 점검 주제다. | medium | source answer와 엄밀한 용어 차이 주의 |
| R30-Q9 | 30회 | 9 | 취약점 점검이력과 보완내용 관리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 제로데이는 공개 전 또는 패치 전 취약점 악용 개념이다. | medium | CVE/CWE 원천 패칭 후 보강 후보 |
| R30-Q10 | 30회 | 10 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | `net share`는 Windows 공유 목록·생성·삭제 명령이다. | high | Windows 공유 관리 |
| R30-Q11 | 30회 | 11 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-PRIVACY-SAFETY-MEASURES | DB 개인정보 마스킹은 개인정보처리시스템/DB 보호조치와 연결된다. | medium | 마스킹 세부 원천 보강 가능 |
| R30-Q12 | 30회 | 12 | 정보자산 위협 및 취약점 분석 정리 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산 분석과 취약성 분석은 위험분석 기본 단계다. | high | 위험분석 직접 연결 |
| R30-Q13 | 30회 | 13 | 운영체제별 보안특성 파악 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | MDM·컨테이너화·모바일 가상화는 모바일 오피스 단말 보안 기술이다. | medium | 모바일 보안 세부 원천 보강 가능 |
| R30-Q14 | 30회 | 14 | 위험평가 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 자산·위협·취약성 관계는 위험 산정의 기본 모델이다. | high | 위험분석 직접 연결 |
| R30-Q15 | 30회 | 15 | IT 자산 위협 분석 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-ISMSP-CRITERIA-GUIDE | EAM/IAM은 계정·권한 수명주기와 접근권한 관리 체계다. | medium | 벤더 용어 차이 주의 |
| R30-Q16 | 30회 | 16 | 보안장비 및 네트워크 장비별 보안특성 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | Snort 탐지 룰 조건 정의는 IDS 운영 정확도와 연결된다. | high | IDS/IPS 키워드 직접 연결 |
| R30-Q17 | 30회 | 17 | 운영체제 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-CIIP-VULN-ASSESSMENT-GUIDE | TMOUT, securetty, passwd/shadow 권한, world-writable, umask, xinetd는 Linux 보안설정 점검 항목이다. | high | 운영체제 취약점 보완 |
| R30-Q18 | 30회 | 18 | 서비스 보안설정 점검과 보완 | REF-KCA-INFOSEC-PRACTICAL-CRITERIA; REF-SECURE-CODING-GUIDE | SQL Injection은 DB 조회 쿼리 입력값 조작 취약점이다. | high | 시큐어코딩 가이드 SQL 삽입 항목과 직접 연결 |

## Coverage

| range | mapped_items | high | medium | low |
|---|---:|---:|---:|---:|
| 28회 | 18 | 16 | 2 | 0 |
| 29회 | 18 | 13 | 5 | 0 |
| 30회 | 18 | 13 | 5 | 0 |

## Follow-Up
- 23~27회는 최근 회차이지만 cross-verify finding이 남아 있으므로 분류 정정 후 같은 스키마로 확장한다.
- CVE/CWE/CVSS/MITRE, OWASP Top 10, 모바일 보안 세부 원천은 medium confidence 행 보강 후보로 둔다.
