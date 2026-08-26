---
title: 정보보안기사 실기 31회 2026년 1회 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-07'
date_updated: '2026-07-07'
source_paths:
- raw/sources/clipping/ddf71bc8d4bfcf328175f06c64edcb3d17236568dff5d63e3c0f514818d53ee7/9ffa138f4758f429f8fb0c52f92abc63acda38357cbcd949871c905b341748e2/manifest.json
summary: 사용자가 제공한 HTML 표와 4번 이미지 문항을 기준으로 정보보안기사 실기 31회 2026년 1회 문제와 정답을 정리한 문서.
---

## Overview





# 정보보안기사 실기 31회 2026년 1회 복원

### Scope
- This is a paraphrased reconstruction from the user-provided HTML table for the 31st practical exam.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.
- Item 4 was image-only in the HTML table; the linked image was downloaded and visually inspected.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | `/etc/passwd` 파일 항목에서 `/etc/shadow`에 비밀번호가 암호화되어 저장되어 있을 때 패스워드 항목의 값을 쓰시오. | `x` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 1-64. |
| 2 | short | Man-in-the-middle 방식의 유형으로, DNS 서버보다 빠른 응답을 통해 DNS 응답을 조작하여 사용자가 의도하지 않은 웹사이트로 접속하게 만드는 공격 기법은 무엇인가? | DNS 스푸핑 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-94. |
| 3 | short | 리눅스 서버에서 외부 네트워크로의 ICMP 패킷 전송을 제한하기 위해 `iptables`를 사용하려고 한다. 내부에서 외부로 나가는 ICMP Echo Request(Type 8) 패킷을 차단하기 위한 `iptables -A OUTPUT -p ① --icmp-type ② -j ③`의 ①, ②, ③에 알맞은 속성값을 쓰시오. | ① `icmp` ② `8` ③ `DROP` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 4-11. |
| 4 | short | 보안 점검 도구 설명의 빈칸을 채우시오. `Tripwire`는 ①을/를 점검하는 대표적인 도구이다. ②은/는 미국 Tenable사가 개발하여 무료로 배포하는 취약점 진단 도구로, 패스워드 취약점·민감 데이터 접근·제어 가능 취약점 등을 점검하여 보고서를 제공한다. | ① 무결성 ② Nessus | User-provided 31st HTML table image URL downloaded and visually inspected; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-190, 3-193. |
| 5 | short | 윈도우 운영체제 환경에서 특정 서비스의 로그 파일 저장 경로이다. IIS 경로 `%SystemRoot%\System32\LogFiles\①`, `%SystemRoot%\System32\LogFiles\W3SVC1`, `%SystemRoot%\System32\LogFiles\MSFTPSVC1`와 DHCP 경로 `%SystemRoot%\System32\②`의 ①, ②에 들어갈 로그 파일 경로를 쓰시오. | ① `HTTPERR` ② `dhcp` | User-provided 31st HTML table; 2026-07-17 technical correction: duplicated IIS path removed and DHCP path normalized. |
| 6 | short | 임의의 길이를 갖는 데이터를 고정된 길이의 값으로 매핑하는 일방향 함수는 무엇인지 쓰시오. | 해시 함수(Hash Function). 해시는 복호화 가능한 암호화 방식이 아니다. | User-provided 31st HTML table; 2026-07-17 terminology correction. |
| 7 | short | 위험 관리 6단계의 빈칸을 채우시오. `위험 관리 전략 및 계획 수립 -> ① -> ② -> 정보보호 대책 선정 -> 정보보호 계획 수립 -> ③`. | ① 위험분석 ② 위험평가 ③ 실행 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 6-18. |
| 8 | short | 소프트웨어에 문제를 일으킬 수 있는 다양한 데이터를 입력하여 에러나 충돌 등의 반응을 분석해 취약성을 찾아내는 기법이며, 보안 취약점 탐지를 목적으로 하드웨어나 소프트웨어 모두에 적용 가능한 무작위 테스트 방식은 무엇인가? | 퍼징(Fuzzing) 테스트 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 필기 기본서 1-157. |
| 9 | short | 스팸메일 릴레이 제한 설정의 빈칸을 채우시오. `cat /etc/mail/①`에서 `R$* $#error $@5.7.1 $ : "550 Relaying denied"`를 확인하고, `cat /etc/mail/②`에는 `localhost.localdomain RELAY`, `localhost RELAY`, `127.0.0.1 RELAY`, `spam.com REJECT`가 있다. `makemap hash /etc/mail/③ < /etc/mail/access`에서 ①~③에 들어갈 파일명 또는 키워드를 쓰시오. | ① `sendmail.cf` ② `access` ③ `access.db` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-243. |
| 10 | short | IIS에서 아웃바운드 설정으로 특정 응답 헤더를 제거할 때 사용하는 모듈을 쓰시오. | URL Rewrite(URL 재작성) | [Microsoft URL Rewrite Module outbound-rules guide](https://learn.microsoft.com/en-us/iis/extensions/url-rewrite-module/creating-outbound-rules-for-url-rewrite-module) cross-check; user-provided 31st HTML table remains non-official reconstruction. |
| 11 | short | 정보통신망법 제46조 내용이다. 타인의 정보통신서비스 제공을 위하여 집적된 정보통신시설을 운영·관리하는 자, 집적된 정보통신시설의 멸실·훼손·운영장애 피해 보상을 위한 보험 가입 주체, 보호조치 이행 점검 및 시정명령 대상에 공통으로 들어갈 용어를 쓰시오. | 집적정보통신시설(IDC) 사업자 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 필기 기본서 6-98. |
| 12 | short | 서버 및 보안 시스템에서 생성되는 로그 데이터를 빅데이터 기법으로 활용해 상관분석, 포렌식 기능, 지능적 위협 조기 경고 모니터링을 제공하는 지능형 보안 시스템은 무엇인가? | SIEM | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 2-195. |
| 13 | essay | 정보보호 최고책임자(CISO; Chief Information Security Officer)의 역할 및 책임(R&R) 4가지를 서술하시오. | ① 정보보호 관리체계의 수립·시행 및 개선 ② 정보보호 위험의 식별·평가 및 정보보호 대책 마련 ③ 정보보호 교육과 모의훈련 계획의 수립 및 시행 ④ 정보통신망법 또는 관계 법령에 따라 정보보호를 위하여 필요한 조치의 이행 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 6-103. |
| 14 | essay | XSS 공격 2가지 종류와 정의를 서술하시오. | ① 저장형 XSS 공격: 악성 스크립트를 웹 애플리케이션의 데이터베이스에 저장해 사용자의 정보를 탈취하거나 리다이렉션하는 공격 기법. ② 반사형 XSS 공격: 사용자가 악성 스크립트 코드를 포함한 악성 URL을 클릭하면 서버 응답으로 악성 스크립트가 실행되어 사용자의 정보를 탈취하거나 리다이렉트하는 공격 기법. | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-51. |
| 15 | essay | 생체인식 보호 6가지 원칙과 내용을 서술하시오. | ① 비례성: 생체인식정보 처리 편익에 비해 개인정보 침해 위험성이 크지 않은지 고려하여 활용 여부를 판단한다. ② 적법성: 생체인식정보의 수집·이용·제공 등 처리 근거는 적법·명확해야 한다. ③ 목적제한: 생체인식정보를 정보주체에게 동의받은 인증·식별 이외의 목적으로 무단 활용해서는 안 된다. ④ 투명성: 생체인식정보 보호에 관한 사항을 정보주체에게 알기 쉽게 공개한다. ⑤ 안전성: 생체인식정보가 분실·도난·유출·위조·변조·훼손되지 않도록 안전하게 처리·관리한다. ⑥ 통제권 보장: 정보주체가 자신의 생체인식정보를 스스로 통제할 수 있는 수단을 제공한다. | User-provided 31st HTML table; source reference column marked 신규. |
| 16 | essay | 전송 계층 위에서 동작하는 SSL/TLS 핸드셰이크 과정에 대한 설명이다. Client Hello와 Server Hello 단계가 완료된 이후, 비대칭키와 대칭키 암호 방식이 각각 어느 단계에서 어떤 용도로 사용되는지 핵심 과정을 포함하여 서술하시오. | 비대칭키는 서버 인증서 검증과 핸드셰이크 서명 검증에 사용된다. TLS 1.2의 RSA 키교환 cipher suite에서는 클라이언트가 premaster secret을 서버 공개키로 암호화할 수 있으나, 현대 TLS 1.3 및 (EC)DHE에서는 양측이 키 합의로 공유 비밀을 만들고 인증서는 서명에 사용된다. 이후 파생한 대칭 세션 키로 application data를 보호한다. | User-provided 31st HTML table; 2026-07-17 technical correction: TLS version and key-exchange boundary. |
| 17 | practical | Fiddler 도구 점검 결과에 답하시오. 그림1에는 `HTTPS decrypted disabled`, `A SSLv3-compatible ClientHello handshake was found`, `Fiddler extracted for following parameter`, `Version:3.3(TLS/1.2)`가 표시된다. 그림2 HTML 코드에는 `Title: <alert>document.cookie();<alert>`가 표시된다. 1) 그림1의 문제 원인 2) 그림1의 문제 해결 방법 3) 그림2의 취약점 설명 4) 해당 취약점 대응방안을 쓰시오. | (1) `HTTPS decrypted disabled`는 Fiddler의 HTTPS 복호화 설정·신뢰 루트 인증서 문제일 수 있다. `SSLv3-compatible ClientHello` 표기만으로 SSL 3.0 협상·POODLE을 확정하지 말고 실제 협상 버전과 cipher suite를 확인한다. (2) 테스트 환경에서만 Fiddler root 인증서를 신뢰하고, 서버·클라이언트의 SSL 3.0을 비활성화하며 최신 TLS를 강제한다. (3) 제공된 `<alert>` 태그는 표준 실행 태그가 아니므로 이것만으로 XSS 실행을 단정할 수 없지만, 신뢰되지 않은 값이 HTML 문맥에 출력되면 XSS 위험이 있다. (4) 입력 차단만 의존하지 말고 출력 위치별 인코딩, 안전한 DOM API, CSP, 세션 쿠키 보호를 적용한다. | User-provided 31st HTML table; 2026-07-17 technical correction: evidence boundary and XSS defense. |
| 18 | practical | CSRF 관련 취약점 조치 코드와 물음에 답하시오. `@GetMapping("/write.do") public String write(HttpSession session) { session.setAttribute("CSRF_RANDOM_TOKEN", UUID.randomUUID().toString()); return "/board/write"; }` 1) Session과 Cookie를 서술하시오. 2) 해당 취약점의 명칭을 쓰고 설명하시오. 3) 웹 취약점 조치방안을 서술하시오. | 1) 쿠키는 브라우저가 저장·전송하는 key/value이고, 세션은 서버가 보관하는 사용자 상태와 보통 세션 식별 쿠키의 조합이다. 2) CSRF는 피해자의 인증 상태를 이용해 의도하지 않은 상태 변경 요청을 보내게 하는 공격이다. 3) 코드는 토큰을 **생성만** 하므로 form/API에 토큰을 전달하고 서버에서 세션 토큰과 동등성·수명·사용자 결속을 검증해야 한다. state-changing GET을 피하고, Origin/Referer 검증과 SameSite는 방어 심층화로 병행하며 중요 기능은 재인증을 고려한다. | User-provided 31st HTML table; 2026-07-17 technical correction: token generation alone is not CSRF protection. |

### Verification Notes
- Completeness: user-provided HTML table exposes 18 numbered items and answers.
- Image handling: item 4 was restored from the linked image by visual inspection; no additional image-only prompt remains in this file.
- Source boundary: this file preserves the user-provided reconstruction and answer table. It does not claim KCA official wording unless a separate official source is later acquired.

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

- `raw/sources/clipping/ddf71bc8d4bfcf328175f06c64edcb3d17236568dff5d63e3c0f514818d53ee7/9ffa138f4758f429f8fb0c52f92abc63acda38357cbcd949871c905b341748e2/manifest.json`
