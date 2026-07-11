---
title: "정보보안기사 실기 6회 2015년 2회 실기 복원"
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
  - "https://information-security.tistory.com/285"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 6회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 6회 2015년 2회 실기 복원

## Scope
- Exam mapping: 2015년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | TCP 스캔 유형에 따른 플래그 응답을 채우시오. | A : SYN B : RST + ACK C : SYN D : SYN + ACK E : RST | source-derived from Information Security Tistory; answer block present |
| 2 | short | SNMPv3 보안 매개변수별로 방지 가능한 공격을 쓰시오. `msgAuthoritativeEngineID`, `msgAuthoritativeEngineBoots`, `msgAuthoritativeEngineTime`이 묶인 항목은 (A), `msgUserName`, `msgAuthenticationParameters`가 묶인 항목은 (B), `msgPrivacyParameters` 항목은 (C)에 해당한다. | A : 재전송(Replay) 공격 방지 B : 메시지 위변조 공격 방지 C : 도청/스니핑 공격 방지 | source-derived from Information Security Tistory; parameter table restored |
| 3 | essay | 동일 IP `10.10.100.27`이 포트를 바꾸어가며 DNS `ANY` 레코드 질의를 지속 수행하는 로그를 보고, 이 공격을 막기 위한 라우터 ACL `access-list 1 deny (A) any any eq (B)`의 빈칸을 채우시오. | A : udp B : 53 해설 : 동일 IP에서 포트를 변경하며 레코드 타입 ANY로 대량의 DNS 질의를 수행하는 DNS 증폭 DDoS 공격이다. | source-derived from Information Security Tistory; context restored from source text |
| 4 | short | `netstat -rn` 라우팅 테이블을 보고 각 목적지로 ping 전송 시 선택되는 게이트웨이 IP를 쓰시오. 라우팅 테이블은 `10.0.160.100/32 -> 10.0.160.1`, `10.0.160.0/24 -> 10.0.160.2`, `10.0.64.101/18 -> 10.0.160.3`, `10.0.128.100/18 -> 10.0.160.4`, `10.0.63.1/23 -> 10.0.160.6`, default `0.0.0.0/0 -> 10.0.160.5`이다. (A) `10.0.160.100`, (B) `10.0.122.64`, (C) `10.0.192.100`으로 전송할 때의 게이트웨이를 구하시오. | A : 10.0.160.1 (목적지 10.0.160.100에 대한 호스트 라우트) B : 10.0.160.2 (10.0.160.0/24 네트워크 범위에 해당) C : 10.0.160.5 (어느 경우에도 해당하지 않으므로 Default Gateway) | source-derived from Information Security Tistory; routing table restored |
| 5 | essay | 유닉스 시스템에서 다음 명령어 수행 시 참조되는 로그 파일명을 각각 쓰시오. (A) `who`, (B) `last`, (C) `lastcomm`. | A : utmp B : wtmp C : acct 또는 pacct | source-derived from Information Security Tistory; command list restored |
| 6 | short | root 계정의 원격 접속을 제한하기 위해 각 운영체제에서 설정하는 파일을 쓰시오. (A) Solaris, (B) AIX, (C) Linux. | A : /etc/default/login B : /etc/security/user C : /etc/securetty | source-derived from Information Security Tistory; OS list restored |
| 7 | short | 정보보호관리체계(ISMS)의 라이프사이클 순서 `(A) -> (B) -> (C) -> 조치단계(Act)`에서 빈칸을 채우시오. | A : 계획단계(Plan) B : 실행단계(Do) C : 점검단계(Check) | source-derived from Information Security Tistory; sequence restored |
| 8 | essay | 위험 분석 관련 용어의 빈칸을 채우시오. (A): 정보, 하드웨어, 소프트웨어, 시설, 관련 인력, 기업 이미지 등 조직이 보호해야 할 유·무형 대상. (B): 자산에 손실을 초래할 수 있는 원치 않는 사건의 잠재적 원인이나 행위자. (C): 위협에 이용될 수 있는 자산의 관리적·물리적·기술적 약점. | A : 자산(Asset) B : 위협(Threat) C : 취약점(Vulnerability) | source-derived from Information Security Tistory; definitions restored |
| 9 | essay | 개인정보 보호책임자 자격요건·지정, 개인정보 보호책임자와 개인정보취급자의 역할·책임, 기술적·관리적 보호조치 이행 여부 내부 점검, 위탁 시 수탁자 관리·감독, 개인정보 분실·도난·누출·변조·훼손 대응절차를 포함하는 문서의 명칭을 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; prompt list restored |
| 10 | short | 발생 가능한 잠재 문제를 사전에 식별해 대처하는 통제, 물리적 시설·장비 접근을 제한하는 통제, 시스템·네트워크 접근 권한을 제한하는 통제의 명칭을 각각 쓰시오. | A : 예방 통제 B : 물리적 접근 통제 C : 논리적 접근 통제 | source-derived from Information Security Tistory; answer block present |
| 11 | essay | IPSec이 제공하는 기능 4가지 이상을 서술하시오. | (1) 데이터 기밀성 : ESP 프로토콜의 페이로드 암호화를 통해 제3자에 의한 도청이 발생해도 내용이 노출되지 않음을 보장한다. (2) 비연결형 무결성 : AH 정보를 통해 비연결형 통신 데이터의 무결성을 보장한다. (3) 데이터 근원지 인증 : 송신자와 수신자만 공유한 키를 통해 메시지 발송자를 식별·인증할 수 있다. (4) 재전송 공격 방지 : IPSec 헤더의 Sequence Number 필드를 통해 재전송(Replay) 공격을 방어한다. (5) 제한된 트래픽 흐름의 비밀성 : 터널 모드에서 원본 IP 헤더를 암호화하여 출발지·목적지 주소를 은닉할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 위험 분석 모델 중 복합적 모델(복합 접근법)의 장단점을 서술하시오. | 장점 : 비용과 자원을 효율적으로 사용할 수 있으며, 고위험 영역을 빠르게 식별할 수 있다. 단점 : 고위험 영역이 잘못 식별된 경우 위험 분석 비용이 낭비되거나 부적절하게 대응될 수 있다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | DNS 증폭 공격(DNS Amplification DDoS Attack) 중 IP 기반 공격에 관한 물음에 답하시오. | (1) IP 스푸핑을 사용하여 출발지 IP를 공격 대상 희생자 서버의 IP로 위조한 후 다수의 DNS 서버에 질의를 수행한다. (2) 공격자의 DNS 질의에 대한 응답 패킷이 IP 스푸핑된 희생자 서버로 전달되므로, 희생자 서버에 대량의 트래픽을 집중시켜 서비스 거부 공격이 가능하다. (3) ANY 또는 TXT 레코드 타입을 사용한다. 요청 패킷의 크기보다 응답 패킷의 크기가 수십 배 크므로, 적은 컴퓨팅 자원으로 대량의 트래픽을 희생자에게 전달할 수 있는 증폭 효과가 있다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | SQL 쿼리 `SELECT password FROM user WHERE username='qfrankr'`에 대해 답하시오. (1) 실행 결과를 서술하시오. (2) 모든 사용자 정보를 얻기 위해 `qfrankr` 자리에 삽입할 SQL Injection 예시를 쓰시오. (3) 해당 예시가 가능한 이유를 서술하시오. | (1) username이 qfrankr인 사용자의 password 정보를 조회한다. (2) ' or '1'='1 또는 ' or 'a'='a 등 조건절을 항상 참으로 만드는 값 (3) 위 값 삽입 시 WHERE 조건절이 WHERE username='' or '1'='1'이 되어 항상 참(True)이 되므로 모든 사용자의 레코드가 조회된다. | source-derived from Information Security Tistory; SQL statement restored |
| 15 | essay | 패킷 캡처에서 클라이언트가 HTTP 요청 헤더를 완성하지 않고 불완전한 헤더 정보를 매우 천천히 지속 전송하면서 웹 서버 연결을 장시간 유지한다. 다수 연결이 같은 상태로 유지되어 정상 접속이 거부되고 있다. (1) 공격명, (2) 발생 현상과 이유, (3) 대응 방법을 서술하시오. | (1) Slow HTTP Header DoS 공격(Slowloris 공격) (2) 서비스가 느려지고 새로운 정상 접속 요청이 거부된다. 공격자가 HTTP 요청 헤더를 비정상적으로 조작하여 불완전한 헤더 정보를 천천히 지속적으로 전달하면, 웹 서버는 헤더 정보가 완전히 수신될 때까지 연결을 유지한다. 웹 서버의 동시 연결 가능 자원이 제한적이므로 다수의 비정상 연결이 자원을 점유하면 정상 사용자의 접속이 불가능해진다. (3) 서버 방화벽 등을 이용하여 동일 IP에서의 동시 연결 수에 대한 임계치(Threshold)를 설정하여 비정상적으로 많은 연결 상태를 유지하는 IP를 차단한다. | source-derived from Information Security Tistory; packet condition restored |
| 16 | essay | 게이트웨이 IP/MAC이 `172.111.11.1`, `11-22-33-44-55-66`인 환경에서 ARP 테이블에 `172.111.11.3`도 동일 MAC `11-22-33-44-55-66`으로 표시된다. 공격 유형, 판단 근거, 대응 방안을 서술하시오. | (1) ARP Spoofing(ARP 스푸핑) 공격이다. 172.111.11.3의 MAC 주소가 게이트웨이(172.111.11.1)의 MAC 주소인 11-22-33-44-55-66과 동일하다. 공격자가 위조된 ARP Reply를 전송하여 게이트웨이 IP에 대한 MAC 주소를 자신의 MAC 주소로 변조한 것으로 판단된다. (2) ARP Cache Table의 게이트웨이 정보를 정적(static)으로 설정하여 위조된 ARP 응답으로 변조되지 않도록 한다. 명령어 : arp -s 172.111.11.1 11-22-33-44-55-66 | source-derived from Information Security Tistory; context restored from source text |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
