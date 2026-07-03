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
date_updated: 2026-07-03
source_paths:
  - "https://jaesung.tistory.com/92"
  - "https://jaesung.tistory.com/category/자격증/정보보안 기사?page=1..8"
  - "cs/information-security/round-1/docs/info-sec-engineer-criteria-2023-2026.pdf"
  - "cs/information-security/round-1/docs/외부자료-검증체크리스트.md"
  - "cs/information-security/round-1/01.system-security/03.linux-basic.md"
  - "cs/information-security/round-1/02.network-security/08.security-solutions-and-monitoring.md"
  - "cs/information-security/round-1/05.management-and-law/02.risk-assessment.md"
source_count: 7
provenance: inferred
summary: "2025년 4회 정보보안기사 실기 30회 복원 문항을 동일 구조로 정리하고 교차 검증한 문서."
evergreen: false
---

# 정보보안기사 실기 30회 2025년 4회 복원

## Scope
- This is a paraphrased reconstruction of the explicit 30th practical restoration post.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | /etc/shadow 해시 문자열의 `$id` 부분이 의미하는 값을 묻는 문항. | 일방향 해시 알고리즘 식별자. 예: 1=MD5, 5=SHA-256, 6=SHA-512. | round-1 Linux notes cover shadow; hash id mapping is standard crypt format. |
| 2 | short | IPsec에서 재생 공격 방지와 재전송 여부 판단에 쓰는 프로토콜/필드. | AH, Sequence Number | IPsec scope is explicit in KCA criteria; AH includes sequence number for anti-replay. |
| 3 | short | Windows 원격 세션을 net session 명령으로 종료할 때 쓰는 옵션. | delete 또는 del | Windows share/session administration concept. |
| 4 | short | LAN 스위치의 프레임 전송 방식 세 가지. | Cut-through, Fragment-free, Store-and-forward | Network switching fundamentals. |
| 5 | short | 전문가에게 반복 설문과 피드백을 수행해 합의를 도출하는 정성 예측 기법. | 델파이 기법 | round-1 risk notes define Delphi as expert-group anonymous consensus. |
| 6 | short | 전자증거의 수집·보존·분석·보고로 법적 증거능력을 확보하는 절차와 기술. | 디지털 포렌식 | Incident response/forensics scope in KCA criteria. |
| 7 | short | 시설 접근 제한과 시스템·데이터 접근 제한을 각각 부르는 통제 유형. | 물리적 접근통제, 논리적 접근통제 | KCA criteria includes access control and physical/logical controls. |
| 8 | short | 유출된 암호/해시 목록을 이용해 계정 로그인을 시도하거나 평문 암호를 찾는 공격 유형. | 크리덴셜 스터핑 | Source uses credential stuffing; note that hash cracking and credential stuffing can be distinguished in strict terminology. |
| 9 | short | 패치가 없거나 공개적으로 알려지기 전 악용되는 취약점. | 제로데이 취약점 | Vulnerability management concept. |
| 10 | short | Windows 공유 목록 확인과 공유 생성·삭제에 쓰는 명령. | net share | Windows network share scope appears in criteria. |
| 11 | short | DB 개인정보 마스킹에서 규칙 기반 문자 치환과 SQL 분석 기반 선택적 마스킹 방식. | 패턴 기반 마스킹, SQL 파싱 기반 마스킹 | DB security scope covers DB object/column access and masking-related controls. |
| 12 | short | 위험분석 기본 단계에서 보호 대상과 가치를 파악하는 분석과 약점 분석. | 자산 분석, 취약성 분석 | KCA criteria includes asset threat analysis and risk assessment. |
| 13 | essay | BYOD 모바일 오피스 보안 기술인 MDM, 컨테이너화, 모바일 가상화를 설명하는 문항. | MDM은 단말 정책·원격관리, 컨테이너화는 업무/개인 영역 분리, 모바일 가상화는 개인용/업무용 OS 영역 분리. | round-1 mobile management notes cover BYOD, containerization, mobile virtualization. |
| 14 | essay | 위험관리의 자산·위협·취약성 관계와 손실 발생 조건을 설명하는 문항. | 자산은 보호 대상, 위협은 손실 원인, 취약성은 위협이 이용하는 약점이다. 취약성이 없거나 보호대책이 충분하면 위협이 있어도 손실로 이어지지 않을 수 있다. | round-1 risk notes explicitly define risk as function of asset, threat, vulnerability, controls. |
| 15 | essay | EAM과 IAM의 공통 목적, EAM 관리 대상과 한계, IAM 개선점을 설명하는 문항. | 둘 다 계정·접근권한 통합관리 목적. EAM은 내부 시스템/애플리케이션 중심이라 범위와 자동화가 제한될 수 있고, IAM은 조직 전체 계정 수명주기와 권한 관리를 통합·자동화한다. | round-1 security solution notes cover SSO/EAM/IAM relationship with caution about vendor terminology. |
| 16 | essay | Snort 탐지 룰이 부정확할 때 발생하는 문제와 정확한 조건 정의 이유를 설명하는 문항. | 오탐과 미탐이 증가해 운영 효율과 보안 수준이 낮아진다. 패턴, 포트, 방향, 임계값 등을 정확히 정의해야 한다. | round-1 Snort notes cover rule structure and threshold/options. |
| 17 | practical | Linux 보안 설정: TMOUT, securetty, passwd/shadow 권한, world-writable file 탐색, umask, xinetd disable 지시어. | export TMOUT=600; /etc/securetty; /etc/passwd 644 및 /etc/shadow 400; find / -type f -perm -2; umask 022; disable | KCA criteria covers OS security settings, authentication, log/file permission management. |
| 18 | practical | `SELECT pw FROM member WHERE id=...` 구문의 의미, 취약점, 공격 입력값을 묻는 SQL Injection 문항. | ID 조건에 맞는 pw 조회. SQL Injection 취약. 예시 입력: `' or '1'='1` | KCA criteria explicitly includes SQL Injection. |

## Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for most technical topics; medium for item 8 terminology because the source answer is credential stuffing while the wording resembles password cracking using leaked hashes.
- Known normalization: item 17 preserves the source answer but `/etc/shadow` permission may be distribution-policy dependent; stricter settings such as 000/400 are commonly seen in exam answers.
