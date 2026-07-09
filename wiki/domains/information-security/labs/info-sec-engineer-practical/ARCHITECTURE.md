---
title: "정보보안기사 실기 독립 실습 스캐폴드 아키텍처"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, labs, architecture, isolation]
status: active
date_created: 2026-07-09
date_updated: 2026-07-09
source_paths:
  - "../../datasets/info-sec-engineer-practical-past-exams/07-study/hands-on-integrated-study-roadmap-2026-02.md"
  - "../../datasets/info-sec-engineer-practical-past-exams/07-study/hands-on-lab-feasibility-deep-research.md"
source_count: 2
provenance: inferred
summary: "기출 데이터셋과 독립 실습 실행물을 분리하고, 각 Lab의 캡슐화·재사용·정리 규칙을 정의한다."
evergreen: false
---

# 정보보안기사 실기 독립 실습 스캐폴드 아키텍처

## 1. 책임 경계
| 영역 | 책임 | 금지 |
|---|---|---|
| `datasets/` | 기출 복원, 분석, 참고문서 매핑, 학습 전략 | 실행 스크립트, 샌드박스 산출물 |
| `labs/info-sec-engineer-practical/` | 시험 대비 실습 세트, 질문, 기대 관찰값, 정리 절차 | 기출 원문 재복제, 공식 레퍼런스 레지스트리 중복 |
| 각 Lab의 `.sandbox/` | 실행 중 생성되는 일회용 파일 | git 추적, 사용자 환경 의존 |

## 2. 구조
```text
labs/info-sec-engineer-practical/
├── README.md
├── ARCHITECTURE.md
├── bin/
│   ├── run-lab.sh
│   ├── clean-lab.sh
│   └── check-labs.sh
├── shared/
│   ├── answer-template.md
│   └── safety-contract.md
└── labs/
    ├── 01-linux-hardening/
    ├── 02-service-config/
    ├── 03-network-protocol/
    ├── 04-web-vuln-review/
    ├── 05-ids-log-triage/
    └── 06-risk-law-tabletop/
```

## 3. 캡슐화 규칙
| 규칙 | 내용 |
|---|---|
| 실행 위치 | 모든 Lab은 자기 디렉터리의 `.sandbox/`에만 파일을 생성한다. |
| 입력 | Lab 내부의 `run.sh`, `questions.md`, `expected-observations.md`만 참조한다. |
| 출력 | `.sandbox/observations.txt` 또는 `.sandbox/answer-sheet.txt`를 생성한다. |
| 정리 | `cleanup.md`의 절차와 `bin/clean-lab.sh`로 `.sandbox/`만 삭제한다. |
| 외부 영향 | 호스트 `/etc`, SSH, 방화벽, 계정, 브라우저 프로필, 실제 네트워크 대상 변경 금지. |

## 4. 선택한 패턴
| 패턴 | 적용 위치 | 이유 |
|---|---|---|
| Lab Capsule | 각 `labs/NN-name/` | 실습 목표, 실행, 질문, 기대값, 정리를 한 캡슐로 묶어 재사용한다. |
| Offline Fixture First | 모든 기본 Lab | Docker 이미지, 인터넷, 외부 서비스 없이도 학습을 시작할 수 있다. |
| Observation Driven Answer | `expected-observations.md`와 `questions.md` | 실기 답안을 관찰 증거 기반으로 쓰게 만든다. |

## 5. 검증 결과
| 항목 | 상태 | 비고 |
|---|---|---|
| 순환 참조 | 통과 | Lab은 데이터셋을 읽기 근거로만 참조한다. |
| 캡슐화 | 통과 | 실행 산출물은 Lab별 `.sandbox/`에 제한된다. |
| 외부 영향 차단 | 통과 | 기본 Lab은 샘플 파일과 텍스트 분석 중심이다. |
| 확장성 | 통과 | Docker/WebGoat/Snort 실제 실행은 별도 optional Lab로 추가 가능하다. |

## 6. 리스크
- Docker 기반 실습을 추가하면 이미지 pull과 컨테이너 네트워크가 필요하다. 기본 Lab과 별도 optional 계층으로만 추가한다.
- 실제 flood, 증폭, 리버스 셸, 웹셸, 크래킹 실습은 이 스캐폴드의 범위 밖이다.
