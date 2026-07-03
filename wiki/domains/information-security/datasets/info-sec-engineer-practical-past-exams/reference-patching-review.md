---
title: "정보보안기사 실기 참고문서 패칭 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, verification, exam-references]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "reference-source-index.md"
  - "document-architecture.md"
  - "raw/sources/web/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.md"
source_count: 3
provenance: inferred
summary: "필수 참고문서 원문 패칭 결과를 SSOT, 독립성, 추출 가능성, 공식성 기준으로 검토한다."
evergreen: false
---

# 정보보안기사 실기 참고문서 패칭 교차검증 리포트

## Verdict
- Pass: 문서 아키텍처의 SSOT/단일 책임/단방향 참조 원칙을 유지했다.
- Pass: 공식 URL이 확인된 원천만 `patched` 또는 `partial`로 올렸다.
- Pass: 공식 URL이 확인되지 않은 문서는 `pending`으로 남기고 raw 원문을 저장하지 않는 fail-closed 원칙을 유지했다.
- Pass: KCA 출제기준, PIPC 개인정보 문서 2개, KISA ISMS-P 인증기준 안내서, KISA 주요정보통신기반시설 기술적 취약점 상세가이드, KISA 소프트웨어 개발보안 가이드는 완전 패칭됐다.

## Checks

| check | result | evidence |
|---|---|---|
| KCA 출제기준 PDF 다운로드 | pass | SHA-256 `ac8c9015d51bc1975e66aa8ef63a024900ce07b6c1baabfce087c76bad726a07` |
| KCA 출제기준 텍스트 추출 | pass | `pdftotext` 성공 |
| 개인정보 안전성 기준 공식 URL | pass | 국가법령정보센터 page title 확인 |
| 개인정보 안전성 확보조치 기준 안내서 PDF 다운로드 | pass | PIPC `FILE_000000000560213`, SHA-256 `dcc29db0bc847049175933e08ea537b1dfed22b39d0bc97164b9ddb6fb90413c` |
| 개인정보 안전성 확보조치 기준 안내서 텍스트 추출 | pass | `pdftotext` 성공 |
| 개인정보 영향평가 수행안내서 PDF 다운로드 | pass | PIPC `FILE_000000000560272`, SHA-256 `5e4746fa960ffa305cd112881c6282e3bd7ca00eb831627d384b8ed87a261c42` |
| 개인정보 영향평가 수행안내서 텍스트 추출 | pass | `pdftotext` 성공 |
| 주요정보통신기반시설 기술적 취약점 상세가이드 PDF 다운로드 | pass | KISA `menuSeq=2060204`, `postSeq=22`, `attachSeq=1`, SHA-256 `44fe393981b244147be6af7423d99dc15633c089fad0bcb296cbe2371dde812d` |
| 주요정보통신기반시설 기술적 취약점 상세가이드 텍스트 추출 | pass | `pdftotext` 성공, 문서 표지와 목차의 `2026 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드` 확인 |
| ISMS-P 인증기준 공식 상세 페이지 | pass | KISA 안내서 상세 페이지와 첨부 파일명 확인 |
| ISMS-P 인증기준 PDF 다운로드 | pass | KISA `menuSeq=2060301`, `postSeq=54`, `attachSeq=1`, SHA-256 `6df06f8ddf007094952ec714341bc466266a4fc5459470b1744495725049e599` |
| ISMS-P 인증기준 텍스트 추출 | pass | `pdftotext` 성공 |
| 소프트웨어 개발보안 가이드 공식 상세 페이지 | pass | KISA `menuSeq=2060204`, `postSeq=5`, 게시일 `2021-11-29`, 첨부명 `소프트웨어_개발보안_가이드(2021.12.29).pdf` 확인 |
| 소프트웨어 개발보안 가이드 PDF 다운로드 | pass | KISA `menuSeq=2060204`, `postSeq=5`, `attachSeq=1`, SHA-256 `fcd8c4343f5f3ec0d7a1beda7ba4a6f86b67f5d6267664241fb66f6710ca0407` |
| 소프트웨어 개발보안 가이드 텍스트 추출 | pass | `pdftotext` 성공, 380 pages, SQL 삽입/PreparedStatement 등 시큐어코딩 항목 추출 확인 |
| 행안부 보조 게시글 확인 | pass | 행안부 `nttId=88956` 게시글은 동일 주제 공식 맥락을 확인했으나, 검색에 노출된 `FILE_000000000046958` 직접 첨부는 8쪽짜리 2013 PDF라 raw asset으로 사용하지 않음 |

## Review Findings

| severity | finding | action |
|---|---|---|
| LOW | 소프트웨어 개발보안 가이드는 KISA 공식 첨부로 패칭 완료됐고, 행안부 보조 게시글의 다른 첨부와 혼동 가능성이 있다. | source metadata와 source index에 KISA 다운로드 패턴과 비원천 행안부 첨부 주의사항을 유지한다. |
| MEDIUM | ISMS-P 전용 도메인 `isms.kisa.or.kr`은 로컬 DNS 문제로 다운로드 검증이 실패했으나, KISA 공식 사이트의 동일 안내서 첨부는 패칭됐다. | 후속 작업에서 전용 도메인 복구 시 동일성 비교를 수행한다. |

## Architecture Review

| 항목 | 결과 | 비고 |
|---|---|---|
| SSOT | pass | 원천 메타데이터는 `reference-source-index.md`에만 기록 |
| 단일 책임 | pass | 패칭 검증은 이 리포트, 메타데이터는 source index로 분리 |
| 독립성 | pass | raw 원문과 wiki 인덱스 분리 |
| OCP | pass | 새 문서는 source index 행 추가로 확장 가능 |
| 순환 참조 | pass | raw/source index/catalog 방향 유지 |
| 중복 | pass | 원문 본문 장문 복제 없음 |
