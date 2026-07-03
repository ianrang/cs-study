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
date_updated: 2026-07-03
source_paths:
  - "index.md"
  - "subject-type-classification-detail.md"
  - "subject-type-matrix.md"
  - "item-reference-map.md"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 1~30회 495문항의 과목·문항유형·연도별 빈도와 23~30회 출제기준/참고문서 연결 빈도를 계산한 분석."
evergreen: false
---

# 정보보안기사 실기 기출 빈도 분석

## Scope
- 분석 단위: `subject-type-classification-detail.md`의 1~30회 495문항.
- 참고문서/출제기준 빈도 단위: `item-reference-map.md`의 23~30회 144문항.
- 공식 PDF 원문 미대조 상태이므로 문구 단위가 아니라 과목·유형·개념 단위 빈도다.

## Overall Frequency
| subject | count | share |
|---|---:|---:|
| 정보보안 관리 및 법규 | 151 | 30.5% |
| 네트워크 보안 | 139 | 28.1% |
| 어플리케이션 보안 | 90 | 18.2% |
| 시스템 보안 | 70 | 14.1% |
| 정보보안 일반 | 45 | 9.1% |
| 합계 | 495 | 100.0% |

## Type Frequency
| type group | count | share |
|---|---:|---:|
| 단답형 | 306 | 61.8% |
| 서술형/실무형 | 189 | 38.2% |
| 합계 | 495 | 100.0% |

## Subject By Type
| subject | short | essay/practical | total |
|---|---:|---:|---:|
| 정보보안 관리 및 법규 | 92 | 59 | 151 |
| 네트워크 보안 | 84 | 55 | 139 |
| 어플리케이션 보안 | 51 | 39 | 90 |
| 시스템 보안 | 44 | 26 | 70 |
| 정보보안 일반 | 35 | 10 | 45 |

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

## Recent Frequency, 23~30회
| subject | count | share |
|---|---:|---:|
| 정보보안 관리 및 법규 | 39 | 27.1% |
| 네트워크 보안 | 38 | 26.4% |
| 시스템 보안 | 31 | 21.5% |
| 어플리케이션 보안 | 27 | 18.8% |
| 정보보안 일반 | 9 | 6.3% |
| 합계 | 144 | 100.0% |

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
- 전체 495문항 기준 최상위 축은 `정보보안 관리 및 법규`와 `네트워크 보안`이다.
- 최근 23~30회 기준으로는 `시스템 보안` 비중이 21.5%까지 올라 전체 평균 14.1%보다 높다.
- `서비스 보안설정 점검과 보완`, `운영체제별 보안특성 파악`, `IT 자산 위협 분석`, `프로토콜별 보안특성 파악`이 최근 23~30회 출제기준 연결의 핵심이다.
- 단답형이 61.8%로 많지만, 관리/법규·네트워크·어플리케이션은 서술형/실무형 비중도 커서 암기형 키워드만으로는 부족하다.
