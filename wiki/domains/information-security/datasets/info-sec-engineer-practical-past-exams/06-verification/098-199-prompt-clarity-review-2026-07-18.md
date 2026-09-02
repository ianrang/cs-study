---
title: 정보보안기사 실기 복원 98~199번 문제·답안 대응성 검토
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
- verification
date_created: '2026-07-18'
date_updated: '2026-07-18'
source_paths:
- raw/sources/clipping/c848db84cd752a141a9eb087628cf6d06da0c4549df318326b7db3e7a028b360/46d8fb7ac5c3ba7fa4dbcc13a33120814af028e9b70881bd761e2db1879b82a2/manifest.json
summary: R07-Q03~R13-Q09, 즉 변환 순서 98~199번을 직접 읽어 질문·정답 항목의 대응, 복원 한계, 기술적 판정 연결을 확인한
  기록. KCA 공식 시험지 문구를 주장하지 않는다.
---

## Overview









# 정보보안기사 실기 복원 98~199번 문제·답안 대응성 검토

### Scope and Boundary

- 대상은 변환 순서 **98~199번**, 즉 `R07-Q03~R07-Q16`, `R08-Q01~R08-Q16`, `R09-Q01~R09-Q16`, `R10-Q01~R10-Q16`, `R11-Q01~R11-Q15`, `R12-Q01~R12-Q16`, `R13-Q01~R13-Q09`이다.
- 각 문항의 복원 prompt·answer를 직접 읽어, 복수 답이 특정 값·명령·상황과 대응하는지 검토했다. 기술 사실의 기존 전수 판정은 [101~513 기술 정확성 검증](101-513-content-review-2026-07-17.md)을 교차 참조한다.
- 회차 MD는 블로그·편집본 기반의 **비공식 복원 SoT**다. 이 기록은 KCA 공식 시험지 문구·공식 정답을 주장하지 않는다.

### Disposition Codes

| code | meaning |
|---|---|
| `CLEAR` | 단일 답이거나, 기존 prompt가 답안 항목을 이미 명확하게 한정한다. |
| `LIST` | 정해진 순서가 아닌 복수 예시·목록을 쓰는 문항이다. 임의 번호를 붙여 단일 순서를 정답으로 만들지 않는다. |
| `PATCHED` | 문제 요구사항과 답안 항목이 섞여 있어, 복원 문구에 라벨·조건·개행을 추가했다. |
| `BOUNDARY` | 법령 시점·제품/구현 환경·비공식 복원 한계가 있어 기존 기술 검증의 경계를 유지한다. |

### Direct Read Results

| source range | per-item disposition |
|---|---|
| `R07-Q03~Q16` | Q03 `CLEAR`; Q04 `CLEAR`; Q05 `CLEAR`; Q06 `CLEAR`; Q07 `CLEAR`; Q08 `CLEAR`; Q09 `CLEAR`; Q10 `BOUNDARY`; Q11 `PATCHED` (공격 원리/라우터·호스트 대응 분리); Q12 `CLEAR`; Q13 `LIST`; Q14 `CLEAR`; Q15 `PATCHED` (캐시 지시자·평문 노출·포트 추론 분리); Q16 `PATCHED` (명칭·원인·연결 행위 분리). |
| `R08-Q01~Q16` | Q01 `BOUNDARY`; Q02 `CLEAR`; Q03 `BOUNDARY`; Q04 `CLEAR`; Q05 `CLEAR`; Q06 `CLEAR`; Q07 `CLEAR`; Q08 `CLEAR`; Q09 `PATCHED` (고유식별정보·연 1회·취약점의 누락된 조건 복원); Q10 `CLEAR`; Q11 `CLEAR`; Q12 `PATCHED` (확인/서버 대응 분리); Q13 `LIST` (연계보관성은 근거상 단일 단계 순서를 강제하지 않음); Q14 `PATCHED` (명칭·영향 버전·대응 분리); Q15 `CLEAR`; Q16 `PATCHED` (승인/공표 분리). |
| `R09-Q01~Q16` | Q01 `LIST`; Q02 `BOUNDARY`; Q03 `CLEAR`; Q04 `CLEAR`; Q05 `PATCHED` (`frag`의 ID·크기·offset 값 대응); Q06 `BOUNDARY`; Q07 `BOUNDARY`; Q08 `CLEAR`; Q09 `CLEAR`; Q10 `LIST`; Q11 `CLEAR`; Q12 `LIST`; Q13 `PATCHED` (각 `ndd` 명령과 대응 공격 분리); Q14 `CLEAR`; Q15 `LIST`; Q16 `PATCHED` (공격·backlog 영향·iptables 예시 완성값 분리, 단일 규칙의 limit 한계 유지). |
| `R10-Q01~Q16` | Q01 `CLEAR`; Q02 `BOUNDARY`; Q03 `CLEAR`; Q04 `CLEAR`; Q05 `CLEAR`; Q06 `BOUNDARY`; Q07 `CLEAR`; Q08 `BOUNDARY`; Q09 `BOUNDARY`; Q10 `CLEAR`; Q11 `CLEAR`; Q12 `LIST`; Q13 `CLEAR`; Q14 `CLEAR`; Q15 `PATCHED` (공격명·증폭 원리·라우터/호스트 대응 분리); Q16 `BOUNDARY`. |
| `R11-Q01~Q15` | Q01 `CLEAR`; Q02 `CLEAR`; Q03 `CLEAR`; Q04 `CLEAR`; Q05 `CLEAR`; Q06 `BOUNDARY`; Q07 `PATCHED` (SNMP Request/Trap·Inform의 방향·포트 분리); Q08 `BOUNDARY`; Q09 `CLEAR`; Q10 `CLEAR`; Q11 `PATCHED` (스캔 방식·서비스명·세 trace 결과 분리); Q12 `BOUNDARY`; Q13 `LIST`; Q14 `PATCHED` (공격명·추론 가능 정보·대응 분리); Q15 `CLEAR`. |
| `R12-Q01~Q16` | Q01 `CLEAR`; Q02 `CLEAR`; Q03 `CLEAR`; Q04 `CLEAR`; Q05 `CLEAR`; Q06 `LIST`; Q07 `BOUNDARY`; Q08 `CLEAR`; Q09 `CLEAR`; Q10 `CLEAR`; Q11 `PATCHED` (인터넷망/업무망 가상화 장점 분리); Q12 `LIST`; Q13 `PATCHED` (Snort depth 빈칸·action·threshold 분리); Q14 `CLEAR`; Q15 `CLEAR`; Q16 `BOUNDARY`. |
| `R13-Q01~Q09` | Q01 `CLEAR`; Q02 `CLEAR`; Q03 `PATCHED` (오용·이상·오탐 정의 분리); Q04 `CLEAR`; Q05 `BOUNDARY`; Q06 `PATCHED` (블랙박스/화이트박스 정의 분리); Q07 `PATCHED` (확률 분포법/델파이법 정의 분리); Q08 `CLEAR`; Q09 `CLEAR`. |

