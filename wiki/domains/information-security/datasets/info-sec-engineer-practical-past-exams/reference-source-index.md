---
title: "정보보안기사 실기 참고문서 원천 인덱스"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-references, source-index]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "document-architecture.md"
  - "exam-criteria-and-reference-catalog.md"
  - "https://owasp.org/www-project-top-ten/"
  - "https://owasp.org/www-project-mobile-top-10/"
  - "https://nvd.nist.gov/vuln/detail/CVE-2014-0160"
  - "https://nvd.nist.gov/vuln/detail/CVE-2021-44228"
  - "https://cwe.mitre.org/top25/"
  - "https://www.first.org/cvss/v4.0/"
  - "https://attack.mitre.org/"
  - "https://www.rfc-editor.org/rfc/rfc9111"
  - "https://cwe.mitre.org/data/definitions/444.html"
  - "https://csrc.nist.gov/glossary/term/data_loss_prevention"
  - "https://csrc.nist.gov/glossary/term/security_orchestration_automation_and_response"
  - "https://csrc.nist.gov/glossary/term/TEMPEST"
  - "https://csrc.nist.gov/pubs/sp/800/83/r1/final"
  - "https://csrc.nist.gov/pubs/sp/800/34/r1/final"
  - "https://csrc.nist.gov/glossary/term/end_to_end_encryption"
  - "https://www.gnu.org/software/acct/manual/accounting.html"
  - "https://owasp.org/www-community/attacks/Credential_stuffing"
  - "https://csrc.nist.gov/glossary/term/zero_day_attack"
  - "https://csrc.nist.gov/pubs/sp/800/124/r2/final"
  - "https://www.law.go.kr/법령/전자금융거래법"
  - "https://www.law.go.kr/법령/정보통신망이용촉진및정보보호등에관한법률"
  - "https://www.law.go.kr/법령/개인정보보호법"
  - "raw/sources/web/information-security-exam-references/kca-info-security-engineer-practical-criteria-2023-2026.md"
  - "raw/sources/web/information-security-exam-references/privacy-safety-measures-law-go-kr.md"
  - "raw/sources/web/information-security-exam-references/pipc-privacy-impact-assessment-guide-2025-10.md"
  - "raw/sources/web/information-security-exam-references/pipc-privacy-safety-measures-guide-2025-11.md"
  - "raw/sources/web/information-security-exam-references/kisa-ciip-technical-vulnerability-assessment-guide-2026.md"
  - "raw/sources/web/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.md"
  - "raw/sources/web/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.md"
source_count: 31
provenance: extracted
summary: "정보보안기사 실기 기출-근거문서 연결을 위한 공식 참고문서 원천 URL, 패칭 상태, 추출 상태를 관리한다."
evergreen: false
---

# 정보보안기사 실기 참고문서 원천 인덱스

## Scope
이 문서는 참고문서 원천 메타데이터의 SSOT이다. 문서 본문 요약, 문항별 연결, 빈도 분석은 이 문서에 넣지 않는다.

## Source Index

