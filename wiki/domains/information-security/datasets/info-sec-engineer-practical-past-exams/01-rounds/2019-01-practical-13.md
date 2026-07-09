---
title: "정보보안기사 실기 13회 2019년 1회 실기 복원"
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
  - "https://information-security.tistory.com/260"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 13회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 13회 2019년 1회 실기 복원

## Scope
- Exam mapping: 2019년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 공격자가 위조 ARP Reply를 희생자에게 지속 전송해 ARP 캐시 테이블을 변조하고, 희생자 패킷이 공격자에게 전달되도록 만들어 트래픽을 도청하는 네트워크 공격 기법의 명칭을 쓰시오. | ARP Spoofing(ARP 스푸핑) | source-derived from Information Security Tistory; answer block present |
| 2 | short | 취약점·침해 요인과 대응 방안 정보를 제공하고 침해사고 발생 시 실시간 경보·분석 체계를 운영하며, 금융·통신 등 분야별 정보통신기반시설 보호를 위해 구축·운영되는 조직의 명칭과 영문 약어를 쓰시오. | ISAC(Information Sharing and Analysis Center, 정보공유·분석센터) | source-derived from Information Security Tistory; answer block present |
| 3 | short | 침입 탐지 방식에는 미리 정의된 패턴과 일치하는 경우 탐지하는 (1) 방식과, 정상적인 행위 패턴에서 벗어난 이상 행위를 감지하는 (2) 방식이 있다. 정상 패턴을 침입으로 잘못 판단하는 경우를 (3)이라 한다. 빈칸 (1), (2), (3)을 채우시오. | (1) 패턴 기반 탐지(Misuse Detection / 오용 탐지) (2) 행위 기반 침입 탐지(Anomaly Detection / 이상 탐지) (3) 오탐(False Positive) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 4 | short | 대규모 데이터 저장소의 부하를 줄이기 위해 데이터를 캐시에 저장하는 도구로, 인터넷에 노출되고 권한 설정이 없으면 대규모 DDoS 증폭 공격 수단으로 악용될 수 있는 서비스의 명칭을 쓰시오. | Memcached(멤캐시드) | source-derived from Information Security Tistory; answer block present |
| 5 | short | 리눅스 `/etc` 디렉토리에 위치하며 패스워드 사용기간 만료, 패스워드 최대 사용기간, 패스워드 최소 변경기간 등 패스워드 정책을 설정할 수 있는 파일의 명칭을 쓰시오. | login.defs | source-derived from Information Security Tistory; answer block present |
| 6 | essay | 웹 애플리케이션 취약점 분석 방법에 관한 설명이다. (ㄱ)은 분석 도구를 사용하여 외부 인터페이스만 살피는 방법으로, 내부 코드 구조를 모르는 상태에서 외부 입력·출력을 분석한다. (ㄴ)은 코드를 직접 확인하고 실행하여 분석하는 방법으로, 소스 코드에 직접 접근하여 취약점을 분석한다. 빈칸 (ㄱ), (ㄴ)을 채우시오. | ㄱ : 블랙박스 테스트(Black Box Test) ㄴ : 화이트박스 테스트(White Box Test) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 7 | essay | 정성적 위험 분석 방법론에 관한 설명이다. (ㄱ)은 미지의 사건을 확률적 분포를 이용하여 최저·보통·최고의 위험 평가를 예측하는 방법이다. (ㄴ)은 전문가 집단을 구성하여 다양한 위험과 취약점을 토론을 통해 분석하는 방법이다. 빈칸 (ㄱ), (ㄴ)을 채우시오. | ㄱ : 확률 분포법 ㄴ : 델파이법(Delphi Method) | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 8 | short | 어떤 기업이 위험에 대한 대응 전략으로 보험에 가입하는 방법을 선택하였다. 이는 어떤 위험 대응 전략인지 쓰시오. | 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; answer block present |
| 9 | essay | 보호 기준 수준을 정하고 모든 조직에서 기본적으로 필요한 보호대책을 선택하는 방식으로, 적정 보안 수준보다 높거나 낮은 보안 통제가 적용될 수 있는 위험 분석 기법의 명칭을 쓰시오. | 베이스라인 접근법(Baseline Approach) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 주요 재난과 컴퓨터 시스템 장애에 대한 서비스 복구 계획을 포함하고, 비즈니스 운영 위험에 대응해 리스크를 최소화하며 신뢰와 안정을 위한 계획을 수립하는 업무 연속성 관련 계획의 명칭과 영문 약어를 쓰시오. | BCP(Business Continuity Plan, 업무 연속성 계획) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | Apache `.htaccess` 설정의 의미를 각각 서술하시오. (1) `<FilesMatch "\.(php\|inc\|lib)"> order allow, deny; deny from all; </FilesMatch>` (2) `AddType text/html .html .php .htm .php3 .php4 .phtml .phps .inc .cgi .pl .shtml .jsp` | (1) FilesMatch 지시자를 이용하여 .php, .inc, .lib 확장자를 가진 서버 사이드 스크립트 파일에 대한 직접 URL 호출을 금지한다. 업로드된 악성 스크립트의 직접 실행을 방지하는 목적이다. (2) AddType 지시자를 이용하여 서버 사이드 스크립트 확장자를 text/html MIME 타입으로 재지정하여 해당 파일이 서버에서 실행되지 않고 HTML 텍스트로 처리되도록 함으로써 업로드된 스크립트의 실행을 방지한다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 12 | essay | IPS는 내부망 진입 지점에서 실시간으로 패킷을 분석하는 인라인 방식으로 구성되고, IDS는 포트 미러링 방식으로 패킷 복사본을 분석한다. 각각 이러한 방식으로 배치하는 이유를 서술하시오. | IPS는 실시간 차단을 목적으로 하므로 인라인 방식으로 네트워크 경로에 직접 배치되어야 하며, 외부의 악의적 침입을 즉시 차단하기 위해 내부·외부의 접점에 위치한다. 반면 IDS는 포트 미러링 방식으로 업무 데이터 흐름에 영향을 주지 않고 패킷을 복사하여 분석하므로 네트워크 장애 없이 침입을 탐지할 수 있다. IPS를 내부망에 배치하면 오탐으로 인한 정상 트래픽 차단으로 네트워크 장애가 발생할 수 있으므로 내부망에는 IDS를 배치하는 것이 적합하다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 13 | essay | IPSec의 AH와 ESP 프로토콜에 관한 물음에 답하시오. (1) AH 전송 모드와 터널 모드의 인증 구간과 암호화 구간을 서술하시오. (2) ESP 전송 모드와 터널 모드의 인증 구간과 암호화 구간을 서술하시오. (3) IPSec에서 사용하는 키 교환 프로토콜명을 쓰시오. | (1) AH 전송 모드 : 인증 구간 — IP 헤더의 변경 가능 필드를 제외한 전체 패킷 / 암호화 — 미지원 터널 모드 : 인증 구간 — New IP 헤더의 변경 가능 필드를 제외한 전체 패킷 / 암호화 — 미지원 (2) ESP 전송 모드 : 인증 구간 — ESP 헤더~ESP 트레일러 / 암호화 구간 — IP 페이로드~ESP 트레일러 터널 모드 : 인증 구간 — ESP 헤더~ESP 트레일러 / 암호화 구간 — 원본 IP 헤더~ESP 트레일러 (3) IKE(Internet Key Exchange) 프로토콜 | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 14 | essay | 다음 Snort 룰의 각 항목 의미를 서술하시오. `alert tcp any any <> any [443,465,523] (content:"\|18 03 00\|"; depth:3; content:"\|01\|"; distance:2; within:1; content:!"\|00\|"; within:1; msg:"SSLv3 Malicious Heartbleed Request V2"; sid:1;)` | (1) 탐지 대상 포트를 443, 465, 523으로 지정한다. (2) 페이로드의 첫 3바이트 내에서 바이너리 값 18 03 00이 있는지 검사한다. (3) (2)가 끝난 위치에서 2바이트 떨어진 위치부터 1바이트를 검사하여 바이너리 값 01이 있는지 검사한다. (4) (3)이 끝난 위치에서 바로 1바이트를 검사하여 바이너리 값 00이 없는지 여부를 검사한다. (5) (1)~(4)의 탐지 룰에 모두 매칭되는 경우 로그에 "SSLv3 Malicious Heartbleed Request V2"로 기록한다. (6) 해당 룰의 식별자(sid)를 1로 지정한다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 15 | essay | `robots.txt`의 개념을 서술하고 다음 설정의 의미를 각각 서술하시오. `User-agent: yeti`, `User-agent: googlebot`, `(가) Allow: /`, `User-agent: googlebot-image`, `(나) Disallow: /admin/`, `(다) Disallow: /*.pdf$` | (1) robots.txt는 검색 엔진의 자동 크롤링 도구(웹 로봇)에 대하여 웹 사이트 내 특정 페이지나 디렉토리의 접근 허용 여부를 제어하기 위한 파일이다. (2) (가) 검색 엔진 로봇(yeti, googlebot)에 대하여 루트 디렉토리(/) 이하의 모든 파일 및 디렉토리 접근을 허용한다. (나) googlebot-image 로봇에 대하여 /admin/ 폴더에 대한 접근을 허용하지 않는다. (다) googlebot-image 로봇에 대하여 .pdf 확장자를 가진 모든 파일에 대한 접근을 허용하지 않는다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
