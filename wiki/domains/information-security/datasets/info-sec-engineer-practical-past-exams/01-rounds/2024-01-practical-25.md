---
title: 정보보안기사 실기 25회 2024년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/8a0822a56fef290224846039024b4a89f05170f0b9caa38d0c1cc4d375dddca0/f4a42dff3dcc043a6703cf9f72e0fe49dbc9f7432bb4d73cbc9e6f9369d6b1b7/manifest.json
summary: '정보보안기사 실기 25회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction,
  Naver blog cross-check.'
---

## Overview




# 정보보안기사 실기 25회 2024년 1회 실기 복원

### Scope
- Exam mapping: 2024년 1회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223481498564`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 다음은 윈도우 OS의 계정 그룹 5가지 유형에 대한 설명이다. ( )에 들어갈 그룹명을 기술하시오. - Administrators: 도메인 또는 로컬 컴퓨터에 대한 모든 권한 보유 - ( A ): 일반 사용자보다는 많은 권한을 가지나, Administrators 그룹보다는 제한적인 권한 보유 - ( B ): 시스템 백업을 목적으로 모든 파일과 디렉터리 접근 가능 - ( C ): 도메인 및 로컬 컴퓨터를 일반적으로 사용하는 그룹 - Guests: 제한된 권한을 가지며 일시적으로 시스템을 사용하는 사용자를 위해 설계됨 | (A): Power Users, (B): Backup Operators, (C): Users | source-derived; exact wording unverified |
| 2 | short | 전자기기에서 발생되는 불필요한 전자 방사를 통해 민감한 정보를 도청하거나 유출하는 것을 방지하기 위한 일련의 표준과 기술을 무엇이라고 하는가? | TEMPEST(Telecommunications Electronics Material Protected from Emanating Spurious Transmissions) | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | IPSec이 제공하는 보안 기능 3가지를 기술하시오. | 접근제어, 비연결형 무결성, 데이터 근원지 인증, 재전송 방지, 기밀성, 제한적 트래픽 흐름의 기밀성 | source-derived; exact wording unverified |
| 4 | short | 공격자가 사용자와 서버 간의 활성화된 세션을 가로채어 사용자의 신원으로 서버와 통신을 시도하는 공격 기법을 무엇이라 하나? | 세션 하이재킹(Session Hijacking) | source-derived; exact wording unverified |
| 5 | short | 정보보호대책은 안전대책, 통제 혹은 위협을 감소시키기 위한 정보보호조치를 의미하며, 크게 다음과 같이 3가지로 구분된다. ( A )은/는 발생 가능한 잠재적인 문제들을 식별하여 사전에 대처하는 능동적인 개념의 통제로 2가지로 나눌 수 있다. ( B )란 관계자 이외의 사람이 특정 시설이나 설비에 접근할 수 없게 하는 각종의 통제를 의미하며, ( C )란 승인을 받지 못한 사람이 정보통신망을 통하여 자산에 대한 접근을 막기 위한 통제방법이다. | (A): 예방 통제, (B): 물리적 접근 통제, (C): 논리적 접근통제 | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | 메일 보안을 위해 릴레이 설정을 하려고 한다. 다음 보기에 기술된 요구사항을 충족시키기 위하여 /etc/mail/access에 설정해야 할 옵션값을 기술하시오. [보기] kca.or.kr 도메인의 메일은 릴레이를 허용한다. spam.com 도메인의 메일은 폐기한다. [/etc/mail/access 설정] kca.or.kr ( A ) spam.com ( B ) | (A): RELAY, (B): DISCARD | source-derived; exact wording unverified |
| 7 | short | 다음 기능을 제공하는 도구를 무엇이라고 하는가? - 사용자가 웹 사이트와 주고받는 HTTP/HTTPS 요청과 응답을 중간에서 가로채어, 수정하거나 분석할 수 있게 해주는 도구이다. - Paros, Burp Suite, ZAP(Zed Attack Proxy)가 대표적이며, 해킹 공격에도 사용되고, 웹 사이트의 보안 취약점 테스트 목적으로도 사용된다. | 웹 프락시(Web Proxy) | source-derived; exact wording unverified |
| 8 | short | IP 주소가 200.100.50.25이고, 서브넷 마스크가 255.255.255.192일 때, 서브넷 마스크를 2진수로 작성하시오. | 11111111 11111111 11111111 11000000 | source-derived; exact wording unverified |
| 9 | short | 프로그램에 의도적으로 잘못된 형식의 데이터 또는 무작위 데이터를 입력하여 프로그램의 취약점이나 버그를 찾는 SW 테스트 기법을 무엇이라고 하나? | Fuzzing(퍼징) | source-derived; exact wording unverified |
| 10 | short | SSRF(Server Side Request Forgery)는 공격자가 서버를 신뢰하는 특정 서버나 네트워크 리소스에 대해 임의의요청을 보내도록 서버를 속이는 웹 보안 취약점이다. 주로 서버가 외부 입력을 기반으로 HTTP 요청을 생성하는 기능을 가지고 있을 때 발생한다. SSRF 공격 대응 기법에 대하여 ( )에 들어갈 용어를 기술하시오. [공격 대응 기법] - 사용자 입력을 기반으로 요청을 생성할 때는 허용된 도메인이나 IP주소에 대하여 ( A ) 리스트를 사용하여 필터링한다. - 임의 URL이 필요한 기능도 DNS 재해석, 사설·link-local 주소, 리다이렉트, 프록시 경계를 검증하고 최소 권한 egress 정책을 적용한다. | (A): 화이트(allowlist). 블랙리스트만으로 임의 URL SSRF를 안전하게 필터링할 수 있다고 단정하지 않는다. | source-derived; 2026-07-17 technical correction: blacklist is insufficient SSRF defense |
| 11 | short | 위험 평가 이후 위험의 중요도에 따라 위험 처리 방안을 결정한다. ( )에 들어갈 위험 처리 방안을 기술하시오. - 위험 감소: 잠재적인 위험에 대해 정보보호 대책을 구현하여 자산, 취약점, 위협 중 하나의 수준을 낮춤 - ( A ): 현재의 위험을 받아들이고 잠재적 손실 비용을 감수 - ( B ): 위험이 존재하는 프로세스나 사업을 수행하지 않고 포기 - ( C ): 보험이나 외주 등으로 잠재적 비용을 제3자에게 이전 | (A): 위험 수용, (B): 위험 회피, (C): 위험 전가 | source-derived; exact wording unverified |
| 12 | short | 가트너가 2015년 제시한 사용자·엔터티 행위 분석 보안 기술로, 행위 기반 이상 탐지에 통계·분석 기법을 활용하는 솔루션 명칭을 기술하시오. | UEBA(User and Entity Behavior Analytics). 복원된 설명만으로는 SOAR와 혼동될 여지가 있어 기능 범위를 보정했다. | source-derived; 2026-07-17 technical correction: 2015 Gartner reference aligns with UEBA, not SOAR |
| 13 | essay | SW 보안 약점 진단원이 분석 단계 진단 시 검토해야 할 산출물 4가지와 그 내용을 간략히 설명하시오. | 요구사항 정의서(or 명세서): 기능·비기능 요구사항을 도출·합의해 작성한 문서. 요구사항 추적표(or 추적매트릭스): 요구사항과 개발 단계별 산출물의 일관성을 추적하는 문서. 유즈케이스 다이어그램: 액터와 시스템 제공 기능을 도식화한 문서. 유즈케이스 명세서: 액터와 유즈케이스 간 상호작용과 내부 업무 흐름을 상세히 설명한 문서. | source-derived; Naver cross-checked; official wording unverified |
| 14 | essay | 네트워크 스니핑을 탐지하는 다양한 방법(ping, arp, dns, decoy) 중 Ping 명령을 이용한 방법을 설명하시오 | 존재하지 않는 MAC 주소를 목적지로 하되 대상 호스트 IP로 ICMP Echo Request를 보내 응답 여부를 관찰하는 휴리스틱이 있다. 일반 NIC는 해당 프레임을 버리지만 promiscuous mode의 호스트가 응답할 가능성이 있다. 다만 응답은 가상화·브리지·중간 장비 등 대체 원인도 있어 스니핑의 단독 확정 증거가 아니며 추가 검증이 필요하다. | source-derived; 2026-07-17 technical correction: detection heuristic evidence boundary |
| 15 | essay | 위험관리를 위하여 정보자산의 중요도는 기밀성, 무결성, 가용성 등급을 기준으로 산정할 수 있다. 기밀성 등급 H(상)은 기밀성이 매우 높은 민감정보를 저장/처리하므로 업무상 반드시 필요한 책임자에 한해 제한 접근 가능한 등급이다. M(중), L(하) 등급 설명을 기술하시오. | M(중): 기밀성이 중간 정도인 민감정보를 저장/처리하므로 업무 담당자와 관리자 등 허가된 직원만 접근 가능하다. L(하): 기밀성이 낮은 민감하지 않은 정보를 저장/처리하므로 내부 일반 직원도 접근 가능하며 공개 정보는 일반 대중도 접근 가능하다. | source-derived; exact wording unverified |
| 16 | essay | 공격이 탐지되었을 때 침입탐지시스템(IDS)이 할 수 있는 행위를 4가지 기술하시오. | 관제 담당자에게 이메일/SMS/콘솔 등으로 알림을 보낸다. 침입 시도를 로그로 남긴다. IPS 기능이 포함된 경우 세션을 종료해 차단한다. SIEM, 방화벽, 스위치, 라우터 등과 연계해 차단 정책 설정 등 대응을 수행한다. 보안정책 업데이트나 HIDS의 프로세스 종료·파일 접근 차단도 가능하다. | source-derived; exact wording unverified |
| 17 | practical | 홍길동은 인터넷 접속이 갑자기 느려져 PC 내 ARP 캐시 테이블을 조회했다. `192.168.100.1`과 `192.168.100.5`가 같은 MAC `01-00-5e-00-00-02`로 표시되는 상황에서 1) 출력 명령, 2) 공격명, 3) 판단 이유, 4) 정적 ARP 대응 명령을 답하시오. | 1) `arp -a` 2) ARP spoofing 또는 캐시 이상을 의심한다. 3) `01:00:5e`는 IPv4 multicast MAC 범위이므로 일반 단말의 유니캐스트 ARP 매핑으로 부적절하다. 다만 실제 게이트웨이·스위치 MAC과 Proxy ARP/VRRP 같은 구성을 함께 확인한다. 4) 정적 ARP는 검증된 게이트웨이 MAC을 알 때만 예: `arp -s 192.168.100.1 <verified-unicast-mac>`로 설정한다. 임의 MAC을 답으로 넣지 않는다. | source-derived; 2026-07-17 technical correction: multicast MAC and static-ARP evidence requirement |
| 18 | practical | 윈도우 PE(Portable Executable) 파일은 윈도우 7과 같이 NT계열 운영체제에서 실행 가능한 파일 포맷이다. PE 파일은 실행 코드, 데이터, 리소스 및 메타데이터를 포함하는 구조를 가지며, 일반적으로 .exe(executable), .dll(dynamic link library), .sys(driver) 확장자를 가진 파일들을 포함한다. 악성파일의 경우에도 윈도우 OS에서 실행되기 위해 PE포맷을 사용하는데, 악성코드 작성자는 PE파일을 난독화하거나, PE헤더와 섹션 정보를 변형하여 디버깅 및 분석을 어렵게 만든다. 이러한 악성파일을 분석하는 3가지 방법을 설명하시오. | 자동 분석은 샌드박스 등으로 실행 행위를 수집하고, 정적 분석은 실행하지 않고 헤더·섹션·코드·문자열을 분석한다. 반자동 분석은 자동 결과를 분석가가 검토·보완하는 방식이며, 수동 동적 분석은 격리 환경의 디버거로 단계별 실행을 추적한다. 정적 분석과 샌드박스 실행 분석을 같은 방법으로 혼동하지 않는다. | source-derived; 2026-07-17 technical correction: static versus dynamic analysis |

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

- `raw/sources/clipping/8a0822a56fef290224846039024b4a89f05170f0b9caa38d0c1cc4d375dddca0/f4a42dff3dcc043a6703cf9f72e0fe49dbc9f7432bb4d73cbc9e6f9369d6b1b7/manifest.json`
