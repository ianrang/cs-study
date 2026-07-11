---
title: "정보보안기사 실기 31회 2026년 1회 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-07
date_updated: 2026-07-07
source_paths:
  - "user-provided Naver HTML table excerpt for 31회 문제·정답, 2026-07-07"
  - "https://cafeptthumb-phinf.pstatic.net/MjAyNjA0MTJfOTYg/MDAxNzc1OTg1MTQzNzg4.Kn6vPteZueR_hZgmsjjkF2gow1QzyxS5t0GlH7msV_gg.U1lSMtR4pBESVkTE30ndDPTpLsmKGf02Ea-cQjrllXYg.JPEG/4%EB%B2%88_%EA%B8%B0%EC%B6%9C.jpg"
source_count: 2
provenance: inferred
summary: "사용자가 제공한 HTML 표와 4번 이미지 문항을 기준으로 정보보안기사 실기 31회 2026년 1회 문제와 정답을 정리한 문서."
evergreen: false
---

# 정보보안기사 실기 31회 2026년 1회 복원

## Scope
- This is a paraphrased reconstruction from the user-provided HTML table for the 31st practical exam.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.
- Item 4 was image-only in the HTML table; the linked image was downloaded and visually inspected.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | `/etc/passwd` 파일 항목에서 `/etc/shadow`에 비밀번호가 암호화되어 저장되어 있을 때 패스워드 항목의 값을 쓰시오. | `x` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 1-64. |
| 2 | short | Man-in-the-middle 방식의 유형으로, DNS 서버보다 빠른 응답을 통해 DNS 응답을 조작하여 사용자가 의도하지 않은 웹사이트로 접속하게 만드는 공격 기법은 무엇인가? | DNS 스푸핑 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-94. |
| 3 | short | 리눅스 서버에서 외부 네트워크로의 ICMP 패킷 전송을 제한하기 위해 `iptables`를 사용하려고 한다. 내부에서 외부로 나가는 ICMP Echo Request(Type 8) 패킷을 차단하기 위한 `iptables -A OUTPUT -p ① --icmp-type ② -j ③`의 ①, ②, ③에 알맞은 속성값을 쓰시오. | ① `icmp` ② `8` ③ `DROP` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 4-11. |
| 4 | short | 보안 점검 도구 설명의 빈칸을 채우시오. `Tripwire`는 ①을/를 점검하는 대표적인 도구이다. ②은/는 미국 Tenable사가 개발하여 무료로 배포하는 취약점 진단 도구로, 패스워드 취약점·민감 데이터 접근·제어 가능 취약점 등을 점검하여 보고서를 제공한다. | ① 무결성 ② Nessus | User-provided 31st HTML table image URL downloaded and visually inspected; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-190, 3-193. |
| 5 | short | 윈도우 운영체제 환경에서 특정 서비스의 로그 파일 저장 경로이다. IIS 경로 `%SystemRoot%\system32\LogFiles\①\%SystemRoot%\system32\LogFiles\W3SVC1`, `%SystemRoot%\system32\LogFiles\MSFTPSVC1`와 DHCP 경로 `%SystemRoot%\System32\②`의 ①, ②에 들어갈 로그 파일 경로를 쓰시오. | ① `HTTPERR` ② `DHCP` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 1-33. |
| 6 | short | 임의의 길이를 갖는 임의의 데이터를 고정된 길이의 데이터로 매핑하는 암호화 방식은 무엇인지 쓰시오. | 해시 암호화 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 5-20. |
| 7 | short | 위험 관리 6단계의 빈칸을 채우시오. `위험 관리 전략 및 계획 수립 -> ① -> ② -> 정보보호 대책 선정 -> 정보보호 계획 수립 -> ③`. | ① 위험분석 ② 위험평가 ③ 실행 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 6-18. |
| 8 | short | 소프트웨어에 문제를 일으킬 수 있는 다양한 데이터를 입력하여 에러나 충돌 등의 반응을 분석해 취약성을 찾아내는 기법이며, 보안 취약점 탐지를 목적으로 하드웨어나 소프트웨어 모두에 적용 가능한 무작위 테스트 방식은 무엇인가? | 퍼징(Fuzzing) 테스트 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 필기 기본서 1-157. |
| 9 | short | 스팸메일 릴레이 제한 설정의 빈칸을 채우시오. `cat /etc/mail/①`에서 `R$* $#error $@5.7.1 $ : "550 Relaying denied"`를 확인하고, `cat /etc/mail/②`에는 `localhost.localdomain RELAY`, `localhost RELAY`, `127.0.0.1 RELAY`, `spam.com REJECT`가 있다. `makemap hash /etc/mail/③ < /etc/mail/access`에서 ①~③에 들어갈 파일명 또는 키워드를 쓰시오. | ① `sendmail.cf` ② `access` ③ `access.db` | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-243. |
| 10 | short | IIS에서 아웃바운드 설정으로 특정 응답 헤더를 제거할 때 사용하는 모듈을 쓰시오. | URL Rewrite(URL 재작성) | User-provided 31st HTML table; source reference column marked 신규. |
| 11 | short | 정보통신망법 제46조 내용이다. 타인의 정보통신서비스 제공을 위하여 집적된 정보통신시설을 운영·관리하는 자, 집적된 정보통신시설의 멸실·훼손·운영장애 피해 보상을 위한 보험 가입 주체, 보호조치 이행 점검 및 시정명령 대상에 공통으로 들어갈 용어를 쓰시오. | 집적정보통신시설(IDC) 사업자 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 필기 기본서 6-98. |
| 12 | short | 서버 및 보안 시스템에서 생성되는 로그 데이터를 빅데이터 기법으로 활용해 상관분석, 포렌식 기능, 지능적 위협 조기 경고 모니터링을 제공하는 지능형 보안 시스템은 무엇인가? | SIEM | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 2-195. |
| 13 | essay | 정보보호 최고책임자(CISO; Chief Information Security Officer)의 역할 및 책임(R&R) 4가지를 서술하시오. | ① 정보보호 관리체계의 수립·시행 및 개선 ② 정보보호 위험의 식별·평가 및 정보보호 대책 마련 ③ 정보보호 교육과 모의훈련 계획의 수립 및 시행 ④ 정보통신망법 또는 관계 법령에 따라 정보보호를 위하여 필요한 조치의 이행 | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 6-103. |
| 14 | essay | XSS 공격 2가지 종류와 정의를 서술하시오. | ① 저장형 XSS 공격: 악성 스크립트를 웹 애플리케이션의 데이터베이스에 저장해 사용자의 정보를 탈취하거나 리다이렉션하는 공격 기법. ② 반사형 XSS 공격: 사용자가 악성 스크립트 코드를 포함한 악성 URL을 클릭하면 서버 응답으로 악성 스크립트가 실행되어 사용자의 정보를 탈취하거나 리다이렉트하는 공격 기법. | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-51. |
| 15 | essay | 생체인식 보호 6가지 원칙과 내용을 서술하시오. | ① 비례성: 생체인식정보 처리 편익에 비해 개인정보 침해 위험성이 크지 않은지 고려하여 활용 여부를 판단한다. ② 적법성: 생체인식정보의 수집·이용·제공 등 처리 근거는 적법·명확해야 한다. ③ 목적제한: 생체인식정보를 정보주체에게 동의받은 인증·식별 이외의 목적으로 무단 활용해서는 안 된다. ④ 투명성: 생체인식정보 보호에 관한 사항을 정보주체에게 알기 쉽게 공개한다. ⑤ 안전성: 생체인식정보가 분실·도난·유출·위조·변조·훼손되지 않도록 안전하게 처리·관리한다. ⑥ 통제권 보장: 정보주체가 자신의 생체인식정보를 스스로 통제할 수 있는 수단을 제공한다. | User-provided 31st HTML table; source reference column marked 신규. |
| 16 | essay | OSI 7계층의 전송 계층에서 보안을 제공하는 SSL/TLS 핸드셰이크 과정에 대한 설명이다. Client Hello와 Server Hello 단계가 완료된 이후, 비대칭키(공개키) 암호화 방식과 대칭키 암호화 방식이 각각 어느 단계에서 어떤 용도로 사용되는지 핵심 과정을 포함하여 서술하시오. | 비대칭키 암호화는 Server Certification 단계를 통해 전달받은 서버의 공개키를 사용하여 클라이언트가 생성한 암호키를 암호화해 전달할 때 사용한다. 대칭키 암호화는 일련의 과정을 통해 클라이언트와 서버가 동일하게 생성한 세션 키를 사용하여 핸드셰이크 종료 이후 실제 데이터를 암호화하여 주고받을 때 사용한다. | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 2-165, 5-15. |
| 17 | practical | Fiddler 도구 점검 결과에 답하시오. 그림1에는 `HTTPS decrypted disabled`, `A SSLv3-compatible ClientHello handshake was found`, `Fiddler extracted for following parameter`, `Version:3.3(TLS/1.2)`가 표시된다. 그림2 HTML 코드에는 `Title: <alert>document.cookie();<alert>`가 표시된다. 1) 그림1의 문제 원인 2) 그림1의 문제 해결 방법 3) 그림2의 취약점 설명 4) 해당 취약점 대응방안을 쓰시오. | 1) `HTTPS decrypted disabled`는 Fiddler가 HTTPS 트래픽을 복호화하지 못하는 상태이고, 클라이언트가 SSLv3 호환 ClientHello를 보냄으로 인한 다운그레이드(POODLE 위험 존재) 문제다. 2) Fiddler Root 인증서 설치 및 신뢰 적용, SSL 3.0 비활성화, TLS 1.2 이상 강제(TLS 1.2/1.3). 3) 쿠키·세션 탈취 시도에 자주 쓰이는 XSS 페이로드로, 필터링·인코딩이 미흡하면 Reflected XSS 또는 Stored XSS로 공격 가능하다. 4) 스크립트 태그 제한, 모든 입력값 필터링, URL 디코딩을 활용한 우회 공격 대응, 웹 방화벽 적용. | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-135~136, 3-209~210. |
| 18 | practical | CSRF 관련 취약점 조치 코드와 물음에 답하시오. `@GetMapping("/write.do") public String write(HttpSession session) { session.setAttribute("CSRF_RANDOM_TOKEN", UUID.randomUUID().toString()); return "/board/write"; }` 1) Session과 Cookie를 서술하시오. 2) 해당 취약점의 명칭을 쓰고 설명하시오. 3) 웹 취약점 조치방안을 서술하시오. | 1) 쿠키는 클라이언트가 방문한 웹 사이트와 관련해 로컬에 저장되는 키와 값이 들어있는 데이터 파일이고, 세션은 클라이언트별 상태 정보를 서버에서 저장하는 기술이다. 2) CSRF는 사용자가 자신의 의지와 무관하게 공격자가 의도한 행위를 특정 웹 사이트에 요청하게 만드는 공격이다. 3) Referer 확인 후 같은 도메인 요청이 아니면 차단하고, 사용자 세션에 임의 난수 값을 저장한 뒤 요청마다 해당 난수를 포함시켜 전송하며, 중요 기능은 재인증으로 안전한 요청 여부를 확인한다. | User-provided 31st HTML table; 수제비 reference noted as 2026 수제비 정보보안기사 실기 기본서 3-64, 3-55. |

## Verification Notes
- Completeness: user-provided HTML table exposes 18 numbered items and answers.
- Image handling: item 4 was restored from the linked image by visual inspection; no additional image-only prompt remains in this file.
- Source boundary: this file preserves the user-provided reconstruction and answer table. It does not claim KCA official wording unless a separate official source is later acquired.
