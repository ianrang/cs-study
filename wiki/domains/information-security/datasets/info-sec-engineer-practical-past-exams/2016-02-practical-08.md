---
title: "정보보안기사 실기 8회 2016년 2회 실기 복원"
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
  - "https://information-security.tistory.com/280"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 8회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 8회 2016년 2회 실기 복원

## Scope
- Exam mapping: 2016년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 다음은 MySQL 설정 파일의 일부이다. 외부 접속을 허용하도록 설정을 변경하시오. | bind-address = 127.0.0.1 부분을 주석 처리하거나 삭제하거나, 허용할 외부 IP 또는 0.0.0.0으로 변경한다. (예: bind-address = 0.0.0.0 또는 해당 행을 #으로 주석 처리) | source-derived from Information Security Tistory; answer block present |
| 2 | short | 정보보호관리체계(ISMS) 인증 도입을 위한 정보보호 대책 항목 중 빈칸 (1), (2), (3)을 채우시오. | (1) 정보보호 조직 (2) 외부자 보안 (3) 접근 통제 | source-derived from Information Security Tistory; answer block present |
| 3 | short | WEP 무선 보안 프로토콜에 관한 설명이다. 빈칸 (A), (B)를 채우시오. | A : RC4 B : IV(Initial Vector, 초기화 벡터) | source-derived from Information Security Tistory; answer block present |
| 4 | short | 다음에서 설명하는 리눅스 디렉토리의 명칭을 쓰시오. | /proc | source-derived from Information Security Tistory; answer block present |
| 5 | short | 정보보호의 5가지 목표 중 빈칸 (A), (B), (C)를 채우시오. | A : 가용성(Availability) B : 인증(Authentication) C : 부인방지(Non-Repudiation) | source-derived from Information Security Tistory; answer block present |
| 6 | short | TCP 3-Way Handshake 과정에서 빈칸 (A), (B), (C)를 채우시오. | A : 3479 (클라이언트 SYN 번호 3478 + 1) B : 3479 (서버의 ACK 번호를 그대로 사용) C : 2325 (서버 SYN 번호 2324 + 1) | source-derived from Information Security Tistory; answer block present |
| 7 | essay | 다음 setuid 관련 함수 호출에 관한 물음에 답하시오. | (1) ruid : (실행 사용자 UID), euid : 0 (root), suid : 0 (root) (2) ruid : 600, euid : 600, suid : 600 | source-derived from Information Security Tistory; answer block present |
| 8 | short | DNS 관련 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : UDP B : Cache(캐시) C : TTL(Time To Live) | source-derived from Information Security Tistory; answer block present |
| 9 | essay | 개인정보 안전성 확보조치 기준에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 고유식별정보 B : 1 C : 취약점 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 위험 처리 방법에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 위험 수용(Risk Acceptance) B : 위험 회피(Risk Avoidance) C : 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | IPSec 프로토콜에 관한 물음에 답하시오. | (가) 전송 모드 : IP 페이로드(데이터)와 ESP 트레일러를 암호화하며 원본 IP 헤더는 그대로 유지한다. 터널 모드 : 원본 IP 패킷 전체(헤더 + 페이로드)와 ESP 트레일러를 암호화하고 새로운 IP 헤더를 추가한다. (나) 구성도 A : 전송 모드 — 호스트 종단 간 보안 서비스를 제공하며 IP 헤더를 그대로 사용한다. 구성도 B : 터널 모드 — 라우터 간 게이트웨이 구간에서 보안 서비스를 제공하며 원본 IP 패킷 전체를 보호한다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 파일 업로드 취약점에 관한 물음에 답하시오. | (가) 악성 스크립트가 첨부된 파일(예: .php, .jsp 등)을 게시판에 업로드하여 성공적으로 업로드되고 실행이 가능하면 파일 업로드 취약점이 존재하는 것으로 판단한다. (나) 업로드 파일의 확장자에 대한 화이트리스트 필터링 정책을 적용하여 허용된 확장자(.jpg, .png, .pdf 등)만 업로드가 가능하도록 한다. 업로드된 파일을 별도의 저장 디렉토리에 보관하고 해당 디렉토리에서 서버 실행 권한을 제거한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 디지털 포렌식의 기본 원칙 중 연계 보관성(Chain of Custody) 원칙을 서술하고 각 단계의 명칭을 순서대로 쓰시오. | 연계 보관성의 원칙 : 증거물의 수집·이송·분석·보관·법정 제출의 각 단계에서 담당자 및 책임자가 명확해야 하며, 전체 과정이 추적 가능해야 한다. 단계 순서 : 증거 수집 → 이송 → 분석 → 보관 → 법정 제출 | source-derived from Information Security Tistory; answer block present |
| 14 | essay | OpenSSL HeartBleed 취약점에 관한 물음에 답하시오. | (가) OpenSSL HeartBleed 취약점(CVE-2014-0160) (나) OpenSSL 1.0.1 ~ OpenSSL 1.0.1f, OpenSSL 1.0.2-beta ~ OpenSSL 1.0.2-beta1 (다) 영향받는 버전을 취약점이 패치된 최신 버전(OpenSSL 1.0.1g 이상)으로 업데이트한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 리눅스 crontab에 관한 물음에 답하시오. | (가) crontab -l (나) crontab -u sis -e (다) 0 3 * * 0 rm -rf /home/* 1>/dev/null 2>&1 | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 정보보호관리체계(ISMS) 인증에 따라 정보보호 정책을 공표·승인하는 방법을 서술하시오. | 정보보호 정책의 승인은 이해관계자의 검토를 거쳐 최고경영자의 승인을 받아야 한다. 정책의 공표는 정보보호 정책 문서를 모든 임직원 및 관련자에게 이해하기 쉬운 형태로 전달하여야 한다. | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
