---
title: "정보보안기사 실기 3회 2014년 1회 실기 복원"
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
  - "https://information-security.tistory.com/291"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 3회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 3회 2014년 1회 실기 복원

## Scope
- Exam mapping: 2014년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 다음은 Diffie-Hellman 알고리즘을 통한 키 교환 과정이다. 빈칸 (A), (B), (C)를 채우시오. | A : B^a mod p (Bob이 전송한 값의 a 거듭제곱 mod p) B : A^b mod p (Alice가 전송한 값의 b 거듭제곱 mod p) C : 비밀키(대칭키) | source-derived from Information Security Tistory; answer block present |
| 2 | essay | HeartBleed 취약점에 관한 물음에 답하시오. | (1) OpenSSL (2) OpenSSL 1.0.1 ~ OpenSSL 1.0.1f, OpenSSL 1.0.2-beta, OpenSSL 1.0.2-beta1 | source-derived from Information Security Tistory; answer block present |
| 3 | short | 다음에서 설명하는 현상이 발생하는 공격의 명칭을 쓰시오. | TCP SYN Flooding | source-derived from Information Security Tistory; answer block present |
| 4 | short | 접근 통제 정책에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : DAC(임의적 접근 통제, Discretionary Access Control) B : MAC(강제적 접근 통제, Mandatory Access Control) C : RBAC(역할 기반 접근 통제, Role-Based Access Control) | source-derived from Information Security Tistory; answer block present |
| 5 | short | 다음 Snort 룰의 빈칸 (A), (B), (C)를 채우시오. | A : any B : content C : msg | source-derived from Information Security Tistory; answer block present |
| 6 | short | 다음에서 설명하는 용어를 쓰시오. | 정보보호관리체계(ISMS, Information Security Management System) | source-derived from Information Security Tistory; answer block present |
| 7 | short | 다음에서 설명하는 OWASP Top 10 공격 기법의 명칭을 쓰시오. | XSS(Cross Site Script) | source-derived from Information Security Tistory; answer block present |
| 8 | short | 정보보호관리체계의 관리적 요구사항 절차를 올바른 순서로 나열하시오. | ㄹ → ㄷ → ㄴ → ㅁ → ㄱ | source-derived from Information Security Tistory; answer block present |
| 9 | short | 다음에서 설명하는 공격 기법의 명칭을 쓰시오. | Teardrop 공격 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 위험 대응 보호 대책에 관한 설명이다. 각각의 명칭을 쓰시오. | (1) 위험 감소(Risk Reduction) (2) 위험 회피(Risk Avoidance) (3) 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 무선랜 MAC 주소 보안에 관한 물음에 답하시오. | (1) MAC 주소는 제조사 코드(OUI) 24비트와 장치 고유 일련번호 24비트로 구성된다. (2) 사전에 등록된 MAC 주소를 가진 단말기만 무선 AP 접속을 허용하고 나머지는 차단하는 방식이다. 장점 : 비인가 단말기의 무선 네트워크 접속을 차단하여 보안성을 높인다. 단점 : 공격자가 허용된 MAC 주소를 탈취하여 자신의 MAC 주소를 위장(MAC 스푸핑)하면 우회가 가능하므로 완전한 보안 수단이 되지 못한다. (3) ARP 스푸핑 또는 MAC 스푸핑을 통해 허용된 MAC 주소를 탈취한 후 자신의 네트워크 인터페이스의 MAC 주소를 허용된 주소로 변경하여 필터링을 우회한다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 다음은 네트워크 패킷 캡처 내용이다. 물음에 답하시오. | (1) Referer : 하이퍼링크를 통해 유입된 경우 링크가 걸려 있던 원래 페이지의 주소를 기록하는 헤더 필드이다. Cache-Control : HTTP 1.1에서 추가된 캐시 제어 속성으로, 동일 페이지 재방문 시 캐시 정보 제어 방식을 지정한다. (예: no-cache, max-age=0 등) (2) Cache-Control 공격(CC 공격) (3) max-age=0으로 설정하여 캐시를 무효화함으로써 서버가 모든 요청에 대해 직접 응답을 생성해야 하므로 서버에 과도한 부하(오버헤드)가 발생한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 재난 복구 서비스의 분류 5가지 이상을 명칭과 함께 특징을 설명하시오. | (1) Mirror Site : 주 센터와 동일한 수준의 정보기술 자원을 원격지에 구축하고 Active-Active 상태로 실시간 동시 서비스를 제공한다. (2) Hot Site : 주 센터와 동일한 수준의 자원을 원격지에 구축하여 Stand-by 상태로 유지하다가 재해 발생 시 즉시 Active 상태로 전환하여 서비스를 제공한다. (3) Warm Site : 중요도가 높은 정보 시스템만 부분적으로 재해복구 센터에 보유하며, 데이터는 주기적으로 백업한다. (4) Cold Site : 데이터만 원격지에 보관하고, 서비스를 위한 정보 자원은 최소한으로만 확보하거나 확보하지 않으며, 재해 발생 시 자원을 새로 조달하여 복구를 시작한다. (5) 상호 지원 협약 : 두 개 이상의 기관이 재해 발생 시 상대 기관의 시스템을 이용하도록 협약을 맺는 방식이다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음 상황을 참조하여 IPSec VPN에 관한 물음에 답하시오. | (1) VPN 장비의 SAD(Security Association Database)에 AH 관련 보안 연계 정보가 존재하지 않거나 호환 가능한 AH 관련 정보가 없었을 것으로 추정된다. 또한 AH 프로토콜은 IP 헤더를 포함하여 인증하므로 NAT 환경에서는 IP 헤더가 변경되어 AH 인증이 실패하는 구조적 문제도 원인일 수 있다. (2) 장점 : 사전에 공유한 키를 사용하여 별도의 인증기관(CA) 없이 간단하게 상호 인증이 가능하다. 단점 : 인증서 방식에 비해 강력한 인증을 제공하지 못하며, 사전에 공유한 키가 유출될 경우 보안이 위협받는 위험이 있다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음 HTTP GET Flooding 공격 상황에 관한 물음에 답하시오. | (1) HTTP GET Flooding 공격 (2) 대량의 HTTP GET 요청을 지속적으로 전송하여 서버의 TCP 세션 자원과 처리 자원을 모두 소진시킨다. 그 결과 정상적인 사용자가 접속 요청을 해도 서버가 새로운 연결을 수용하지 못하여 서비스 거부 상태가 발생한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 개인정보 영향평가 대상으로 대통령령으로 정한 기준에 해당하는 개인정보 파일의 유형을 서술하시오. | (1) 구축·운용 또는 변경하려는 개인정보 파일로서 5만 명 이상의 정보주체에 관한 민감 정보 또는 고유식별정보의 처리가 수반되는 개인정보 파일 (2) 구축·운용하고 있는 개인정보 파일을 해당 공공기관 내부 또는 외부에서 구축·운용하고 있는 다른 개인정보 파일과 연계하려는 경우로서, 연계 결과 50만 명 이상의 정보주체에 관한 개인정보가 포함되는 개인정보 파일 (3) 구축·운용 또는 변경하려는 개인정보 파일로서 100만 명 이상의 정보주체에 관한 개인정보 파일 | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
