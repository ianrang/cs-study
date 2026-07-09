---
title: "정보보안기사 실기 16회 2020년 2회 실기 복원"
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
  - "https://blog.naver.com/stereok2/222191200052"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 16회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 16회 2020년 2회 실기 복원

## Scope
- Exam mapping: 2020년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | /etc/shadow 파일 해시 알고리즘 식별자 | 1=MD5, 5=SHA-256, 6=SHA-512 | Naver answer cross-check; exact official wording unverified |
| 2 | short | 다음 업무를 총괄하는 사람을 쓰시오. 정보보호관리체계의 수립 및 관리·운영, 정보보호 취약점 분석·평가 및 개선, 침해사고의 예방 및 대응, 사전 정보보호대책 마련 및 보안조치 설계·구현. | CISO | Naver text extracted; official wording unverified |
| 3 | short | 기업의 정보보호에 대한 방향(목적, 활동 등)을 기술 및 솔루션과 독립적으로 가장 상위 개념으로 정의한 문서는 무엇인가? | Policy, 정보보호정책 | Naver text extracted; official wording unverified |
| 4 | short | 무선랜 보안 표준에서 사용하는 주요 암호화 알고리즘을 쓰시오. WEP: (A), WPA: (B), WPA2: (C) | WEP=RC4, WPA=TKIP, WPA2=AES/CCMP | Naver text extracted; official wording unverified |
| 5 | short | 엔드포인트 영역에 대한 지속적인 모니터링을 통해 행위 기반 위협 탐지, 분석, 대응 기능을 제공하는 솔루션은 무엇인가? | EDR(Endpoint Detection and Response) | Naver text extracted; official wording unverified |
| 6 | short | TLS 1.3에서 세션키를 합의하는 핸드셰이크 과정을 간소화하여 암호화 시간을 줄여주는 기능을 쓰시오. | 1-RTT와 0-RTT 지원 | Naver text extracted; official wording unverified |
| 7 | short | 프로그램에서 실행하는 시스템 콜을 추적할 수 있고, 바이너리 파일에 포함된 컴파일 경로 정보를 통해 프로그램을 진단하거나 디버깅할 수 있는 명령어를 쓰시오. 예: `(A) -e trace=open ps \| more` | strace | Naver text extracted; official wording unverified |
| 8 | short | 전사적 IT 인프라의 위협정보를 수집·분석·경보·관리하고, 공신력 있는 대외 정보보호기관의 위협정보를 수집·분석하여 APT 등 알려지지 않은 공격에 대한 조기 대응을 유도하는 정보보호 통합관리 시스템 (A)의 이름을 쓰시오. | TMS(Threat Management System) | Naver text extracted; official wording unverified |
| 9 | short | ISO/IEC 위험관리 모델에서 위험 구성 요소 간 관계를 나타내는 도식의 빈칸을 채우시오. 취약성은 (A)를 노출시켜 위험을 증가시키고, (B)는 위험에 의해 영향을 받으며, 보안대책은 위험을 (C)시킨다. | 위협, 자산, 감소 | Naver text extracted; official wording unverified |
| 10 | short | 전송 계층 프로토콜인 UDP 기반으로 통신을 수행하는 경우 SSL/TLS와 유사한 보안 기능을 제공하는 프로토콜명을 쓰시오. | DTLS | Naver text extracted; official wording unverified |
| 11 | essay | 쿠키에 설정되는 보안 기능과 관련하여 답하시오. (1) Secure 속성의 기능 (2) Secure 속성으로 대응 가능한 공격 (3) HttpOnly 속성 설정 시 쿠키 값 (4) HttpOnly 속성의 기능 (5) HttpOnly 속성으로 대응 가능한 공격 | Secure는 TLS 연결에서만 쿠키를 전송해 스니핑을 줄이고, HttpOnly는 JavaScript 접근을 막아 XSS 기반 쿠키 탈취를 줄인다 | Naver text extracted; official wording unverified |
| 12 | essay | 디지털 포렌식 5대 원칙 중 3가지를 설명하시오. | 정당성, 재현성, 신속성, 연계보관성, 무결성 중 요구 개수 기술 | Naver text extracted; official wording unverified |
| 13 | essay | 스팸 메일 방지 기술에 대하여 답하시오. (1) SPF 적용 시 수신자 측에서 확인할 수 있는 항목 (2) SPF 적용 시 수신 메일의 정당성 검증 방법 (3-1) DKIM에서 전자서명 주체 (3-2) DKIM에서 키 공유 방법 (4) SPF와 DKIM을 혼합한 기법의 명칭 | SPF는 발신 IP를 DNS TXT 정책으로 검증하고, DKIM은 개인키 서명과 DNS 공개키로 무결성을 확인하며, DMARC는 SPF/DKIM 결과 기반 처리 정책을 제공한다 | Naver text extracted; official wording unverified |
| 14 | essay | 두 개의 취약한 XML 코드에 대하여 답하시오. 코드1은 외부 엔터티 `<!ENTITY xxe SYSTEM "file:///etc/passwd">`를 선언하고 `<foo>&xxe;</foo>`를 참조한다. 코드2는 `lol`, `lol2`, ..., `lol9`처럼 엔터티가 다른 엔터티를 반복 참조한다. (1) 코드1은 어떤 공격인가? (2) 코드1의 공격 원리는? (3) 코드2를 통한 공격 실행 결과는? | XXE는 XML 외부 엔터티를 악용해 파일 노출·SSRF 등을 유발하며, 반복 엔터티 확장으로 Billion Laughs DoS가 가능하다 | Naver text extracted; official wording unverified |
| 15 | essay | 정보보호 위험평가에서 A/B 보호대책 적용 시 SLE, ALE, 보호대책 효과를 계산하고 더 효과적인 대책을 선정하시오. A 적용 시 AV=100,000, EF=0.2, ARO=0.5, 감소한 ALE=30,000, 운영비용=17,000이다. B 적용 시 AV=100,000, EF=0.8이며, 답안 기준으로 ALE와 효과를 비교한다. | A: SLE 20,000, ALE 10,000, 효과 13,000. B: SLE 80,000, ALE 20,000, 효과 16,000. 효과가 큰 B를 선정한다 | Naver text extracted; B-side source line partly truncated in local extraction; official wording unverified |
| 16 | essay | 공공기관의 개인정보 흐름표에서 문제가 되는 사항 4가지를 찾아 설명하시오. 흐름표 주요 내용은 다음과 같다. (1) 수집: 수집항목은 성명, 주민등록번호, 전화번호, 이메일이고 주민등록번호 수집 근거는 정보주체의 동의이다. (2) 저장: 저장항목은 성명, 주민등록번호, 전화번호, 이메일이며 주민등록번호를 MD5로 암호화한다. (3) 제공 및 파기: 주민등록번호를 DB 실시간 연동 방식으로 제공하고 암호화 적용 여부는 평문전송이며 파기주기는 영구보관이다. | 주민등록번호 수집 법령 근거 부재, 안전하지 않은 MD5 사용, 주민번호 평문 전송, 영구보관으로 파기주기 부재 | PDF compilation cross-check restored prompt condition |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
