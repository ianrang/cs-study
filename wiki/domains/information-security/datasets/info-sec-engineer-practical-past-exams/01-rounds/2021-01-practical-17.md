---
title: "정보보안기사 실기 17회 2021년 1회 실기 복원"
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
  - "https://blog.naver.com/stereok2/222396448808"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 17회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 17회 2021년 1회 실기 복원

## Scope
- Exam mapping: 2021년 1회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 로그인 인증 우회 공격 기법 | Pass the Hash | Naver answer cross-check; exact official wording unverified |
| 2 | short | DNS의 캐시 정보를 조작하여 가짜 사이트로 접속을 유도하는 공격 기법명을 쓰시오. | DNS Cache Poisoning | Naver text extracted; official wording unverified |
| 3 | short | 사이버 공격의 흐름을 분류하는 기준으로 사이버 킬 체인의 7단계를 확장하여 14단계로 구성된 모델명을 쓰시오. | MITRE ATT&CK | Naver text extracted; official wording unverified |
| 4 | short | 공격자가 미리 확보한 로그인 자격증명(ID, 패스워드)을 이용하여 사용자가 이용할 만한 다른 사이트에 무작위로 대입해 비인가 접속을 시도하는 공격기법명을 쓰시오. | Credential Stuffing | Naver text extracted; official wording unverified |
| 5 | short | 취약점의 코드베이스, 시간성(유효성), 악영향, 환경적 요소를 고려하여 공격 난이도와 피해 규모를 평가하고 점수화하는 보안 취약점 평가 기준을 쓰시오. | CVSS | Naver text extracted; official wording unverified |
| 6 | short | 침해사고 대응 7단계 `사고 전 준비과정 > 사고 탐지 > (A) > 대응 전략 체계화 > 사고 조사 > 보고서 작성 > 해결`에서 빈칸 절차를 쓰시오. | 초기 대응 | Naver text extracted; official wording unverified |
| 7 | short | 정보보호 관련 법령 용어를 쓰시오. (A)는 개인정보의 안전한 처리를 위한 개인정보보호 조직 구성, 개인정보취급자 교육, 개인정보 보호조치 등을 규정한 계획이다. (B)는 정상적인 보호·인증 절차를 우회하여 정보통신기반시설에 접근할 수 있도록 하는 프로그램이나 기술적 장치 등을 설치하는 방법의 공격 행위이다. (C)는 정보통신망 구축 또는 정보통신서비스 제공 이전의 계획·설계 과정에서 정보보호를 고려해 필요한 조치나 계획을 마련하는 것이다. | 내부관리계획, 전자적 침해행위, 정보보호 사전점검 | Naver text extracted; legal wording needs current-law check |
| 8 | short | 정보보호 관련 법령 용어를 쓰시오. (A)는 전기통신설비와 컴퓨터 이용기술을 활용하여 정보를 수집·가공·저장·검색·송신·수신하는 정보통신체제이다. (B)는 정보의 유출, 위·변조, 훼손 등을 방지하기 위한 하드웨어 및 소프트웨어 일체이다. (C)는 국가안전보장, 행정, 국방, 치안, 금융, 통신, 운송, 에너지 등의 업무와 관련된 전자적 제어·관리시스템이다. | 정보통신망, 정보보호시스템, 정보통신기반시설 | Naver text extracted; legal wording needs current-law check |
| 9 | short | ISO 27005 위험평가 절차를 쓰시오. (A)는 자산, 위협, 현 통제 현황, 취약점을 식별하는 단계이다. (B)는 시나리오별 영향 및 발생 가능성을 객관적·주관적으로 분석하는 단계이다. (C)는 기준에 따라 분석된 위험 목록의 우선순위를 산정하는 단계이다. | 위험식별, 위험분석, 위험수준평가 | Naver text extracted; official wording unverified |
| 10 | short | 개인정보의 안전성 확보조치 기준에서 "접속기록"은 개인정보취급자 등의 계정, (A), 접속지 정보, (B), 수행업무 등을 전자적으로 기록한 것이다. 개인정보를 다운로드한 것이 발견된 경우에는 (C)으로 정하는 바에 따라 사유를 확인해야 한다. | 접속일시, 처리한 정보주체 정보, 내부관리계획 | Naver text extracted; current-law wording needs check |
| 11 | essay | 개인정보보호법상 가명정보와 익명정보 | 가명처리는 추가정보 없이는 특정 개인을 알아볼 수 없게 처리하는 것이며, 가명정보는 통계작성·과학적 연구·공익적 기록보존 등에 활용 가능하고 익명정보는 더 이상 개인을 식별할 수 없는 정보다 | Naver answer cross-check; exact official wording unverified |
| 12 | essay | NAC의 물리적 구성 방법 두 가지와 특징을 설명하시오. | 인라인 방식은 트래픽 경로에 장비를 배치하여 실시간 탐지·차단에 유리하지만 물리적 재구성이 필요하고 장애 시 서비스 영향이 있다. 아웃오브밴드 방식은 스위치 일반 포트 또는 미러링 포트에 연결하여 구축이 쉽고 장애 영향은 작지만 탐지·차단 실시간성은 낮다. | PDF compilation cross-check restored prompt condition |
| 13 | essay | 정보보호최고책임자의 역할 및 책임을 4가지 이상 기술하시오. | 정보보호관리체계 수립·관리·운영, 정보보호 취약점 분석·평가 및 개선, 침해사고 예방 및 대응, 사전 정보보호대책 마련과 보안조치 설계·구현, 정보보호 사전 보안성 검토, 중요 정보 암호화 및 보안서버 적합성 검토 등 | PDF compilation cross-check restored prompt condition |
| 14 | essay | 웹로그 `192.168.0.10 - - [30/May/2021:10:10:10 +0900] "GET /script/..%c1%1c../winnt/system32/cmd.exe?/c+dir+c:\\ HTTP/1.1" 404 180`에 대하여 답하시오. (1) 어떤 취약점을 이용한 공격인가? (2) 공격 성공 여부와 판단 근거는? (3) 대응 방안 2가지는? | Unicode 취약점 기반 원격명령실행 시도이나 404 등으로 실패한 것으로 판단하며, 패치·입력 필터링·화이트리스트·웹/IIS 구성 분리·IPS 탐지로 대응한다 | Naver text extracted; official wording unverified |
| 15 | essay | Snort 룰 `alert tcp any any -> any 80 (msg:"GET Flooding"; content:"GET /HTTP1."; content:"USER"; content:!"anonymous"; content:"\|00\|"; depth:1; nocase; sid:1;)`에 대하여 `msg`, `content:"GET /HTTP1."`, `content:"USER"; content:!"anonymous"`, `content:"\|00\|"; depth:1`의 의미를 설명하시오. | msg는 경고 메시지, content:"GET"은 HTTP GET 탐지, content:"USER"와 !content:"anonymous"는 익명 아닌 FTP USER 조건, \|00\| depth 1은 첫 바이트 NULL 조건을 의미한다 | Naver text extracted; official wording unverified |
| 16 | essay | Apache 설정 `<Directory /> Options FollowSymLinks AllowOverride none Require all granted </Directory>`와 `<Directory /var/www> Options indexes FollowSymLinks AllowOverride none Require all granted </Directory>`를 보고 답하시오. (1) 발생 가능한 두 가지 문제점은? (2) 두 가지 문제점에 대한 대응 방안은? | Indexes로 디렉터리 인덱싱이 가능하고 FollowSymLinks로 심볼릭 링크 경유 접근이 가능하다. Indexes/FollowSymLinks 제거 또는 -Indexes/-FollowSymLinks, 필요 시 AllowOverride 설정으로 대응한다 | Naver text extracted; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
