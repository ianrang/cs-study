---
title: "정보보안기사 실기 20회 2022년 2회 실기 복원"
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
  - "https://nhustler.tistory.com/38"
  - "https://nhustler.tistory.com/39"
  - "https://blog.naver.com/stereok2/222860841923"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 20회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 20회 2022년 2회 실기 복원

## Scope
- Exam mapping: 2022년 2회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Telnet으로 웹 서버에 접속한 뒤 허용 HTTP method를 확인하는 명령. | OPTIONS | source-derived; Naver cross-checked; official wording unverified |
| 2 | short | 전문가 토론, 조건별 결과 추정, 서술적 순위 결정 위험분석 방법. | 델파이법, 시나리오법, 순위결정법 | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | 기준선·상세·복합 위험분석 접근법 구분. | 베이스라인 접근법, 상세 위험분석, 복합 접근법 | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | 사용자 중심, 보안등급 기반, 역할 기반 접근통제 모델. | DAC, MAC, RBAC | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | IDS 탐지 정책에서 정상 행위를 이상으로 판단하거나 이상 행위를 놓치는 상황. | 오탐(False Positive), 미탐(False Negative) | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | IPSec에서 지원하는 보안 서비스. | 기밀성, 제한된 트래픽 흐름 기밀성, 데이터 근원지 인증, 접근제어, 비연결형 무결성, 재전송 공격 방지 중 3개 | source-derived; Naver cross-checked; official wording unverified |
| 7 | short | 사토시 나카모토, 거래 저장소, 작업증명 보상 행위. | 비트코인, 블록체인, 채굴/마이닝 | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | Apache Directory Indexing 취약점 대응을 위해 삭제할 지시자. | `Indexes` | source-derived; Naver cross-checked; official wording unverified |
| 9 | short | 삭제하지 않은 CNAME이 피싱 사이트 등으로 악용되는 공격. | 서브도메인 하이재킹 또는 서브도메인 테이크오버 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | ISMS-P 물리적 정보보호 대책 항목. | 보호구역 지정, 출입통제, 정보시스템 보호, 보호설비 운영, 보호구역 내 작업, 반출입 기기 통제, 업무환경 보안 중 3개 | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | 개인정보 최소수집 원칙에 따라 개인정보 수집이 가능한 경우. | 정보주체 동의, 법령상 의무, 공공기관 소관업무, 계약 체결·이행, 급박한 생명·신체·재산 이익, 정당한 이익 등 | source-derived; Naver cross-checked; legal wording needs current-law check |
| 12 | essay | 스위칭 허브 기능과 동작 원리. | 목적지 주소 기반 포트 전송 장치이며 learning, forwarding, filtering, flooding, aging 방식으로 MAC table을 운용 | source-derived; Naver cross-checked; official wording unverified |
| 13 | essay | Snort 룰과 패킷에서 FTP 공격을 식별하고 설명. | Anonymous FTP 로그인 시도. 대소문자 혼합 입력은 탐지 우회 목적이며 `nocase`로 탐지 가능 | source-derived; Naver cross-checked; official wording unverified |
| 14 | practical | Sendmail 스팸메일 릴레이 제한 설정 관련 access DB 생성 명령. | `/etc/mail/access` 편집 후 `makemap hash /etc/mail/access.db < /etc/mail/access` 실행 | source-derived; Naver cross-checked; exact shell path wording unverified |
| 15 | practical | Smurf attack 방지를 위한 라우터 설정. | directed broadcast 차단, ICMP broadcast 응답 제한, ACL/rate-limit 적용 | source-derived; Naver cross-checked; exact command wording unverified |
| 16 | practical | 위험 대응 기법 설명. | 위험수용, 위험감소, 위험회피, 위험전가 | source-derived; Naver cross-checked; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