### Applied Prompt Corrections

아래 항목만 복수 요구사항이 한 문장에 섞였거나, 답안의 순서·조건을 문제에서 찾기 어려워 source-derived 복원 문구를 정리했다. 기술 정답의 근거는 각 회차 MD의 verification과 [101~513 기술 정확성 검증](101-513-content-review-2026-07-17.md)의 개별 판정을 따른다.

| item IDs | correction |
|---|---|
| `R07-Q11/Q15/Q16` | Smurf의 원리·대응 범위, HTTP 캐시/평문/TLS 추론, ShellShock의 명칭·원인·연결 행위를 분리했다. |
| `R08-Q09/Q12/Q14/Q16` | 누락된 고유식별정보 취약점 점검 조건을 복원하고, 파일 업로드·HeartBleed·ISMS 승인/공표 요구사항을 항목별로 매핑했다. |
| `R09-Q05/Q13/Q16` | `frag` 수치, 두 `ndd` 명령, SYN Flood·backlog·iptables 문법을 각각 분리했다. R09-Q16의 예시는 완전한 rate-limit 정책이 아니라는 기존 경계를 보존한다. |
| `R10-Q15` | Smurf 공격명·증폭 원리·라우터와 호스트의 조치를 분리했다. |
| `R11-Q07/Q11/Q14` | SNMP 방향과 포트, TCP scan trace별 판정, Blind SQL Injection의 식별·추론·대응을 분리했다. |
| `R12-Q11/Q13` | 망 가상화 두 종류의 장점과 Snort rule의 depth·action·threshold를 분리했다. |
| `R13-Q03/Q06/Q07` | 침입 탐지, 웹 분석, 정성 위험 분석의 각 정의를 대응하는 빈칸별로 분리했다. |

### Cross-Verification and Non-Expansion Rules

- `R08-Q09`는 회차별 복원 원천의 문장(고유식별정보·연 1회·취약점)을 대조해 누락된 조건만 복구했다. 현행 법령을 과거 시험 정답으로 치환하지 않는다.
- `R09-Q16`, `R11-Q07`, `R11-Q11`, `R12-Q13`은 [101~513 기술 정확성 검증](101-513-content-review-2026-07-17.md)의 Netfilter, SNMP, TCP, Snort 관련 경계와 모순하지 않는지 재확인했다.
- `LIST` 문항에는 임의의 항목별 고정 순서·추가 답안을 만들지 않았다. `BOUNDARY` 문항에는 제품 버전·법령 시행일·공식 KCA 원문이 없는 사실을 감춘 단정문을 추가하지 않았다.
- 계약 검증은 이번 `PATCHED` 항목의 prompt와 answer에 동일한 라벨 및 줄바꿈이 남아 있는지 확인한다.

## Schema / Composition

## Usage

## Limitations / Biases

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|


## Relations

| type | target | notes |
|---|---|---|


## Sources

- `raw/sources/clipping/c848db84cd752a141a9eb087628cf6d06da0c4549df318326b7db3e7a028b360/46d8fb7ac5c3ba7fa4dbcc13a33120814af028e9b70881bd761e2db1879b82a2/manifest.json`
