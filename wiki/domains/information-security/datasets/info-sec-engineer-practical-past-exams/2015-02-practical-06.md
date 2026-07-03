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
date_updated: 2026-07-03
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
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | TCP 스캔 유형에 따른 플래그 응답을 채우시오. | A : SYN B : RST + ACK C : SYN D : SYN + ACK E : RST | source-derived from Information Security Tistory; answer block present |
| 2 | short | SNMPv3에서 다음 보안 매개변수 설정으로 방지 가능한 공격을 각각 쓰시오. | A : 재전송(Replay) 공격 방지 B : 메시지 위변조 공격 방지 C : 도청/스니핑 공격 방지 | source-derived from Information Security Tistory; answer block present |
| 3 | essay | 다음 DNS 로그를 분석하여 이 공격을 막기 위한 라우터 ACL 설정 명령어의 빈칸 (A), (B)를 채우시오. | A : udp B : 53 해설 : 동일 IP에서 포트를 변경하며 레코드 타입 ANY로 대량의 DNS 질의를 수행하는 DNS 증폭 DDoS 공격이다. | source-derived from Information Security Tistory; answer block present |
| 4 | short | 다음은 netstat -rn 명령 수행 결과의 라우팅 테이블이다. 각 IP로 ping 전송 시 라우팅되는 게이트웨이 IP를 쓰시오. | A : 10.0.160.1 (목적지 10.0.160.100에 대한 호스트 라우트) B : 10.0.160.2 (10.0.160.0/24 네트워크 범위에 해당) C : 10.0.160.5 (어느 경우에도 해당하지 않으므로 Default Gateway) | source-derived from Information Security Tistory; answer block present |
| 5 | essay | 유닉스 시스템에서 다음 명령어 수행 시 참조되는 로그 파일명을 각각 쓰시오. | A : utmp B : wtmp C : acct 또는 pacct | source-derived from Information Security Tistory; answer block present |
| 6 | short | root 계정의 원격 접속을 제한하기 위해 각 운영체제에서 설정하는 파일을 쓰시오. | A : /etc/default/login B : /etc/security/user C : /etc/securetty | source-derived from Information Security Tistory; answer block present |
| 7 | short | 정보보호관리체계(ISMS)의 라이프사이클 4단계 중 빈칸 (A), (B), (C)를 채우시오. | A : 계획단계(Plan) B : 실행단계(Do) C : 점검단계(Check) | source-derived from Information Security Tistory; answer block present |
| 8 | essay | 위험 분석과 관련된 용어에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 자산(Asset) B : 위협(Threat) C : 취약점(Vulnerability) | source-derived from Information Security Tistory; answer block present |
| 9 | essay | 다음은 개인정보의 기술적·관리적 보호조치 항목을 포함하는 문서이다. 이 문서의 명칭을 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 다음에서 설명하는 통제 유형의 명칭을 각각 쓰시오. | A : 예방 통제 B : 물리적 접근 통제 C : 논리적 접근 통제 | source-derived from Information Security Tistory; answer block present |
| 11 | essay | IPSec이 제공하는 기능 4가지 이상을 서술하시오. | (1) 데이터 기밀성 : ESP 프로토콜의 페이로드 암호화를 통해 제3자에 의한 도청이 발생해도 내용이 노출되지 않음을 보장한다. (2) 비연결형 무결성 : AH 정보를 통해 비연결형 통신 데이터의 무결성을 보장한다. (3) 데이터 근원지 인증 : 송신자와 수신자만 공유한 키를 통해 메시지 발송자를 식별·인증할 수 있다. (4) 재전송 공격 방지 : IPSec 헤더의 Sequence Number 필드를 통해 재전송(Replay) 공격을 방어한다. (5) 제한된 트래픽 흐름의 비밀성 : 터널 모드에서 원본 IP 헤더를 암호화하여 출발지·목적지 주소를 은닉할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 위험 분석 모델 중 복합적 모델(복합 접근법)의 장단점을 서술하시오. | 장점 : 비용과 자원을 효율적으로 사용할 수 있으며, 고위험 영역을 빠르게 식별할 수 있다. 단점 : 고위험 영역이 잘못 식별된 경우 위험 분석 비용이 낭비되거나 부적절하게 대응될 수 있다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | DNS 증폭 공격(DNS Amplification DDoS Attack) 중 IP 기반 공격에 관한 물음에 답하시오. | (1) IP 스푸핑을 사용하여 출발지 IP를 공격 대상 희생자 서버의 IP로 위조한 후 다수의 DNS 서버에 질의를 수행한다. (2) 공격자의 DNS 질의에 대한 응답 패킷이 IP 스푸핑된 희생자 서버로 전달되므로, 희생자 서버에 대량의 트래픽을 집중시켜 서비스 거부 공격이 가능하다. (3) ANY 또는 TXT 레코드 타입을 사용한다. 요청 패킷의 크기보다 응답 패킷의 크기가 수십 배 크므로, 적은 컴퓨팅 자원으로 대량의 트래픽을 희생자에게 전달할 수 있는 증폭 효과가 있다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음 SQL 쿼리에 관한 물음에 답하시오. | (1) username이 qfrankr인 사용자의 password 정보를 조회한다. (2) ' or '1'='1 또는 ' or 'a'='a 등 조건절을 항상 참으로 만드는 값 (3) 위 값 삽입 시 WHERE 조건절이 WHERE username='' or '1'='1'이 되어 항상 참(True)이 되므로 모든 사용자의 레코드가 조회된다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음은 패킷 캡처 결과를 분석한 것이다. 물음에 답하시오. | (1) Slow HTTP Header DoS 공격(Slowloris 공격) (2) 서비스가 느려지고 새로운 정상 접속 요청이 거부된다. 공격자가 HTTP 요청 헤더를 비정상적으로 조작하여 불완전한 헤더 정보를 천천히 지속적으로 전달하면, 웹 서버는 헤더 정보가 완전히 수신될 때까지 연결을 유지한다. 웹 서버의 동시 연결 가능 자원이 제한적이므로 다수의 비정상 연결이 자원을 점유하면 정상 사용자의 접속이 불가능해진다. (3) 서버 방화벽 등을 이용하여 동일 IP에서의 동시 연결 수에 대한 임계치(Threshold)를 설정하여 비정상적으로 많은 연결 상태를 유지하는 IP를 차단한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음은 게이트웨이 정보와 ARP 테이블이다. 물음에 답하시오. | (1) ARP Spoofing(ARP 스푸핑) 공격이다. 172.111.11.3의 MAC 주소가 게이트웨이(172.111.11.1)의 MAC 주소인 11-22-33-44-55-66과 동일하다. 공격자가 위조된 ARP Reply를 전송하여 게이트웨이 IP에 대한 MAC 주소를 자신의 MAC 주소로 변조한 것으로 판단된다. (2) ARP Cache Table의 게이트웨이 정보를 정적(static)으로 설정하여 위조된 ARP 응답으로 변조되지 않도록 한다. 명령어 : arp -s 172.111.11.1 11-22-33-44-55-66 | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
