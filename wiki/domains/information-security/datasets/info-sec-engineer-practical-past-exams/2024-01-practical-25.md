---
title: "정보보안기사 실기 25회 2024년 1회 실기 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "https://it-utopia.tistory.com/entry/정보보안기사-2024년-25회-정보보안기사-실기-기출문제-복원"
  - "https://blog.naver.com/stereok2/223481498564"
source_count: 2
provenance: inferred
summary: "정보보안기사 실기 25회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction, Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 25회 2024년 1회 실기 복원

## Scope
- Exam mapping: 2024년 1회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223481498564`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
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
| 10 | short | SSRF(Server Side Request Forgery)는 공격자가 서버를 신뢰하는 특정 서버나 네트워크 리소스에 대해 임의의요청을 보내도록 서버를 속이는 웹 보안 취약점이다. 주로 서버가 외부 입력을 기반으로 HTTP 요청을 생성하는 기능을 가지고 있을 때 발생한다. SSRF 공격 대응 기법에 대하여 ( )에 들어갈 용어를 기술하시오. [공격 대응 기법] - 사용자 입력을 기반으로 요청을 생성할 때는 허용된 도메인이나 IP주소에 대하여 ( A ) 리스트를 사용하여 필터링한다. - 만일, 무작위의 입력값을 사용해야 한다면 ( B ) 리스트 방식으로 필터링한다. | (A): 화이트, (B): 블랙 | source-derived; exact wording unverified |
| 11 | short | 위험 평가 이후 위험의 중요도에 따라 위험 처리 방안을 결정한다. ( )에 들어갈 위험 처리 방안을 기술하시오. - 위험 감소: 잠재적인 위험에 대해 정보보호 대책을 구현하여 자산, 취약점, 위협 중 하나의 수준을 낮춤 - ( A ): 현재의 위험을 받아들이고 잠재적 손실 비용을 감수 - ( B ): 위험이 존재하는 프로세스나 사업을 수행하지 않고 포기 - ( C ): 보험이나 외주 등으로 잠재적 비용을 제3자에게 이전 | (A): 위험 수용, (B): 위험 회피, (C): 위험 전가 | source-derived; exact wording unverified |
| 12 | short | 다음 설명에 해당하는 보안 솔루션 명칭을 기술하시오. - 2015년 가트너에서 처음 제시하였음 - 인공지능이 적용되어 지능형 탐지가 가능하고 빅데이터 기반 솔루션보다 진보된 형태의 보안 관제 솔루션 | SOAR | source-derived; exact wording unverified |
| 13 | essay | SW 보안 약점 진단원이 분석 단계 진단 시 검토해야 할 산출물 4가지와 그 내용을 간략히 설명하시오. | 요구사항 정의서(or 명세서): 기능·비기능 요구사항을 도출·합의해 작성한 문서. 요구사항 추적표(or 추적매트릭스): 요구사항과 개발 단계별 산출물의 일관성을 추적하는 문서. 유즈케이스 다이어그램: 액터와 시스템 제공 기능을 도식화한 문서. 유즈케이스 명세서: 액터와 유즈케이스 간 상호작용과 내부 업무 흐름을 상세히 설명한 문서. | source-derived; Naver cross-checked; official wording unverified |
| 14 | essay | 네트워크 스니핑을 탐지하는 다양한 방법(ping, arp, dns, decoy) 중 Ping 명령을 이용한 방법을 설명하시오 | 스니핑이 의심스러운 호스트에 NW에 존재하지 않은 MAC주소로 위조된 PING 메시지(ICMP Echo Request)를 보낸다. ICMP Echo Reply가 돌아온다면, 해당 호스트는 무차별 모드로 스니핑 중인 것으로 판단할 수 있다. | source-derived; exact wording unverified |
| 15 | essay | 위험관리를 위하여 정보자산의 중요도는 기밀성, 무결성, 가용성 등급을 기준으로 산정할 수 있다. 이 중 기밀성 등급에 대하여 ( )에 적절한 설명을 기술하시오. 1) H(상) 등급: 기밀성이 매우 높은 민감한 정보를 저장/처리하므로, 업무상 반드시 필요한 책임자(예: 고위 관리자)에 한하여 제한적으로 접근 가능 2) M(중) 등급: ( A ) 3) L(하) 등급: ( B ) - (A): 기밀성이 중간 정도인 민감 정보를 저장/처리하므로, 업무 담당자 및 관리자 등 허가된 직원만 접근 가능(예: 인사 정보, 내부 재무 정보 등) | (B): 기밀성이 낮은 민감하지 않은 정보를 저장/처리하므로, 내부의 일반 직원도 접근 가능하며, 공개된 정보인 경우 일반 대중도 접근 가능(예: 마케팅 자료, 공시 정보, 웹사이트 콘텐츠 등) | source-derived; exact wording unverified |
| 16 | essay | 공격이 탐지되었을 때, 침입탐지시스템(IDS)이 할 수 있는 행위를 4가지 기술하시오. 1) 이메일, SMS, 관리 콘솔 내 메시지 출력 등을 통하여 보안 관제 담당자에게 알린다. 2) 탐지된 침입 시도를 로그로 남긴다. (이후 분석 및 포렌식 조사를 위한 기초 자료로 사용) 3) 공격이 진행 중인 세션을 강제로 종료하여 침입을 차단한다. (IPS 기능이 포함된 IDS의 경우) 4) 다른 시스템(예: SIEM, 방화벽, 스위치, 라우터)과 통합되어 효과적인 대응 수행(예: 종합 분석, 차단 정책 설정 등) - 향 후 유사 공격이 들어오는 경우 예방이 가능하도록 IDS의 보안 정책 업데이트 | 호스트 기반 IDS의 경우, 탐지된 침입에 대해 특정 프로세스를 종료하거나, 파일 접근을 차단하는 등의 보호 조치 수행 | source-derived; exact wording unverified |
| 17 | practical | 홍길동은 인터넷 접속이 갑자기 느려져, PC 내 ARP 캐시 테이블 상태를 조회해 보았더니 다음과 같이 출력되었다. 각 물음에 답하시오. [ARP 캐시 테이블] 인터넷 주소 물리적 주소 유형 192.168.100.1 01-00-5e-00-00-02 동적 192.168.100.5 01-00-5e-00-00-02 동적 192.168.100.20 b0-e4-5c-7c-37-6e 동적 192.168.100.21 00-07-89-72-3d-04 동적 192.168.100.22 01-00-5e-7f-ff-fa 동적 (1) 위 리스트를 출력하기 위한 명령은? - arp -a (2) 어떤 공격이 일어난 것으로 판단할 수 있나? - ARP Redirect (192.168.100.1이 GW라고 가정함). 만약 해당 IP가 GW가 아니라면 공격명은 ARP Spoofing임 (3) 해당 공격이라고 판단한 이유는? - Gateway에 해당하는 IP(192.168.100.1)의 MAC 주소가 192.168.100.5를 사용하는 PC의 MAC주... | arp -s 192.168.100.1 00-0a-00-62-c6-09 | source-derived; exact wording unverified |
| 18 | practical | 윈도우 PE(Portable Executable) 파일은 윈도우 7과 같이 NT계열 운영체제에서 실행 가능한 파일 포맷이다. PE 파일은 실행 코드, 데이터, 리소스 및 메타데이터를 포함하는 구조를 가지며, 일반적으로 .exe(executable), .dll(dynamic link library), .sys(driver) 확장자를 가진 파일들을 포함한다. 악성파일의 경우에도 윈도우 OS에서 실행되기 위해 PE포맷을 사용하는데, 악성코드 작성자는 PE파일을 난독화하거나, PE헤더와 섹션 정보를 변형하여 디버깅 및 분석을 어렵게 만든다. 이러한 악성파일을 분석하는 3가지 방법을 설명하시오. | 자동 분석: 정적 분석 도구와 샌드박스 등을 사용해 파일 헤더, 섹션, 코드 패턴, 실행 행위를 자동 분석한다. 반자동화 분석: 자동화 도구 결과를 분석가가 검토하고 추가 분석한다. 수동 분석: 디버거 등으로 악성코드를 단계별로 실행·추적해 동작과 특정 행위 유발 코드를 식별한다. | source-derived; Naver cross-checked; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
