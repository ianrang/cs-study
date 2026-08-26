---
title: 정보보안기사 실기 22회 2023년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/c816535cca959b2e121c47635f6fa46c730a3c1b24dcb2fca034ddd6554e2436/aeb3764c219e5b0b8bbd7361be8b10cfcd8aac50e1471de1b011864f2ada2695/manifest.json
summary: '정보보안기사 실기 22회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check.'
---

## Overview






# 정보보안기사 실기 22회 2023년 1회 실기 복원

### Scope
- Exam mapping: 2023년 1회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 라우팅 프로토콜의 빈칸을 채우시오. (A)는 거리 벡터 알고리즘을 사용하는 오래된 내부 라우팅 프로토콜, (B)는 링크 상태 알고리즘을 사용하며 변화 시 즉시 갱신하고 주기적 refresh도 수행하는 내부 라우팅 프로토콜, (C)는 Cisco가 제안한 하이브리드 라우팅 프로토콜이다. | (A) RIP, (B) OSPF, (C) EIGRP | source-derived; 2026-07-17 wording correction: OSPF is not change-only |
| 2 | short | Unix 로그 파일명의 빈칸을 채우시오. (A)는 사용자의 가장 최근 로그인 시각과 접근 호스트 정보, (B)는 `su` 권한 변경 성공/실패 로그, (C)는 시스템에 로그인한 모든 사용자가 실행한 명령어 정보를 기록한다. | (A) `lastlog`, (B) `sulog`, (C) `acct`/`pacct` | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | `/etc/passwd` 정보 `test01:x:100:1000:/home/exam:/bin/bash`에서 `1000`, `/home/exam`, `/bin/bash`의 의미를 설명하시오. | `1000`: GID, `/home/exam`: 사용자 홈 디렉터리, `/bin/bash`: 로그인 셸 | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | HTTP 요청 메시지 입력값이 HTTP 응답 헤더에 포함될 때 응답이 여러 개로 분리되는 HTTP 응답 분할(Response Splitting) 취약점이 발생할 수 있다. 쿠키 탈취, XSS 등을 유발할 수 있는 이 공격에서 HTTP 요청 메시지에 삽입되는 개행 문자 2개를 쓰시오. | CRLF 또는 `%0d%0a` | source-derived; PDF compilation cross-check restored prompt condition |
| 5 | short | 원격 파일 삽입 취약점 대응책의 빈칸을 채우시오. 1) PHP 소스 코드에 (A) 함수가 존재하는지 확인한다. 2) PHP 설정 파일 (B)에서 `allow_url_include` 값을 (C)로 설정한다. | (A) `require` 또는 `include`, (B) `php.ini`, (C) `Off`. `allow_url_fopen`만 꺼서는 include/require URL wrapper 제어와 동일하지 않다. | source-derived; 2026-07-17 technical correction: PHP remote include directive |
| 6 | short | Snort에서 대량 패킷에 대응하기 위해 설정하는 Threshold 옵션의 type 3가지를 쓰시오. | `limit`, `threshold`, `both` | source-derived; Naver cross-checked; source typo `treshold` normalized |
| 7 | short | ARP request 요청을 보내는 경우 목적지 MAC 주소를 형식에 맞춰 기술하시오. | `FF:FF:FF:FF:FF:FF` | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | DNS 서비스의 빈칸을 채우시오. 1) DNS는 53번 포트를 사용하고 전송 계층 프로토콜로 (A)를 사용한다. 2) DNS 서버는 반복 질의 부하를 줄이기 위해 (B)를 사용하며 해당 정보 유지 기간을 (C)라고 한다. | (A) UDP/TCP, (B) Cache(DNS 캐시), (C) TTL(Time To Live) | source-derived; Naver cross-checked; official wording unverified |
| 9 | short | 애플리케이션 소스 코드를 보지 않고 외부 인터페이스나 구조를 분석하는 방식 (A)와, 개발된 소스 코드를 살펴보며 취약점을 찾는 방식 (B)를 쓰시오. | (A) 블랙박스 테스트, (B) 화이트박스 테스트 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | DBMS 조회 질의문 생성 시 검증방법 설계 고려사항의 빈칸을 채우시오. 1) DB 연결 계정은 (A)이 설정된 계정을 사용한다. 2) 외부 입력값이 삽입되는 SQL 쿼리문을 (B)으로 생성해 실행하지 않는다. 3) 동적 SQL 생성 시 (C)에 대한 검증을 수행한다. | (A) 최소권한, (B) 동적, (C) 입력값 | source-derived; Naver cross-checked; KISA software security guide basis |
| 11 | short | 개인정보의 안전성 확보조치 기준 중 접속기록 보관·관리의 빈칸을 채우시오. 개인정보처리자는 개인정보처리시스템 접속기록을 최소 (A) 이상 보관·관리해야 하며, 5만명 이상의 정보주체에 관한 개인정보를 처리하거나 (B) 또는 고유식별정보를 처리하는 시스템은 2년 이상 보관·관리해야 한다. | (A) 1년, (B) 민감정보 | source-derived; Naver cross-checked; current-law wording needs check |
| 12 | short | 위험관리 용어의 빈칸을 채우시오. (A): 내외부 위협과 취약점으로 인해 자산에서 발생 가능한 위험을 감소시키기 위한 관리적·물리적·기술적 대책. (B): (A)을 적용한 이후에도 남는 위험. (C): 조직에서 수용 가능한 목표 위험 수준으로 경영진 승인을 받아 관리해야 한다. | (A) 정보보호대책, (B) 잔여 리스크/위험, (C) 위험수용기준 또는 허용 가능한 위험 수준. 복원 원천의 `DoA` 약어 확장은 확인되지 않아 일반 약어 정답으로 단정하지 않는다. | source-derived; 2026-07-17 reconstruction-limit correction: unsupported DoA expansion |
| 13 | essay | BYOD 환경에서 모바일 오피스 서비스를 하려고 한다. 관련 보안 기술인 1) MDM(Mobile Device Management), 2) 컨테이너화, 3) 모바일 가상화를 각각 설명하시오. | MDM은 단말 정책·앱·분실통제를 관리하고, 컨테이너화는 업무/개인 영역을 분리하며, 모바일 가상화는 격리된 실행환경을 제공 | source-derived; PDF compilation cross-check restored prompt condition |
| 14 | essay | 위험 분석 방법인 1) 기준선 접근법, 2) 상세 위험 분석법에 대해 각각 개념, 장점, 단점을 설명하시오. | 기준선은 빠르고 표준화되나 과소/과대보호 위험이 있고, 상세 위험분석은 정확하지만 비용과 시간이 크다 | source-derived; PDF compilation cross-check restored prompt condition |
| 15 | essay | 쿠키 설정값 1) Secure, 2) HttpOnly, 3) Expires의 의미를 보안 측면에서 설명하시오. | Secure는 HTTPS 전송 제한, HttpOnly는 스크립트 접근 제한, Expires는 만료시각 지정 | source-derived; PDF compilation cross-check restored prompt condition |
| 16 | essay | DNS 증폭 공격에 사용되는 IP 공격 기법을 설명하고, 해당 공격 기법을 사용하는 이유를 설명하시오. | 출발지 IP spoofing을 이용해 피해자 IP로 대량 응답이 향하게 하며, 작은 질의 대비 큰 응답으로 증폭 효과를 얻음 | source-derived; PDF compilation cross-check restored prompt condition |
| 17 | practical | HTTP Request 로그 `GET /member/login.php?user_id=1' or '1' = '1'# &user_pw=foo HTTP/1.1`와 `GET /member/login.php?user_id=1' or '1' = '1 &user_pw=foo HTTP/1.1`을 보고 답하시오. 1) 해당 취약점은 무엇인가? 2) 그렇게 판단한 이유는? 3) 대응 방안은? | SQL Injection. 입력값이 쿼리 구조를 바꿀 수 있으면 취약하며 입력검증, PreparedStatement, 최소권한, 오류노출 제한으로 조치 | source-derived; PDF compilation cross-check restored prompt condition |
| 18 | practical | 개인정보의 안전성 확보조치 기준에서 요구하는 보호조치 5가지를 기술하시오. 예시는 접근통제, 접속기록의 위·변조 방지, 개인정보 암호화, 악성프로그램 등 방지, 물리적 안전조치 관점이다. | 내부관리계획, 접근권한 관리, 접근통제, 암호화, 접속기록 보관·점검, 악성프로그램 방지, 물리적 안전조치 등 | source-derived; PDF compilation cross-check restored prompt condition; current-law wording needs check |

### Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
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

- `raw/sources/clipping/c816535cca959b2e121c47635f6fa46c730a3c1b24dcb2fca034ddd6554e2436/aeb3764c219e5b0b8bbd7361be8b10cfcd8aac50e1471de1b011864f2ada2695/manifest.json`
