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
date_updated: 2026-07-18
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
| 3 | short | 침입 탐지 방식의 빈칸을 채우시오.<br>(1) 미리 정의된 패턴과 일치하는 경우 탐지하는 방식<br>(2) 정상적인 행위 패턴에서 벗어난 이상 행위를 감지하는 방식<br>(3) 정상 패턴을 침입으로 잘못 판단하는 경우 | (1) 패턴 기반 탐지(Misuse Detection / 오용 탐지)<br>(2) 행위 기반 침입 탐지(Anomaly Detection / 이상 탐지)<br>(3) 오탐(False Positive) | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: each definition is explicitly mapped to its term; source image was visually inspected, but official KCA wording is unavailable |
| 4 | short | 대규모 데이터 저장소의 부하를 줄이기 위해 데이터를 캐시에 저장하는 도구로, 인터넷에 노출되고 권한 설정이 없으면 대규모 DDoS 증폭 공격 수단으로 악용될 수 있는 서비스의 명칭을 쓰시오. | Memcached(멤캐시드) | source-derived from Information Security Tistory; answer block present |
| 5 | short | 리눅스 `/etc` 디렉토리에 위치하며 패스워드 사용기간 만료, 패스워드 최대 사용기간, 패스워드 최소 변경기간 등 패스워드 정책을 설정할 수 있는 파일의 명칭을 쓰시오. | login.defs | source-derived from Information Security Tistory; answer block present |
| 6 | essay | 웹 애플리케이션 취약점 분석 방법의 빈칸을 채우시오.<br>(ㄱ) 분석 도구를 사용하여 외부 인터페이스만 살피며, 내부 코드 구조를 모르는 상태에서 외부 입력·출력을 분석하는 방법<br>(ㄴ) 코드를 직접 확인하고 실행하며, 소스 코드에 직접 접근하여 취약점을 분석하는 방법 | (ㄱ) 블랙박스 테스트(Black Box Test)<br>(ㄴ) 화이트박스 테스트(White Box Test) | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: each analysis method is explicitly mapped to its definition; source image was visually inspected, but official KCA wording is unavailable |
| 7 | essay | 정성적 위험 분석 방법론의 빈칸을 채우시오.<br>(ㄱ) 미지의 사건을 확률적 분포를 이용하여 최저·보통·최고의 위험 평가를 예측하는 방법<br>(ㄴ) 전문가가 익명 설문과 피드백을 반복하여 다양한 위험과 취약성에 대한 합의를 도출하는 방법 | (ㄱ) 확률 분포법<br>(ㄴ) 델파이법(Delphi Method) | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction preserves the 2026-07-17 boundary: Delphi is not direct group discussion; exact official wording unavailable |
| 8 | short | 어떤 기업이 위험에 대한 대응 전략으로 보험에 가입하는 방법을 선택하였다. 이는 어떤 위험 대응 전략인지 쓰시오. | 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; answer block present |
| 9 | essay | 보호 기준 수준을 정하고 모든 조직에서 기본적으로 필요한 보호대책을 선택하는 방식으로, 적정 보안 수준보다 높거나 낮은 보안 통제가 적용될 수 있는 위험 분석 기법의 명칭을 쓰시오. | 베이스라인 접근법(Baseline Approach) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 주요 재난과 컴퓨터 시스템 장애에 대한 서비스 복구 계획을 포함하고, 비즈니스 운영 위험에 대응해 리스크를 최소화하며 신뢰와 안정을 위한 계획을 수립하는 업무 연속성 관련 계획의 명칭과 영문 약어를 쓰시오. | BCP(Business Continuity Plan, 업무 연속성 계획) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | Apache `.htaccess`의 다음 설정 의미를 각각 서술하시오.<br>{{code:config}}(1) <FilesMatch "\.(php\|inc\|lib)"> order allow, deny; deny from all; </FilesMatch>\n(2) AddType text/html .html .php .htm .php3 .php4 .phtml .phps .inc .cgi .pl .shtml .jsp{{/code}} | (1) FilesMatch 지시자는 해당 확장자 파일의 직접 URL 접근을 제한하는 구형 Apache 접근제어 문맥이다. (2) AddType은 MIME type 매핑일 뿐이며, 별도 PHP/CGI handler가 있으면 실행을 보장되게 막지 못할 수 있다. 업로드 디렉터리는 웹 루트 밖 저장, 서버 측 allowlist·파일 시그니처 검증, 실행 handler 제거와 접근제어를 함께 적용해야 한다. | source-derived from Information Security Tistory; 2026-07-17 technical correction: MIME mapping alone is not execution prevention |
| 12 | essay | IPS는 일반적으로 인라인, IDS는 일반적으로 포트 미러링 방식으로 구성될 수 있다. 각각 이러한 방식으로 배치하는 이유와 설계 시 고려사항을 서술하시오. | IPS는 정책상 즉시 차단이 필요한 경로에 인라인으로 배치할 수 있고, IDS는 패킷 복사본 분석으로 서비스 경로에 미치는 영향을 줄일 수 있다. 다만 IPS의 내부망 배치 여부는 자산 중요도, 탐지 품질, fail-open/close 정책과 운영 절차에 따라 결정하며, 오탐 가능성만으로 내부망에는 IDS만 적합하다고 단정하지 않는다. | source-derived from Information Security Tistory; 2026-07-17 technical correction: deployment is a risk/policy decision |
| 13 | essay | IPSec의 AH와 ESP 프로토콜에 관한 물음에 답하시오. (1) AH 전송 모드와 터널 모드의 인증 구간과 암호화 구간을 서술하시오. (2) ESP 전송 모드와 터널 모드의 인증 구간과 암호화 구간을 서술하시오. (3) IPSec에서 사용하는 키 교환 프로토콜명을 쓰시오. | (1) AH는 암호화를 제공하지 않는다. 전송 모드에서는 변경 가능한 필드를 제외한 IP 헤더 부분과 페이로드를, 터널 모드에서는 외부 IP 헤더의 변경 가능한 부분을 제외한 필드와 전체 내부 IP 패킷을 무결성·출처 인증한다. (2) ESP 전송 모드는 IP 페이로드와 ESP trailer를 암호화하고, 터널 모드는 전체 내부 IP 패킷과 ESP trailer를 암호화한다. ESP의 무결성·출처 인증 적용은 SA 선택에 따르며 ESP header·payload·trailer가 범위이고 Authentication Data 자체는 포함하지 않는다. (3) IKE(Internet Key Exchange) 프로토콜 | source-derived from Information Security Tistory; 2026-07-17 technical correction: AH/ESP mode coverage and optional integrity |
| 14 | essay | 다음 Snort 룰의 각 항목 의미를 서술하시오.<br>{{code:snort}}alert tcp any any <> any [443,465,523] (content:"\|18 03 00\|"; depth:3; content:"\|01\|"; distance:2; within:1; content:!"\|00\|"; within:1; msg:"SSLv3 Malicious Heartbleed Request V2"; sid:1;){{/code}} | (1) 탐지 대상 포트를 443, 465, 523으로 지정한다. (2) 페이로드의 첫 3바이트 내에서 바이너리 값 18 03 00이 있는지 검사한다. (3) (2)가 끝난 위치에서 2바이트 떨어진 위치부터 1바이트를 검사하여 바이너리 값 01이 있는지 검사한다. (4) (3)이 끝난 위치에서 바로 1바이트를 검사하여 바이너리 값 00이 없는지 여부를 검사한다. (5) (1)~(4)의 탐지 룰에 모두 매칭되는 경우 로그에 "SSLv3 Malicious Heartbleed Request V2"로 기록한다. (6) 해당 룰의 식별자(sid)를 1로 지정한다. | source-derived from Information Security Tistory; image visually inspected, OCR attempted |
| 15 | essay | `robots.txt`의 개념을 서술하고 다음 설정의 의미를 각각 서술하시오.<br>{{reference}}User-agent: yeti\nUser-agent: googlebot\n(가) Allow: /\nUser-agent: googlebot-image\n(나) Disallow: /admin/\n(다) Disallow: /*.pdf${{/reference}} | (1) robots.txt는 협조하는 웹 크롤러에 대한 수집 지침이며, 브라우저·공격자의 접근을 통제하는 접근제어 수단이 아니다. (2) (가) yeti와 googlebot에 루트 이하 수집을 허용한다. (나)·(다)는 googlebot-image에 /admin/ 및 PDF 패턴 수집을 하지 말라고 요청한다. 실제 비공개 보호에는 인증·인가와 서버 접근통제가 필요하다. | source-derived from Information Security Tistory; 2026-07-17 technical correction: robots.txt is advisory, not access control |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
