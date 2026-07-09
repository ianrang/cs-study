---
title: "실습 안전 계약"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, lab-safety]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "../../../datasets/info-sec-engineer-practical-past-exams/07-study/hands-on-lab-feasibility-deep-research.md"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 독립 Lab의 외부 영향 금지와 정리 원칙."
evergreen: false
---

# 실습 안전 계약

## 허용
- Lab 내부 `.sandbox/`에 샘플 파일 생성
- 샘플 설정, 로그, 룰, HTTP 요청 텍스트 분석
- localhost 또는 offline fixture 기반 관찰

## 금지
- 인터넷 또는 제3자 시스템 대상 스캔·공격·부하 발생
- 호스트 `/etc`, SSH, 방화벽, 사용자 계정, 브라우저 프로필 변경
- 실제 flood, amplification, reverse shell, web shell, cracking 수행
- 실사용 서비스 코드에 취약 코드 주입

## 정리
각 Lab은 `.sandbox/` 외부 파일을 생성하지 않아야 한다. 정리 명령은 `.sandbox/`만 제거해야 한다.
