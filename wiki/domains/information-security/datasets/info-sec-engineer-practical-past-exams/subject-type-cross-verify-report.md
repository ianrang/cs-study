---
title: "정보보안기사 실기 과목/유형 매트릭스 교차검증 리포트"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction, verification]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "subject-type-matrix.md"
  - "subject-type-classification-detail.md"
source_count: 2
provenance: inferred
summary: "회차별 과목/문제유형 매트릭스와 상세 분류의 내부 정합성 및 실제 원문 대조 한계를 검증한 report-only 결과."
evergreen: false
---

# 정보보안기사 실기 과목/유형 매트릭스 교차검증 리포트

## Verdict
- Internal consistency: pass. The matrix cells and item-level classification detail contain matching classified item numbers.
- Original-problem verification: blocked for official PDF cross-check because the local PDF returns `Incorrect password` with `pdftotext`.
- Classification accuracy: fail-closed. Several rows are clearly misclassified or left unclassified despite visible subject evidence.
- Round reliability: low for rounds where unclassified plus excluded rows are high, especially 11회, 15회, 19회, 20회, 21회, 22회.

## Finding Summary
| severity | count |
|---|---:|
| HIGH | 12 |
| MEDIUM | 14 |

| category | count |
|---|---:|
| unclassified_with_clear_evidence | 5 |
| subject_keyword_conflict | 14 |
| source_quality_low | 6 |
| official_pdf_unverified | 1 |

## HIGH Findings
- `unclassified_with_clear_evidence`: 1회 #2 미분류이나 명확한 과목 키워드 존재 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:53)
  - detail: suggest=['네트워크 보안'] hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=네트워크 장비 상태 정보 전송 방식
- `unclassified_with_clear_evidence`: 8회 #16 미분류이나 명확한 과목 키워드 존재 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:173)
  - detail: suggest=['정보보안 일반'] hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 2, '정보보안 관리 및 법규': 0} text=(A) 연계보관성(Chain of Custody)
- `unclassified_with_clear_evidence`: 8회 #17 미분류이나 명확한 과목 키워드 존재 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:174)
  - detail: suggest=['정보보안 일반'] hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=(B) 연계보관성 5단계: 획득 → 이송 → 분석 → 보관 → 법정 제출
- `unclassified_with_clear_evidence`: 9회 #14 미분류이나 명확한 과목 키워드 존재 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:189)
  - detail: suggest=['정보보안 일반'] hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=(나) instances: 동시 서비스 가능 서버 수 50개 제한
- `unclassified_with_clear_evidence`: 14회 #14 미분류이나 명확한 과목 키워드 존재 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:229)
  - detail: suggest=['네트워크 보안'] hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=포트 스캔 종류, 목적, 의미
- `source_quality_low`: 11회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:102)
  - detail: total=1 unclassified=0 excluded=1 ratio=1.00
- `source_quality_low`: 15회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:105)
  - detail: total=16 unclassified=2 excluded=13 ratio=0.94
- `source_quality_low`: 19회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:108)
  - detail: total=18 unclassified=6 excluded=11 ratio=0.94
- `source_quality_low`: 20회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:109)
  - detail: total=18 unclassified=6 excluded=10 ratio=0.89
- `source_quality_low`: 21회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:110)
  - detail: total=18 unclassified=5 excluded=11 ratio=0.89
- `source_quality_low`: 22회 미분류+제외 비율이 높아 실제 회차 분포로 신뢰하기 어려움 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-matrix.md:111)
  - detail: total=18 unclassified=5 excluded=7 ratio=0.67
- `official_pdf_unverified`: 공식/원본 PDF가 암호화되어 현재 산출물과 실제 문제 원문 직접 대조가 불가 (/Users/ian/Downloads/[문제+답] 1회~28회 정보보안기사 실기 단답형.pdf:0)
  - detail: pdftotext/pdfinfo returned Incorrect password in prior verification

