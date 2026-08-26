---
title: "정보보안기사 실기 기출 빈도 분석"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-analysis, frequency]
status: active
date_created: 2026-07-03
date_updated: 2026-07-07
source_paths:
  - "../index.md"
  - "../03-classification/subject-type-classification-detail.md"
  - "../03-classification/subject-type-matrix.md"
  - "../04-mapping/item-reference-map.md"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 1~31회 513문항의 과목·문항유형·연도별 빈도와 최근 회차 출제기준/참고문서 연결 빈도를 계산한 분석."
evergreen: false
---

# 정보보안기사 실기 기출 빈도 분석

## Scope
- 분석 단위: `subject-type-classification-detail.md`의 1~31회 513문항.
- 참고문서/출제기준 빈도 단위: `item-reference-map.md`의 23~30회 144문항. 31회는 아직 `item-reference-map.md`에 세부 기준 매핑을 확장하지 않았으므로 과목·유형 빈도에만 반영한다.
- 1~28회 thodi-lab/blog-source PDF 편집본은 대조했지만 KCA 공식 원문 문구는 미주장이므로 문구 단위가 아니라 과목·유형·개념 단위 빈도다.

## Overall Frequency
| subject | count | share |
|---|---:|---:|
| 정보보안 관리 및 법규 | 156 | 30.4% |
| 네트워크 보안 | 142 | 27.7% |
| 어플리케이션 보안 | 96 | 18.7% |
| 시스템 보안 | 73 | 14.2% |
| 정보보안 일반 | 46 | 9.0% |
| 합계 | 513 | 100.0% |

## Type Frequency
| type group | count | share |
|---|---:|---:|
| 단답형 | 318 | 62.0% |
| 서술형/실무형 | 195 | 38.0% |
| 합계 | 513 | 100.0% |

## Subject By Type
| subject | short | essay/practical | total |
|---|---:|---:|---:|
| 정보보안 관리 및 법규 | 95 | 61 | 156 |
| 네트워크 보안 | 86 | 56 | 142 |
| 어플리케이션 보안 | 54 | 42 | 96 |
| 시스템 보안 | 47 | 26 | 73 |
| 정보보안 일반 | 36 | 10 | 46 |

## Yearly Subject Frequency
| year | total | 시스템 보안 | 네트워크 보안 | 어플리케이션 보안 | 정보보안 일반 | 정보보안 관리 및 법규 |
|---:|---:|---:|---:|---:|---:|---:|
| 2013 | 31 | 4 | 8 | 3 | 5 | 11 |
| 2014 | 32 | 1 | 6 | 7 | 7 | 11 |
| 2015 | 32 | 3 | 10 | 7 | 4 | 8 |
| 2016 | 32 | 6 | 10 | 2 | 5 | 9 |
| 2017 | 32 | 3 | 13 | 1 | 3 | 12 |
| 2018 | 31 | 2 | 6 | 9 | 4 | 10 |
| 2019 | 31 | 5 | 10 | 5 | 2 | 9 |
| 2020 | 32 | 5 | 9 | 5 | 1 | 12 |
| 2021 | 32 | 2 | 10 | 7 | 3 | 10 |
| 2022 | 48 | 5 | 14 | 11 | 2 | 16 |
| 2023 | 54 | 12 | 16 | 12 | 1 | 13 |
| 2024 | 54 | 8 | 17 | 13 | 3 | 13 |
| 2025 | 54 | 14 | 10 | 8 | 5 | 17 |
| 2026 | 18 | 3 | 3 | 6 | 1 | 5 |

## Recent Frequency, 23~31회
| subject | count | share |
|---|---:|---:|
| 정보보안 관리 및 법규 | 44 | 27.2% |
| 네트워크 보안 | 41 | 25.3% |
| 시스템 보안 | 34 | 21.0% |
| 어플리케이션 보안 | 33 | 20.4% |
| 정보보안 일반 | 10 | 6.2% |
| 합계 | 162 | 100.0% |

## Criteria Frequency, 23~30회
| criteria detail | count |
|---|---:|
| 서비스 보안설정 점검과 보완 | 28 |
| 운영체제별 보안특성 파악 | 22 |
| IT 자산 위협 분석 | 18 |
| 프로토콜별 보안특성 파악 | 18 |
| 위험평가 | 12 |
| 운영체제 보안설정 점검과 보완 | 12 |
| 보안장비 및 네트워크 장비별 보안특성 | 9 |
| 정보수집 및 모니터링 | 7 |
| 취약점 점검이력과 보완내용 관리 | 6 |
| 로그분석 및 대응 | 5 |
| 서비스별 보안특성 파악 | 4 |
| 정보자산 위협 및 취약점 분석 정리 | 2 |
| 네트워크 및 보안장비 설정 점검과 보완 | 1 |

## Reference Frequency, 23~30회
| reference id | count |
|---|---:|
| `REF-KCA-INFOSEC-PRACTICAL-CRITERIA` | 144 |
| `REF-CIIP-VULN-ASSESSMENT-GUIDE` | 35 |
| `REF-SECURE-CODING-GUIDE` | 17 |
| `REF-ISMSP-CRITERIA-GUIDE` | 9 |
| `REF-NVD-CVE-DETAILS` | 4 |
| `REF-CWE-TOP-25` | 4 |
| `REF-FIRST-CVSS` | 3 |
| `REF-PRIVACY-SAFETY-MEASURES` | 3 |
| `REF-OWASP-MOBILE-TOP-10` | 3 |
| `REF-PIPC-PIA-GUIDE` | 2 |
| `REF-NIST-DLP-GLOSSARY` | 2 |
| `REF-MITRE-ATTACK` | 2 |

## Findings
- 전체 513문항 기준 최상위 축은 `정보보안 관리 및 법규`와 `네트워크 보안`이다.
- 최근 23~31회 기준으로는 `시스템 보안` 비중이 21.0%로 전체 평균 14.2%보다 높고, 31회 XSS/CSRF/Fiddler 문항 반영으로 `어플리케이션 보안` 최근 비중도 20.4%까지 올라갔다.
- `서비스 보안설정 점검과 보완`, `운영체제별 보안특성 파악`, `IT 자산 위협 분석`, `프로토콜별 보안특성 파악`은 23~30회 출제기준 연결의 핵심이다. 31회 세부 기준 매핑은 아직 확장하지 않았으므로 이 절은 23~30회 기준으로 유지한다.
- 단답형이 62.0%로 많지만, 관리/법규·네트워크·어플리케이션은 서술형/실무형 비중도 커서 암기형 키워드만으로는 부족하다.
