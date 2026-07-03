---
title: "정보보안기사 실기 14회 2019년 2회 실기 복원"
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
  - "https://blog.naver.com/stereok2/221751404526"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 14회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 14회 2019년 2회 실기 복원

## Scope
- Exam mapping: 2019년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 접근통제 정책 모델 | MAC, DAC, RBAC | Naver answer cross-check; exact official wording unverified |
| 2 | short | ARP 프로토콜 목적지 물리 주소 형식 | ff:ff:ff:ff:ff:ff | Naver answer cross-check; exact official wording unverified |
| 3 | short | IPSec 프로토콜 | 네트워크 계층, AH, ESP | Naver answer cross-check; exact official wording unverified |
| 4 | short | MS 오피스와 애플리케이션 사이 데이터 전달 프로토콜 | DDE(Dynamic Data Exchange) | Naver answer cross-check; exact official wording unverified |
| 5 | short | 사이버위기 경보 단계 | 관심, 경계, 심각 | Naver answer cross-check; exact official wording unverified |
| 6 | short | 리눅스 시스템 로그 파일 | utmp, wtmp, btmp | Naver answer cross-check; exact official wording unverified |
| 7 | short | 정보보호제품 국제 표준 인증 | CC 인증 | Naver answer cross-check; exact official wording unverified |
| 8 | short | Apache 업로드 가능 최대 파일 크기 제한 지시자 | LimitRequestBody | Naver answer cross-check; exact official wording unverified |
| 9 | short | 정보보호 관련 법률 명칭 | 정보통신망법, 정보통신기반보호법, 위치정보법 | Naver answer cross-check; exact official wording unverified |
| 10 | short | ISMS-P 인증 평가 항목 빈칸 | 중요도, 위협 정보, 경영진 | Naver answer cross-check; exact official wording unverified |
| 11 | essay | 유닉스 계정 패스워드 임계값 설정 | deny=5는 5회 실패 시 잠금, unlock_time=120은 120초 후 해제, no_magic_root는 root 예외, reset은 성공 시 실패 횟수 초기화 | Naver answer cross-check; exact official wording unverified |
| 12 | essay | /etc/shadow 파일 설정 | a는 해시 알고리즘, b는 salt, c는 해시값이다. salt로 레인보우테이블 공격을 완화하며, pwunconv는 shadow 비밀번호를 passwd로 되돌리고 shadow를 비활성화한다 | Naver answer cross-check; exact official wording unverified |
| 13 | essay | 강제적 접근제어 모델 | 기밀성 중심 모델은 BLP이며 no-read-up은 낮은 등급 주체의 높은 등급 객체 읽기 금지, no-write-down은 높은 등급 주체의 낮은 등급 객체 쓰기 금지, Biba write 정책은 no-write-up이다 | Naver answer cross-check; exact official wording unverified |
| 14 | essay | TCP ACK 스캔 목적과 결과 | TCP ACK 스캔이며 방화벽 필터링 여부 확인이 목적이다. RST가 온 2017 포트는 필터링되지 않고, 무응답 포트는 필터링되는 것으로 판단한다 | Naver answer cross-check; exact official wording unverified |
| 15 | essay | Apache 설정 옵션 의미 | Timeout 300은 300초 무응답 시 연결 종료, MaxKeepAliveRequests 100은 KeepAlive 연결당 최대 요청 수, DirectoryIndex는 기본 인덱스 파일 순서, ErrorLog는 오류 로그 경로를 의미한다 | Naver answer cross-check; exact official wording unverified |
| 16 | essay | XSS 탐지 Snort 룰 | offset/depth는 지정 위치와 길이에서 GET을 찾고, distance 1은 이전 매치 뒤 1바이트 이후 문자열을 찾는다. 탐지 누락 시 offset 조정 또는 삭제와 nocase 추가/대소문자 보정을 적용한다 | Naver answer cross-check; exact official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and must be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