## MEDIUM Findings
- `subject_keyword_conflict`: 12회 #3 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:213)
  - detail: suggest=네트워크 보안 assigned=정보보안 일반 hits={'네트워크 보안': 3, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=📚 서술형 문제(11-13번) 문제 11번 (정보보안 일반 - 망분리: 논리적 망분리) 논리적 망분리 시 인터넷망 가상화와 업무망 가상화의 장점을 각각 2가지 이상 서술하시오. 문제 12번 (보안관리솔루션 - 보안장비 취약점 관리) 사이트 보안 담당자는 신규 도입된 보안 장비(방화벽, IPS, IDS, VPN 등)에 대해
- `subject_keyword_conflict`: 14회 #16 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:231)
  - detail: suggest=네트워크 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 2, '시스템 보안': 0, '어플리케이션 보안': 1, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=Snort rule 설정 (XSS 공격 탐지) ※ 출제 영역별 분석은 다음과 같습니다. ​ 전통적으로 출제 비중이 높았던 네트워크 및 시스템 보안 문제가 도합 50%로 비중 있게 출제되었고, 애플리케이션 보안, 정보보안 일반 및 관리 문제도 각각 13% 이상 균형되게 출제되었습니다. 법규의 경우 지난 회차와 유사하게 1문
- `subject_keyword_conflict`: 18회 #15 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:281)
  - detail: suggest=시스템 보안 assigned=어플리케이션 보안 hits={'네트워크 보안': 0, '시스템 보안': 2, '어플리케이션 보안': 0, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=리눅스 계정 잠김 임계값, IPtables, /etc/shadow, Limitrequestbody
- `subject_keyword_conflict`: 18회 #16 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:282)
  - detail: suggest=네트워크 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 2, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=DNS 기반 공격 기법, 판단 사유, 공격원리 ※ 출제 영역별 분석은 다음과 같습니다. ​ 지난 회차에 이어 애플리케이션 보안(31%), 정보보호관리(19%) 영역의 강세가 이어졌습니다. 지난 회차 크게 감소하였던 네트워크보안과 시스템 보안은 이번 회차에서 도합 50%로 예년 수준으로 다시 회복되었습니다. 지난 회차 충격
- `subject_keyword_conflict`: 21회 #2 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:298)
  - detail: suggest=네트워크 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 2, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 1} text=특히 21회에서는 이메일 보안, SNMP, 위험관리, IDS 등 다양한 보안 영역에서 실무적인 문제들이 출제되었습니다.
- `subject_keyword_conflict`: 23회 #1 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:316)
  - detail: suggest=시스템 보안 assigned=네트워크 보안 hits={'네트워크 보안': 1, '시스템 보안': 2, '어플리케이션 보안': 0, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=윈도우 OS 환경에서 특정 서비스의 로그 파일 저장 경로를 참고하여, ( )에 들어갈 로그 파일 경로를 기술하시오. (IIS 로그) C:\Windows\inetpub\logs\Logfiles\W3SVC1 C:\Windows\inetpub\logs\Logfiles\MSFTPSVC1 C:\Windows\System32\Log
- `subject_keyword_conflict`: 23회 #16 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:331)
  - detail: suggest=어플리케이션 보안 assigned=네트워크 보안 hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=보안 이벤트 분석 결과 1초에 1000번 이상 다음과 같은 패킷이 유입되고 있는 것이 확인되었다. 패킷 헤더 중 a, b를 보고 어떤 공격인지 설명하시오. (HTTP Request) GET /test.jsp Host : webserver.com User-Agent : Mozilla/5.0
- `subject_keyword_conflict`: 24회 #4 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:337)
  - detail: suggest=정보보안 일반 assigned=네트워크 보안 hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 2, '정보보안 관리 및 법규': 0} text=EAP를 통해 인증을 수행하고 AES-CCMP 기반 암호화를 지원하는 무선랜 보안 표준은?
- `subject_keyword_conflict`: 24회 #8 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:341)
  - detail: suggest=어플리케이션 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 1, '정보보안 관리 및 법규': 0} text=다음과 같은 기능을 수행하는 정보보호 솔루션의 이름은 무엇인가? - PC에 설치된 에이전트, 네트워크 센서를 통하여 이동식 디스크, 이메일, 메신저, 웹사이트 파일 업로드 등 내부 문서 이동을 탐지 - HTTPS와 같은 암호화 통신에서도 중요 내부 문서 이동 탐지 가능 - 일부 솔루션에서는 파일 암호화, 파일 삭제와 같은
