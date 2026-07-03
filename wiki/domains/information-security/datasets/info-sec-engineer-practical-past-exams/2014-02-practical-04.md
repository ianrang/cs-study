---
title: "정보보안기사 실기 4회 2014년 2회 실기 복원"
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
  - "https://information-security.tistory.com/290"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 4회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 4회 2014년 2회 실기 복원

## Scope
- Exam mapping: 2014년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 다음은 CVE 취약점 표기 방식이다. 각 항목의 의미를 쓰시오. | (1) 해당 취약점이 발견된 연도 (2) 해당 연도에 부여된 취약점 고유 번호 | source-derived from Information Security Tistory; answer block present |
| 2 | short | 다음은 OWASP Top 10의 취약점 설명이다. 각각의 취약점 명칭을 쓰시오. | (1) Injection(인젝션) (2) XSS(Cross Site Script) (3) CSRF(Cross Site Request Forgery) | source-derived from Information Security Tistory; answer block present |
| 3 | essay | 개인정보보호법 제17조에 따라 개인정보를 제3자에게 제공할 때 정보주체에게 알려야 하는 사항 5가지를 쓰시오. | (1) 개인정보를 제공받는 자 (2) 개인정보를 제공받는 자의 개인정보 이용 목적 (3) 제공하는 개인정보의 항목 (4) 개인정보를 제공받는 자의 개인정보 보유 및 이용 기간 (5) 동의를 거부할 권리가 있다는 사실 및 동의 거부에 따른 불이익이 있는 경우 그 불이익의 내용 | source-derived from Information Security Tistory; answer block present |
| 4 | essay | 위험 분석 및 위험 평가 접근법에 관한 설명이다. 빈칸 (A), (B), (C), (D)를 채우시오. | A : 베이스라인 접근법 B : 비정형화된 접근법 C : 상세 위험 분석 D : 복합 접근법 | source-derived from Information Security Tistory; answer block present |
| 5 | short | 위험 관리 관련 용어에 관한 설명이다. 빈칸 (A), (B), (C), (D)를 채우시오. | A : 위험관리 B : 위험분석 C : 위험평가 D : 위험대응 | source-derived from Information Security Tistory; answer block present |
| 6 | short | 다음에서 설명하는 도구의 명칭을 쓰시오. | 프록시(Proxy) | source-derived from Information Security Tistory; answer block present |
| 7 | short | 다음에서 설명하는 보안 용어를 각각 쓰시오. | A : IDS(침입탐지 시스템) B : False Negative(미탐) C : False Positive(오탐) | source-derived from Information Security Tistory; answer block present |
| 8 | short | 다음 5가지 스캔 방법 중 포트가 닫혀 있을 때만 응답이 오는 스캔 방식을 모두 고르시오. | FIN Scan, Xmas Scan, NULL Scan | source-derived from Information Security Tistory; answer block present |
| 9 | essay | Telnet을 이용하여 웹 서버의 지원 HTTP 메소드를 확인하기 위한 명령어를 작성하시오. | telnet hostname 80 OPTIONS / HTTP/1.1 Host: hostname | source-derived from Information Security Tistory; answer block present |
| 10 | essay | 다음 C 코드의 보안 취약점을 설명하고 안전한 코드로 수정하시오. | 취약점 : 8바이트 크기로 선언한 buff 변수에 strcpy()를 통해 입력값 크기 검증 없이 복사를 수행하므로 버퍼 오버플로우가 발생할 수 있다. 수정 방법 : strcpy() 대신 복사할 크기를 명시하는 strncpy() 또는 안전한 함수인 strcpy_s()를 사용하여 버퍼 크기를 초과하지 않도록 한다. strncpy(buff, argv[1], sizeof(buff) - 1); buff[sizeof(buff) - 1] = '\0'; | source-derived from Information Security Tistory; answer block present |
| 11 | essay | VPN 구성에 사용하는 프로토콜에 관한 물음에 답하시오. | A : PPTP, L2TP, L2F B : IPSec C : 전송 모드(Transport Mode) : End-to-End 방식으로 호스트 간 종단 통신에서 IP 페이로드(데이터)만 암호화하여 보호한다. 터널 모드(Tunnel Mode) : Gateway-to-Gateway 방식으로 라우터 간 통신에서 IP 헤더와 IP 페이로드 전체를 암호화하여 보호한다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 다음 웹 서버 접근 로그에서 나타나는 공격에 관한 물음에 답하시오. | (1) Blind SQL Injection 공격 (2) 일반적인 SQL Injection과 달리 서버의 오류 메시지나 직접적인 쿼리 결과가 화면에 표시되지 않는 경우에도, 참(True)/거짓(False)에 따른 서버 응답 차이를 이용하여 데이터베이스에 저장된 값을 한 문자씩 추정하는 기법이다. (3) id가 1인 사용자의 password 컬럼 값에 대해 substr() 함수를 이용하여 1번째 문자부터 순차적으로 한 문자씩 비교를 수행하여 패스워드 값을 추출한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 개인정보보호법에 따른 개인정보 안전성 확보 조치 방안을 기술적·관리적·물리적 관점에서 6가지를 서술하시오. | (1) 개인정보의 안전한 처리를 위한 내부 관리계획의 수립·시행 → 관리적 관점 (2) 개인정보에 대한 접근 통제 및 접근 권한의 제한 조치 → 기술적·물리적 관점 (3) 개인정보를 안전하게 저장·전송할 수 있는 암호화 기술의 적용 → 기술적 관점 (4) 개인정보 침해사고 대응을 위한 접속 기록의 보관 및 위·변조 방지 조치 → 관리적·기술적 관점 (5) 개인정보에 대한 보안 프로그램의 설치 및 갱신 → 기술적 관점 (6) 개인정보의 안전한 보관을 위한 보관 시설의 마련 또는 잠금장치 설치 등 물리적 조치 → 물리적 관점 | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음 Snort PCRE 룰의 문제점과 해결 방안을 서술하시오. | (1) 문제점 : 룰의 목적지 주소 및 포트가 any any로 설정되어 있어 모든 주소와 포트를 목적지로 하는 패킷을 검사하게 된다. 이로 인해 불필요한 패킷까지 모두 검사하여 보안 장비에 과도한 부하가 발생한다. (2) 해결 방안 : 목적지 주소를 웹 서버 IP 주소로, 목적지 포트를 80번(HTTP)으로 명시하여 불필요한 패킷 검사를 줄이고 부하를 감소시킨다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | WPA 크래킹 과정에 관한 물음에 답하시오. | (1) 공격 대상 AP(무선 공유기)의 MAC 주소 (2) 공격 대상 AP에 연결된 클라이언트의 MAC 주소를 지정하는 옵션 (3) 사전(Dictionary) 공격을 위해 미리 정의된 패스워드 목록이 기록된 파일 (4) 공격 대상 AP의 MAC 주소를 이용하여 해당 AP와 클라이언트 간의 4-Way Handshake 패킷을 캡처하고, 사전 파일과 비교하여 WPA 패스워드를 크래킹하는 것이다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음 상황을 참고하여 위험 분석 관련 수치를 계산하시오. | (1) 자산 가치(AV) : 40억 원 (2) 노출 계수(EF) : 30%(0.3) (3) 단일 손실 예상액(SLE) : 40억 × 0.3 = 12억 원 (4) 연간 발생률(ARO) : 0.2 (5년에 1회 = 1/5) (5) 연간 예상 손실액(ALE) : 12억 × 0.2 = 2.4억 원 (6) 소방 방재 시설 설치 → 위험 감소(위험 완화) / 화재 보험 가입 → 위험 전가(위험 전이) | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