| ref_id | 문서 | 발행/운영 주체 | 공식 URL | 상태 | local raw/source | local asset | version/effective | text_extract | 시험 연결 우선순위 | 비고 |
|---|---|---|---|---|---|---|---|---|---:|---|
| REF-KCA-INFOSEC-PRACTICAL-CRITERIA | 정보보안기사 실기 출제기준 | KCA 국가기술자격검정 | https://www.cq.or.kr/ac_flecm02_001.do?atchFileId=264170cf5e4d474994e22bb04ec478d4&fileSn=1 | patched | raw/sources/web/information-security-exam-references/kca-info-security-engineer-practical-criteria-2023-2026.md | raw/assets/information-security-exam-references/kca-info-security-engineer-criteria-2023-2026.pdf | 2023-01-01 ~ 2026-12-31 | success | 1 | 전체 분석의 1차 기준 |
| REF-PRIVACY-SAFETY-MEASURES | 개인정보의 안전성 확보조치 기준/안내서 | 국가법령정보센터 / 개인정보보호위원회 | https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=D010030000&nttId=11641 | patched | raw/sources/web/information-security-exam-references/pipc-privacy-safety-measures-guide-2025-11.md | raw/assets/information-security-exam-references/pipc-privacy-safety-measures-guide-2025-11.pdf | 2025.11, 안전성 기준 일부개정 2025.10 반영 | success | 1 | 국가법령정보센터 URL도 보조 원천으로 확인됨: raw/sources/web/information-security-exam-references/privacy-safety-measures-law-go-kr.md |
| REF-PIPC-PIA-GUIDE | 개인정보 영향평가 수행안내서 | 개인정보보호위원회 | https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=D010030000&nttId=11680 | patched | raw/sources/web/information-security-exam-references/pipc-privacy-impact-assessment-guide-2025-10.md | raw/assets/information-security-exam-references/pipc-privacy-impact-assessment-guide-2025-10.pdf | 2025.10 개정, 2025-12-12 파일수정게시 | success | 1 | 공식 첨부 PDF 저장 및 텍스트 추출 성공 |
| REF-ISMSP-CRITERIA-GUIDE | 정보보호 및 개인정보보호 관리체계 인증기준 안내서 | KISA | https://www.kisa.or.kr/2060301/form?postSeq=54&page=1 | patched | raw/sources/web/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.md | raw/assets/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.pdf | 2023.11 guide, posted 2025-10-15 | success | 1 | 기존 ISMS-P 전용 도메인 상세 페이지도 확인됐으나 로컬 DNS 문제로 KISA 공식 사이트 첨부를 원천으로 패칭 |
| REF-CIIP-VULN-ASSESSMENT-GUIDE | 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드 | KISA | https://www.kisa.or.kr/2060204/form?page=1&postSeq=22 | patched | raw/sources/web/information-security-exam-references/kisa-ciip-technical-vulnerability-assessment-guide-2026.md | raw/assets/information-security-exam-references/kisa-ciip-technical-vulnerability-assessment-guide-2026.pdf | 2026 guide, posted 2025-12-24 | success | 1 | Unix/Windows/웹/보안장비/네트워크/제어시스템/DBMS/가상화/클라우드/모바일/5G/API 보안 점검 항목 연결 후보 |
| REF-SECURE-CODING-GUIDE | 소프트웨어 개발보안 가이드 | KISA | https://www.kisa.or.kr/2060204/form?postSeq=5 | patched | raw/sources/web/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.md | raw/assets/information-security-exam-references/kisa-secure-coding-guide-2021-12-29.pdf | 2021.12.29 PDF, posted 2021-11-29 | success | 1 | SQL Injection, XSS, 파일 업로드, SSRF, Prepared Statement 문항 연결 후보. 행안부 게시글도 확인했으나 KISA 첨부를 원천 asset으로 사용 |
| REF-OWASP-TOP-10-WEB | OWASP Top Ten Web Application Security Risks | OWASP Foundation | https://owasp.org/www-project-top-ten/ | official page confirmed | - | - | 2025 current release, 2021/2017 archive retained | not stored | 2 | 웹 애플리케이션 보안 위험 공통 기준. 원문 asset 저장은 미수행 |
| REF-OWASP-MOBILE-TOP-10 | OWASP Mobile Top 10 | OWASP Foundation | https://owasp.org/www-project-mobile-top-10/ | official page confirmed | - | - | 2024 final release | not stored | 2 | 모바일 앱 보안 위험 공통 기준. Deep link, 인증서 고정, 모바일 통신/저장/인증 주제 보조 원천 |
| REF-NVD-CVE-DETAILS | NIST National Vulnerability Database CVE detail pages | NIST NVD | https://nvd.nist.gov/vuln/ | official page confirmed | - | - | CVE별 상세 페이지, checked 2026-07-03 | not stored | 2 | Heartbleed, Log4j, zero-day 등 CVE 기반 취약점 문항의 보조 원천 |
| REF-CWE-TOP-25 | CWE Top 25 Most Dangerous Software Weaknesses | MITRE CWE | https://cwe.mitre.org/top25/ | official page confirmed | - | - | current page plus archives, checked 2026-07-03 | not stored | 2 | 취약점 root cause, weakness 분류, CWE 기반 보안약점 문항의 보조 원천 |
| REF-FIRST-CVSS | Common Vulnerability Scoring System | FIRST CVSS SIG | https://www.first.org/cvss/v4.0/ | official page confirmed | - | - | CVSS v4.0 documentation, v3.1 archive retained | not stored | 2 | CVSS 점수·벡터·취약점 심각도 문항의 보조 원천 |
| REF-MITRE-ATTACK | MITRE ATT&CK | MITRE | https://attack.mitre.org/ | official page confirmed | - | - | enterprise matrix, checked 2026-07-03 | not stored | 2 | APT, 공격 전술·기술, 침해 분석 단계 모델 문항의 보조 원천 |
| REF-IETF-HTTP-CACHING | RFC 9111 HTTP Caching | IETF / RFC Editor | https://www.rfc-editor.org/rfc/rfc9111 | official page confirmed | - | - | Internet Standard, 2022, checked 2026-07-03 | not stored | 2 | HTTP cache와 Cache-Control 헤더 동작 보조 원천 |
| REF-CWE-444-HTTP-SMUGGLING | CWE-444 HTTP Request/Response Smuggling | MITRE CWE | https://cwe.mitre.org/data/definitions/444.html | official page confirmed | - | - | CWE entry, checked 2026-07-03 | not stored | 2 | HTTP request smuggling 전용 weakness 원천 |
| REF-NIST-DLP-GLOSSARY | NIST CSRC Data Loss Prevention glossary | NIST CSRC | https://csrc.nist.gov/glossary/term/data_loss_prevention | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | DLP 정의와 data in use/in motion/at rest 보호 범위 보조 원천 |
| REF-NIST-SOAR-GLOSSARY | NIST CSRC SOAR glossary | NIST CSRC | https://csrc.nist.gov/glossary/term/security_orchestration_automation_and_response | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | 보안 오케스트레이션·자동화·대응 용어 보조 원천 |
| REF-NIST-TEMPEST-GLOSSARY | NIST CSRC TEMPEST glossary | NIST CSRC | https://csrc.nist.gov/glossary/term/TEMPEST | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | 비의도 방사·전자파 정보유출 통제 개념 보조 원천 |
| REF-NIST-MALWARE-INCIDENT-GUIDE | NIST SP 800-83 Rev. 1 Malware Incident Guide | NIST CSRC | https://csrc.nist.gov/pubs/sp/800/83/r1/final | official page confirmed | - | - | July 2013, checked 2026-07-03 | not stored | 2 | 악성코드 침해 예방·대응과 분석 문항 보조 원천 |
| REF-NIST-CONTINGENCY-PLANNING | NIST SP 800-34 Rev. 1 Contingency Planning Guide | NIST CSRC | https://csrc.nist.gov/pubs/sp/800/34/r1/final | official page confirmed | - | - | May 2010, checked 2026-07-03 | not stored | 2 | 재해복구·contingency planning·DR site 유형 보조 원천 |
| REF-NIST-E2EE-GLOSSARY | NIST CSRC End-to-End Encryption glossary | NIST CSRC | https://csrc.nist.gov/glossary/term/end_to_end_encryption | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | 종단 간 암호화 용어 보조 원천 |
| REF-GNU-ACCOUNTING-UTILITIES | GNU Accounting Utilities Manual | GNU Project | https://www.gnu.org/software/acct/manual/accounting.html | official page confirmed | - | - | edition 6.6.2, checked 2026-07-03 | not stored | 2 | `lastcomm`과 process accounting 명령 이력 확인 보조 원천 |
| REF-OWASP-CREDENTIAL-STUFFING | OWASP Credential Stuffing | OWASP Foundation | https://owasp.org/www-community/attacks/Credential_stuffing | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | 유출 자격증명 악용·credential stuffing 보조 원천 |
| REF-NIST-ZERO-DAY-GLOSSARY | NIST CSRC Zero Day Attack glossary | NIST CSRC | https://csrc.nist.gov/glossary/term/zero_day_attack | official page confirmed | - | - | checked 2026-07-03 | not stored | 2 | 제로데이 공격 정의 보조 원천 |
| REF-NIST-MOBILE-DEVICE-SECURITY | NIST SP 800-124 Rev. 2 Mobile Device Security | NIST CSRC | https://csrc.nist.gov/pubs/sp/800/124/r2/final | official page confirmed | - | - | May 2023, checked 2026-07-03 | not stored | 2 | MDM, enterprise mobility management, BYOD 모바일 보안 보조 원천 |
| REF-LAW-ELECTRONIC-FINANCIAL-TRANSACTION | 전자금융거래법 | 국가법령정보센터 | https://www.law.go.kr/법령/전자금융거래법 | official page confirmed | - | - | current law page checked 2026-07-03 | not stored | 2 | CISO 지정과 전자금융 법적 준거성 보조 원천 |
| REF-LAW-NETWORK-ACT | 정보통신망 이용촉진 및 정보보호 등에 관한 법률 | 국가법령정보센터 | https://www.law.go.kr/법령/정보통신망이용촉진및정보보호등에관한법률 | official page confirmed | - | - | current law page checked 2026-07-03 | not stored | 2 | 정보통신망 정의와 정보보호 법적 준거성 보조 원천 |
| REF-LAW-PIPA | 개인정보 보호법 | 국가법령정보센터 | https://www.law.go.kr/법령/개인정보보호법 | official page confirmed | - | - | current law page checked 2026-07-03 | not stored | 2 | CCTV, 영상정보처리기기, 개인정보 처리 근거 보조 원천 |

