---
title: "정보보안기사 실기 12회 2018년 2회 실기 복원"
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
  - "https://information-security.tistory.com/269"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 12회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 12회 2018년 2회 실기 복원

## Scope
- Exam mapping: 2018년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 악성코드와 광고의 합성어로, 온라인 광고 네트워크를 이용해 정상 광고처럼 위장하고 사용자가 클릭하거나 광고가 로드될 때 악성코드를 전파하는 공격 기법의 명칭을 쓰시오. | Malvertising(멀버타이징) | source-derived from Information Security Tistory; answer block present |
| 2 | short | IPSec은 OSI 7 Layer 중 (A) 계층에 보안성을 제공하는 표준화된 보안 프로토콜로 두 가지 세부 프로토콜을 가지고 있다. (B) 프로토콜은 송신자 인증과 무결성을 보장하며 프로토콜 식별번호 51번을 사용한다. (C) 프로토콜은 송신처 인증, 무결성, 기밀성을 보장하며 프로토콜 식별번호 50번을 사용한다. 빈칸 (A), (B), (C)를 채우시오. | A : 네트워크 계층(3계층) B : AH(Authentication Header) C : ESP(Encapsulating Security Payload) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 3 | short | HTTP Request의 파라미터가 HTTP Response 응답 헤더로 다시 전달될 때, 파라미터 내에 개행문자 (A) 혹은 (B)가 존재하면 HTTP 응답이 여러 개로 분리될 수 있다. 이 취약점을 통해 응답 메시지에 악의적인 코드를 주입하여 XSS 및 캐시 훼손을 유발하는 공격이다. 빈칸 (A), (B)를 채우시오. | A : CR(%0D) B : LF(%0A) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 4 | short | 데이터베이스 보안 위협에 관한 설명이다. (A)는 낮은 보안 등급의 정보를 조각별로 조합하여 높은 등급의 정보를 알아내는 방식이다. (B)는 접근 가능한 정당한 사용자 계정으로 수집한 정보를 통해 유추하여 높은 보안 등급의 정보에 접근하는 방식이다. (C)는 원본 정보를 위·변조하여 끼워 넣거나 바꿔치기하는 수법으로, 디스크 측에 대체할 자료를 만들어 두었다가 데이터를 추가하는 방식이다. 빈칸 (A), (B), (C)를 채우시오. | A : 집성(Aggregation) B : 추론(Inference) C : 데이터 디들링(Data Diddling) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 5 | short | logrotate 설정 파일의 각 옵션에 관한 설명이다. (A)는 주 단위로 로그 파일을 순환한다. `size 1M`은 로그 파일이 1MB가 되면 순환한다. (B)는 오래된 로그를 순환한 후 새로운 로그 파일을 생성한다. (C)는 로그를 압축하여 저장한다. 빈칸 (A), (B), (C)를 채우시오. | A : weekly B : create C : compress | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 6 | essay | 클라우드 서비스 유형 3가지를 명칭과 함께 서술하시오. | IaaS(Infrastructure as a Service) : 서버, 저장장치, 네트워크 등의 인프라 자원을 서비스 형태로 제공한다. PaaS(Platform as a Service) : 응용 프로그램 개발·배포·운영·관리 등을 위한 플랫폼 환경을 서비스 형태로 제공한다. SaaS(Software as a Service) : 응용 프로그램 소프트웨어를 서비스 형태로 제공한다. | source-derived from Information Security Tistory; answer block present |
| 7 | short | 개인정보보호법상 "접속기록"이란 개인정보취급자 등이 (A)에 접속한 사실을 알 수 있는 계정, 접속일시, 접속자 정보, (B) 등을 (C)으로 기록한 것을 말한다. 빈칸 (A), (B), (C)를 채우시오. | A : 개인정보처리 시스템 B : 수행업무 C : 전자적 | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 8 | short | 위험의 구성 요소를 포함하는 식 `위험 = (A) × (B) × (C) - 정보보호 대책`에서 빈칸 (A), (B), (C)를 채우시오. | A : 자산(Asset) B : 위협(Threat) C : 취약성(Vulnerability) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 9 | short | CC(공통 평가 기준) 구성 요소에 관한 설명이다. (A)는 보증 요구에 관련된 컴포넌트의 집합으로 구성된 패키지의 일종으로 미리 정의된 보증 수준을 나타낸다. (B)는 특정 소비자의 요구에 부합하는 구현에 독립적인 보안 요구사항의 집합이다. (C)는 식별된 평가대상의 평가를 위한 보안 요구사항과 구현 명세의 집합이다. 빈칸 (A), (B), (C)를 채우시오. | A : EAL(Evaluation Assurance Level, 평가 보증 등급) B : PP(Protection Profile, 보호 프로파일) C : ST(Security Target, 보안 목표 명세서) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 10 | short | 재난 복구 시스템 유형에 관한 설명이다. (A)는 주 센터와 동일한 수준의 정보기술 자원을 실시간 Active-Active 상태로 운영하는 방식이다. (B)는 장소 또는 전산실만 준비하며 비용이 저렴하지만 복구에 상당한 지연이 발생하는 방식이다. (C)는 (A)와 달리 동일한 수준의 자원을 보유하되 Stand-by 상태로 유지하는 방식이다. (D)는 (B)와 (C)의 중간 수준으로 중요도가 높은 정보기술 자원만 부분적으로 보유하는 방식이다. 빈칸 (A), (B), (C), (D)를 채우시오. | A : 미러 사이트(Mirror Site) B : 콜드 사이트(Cold Site) C : 핫 사이트(Hot Site) D : 웜 사이트(Warm Site) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 11 | essay | 서버 기반 논리적 망분리 기술 중 인터넷망 가상화와 업무망 가상화의 장점을 각각 2가지 이상 서술하시오. | 인터넷망 가상화 장점 : 가상화된 인터넷 환경을 제공하여 악성코드 감염을 최소화할 수 있다. 인터넷 환경이 악성코드에 감염되거나 해킹을 당해도 업무 환경은 안전하게 유지할 수 있다. 업무망 가상화 장점 : 가상화 서버 환경에 업무 데이터가 저장되므로 중앙 관리 및 백업이 용이하고 내부 정보 유출을 방지할 수 있다. 사용자 통제 및 관리 정책을 일괄 적용할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 신규 도입된 보안 장비의 계정 관리 취약점 측면에서 조치해야 할 사항 4가지 이상을 서술하시오. | (1) 기본 관리자 계정 변경 : 보안 장비에 기본 설정된 관리자 계정(default account)을 다른 계정명으로 변경한다. (2) 관리자 계정 패스워드 변경 : 기본 설정된 관리자 계정의 패스워드를 복잡도 규칙에 맞는 강력한 패스워드로 변경한다. (3) 계정별 권한 설정 : 등록된 계정별로 업무에 필요한 최소한의 권한만 부여한다. (4) 불필요한 계정 제거 : 사용하지 않거나 퇴직 등으로 불필요해진 계정을 제거하거나 비활성화한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | HTTP GET Flooding 탐지 Snort 룰 `alert tcp any any -> any 80 (msg:"HTTP Get Flooding Detect"; content:"GET / HTTP1."; (); nocase; threshold:type threshold, track by_src, count 10, seconds 1; sid:1000999)`을 보고, 차단 및 로그 action 2가지, content 문자열을 첫 13바이트 범위에서 검사하는 옵션, threshold 이벤트 발생 기준을 답하시오. | (1) drop, reject (2) depth:13 (3) 출발지 IP를 기준으로 매 1초 동안 10번째 이벤트마다 alert 액션을 수행한다. | source-derived from Information Security Tistory; context restored from source text |
| 14 | essay | 리눅스 명령어에 관한 물음에 답하시오. (1) 최근 로그인한 사용자 기록을 확인하는 명령어를 쓰시오. (2) 파일의 특수 속성(immutable, append only 등)을 확인하는 명령어를 쓰시오. (3) root 권한으로도 삭제되지 않는 파일의 불변(immutable) 속성을 해제하는 명령어를 쓰시오. | (1) last (2) lsattr (3) chattr -i 파일명 | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 15 | essay | NTP 취약점을 이용한 DDoS 공격 대응 방안이다. 다음 각 항목의 의미를 서술하시오. (1) `ntp -version` (2) `disable monlist` (3) `ntpdc -c monlist [점검 대상 NTP 서버 IP]` (4) `iptables -A OUTPUT -p udp --sport 123 -m length --length 100 -j DROP` | (1) NTP 데몬의 버전을 확인하여 monlist 기능이 비활성화된 최신 버전으로 업그레이드한다. (2) NTP 데몬의 monlist 기능을 비활성화한다. (3) 점검 대상 NTP 서버가 monlist 명령을 허용하는지 여부를 점검한다. (4) NTP 서버의 iptables를 이용하여 100바이트 이상의 NTP 응답 패킷을 차단한다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 16 | essay | 개인정보 파일에서 최소한 암호화가 필요한 항목 (A)과 대상별 암호화 알고리즘 (B)을 서술하시오. | (A) 암호화 필요 항목 : 비밀번호, 주민등록번호, 여권번호, 신용카드번호 (B) 비밀번호 : 복호화가 불가능하도록 안전한 일방향 해시 알고리즘을 사용한다. SHA-224/256/384/512 등을 사용하며, 레인보우 테이블 공격 방어를 위해 Salt 및 반복 횟수를 추가하여 암호 강도를 높인다. 주민등록번호·여권번호·신용카드번호 : 안전한 대칭키 암호화 알고리즘을 사용한다. 국내 알고리즘으로 SEED, ARIA-128/192/256이 있으며, 국제 표준으로 AES-128/192/256 등이 있다. 공개키 암호화 알고리즘을 사용하는 경우 키 길이 2048비트 이상의 RSA 등을 사용한다. | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
