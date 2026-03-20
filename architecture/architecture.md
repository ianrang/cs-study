# 백엔드 아키텍처 종합 분석 — 종류, 조합, 트레이드오프, 의사결정 기준

> 작성일: 2026-03-16 | 개정일: 2026-03-19
> 목적: 백엔드 아키텍처의 종류와 조합을 체계적으로 정리하고, 각각의 트레이드오프와 의사결정 기준을 명확히 한 뒤, v0.3 메타 기반 워크플로 커널 아키텍처의 위치를 객관적으로 평가한다.

---

## 목차

1. [아키텍처 분류 체계 — 6개 카테고리](#1-아키텍처-분류-체계--6개-카테고리)
2. [카테고리 A: 배포 단위 아키텍처](#2-카테고리-a-배포-단위-아키텍처--시스템을-어떻게-나눠서-배포하는가)
3. [카테고리 B: 코드 구조 아키텍처](#3-카테고리-b-코드-구조-아키텍처--하나의-배포-단위-안에서-코드를-어떻게-배치하는가)
4. [카테고리 C: 도메인 모델링 패턴](#4-카테고리-c-도메인-모델링-패턴--비즈니스-로직을-어떻게-표현하는가)
5. [카테고리 D: 데이터 흐름 패턴](#5-카테고리-d-데이터-흐름-패턴--데이터를-어떻게-읽고-쓰는가)
6. [카테고리 E: 시스템 통합 패턴](#6-카테고리-e-시스템-통합-패턴--모듈시스템-간-어떻게-소통하는가)
7. [카테고리 F: 실행 제어 패턴](#7-카테고리-f-실행-제어-패턴--실행-흐름을-어떻게-제어하는가)
8. [아키텍처 전체 지도 — 카테고리 간 관계](#8-아키텍처-전체-지도--카테고리-간-관계)
9. [아키텍처 조합 패턴 — 현업에서 실제 사용되는 방식](#9-아키텍처-조합-패턴--현업에서-실제-사용되는-방식)
10. [왜 대부분의 현업에서 v0.3 같은 아키텍처를 사용하지 않는가](#10-왜-대부분의-현업에서-v03-같은-아키텍처를-사용하지-않는가)
11. [아키텍처 의사결정 프레임워크 — 정확한 기준](#11-아키텍처-의사결정-프레임워크--정확한-기준)
12. [종합 트레이드오프 매트릭스](#12-종합-트레이드오프-매트릭스)
13. [v0.3 아키텍처의 객관적 위치 평가](#13-v03-아키텍처의-객관적-위치-평가)
14. [결론 — "무조건 좋은 아키텍처는 없다"의 구체적 의미](#14-결론--무조건-좋은-아키텍처는-없다의-구체적-의미)

---

## 1. 아키텍처 분류 체계 — 6개 카테고리

### 1.1 왜 분류가 중요한가

아키텍처를 논의할 때 가장 흔한 혼란은 **서로 다른 카테고리의 것을 같은 선상에서 비교**하는 것이다.
예: "Layered vs Microservices"는 부적절한 비교다 — Layered는 코드 배치 방식이고, Microservices는 배포 단위 방식이다.

> **핵심 원칙: 아키텍처는 6개 독립적 축에서 각각 하나씩 선택하고 조합하는 것이다.**
> 모든 프로젝트는 의식적이든 아니든 6개 축 모두에서 선택을 한다. 명시적으로 선택하지 않으면 "기본값"이 자동으로 적용된다.

### 1.2 아키텍처 패턴 vs 디자인 패턴 — 분류 기준

이 문서에서 다루는 것은 **아키텍처 패턴**이다. 디자인 패턴과 구분해야 한다.

```
아키텍처 패턴 (이 문서의 범위):
  시스템/모듈 전체의 구조적 결정. 선택하면 코드 전체의 배치·흐름이 바뀜.
  예: "Hexagonal로 한다" → 모든 코드가 Port/Adapter 구조를 따름
  예: "CQRS로 한다" → 읽기/쓰기 경로가 시스템 전체에서 분리됨
  예: "Metadata-Driven으로 한다" → 실행 흐름 정의 방식 자체가 바뀜

디자인 패턴 (이 문서의 범위가 아님):
  특정 문제를 해결하는 코드 수준의 기법. 일부 코드에만 영향.
  예: Strategy, Observer, Factory, Builder, Decorator
  예: Plugin Architecture — 확장 포인트를 제공하는 디자인 패턴
  예: Actor Model — 동시성 프로그래밍 모델
  예: Repository Pattern — 데이터 접근 추상화 패턴

  이들은 어떤 아키텍처 조합에서든 필요에 따라 적용할 수 있다.
  아키텍처 축의 "선택지"가 아니라, 구현 시 활용하는 "도구"다.
```

> **Plugin Architecture, Actor Model, Strategy Pattern** 등은 디자인 패턴이다.
> 이들은 아키텍처 선택과 무관하게 어디서든 사용할 수 있으므로 6개 축의 선택지에 포함하지 않는다.

### 1.3 6개 카테고리 개요

```
┌────────────────────────────────────────────────────────────────────────┐
│                     아키텍처 분류 체계 (6개 축)                           │
│                                                                        │
│  모든 프로젝트는 6개 축 모두에서 반드시 하나를 선택한다.                     │
│  명시적으로 선택하지 않으면 [기본값]이 자동 적용된다.                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  A. 배포 단위 (시스템 수준)         "전체 시스템을 어떻게 나눠 배포하나?"   │
│     [Monolithic] │ Modular Monolith │ Microservices │ Serverless       │
│                                                                        │
│  B. 코드 구조 (애플리케이션 수준)   "하나의 배포 단위 안에서 코드를          │
│     [Layered] │ Hexagonal │ Clean/Onion │   어떻게 배치하나?"            │
│     Vertical Slice                                                     │
│                                                                        │
│  C. 도메인 모델링 (비즈니스 로직)   "비즈니스 로직을 어떤 형태로            │
│     [Transaction Script] │ Table Module │   코드에 표현하나?"            │
│     Domain Model (DDD Tactical)                                        │
│                                                                        │
│  D. 데이터 흐름 (읽기/쓰기)        "데이터를 어떻게 읽고 쓰나?"            │
│     [단일 모델] │ CQRS │ Event Sourcing │ Pipe & Filter                │
│                                                                        │
│  E. 시스템 통합 (모듈/서비스 간)    "모듈/시스템 간 어떻게 소통하나?"       │
│     [동기 호출] │ Event-Driven │ Saga │ API Gateway/BFF                │
│                                                                        │
│  F. 실행 제어 (실행 흐름)          "비즈니스 실행 흐름을 무엇이 결정하나?" │
│     [코드 직접 작성] │ Metadata-Driven │ Workflow Engine │ Rule Engine  │
│                                                                        │
│  [대괄호] = 명시적 선택 없이 Spring Boot 프로젝트를 만들면 자동으로         │
│             적용되는 기본값                                               │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.4 기본값 원칙

**명시적으로 선택하지 않으면 자동으로 기본값이 적용된다:**

| 카테고리 | 기본값 | 의미 |
|---------|-------|------|
| A. 배포 단위 | Monolithic | 하나의 JAR로 배포 |
| B. 코드 구조 | Layered | Controller → Service → Repository |
| C. 도메인 모델링 | Transaction Script | Service에 절차적 로직 작성 |
| D. 데이터 흐름 | 단일 모델 | 읽기/쓰기 동일 경로 |
| E. 시스템 통합 | 동기 호출 | 메서드 직접 호출 |
| F. 실행 제어 | 코드 직접 작성 | 실행 흐름이 Java 코드에 명시 |

> **"아키텍처를 선택하지 않았다"는 것은 불가능하다.**
> 선택하지 않으면 위 기본값 조합이 자동으로 적용된 것이다.
> 이것이 대부분의 Spring Boot 프로젝트가 같은 구조를 갖는 이유다.

### 1.5 분류 기준의 독립성

각 카테고리는 **독립적인 결정 축**이다. 예시:

```
프로젝트 X:  A=Modular Monolith + B=Hexagonal + C=Domain Model + D=CQRS + E=Event-Driven + F=코드 직접 작성
프로젝트 Y:  A=Monolithic + B=Layered + C=Transaction Script + D=단일 모델 + E=동기 호출 + F=코드 직접 작성
프로젝트 Z:  A=Microservices + B=Vertical Slice + C=Domain Model + D=Event Sourcing + E=Saga + F=Workflow Engine
```

---

## 2. 카테고리 A: 배포 단위 아키텍처 — "시스템을 어떻게 나눠서 배포하는가"

> 이 카테고리는 **전체 시스템의 물리적 배포 구조**를 결정한다.
> 코드를 어떻게 쓰는지(B, C)와는 독립적이다.

### 2.1 Monolithic (모놀리식)

구조:
```
┌──────────────────────────────────────┐
│           단일 애플리케이션             │
│                                      │
│  직원관리 + 급여계산 + 회계처리 + ...   │
│                                      │
│  하나의 코드베이스, 하나의 빌드,         │
│  하나의 배포 단위                      │
└──────────────────────────────────────┘
         │
    단일 DB
```

핵심 특성:
- 모든 기능이 하나의 프로세스에서 실행
- 하나의 코드베이스, 하나의 빌드 산출물 (JAR/WAR)
- 내부적으로 코드가 어떻게 구조화되든 배포는 하나

장점:
- 개발, 테스트, 배포가 가장 단순
- 트랜잭션 관리가 쉬움 (단일 DB, ACID 보장)
- 로컬에서 전체 시스템 실행 가능
- 모듈 간 호출이 메서드 호출 (네트워크 없음 = 빠르고 안정적)

단점:
- 규모가 커지면 빌드/배포 시간 증가
- 하나의 모듈 장애가 전체 시스템에 영향
- 기술 스택 고정 (하나의 언어/프레임워크)
- 팀이 커지면 코드 충돌과 조율 비용 증가

적합한 상황:
- 팀 1~10명, 프로젝트 초기~중기
- 도메인 경계가 아직 불명확한 경우
- 빠른 개발과 단순한 운영이 필요한 경우

### 2.2 Modular Monolith (모듈형 모놀리스)

구조:
```
┌──────────────────────────────────────────────────────┐
│                  단일 배포 단위 (하나의 JAR)             │
│                                                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Employee  │  │  Payroll  │  │ Accounting│       │
│  │  Module    │  │  Module   │  │  Module   │  ...  │
│  │           │  │           │  │           │       │
│  │  공개 API  │──│  공개 API  │──│  공개 API  │       │
│  │  (interface)│  │  (interface)│  │  (interface)│       │
│  │           │  │           │  │           │       │
│  │ [내부 구현  │  │ [내부 구현  │  │ [내부 구현  │       │
│  │  은닉됨]   │  │  은닉됨]   │  │  은닉됨]   │       │
│  └───────────┘  └───────────┘  └───────────┘       │
│                                                      │
│  규칙: 모듈 간 통신은 반드시 공개 API를 통해서만           │
│        모듈 내부 클래스를 다른 모듈이 직접 참조 금지        │
└──────────────────────────────────────────────────────┘
```

핵심 특성:
- **배포는 모놀리스** (단일 JAR/WAR)이지만 **내부적으로 강한 모듈 경계**를 유지
- 각 모듈은 자신의 공개 인터페이스만 노출, 내부 구현은 은닉
- Microservices의 "경계 분리" 장점 + Monolithic의 "단일 배포 단순함"
- Spring Modulith (2023~)가 이를 공식 지원

Monolithic과의 차이:
```
Monolithic:          → EmployeeService가 PayrollRepository를 직접 호출 가능
                       (경계 없음, 아무거나 import)

Modular Monolith:    → EmployeeModule은 PayrollModule의 공개 API만 호출
                       (PayrollInternalService는 접근 불가)
                       모듈 간 의존성이 명시적이고 강제됨
```

장점:
- 모놀리스의 단순한 배포 + 마이크로서비스의 경계 분리
- 나중에 마이크로서비스로 전환 시 모듈 경계가 그대로 서비스 경계
- 단일 프로세스이므로 트랜잭션/디버깅이 쉬움
- 모듈별 독립적 개발이 가능하면서도 네트워크 복잡성 없음

단점:
- 모듈 경계를 강제하는 규율이 필요 (도구나 규칙 없이는 경계가 무너짐)
- 결국 하나의 프로세스이므로 독립 스케일링은 불가
- 모듈 간 DB 분리를 하지 않으면 데이터 레벨 커플링 위험

적합한 상황:
- 팀 2~15명, 도메인이 여러 개이지만 마이크로서비스까지는 불필요
- 나중에 마이크로서비스 전환 가능성을 열어두고 싶은 경우
- 모듈별 독립 개발이 필요하지만 운영 복잡도를 낮추고 싶은 경우

대표 사례: Shopify (Ruby 모놀리스를 모듈화), Spring Modulith 프로젝트

### 2.3 Microservices (마이크로서비스)

구조:
```
┌───────────┐     ┌───────────┐     ┌───────────┐
│  Employee  │     │  Payroll  │     │ Accounting│
│  Service   │     │  Service  │     │  Service  │
│           │     │           │     │           │
│ 자체 DB    │     │ 자체 DB    │     │ 자체 DB    │
└─────┬─────┘     └─────┬─────┘     └─────┬─────┘
      │                 │                 │
      └────── 네트워크 통신 (REST/gRPC/Event) ──────┘
              각각 독립 배포, 독립 스케일링
```

핵심 특성:
- 각 서비스가 독립된 프로세스, 독립된 DB, 독립 배포
- 서비스 간 통신은 네트워크를 통해 (REST, gRPC, 메시지 큐)
- 각 서비스가 자체 기술 스택을 선택할 수 있음 (Polyglot)

장점:
- 서비스별 독립 배포, 독립 스케일링
- 장애 격리 (하나의 서비스 장애가 전체에 영향 최소화)
- 팀별 독립적 개발 속도
- 기술 스택 자유도

단점:
- **운영 복잡도가 매우 높음**: 서비스 디스커버리, 로드밸런싱, 서킷브레이커, 분산 추적
- **분산 트랜잭션 문제**: 2PC 또는 Saga 필요
- **데이터 일관성**: 서비스 간 최종 일관성(Eventual Consistency)만 보장
- **네트워크 지연과 장애**: 모든 호출이 네트워크를 탐
- **테스트 복잡도**: 통합 테스트가 매우 어려움
- **오버헤드**: 각 서비스마다 CI/CD, 모니터링, 로깅 필요

적합한 상황:
- 대규모 팀 (20명+), 여러 팀이 독립적으로 개발
- 서비스별 독립 스케일링이 비즈니스적으로 필요한 경우
- 도메인 경계가 명확하고 서비스 간 결합이 낮은 경우

> **중요**: 1~2명 팀에서 마이크로서비스는 거의 항상 과잉이다.
> "마이크로서비스는 조직의 문제(여러 팀의 독립성)를 해결하는 것이지, 기술의 문제를 해결하는 것이 아니다." — Sam Newman

대표 사례: Netflix, Amazon, Uber (모두 100명+ 엔지니어링 조직)

### 2.4 Serverless

구조:
```
API Gateway → Lambda/Cloud Function → 관리형 DB
                    │
              이벤트 트리거 (S3, SQS, ...)
              자동 스케일링, 사용한 만큼 과금
```

핵심 특성:
- 서버를 직접 관리하지 않음 (FaaS: Function as a Service)
- 요청이 있을 때만 실행, 사용한 만큼 과금
- AWS Lambda, Google Cloud Functions, Azure Functions

장점:
- 인프라 관리 부담 제로
- 자동 스케일링, 요청 없으면 비용 없음
- 빠른 프로토타이핑에 유리

단점:
- Cold Start 지연 (JVM 기반은 특히 심각)
- 실행 시간 제한 (Lambda: 15분)
- 상태 관리 어려움 (함수는 Stateless)
- 로컬 개발/디버깅이 어려움
- 벤더 종속(Vendor Lock-in)

적합한 상황:
- 이벤트 기반 비동기 처리 (파일 업로드 후 처리, 알림 전송)
- 트래픽이 매우 불규칙한 서비스
- 빠른 MVP, 사이드 프로젝트

> Spring Boot 기반 프로젝트에서는 주 아키텍처보다는 보조적으로 사용하는 경우가 많음 (예: 비동기 배치 처리를 Lambda로)

### 2.5 배포 단위 아키텍처 비교 요약

| 기준 | Monolithic | Modular Monolith | Microservices | Serverless |
|------|-----------|-----------------|---------------|-----------|
| 배포 단위 | 1개 | 1개 (내부 모듈화) | N개 | 함수 단위 |
| 운영 복잡도 | ★ | ★★ | ★★★★★ | ★★★ |
| 독립 스케일링 | 불가 | 불가 | 가능 | 자동 |
| 트랜잭션 | 단일 DB ACID | 단일 DB ACID | 분산 트랜잭션 필요 | Stateless |
| 디버깅 | ★★★★★ | ★★★★ | ★★ | ★★ |
| 팀 독립성 | 낮음 | 중간 | 높음 | 높음 |
| 적합 팀 규모 | 1~10 | 2~15 | 20+ | 1~5 |
| 적합 도메인 | 소~중 | 중~대 | 대 | 이벤트 처리 |

---

## 3. 카테고리 B: 코드 구조 아키텍처 — "하나의 배포 단위 안에서 코드를 어떻게 배치하는가"

> 이 카테고리는 **하나의 애플리케이션(또는 모듈) 내부의 패키지/클래스 구조**를 결정한다.
> 어떤 배포 단위(A)를 사용하든, 그 내부 코드는 이 카테고리의 패턴 중 하나로 구조화된다.

### 3.1 Layered Architecture (계층형 아키텍처)

구조:
```
┌──────────────────┐
│  Presentation    │  Controller, DTO
├──────────────────┤
│  Application     │  Service (유스케이스 오케스트레이션)
├──────────────────┤
│  Domain          │  Entity, Value Object (선택적)
├──────────────────┤
│  Infrastructure  │  Repository, 외부 API Client
└──────────────────┘
  의존성: 위 → 아래 (단방향)
```

핵심 규칙:
- 상위 계층만 하위 계층을 호출할 수 있다
- 같은 계층 내 호출은 허용 (Service → Service)
- 계층 스킵은 허용하지 않는 것이 원칙 (Controller가 직접 Repository 호출 금지)

장점:
- 가장 직관적이고 학습 곡선이 낮음
- Spring Boot가 기본적으로 권장하는 구조
- IDE 자동완성, 디버깅이 가장 쉬움
- 대부분의 개발자가 이미 알고 있어 채용·온보딩이 쉬움

단점:
- Service 계층이 비대해지는 "Fat Service" 문제 (God Class)
- 도메인 로직이 Service에 흩어지거나 Repository에 누출됨
- 비즈니스 규칙 변경 시 여러 Service를 수정해야 할 수 있음
- 테스트 시 DB/외부 의존성 mock이 복잡해질 수 있음

적합한 상황:
- 팀 규모 1~5명
- 도메인 복잡도가 낮거나 중간
- CRUD 위주 애플리케이션
- 빠른 MVP 개발이 필요한 경우

대표 사례: 대부분의 Spring Boot 프로젝트, Rails, Django 기본 구조

---

### 3.2 Hexagonal Architecture (포트 & 어댑터)

구조:
```
          ┌─────────────────────────────┐
Adapter → │  Port(Interface)            │
(REST)    │       ↓                     │
          │  ┌─────────────────────┐    │ ← Port(Interface)  → Adapter
          │  │    Domain Core      │    │                      (DB)
          │  │  (비즈니스 로직만)     │    │
          │  └─────────────────────┘    │ ← Port(Interface)  → Adapter
Adapter → │  Port(Interface)            │                      (외부API)
(Batch)   └─────────────────────────────┘
```

핵심 규칙:
- 도메인 코어는 외부를 모른다 — 어떤 DB를 쓰는지, REST인지 gRPC인지 모름
- 외부와의 소통은 반드시 Port(인터페이스)를 통해서만
- 의존성 방향: Adapter → Port → Domain (도메인이 중심)
- Port는 두 종류: Inbound(Driving) — 외부가 도메인을 호출 / Outbound(Driven) — 도메인이 외부에 의존

장점:
- 도메인 로직이 프레임워크에 독립적 → 단위 테스트가 매우 쉬움
- 인바운드/아웃바운드 어댑터 교체가 자유로움 (DB 교체, API 프로토콜 변경)
- 관심사 분리가 명확

단점:
- 인터페이스(Port) 수가 많아져서 보일러플레이트 증가
- 간단한 CRUD에도 Port + Adapter + Domain 클래스가 필요
- Layered보다 학습 곡선이 높음
- 작은 프로젝트에서는 과잉 설계(over-engineering)가 될 수 있음

적합한 상황:
- 외부 시스템 연동이 많은 프로젝트
- DB나 인프라 변경 가능성이 높은 경우
- 도메인 로직의 단위 테스트가 중요한 경우
- 팀이 TDD/BDD를 실천하는 경우

대표 사례: Netflix Zuul, Spotify 내부 서비스, Alistair Cockburn 원저

---

### 3.3 Clean Architecture

구조:
```
┌─────────────────────────────────────┐
│  Frameworks & Drivers               │  Spring, JPA, Web
│  ┌─────────────────────────────┐    │
│  │  Interface Adapters          │    │  Controller, Gateway, Presenter
│  │  ┌─────────────────────┐    │    │
│  │  │  Use Cases           │    │    │  Application Service (비즈니스 유스케이스)
│  │  │  ┌─────────────┐    │    │    │
│  │  │  │  Entities    │    │    │    │  Enterprise Business Rules (핵심 도메인)
│  │  │  └─────────────┘    │    │    │
│  │  └─────────────────────┘    │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
  의존성: 바깥 → 안쪽 (Dependency Rule)
```

핵심 규칙:
- 의존성 규칙(Dependency Rule): 안쪽 원은 바깥쪽 원에 대해 절대 알 수 없다
- Entities는 가장 일반적인 비즈니스 규칙 (프레임워크와 완전 독립)
- Use Cases는 애플리케이션 고유의 비즈니스 규칙
- Hexagonal과 유사하나 **Use Case 계층이 명시적으로 분리**됨

장점:
- 프레임워크 독립성이 가장 높음 (Spring → Quarkus 전환도 이론적으로 가능)
- Entities 계층의 단위 테스트가 가장 순수함
- Use Case 단위로 기능을 구분하므로 기능 추가/제거가 깔끔

단점:
- 가장 많은 보일러플레이트 — 계층 간 데이터 변환(DTO → Domain → Entity → Response)이 많음
- 현실에서 "프레임워크 교체"가 발생하는 경우는 극히 드묾
- 과잉 추상화의 위험이 가장 높음
- Robert C. Martin의 원저가 모호한 부분이 있어 해석이 갈림

적합한 상황:
- 10년 이상 유지보수해야 하는 장기 프로젝트
- 프레임워크 교체 가능성이 실제로 있는 경우
- 도메인 규칙이 매우 복잡하고 비즈니스 크리티컬한 경우
- 대규모 팀 (10명+)이 동시 개발하는 경우

대표 사례: 금융권 코어 뱅킹 시스템, 대기업 ERP 내부 모듈

---

### 3.4 Onion Architecture (양파 아키텍처)

구조:
```
┌───────────────────────────────────┐
│  Infrastructure (외부 계층)         │  DB, File, External API, Framework
│  ┌───────────────────────────┐    │
│  │  Application Services      │    │  유스케이스 오케스트레이션, DTO
│  │  ┌───────────────────┐    │    │
│  │  │  Domain Services   │    │    │  여러 Aggregate에 걸친 도메인 로직
│  │  │  ┌─────────────┐  │    │    │
│  │  │  │Domain Model │  │    │    │  Entity, Value Object, Aggregate
│  │  │  └─────────────┘  │    │    │
│  │  └───────────────────┘    │    │
│  └───────────────────────────┘    │
└───────────────────────────────────┘
  의존성: 바깥 → 안쪽 (Clean Architecture와 동일)
```

핵심 규칙:
- Clean Architecture와 같은 의존성 규칙 (바깥 → 안쪽)
- **Domain Service와 Application Service를 명확히 구분**하는 것이 핵심 차이점
- Domain Model이 최중심, Infrastructure가 가장 바깥

Clean Architecture와의 차이:
| 측면 | Clean Architecture | Onion Architecture |
|------|-------------------|-------------------|
| 제안자 | Robert C. Martin (2012) | Jeffrey Palermo (2008) |
| 핵심 강조 | Use Case 계층의 독립성 | Domain Service vs Application Service 분리 |
| 계층 이름 | Entities / Use Cases / Adapters / Frameworks | Domain Model / Domain Services / App Services / Infra |
| 생태계 | 언어 무관 (Java, JS, Go 모두) | 주로 .NET 생태계 |
| 실무 차이 | 거의 동일 | 거의 동일 |

> 실무에서는 Clean Architecture와 Onion Architecture를 구분하지 않고 사용하는 경우가 많다.
> 둘 다 "의존성이 안쪽을 향한다"는 동일 원칙의 변형이며, 핵심 가치는 같다.

---

### 3.5 Vertical Slice Architecture (수직 슬라이스 아키텍처)

구조:
```
전통적 Layered (수평 분할):          Vertical Slice (수직 분할):
┌──────────────────────┐          ┌──────┐ ┌──────┐ ┌──────┐
│    Controllers       │          │직원등록│ │급여계산│ │전표생성│
├──────────────────────┤          │      │ │      │ │      │
│    Services          │          │ Ctrl │ │ Ctrl │ │ Ctrl │
├──────────────────────┤          │ Svc  │ │ Svc  │ │ Svc  │
│    Repositories      │          │ Repo │ │ Repo │ │ Repo │
└──────────────────────┘          └──────┘ └──────┘ └──────┘

수평: "모든 Controller"가 한 폴더     수직: "직원등록에 필요한 모든 것"이 한 폴더
수평: 기술 계층으로 분류               수직: 기능(Feature)으로 분류
```

핵심 규칙:
- **기술 계층이 아닌 기능(Feature/UseCase) 단위로 코드를 구성**
- 하나의 기능에 필요한 Controller, Service, Repository, DTO가 모두 한 곳에
- 기능 간 공유 코드는 별도 shared 계층에 (최소화)
- 각 슬라이스가 독립적으로 구현 가능

장점:
- **기능 추가/수정 시 관련 코드가 한 곳에 모여 있음** → 인지 부담 최소
- 슬라이스 간 결합이 낮아 독립적 변경 가능
- 코드 내비게이션이 직관적 ("급여계산 관련 코드는 payroll-calculation/ 폴더에 다 있음")
- 불필요한 추상화 없이 각 기능에 최적화된 구현 가능

단점:
- 슬라이스 간 공통 로직 재사용이 덜 구조화됨
- 동일한 도메인 엔티티를 여러 슬라이스에서 다르게 표현할 수 있음 (일관성 위험)
- 프로젝트가 커지면 슬라이스 수가 매우 많아짐
- 기존 Layered에 익숙한 개발자에게 낯설 수 있음

적합한 상황:
- 기능별로 독립적인 변경이 잦은 프로젝트
- 각 기능의 복잡도가 다양한 경우 (단순 CRUD ~ 복잡 로직 혼재)
- **"하나의 기능을 수정할 때 여러 패키지를 돌아다니는 것"이 비용인 경우**
- CQRS와 자연스럽게 결합 (각 Command/Query가 하나의 슬라이스)

대표 사례: Jimmy Bogard의 MediatR 패턴 (.NET), 일부 Spring 프로젝트에서 feature-based 패키지 구조

---

### 3.6 코드 구조 아키텍처 비교 요약

| 기준 | Layered | Hexagonal | Clean | Onion | Vertical Slice |
|------|---------|-----------|-------|-------|---------------|
| 코드 분류 기준 | 기술 계층 | Port/Adapter | 의존성 원 | 의존성 원 | 기능(Feature) |
| 의존성 방향 | 위→아래 | Adapter→Domain | 바깥→안쪽 | 바깥→안쪽 | 슬라이스 내 자유 |
| 보일러플레이트 | ★ (최소) | ★★★ | ★★★★ | ★★★★ | ★★ |
| 테스트 격리 | ★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| 기능 수정 시 변경 범위 | 여러 패키지 | 여러 패키지 | 여러 패키지 | 여러 패키지 | **한 폴더** |
| 학습 곡선 | ★ (최저) | ★★★ | ★★★★ | ★★★★ | ★★ |
| 도메인 보호 | ★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ |

---

## 4. 카테고리 C: 도메인 모델링 패턴 — "비즈니스 로직을 어떻게 표현하는가"

> 이 카테고리는 코드 구조(B)와 독립적으로, **비즈니스 로직이 코드에서 어떤 형태로 존재하는가**를 결정한다.
> Martin Fowler의 "Patterns of Enterprise Application Architecture"에서 분류한 3가지 기본 패턴이다.

### 4.1 Transaction Script

구조:
```java
// Service가 비즈니스 로직을 절차적으로 처리
public class PayrollService {
    public void calculatePayroll(Long employeeId, String yearMonth) {
        // 1. 직원 조회
        Employee emp = employeeRepo.findById(employeeId);
        // 2. 근무일수 계산
        int workDays = calculateWorkDays(emp, yearMonth);
        // 3. 기본급 계산
        BigDecimal basePay = emp.getSalary().multiply(workDays).divide(totalDays);
        // 4. 4대보험 계산
        BigDecimal insurance = basePay.multiply(INSURANCE_RATE);
        // 5. 저장
        payrollRepo.save(new PayrollResult(emp, basePay, insurance));
    }
}
```

핵심 특성:
- **비즈니스 로직이 Service 메서드에 절차적으로 작성됨**
- 도메인 객체(Entity)는 데이터 컨테이너(getter/setter)에 불과
- 하나의 요청 = 하나의 트랜잭션 스크립트
- "빈약한 도메인 모델(Anemic Domain Model)"이라고도 불림

장점:
- 가장 직관적 — 로직 흐름이 코드 순서대로 읽힘
- 단순 CRUD에서 가장 빠른 구현 속도
- 모든 개발자가 즉시 이해 가능
- 디버깅이 쉬움 (스택 트레이스 = 비즈니스 흐름)

단점:
- 로직이 복잡해지면 Service가 비대해짐 (Fat Service / God Class)
- 같은 비즈니스 규칙이 여러 Service에 중복됨
- 도메인 불변식(invariant)이 코드에 명시적이지 않음
- 로직과 데이터가 분리되어 객체지향의 장점을 활용하지 못함

적합한 상황:
- 단순 CRUD 위주 (비즈니스 규칙이 적음)
- 빠른 MVP, 프로토타이핑
- 팀이 주니어 위주일 때

### 4.2 Table Module

구조:
```java
// 테이블 하나에 대응하는 클래스가 해당 테이블의 모든 로직을 담당
public class EmployeeModule {
    private DataTable employeeTable;  // DB 테이블의 인메모리 표현

    public void register(EmployeeData data) { /* 등록 로직 */ }
    public void terminate(Long id) { /* 퇴직 처리 로직 */ }
    public BigDecimal calculateTotalSalary(String yearMonth) { /* 집계 */ }
}
```

핵심 특성:
- **DB 테이블 하나에 클래스 하나가 대응**
- 해당 테이블에 대한 모든 비즈니스 로직이 하나의 클래스에 집중
- Transaction Script와 Domain Model의 중간 단계
- .NET의 DataSet/DataTable 패턴에서 유래

장점:
- Transaction Script보다 로직이 응집됨 (테이블별로 모임)
- Domain Model보다 단순함 (식별자, 불변식 설계 불필요)
- 기존 DB 스키마에 맞추기 쉬움

단점:
- 여러 테이블에 걸친 비즈니스 규칙 표현이 어려움
- 객체 간 관계(has-a, is-a)를 표현하지 못함
- Java/Spring 생태계에서는 잘 사용되지 않음 (.NET에서 주로 사용)

적합한 상황:
- DB 중심 설계, 테이블 단위 로직이 대부분인 경우
- .NET + DataSet 기반 레거시 시스템

### 4.3 Domain Model (DDD 전술적 패턴)

DDD는 설계 사상이다. 전략적 패턴과 전술적 패턴으로 나뉜다.

전략적 패턴 (팀/시스템 수준 — 카테고리 A, E와 연관):

| 패턴 | 설명 | 효과 |
|------|------|------|
| Bounded Context | 같은 용어가 다른 의미를 갖는 경계 정의 | "계약"이 HR에서와 법무에서 다른 엔티티 |
| Context Map | Bounded Context 간 관계 정의 | 팀 간 통합 전략 명확화 |
| Ubiquitous Language | 코드에 비즈니스 용어 그대로 사용 | 개발자-도메인 전문가 소통 |
| Anti-Corruption Layer | 외부 시스템의 모델이 내부를 오염시키지 않게 방어 | 레거시 연동 시 필수 |

전술적 패턴 (코드 수준 — 이 카테고리의 핵심):

| 패턴 | 설명 | 예시 |
|------|------|------|
| Aggregate | 일관성 경계 (트랜잭션 단위) | `PayrollRun` + `PayrollResult` + `AllowanceLine` |
| Aggregate Root | Aggregate의 진입점 (불변식 보호) | `PayrollRun`이 Root |
| Entity | 식별자로 구분되는 도메인 객체 | `Employee(id)` |
| Value Object | 값으로 비교되는 불변 객체 | `Money(amount, currency)`, `Address(...)` |
| Domain Event | 도메인에서 발생한 사건 | `PayrollCalculated`, `EmployeeRegistered` |
| Domain Service | 단일 Aggregate에 속하지 않는 도메인 로직 | `PayrollCalculator` |
| Repository | Aggregate 단위 영속화 | `PayrollRunRepository` |
| Factory | 복잡한 Aggregate 생성 | `PayrollRunFactory.create(facility, yearMonth)` |

구조 예시:
```java
// 비즈니스 로직이 도메인 객체 안에 존재
public class PayrollRun {          // Aggregate Root
    private PayrollRunId id;        // Value Object
    private FacilityId facilityId;  // Value Object
    private YearMonth period;
    private List<PayrollLine> lines;  // Aggregate 내부 엔티티
    private PayrollStatus status;

    public PayrollResult calculate() {
        // 불변식(invariant) 검증
        if (this.status != DRAFT) throw new IllegalStateException("확정된 급여는 재계산 불가");
        // 비즈니스 로직이 도메인 객체 안에 존재
        Money totalGross = lines.stream().map(PayrollLine::grossPay).reduce(Money.ZERO, Money::add);
        // 도메인 이벤트 발생
        registerEvent(new PayrollCalculated(this.id, totalGross));
        return new PayrollResult(this.id, totalGross);
    }
}
```

장점:
- 복잡한 도메인 로직을 가장 정확하게 표현
- 비즈니스 전문가와 개발자가 같은 언어로 소통
- 불변식(invariant)이 코드에 명시적으로 존재 → 버그 감소
- Aggregate 경계가 트랜잭션/일관성 경계와 일치

단점:
- 학습 곡선이 가장 높음 — Eric Evans의 원저는 560페이지
- 도메인 전문가와의 지속적 협업이 필요 (없으면 "가짜 DDD"가 됨)
- 단순 CRUD에 DDD를 적용하면 과잉 설계
- Value Object, Aggregate 경계 설계가 잘못되면 오히려 복잡도 증가
- "DDD를 한다"고 하면서 실제로는 "폴더 이름만 domain인 Layered"인 경우가 많음

적합한 상황:
- 도메인 규칙이 복잡하고 자주 변경되는 경우
- 도메인 전문가(현업 담당자)와 긴밀히 협업 가능한 경우
- 팀에 DDD 경험자가 1명 이상 있는 경우
- 비즈니스 규칙 오류가 치명적인 시스템 (금융, 의료, 보험)

대표 사례: 독일 보험사 내부 시스템, 금융 트레이딩 플랫폼

### 4.4 도메인 모델링 패턴 비교 요약

| 기준 | Transaction Script | Table Module | Domain Model (DDD) |
|------|-------------------|-------------|-------------------|
| 로직 위치 | Service 메서드 | 테이블 대응 클래스 | 도메인 객체 내부 |
| 도메인 객체 역할 | 데이터 컨테이너 | 데이터+로직 (테이블 단위) | 풍부한 행위 보유 |
| 불변식 보호 | 없음 (서비스에서 검증) | 부분적 | 명시적 (Aggregate Root) |
| 복잡도 대응력 | 낮음 | 중간 | 높음 |
| 적합한 복잡도 | 단순 CRUD | 테이블 단위 로직 | 복잡한 비즈니스 규칙 |
| 학습 곡선 | ★ | ★★ | ★★★★★ |

> **핵심 인사이트**: 하나의 프로젝트에서도 영역별로 다른 패턴을 적용할 수 있다.
> 예: 직원 CRUD = Transaction Script / 급여계산 = Domain Model

---

## 5. 카테고리 D: 데이터 흐름 패턴 — "데이터를 어떻게 읽고 쓰는가"

> 이 카테고리는 **데이터의 읽기와 쓰기 경로를 어떻게 설계하는가**를 결정한다.
> 코드 구조(B)나 도메인 모델링(C)과는 독립적으로 적용할 수 있다.

### 5.1 단일 모델 (기본형)

```
Client → Controller → Service → Repository → DB (읽기/쓰기 동일 경로)
```

- 가장 단순, 대부분의 프로젝트 기본값
- 읽기와 쓰기가 같은 모델, 같은 경로, 같은 DB
- 적합: 읽기/쓰기 복잡도가 비슷한 경우

### 5.2 CQRS (Command Query Responsibility Segregation)

구조:
```
Client ──┬── Command ──→ Write Model ──→ Command DB
         │                    │
         │              Domain Event
         │                    │
         └── Query ──→ Read Model ──→ Query DB (or same DB, different view)
```

핵심 규칙:
- 데이터를 변경하는 경로(Command)와 조회하는 경로(Query)를 분리
- Write Model은 비즈니스 규칙 검증에 최적화
- Read Model은 조회 성능에 최적화 (비정규화, 인덱스, 캐시)

단독 CQRS (Event Sourcing 없이):
- 같은 DB에서 Write는 정규화된 테이블, Read는 뷰/DTO로 분리
- 가장 실용적이고 도입 비용이 낮은 형태
- v0.3이 이 형태를 사용

CQRS + Event Sourcing:
- Write 측에서 상태 변경을 이벤트로 저장
- Read 측에서 이벤트를 구독하여 조회용 모델을 구성
- 최종 일관성(Eventual Consistency) 허용이 필요

장점:
- 읽기/쓰기 최적화를 독립적으로 할 수 있음
- 조회 성능 튜닝이 비즈니스 로직에 영향을 주지 않음
- 스케일링이 독립적 (읽기 부하만 높으면 Read Replica 추가)

단점:
- 두 모델 간 데이터 동기화 복잡성
- Event Sourcing과 결합 시 학습 곡선이 급격히 상승
- 단순한 CRUD 앱에서는 불필요한 복잡도

적합한 상황:
- 읽기:쓰기 비율이 10:1 이상으로 차이가 큰 경우
- 복잡한 조회 요구사항 (다중 조인, 집계, 필터)
- 쓰기 모델과 읽기 모델의 구조가 본질적으로 다른 경우

---

### 5.3 Event Sourcing

구조:
```
Command → Domain Logic → Event(s) → Event Store (append-only)
                                         │
                                    Event Replay
                                         │
                                    Current State (재구성)
```

핵심 규칙:
- 상태를 직접 저장하지 않고 상태 변경 이벤트만 저장
- 현재 상태 = 이벤트를 처음부터 순서대로 재생한 결과
- 이벤트는 불변(immutable), 삭제/수정 불가

장점:
- 완전한 감사 추적 (모든 변경 이력이 자동으로 보존)
- 시간 여행(Time Travel) — 특정 시점의 상태를 정확히 복원 가능
- 이벤트 재생으로 버그 재현이 쉬움
- 이벤트 기반 통합이 자연스러움

단점:
- 가장 높은 구현 복잡도 — 초기 구현 + 운영 모두
- 이벤트 스키마 버전 관리(Event Versioning)가 어려움
- 조회가 기본적으로 느림 (매번 이벤트 재생) → CQRS 거의 필수
- 개발자 채용이 어려움 (경험자가 적음)
- "삭제"라는 개념이 없음 (보상 이벤트로 처리)

적합한 상황:
- 법적으로 모든 변경 이력 보존이 필수인 경우 (금융 원장)
- 복잡한 이벤트 기반 비즈니스 프로세스
- 팀에 Event Sourcing 경험자가 있는 경우
- 이벤트 재생/시간 여행이 비즈니스 요구사항인 경우

대표 사례: 은행 원장 시스템, Axon Framework 기반 프로젝트

---

### 5.4 Pipe and Filter (파이프 & 필터)

구조:
```
Input → [Filter A] → [Filter B] → [Filter C] → Output
         (검증)       (변환)        (계산)

각 Filter는 독립적:
  - 하나의 입력을 받아 하나의 출력을 생성
  - 이전/이후 Filter에 대해 알지 못함
  - 독립적으로 테스트 가능
```

핵심 특성:
- 데이터 처리를 **독립적인 단계(Filter)**의 체인으로 구성
- 각 Filter는 입력을 받아 변환/처리 후 다음 Filter로 전달
- Filter의 추가/제거/순서 변경이 자유로움

장점:
- 각 단계가 독립적 → 단위 테스트가 매우 쉬움
- 단계 추가/제거가 용이 (새 필터를 체인에 끼워넣기)
- 병렬 처리가 자연스러움

단점:
- 단계 간 데이터 변환 오버헤드
- 전체 파이프라인의 에러 핸들링이 복잡할 수 있음
- 상태를 공유해야 하는 경우에는 부적합

적합한 상황:
- 데이터 변환/처리 파이프라인 (ETL)
- 단계별 처리가 자연스러운 도메인 (급여계산: 기본급 → 수당 → 4대보험 → 세금)
- 스트리밍 데이터 처리

대표 사례: Apache Kafka Streams, Spring Integration, Unix 파이프, Java Stream API

### 5.5 데이터 흐름 패턴 비교 요약

| 기준 | 단일 모델 | CQRS | Event Sourcing | Pipe & Filter |
|------|----------|------|---------------|--------------|
| 복잡도 | ★ | ★★★ | ★★★★★ | ★★ |
| 조회 최적화 | ★★ | ★★★★★ | ★★★★ (Projection) | 해당없음 |
| 이력 추적 | ★ | ★★ | ★★★★★ | ★ |
| 데이터 처리 유연성 | ★★ | ★★★ | ★★★★ | ★★★★★ |
| 적합한 영역 | 범용 | 읽기/쓰기 비대칭 | 이력 보존 필수 | 단계별 처리 |

---

## 6. 카테고리 E: 시스템 통합 패턴 — "모듈/시스템 간 어떻게 소통하는가"

> 이 카테고리는 **모듈, 서비스, 외부 시스템 간의 통신 방식**을 결정한다.
> 배포 단위(A)가 Microservices이면 이 카테고리의 중요도가 크게 높아진다.
> Modular Monolith에서도 모듈 간 느슨한 결합을 위해 활용된다.

### 6.1 동기 호출 (Synchronous)

```
Module A ──(메서드 호출 or REST/gRPC)──→ Module B ──→ 응답 대기 ──→ Module A 계속
```

- 가장 단순하고 직관적
- 호출자가 응답을 기다림 (Blocking)
- Monolith에서는 메서드 호출, Microservices에서는 REST/gRPC
- 단점: 호출 체인이 길어지면 지연 누적, 장애 전파

### 6.2 Event-Driven Architecture (이벤트 기반)

```
Module A → Event 발행 → Event Bus/Broker → Module B (구독)
                                          → Module C (구독)
    (A는 B, C의 존재를 모름. 이벤트만 발행)
```

핵심 특성:
- 모듈 간 **직접 호출 대신 이벤트를 통해 간접 소통**
- 발행자(Publisher)는 구독자(Subscriber)를 알지 못함 → 느슨한 결합
- 비동기 처리가 기본

구현 방식:
- **In-Process**: Spring ApplicationEvent, EventBus (Modular Monolith에서 사용)
- **Message Broker**: Kafka, RabbitMQ, AWS SQS (Microservices에서 사용)
- **Transactional Outbox**: 이벤트 발행의 원자성 보장 (DB 트랜잭션 + 이벤트 아웃박스 테이블)

장점:
- 모듈 간 결합도가 가장 낮음
- 새 구독자 추가가 발행자 변경 없이 가능
- 비동기 처리로 응답 성능 향상

단점:
- 최종 일관성(Eventual Consistency) — 즉각 일관성 보장 불가
- 이벤트 순서 보장, 중복 처리(멱등성) 고려 필요
- 디버깅이 어려움 (이벤트 흐름 추적)
- 이벤트 스키마 관리 필요

### 6.3 Saga Pattern (사가 패턴)

```
분산 트랜잭션 문제:
  주문 생성 → 결제 처리 → 재고 차감 → 배송 요청
  (각각 다른 서비스/DB → 하나의 ACID 트랜잭션 불가)

Saga로 해결:
  Choreography (안무):
    주문 생성 → OrderCreated 이벤트 → 결제 서비스가 구독 → 결제 완료
    → PaymentCompleted 이벤트 → 재고 서비스가 구독 → ...
    (실패 시 보상 이벤트 발행: PaymentFailed → 주문 취소)

  Orchestration (지휘):
    SagaOrchestrator가 각 단계를 순서대로 호출
    → 실패 시 이전 단계의 보상(Compensation)을 역순으로 실행
```

핵심 특성:
- **분산 환경에서 여러 서비스에 걸친 비즈니스 트랜잭션**을 관리
- ACID 대신 보상 트랜잭션(Compensation)으로 일관성 유지
- 두 가지 방식: Choreography (이벤트 기반 자율) / Orchestration (중앙 조율)

적합한 상황:
- Microservices에서 여러 서비스에 걸친 비즈니스 프로세스
- 2PC(Two-Phase Commit)가 불가능하거나 성능 문제가 있는 경우

> Modular Monolith에서는 단일 DB ACID 트랜잭션으로 처리 가능하므로 Saga가 불필요한 경우가 많다.

### 6.4 API Gateway / BFF (Backend For Frontend)

```
API Gateway:
  Client → API Gateway → Service A
                       → Service B
  (인증, 라우팅, 속도 제한을 Gateway에서 처리)

BFF (Backend For Frontend):
  Mobile App  → Mobile BFF  → Service A, B
  Web App     → Web BFF     → Service A, C
  (클라이언트별 최적화된 API를 각 BFF가 제공)
```

핵심 특성:
- 여러 서비스를 하나의 진입점으로 통합
- 클라이언트별 최적화된 API 제공 (BFF)
- 횡단 관심사(인증, 로깅, 속도 제한)를 중앙에서 처리

적합한 상황:
- Microservices 환경에서 클라이언트의 복잡도를 줄이고 싶을 때
- 여러 종류의 클라이언트(Web, Mobile, 3rd Party)를 지원할 때

> Monolith/Modular Monolith에서는 일반적으로 불필요

### 6.5 시스템 통합 패턴 비교 요약

| 기준 | 동기 호출 | Event-Driven | Saga | API Gateway/BFF |
|------|----------|-------------|------|----------------|
| 결합도 | 높음 | 낮음 | 중간 | 낮음 (클라이언트 관점) |
| 일관성 | 즉각 (ACID) | 최종 일관성 | 최종 일관성 | 해당없음 |
| 구현 복잡도 | ★ | ★★★ | ★★★★ | ★★★ |
| 적합한 배포 단위 | Monolith, Modular | 모두 | Microservices | Microservices |
| 디버깅 | ★★★★★ | ★★ | ★★ | ★★★ |

---

## 7. 카테고리 F: 실행 제어 패턴 — "비즈니스 실행 흐름을 무엇이 결정하는가"

> 이 카테고리는 **"비즈니스 로직의 실행 순서와 조건을 무엇이 결정하는가"**에 관한 것이다.
> 대부분의 프로젝트는 "코드 직접 작성"이지만, 반복 패턴이 많거나 복잡한 프로세스에서는 다른 패턴이 강력한 이점을 제공한다.

> **주의: Plugin Architecture, Actor Model, Strategy Pattern 등은 디자인 패턴이다.**
> 이들은 어떤 아키텍처 조합에서든 필요에 따라 적용할 수 있는 "구현 도구"이므로
> 아키텍처 축의 선택지에 포함하지 않는다. (1.2절 참조)

### 7.1 코드 직접 작성 (기본값)

```java
// 실행 흐름이 Java 코드에 명시적으로 작성됨
public void processPayroll() {
    validate();       // 1단계
    calculate();      // 2단계
    applyTax();       // 3단계
    save();           // 4단계
}
// 흐름 변경 = 코드 수정 + 컴파일 + 재배포
```

핵심 특성:
- 비즈니스 실행 흐름이 Java/Kotlin 코드로 직접 작성됨
- 가장 직관적이고 디버깅이 쉬움 (스택 트레이스 = 비즈니스 흐름)
- **대부분의 프로젝트에서 이것이 정답**이며, 다른 패턴은 특수한 이유가 있을 때만 선택

장점:
- IDE 지원 최고 (자동완성, 리팩토링, 타입 체크)
- 컴파일 타임에 오류 발견
- 모든 개발자가 즉시 이해 가능
- 디버깅 브레이크포인트 = 비즈니스 로직 위치

단점:
- 동일 패턴이 수십 개 반복되면 코드 중복이 누적됨
- 흐름 변경 시 코드 수정 + 재빌드 + 재배포 필요
- 비개발자가 실행 흐름을 이해하거나 수정하기 어려움

적합한 상황:
- 대부분의 프로젝트 (이것이 기본값이다)
- 기능마다 고유한 로직이 있는 경우
- 팀이 작고 빠른 개발이 필요한 경우

---

### 7.2 Metadata-Driven Architecture (메타 기반)

구조:
```
JSON/YAML 메타데이터 → 런타임 해석 엔진 → 실행 결과

메타데이터 예시:
{
  "aggregate": "employee",
  "action": "create",
  "steps": ["validate", "insert", "publish_event"],
  "tenantFilter": "facilityId"
}
→ 엔진이 이 JSON을 읽어서 validate → insert → event 순으로 실행
```

핵심 규칙:
- 실행 흐름을 코드가 아닌 데이터(메타데이터)로 정의
- 범용 엔진이 메타데이터를 읽어 런타임에 동작을 결정
- 새 기능 추가 = 메타데이터 추가 (코드 변경 최소화)

장점:
- 반복적인 패턴(CRUD, 조회, 상태 변경)을 코드 없이 처리
- 비개발자도 메타데이터를 수정하여 동작 변경 가능 (잠재적)
- 메타데이터가 자기 서술적(self-descriptive) → 시스템 문서화 효과
- 코드 중복이 극적으로 줄어듦

단점:
- 디버깅이 가장 어려움 — "어떤 메타가 어떤 경로로 실행되었나" 추적 필요
- 타입 안전성 부재 — JSON에 오타가 있으면 런타임까지 발견 불가
- 범용 엔진 자체의 복잡도가 높음 (누군가는 만들어야 함)
- 메타 구조 설계가 잘못되면 제약이 됨 (메타가 표현 못하는 로직이 생김)
- 팀원 모두가 메타 구조를 이해해야 함 → 학습 곡선

적합한 상황:
- 동일한 패턴의 기능이 수십~수백 개 반복되는 경우
- 실행 흐름의 런타임 변경이 필요한 경우
- 메타 엔진을 이미 보유하고 있는 경우 (v0.3의 ddd-framework-core)
- 비개발자가 비즈니스 규칙을 관리해야 하는 경우

대표 사례: Salesforce Platform, SAP ABAP Customizing, Low-Code 플랫폼, v0.3 Care 프로젝트

---

### 7.3 Workflow Engine Pattern

구조:
```
Workflow Definition (BPMN/JSON/DSL)
  └─ Step 1 → Step 2 → Step 3 (조건 분기, 병렬, 재시도)
       │          │          │
    Handler    Handler    Handler

특징: 상태 전이, 조건 분기, 타임아웃, 재시도, 보상이 엔진에 내장
```

대표 구현체:
- Camunda / Flowable (BPMN 기반)
- Temporal / Cadence (코드 기반 워크플로)
- AWS Step Functions (서버리스)
- Spring State Machine
- v0.3의 TreeBasedWorkflowExecutor (자체 구현)

장점:
- 복잡한 비즈니스 프로세스를 시각적으로 표현 가능
- 재시도, 타임아웃, 보상 처리가 엔진에 내장
- 장기 실행(long-running) 프로세스 지원

단점:
- 단순 CRUD에 워크플로 엔진은 과잉
- 엔진 자체의 학습 곡선과 운영 부담
- 엔진이 SPOF(Single Point of Failure)가 될 수 있음

적합한 상황:
- 다단계 승인, 상태 전이가 복잡한 비즈니스 프로세스
- 외부 시스템과의 비동기 연동이 많은 경우
- 보상 트랜잭션(Saga)이 필요한 분산 시스템

---

### 7.4 Rule Engine (규칙 엔진)

구조:
```
비즈니스 규칙 정의 (DSL/스크립트/테이블)
  │
  ▼
Rule Engine이 사실(Fact)에 규칙을 적용
  │
  ▼
실행 결과

예시:
  Rule: "근속 5년 이상이면 장기근속수당 = 기본급 × 5%"
  Fact: Employee(tenure=7, basePay=3000000)
  Result: 장기근속수당 = 150000
```

대표 구현체:
- Drools (Java 생태계 대표)
- Easy Rules (경량 Java 규칙 엔진)
- OpenL Tablets (엑셀 기반 규칙 정의)
- SpEL / MVEL (표현식 기반, 간이 규칙 엔진으로 활용)

핵심 특성:
- **비즈니스 규칙(조건 → 행동)을 코드 외부에서 정의**
- 엔진이 규칙을 사실(Fact)에 적용하여 결과를 도출
- 규칙의 추가/변경이 코드 변경 없이 가능 (잠재적)
- Metadata-Driven과 유사하지만, 규칙의 조건부 로직에 특화

장점:
- 조건 분기가 매우 많은 비즈니스 규칙을 깔끔하게 관리
- 비개발자(도메인 전문가)가 규칙을 직접 관리 가능 (이상적인 경우)
- 규칙 변경 시 재배포 불필요 (런타임 규칙 로딩 시)

단점:
- 엔진 도입의 학습 곡선
- 규칙 간 충돌/우선순위 관리가 복잡해질 수 있음
- 단순한 if-else로 충분한 경우 과잉 설계
- 디버깅: "어떤 규칙이 왜 발동했는가" 추적 필요

적합한 상황:
- 비즈니스 규칙이 자주 변경되고 수가 많은 경우 (보험 요율, 세율, 수당 계산)
- 도메인 전문가가 규칙을 직접 관리해야 하는 경우
- 조건 분기가 매우 복잡한 도메인 (보험, 세무, 의료)

대표 사례: 보험사 언더라이팅 시스템, 세무 계산 시스템, 의료 진단 보조

---

### 7.5 실행 제어 패턴 비교 요약

| 기준 | 코드 직접 작성 | Metadata-Driven | Workflow Engine | Rule Engine |
|------|-------------|----------------|----------------|------------|
| 흐름 정의 위치 | Java 코드 | JSON/YAML | BPMN/JSON/DSL | Rule DSL/스크립트 |
| 흐름 변경 방식 | 코드 수정+재배포 | 메타데이터 수정 | 워크플로 정의 수정 | 규칙 수정 |
| 디버깅 | ★★★★★ | ★★ | ★★★ | ★★★ |
| 타입 안전성 | ★★★★★ | ★★ | ★★★ | ★★★ |
| 반복 패턴 제거 | ★ | ★★★★★ | ★★★ | ★★★ |
| 복잡 조건 분기 처리 | ★★★ | ★★ | ★★★★ | ★★★★★ |
| 학습 곡선 | ★ (최저) | ★★★★ | ★★★ | ★★★ |
| 적합 영역 | 범용 (기본값) | 반복 패턴 다수 | 다단계 프로세스 | 조건 분기 다수 |

---

## 8. 아키텍처 전체 지도 — 카테고리 간 관계

### 8.1 6개 축의 독립성과 조합

```
┌────────────────────────────────────────────────────────────────────┐
│                      실제 프로젝트 아키텍처                          │
│                                                                    │
│   A. 배포 단위         ── 어떤 카테고리와도 독립적 선택 가능            │
│   B. 코드 구조         ── A와 독립 (Monolith든 Microservice든 적용)   │
│   C. 도메인 모델링      ── B와 독립 (Layered든 Hexagonal이든 적용)     │
│   D. 데이터 흐름        ── B, C와 독립적으로 추가                     │
│   E. 시스템 통합        ── A에 의존 (Microservices이면 E가 중요해짐)   │
│   F. 실행 제어          ── 모든 카테고리와 독립적으로 선택               │
│                                                                    │
│   단, A와 E는 강한 상관관계:                                         │
│   - A=Monolith → E=동기 호출(메서드) 이 기본                         │
│   - A=Microservices → E=Event-Driven/Saga가 거의 필수                │
│   - A=Modular Monolith → E=In-Process Event 또는 동기 호출           │
└────────────────────────────────────────────────────────────────────┘
```

### 8.2 전체 지도 다이어그램

```
A. 배포 ──→  Monolithic    Modular Monolith    Microservices    Serverless
               │                 │                  │               │
               ▼                 ▼                  ▼               ▼
B. 코드 ──→  ┌─────────────────────────────────────────────────────────┐
구조         │  Layered │ Hexagonal │ Clean │ Onion │ Vertical Slice  │
             └─────────────────────────────────────────────────────────┘
                                      │
                                      ▼
C. 도메인 ──→ Transaction Script │ Table Module │ Domain Model (DDD)
모델링                                │
                                      ▼
D. 데이터 ──→ 단일 모델 │ CQRS │ Event Sourcing │ Pipe & Filter
흐름                          │
                              ▼
E. 통합 ────→ 동기 호출 │ Event-Driven │ Saga │ API Gateway/BFF
                              │
                              ▼
F. 실행 ────→ 코드 직접 작성 │ Metadata-Driven │ Workflow Engine │ Rule Engine
제어
```

### 8.3 대표적 조합 예시

```
일반적인 Spring Boot 프로젝트 (모든 축이 기본값):
  A=Monolithic + B=Layered + C=Transaction Script + D=단일 모델 + E=동기 호출 + F=코드 직접 작성

DDD를 진지하게 하는 팀:
  A=Modular Monolith + B=Hexagonal + C=Domain Model + D=CQRS + E=Event-Driven + F=코드 직접 작성

대규모 분산 시스템:
  A=Microservices + B=Vertical Slice + C=Domain Model + D=Event Sourcing + E=Saga + F=Workflow Engine

보험/세무 시스템 (복잡한 규칙):
  A=Modular Monolith + B=Layered + C=Domain Model + D=CQRS + E=동기 호출 + F=Rule Engine

v0.3 Care 프로젝트:
  A=Monolithic + B=커스텀(Meta 구조) + C=Transaction Script(단순)/Domain Model(복잡) + D=CQRS + E=Event-Driven + F=Metadata-Driven
```

---

## 9. 아키텍처 조합 패턴 — 현업에서 실제 사용되는 방식

핵심 인사이트: **현업에서는 6개 축에서 각각 선택하여 조합한다. 단일 아키텍처는 없다.**

### 9.1 가장 일반적인 조합들

#### 조합 A: 모든 축 기본값 (가장 흔함 — 70% 이상)

```
A=Monolithic + B=Layered + C=Transaction Script + D=단일 모델 + E=동기 호출 + F=코드 직접 작성
```

```
Controller → Service(비즈니스 로직 절차적 작성) → Repository
```

특징:
- 가장 직관적이고 대부분의 Spring Boot 프로젝트가 이 조합
- 도메인 객체는 JPA Entity(데이터 컨테이너), 로직은 Service에
- 복잡도가 높아지면 Fat Service 문제 발생

사용하는 곳: 대부분의 중소규모 Spring Boot 프로젝트

#### 조합 B: Layered + 부분적 DDD (실용적 DDD)

```
A=Monolithic + B=Layered + C=Transaction Script(단순) / Domain Model(복잡) + D=단일 모델 or CQRS + E=동기 호출 + F=코드 직접 작성
```

```
Controller → ApplicationService → Domain Model → Repository
                                      │
                                  (DDD 전술 패턴을
                                   복잡한 도메인에만 부분적으로 적용)
```

특징:
- 기본 구조는 Layered이지만, 복잡한 도메인에만 Aggregate/Value Object 적용
- 단순 CRUD는 Transaction Script, 복잡 로직은 Domain Model
- "실용적 DDD" — 전략적 패턴(Bounded Context)은 채택하되, 전술적 패턴은 선택적

사용하는 곳: 쿠팡, 배달의민족, 카카오 대부분의 서비스

#### 조합 C: Modular Monolith + Hexagonal + DDD (DDD를 진지하게 하는 팀)

```
A=Modular Monolith + B=Hexagonal + C=Domain Model + D=CQRS + E=Event-Driven(In-Process) + F=코드 직접 작성
```

```
[Employee Module]                           [Payroll Module]
Adapter → Port → UseCase → Domain → Port    Adapter → Port → UseCase → Domain → Port
                              │                                         ▲
                              └──── Domain Event ──── Event Bus ────────┘
```

특징:
- Modular Monolith가 배포 단위를 잡고
- Hexagonal이 모듈 내부 구조를 잡고
- DDD 전술적 패턴이 도메인 계층을 채우고
- Event-Driven으로 모듈 간 느슨한 결합
- 가장 "교과서적"인 조합

사용하는 곳: 독일/유럽 보험사, 일부 핀테크 스타트업

#### 조합 D: DDD + CQRS + Event Sourcing (풀 세트)

```
A=Microservices + B=Hexagonal + C=Domain Model + D=CQRS + Event Sourcing + E=Saga + F=코드 직접 작성
```

```
Command: Aggregate → Domain Event → Event Store
Query:   Event → Projection → Read Model
통합:    Event → Event Bus → 다른 Bounded Context
```

특징:
- 모든 패턴을 결합한 "풀 스펙"
- 가장 강력하지만 가장 복잡
- 팀 전원이 높은 수준의 이해를 필요로 함

사용하는 곳: 금융 트레이딩, 대규모 이벤트 기반 시스템

#### 조합 E: Metadata-Driven + Workflow + CQRS (v0.3)

```
A=Monolithic + B=커스텀(Meta) + C=Transaction Script(단순)/Domain Model(복잡) + D=CQRS + E=Event-Driven + F=Metadata-Driven
```

```
Command: JSON WorkflowMeta → Workflow Engine → Plugin Handler
Query:   JSON QuerySchema → DynamicQueryExecutor → SQL
```

특징:
- 메타데이터가 실행 흐름과 조회 스키마를 모두 정의
- 워크플로 엔진이 오케스트레이션 담당
- 플러그인 핸들러가 도메인 로직 담당
- 반복적 패턴의 코드 제거가 핵심 가치

사용하는 곳: SaaS 플랫폼, Low-Code/No-Code, ERP 커스터마이징, Care v0.3

### 9.2 조합별 비교

| 조합 | 초기 비용 | 유지보수 비용 | 확장성 | 팀 요구 수준 | 적합 규모 |
|------|----------|-------------|--------|------------|----------|
| A: Layered + Transaction Script | ★ | ★★★★ (규모↑ 시) | ★★ | 낮음 | 소 |
| B: Layered + 부분 DDD | ★★ | ★★★ | ★★★ | 중간 | 소~대 |
| C: Modular Monolith + Hex + DDD | ★★★★ | ★★ | ★★★★ | 높음 | 중~대 |
| D: DDD + CQRS + ES | ★★★★★ | ★★★★ | ★★★★★ | 매우 높음 | 대 |
| E: Meta + Workflow + CQRS | ★★★★ | ★★ (패턴 반복 시) | ★★★★ | 높음 (엔진 이해) | 중~대 |

---

## 10. 왜 대부분의 현업에서 v0.3 같은 아키텍처를 사용하지 않는가

### 10.1 핵심 이유 5가지

#### 이유 1: 범용 엔진이 없다

v0.3은 `ddd-framework-core`라는 이미 구현된 워크플로 엔진이 있기 때문에 가능하다.
대부분의 프로젝트는 이런 엔진을 갖고 있지 않으며, 엔진을 처음부터 만드는 비용은 매우 높다.

```
v0.3의 전제조건:
  TreeBasedWorkflowExecutor      ← 이미 존재
  WorkflowStepProcessorManager   ← 이미 존재
  AggregateActionProcessor       ← 이미 존재
  SpEL 조건 평가                  ← 이미 존재
  Hook / AfterAction             ← 이미 존재
```

일반 팀이 같은 구조를 만들려면 엔진 구현에 3~6개월이 필요하다. v0.3은 이 비용이 0이기 때문에 성립하는 설계다.

#### 이유 2: 메타 구조 설계 역량이 필요하다

메타 기반 아키텍처의 성패는 "메타 구조가 실제 도메인을 충분히 표현할 수 있느냐"에 달려 있다.
잘못 설계하면 "메타로 표현 못하는 예외 케이스"가 누적되어, 결국 메타를 우회하는 하드코딩이 늘어난다.

```
메타 기반 아키텍처의 생사가 갈리는 순간:

  "이 비즈니스 규칙은 메타로 표현할 수 없으니 코드로 하드코딩하자"
     → 이런 경우가 10%를 넘으면 메타 기반 아키텍처의 가치가 사라짐

  v0.3은 이 문제를 "actionId로 전용 핸들러 플러그인"으로 해결
     → 메타로 표현 못하는 복잡 로직 = 전용 핸들러로 위임
     → 핵심 설계 결정이 잘 되어 있음
```

#### 이유 3: 디버깅 난이도

```
Layered 아키텍처의 디버깅:
  EmployeeController.create()  ← 브레이크포인트
    → EmployeeService.register()  ← 브레이크포인트
      → EmployeeRepository.save()  ← 브레이크포인트
  스택 트레이스가 비즈니스 흐름과 1:1 대응

v0.3의 디버깅:
  DynamicRestHandler.handle()
    → CareWorkflowEntryPoint.execute()
      → TreeBasedWorkflowExecutor.executeRequest()
        → WorkflowStepProcessorManager.executeStep()
          → AggregateActionProcessor.process()
            → AggregateActionHandlerRegistry.getHandler()
              → EmployeeRegisterHandler.execute()  ← 실제 로직은 여기
  "어떤 JSON의 어떤 step이 어떤 핸들러를 호출했는지" 추적이 필요
```

#### 이유 4: 업계 표준이 아님

대부분의 개발자 교육, 부트캠프, 기술 블로그는 Layered 또는 DDD를 다룬다.
메타 기반 워크플로 아키텍처에 대한 공개 자료, 교육 과정, 커뮤니티가 거의 없다.

```
채용 시:
  "Spring Boot + Layered Architecture 경험자" → 지원자 풍부
  "DDD + Hexagonal 경험자" → 지원자 적당
  "메타 기반 워크플로 엔진 경험자" → 지원자 거의 없음
```

#### 이유 5: "충분히 좋은" 대안이 존재

86개 테이블 규모의 프로젝트도 Layered + Spring Data JPA + 코드 생성기로 충분히 빠르게 개발할 수 있다.

```
대안적 접근:
  JHipster / Spring Initializr → 보일러플레이트 자동 생성
  Spring Data JPA → Repository 자동 생성
  MapStruct → DTO 변환 자동 생성
  QueryDSL → 동적 조회 자동 생성

  → 코드량은 v0.3보다 많지만, 모든 팀원이 즉시 이해하고 기여할 수 있음
```

### 10.2 그럼에도 v0.3이 성립하는 이유

| 이유 | 설명 |
|------|------|
| 엔진이 이미 존재 | `ddd-framework-core` 재사용 — 엔진 구현 비용 0 |
| 패턴 반복도가 극히 높음 | 86개 테이블 중 60~70%가 동일한 CRUD 패턴 |
| 멀티테넌시 강제가 필수 | `facilityId` 누락이 보안 사고 — 엔진 레벨 강제가 유리 |
| 프론트엔드와 철학 일치 | 프론트엔드도 메타 기반 UI — 팀 전체의 인지 모델 통일 |
| 팀 구성 | 엔진 이해자(설계자)가 팀에 존재 |

---

## 11. 아키텍처 의사결정 프레임워크 — 정확한 기준

### 11.1 1차 기준: 프로젝트 특성 (가장 중요)

```
질문 1: 배포 단위를 어떻게 할 것인가? (카테고리 A)
  ├─ 팀 1~10명, 단일 서비스 → Monolithic 또는 Modular Monolith
  ├─ 팀 10명+, 독립 배포 필요 → Microservices
  └─ 이벤트 처리/사이드 프로젝트 → Serverless

질문 2: 코드를 어떻게 구조화할 것인가? (카테고리 B)
  ├─ 도메인 복잡도 낮음 → Layered
  ├─ 테스트 격리 중요 → Hexagonal
  ├─ 기능별 응집 중요 → Vertical Slice
  └─ 프레임워크 독립 중요 → Clean / Onion

질문 3: 비즈니스 로직을 어떻게 표현할 것인가? (카테고리 C)
  ├─ 단순 CRUD → Transaction Script
  ├─ 도메인 복잡도 높음 → Domain Model (DDD)
  └─ 혼합 → 영역별 다른 패턴 적용 (단순 CRUD = Script, 복잡 = DDD)

질문 4: 읽기와 쓰기를 분리할 것인가? (카테고리 D)
  ├─ 읽기/쓰기 복잡도 비슷 → 단일 모델
  ├─ 복잡한 조회 vs 단순 쓰기 → CQRS
  ├─ 모든 변경 이력 보존 필수 → Event Sourcing
  └─ 단계별 데이터 처리 → Pipe & Filter

질문 5: 모듈/시스템 간 어떻게 소통할 것인가? (카테고리 E)
  ├─ Monolith + 단순 → 동기 호출
  ├─ 모듈 간 느슨한 결합 원함 → Event-Driven
  └─ Microservices + 분산 트랜잭션 → Saga

질문 6: 비즈니스 실행 흐름을 무엇이 결정할 것인가? (카테고리 F)
  ├─ 기능마다 고유 로직 → 코드 직접 작성 (기본값)
  ├─ 동일 패턴 반복 (수십 개 CRUD) → Metadata-Driven
  ├─ 다단계 프로세스 (승인, 상태 전이) → Workflow Engine
  └─ 조건 분기가 매우 복잡 (보험, 세무) → Rule Engine
```

### 11.2 2차 기준: 팀 특성

```
질문 7: 팀 규모는?
  ├─ 1~3명  → 단순할수록 좋다 (Layered, Transaction Script)
  ├─ 4~10명 → 모듈 경계가 필요 (Hexagonal, Bounded Context)
  └─ 10명+  → 명확한 계약과 경계 필수 (DDD, CQRS, Modular Monolith)

질문 8: 팀의 기술 수준은?
  ├─ 주니어 다수     → Layered (학습 곡선 최소)
  ├─ 시니어 혼합     → Hexagonal + 부분 DDD
  └─ 시니어 다수     → Clean, DDD, Event Sourcing 가능

질문 9: 채용 시장에서 어떤 경험자를 구할 수 있는가?
  ├─ Spring Boot 경험자 → Layered 또는 Hexagonal
  └─ 특수 프레임워크 경험자 필요 → 그 프레임워크 기반 아키텍처의 유지보수 비용 상승

질문 10: 아키텍처를 설계하고 유지할 수 있는 사람이 있는가?
  ├─ 아니오 → 업계 표준 아키텍처 사용 (참고 자료 풍부)
  └─ 예    → 프로젝트에 최적화된 커스텀 아키텍처 가능
```

### 11.3 3차 기준: 운영 환경

```
질문 11: 프로젝트 수명은?
  ├─ 1년 이하 (MVP, PoC)      → 가장 단순한 구조 (Layered + Script)
  ├─ 1~5년                    → 중간 복잡도 허용
  └─ 5년 이상                  → 유지보수성에 투자 가치 있음

질문 12: 성능 요구사항의 비대칭성은?
  ├─ 읽기:쓰기 비율이 비슷  → 단일 모델
  └─ 읽기가 압도적         → CQRS
```

### 11.4 의사결정 플로우차트

```
시작
 │
 ├─ 도메인 복잡도가 낮고 팀이 작다
 │    → A=Monolithic + B=Layered + C=Transaction Script
 │    → 끝
 │
 ├─ 도메인 복잡도가 높고 비즈니스 규칙이 핵심이다
 │    ├─ 테스트 용이성 + 기능 응집이 중요하다
 │    │    → A=Modular Monolith + B=Hexagonal + C=Domain Model
 │    ├─ 기능별 독립 변경이 중요하다
 │    │    → A=Modular Monolith + B=Vertical Slice + C=Domain Model
 │    └─ 프레임워크 독립성이 중요하다
 │         → A=Modular Monolith + B=Clean + C=Domain Model
 │
 ├─ 읽기/쓰기 복잡도가 매우 다르다
 │    → D=CQRS 추가
 │    ├─ 변경 이력의 완전한 보존이 필수다
 │    │    → D=Event Sourcing 추가
 │    └─ 감사 로그로 충분하다
 │         → Transactional Outbox로 충분
 │
 ├─ 동일 패턴의 기능이 수십 개 반복된다
 │    ├─ 메타 엔진을 이미 갖고 있다
 │    │    → F=Metadata-Driven
 │    └─ 엔진이 없다
 │         ├─ 엔진 구현에 투자할 여력이 있다
 │         │    → F=Metadata-Driven 또는 Low-Code 플랫폼 도입
 │         └─ 여력이 없다
 │              → 코드 생성기 + F=코드 직접 작성
 │
 ├─ 다단계 프로세스/분산 트랜잭션이 핵심이다
 │    → F=Workflow Engine + E=Saga Pattern
 │
 └─ 조건 분기가 매우 많고 자주 변경된다 (보험 요율, 세율 등)
      → F=Rule Engine
```

---

## 12. 종합 트레이드오프 매트릭스

### 12.1 카테고리별 핵심 비교

#### 카테고리 B: 코드 구조

| 평가 기준 | Layered | Hexagonal | Clean | Onion | Vertical Slice |
|-----------|---------|-----------|-------|-------|---------------|
| 초기 구현 비용 | ★ | ★★★ | ★★★★ | ★★★★ | ★★ |
| 학습 곡선 | ★ | ★★★ | ★★★★ | ★★★★ | ★★ |
| 디버깅 용이성 | ★★★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★★ |
| 테스트 격리 | ★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| 기능 수정 시 응집도 | ★★ | ★★★ | ★★★ | ★★★ | ★★★★★ |
| 도메인 보호 | ★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★ |
| 보일러플레이트 | ★ (최소) | ★★★ | ★★★★ | ★★★★ | ★★ |
| 채용 용이성 | ★★★★★ | ★★★ | ★★ | ★★ | ★★★ |

> ★이 많을수록 해당 기준에서 더 나은 것을 의미.
> 단, "초기 구현 비용"과 "학습 곡선"은 ★이 적을수록 좋음 (비용이 낮음).

#### 카테고리 C: 도메인 모델링

| 평가 기준 | Transaction Script | Table Module | Domain Model (DDD) |
|-----------|-------------------|-------------|-------------------|
| 단순 CRUD 속도 | ★★★★★ | ★★★★ | ★★ |
| 복잡 로직 표현 | ★★ | ★★★ | ★★★★★ |
| 타입 안전성 | ★★★ | ★★★ | ★★★★★ |
| 불변식 보호 | ★ | ★★ | ★★★★★ |
| 학습 곡선 | ★ (최저) | ★★ | ★★★★★ |

### 12.2 주요 조합 비교

| 평가 기준 | A: Layered+Script | B: Layered+부분DDD | C: ModMono+Hex+DDD | D: DDD+CQRS+ES | E: v0.3 (Meta+WF+CQRS) |
|-----------|------------------|---------------------|--------------------|--------------|-----------------------------|
| 단순 CRUD 속도 | ★★★★ | ★★★ | ★★ | ★★ | ★★★★★ |
| 복잡 로직 표현 | ★★ | ★★★ | ★★★★★ | ★★★★★ | ★★★ |
| 디버깅 | ★★★★★ | ★★★★★ | ★★★★ | ★★★ | ★★ |
| 타입 안전성 | ★★★ | ★★★★ | ★★★★★ | ★★★★★ | ★★ |
| 테스트 용이성 | ★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★ |
| 기능 수정 시 응집도 | ★★ | ★★★ | ★★★★ | ★★★★ | ★★★★★ |
| 멀티테넌시 | ★★ | ★★ | ★★★ | ★★★ | ★★★★★ |
| 팀 온보딩 | ★★★★★ | ★★★★★ | ★★★ | ★★ | ★★ |
| 코드 중복 | ★★ | ★★ | ★★★ | ★★★ | ★★★★★ |
| 총 구현 비용 | ★★★★★ | ★★★★ | ★★★ | ★ | ★★★ (엔진有) / ★ (엔진無) |

---

## 13. v0.3 아키텍처의 객관적 위치 평가

### 13.1 6개 카테고리로 분석한 v0.3의 선택

| 카테고리 | v0.3의 선택 | 선택 이유 |
|---------|-----------|----------|
| A. 배포 단위 | Monolithic | 1~2명 팀, 단일 배포의 단순함 |
| B. 코드 구조 | 커스텀 (Meta 기반 구조) | 전통적 코드 구조 대신 메타 + 핸들러 구조 |
| C. 도메인 모델링 | Transaction Script(단순) / 핸들러 내 도메인 로직(복잡) | 86개 테이블 중 60~70%가 단순 CRUD |
| D. 데이터 흐름 | CQRS (동일 DB, 경로 분리) | 복잡한 조회와 단순 명령의 분리 |
| E. 시스템 통합 | Event-Driven (Transactional Outbox) | 도메인 이벤트 기반 모듈 간 소통 |
| F. 실행 제어 | Metadata-Driven | 반복 CRUD 제거 (복잡 로직은 디자인 패턴인 Plugin으로 위임) |

### 13.2 v0.3이 취하지 않은 것 (의도적 선택)

| 취하지 않은 것 | 이유 |
|--------------|------|
| DDD 전술적 패턴 (Aggregate Root, Value Object) | 86개 테이블에 각각 Aggregate를 만들면 보일러플레이트 폭증. 대신 AggregateMeta JSON으로 대체 |
| Clean Architecture의 Entities 계층 | 프레임워크 독립적 도메인 모델의 실질적 필요성 대비 비용이 너무 높음 |
| Event Sourcing | 감사 로그 + EventOutbox로 필요한 수준의 이력 추적이 충분. 이벤트 재생은 요구사항이 아님 |
| Hexagonal의 명시적 Port/Adapter | `AggregateActionHandler` 인터페이스가 사실상 Port 역할. 형식적인 Port 계층을 추가하는 것은 과잉 |
| Modular Monolith | 메타 기반 구조에서는 모듈 경계가 메타데이터 수준에서 자연스럽게 형성 |

### 13.3 v0.3이 취한 것 (핵심 가치)

| 취한 것 | 이유 |
|--------|------|
| Metadata-Driven | 86개 테이블, 60~70% 동일 패턴 → 코드 없는 CRUD가 핵심 생산성 |
| Workflow Engine 재사용 | ddd-framework-core가 이미 존재 → 구현 비용 0 |
| CQRS | 복잡한 조회(다중 조인, 집계, 필터)와 단순 명령의 분리가 자연스러움 |
| Plugin Architecture | 단순 CRUD(generic) ~ 복잡 계산(전용 핸들러) 연속체를 하나의 메커니즘으로 수용 |
| 엔진 레벨 멀티테넌시 | facilityId 누락 = 보안 사고. 핸들러 개발자에게 맡기면 안 되는 영역 |

### 13.4 DDD/Hexagonal/Clean이었다면 어떻게 다를까

같은 프로젝트를 다른 아키텍처로 구현했을 때의 구체적 차이:

#### 시나리오: 새 테이블 `benefit_payment`(본인부담금) 단순 CRUD 추가

v0.3 (현재):
```
작성해야 할 것:
  1. metadata/aggregates/benefit_payment.json       (AggregateMeta)
  2. metadata/workflows/benefit_payment.create.json (WorkflowMeta)
  3. metadata/queries/benefit_payment.list.json     (QueryEntityMeta)
Java 코드: 0줄 (generic_insert 사용)
```

Layered:
```
작성해야 할 것:
  1. BenefitPaymentController.java      (~50줄)
  2. BenefitPaymentService.java         (~80줄)
  3. BenefitPaymentRepository.java      (~20줄)
  4. BenefitPayment.java (Entity)       (~60줄)
  5. BenefitPaymentDTO.java             (~40줄)
  6. BenefitPaymentMapper.java          (~20줄)
Java 코드: ~270줄
```

Hexagonal + DDD:
```
작성해야 할 것:
  1. CreateBenefitPaymentUseCase.java   (Port Interface ~10줄)
  2. BenefitPaymentService.java         (UseCase 구현 ~80줄)
  3. BenefitPayment.java (Aggregate)    (~100줄, 불변식 포함)
  4. BenefitPaymentId.java (Value Object) (~20줄)
  5. Money.java (Value Object)          (~30줄, 이미 있으면 재사용)
  6. BenefitPaymentRepository.java      (Port Interface ~10줄)
  7. BenefitPaymentJpaRepository.java   (Adapter ~30줄)
  8. BenefitPaymentJpaEntity.java       (Adapter ~50줄)
  9. BenefitPaymentMapper.java          (~30줄)
  10. BenefitPaymentController.java     (Adapter ~40줄)
  11. BenefitPaymentResponse.java       (Adapter ~30줄)
Java 코드: ~430줄
```

이것이 86개 테이블에서 반복된다:

| 아키텍처 | 단순 CRUD 1개당 코드 | 86개 테이블 (60% 단순 CRUD) | 유지보수 대상 |
|---------|---------------------|---------------------------|-------------|
| v0.3 | JSON 3개 (0줄 Java) | JSON ~150개 | JSON 파일 |
| Layered | ~270줄 | ~14,000줄 | Java 코드 |
| Hexagonal + DDD | ~430줄 | ~22,000줄 | Java 코드 |

> 이 숫자가 v0.3의 존재 이유다. 단, 복잡한 도메인 로직(급여계산)에서는 DDD의 도메인 모델이 더 표현력이 높다.

---

## 14. 결론 — "무조건 좋은 아키텍처는 없다"의 구체적 의미

### 14.1 아키텍처 선택은 6개 축의 최적화 문제다

모든 아키텍처는 무언가를 최적화하면 다른 무언가를 희생한다.

| 카테고리 | 선택지 | 최적화하는 것 | 희생하는 것 |
|---------|-------|-------------|-----------|
| A | Monolithic | 배포 단순성, 트랜잭션 | 독립 스케일링, 팀 독립성 |
| A | Modular Monolith | 경계 분리 + 단순 배포 | 독립 스케일링 |
| A | Microservices | 팀 독립성, 독립 스케일링 | 운영 복잡도, 데이터 일관성 |
| B | Layered | 학습 용이성, 개발 속도 | 도메인 보호, 테스트 격리 |
| B | Hexagonal | 테스트 격리, 교체 가능성 | 초기 비용, 보일러플레이트 |
| B | Vertical Slice | 기능 응집, 수정 범위 최소화 | 공통 코드 재사용 구조화 |
| C | Transaction Script | 직관성, CRUD 속도 | 복잡 로직 표현, 불변식 보호 |
| C | Domain Model | 도메인 표현력, 불변식 | 학습 곡선, CRUD 생산성 |
| D | CQRS | 읽기/쓰기 독립 최적화 | 데이터 동기화 복잡도 |
| D | Event Sourcing | 완전한 이력 추적 | 구현 복잡도, 조회 성능 |
| F | Metadata-Driven | 반복 패턴 제거, 유연성 | 타입 안전성, 디버깅 |
| F | Workflow Engine | 프로세스 오케스트레이션 | 단순 케이스의 과잉 설계 |
| F | Rule Engine | 복잡 조건 분기 관리 | 엔진 학습 곡선, 규칙 충돌 관리 |

### 14.2 의사결정의 진짜 기준: "가장 비싼 실수를 피하라"

```
질문: "어떤 아키텍처가 좋은가?"
답: "이 프로젝트에서 가장 비싼 실수가 무엇인가?"

├─ 가장 비싼 실수 = "개발이 늦어지는 것"
│    → 가장 단순한 조합 (Monolith + Layered + Transaction Script)
│
├─ 가장 비싼 실수 = "비즈니스 규칙 버그"
│    → 도메인 표현력 (DDD Domain Model + Hexagonal)
│
├─ 가장 비싼 실수 = "기능 수정 시 여러 곳을 고쳐야 해서 버그 유발"
│    → 기능 응집 (Vertical Slice + Modular Monolith)
│
├─ 가장 비싼 실수 = "보일러플레이트 유지보수"
│    → 반복 제거 (Metadata-Driven)
│
├─ 가장 비싼 실수 = "테넌트 간 데이터 유출"
│    → 격리를 엔진 레벨에서 강제 (v0.3)
│
├─ 가장 비싼 실수 = "테스트가 어려워서 변경이 두려움"
│    → 테스트 격리 (Hexagonal + Domain Model)
│
└─ 가장 비싼 실수 = "변경 이력 소실"
     → 이벤트 소싱 (Event Sourcing)
```

### 14.3 v0.3 Care 프로젝트의 의사결정 근거

```
이 프로젝트에서 가장 비싼 실수:
  1. 86개 테이블에 각각 Controller/Service/Repository를 만드는 보일러플레이트 → Metadata-Driven
  2. facilityId 누락으로 인한 테넌트 간 데이터 유출 → 엔진 레벨 강제
  3. 단순 CRUD와 복잡 계산기를 별도 메커니즘으로 관리하는 이중 구조 → actionId 플러그인

이 프로젝트에서 감수할 수 있는 비용:
  1. 디버깅 난이도 증가 → 상세한 문서(8개)로 완화
  2. 타입 안전성 부족 → JSON Schema + 통합 테스트로 보완
  3. 학습 곡선 → 아키텍처 설계자가 팀에 존재
```

### 14.4 최종 권장사항

아키텍처 선택 체크리스트:

- [ ] 6개 카테고리(배포/코드구조/도메인모델링/데이터흐름/통합/실행제어)에서 각각 선택했는가?
- [ ] "이 프로젝트에서 가장 비싼 실수"를 정의했는가?
- [ ] 팀의 기술 수준과 경험을 솔직하게 평가했는가?
- [ ] 프로젝트 수명과 유지보수 기간을 고려했는가?
- [ ] 도메인 복잡도를 과대/과소 평가하지 않았는가?
- [ ] "이 아키텍처의 단점을 감수할 수 있는가?"를 확인했는가?
- [ ] 선택한 아키텍처를 유지할 수 있는 사람이 팀에 있는가?
- [ ] 채용 시장에서 이 아키텍처 경험자를 구할 수 있는가?
- [ ] 가장 단순한 대안으로는 정말 안 되는가? (이것이 가장 중요한 질문)

> "아키텍처는 제약(constraint)이다. 좋은 아키텍처는 올바른 제약을 거는 것이고, 나쁜 아키텍처는 잘못된 제약을 거는 것이다."
> — 아키텍처의 본질은 "무엇을 할 수 있게 하느냐"가 아니라 "무엇을 못 하게 막느냐"에 있다.
