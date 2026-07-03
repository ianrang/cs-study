---
title: "정보보안기사 실기 11회 2018년 1회 실기 복원"
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
  - "https://information-security.tistory.com/270"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 11회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 11회 2018년 1회 실기 복원

## Scope
- Exam mapping: 2018년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Windows에서 하나 이상의 볼륨을 암호화하고, TPM을 사용해 초기 시작 구성 요소의 무결성을 검사하는 암호화 기능의 명칭을 쓰시오. | BitLocker | source-derived from Information Security Tistory; answer block present |
| 2 | short | 데이터베이스 보안 접근 통제 방법에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 접근 통제 B : 추론 통제 C : 흐름 통제 | source-derived from Information Security Tistory; answer block present |
| 3 | short | VPN에서 사용되는 보안 프로토콜에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : IPSec B : AH(Authentication Header) C : ESP(Encapsulating Security Payload) | source-derived from Information Security Tistory; answer block present |
| 4 | essay | DNS 서버(192.168.1.18)의 named.conf에 2차 DNS 서버(192.168.10.3)의 Zone Transfer를 허용하는 설정을 작성하시오. | allow-transfer { 192.168.10.3; }; | source-derived from Information Security Tistory; answer block present |
| 5 | short | HTTP 헤더의 CRLF 필드를 조작해 조작된 HTTP 헤더를 지속적으로 전송하고 연결을 장시간 유지하여 서비스 가용성을 저하시키는 공격의 명칭을 쓰시오. | Slow HTTP Header DoS(Slowloris) | source-derived from Information Security Tistory; answer block present |
| 6 | short | 개인정보보호법에 따른 영상정보처리기기 설치 시 안내문에 포함해야 하는 사항이다. 빈칸 (A)를 채우시오. | A : 설치 장소 및 목적 | source-derived from Information Security Tistory; answer block present |
| 7 | short | SNMP(Simple Network Management Protocol)에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 161 B : 이벤트 리포팅(Event Reporting) C : 162 | source-derived from Information Security Tistory; answer block present |
| 8 | short | 정보통신망 이용촉진 및 정보보호 등에 관한 법률에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 5 B : 1 C : 6 | source-derived from Information Security Tistory; answer block present |
| 9 | essay | 위험 분석 관련 계산식이다. 빈칸 (A), (B)를 채우시오. | A : EF(노출 계수, Exposure Factor) B : ARO(연간 발생률, Annual Rate of Occurrence) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 공격자가 소프트웨어 빌드 단계 관련 서버를 침해한 뒤 악성코드를 삽입해, 개발사의 제품 패키징 과정에서 정상 파일에 악성 모듈이 포함되어 배포되도록 하는 공격의 명칭을 쓰시오. | 공급망 공격(Supply Chain Attack) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 다음 포트 스캔 과정을 분석하여 물음에 답하시오. | (1) TCP Half-Open Scan(TCP SYN 스캔) (2) 25번 : SMTP, 443번 : HTTPS, 110번 : POP3 (3) 가) B가 SYN/ACK를 응답하였으므로 25번 포트는 열려 있는 상태이다. A가 RST를 전송하여 연결을 완성하지 않는 스텔스 스캔 기법이다. 나) B가 RST를 응답하였으므로 443번 포트는 닫혀 있는 상태이다. 다) 응답이 없으므로 110번 포트는 방화벽 등에 의해 차단된 상태이다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 쇼핑몰 개인정보취급자에게 적용해야 하는 비밀번호 작성 규칙 3가지를 서술하시오. | (1) 영문·숫자·특수문자 중 2종류 이상을 조합하여 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 구성한다. (2) 연속적인 숫자, 생년월일, 전화번호 등 추측하기 쉬운 개인정보 및 아이디와 유사한 비밀번호는 사용하지 않도록 권고한다. (3) 비밀번호에 유효기간을 설정하여 반기별 1회 이상 변경한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 다음 여행사 개인정보 이용 약관 동의서에서 정보보안 법규에 어긋나는 부분 3가지를 찾아 서술하시오. | (1) 이벤트 업체에 개인정보를 제공하는 것은 제3자 제공에 해당하므로 별도의 동의를 받아야 하며, 제공 항목·목적·기간 등을 별도로 안내해야 한다. (2) 멤버십 등록 목적으로 주민등록번호를 수집하는 것은 법적 근거가 없는 과도한 수집이며, 정당한 근거가 있더라도 별도 동의를 받아야 한다. (3) 동의 거부 권리를 안내할 때 동의 거부에 따른 불이익도 함께 안내해야 한다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음 Blind SQL Injection 공격에 관한 물음에 답하시오. | (1) Blind SQL Injection (2) 데이터베이스 명을 파악할 수 있다. 위 공격을 통해 데이터베이스 첫 글자가 't'임을 확인할 수 있으며, 유사한 공격을 반복하여 전체 데이터베이스 이름을 알아낼 수 있다. (3) HTML 수정으로 특정 출력 필드를 숨기더라도 SQL Injection이 동작하는 한 다른 페이지에도 동일한 공격이 가능하며, 출력이 차단되더라도 악의적인 쿼리가 내부적으로 실행되는 것은 막을 수 없다. HTML 수정이 아닌 Prepared Statement(준비된 구문)를 이용하여 SQL Injection 공격을 원천 차단해야 한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음 조건에 맞는 Snort 룰을 작성하시오. | alert tcp any any -> any 23 (msg:"Dangerous"; content:"anonymous"; depth:14;) | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