## Status Semantics

| status | 의미 |
|---|---|
| patched | 공식 URL 확인, 원문 asset 저장, raw source metadata 작성, 텍스트 추출 가능 |
| partial | 공식 URL 및 일부 원문 저장은 되었으나 학습용 텍스트 추출이 불완전 |
| official page confirmed | 공식 상세 페이지는 확인했으나 첨부 원문 다운로드 또는 asset 저장이 아직 미완료 |
| pending | 공식 URL 또는 원문 파일을 아직 확인하지 못함 |

## Next Patch Targets

| priority | ref_id | next action |
|---:|---|---|
| 1 | REF-OWASP-TOP-10-WEB | 원문 asset 저장이 필요하면 OWASP 2025/2021 페이지 또는 GitHub release를 raw/source로 패칭 |
| 2 | REF-OWASP-MOBILE-TOP-10 | 모바일 문항 보강 범위가 커지면 2024 final release를 raw/source로 패칭 |
| 3 | REF-NVD-CVE-DETAILS / REF-CWE-TOP-25 / REF-FIRST-CVSS / REF-MITRE-ATTACK | 취약점·위협모델 문항 확대 시 CVE별 상세 페이지와 CWE/CVSS/ATT&CK 원천을 raw/source로 패칭 |
| 4 | REF-IETF-HTTP-CACHING / REF-CWE-444-HTTP-SMUGGLING / REF-NIST-* / REF-LAW-* / REF-GNU-ACCOUNTING-UTILITIES / REF-OWASP-CREDENTIAL-STUFFING | 이번 보강에서 official page confirmed로 추가한 원천. 재현 가능한 오프라인 보존이 필요하면 raw/source 패칭 |
