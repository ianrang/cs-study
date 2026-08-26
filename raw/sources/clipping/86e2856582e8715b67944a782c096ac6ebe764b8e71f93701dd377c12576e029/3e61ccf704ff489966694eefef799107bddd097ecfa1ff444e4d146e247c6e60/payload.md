---
title: "정보보안기사 실기 30회 2025년 4회 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-17
source_paths:
  - "<local-user-home>/Downloads/정보보안기사 실기 - 30회.pdf"
  - "<local-user-home>/Downloads/KakaoTalk_Photo_2026-07-17-13-29-26 002.jpeg"
  - "<local-user-home>/Downloads/KakaoTalk_Photo_2026-07-17-13-29-26 003.jpeg"
  - "https://jaesung.tistory.com/92"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 10
provenance: inferred
summary: "2025년 4회 정보보안기사 실기 30회 복원 문항을 이전 사용자 제공 PDF 기록, 사용자 제공 보조 사진, 기존 웹 복원 원천으로 교차 검증한 문서."
evergreen: false
---

# 정보보안기사 실기 30회 2025년 4회 복원

## Scope
- This is a paraphrased reconstruction of the explicit 30th practical restoration post and the user-provided 30th practical PDF.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Linux `/etc/shadow` 파일의 해시 문자열 `$id$salt$encryption-password`에서 밑줄 친 `$id`가 의미하는 값을 쓰시오. | 일방향 해시 알고리즘 식별자. 예: 1=MD5, 5=SHA-256, 6=SHA-512. | Jaesung source text cross-check; round-1 Linux notes cover shadow; hash id mapping is standard crypt format. |
| 2 | short | IPsec에서 재생 공격 방지와 재전송 여부 판단에 쓰는 필드. | AH와 ESP의 Sequence Number(및 수신 측 anti-replay window). 재생 방지는 AH에만 한정되지 않는다. | IPsec scope is explicit in KCA criteria; 2026-07-17 technical correction: ESP also has an anti-replay sequence number. |
| 3 | short | Windows 원격 세션을 `net session` 명령으로 종료할 때 쓰는 옵션. | `/delete` | Microsoft `net session` 문서의 구문은 `/delete`이며 대상 컴퓨터를 생략하면 로컬 서버의 모든 세션을 종료한다. |
| 4 | short | LAN 스위치의 프레임 전송 방식 세 가지. | Cut-through, Fragment-free, Store-and-forward | Network switching fundamentals. |
| 5 | short | 전문가에게 반복 설문과 피드백을 수행해 합의를 도출하는 정성 예측 기법. | 델파이 기법 | round-1 risk notes define Delphi as expert-group anonymous consensus. |
| 6 | short | 침해사고 발생 시 디지털 장비에서 전자적 증거를 수집·보존·분석·보고하여 법적 증거능력을 확보하는 절차와 기술을 통칭하는 용어를 쓰시오. | 디지털 포렌식 | Jaesung source text cross-check; incident response/forensics scope in KCA criteria. |
| 7 | short | 시설 접근 제한과 시스템·데이터 접근 제한을 각각 부르는 통제 유형. | 물리적 접근통제, 논리적 접근통제 | KCA criteria includes access control and physical/logical controls. |
| 8 | short | 다음 설명을 읽고 괄호 안에 들어갈 알맞은 용어를 `<보기>`에서 고르시오. “( )은 무차별 공격기법으로 대규모 데이터 로그인 자격증명을 무차별로 대입하여 계정을 탈취한다.” `<보기>`: 비밀번호 암호화, 역방향 무차별 대입 공격, 사전공격, 크리덴셜 스터핑. | 크리덴셜 스터핑 | 사용자 제공 사진의 문장·보기로 복원했다. “무차별 공격기법”은 문항의 분류 설명일 뿐 선택지의 `역방향 무차별 대입 공격`을 함께 정답으로 받는 근거가 아니다. 유출 비밀번호·자격증명 쌍을 여러 서비스에 재사용해 로그인하는 행위와 해시 평문 복구는 구별한다. 사진은 KCA 공식 시험지가 아닌 보조 복원 근거다. |
| 9 | short | 패치가 없거나 공개적으로 알려지기 전 악용되는 취약점. | 제로데이 취약점 | Vulnerability management concept. |
| 10 | short | Windows 공유 목록 확인과 공유 생성·삭제에 쓰는 명령. | net share | Windows network share scope appears in criteria. |
| 11 | short | DB 개인정보 마스킹에서 규칙 기반 문자 치환과 SQL 분석 기반 선택적 마스킹 방식. | 패턴 기반 마스킹, SQL 파싱 기반 마스킹 | DB security scope covers DB object/column access and masking-related controls. |
| 12 | short | 위험분석 기본 단계에서 보호 대상과 가치를 파악하는 분석과 약점 분석. | 자산 분석, 취약성 분석 | KCA criteria includes asset threat analysis and risk assessment. |
| 13 | essay | BYOD 환경에서 모바일 오피스 서비스를 하려고 한다. 관련 보안 기술인 1) MDM(Mobile Device Management), 2) 컨테이너화, 3) 모바일 가상화를 각각 설명하시오. | MDM은 모바일 기기를 도난·분실·악용 등으로부터 보호하기 위해 인증, 앱 화이트리스트, 원격 삭제, 탈옥 탐지, 스크린 캡처 방지, 카메라 제어 등 보안 정책을 적용·관리하는 기술이다. 컨테이너화는 하나의 모바일 기기 안에서 업무용 영역과 개인용 영역을 컨테이너라는 별도 공간으로 분리해 프라이버시를 보호하는 기술이다. 모바일 가상화는 가상화 기술로 개인용 OS 영역과 업무용 OS 영역을 완전히 분리하고 필요 시 업무용 OS로 전환해 사용하는 기술이다. | User-provided 30th PDF text extraction; Jaesung source text cross-check; round-1 mobile management notes cover BYOD, containerization, mobile virtualization. |
| 14 | essay | 정보보호 위험관리의 기본 개념인 자산, 위협, 취약성과 이들 사이의 관계를 설명하고, 위협 발생 시 손실이 실제로 발생하는 조건을 논하시오. | 자산은 조직이 보호해야 할 모든 유·무형의 대상이다. 위협은 자산에 손실을 초래할 수 있는 원하지 않는 사건의 잠재적 원인 또는 행위자다. 취약성은 위협의 이용 대상이 되는 자산의 기술적·관리적·물리적 약점이다. 위협이 발생해도 관련 취약성이 없거나 취약성에 대한 적절한 보호대책이 있으면 손실이 발생하지 않을 수 있다. | User-provided 30th PDF text extraction; Jaesung source text cross-check; round-1 risk notes explicitly define risk as function of asset, threat, vulnerability, controls. |
| 15 | essay | 다음 EAM, IAM에 대한 질문에 답하시오. (1) EAM과 IAM의 공통적인 기능 한 가지를 기술하시오. (2) EAM 관리 대상을 기술하시오. (3) EAM 문제점 두 가지를 기술하시오. (4) IAM에 추가된 기능을 설명하시오. | (1) 기업 계정과 접근권한의 중앙 관리. (2) 서버·OS·DB 등 내부 시스템 및 애플리케이션 계정. (3) 내부 시스템·애플리케이션 중심이라 조직 전체 사용자·고객 계정까지 확장하기 어렵고, 계정·권한 관리가 수작업 중심이면 운영 부담·비용이 커질 수 있다. (4) 직원·고객·외부 사용자·협력업체의 신원을 한 플랫폼에서 다루고, 계정 생성·권한 부여·변경·회수 같은 생명주기 관리를 자동화한다. | 사용자 제공 사진에서 네 개의 요구사항을 확인했다. 사진에는 답안 페이지가 없으므로 답안은 기존 PDF/웹 복원과 보안 솔루션 학습 자료를 교차한 최소 핵심어만 유지한다. EAM/IAM의 제품별 관리 범위·명칭은 다를 수 있으므로 특정 제품의 보편적 정의로 단정하지 않는다. 사진은 KCA 공식 시험지가 아닌 보조 복원 근거다. |
| 16 | essay | 침입탐지시스템 Snort에서 탐지 룰을 부정확하게 작성할 경우 발생할 수 있는 문제점 두 가지를 쓰고, 왜 룰의 조건을 최대한 정확하게 정의해야 하는지 설명하시오. | 탐지 룰이 부정확하면 정상 트래픽을 공격으로 오탐(false positive)하거나 실제 공격을 놓치는 미탐(false negative)이 증가한다. 이로 인해 운영 효율과 보안 수준이 저하되므로 패턴, 포트, 임계값을 정확히 정의해야 한다. | User-provided 30th PDF text extraction; Jaesung source text cross-check; round-1 Snort notes cover rule structure and threshold/options. |
| 17 | practical | 리눅스 서버 보안 강화 설정에 답하시오. 1) `/etc/profile` 등에 세션 타임아웃을 600초로 설정하는 환경변수와 export 명령. 2) root 계정 로그인 터미널 제한 파일. 3) `/etc/passwd`와 `/etc/shadow` 권한. 4) `/` 이하 world-writable 일반 파일 탐색 find 명령. 5) 그룹 및 기타 사용자 쓰기 권한을 제거하는 일반적 umask 값. 6) xinetd 관리 테스트 서비스 비활성화 지시어. | 1) `export TMOUT=600` 2) `/etc/securetty` 3) `/etc/passwd` 644, `/etc/shadow` 400 4) `find / -type f -perm -2` 5) `umask 022` 6) `disable` | User-provided 30th PDF text extraction; KCA criteria covers OS security settings, authentication, log/file permission management. |
| 18 | practical | 홈페이지 DB SQL 요청 `SELECT pw FROM member WHERE id='user01'`을 보고 답하시오. 1) 위 SQL 구문을 설명하시오. 2) 해당 쿼리에 어떤 취약점을 이용할 수 있는가? 3) 2번 취약점을 이용하여 `pw` 값을 알아내려면 `user01` 위치에 어떤 값을 입력해야 하는가? | 1) `member` 테이블에서 ID가 `user01`인 사용자의 `pw` 정보를 확인하는 쿼리다. 2) SQL Injection 공격. 3) `' or '1'='1` | User-provided 30th PDF text extraction; Jaesung source text cross-check; KCA criteria explicitly includes SQL Injection. |

## Verification Notes
- Completeness: user-provided PDF exposes 18 numbered items and answers.
- Confidence: high for most technical topics; medium for item 8 terminology because the source answer is credential stuffing while the wording resembles password cracking using leaked hashes.
- Known normalization: item 17 preserves the source answer but `/etc/shadow` permission may be distribution-policy dependent; stricter settings such as 000/400 are commonly seen in exam answers.
