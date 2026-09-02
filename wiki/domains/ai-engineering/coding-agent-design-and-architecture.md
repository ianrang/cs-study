---
title: 코딩 에이전트 설계 개념과 구현 구조
page_type: concept
tags:
- agent
- architecture
- tool-use
date_created: '2026-09-02'
date_updated: '2026-09-02'
source_paths:
- raw/sources/video/tBRz9JonUUw/9ccab2007ecc554464250fb3b78f40f5daf5e68d6cf1dc423945cfef59be8577/manifest.json
- raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json
summary: 뉴런데브의 연속 방송 두 편을 중복 없이 통합해 에이전트의 제어 경계, 세션·턴·도구 런타임, 서브에이전트·목표·대기열, 훅·가드레일·모듈
  경계를 정리한다.
---

## Definition

이 문서는 중단된 첫 방송과 그 내용을 복기하며 이어진 두 번째 방송을 하나의 강의 흐름으로 재구성한다. 첫 영상의 마지막 비결정성 설명과 둘째 영상 초반의 복기는 한 번만 서술한다. [영상 A 00:22:16](https://www.youtube.com/watch?v=tBRz9JonUUw&t=1336s), [영상 B 00:02:11](https://www.youtube.com/watch?v=fsou1Butd6U&t=131s)

이 강의에서 코딩 에이전트의 핵심은 파일·터미널 도구의 유무가 아니라 **모델이 런타임에 다음 행동·반복·종료의 일부를 결정하는가**에 있다. 코드가 경로를 사전 고정하면 워크플로우이고, 모델이 제한된 경계 안에서 다음 행동을 선택하면 에이전트다. 실제 시스템은 상위 구조를 코드가 제한하고 그 안의 행동을 모델이 결정하는 혼합형일 수 있다. [영상 A 00:16:45](https://www.youtube.com/watch?v=tBRz9JonUUw&t=1005s)

## Mechanism

### 실행 단위와 컨텍스트

| 단위 | 역할 | 경계 |
|---|---|---|
| request | 동작을 촉발하는 입력 | 사용자·모델·스케줄러가 생성 가능 |
| iteration | 한 턴 안의 모델 호출 단위 | 응답과 도구 요청·결과에 따라 반복 |
| turn | 요청 하나를 처리하는 실행 구간 | 요청으로 시작해 최종 응답으로 종료 |
| session | 연속된 턴과 누적 컨텍스트의 그릇 | 여러 턴을 순차 축적 |

현대 모델의 한 응답은 추론, 사용자 메시지, 여러 도구 호출을 스트리밍할 수 있다. 런타임은 도구의 직렬·병렬 관계, 권한 승인·거부, 실패 결과 전달을 조정한다. [영상 B 00:14:05](https://www.youtube.com/watch?v=fsou1Butd6U&t=845s)

### 서브에이전트, 목표, 대기열

서브에이전트는 모델이 도구로 연 별도 세션으로 설명된다. 컨텍스트를 상속하면 기존 결정 배경을 유지하고, 비우면 독립 리뷰·국소 문제 해결에 유리하다. 세션 간 통신은 요청과 최종 응답을 대기열로 전달하는 메시징 문제로 다룰 수 있다. [영상 B 00:32:13](https://www.youtube.com/watch?v=fsou1Butd6U&t=1933s), [영상 B 00:46:17](https://www.youtube.com/watch?v=fsou1Butd6U&t=2777s)

목표(goal)는 턴 종료 시 달성 여부를 평가하고, 미달성이면 새 요청으로 다음 턴을 시작하는 장치다. 비동기 도구, 서브세션 응답, 후속 요청을 별도 대기열로 두기보다 메시지 타입으로 구분하는 통합 대기열이 런타임 표면을 줄인다는 설계가 제시된다. [영상 B 00:49:08](https://www.youtube.com/watch?v=fsou1Butd6U&t=2948s), [영상 B 00:56:37](https://www.youtube.com/watch?v=fsou1Butd6U&t=3397s)

### 도구 런타임과 훅

도구는 단순 기능 목록이 아니라 모델의 제어면이다. [영상 B 00:52:32](https://www.youtube.com/watch?v=fsou1Butd6U&t=3152s) 실행기는 인메모리 호출과 외부 프로세스를 캡슐화하고, 외부 프로세스에서는 진행·취소·오류·최종 결과 프로토콜을 조정해야 한다. 도구 결과는 문자열 반환을 넘어 진행 스트리밍, 컨텍스트 메시지 추가, 별도 세션, 리마인더 삽입 같은 부수 효과를 가질 수 있다. [영상 B 01:13:51](https://www.youtube.com/watch?v=fsou1Butd6U&t=4431s), [영상 B 01:24:43](https://www.youtube.com/watch?v=fsou1Butd6U&t=5083s)

턴 루프 사이에 이벤트와 훅을 두면 요청 재작성, 컨텍스트 검사, 반복 감지, 도구 권한·인자 검사, 출력 가드레일과 같은 정책을 핵심 오케스트레이션에서 분리할 수 있다. [영상 B 01:46:55](https://www.youtube.com/watch?v=fsou1Butd6U&t=6415s)

## Variants

### 제어 구조

| 구분 | 워크플로우 | 에이전트 |
|---|---|---|
| 제어 주체 | 개발자 코드 | 모델 |
| 경로 | 사전 정의 그래프 | 런타임 다음 행동 결정 |
| 강점 | 예측 가능성·비용 통제 | 새로운 문제에 대한 유연성 |
| 위험 | 정의된 경로 밖 문제에 취약 | 비결정성·토큰·통제 비용 |

### 도구 설계

| 접근 | 장점 | 비용·조건 |
|---|---|---|
| 전용 도구 다수 | 인자와 행동 범위가 명확 | 도구 선택 경합·설명 관리·확장 비용 |
| 셸 같은 범용 도구 | 런타임 표면을 줄이고 다양한 작업 수용 | 자연어를 안전한 명령으로 번역할 모델 능력과 샌드박스 필요 |

도구와 스킬이 동일한 선택 후보로 경합하지 않도록 실행 능력은 범용 도구에, 상황별 절차·예제·참고 자료는 스킬에 두는 조합이 소개된다. [영상 B 01:00:41](https://www.youtube.com/watch?v=fsou1Butd6U&t=3641s), [영상 B 01:08:45](https://www.youtube.com/watch?v=fsou1Butd6U&t=4125s)

### 실행·대기 방식

| 선택 | 특성 |
|---|---|
| 인메모리 실행 | 호출 비용이 낮지만 블로킹·실패가 본체에 전파될 수 있음 |
| 외부 프로세스 | 실패·블로킹 격리가 쉬우나 직렬화·통신 프로토콜 필요 |
| 지속 대기 | 새 이벤트에 빠르게 반응하지만 세션 점유 |
| 스케줄러 재개 | 대기 중 다른 작업이 가능하지만 재개 상태 관리 필요 |

[영상 B 01:13:51](https://www.youtube.com/watch?v=fsou1Butd6U&t=4431s), [영상 B 01:22:50](https://www.youtube.com/watch?v=fsou1Butd6U&t=4970s)

## Trade-offs

### 비결정성과 변경 영향

샘플링·디코딩과 다양한 학습 궤적은 같은 입력에서도 다른 해결법을 만든다. 강의는 이를 유연성의 원천이자 예측·리뷰 난도의 원인으로 설명한다. [영상 A 00:01:48](https://www.youtube.com/watch?v=tBRz9JonUUw&t=108s), [영상 A 00:22:16](https://www.youtube.com/watch?v=tBRz9JonUUw&t=1336s) 제품 코드에서는 변화 이유가 다른 기능을 모듈·디렉터리 경계로 격리해 재생성 실패와 수정 영향을 국소화하라고 제안한다. [영상 B 00:39:51](https://www.youtube.com/watch?v=fsou1Butd6U&t=2391s) 이를 구현 관점에서 정규화하면 경계의 목적은 파일 수 증가가 아니라 변경 이유·도메인·외부 의존성·오케스트레이션 책임의 분리다. 이 분류는 강의 내용을 편집자가 설계 원칙으로 정리한 것이다.

### 컨텍스트와 운용 휴리스틱

턴이 축적될수록 컨텍스트는 커지고, 변경된 요구와 비슷하지만 모순된 지시가 함께 남으면 성능이 희석될 수 있다. 강의자는 컨텍스트 사용량을 시계로 표현하며 민감한 작업의 마지막 큰 요청을 약 4시, 불가피한 상한을 7시 부근으로 두는 개인 경험칙을 제시한다. 이는 공식 임계값이 아니며 작업 분리와 컴팩션 전후 재작업 비용을 관찰하라는 운용 휴리스틱이다. [영상 B 00:20:36](https://www.youtube.com/watch?v=fsou1Butd6U&t=1236s), [영상 B 00:25:21](https://www.youtube.com/watch?v=fsou1Butd6U&t=1521s)

### 로컬 모델과 안전성

로컬·온프레미스 배포는 가중치, KV 캐시, 컨텍스트 길이, 동시 세션 수를 함께 계산해야 한다. 강의자가 제시한 약 200B 이상·Q5 이상은 개인적 경험칙이지 모든 모델·하드웨어에 적용되는 검증된 하한선이 아니다. 약한 모델일수록 리마인더·도구 라우팅·반복 감지 같은 하네스 개입이 더 필요하다는 것이 강의의 결론이다. [영상 B 01:37:56](https://www.youtube.com/watch?v=fsou1Butd6U&t=5876s), [영상 B 01:40:17](https://www.youtube.com/watch?v=fsou1Butd6U&t=6017s), [영상 B 01:45:20](https://www.youtube.com/watch?v=fsou1Butd6U&t=6320s)

반복적인 사람 승인은 피로로 기계적 허용을 유발할 수 있으므로, 입력 재작성, 도구 권한·인자·반복 검사, 비밀값 출력 차단 같은 시스템 가드레일을 분리해야 한다. [영상 A 00:10:24](https://www.youtube.com/watch?v=tBRz9JonUUw&t=624s), [영상 A 00:15:03](https://www.youtube.com/watch?v=tBRz9JonUUw&t=903s)

## Open Questions

강의는 훅 구조까지 다룬 뒤 종료되며, 세션·컨텍스트의 상세 구현, 비즈니스용 에이전트 요구사항, 단계별 구현은 후속 강의 범위로 남긴다. [영상 B 01:53:54](https://www.youtube.com/watch?v=fsou1Butd6U&t=6834s)

두 영상을 구현 결정으로 바꾸려면 다음을 추가로 결정해야 한다.

- 모델이 제어할 범위를 iteration·turn·session 중 어디까지 허용할지, goal의 종료 조건과 예산 상한을 어디에 둘지
- 서브에이전트의 컨텍스트를 상속할지 비울지, 도구·서브세션·후속 요청을 하나의 메시지 규약으로 통합할지
- 전용 도구와 범용 셸, 인메모리와 프로세스 격리, 지속 대기와 스케줄러 재개 중 모델 능력·샌드박스·배포 환경에 맞는 조합
- 반복 승인을 줄이면서도 입력·실행·출력 가드레일, 반복 감지, 중단, 예산 통제를 어떻게 검증할지

이 목록은 강의 내용을 설계 질문으로 변환한 편집 산출물이며 영상의 직접 발언 목록은 아니다.

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|
| C1 | true | 강의는 사전 고정된 경로를 코드가 제어하면 워크플로우, 런타임의 다음 행동을 모델이 결정하면 에이전트로 구분한다. | verified | raw/sources/video/tBRz9JonUUw/9ccab2007ecc554464250fb3b78f40f5daf5e68d6cf1dc423945cfef59be8577/manifest.json | 영상 A 00:16:45–00:21:46의 직접 설명. |
| C2 | true | 강의는 request, iteration, turn, session을 에이전트 런타임의 서로 다른 경계로 설명한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:14:05–00:19:37의 직접 설명. |
| C3 | true | 강의의 구현 관점에서 서브에이전트는 모델이 도구를 통해 생성한 별도 세션이다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:32:13–00:38:37의 직접 설명. |
| C4 | true | 강의에서 goal은 턴 종료 후 달성 여부를 평가해 미달성이면 새 요청과 다음 턴을 만드는 장치다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:49:08–00:51:49의 직접 설명. |
| C5 | true | 강의는 비동기 도구·서브세션·후속 요청을 메시지 타입으로 구분하는 하나의 대기열로 통합하는 방향을 제시한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:56:37–00:57:18의 직접 설명. |
| C6 | true | 강의는 도구와 스킬의 선택 경합을 줄이기 위해 실행 능력과 운용 지식의 책임을 분리하는 조합을 소개한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 01:08:45–01:12:55의 직접 설명. |
| C7 | true | 강의는 도구를 외부 프로세스로 격리하면 진행·취소·오류·최종 결과를 전달하는 공통 프로토콜이 필요하다고 설명한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 01:13:51–01:19:51의 직접 설명. |
| C8 | true | 강의는 변경 이유가 다른 기능을 모듈·디렉터리 경계로 격리해 수정 영향을 국소화하는 구조를 제안한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:39:51–00:45:38의 직접 설명. |
| C9 | true | 강의는 턴 루프 사이의 훅으로 반복 감지, 도구 검사, 출력 가드레일 같은 정책을 핵심 제어 코드에서 분리하는 구조를 제안한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 01:46:55–01:53:40의 직접 설명. |
| C10 | true | 강의는 반복적인 사람 승인에만 의존하지 말고 입력·실행·출력 가드레일을 시스템 수준에서 분리해야 한다고 주장한다. | verified | raw/sources/video/tBRz9JonUUw/9ccab2007ecc554464250fb3b78f40f5daf5e68d6cf1dc423945cfef59be8577/manifest.json | 영상 A 00:10:24–00:16:34의 직접 설명. |
| C11 | true | 강의자는 민감한 작업의 컨텍스트 사용량에 대해 약 4시에 마지막 큰 요청을 보내고 7시 부근을 불가피한 상한으로 두는 개인 경험칙을 제시한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 00:25:21–00:31:35의 강의자 휴리스틱이며 공식 임계값이 아님. |
| C12 | true | 강의자는 제품 수준 코딩에 필요한 로컬 모델의 개인적 경험 하한으로 약 200B 이상과 Q5 이상을 제시한다. | verified | raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json | 영상 B 01:40:17–01:45:03의 개인적·경험적 판단이며 보편 기준이 아님. |

## Relations

| type | target | notes |
|---|---|---|

## Sources

- `raw/sources/video/tBRz9JonUUw/9ccab2007ecc554464250fb3b78f40f5daf5e68d6cf1dc423945cfef59be8577/manifest.json`
- `raw/sources/video/fsou1Butd6U/2ada173b83e1e10bbe734029fb39f008b325e0964b09be4002349c015a889045/manifest.json`