- `subject_keyword_conflict`: 26회 #4 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:373)
  - detail: suggest=어플리케이션 보안 assigned=네트워크 보안 hits={'네트워크 보안': 1, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=공격자가 HTTP 패킷의 헤더(Content-Length, Transfer Encoding: Chunked 등)를 변조하여 일반 사용자가 접근할 수 없는 Back-end 서버로 직접 보내 중요 정보 획득, XSS 공격유도, 서버 웹 캐시 포이즈닝 등을 수행하는 공격 기법을 무엇이라고 하는가? (보기) XSS, CSRF,
- `subject_keyword_conflict`: 26회 #16 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:385)
  - detail: suggest=어플리케이션 보안 assigned=네트워크 보안 hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=XSS(Cross Site Script) 공격의 정의와 공격 기법 2가지를 설명하시오. 1) XSS 공격 정의 - 웹페이지에 악의적인 스크립트를 포함시켜 사용자 측에서 실행되도록 이득을 취하는 공격 2) XSS 공격 기법 2가지 - Reflected XSS: 검색 결과, 에러 메시지 등을 통해 서버가 외부에서 입력받은 악
- `subject_keyword_conflict`: 27회 #7 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:394)
  - detail: suggest=어플리케이션 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 0, '정보보안 관리 및 법규': 1} text=SW 개발 보안과 관련하여 ( )에 들어갈 취약점명(공격기법)을 기술하시오. - (A) : DB와 연결되어 있는 애플리케이션의 입력값을 조작하여 의도하지 않은 결과를 반환하도록 하는 공격 기법 - (B) : 게시판, 웹, 메일 등에 삽입된 악의적인 스크립트에 의해 쿠키 및 기타 개인정보를 특정 사이트로 전송시키는 공격 기
- `subject_keyword_conflict`: 28회 #4 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:409)
  - detail: suggest=어플리케이션 보안 assigned=네트워크 보안 hits={'네트워크 보안': 0, '시스템 보안': 0, '어플리케이션 보안': 2, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=XSS 상황에서 JavaScript의 쿠키 접근을 막는 쿠키 보안 속성.
- `subject_keyword_conflict`: 28회 #18 키워드 우세 과목과 현재 분류 차이 (/Users/ian/dev/personal/001_cs-study/wiki/domains/information-security/datasets/info-sec-engineer-practical-past-exams/subject-type-classification-detail.md:423)
  - detail: suggest=네트워크 보안 assigned=정보보안 관리 및 법규 hits={'네트워크 보안': 2, '시스템 보안': 0, '어플리케이션 보안': 0, '정보보안 일반': 0, '정보보안 관리 및 법규': 0} text=Telnet 및 FTP 서비스 운영 배너를 보고 취약점과 전환 방안을 쓰는 문항.

## Method
- Parsed all same-directory `*-practical-*.md` reconstruction tables.
- Parsed `subject-type-classification-detail.md` item rows.
- Parsed `subject-type-matrix.md` matrix cells and unclassified/excluded rows.
- Checked that each matrix cell item list equals the corresponding item-level detail list.
- Checked that classified + unclassified + excluded row counts close against source reconstruction row counts.
- Flagged clear subject evidence by deterministic keyword rules only; no missing original wording was inferred.
