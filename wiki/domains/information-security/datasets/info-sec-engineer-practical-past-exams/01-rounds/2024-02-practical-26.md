---
title: 정보보안기사 실기 26회 2024년 2회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/427ee7551bda6628e3ca517472a0f13fdb035608286540afbd06a1f7fac72c91/682fbb2d9fdbc016a9770b4fba19450727ea7bbddc74c2aa03ab5a3056b18276/manifest.json
summary: '정보보안기사 실기 26회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction,
  Naver blog cross-check.'
---

## Overview




# 정보보안기사 실기 26회 2024년 2회 실기 복원

### Scope
- Exam mapping: 2024년 2회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223603394618`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 리눅스에서 패스워드 최소 길이를 8자리 이상으로 설정하려고 한다. 패스워드 설정을 위한 파일명(A)과 설정 내용(B, C)을 기술하시오. # cat /etc/(A) (B) (C) | (A) : login.defs, (B) : PASS_MIN_LEN, (C) : 8 | source-derived; exact wording unverified |
| 2 | short | 무선네트워크에서는 다중 접속 시 상호 충돌을 회피하기 위하여 CSMA/CA 프로토콜을 사용한다. 이 경우, 타임아웃 설정은 어느 신호에 포함되는지 보기에서 2개를 선택하여 답하시오. (보기) CTS, DATA, RST, SYN, ACK, RTS | RTS, CTS | source-derived; exact wording unverified |
| 3 | short | Domain Name(URL)에 대한 IP 정보를 찾아주는 DNS는 먼저 클라이언트 영역에 위치한 (A) DNS 서버에 질의하여 IP정보를 찾고, 없으면 (B) DNS서버에 추가로 요청하여 IP 정보를 얻는다. | (A) : Recursive(Cache), (B) : Authoritative | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | 공격자가 HTTP 패킷의 헤더(Content-Length, Transfer Encoding: Chunked 등)를 변조하여 일반 사용자가 접근할 수 없는 Back-end 서버로 직접 보내 중요 정보 획득, XSS 공격유도, 서버 웹 캐시 포이즈닝 등을 수행하는 공격 기법을 무엇이라고 하는가? (보기) XSS, CSRF, SQL Injection, HTTP request smuggling | HTTP request smuggling | source-derived; exact wording unverified |
| 5 | short | 침입 탐지 시스템에서 공격이 아닌데 공격이라고 오판하는 것을 (A)라 하고, 공격인데 공격이 아니라고 오판하는 것을 (B)라고 한다. | (A) : 오탐(False Positive), (B) : 미탐(False Negative) | source-derived; exact wording unverified |
| 6 | short | XML 문서를 조회하는 기능을 구현해야 하는 경우 XML 쿼리에 사용되는 파라미터는 반드시 XML 쿼리를 조작할 수 없도록 필터링해서 사용하거나, 미리 작성된 쿼리문에 입력값을 자료형에 따라 바인딩해서 사용해야 한다. 관련하여 다음은 SW 설계시 고려해야 할 사항이다. (ㄱ) (A) 컴포넌트를 이용한 입력값 필터링: 외부입력값에서 XML 삽입 공격이 가능한 문자열들을 필터링하는 Validator 컴포넌트를 개발하여 XML 조회를 수행하는 애플리케이션 작성 시 입력값에 대한 검증 작업이 일괄 적용되도록 설계한다. (ㄴ) 개별 코드에서 입력값 (B) 하도록 시큐어코딩 규칙 정의: 각각의 컴포넌트에서 입력값에 대해 XML 삽입을 발생시킬 수 있는 문자열(", [, ], /, =, @ 등)을 제거 또는 안전하게 치환하여 사용할 수 있도록 시큐어코딩 규칙을 정의한다. (ㄷ) 안전한 (C) 를 사용하도록 시큐어코딩 규칙 정의: XML 조회를 수행하는 쿼리문 작성시 외부입력값이 쿼리문의 구조를 바꾸지 않도록 한다. | (A) : 공통 검증, (B) : 필터링, (C) : API | source-derived; Naver cross-checked; official wording unverified |
| 7 | short | 공격자들이 표적으로 삼은 조직 네트워크망에 침투한 후 오랜 기간 탐지를 회피하여 정보를 수집해 빼돌리는 고도의 지능형 표적 공격을 무엇이라고 하는가? | APT(Advanced Persistent Threat) | source-derived; exact wording unverified |
| 8 | short | 공격자가 자신의 TCP 윈도우 사이즈를 0으로 설정한 후 다수의 HTTP 패킷을 송신하여 웹서버가 정상적으로 응답하지 못하도록 만드는 공격 기법을 무엇이라 하는가? | Slow Read Attack | source-derived; exact wording unverified |
| 9 | short | XSS 취약점 유형에 대한 설명이다. ( )안에 들어갈 용어를 기술하시오. (1) (A) : 공격자의 입력값이 서버에 저장되지 않고 HTTP 응답에 그대로 포함되도록 허용되는 경우, 사용자가 공격자가 전달한 악의적인 링크에 접속할 때 발생 (2) (B) : 서버가 충분한 검증 없이 공격자로부터 입력받은 값을 저장한 뒤 다른 사용자에게 표시해 줄 때 발생 (3) (C) : 스크립트(일반적으로 자바스크립트)가 DOM을 제어하는 과정에서 공격자가 조작 가능할 때 발생 | (A) : Reflected XSS, (B) : Stored XSS, (C) : DOM Based XSS | source-derived; exact wording unverified |
| 10 | short | 침입탐지 시스템에는 호스트 컴퓨터의 내부 상태 또는 저장된 로그를 분석하여 침입을 탐지하는 (A), 통신망을 통해 전송되는 패킷 데이터를 분석하여 침입 여부를 판단하는 (B)가 있다. | (A) : HIDS(호스트기반 IDS), (B) : NIDS(네트워크기반 IDS) | source-derived; exact wording unverified |
| 11 | short | 위험을 구성하는 요소에 대한 설명이다. ( )에 들어갈 용어를 기술하시오. (1) (A) : 조직 내에서 가치를 가지고 있는 모든 것으로, 보호해야 할 대상 (2) (B) : 자산에 손실을 초래할 수 있는 원치 않는 사건의 잠재적인 원인 또는 행위자 (3) (C) : 위협의 이용 대상이 되는 자산의 잠재적인 약점 | (A) : 자산(Asset), (B) : 위협(Threat), (C) : 취약성 또는 취약점(Vulnerability) | source-derived; exact wording unverified |
| 12 | short | (A)는 조직의 자산에 대한 위험을 감수할 수 있는 수준으로 유지하기 위해 위험을 분석하고, 비용대비 효과적인 대책을 마련하는 일련의 과정이다. (A)의 단계는 (B), 위험평가, (C)이다. (B)는 잠재적으로 식별된 위험이 조직의 목표 및 운영에 미칠 가능성과 잠재적 영향을 분석하는 단계이다. (C)는 식별된 위험을 완화, 이전, 수용 또는 방지하기 위한 위험 처리 방안을 결정하는 단계이다. | (A) : 위험관리, (B) : 위험분석, (C) : 보호대책 선정(위험 처리) | source-derived; exact wording unverified |
| 13 | essay | 사용자가 `cmd.exe`를 실행하려고 할 때 UAC 팝업에 "다음 프로그램이 이 컴퓨터를 변경할 수 있도록 허용하시겠습니까?", 프로그램 이름 `Windows 명령 처리기`, 확인된 게시자 `Microsoft Windows`, 파일 원본 `이 컴퓨터의 하드 드라이브`가 표시되고, 관리자 암호 입력 안내와 함께 [예] 버튼은 비활성화되고 [아니오] 버튼만 활성화되어 있다. 1) 사용자가 윈도우 명령 처리기를 실행한 의도와 2) [예] 버튼이 비활성화된 이유를 설명하시오. | 1) 현재 권한으로 수행할 수 없는 명령을 처리하기 위해 명령 처리기를 관리자 권한으로 실행하려는 의도이다. 2) 화면만으로 관리자 계정 비활성·시스템 파일 손상을 확정할 수 없다. 표준 사용자 정책에서 elevation 요청을 자동 거부하거나 유효한 관리자 자격증명이 제공되지 않은 경우 등 UAC 정책·계정 상태를 확인해야 한다. | source-derived; 2026-07-17 technical correction: UAC evidence boundary |
| 14 | essay | 개인정보 처리가 수반되는 사업 추진 시 해당 사업이 개인정보에 미치는 영향을 사전에 분석하고 이에 대한 개선방안을 수립하여 개인정보 침해사고를 사전에 예방하기 위하여 개인정보 영향평가를 수행한다. 개인정보 영향평가 수행 시 고려해야 할 사항 5가지를 기술하시오. | 처리하는 개인정보의 수, 개인정보의 제3자 제공 여부, 정보주체의 권리를 해할 가능성 및 그 위험 정도, 민감정보 또는 고유식별정보의 처리 여부, 개인정보 보유기간 | source-derived; Naver cross-checked; official wording unverified |
| 15 | essay | 시스템 로그 점검 중 `device eth0 entered Promiscuous mode` 로그가 발견되었다. 1) Promiscuous mode의 의미, 2) 해당 모드에서 가능한 공격, 3) 대응 방법을 설명하시오. | 1) `eth0`이 목적지 MAC과 무관한 프레임을 수신하도록 하는 모드이다. 2) 패킷 스니핑에 악용될 수 있으나 가상화·브리지·모니터링에도 사용되므로 단일 로그만으로 공격을 확정하지 않는다. 3) 승인된 사용 여부를 확인하고 불필요하면 `ip link set dev eth0 promisc off`로 해제하며, 암호화 통신·스위치 포트 보안·변경 모니터링을 병행한다. | source-derived; 2026-07-17 technical correction: promiscuous mode is not conclusive attack evidence |
| 16 | essay | XSS(Cross Site Script) 공격의 정의와 공격 기법 2가지를 설명하시오. | XSS는 웹페이지에 악성 스크립트를 포함시켜 사용자 브라우저에서 실행되도록 하는 공격이다. Reflected XSS는 악성 URL 파라미터가 응답에 반사되어 실행되는 방식, Stored XSS는 게시판·프로필 등에 저장된 악성 스크립트가 다른 사용자 열람 시 실행되는 방식이다. DOM based XSS는 서버를 거치지 않고 DOM 생성 과정에서 실행되는 유형이다. | source-derived; exact wording unverified |
| 17 | practical | 데이터베이스 권한 관리가 미흡한 경우 비인가자가 DB에 접근해 정보 유출·훼손·파괴 등 악의적 행위를 할 수 있다. (1) DBA가 일반 사용자 또는 원격 사용자에게 부여하면 안 되는 권한 3가지, (2) 접근권한을 최소화할 수 있는 방법 4가지를 기술하시오. | (1) Oracle 예시로 `CREATE USER`, `DROP USER`, `DROP ANY TABLE`, `BACKUP ANY TABLE` 중 3가지. (2) 지정 IP에서만 원격 DB 접속 허용, DBA 외 시스템 테이블 접근 제한, 응용프로그램/DBA 계정 Role의 Public 설정 금지, `OS_ROLES`·`REMOTE_OS_AUTHENTICATION`·`REMOTE_OS_ROLES`를 `FALSE`로 제한, 최신 보안 패치·벤더 권고 적용 중 4가지. 이는 Oracle 예시이며 권한명·매개변수 지원 여부는 제품·버전에 종속된다. | PDF compilation cross-check restored the full question and listed choices. This is a non-official blog compilation, not KCA wording; the answer is explicitly Oracle-version-bound. |
| 18 | practical | 아래 취약점 점검 결과를 기반으로, 다음 물음에 답하시오. [취약점 점검 결과] # openssl version -a OpenSSL 1.0.1 14 May 2012 # openssl s_client -connect domain.com:8443 -tlsextdebug -debug -state \| grep -i heartbeat SSL_connect:before SSL initialization SSL_connect:SSLv3/TLS write client hello SSL_connect:SSLv3/TLS read server hello TLS server extension "heartbeat" (id=15), len=1 1) 취약점 명은? 2) 시스템적으로 해당 취약점을 조치하는 방법은? 3) 서비스적으로 해당 취약점을 조치하는 방법은? | 취약점명: 하트블리드(HeartBleed). 시스템 조치: OpenSSL을 취약점이 패치된 버전으로 업데이트하거나 Heartbeat를 비활성화해 재컴파일한다. 서비스 조치: 인증서와 개인키를 교체하고 취약점 조치 완료 후 사용자 비밀번호 재설정을 안내한다. | source-derived; Naver cross-checked; official wording unverified |

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

- `raw/sources/clipping/427ee7551bda6628e3ca517472a0f13fdb035608286540afbd06a1f7fac72c91/682fbb2d9fdbc016a9770b4fba19450727ea7bbddc74c2aa03ab5a3056b18276/manifest.json`
