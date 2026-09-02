---
title: 정보보안기사 실기 8회 2016년 2회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-18'
source_paths:
- raw/sources/clipping/450bdbbbd7c20be00a661899017225f98ec56e260de91404628124a62ba711ad/d8ac428080f74a3bf3babc88fc67c8a3fa40dc818cf5633bd56b72df43fac4c6/manifest.json
summary: 정보보안기사 실기 8회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 8회 2016년 2회 실기 복원

### Scope
- Exam mapping: 2016년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | MySQL 설정 파일의 현재 설정이 다음과 같을 때 외부 인터페이스에서 리스닝하도록 설정을 변경하시오.<br>{{code:config}}bind-address = 127.0.0.1{{/code}} | {{code:config}}bind-address = 허용할 서버 IP 또는 0.0.0.0{{/code}}로 변경한다. 이 설정은 리스닝 주소만 정하므로, 실제 외부 접속에는 방화벽·계정 host 권한·TLS 정책도 별도로 충족해야 한다. | source-derived from Information Security Tistory; 2026-07-17 wording correction: bind address alone does not authorize remote access |
| 2 | short | ISMS 인증 도입을 위한 정보보호 대책 항목 목록 `정보보호정책, (1), (2), 정보자산 분류, 정보보호 교육, 인적보안, 물리적 보안, 시스템개발 보안, 암호통제, (3), 운영보안, 침해사고관리, IT 재해복구`의 빈칸을 채우시오. | (1) 정보보호 조직 (2) 외부자 보안 (3) 접근 통제 | source-derived from Information Security Tistory; item list restored |
| 3 | short | WEP 설명의 빈칸을 채우시오. WEP는 IEEE 802.11b에서 적용되기 시작했으며 (A) 암호화 알고리즘을 사용한다. 40비트 WEP 비밀키와 임의로 할당되는 24비트 (B)를 조합한 총 64비트 키를 이용해 (A) 알고리즘으로 암호화한다. | A : RC4 B : IV(Initial Vector, 초기화 벡터) | source-derived from Information Security Tistory; prompt description restored |
| 4 | short | 현재 실행 중인 프로세스의 정보를 기록하는 가상 파일 시스템이 위치하는 리눅스 디렉토리의 명칭을 쓰시오. | /proc | source-derived from Information Security Tistory; answer block present |
| 5 | short | 정보보호 5가지 목표 `가. 기밀성`, `나. 무결성`, `다. (A)`, `라. (B)`, `마. (C)`의 빈칸을 채우시오. | A : 가용성(Availability) B : 인증(Authentication) C : 부인방지(Non-Repudiation) | source-derived from Information Security Tistory; sequence restored |
| 6 | short | TCP 3-Way Handshake에서 다음 흐름의 빈칸을 채우시오.<br>{{reference}}Client -- SYN(3478) --> Server\nClient <-- SYN(2324), ACK(A) -- Server\nClient -- SYN(B), ACK(C) --> Server{{/reference}} | A : 3479 (클라이언트 SYN 번호 3478 + 1), B : 3479, C : 2325 (서버 SYN 번호 2324 + 1) | PDF compilation cross-check restored the packet flow; RFC 9293 sequence-number rules cross-check the calculation. This is a non-official blog compilation, not KCA wording. |
| 7 | essay | setuid 관련 함수 호출에 답하시오. (1) 실행 파일 소유자가 root이고 setuid가 설정된 초기 상태에서 `getresuid()` 호출 시 `ruid`, `euid`, `suid` 값은 무엇인가? (2) `setuid(600)` 호출 이후 `getresuid()` 호출 시 각 값은 무엇인가? | (1) ruid : (실행 사용자 UID), euid : 0 (root), suid : 0 (root) (2) ruid : 600, euid : 600, suid : 600 | source-derived from Information Security Tistory; function-call prompts restored |
| 8 | short | DNS 관련 설명의 빈칸을 채우시오. 도메인네임 서비스는 IP 주소를 네임 주소로 변환해 주는 서비스이며, (A) 프로토콜을 사용한다. 동일 DNS 질의를 짧은 시간에 빈번히 수행하는 것을 방지하기 위해 (B)에 질의 결과를 일정 기간 저장한다. 소스 레코드는 지정된 (C) 시간 동안 리졸버 (B)에 존재한 뒤 삭제된다. | A : UDP(일반 질의 기준이며 DNS는 TCP도 사용할 수 있음), B : Cache(캐시), C : TTL(Time To Live) | PDF compilation cross-check restored all conditions. The exam blank expects UDP; it is not a claim that every DNS exchange uses UDP. This is a non-official blog compilation, not KCA wording. |
| 9 | essay | 개인정보 안전성 확보조치 기준에 관한 설명의 빈칸을 채우시오.<br>(A)를 처리하는 개인정보처리자는 인터넷 홈페이지를 통해 (A) 정보가 유출·변조·훼손되지 않도록 연 (B)회 이상 (C)을 점검하고 필요한 보안 조치를 하여야 한다. | (A) 고유식별정보<br>(B) 1<br>(C) 취약점 | source-derived from Information Security Tistory; 2026-07-18 prompt completeness correction cross-checked against the reconstruction source; statutory wording remains exam-time source-derived, not current-law substitution |
| 10 | short | 위험 처리 방법의 설명에 맞는 용어를 채우시오. (A): 별도 통제로 완전히 제거할 수 없는 잠재 손실 비용을 감수하고 사업을 진행한다. (B): 위험이 존재하는 프로세스나 사업을 수행하지 않고 포기한다. (C): 보험이나 외주 등으로 잠재 비용을 제3자에게 이전하거나 할당한다. | A : 위험 수용(Risk Acceptance), B : 위험 회피(Risk Avoidance), C : 위험 전가(Risk Transfer) | PDF compilation cross-check restored all three definitions; this is a non-official blog compilation, not KCA wording. |
| 11 | essay | IPSec 프로토콜에 대해 답하시오. (가) 전송 모드와 터널 모드의 차이점을 서술하시오. (나) 구성도 A는 호스트 ↔ 호스트 End-to-End 통신이고, 구성도 B는 라우터 ↔ 라우터 Gateway 간 통신이다. 각 구성도에 적절한 모드와 이유를 서술하시오. | (가) 전송 모드 : IP 페이로드(데이터)와 ESP 트레일러를 암호화하며 원본 IP 헤더는 그대로 유지한다. 터널 모드 : 원본 IP 패킷 전체(헤더 + 페이로드)와 ESP 트레일러를 암호화하고 새로운 IP 헤더를 추가한다. (나) 구성도 A : 전송 모드 — 호스트 종단 간 보안 서비스를 제공하며 IP 헤더를 그대로 사용한다. 구성도 B : 터널 모드 — 라우터 간 게이트웨이 구간에서 보안 서비스를 제공하며 원본 IP 패킷 전체를 보호한다. | source-derived from Information Security Tistory; topology prompts restored |
| 12 | essay | 파일 업로드 취약점에 관하여 각각 서술하시오.<br>(가) 취약점 존재 여부를 확인하는 방법<br>(나) 서버 측 대응 방법 | (가) 악성 스크립트가 첨부된 파일(예: .php, .jsp 등)을 게시판에 업로드하여 성공적으로 업로드되고 실행이 가능하면 파일 업로드 취약점이 존재하는 것으로 판단한다.<br>(나) 업로드 파일의 확장자에 대한 화이트리스트 필터링 정책을 적용하여 허용된 확장자(.jpg, .png, .pdf 등)만 업로드가 가능하도록 한다. 업로드된 파일을 별도의 저장 디렉토리에 보관하고 해당 디렉토리에서 서버 실행 권한을 제거한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: verification and defense requirements are explicitly mapped; exact official wording unavailable |
| 13 | essay | 보안관제 업무에서 사고 발생 후 시행되는 디지털 포렌식의 기본 원칙 중 연계보관성(Chain of Custody)의 원칙을 서술하고 각 단계를 설명하시오. | 증거물의 수집·이동(이송)·분석·보관·법정 제출 전 과정에서 담당자와 책임자를 명확히 기록하고 추적 가능하게 유지하는 원칙이다. PDF 편집본의 단계 열거 순서가 서로 달라, 핵심 단계와 연속적 책임·추적성을 채점 핵심으로 두며 단일 순서를 정답으로 고정하지 않는다. | PDF compilation cross-check restored the question. The compilation's own answer has inconsistent order for analysis/storage, so it cannot support a unique sequence; this is a non-official blog compilation, not KCA wording. |
| 14 | essay | OpenSSL HeartBleed 취약점에 관하여 각각 답하시오.<br>(가) 취약점 명칭<br>(나) 영향받는 버전 범위<br>(다) 대응 방법 | (가) OpenSSL HeartBleed 취약점(CVE-2014-0160)<br>(나) OpenSSL 1.0.1 ~ OpenSSL 1.0.1f, OpenSSL 1.0.2-beta ~ OpenSSL 1.0.2-beta1<br>(다) 영향받는 버전을 취약점이 패치된 최신 버전(OpenSSL 1.0.1g 이상)으로 업데이트한다. | [CVE-2014-0160](https://www.cve.org/CVERecord?id=CVE-2014-0160) cross-check; version 범위는 역사적 취약 버전 사실이며 KCA 공식 문구는 아니다. |
| 15 | essay | Linux crontab에 대해 답하시오. (가) cron에 현재 등록된 작업 내용을 보는 명령어, (나) `sis` 계정의 crontab을 편집하는 명령어, (다) 매주 일요일 새벽 3시에 `/home` 하위의 일반(비숨김) 항목을 삭제하는 crontab 설정을 작성하시오. | (가) crontab -l (나) crontab -u sis -e (다) `0 3 * * 0 rm -rf /home/* 1>/dev/null 2>&1`. 이 glob은 숨김 항목을 포함하지 않으므로, 원문 표현처럼 `/home`의 모든 항목을 삭제한다고 일반화하지 않는다. | source-derived from Information Security Tistory; 2026-07-17 wording correction: shell glob scope |
| 16 | essay | 정보보호관리체계(ISMS) 인증에 따라 정보보호 정책을 각각 어떻게 승인·공표하는지 서술하시오.<br>(1) 승인<br>(2) 공표 | (1) 정보보호 정책의 승인은 이해관계자의 검토를 거쳐 최고경영자의 승인을 받아야 한다.<br>(2) 정책의 공표는 정보보호 정책 문서를 모든 임직원 및 관련자에게 이해하기 쉬운 형태로 전달하여야 한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: approval and publication requirements are explicitly mapped; exact official wording unavailable |

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

- `raw/sources/clipping/450bdbbbd7c20be00a661899017225f98ec56e260de91404628124a62ba711ad/d8ac428080f74a3bf3babc88fc67c8a3fa40dc818cf5633bd56b72df43fac4c6/manifest.json`
