---
title: 정보보안기사 실기 6회 2015년 2회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/b5090bba7ef6152006fcc3c4d649f39bf2b978621eaf86dd05c041a663d102bc/edbd036cbc7fccabf130006336b0c5bd5239f1d63e70627de9aafe12157dfab6/manifest.json
summary: 정보보안기사 실기 6회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 6회 2015년 2회 실기 복원

### Scope
- Exam mapping: 2015년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | TCP 스캔을 수행 중이다. 각 경우에 알맞은 Flag를 쓰시오.<br>(1) TCP Open Scan에서 포트가 닫힌 경우: 공격자가 (A)를 송신하면 수신 호스트는 (B)를 응답한다.<br>(2) TCP Half-Open Scan에서 포트가 열린 경우: 공격자가 (C)를 송신하면 수신 호스트는 (D)를 응답하고, 공격자는 (E)를 송신하여 연결을 끊는다. | (A) SYN, (B) RST+ACK, (C) SYN, (D) SYN+ACK, (E) RST | PDF compilation cross-check restored all A~E conditions; RFC 9293 confirms a closed endpoint responds to an initial SYN with RST+ACK and SYN consumes one sequence number. This is a non-official blog compilation, not KCA wording. |
| 2 | short | SNMPv3 보안 매개변수별 기능을 빈칸 (A), (B), (C)에 쓰시오.<br>(A) `msgAuthoritativeEngineID`, `msgAuthoritativeEngineBoots`, `msgAuthoritativeEngineTime` 묶음<br>(B) `msgUserName`, `msgAuthenticationParameters` 묶음<br>(C) `msgPrivacyParameters` | (A) 재전송(Replay) 공격 방지<br>(B) 데이터 근원지 인증 및 메시지 무결성 보장<br>(C) privacy 모듈로 scopedPDU를 암호화할 때 도청·노출 방지. privacy는 인증을 전제로 한다. | source-derived from Information Security Tistory; 2026-07-16 technical wording correction cross-checked against RFC 3414 |
| 3 | essay | 동일 IP `10.10.100.27`이 포트를 바꾸어가며 DNS `ANY` 레코드 질의를 지속 수행하는 로그를 보고, 이 트래픽을 차단하는 라우터 ACL `access-list 1 deny (A) any any eq (B)`의 빈칸을 채우시오. | A : udp B : 53 해설 : 이 로그만으로는 반사·증폭 여부까지 단정할 수 없고 DNS 질의 폭주로 판단한다. 실제 운영에서는 전체 UDP/53 차단이 아니라 출발지·목적지·rate limit·재귀 질의 정책을 함께 제한한다. | source-derived from Information Security Tistory; 2026-07-16 technical wording correction: ANY queries alone do not prove reflected amplification |
| 4 | short | `netstat -rn` 라우팅 테이블을 보고 각 목적지로 ping 전송 시 선택되는 게이트웨이 IP를 쓰시오. 라우팅 테이블은 `10.0.160.100/32 -> 10.0.160.1`, `10.0.160.0/24 -> 10.0.160.2`, `10.0.64.101/18 -> 10.0.160.3`, `10.0.128.100/18 -> 10.0.160.4`, `10.0.63.1/23 -> 10.0.160.6`, default `0.0.0.0/0 -> 10.0.160.5`이다. (A) `10.0.160.100`, (B) `10.0.122.64`, (C) `10.0.192.100`으로 전송할 때의 게이트웨이를 구하시오. | A : 10.0.160.1 (목적지 10.0.160.100에 대한 호스트 라우트) B : 10.0.160.3 (`10.0.64.101/18`은 `10.0.64.0/18`, 즉 `10.0.64.0~10.0.127.255` 범위이므로 목적지 10.0.122.64와 최장 일치) C : 10.0.160.5 (어느 경우에도 해당하지 않으므로 Default Gateway) | source-derived from Information Security Tistory; 2026-07-16 calculation correction: B was incorrectly mapped to 10.0.160.2 |
| 5 | essay | 유닉스 시스템에서 다음 명령어 수행 시 참조되는 로그 파일명을 각각 쓰시오.<br>(A) `who`<br>(B) `last`<br>(C) `lastcomm` | (A) utmp<br>(B) wtmp<br>(C) acct 또는 pacct | source-derived from Information Security Tistory; command list restored |
| 6 | short | root 계정의 원격 접속을 제한하기 위해 각 운영체제에서 설정하는 파일을 쓰시오. (A) Solaris, (B) AIX, (C) Linux. | A : /etc/default/login B : /etc/security/user C : /etc/securetty | source-derived from Information Security Tistory; OS list restored |
| 7 | short | 정보보호관리체계(ISMS)의 라이프사이클 순서 `(A) -> (B) -> (C) -> 조치단계(Act)`에서 빈칸을 채우시오. | A : 계획단계(Plan) B : 실행단계(Do) C : 점검단계(Check) | source-derived from Information Security Tistory; sequence restored |
| 8 | essay | 위험 분석 관련 용어의 빈칸을 채우시오. (A): 정보, 하드웨어, 소프트웨어, 시설, 관련 인력, 기업 이미지 등 조직이 보호해야 할 유·무형 대상. (B): 자산에 손실을 초래할 수 있는 원치 않는 사건의 잠재적 원인이나 행위자. (C): 위협에 이용될 수 있는 자산의 관리적·물리적·기술적 약점. | A : 자산(Asset) B : 위협(Threat) C : 취약점(Vulnerability) | source-derived from Information Security Tistory; definitions restored |
| 9 | essay | 개인정보 보호책임자 자격요건·지정, 개인정보 보호책임자와 개인정보취급자의 역할·책임, 기술적·관리적 보호조치 이행 여부 내부 점검, 위탁 시 수탁자 관리·감독, 개인정보 분실·도난·누출·변조·훼손 대응절차를 포함하는 문서의 명칭을 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; prompt list restored |
| 10 | short | 다음 통제의 명칭을 빈칸 (A), (B), (C)에 각각 쓰시오.<br>(A) 오류·부정 등 발생 가능한 잠재 문제를 사전에 식별해 대처하는 통제<br>(B) 관계자 외의 사람이 특정 시설·설비에 접근하지 못하게 하는 통제<br>(C) 승인받지 못한 사람이 정보통신망을 통해 자산에 접근하지 못하게 하는 통제 | (A) 예방 통제<br>(B) 물리적 접근 통제<br>(C) 논리적 접근 통제 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: purpose-based (A) and access-target-based (B)/(C) labels are explicitly mapped; exact official wording unavailable |
| 11 | essay | IPSec이 제공하는 기능 4가지 이상을 서술하시오. | (1) 데이터 기밀성 : ESP 프로토콜의 페이로드 암호화를 통해 제3자에 의한 도청이 발생해도 내용이 노출되지 않음을 보장한다. (2) 비연결형 무결성 : AH 정보를 통해 비연결형 통신 데이터의 무결성을 보장한다. (3) 데이터 근원지 인증 : 송신자와 수신자만 공유한 키를 통해 메시지 발송자를 식별·인증할 수 있다. (4) 재전송 공격 방지 : IPSec 헤더의 Sequence Number 필드를 통해 재전송(Replay) 공격을 방어한다. (5) 제한된 트래픽 흐름의 비밀성 : 터널 모드에서 원본 IP 헤더를 암호화하여 출발지·목적지 주소를 은닉할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 위험 분석 모델 중 복합적 모델(복합 접근법)의 장단점을 서술하시오. | 장점 : 비용과 자원을 효율적으로 사용할 수 있으며, 고위험 영역을 빠르게 식별할 수 있다. 단점 : 고위험 영역이 잘못 식별된 경우 위험 분석 비용이 낭비되거나 부적절하게 대응될 수 있다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | DNS 증폭 공격(DNS Amplification DDoS Attack)에 관하여 다음을 서술하시오. (1) IP 기반 DNS 증폭 공격에 사용하는 기법의 명칭과 동작 (2) 그 기법을 사용하는 이유와 DNS 응답이 향하는 대상 (3) 큰 DNS 응답을 유도할 수 있는 질의 유형의 예와 증폭되는 이유 | (1) IP 스푸핑이다. 공격자는 출발지 IP를 피해자 IP로 위조하여 다수의 DNS 서버에 질의한다. (2) DNS 서버의 응답이 위조된 출발지인 피해자에게 전달되어, 여러 서버의 트래픽이 피해자에게 반사·집중되는 DRDoS 효과가 발생한다. (3) 역사적으로 `ANY` 질의나 큰 `TXT` 응답을 유도하는 질의가 예시다. 질의보다 응답이 훨씬 클 수 있어 증폭이 가능하다. 다만 `ANY`·`TXT`가 필수는 아니며 응답 크기와 증폭률은 DNS 설정·EDNS·DNSSEC·질의 내용에 따라 달라진다. | source-derived from Information Security Tistory; 2026-07-18 prompt completeness and technical wording correction cross-checked against RFC 5358. The original blog asks three parts; ANY/TXT are historical examples, not mandatory indicators. Exact KCA wording unavailable. |
| 14 | essay | 다음 SQL 쿼리에 답하시오.<br>`SELECT password FROM user WHERE username='qfrankr'`<br>(1) 현재 쿼리의 실행 결과<br>(2) `qfrankr` 입력 위치에 넣어 조건절을 항상 참으로 만들 수 있는 SQL Injection 입력 예<br>(3) (2)의 입력이 가능한 이유 | (1) username이 qfrankr인 사용자의 password 정보를 조회한다.<br>(2) `' or '1'='1` 또는 `' or 'a'='a` 등 조건절을 항상 참으로 만드는 값<br>(3) 위 값 삽입 시 WHERE 조건절이 `WHERE username='' or '1'='1'`이 되어 항상 참(True)이 되므로 모든 사용자 행의 `password` 값이 조회된다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format and precision correction: this SELECT projects password values, not all columns; exact official wording unavailable |
| 15 | essay | 패킷 캡처에서 클라이언트가 HTTP 요청 헤더를 완성하지 않고 불완전한 헤더 정보를 매우 천천히 지속 전송하면서 웹 서버 연결을 장시간 유지한다. 다수 연결이 같은 상태로 유지되어 정상 접속이 거부되고 있다. (1) 공격명, (2) 발생 현상과 이유, (3) 대응 방법을 서술하시오. | (1) Slow HTTP Header DoS 공격(Slowloris 공격) (2) 서비스가 느려지고 새로운 정상 접속 요청이 거부된다. 공격자가 HTTP 요청 헤더를 비정상적으로 조작하여 불완전한 헤더 정보를 천천히 지속적으로 전달하면, 웹 서버는 헤더 정보가 완전히 수신될 때까지 연결을 유지한다. 웹 서버의 동시 연결 가능 자원이 제한적이므로 다수의 비정상 연결이 자원을 점유하면 정상 사용자의 접속이 불가능해진다. (3) 서버 방화벽 등을 이용하여 동일 IP에서의 동시 연결 수에 대한 임계치(Threshold)를 설정하여 비정상적으로 많은 연결 상태를 유지하는 IP를 차단한다. | source-derived from Information Security Tistory; packet condition restored |
| 16 | essay | 게이트웨이 IP/MAC이 `172.111.11.1`, `11-22-33-44-55-66`인 환경에서 ARP 테이블에 `172.111.11.3`도 동일 MAC `11-22-33-44-55-66`으로 표시된다. 다음을 서술하시오.<br>(1) 공격 판단과 판단 전 확인할 정상 구성 조건<br>(2) 대응 방안 | (1) 정상 자산 목록에서 172.111.11.3의 MAC이 달라야 하고 Proxy ARP·VRRP/HSRP 등 정상 공유 MAC 구성이 아니라는 조건이 확인되면 ARP Spoofing을 의심한다. 동일 MAC 표시만으로 공격을 단정하지 않는다.<br>(2) 정적 ARP는 제한된 단말에서의 보조 대응이며, 스위치 DHCP Snooping/DAI와 ARP 변경 모니터링을 병행한다. | source-derived from Information Security Tistory; 2026-07-16 technical correction: identical MAC can be legitimate in proxy or redundancy configurations |

### Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.

## Schema / Composition

## Usage

## Limitations / Biases

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|


## Relations

| type | target | notes |
|---|---|---|


## Sources

- `raw/sources/clipping/b5090bba7ef6152006fcc3c4d649f39bf2b978621eaf86dd05c041a663d102bc/edbd036cbc7fccabf130006336b0c5bd5239f1d63e70627de9aafe12157dfab6/manifest.json`
