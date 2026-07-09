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
date_updated: 2026-07-06
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
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Windows에서 하나 이상의 볼륨을 암호화하고, TPM을 사용해 초기 시작 구성 요소의 무결성을 검사하는 암호화 기능의 명칭을 쓰시오. | BitLocker | source-derived from Information Security Tistory; answer block present |
| 2 | short | 데이터베이스 보안 접근 통제 방법의 빈칸을 채우시오. (A): 인증된 사용자에게 허가된 범위 내에서 시스템 내부 정보 접근을 허용하는 기술적 방법. (B): 사용자가 찾는 통계 함수 관계를 통해 키 값을 유도하는 것으로 간접 접근을 통한 추론과 상관 데이터로 정보를 찾는 것을 통제하는 방법. (C): 보안 등급이 높은 객체에서 낮은 객체로의 정보 흐름을 제어하는 방법. | A : 접근 통제 B : 추론 통제 C : 흐름 통제 | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 3 | short | VPN 보안 프로토콜의 빈칸을 채우시오. (A): 3계층 보안 프로토콜로 VPN에서 가장 많이 사용되는 프로토콜. (B): (A)에서 데이터 무결성 보장과 메시지 인증을 위한 세부 프로토콜. (C): (A)에서 암호화를 통해 기밀성을 유지하기 위한 세부 프로토콜. | A : IPSec B : AH(Authentication Header) C : ESP(Encapsulating Security Payload) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 4 | essay | DNS 서버 `192.168.1.18`의 `named.conf`에서 2차 DNS 서버 `192.168.10.3`의 Zone Transfer를 허용하도록 `options { directory "/var/named"; forward only; forwarders { 8.8.8.8; }; datasize 1024M; (빈칸); };`의 빈칸 설정을 작성하시오. | allow-transfer { 192.168.10.3; }; | source-derived from Information Security Tistory; config context restored |
| 5 | short | HTTP 헤더의 CRLF 필드를 조작해 조작된 HTTP 헤더를 지속적으로 전송하고 연결을 장시간 유지하여 서비스 가용성을 저하시키는 공격의 명칭을 쓰시오. | Slow HTTP Header DoS(Slowloris) | source-derived from Information Security Tistory; answer block present |
| 6 | short | 개인정보보호법에 따른 영상정보처리기기 설치 시 안내문에 포함해야 하는 사항이다. 빈칸 (A)를 채우시오. | A : 설치 장소 및 목적 | source-derived from Information Security Tistory; answer block present |
| 7 | short | SNMP 설명의 빈칸을 채우시오. (1) 매니저가 에이전트로 Request하는 포트 번호: UDP (A). (2) 에이전트가 매니저로 주기적으로 보고하는 과정: (B). (3) 에이전트가 매니저로 보고하는 포트 번호: UDP (C). | A : 161 B : 이벤트 리포팅(Event Reporting) C : 162 | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 8 | short | 개인정보의 안전성 확보조치 기준 제5조 접근 권한의 관리 및 접속기록 보관·점검 기준의 빈칸을 채우시오. 접근권한 부여·말소 등의 기록을 최소 (A)년간 보관하고, 접속기록의 위·변조·훼손 대응을 위해 월 (B)회 이상 점검하며, 개인정보처리시스템 접속기록을 최소 (C)년 이상 보관해야 한다. | A : 3 B : 1 C : 1 | source-derived from Information Security Tistory; PDF compilation cross-check corrected 2026-07-06 |
| 9 | essay | 위험 분석 계산식 `SLE = AV × (A)`, `ALE = SLE × (B)`의 빈칸을 채우시오. | A : EF(노출 계수, Exposure Factor) B : ARO(연간 발생률, Annual Rate of Occurrence) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 10 | short | 공격자가 소프트웨어 빌드 단계 관련 서버를 침해한 뒤 악성코드를 삽입해, 개발사의 제품 패키징 과정에서 정상 파일에 악성 모듈이 포함되어 배포되도록 하는 공격의 명칭을 쓰시오. | 공급망 공격(Supply Chain Attack) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 포트 스캔 과정을 분석하여 답하시오. 가) `A -> (TCP 25) SYN -> B`, `A <- (TCP 25) SYN/ACK <- B`, `A -> (TCP 25) RST -> B`. 나) `A -> (TCP 443) SYN -> B`, `A <- (TCP 443) RST <- B`. 다) `A -> (TCP 110) SYN -> B`, 응답 없음. (1) 포트 스캔 방식, (2) 각 포트의 서비스명, (3) 각 포트 스캔 결과와 근거를 서술하시오. | (1) TCP Half-Open Scan(TCP SYN 스캔) (2) 25번 : SMTP, 443번 : HTTPS, 110번 : POP3 (3) 가) B가 SYN/ACK를 응답하였으므로 25번 포트는 열려 있는 상태이다. A가 RST를 전송하여 연결을 완성하지 않는 스텔스 스캔 기법이다. 나) B가 RST를 응답하였으므로 443번 포트는 닫혀 있는 상태이다. 다) 응답이 없으므로 110번 포트는 방화벽 등에 의해 차단된 상태이다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 12 | essay | 쇼핑몰 개인정보취급자에게 적용해야 하는 비밀번호 작성 규칙 3가지를 서술하시오. | (1) 영문·숫자·특수문자 중 2종류 이상을 조합하여 최소 10자리 이상 또는 3종류 이상을 조합하여 최소 8자리 이상의 길이로 구성한다. (2) 연속적인 숫자, 생년월일, 전화번호 등 추측하기 쉬운 개인정보 및 아이디와 유사한 비밀번호는 사용하지 않도록 권고한다. (3) 비밀번호에 유효기간을 설정하여 반기별 1회 이상 변경한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 여행사 개인정보 이용 약관 동의서에서 법규에 어긋나는 부분 3가지를 찾으시오. 약관에는 수집·이용 목적이 `여행자 멤버십 등록 및 이벤트 업체 정보 제공`, 보유·이용기간이 `멤버십 탈퇴 시까지`, 수집 항목이 `성명, 생년월일, 주민등록번호, 주소, 이메일, 전화번호`, 안내 문구가 `동의를 거부하실 수 있습니다.`로 제시되어 있다. | (1) 이벤트 업체에 개인정보를 제공하는 것은 제3자 제공에 해당하므로 별도의 동의를 받아야 하며, 제공 항목·목적·기간 등을 별도로 안내해야 한다. (2) 멤버십 등록 목적으로 주민등록번호를 수집하는 것은 법적 근거가 없는 과도한 수집이며, 정당한 근거가 있더라도 별도 동의를 받아야 한다. (3) 동의 거부 권리를 안내할 때 동의 거부에 따른 불이익도 함께 안내해야 한다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 14 | essay | 공격자가 `view.php`의 `no` 파라미터에 `union select`와 `substr(database(),0,1)='t'` 조건을 포함한 URL을 입력했더니 화면에 `1`이 출력되었다. 공격 명칭, 공격자가 알 수 있는 정보, HTML 출력만 숨기는 조치의 한계와 올바른 대응 방안을 서술하시오. | (1) Blind SQL Injection (2) 데이터베이스 명을 파악할 수 있다. 위 공격을 통해 데이터베이스 첫 글자가 't'임을 확인할 수 있으며, 유사한 공격을 반복하여 전체 데이터베이스 이름을 알아낼 수 있다. (3) HTML 수정으로 특정 출력 필드를 숨기더라도 SQL Injection이 동작하는 한 다른 페이지에도 동일한 공격이 가능하며, 출력이 차단되더라도 악의적인 쿼리가 내부적으로 실행되는 것은 막을 수 없다. HTML 수정이 아닌 Prepared Statement(준비된 구문)를 이용하여 SQL Injection 공격을 원천 차단해야 한다. | source-derived from Information Security Tistory; context restored from source text |
| 15 | essay | 조건에 맞는 Snort 룰을 작성하시오. (1) 텔넷 서비스 기본 포트 23번을 대상으로 한다. (2) 탐지 시 alert를 발생시키고 이벤트명은 `Dangerous`로 설정한다. (3) 첫 번째 바이트부터 14번째 바이트 범위 내에 `anonymous` 문자열 패턴이 있는지 검사한다. | alert tcp any any -> any 23 (msg:"Dangerous"; content:"anonymous"; depth:14;) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
