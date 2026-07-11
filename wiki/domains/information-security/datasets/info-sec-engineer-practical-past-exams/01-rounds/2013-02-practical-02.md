---
title: "정보보안기사 실기 2회 2013년 2회 실기 복원"
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
  - "https://information-security.tistory.com/292"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 2회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 2회 2013년 2회 실기 복원

## Scope
- Exam mapping: 2013년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 소스 IP가 정당한 범위인지 기준으로 트래픽을 허용하는 필터링 방식에서, 로컬 네트워크로 들어오는 트래픽 필터링, 로컬 네트워크에서 나가는 트래픽 필터링, 특정 IP 또는 대역을 가상 인터페이스로 보내 차단하는 기법의 빈칸 (가), (나), (다)를 채우시오. | 가 : Ingress 필터링 나 : Egress 필터링 다 : Blackhole 필터링(Null Routing) | source-derived from Information Security Tistory; answer block present |
| 2 | essay | 위험 분석 방법론의 빈칸을 채우시오. (A): 전문가 집단 토론으로 위험을 분석하며 짧은 기간에 결과를 도출할 수 있으나 위험 추정 정확도가 낮다. (B): 일정 조건에서 위험의 발생 가능한 결과를 추정하며 적은 정보로 전반적 가능성을 추론하고 관리자와의 의사소통을 원활히 한다. (C): 각각의 위협을 상호 비교해 우선순위를 도출하며 시간과 자원이 적게 소모되나 위험 추정 정확도가 낮다. | A : 델파이법 B : 시나리오법 C : 순위결정법 | source-derived from Information Security Tistory; prompt descriptions restored |
| 3 | short | UDP 69번 포트의 인증 없는 파일 전송 서비스를 악용하는 공격, 익명 FTP 접근 허용으로 발생하는 공격, FTP가 데이터 전송 목적지를 충분히 검사하지 않는 설계 문제를 이용해 제3의 시스템을 공격하는 기법의 명칭을 각각 쓰시오. | A : TFTP 공격 B : Anonymous FTP 공격 C : FTP Bounce Attack | source-derived from Information Security Tistory; answer block present |
| 4 | short | 정보보호 정책의 빈칸을 채우시오. 정책에는 중요 정보자산과 만족되어야 할 정보 특성을 선언하는 (A)가 제시되어야 한다. 중요한 업무·서비스·조직·사람·자산을 포함하도록 정책의 (B)를 설정해야 한다. 정책 수행에 필요한 경영진, 정보보호조직, 일반 직원 등의 (C)를 정의해야 하며, 최고경영자의 의지를 확인할 수 있도록 (D)로 승인되어야 한다. | A : 목적 B : 적용범위 C : 책임 D : 문서 | source-derived from Information Security Tistory; prompt descriptions restored |
| 5 | short | 보안 취약점 점검 도구의 빈칸을 채우시오. Tripwire는 파일 시스템의 (A)을 점검하는 도구이며, (B)는 Tenable사가 개발·배포한 취약점 점검 도구로 패스워드 취약점, TCP/IP 스택 DoS, 취약한 서버 설정 등 알려진 취약점을 점검하고 text, HTML 등 보고서를 제공한다. | A : 무결성 B : Nessus | source-derived from Information Security Tistory; prompt descriptions restored |
| 6 | short | 유닉스 기반 방화벽 룰로 외부 TCP 연결로부터 네트워크 서비스를 보호하고 허용·거부 정책 파일로 통제하는 도구, 명시적 접근 거부 파일, 명시적 접근 허용 파일의 빈칸 (A), (B), (C)를 채우시오. | A : TCP Wrapper(tcpwrapper) B : hosts.deny C : hosts.allow | source-derived from Information Security Tistory; answer block present |
| 7 | short | 정보보안 3요소의 빈칸을 채우시오. (A): 정보 유출 측면의 특성으로 인가된 사용자만 정보에 접근 가능해야 한다. (B): 정보 변조 측면의 특성으로 정보가 허가 없이 변경되지 않아야 한다. (C): 정보 상실 측면의 특성으로 인가된 사용자가 필요할 때 정보에 접근 가능해야 한다. | A : 기밀성(Confidentiality) B : 무결성(Integrity) C : 가용성(Availability) | source-derived from Information Security Tistory; prompt descriptions restored |
| 8 | short | 여러 호스트가 특정 대상에게 다량의 ICMP Echo Request를 보내게 하여 서비스 거부를 유발하는 공격, 라우터에서 차단해야 하는 브로드캐스트 패킷, 호스트가 IP Broadcast Address 수신 시 응답하지 않아야 하는 패킷의 빈칸 (A), (B), (C)를 채우시오. | A : 스머프(Smurf) B : Directed Broadcast C : ICMP Echo Request | source-derived from Information Security Tistory; answer block present |
| 9 | short | 공격자가 위조 MAC 주소를 지속적으로 전송해 스위치 MAC 주소 테이블을 가득 채우고, 스위치가 허브처럼 트래픽을 브로드캐스트하게 만들어 스니핑하는 공격 기법의 명칭을 쓰시오. | Switch Jamming(스위치 재밍) 또는 MAC Flooding | source-derived from Information Security Tistory; answer block present |
| 10 | essay | 위험 분석 구성 요소의 빈칸을 채우시오. (A): 위험을 보유하고 있는 대상으로 위험 발생 시 피해 규모 측정에 반드시 포함되는 요소. (B): 외부에서 발생해 (A)에 손실을 일으키는 요소로 발생 가능성으로 측정한다. (C): (A) 내부에 존재하는 약점으로, (B)은 이 요소를 활용해 위험을 발생시킨다. | A : 자산(Asset) B : 위협(Threat) C : 취약성(Vulnerability) | source-derived from Information Security Tistory; prompt descriptions restored |
| 11 | essay | 소프트웨어 보안 취약점의 7가지 유형을 각각 명칭과 함께 간략히 설명하시오. | (1) 입력 데이터 검증 및 표현 : 입력값에 대한 검증 부재로 발생하는 취약점 (SQL 인젝션, XSS 등) (2) 보안 기능 : 인증, 접근 제어, 암호화 등 보안 기능의 부적절한 구현 (3) 시간 및 상태 : 병렬 시스템에서 자원의 상태를 잘못 관리하는 경우 (레이스 컨디션 등) (4) 에러 처리 : 에러 발생 시 민감한 정보를 외부에 노출하거나 예외 처리 미흡 (5) 코드 품질 : 메모리 누수, 버퍼 오버플로우 등 코드 구현상의 결함 (6) 캡슐화 : 내부 데이터와 함수를 적절히 은닉하지 않아 발생하는 취약점 (7) API 오용 : 의도된 사용 방법과 다르게 API를 사용하여 발생하는 취약점 | source-derived from Information Security Tistory; answer block present |
| 12 | essay | `alert tcp any any -> any any` 룰에 `msg:"GET Flooding"`, `content:"GET / HTTP1."`, `nocase`, `depth:13`, `threshold: type threshold, track by_dst, count 10, seconds 1`, `sid:10000999`가 포함되어 있다. 이벤트명, `nocase`, `content`, `threshold`의 의미를 서술하시오. | (1) GET Flooding (2) 대소문자를 구분하지 않고 패턴을 탐지한다. (3) 패킷 페이로드에 "GET / HTTP1." 문자열이 포함된 경우 탐지한다. (4) 목적지 IP 주소를 기준으로 1초 동안 10번째마다 alert 액션을 수행한다. | source-derived from Information Security Tistory; context restored from source text |
| 13 | essay | 위험 분석 수행 시 정보자산 그룹핑에 관한 물음에 답하시오. | (1) 조사된 자산을 기밀성·무결성·가용성 평가 결과에 기초하여 자산의 유형·보안 특성·중요도가 같은 것을 묶어서 공통 자산 그룹으로 명시하는 것이다. (2) 관련 위협 및 취약성 평가와 위험 평가 수행 시, 자산 유형·보안 특성·중요도에 따라 결과가 달라지므로 같은 결과가 나오는 자산에 대한 동일한 작업의 반복을 방지하여 효율적으로 위험 분석을 수행할 수 있다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 정보통신망 이용촉진 및 정보보호 등에 관한 법률에 따라 고객 정보 보호를 위해 취해야 할 기술적·관리적 조치를 5가지 이상 서술하시오. | (1) 개인정보에 대한 접근 권한을 차등 부여하고 접근 권한의 변경·말소 이력을 관리한다. (2) 개인정보를 안전하게 저장·전송하기 위해 암호화를 적용한다. (3) 개인정보처리시스템에 대한 접속 기록을 보관하고 위변조 방지 조치를 한다. (4) 악성 소프트웨어 방지를 위해 보안 프로그램을 설치하고 주기적으로 갱신·점검한다. (5) 개인정보 보호를 위한 내부관리계획을 수립하고 시행한다. (6) 개인정보취급자에 대한 정기적인 교육을 실시한다. (7) 개인정보처리시스템에 대한 불법적인 접근 및 침해 사고 방지를 위한 시스템을 구축한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | IIS 웹 로그에서 정상 URL `login.asp?id=admin&pw=1234`와 공격 URL `login.asp?id=admin'--&pw=anything`가 확인되었다. 웹 서버가 내부 정보 유출 및 악성코드 유포지로 악용될 수 있는 공격명, 공격 URL 실행 결과, 취약점 제거 조치를 서술하시오. | (1) SQL Injection (2) SQL 쿼리문에서 '--로 인해 패스워드 검증 조건이 주석 처리되어 무력화되므로, 올바른 패스워드 입력 없이 admin 계정으로 인증이 우회되어 로그인이 가능해진다. (3) 모든 입력값을 검증하여 사용자가 입력한 값에 ', or, and, --, " 등 SQL 특수문자가 포함되지 않도록 필터링한다. | source-derived from Information Security Tistory; context restored from source text |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
