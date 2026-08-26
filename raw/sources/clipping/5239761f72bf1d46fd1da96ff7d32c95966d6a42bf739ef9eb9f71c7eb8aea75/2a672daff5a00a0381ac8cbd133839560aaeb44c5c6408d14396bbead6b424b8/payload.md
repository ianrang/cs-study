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
date_updated: 2026-07-06
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
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Diffie-Hellman 키 교환 과정에서 빈칸을 채우시오. 공개값은 소수 `p`와 원시근 `g`, Alice의 비밀값은 `a`, Bob의 비밀값은 `b`이다. Alice는 `g^a mod p`를 Bob에게 보내고 Bob은 `g^b mod p`를 Alice에게 보낸다. (A): Alice가 계산하는 최종 공유 비밀값. (B): Bob이 계산하는 최종 공유 비밀값. (C): 최종 공유값의 용도. | A : B^a mod p (Bob이 전송한 값의 a 거듭제곱 mod p) B : A^b mod p (Alice가 전송한 값의 b 거듭제곱 mod p) C : 비밀키(대칭키) | source-derived from Information Security Tistory; DH process restored |
| 2 | essay | HeartBleed 취약점에 답하시오. CVE-2014-0160은 OpenSSL 하트비트 확장 모듈에서 클라이언트 요청 메시지의 데이터 길이를 검증하지 않아 시스템 메모리의 최대 64KB 데이터를 외부에서 탈취할 수 있는 취약점이다. (1) 취약점이 존재하는 프로토콜·라이브러리, (2) 영향받는 버전을 쓰시오. | (1) OpenSSL (2) OpenSSL 1.0.1 ~ OpenSSL 1.0.1f, OpenSSL 1.0.2-beta, OpenSSL 1.0.2-beta1 | source-derived from Information Security Tistory; prompt context restored |
| 3 | short | 서버의 연결 대기 큐가 가득 차고 다수의 `SYN_RECEIVED` 상태 연결이 유지되어 정상 사용자의 신규 접속이 불가능해지는 공격의 명칭을 쓰시오. | TCP SYN Flooding | source-derived from Information Security Tistory; answer block present |
| 4 | short | 접근 통제 정책의 빈칸을 채우시오. (A): 객체 소유자가 재량으로 다른 사용자에게 접근 권한을 부여·취소할 수 있다. (B): 주체와 객체의 보안 등급을 비교해 접근을 제한하며 보안 운영체제에서 주로 사용한다. (C): 주체에 할당된 역할 기반으로 객체 접근을 제한한다. | A : DAC(임의적 접근 통제, Discretionary Access Control) B : MAC(강제적 접근 통제, Mandatory Access Control) C : RBAC(역할 기반 접근 통제, Role-Based Access Control) | source-derived from Information Security Tistory; prompt descriptions restored |
| 5 | short | `"/administrator"` 문자열이 포함된 패킷을 탐지하고 `"Web Scan Detected"` 메시지를 로깅하는 Snort 룰 `alert tcp any any -> 192.168.0.1 (A) (B):"/administrator"; (C):"Web Scan Detected";)`의 빈칸을 채우시오. | A : any B : content C : msg | source-derived from Information Security Tistory; Snort rule restored |
| 6 | short | 정보자산의 기밀성·무결성·가용성을 실현하기 위한 절차와 과정을 체계적으로 수립·문서화하고 지속적으로 관리·운영하는 체계의 명칭을 쓰시오. | 정보보호관리체계(ISMS, Information Security Management System) | source-derived from Information Security Tistory; answer block present |
| 7 | short | 신뢰할 수 없는 데이터가 검증 없이 브라우저로 전달되어 공격자가 피해자 브라우저에서 악성 스크립트를 실행하고 세션 탈취·사이트 변조·악성 사이트 이동 등을 유발하는 OWASP Top 10 공격 기법의 명칭을 쓰시오. | XSS(Cross Site Script) | source-derived from Information Security Tistory; answer block present |
| 8 | short | 정보보호관리체계의 관리적 요구사항 절차를 올바른 순서로 나열하시오. 보기: ㄱ. 사후관리, ㄴ. 위험관리, ㄷ. 경영진 책임 및 조직 구성, ㄹ. 정보보호정책 수립 및 범위설정, ㅁ. 정보보호대책 구현. | ㄹ → ㄷ → ㄴ → ㅁ → ㄱ | source-derived from Information Security Tistory; option list restored |
| 9 | short | IP 패킷 단편화 재조합 취약점을 이용해 중첩된 offset 값을 가진 조각 패킷을 보내 목표 시스템 정지나 재부팅을 유발하는 공격 기법의 명칭을 쓰시오. | Teardrop 공격 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 위험 대응 보호 대책의 명칭을 쓰시오. (1) 사업 목적 달성을 위해 보안 통제를 적용하여 위험 수준을 낮추는 방안. (2) 위험이 존재하는 프로세스나 사업 자체를 수행하지 않고 포기하는 방안. (3) 보험이나 외주 등으로 잠재적 위험의 재정적 책임을 제3자에게 이전하는 방안. | (1) 위험 감소(Risk Reduction) (2) 위험 회피(Risk Avoidance) (3) 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; prompt descriptions restored |
| 11 | essay | 무선랜의 MAC 주소 필터링에 관하여 다음을 서술하시오. (1) 48비트 MAC 주소의 구성 (2) MAC 주소 필터링의 개념과 장점·단점 (3) MAC 주소 필터링 우회 방법 | (1) 48비트 MAC 주소는 제조사 식별자(OUI) 24비트와 장치 식별자 24비트로 구성된다. (2) 사전에 등록된 MAC 주소를 가진 단말기만 무선 AP 접속을 허용하고 나머지는 차단하는 방식이다. 장점: 비인가 단말기의 무선 네트워크 접속을 차단한다. 단점: 공격자가 허용된 MAC 주소를 관찰·위장(MAC 스푸핑)하면 우회할 수 있어 완전한 보안 수단이 되지 못한다. (3) 공격자는 무선 트래픽을 관찰해 허용된 MAC 주소를 확인한 뒤, 자신의 네트워크 인터페이스 MAC 주소를 그 값으로 변경하는 MAC 스푸핑으로 필터링을 우회한다. | source-derived from Information Security Tistory; answer block present; 2026-07-18 prompt restoration: answer's three-part structure made explicit; technical correction: MAC spoofing is the direct filtering-bypass technique, and ARP spoofing is not required; exact official wording unavailable |
| 12 | essay | 네트워크 패킷에 `Cache-Control: no-cache, max-age=0` 헤더가 포함되어 있고 동일 출발지 IP에서 짧은 시간에 대량 트래픽이 발생한다. 다음을 서술하시오.<br>(1) `Referer`와 `Cache-Control`의 의미<br>(2) 공격 유형<br>(3) 서버 영향 | (1) Referer : 하이퍼링크를 통해 유입된 경우 링크가 걸려 있던 원래 페이지의 주소를 기록하는 헤더 필드이다. Cache-Control : HTTP 1.1에서 추가된 캐시 제어 속성으로, 동일 페이지 재방문 시 캐시 정보 제어 방식을 지정한다. (예: no-cache, max-age=0 등)<br>(2) Cache-Control 공격(CC 공격)<br>(3) max-age=0으로 설정하여 캐시를 무효화함으로써 서버가 모든 요청에 대해 직접 응답을 생성해야 하므로 서버에 과도한 부하(오버헤드)가 발생한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three requested answer parts are explicitly mapped; exact official wording unavailable |
| 13 | essay | 재난 복구 서비스의 분류 5가지 이상을 명칭과 함께 특징을 설명하시오. | (1) Mirror Site : 주 센터와 동일한 수준의 정보기술 자원을 원격지에 구축하고 Active-Active 상태로 실시간 동시 서비스를 제공한다. (2) Hot Site : 주 센터와 동일한 수준의 자원을 원격지에 구축하여 Stand-by 상태로 유지하다가 재해 발생 시 즉시 Active 상태로 전환하여 서비스를 제공한다. (3) Warm Site : 중요도가 높은 정보 시스템만 부분적으로 재해복구 센터에 보유하며, 데이터는 주기적으로 백업한다. (4) Cold Site : 데이터만 원격지에 보관하고, 서비스를 위한 정보 자원은 최소한으로만 확보하거나 확보하지 않으며, 재해 발생 시 자원을 새로 조달하여 복구를 시작한다. (5) 상호 지원 협약 : 두 개 이상의 기관이 재해 발생 시 상대 기관의 시스템을 이용하도록 협약을 맺는 방식이다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 사설망의 IPsec 피어가 경로상의 NAT를 통과한다. ESP는 NAT-T를 사용하여 정상 동작하지만 AH 보안 연결은 수립되지 않는다. (1) AH 연결이 실패하는 원인을 서술하시오. (2) PSK 방식의 의미와 IKE 피어 인증에 PSK를 사용하는 방식의 장점 및 단점을 서술하시오. | (1) AH는 IP 헤더의 변경 불가능한 필드와 상위 계층 데이터를 무결성·인증 범위에 포함한다. NAT가 외부 IP 헤더의 출발지·목적지 주소를 변경하면 AH 무결성 검증값이 일치하지 않아 연결이 실패한다. 따라서 NAT 환경에서는 일반적으로 NAT-T를 적용한 ESP를 사용한다. (2) PSK(Pre-Shared Key)는 VPN 피어가 사전에 동일하게 설정한 공유 비밀키로, IKE에서 상대 피어 인증에 사용할 수 있다. 장점: 인증서·CA 없이 설정이 간단하다. 단점: 피어가 많아질수록 키 배포·교체 관리가 어렵고, 키가 유출되면 해당 연결의 신뢰성이 훼손된다. | source-derived from Information Security Tistory; 2026-07-18 prompt restoration: NAT path and two independent answer parts made explicit; technical correction cross-checked against RFC 4302, RFC 3948, and RFC 7296; SAD 누락 여부는 제시 조건만으로 단정할 수 없다, and SAD is intentionally not a condition in this revised prompt; exact official wording unavailable |
| 15 | essay | HTTP 웹 서버 접속 후 로그인이 되지 않는 상황에서 동일 출발지 IP가 짧은 시간 동안 대량의 GET 요청을 지속 전송하는 것이 확인되었다. 다음을 서술하시오.<br>(1) 공격 유형<br>(2) 서버에 미치는 영향 | (1) HTTP GET Flooding 공격<br>(2) 대량의 HTTP GET 요청을 지속적으로 전송하여 서버의 TCP 세션 자원과 처리 자원을 모두 소진시킨다. 그 결과 정상적인 사용자가 접속 요청을 해도 서버가 새로운 연결을 수용하지 못하여 서비스 거부 상태가 발생한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: two requested answer parts are explicitly mapped; exact official wording unavailable |
| 16 | essay | 개인정보 영향평가 대상으로 대통령령으로 정한 기준에 해당하는 개인정보 파일 유형을 각각 서술하시오.<br>(1) 민감정보 또는 고유식별정보 처리 기준<br>(2) 개인정보 파일 연계 기준<br>(3) 일반 개인정보 파일 기준 | (1) 구축·운용 또는 변경하려는 개인정보 파일로서 5만 명 이상의 정보주체에 관한 민감 정보 또는 고유식별정보의 처리가 수반되는 개인정보 파일<br>(2) 구축·운용하고 있는 개인정보 파일을 해당 공공기관 내부 또는 외부에서 구축·운용하고 있는 다른 개인정보 파일과 연계하려는 경우로서, 연계 결과 50만 명 이상의 정보주체에 관한 개인정보가 포함되는 개인정보 파일<br>(3) 구축·운용 또는 변경하려는 개인정보 파일로서 100만 명 이상의 정보주체에 관한 개인정보 파일 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three requested answer slots are explicit; statutory answer remains source-derived |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
