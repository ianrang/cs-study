---
title: "정보보안기사 실기 21회 2022년 4회 실기 복원"
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
  - "https://nhustler.tistory.com/36"
  - "https://nhustler.tistory.com/37"
  - "https://blog.naver.com/stereok2/222985383781"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 21회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 21회 2022년 4회 실기 복원

## Scope
- Exam mapping: 2022년 4회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Sendmail 스팸 릴레이 제한 설정 후 access DB 생성 명령. | `makemap hash /etc/mail/access.db < /etc/mail/access` | source-derived; Naver cross-checked; exact shell path wording unverified |
| 2 | short | SNMP를 비활성화하거나 제한하는 라우터 설정. | SNMP service/community 제거 또는 ACL로 SNMP 접근 제한 | source-derived; Naver cross-checked; exact command wording unverified |
| 3 | short | 조직이 수용 가능한 위험 수준. | 위험허용 수준 또는 목표 위험수준 | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | BCP 수립 단계. | 프로젝트 범위 설정, BIA, 복구전략 수립, 계획 개발, 교육·훈련·유지관리 등 | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | 지능형 지속 공격. | APT(Advanced Persistent Threat) | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | 불완전한 암호화 저장 취약점 점검 방법. | 중요정보 저장 여부와 암호화·해시·키관리 적정성 점검 | source-derived; Naver cross-checked; official wording unverified |
| 7 | short | IPSec 관련 빈칸 또는 기능 확인 문제. | AH/ESP, 터널/전송 모드, 인증·무결성·기밀성 등 IPSec 구성요소 | source-derived; Naver cross-checked; exact prompt wording unverified |
| 8 | short | 위험분석 방법 구분. | 기준선 접근법, 상세 위험분석, 복합 접근법 등 | source-derived; Naver cross-checked; official wording unverified |
| 9 | short | 취약점 공격에 쓰이는 익스플로잇 코드. | Exploit 또는 Exploit Code | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | Apache 업로드 가능 파일 크기 제한 명령/지시자. | `LimitRequestBody` | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | 침입탐지 방식인 오용 탐지와 이상 탐지의 정의와 장단점. | 오용 탐지는 알려진 패턴 기반으로 오탐이 낮지만 신규 공격에 약하고, 이상 탐지는 정상 행위와의 차이 기반으로 신규 공격 탐지가 가능하지만 오탐 가능성이 높음 | source-derived; Naver cross-checked; official wording unverified |
| 12 | essay | 미러사이트 정의, 장단점, RTO. | 원격지에 동일 시스템을 유지하는 재해복구 사이트로 빠른 복구가 가능하지만 구축·운영 비용이 높고 RTO가 짧음 | source-derived; Naver cross-checked; official wording unverified |
| 13 | essay | 비밀번호 작성 규칙. | 길이, 문자종류 조합, 추측 쉬운 문자열 금지, 주기적 변경 또는 유출 시 변경, 이전 비밀번호 재사용 제한 등 | source-derived; Naver cross-checked; current policy wording may vary |
| 14 | practical | SYN 플래그 차단 iptables 룰 설정. | TCP SYN 조건을 매칭해 DROP/REJECT하는 iptables INPUT/FORWARD 룰 | source-derived; Naver cross-checked; exact command wording unverified |
| 15 | practical | SLE, ALE, ARO, ROI 기반 위험 평가. | SLE는 단일 손실액, ARO는 연간 발생률, ALE는 SLE x ARO, ROI는 통제 비용 대비 손실 감소 효과 | source-derived; Naver cross-checked; official wording unverified |
| 16 | practical | DNS 존 파일 설정. | SOA/NS/A/MX/CNAME 등 레코드와 serial/refresh/retry/expire/minimum 값을 상황에 맞게 설정 | source-derived; Naver cross-checked; exact zone file wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
