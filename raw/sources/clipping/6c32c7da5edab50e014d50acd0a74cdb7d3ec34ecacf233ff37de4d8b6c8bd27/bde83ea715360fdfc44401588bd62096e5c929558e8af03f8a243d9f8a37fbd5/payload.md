---
title: "정보보안기사 실기 — 시기별 반복 출제 주제와 보완 우선순위"
tier: llm-synthesis
page_type: benchmark
domain: information-security
domain_confidence: high
shared_scope: domain
tags: []
status: active
date_created: 2026-07-17
date_updated: 2026-07-17
source_paths:
  - drafts/study/1장 정리.md
  - drafts/study/2장 정리.md
  - drafts/study/3장 정리.md
  - drafts/study/4장 정리.md
  - drafts/study/5장 정리.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2013-01-practical-01.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2013-02-practical-02.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2014-01-practical-03.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2014-02-practical-04.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2015-01-practical-05.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2015-02-practical-06.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2016-01-practical-07.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2016-02-practical-08.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2017-01-practical-09.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2017-02-practical-10.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2018-01-practical-11.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2018-02-practical-12.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2019-01-practical-13.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2019-02-practical-14.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2020-01-practical-15.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2020-02-practical-16.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2021-01-practical-17.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2021-02-practical-18.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2022-01-practical-19.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2022-02-practical-20.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2022-04-practical-21.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2023-01-practical-22.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2023-02-practical-23.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2023-04-practical-24.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2024-01-practical-25.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2024-02-practical-26.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2024-04-practical-27.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2025-01-practical-28.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2025-02-practical-29.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2025-04-practical-30.md
  - datasets/info-sec-engineer-practical-past-exams/01-rounds/2026-01-practical-31.md
source_count: 36
provenance: extracted
summary: "2013–2020과 2021–2026의 복원 기출을 서로 다른 모수로 나누어 회차별 반복 주제와 현재 P1·P2·P3 정리 범위를 집계한 우선순위표."
evergreen: false
---

# 정보보안기사 실기 — 반복 출제 주제와 보완 우선순위

두 기간의 문항 수·유형 구성이 다르므로 회차 수와 우선순위를 합산하지 않는다. 각 기간의 표와 회차 근거를 별도로 읽는다.

## 2013–2020 집계

### 판단 기준

- 대상은 2013년 1회부터 2020년 2회까지, 총 16회차의 복원 문항이다.
- **회차 수**는 하나의 회차에서 같은 주제가 여러 문항이어도 1회로 센다.
- **서술·실무형 수**는 해당 주제에 속한 `essay`·`practical` 문항을 각각 센다. 이는 답안 분량·복합성을 보는 지표일 뿐, 배점이 아니다.
- 복원 파일에는 문항별 공식 배점이 없으므로, 이 문서는 “고배점”이나 합격 점수를 추정하지 않는다.
- 대상 파일은 비공식 복원본이므로, 집계는 그 파일에 기록된 문항 유형·답을 기준으로만 성립한다. 공식 시험지의 배점·원문을 확정하지 않는다.
- `P1 직접`은 현재 정리만으로 핵심 개념·답안 구조를 쓸 수 있다는 뜻이다. 당시 법령 수치, 벤더·운영체제별 명령, 문제 고유의 옵션값까지 자동으로 보장한다는 뜻은 아니다.

### 반복 출제 집계

| 우선 | 주제 묶음 | 출제 회차 | 서술·실무형 | 반복해서 요구한 핵심 | 현재 정리 기준 |
|---|---|---:|---:|---|---|
| 최우선 | 위험관리·위험평가 | 16/16 | 14 | 자산·위협·취약점·통제, 평가 접근법, SLE/ALE, 위험처리 4종 | P1 직접 |
| 최우선 | 웹·서비스·코드 취약점 | 15/16 | 23 | SQLi·XSS·파일 업로드, HTTP/웹 서버 설정, 쿠키, Slow HTTP, 메모리 취약점 | P1 핵심 직접; 고유 설정·명령은 별도 연습 필요 |
| 최우선 | 개인정보보호·안전성 확보조치 | 14/16 | 16 | 수집·제공·위탁·파기, 접근권한·접속기록, 내부관리계획, 유출·PIA | P1 원칙 직접; 당시 조문·기간·열거사항은 분리 필요 |
| 최우선 | 운영체제 계정·권한·로그·운영 설정 | 14/16 | 14 | 계정·패스워드, 특수권한, 로그인 로그, `/proc`, cron, 백업·설정 파일 | P1/P2 핵심 직접; OS·버전별 정확 명령은 부분 범위 |
| 높음 | DoS/DDoS와 패킷 기반 판별 | 11/16 | 10 | SYN Flooding, Smurf, 반사·증폭, Slow HTTP, 패킷 근거와 대응 | P1 핵심 직접; 벡터별 세부값은 P2/P3 또는 문제 제시값 우선 |
| 높음 | IDS/IPS·Snort·관제 | 10/16 | 7 | IDS/IPS 배치, 탐지 방식·오탐, rule header·option·threshold | P1 핵심 직접; 복합 rule 작성은 부분 범위 |
| 높음 | VPN·IPsec | 9/16 | 6 | AH/ESP/IKE/SA, 전송·터널 모드, 암호화·인증 범위 | P1 핵심 직접; ESP 인증의 정확 범위는 SA·알고리즘 의존 |

### 회차 근거

| 주제 묶음 | 포함 회차 |
|---|---|
| 위험관리·위험평가 | 2013-1, 2013-2, 2014-1, 2014-2, 2015-1, 2015-2, 2016-1, 2016-2, 2017-1, 2017-2, 2018-1, 2018-2, 2019-1, 2019-2, 2020-1, 2020-2 |
| 웹·서비스·코드 취약점 | 2013-2, 2014-1, 2014-2, 2015-1, 2015-2, 2016-1, 2016-2, 2017-1, 2017-2, 2018-1, 2018-2, 2019-1, 2019-2, 2020-1, 2020-2 |
| 개인정보보호·안전성 확보조치 | 2013-1, 2013-2, 2014-1, 2014-2, 2015-1, 2015-2, 2016-1, 2016-2, 2017-1, 2017-2, 2018-1, 2018-2, 2020-1, 2020-2 |
| 운영체제 계정·권한·로그·운영 설정 | 2013-1, 2013-2, 2015-1, 2015-2, 2016-1, 2016-2, 2017-1, 2017-2, 2018-1, 2018-2, 2019-1, 2019-2, 2020-1, 2020-2 |
| DoS/DDoS와 패킷 기반 판별 | 2013-2, 2014-1, 2015-1, 2015-2, 2016-1, 2017-1, 2017-2, 2018-1, 2018-2, 2019-1, 2020-1 |
| IDS/IPS·Snort·관제 | 2013-1, 2013-2, 2014-1, 2014-2, 2016-1, 2018-1, 2018-2, 2019-1, 2019-2, 2020-1 |
| VPN·IPsec | 2014-1, 2014-2, 2015-2, 2016-2, 2018-1, 2018-2, 2019-1, 2019-2, 2020-1 |

### 보완 우선순위

현재 P1~P3에 고빈도 대주제 자체는 모두 있다. 따라서 새로 넓은 장을 추가하기보다, 아래처럼 **답 전체를 막는 세부 공백**을 보완하는 편이 이 범위의 기출 대응에는 직접적이다.

1. **당시 법령·고시의 열거형 답안**
   - 제3자 제공·위탁·유출 통지·PIA·접속기록에서 당시의 기간, 인원 기준, 고지 항목을 한 묶음으로 분리한다.
   - 현행 기준과 과거 기출 기준을 섞지 않는다. 현행 원칙은 P1로 답하되, 역사적 수치가 필요한 문제는 해당 회차 기준으로만 답한다.

2. **Snort 복합 rule의 기계적 해석·작성**
   - `action`, 방향, IP·port, `content`, `offset/depth`, `distance/within`, `nocase`, `threshold`, `sid`를 한 rule에서 모두 읽고 쓴다.
   - 기본 문법은 P1에 있으나, 여러 option이 결합된 과거 문항은 답안 재현 연습이 필요하다.

3. **IPsec 패킷 도식의 정확 범위**
   - AH/ESP와 전송/터널을 4개 도식으로 구분하고, 새 외부 IP 헤더·원본 패킷·ESP trailer·Auth/Tag의 위치를 쓴다.
   - ESP의 인증 범위·표현은 SA·알고리즘·문서 버전에 따라 달라질 수 있으므로 문제 조건을 우선한다.

4. **운영체제·제품 고유 명령과 설정값**
   - Solaris/AIX/Linux 파일 경로, PAM 옵션, cron, `/proc`, Apache·DNS·라우터 설정은 “개념”이 아니라 제시된 OS·버전·명령 문맥으로 암기한다.
   - 일반 원리를 특정 배포판의 정답으로 바꾸거나, 반대로 오래된 명령을 현행 환경의 일반 규칙으로 확대하지 않는다.

### 낮은 빈도의 개별 항목

EDR, `strace`, TMS, Billion Laughs, SSDP DRDoS, `alert(document.cookie)` 같은 항목은 이 16회 범위에서 각각 한 회차의 개별 문항이다. 현재 자료에서 빈도가 높다고 분류할 근거는 없으므로, 위 반복 주제를 먼저 끝낸 뒤 P3 단답 암기 항목으로 다룬다.

### 결론

- 이 구간에서 가장 먼저 답안화할 것은 **위험관리 → 웹 → 개인정보 → 시스템 운영**이다.
- 그 다음은 **DoS/DDoS → Snort → IPsec**의 패킷·설정·도식형 문항이다.
- 현재 정리의 넓은 개념 범위보다 부족한 부분은 대주제가 아니라, 역사적 법규 열거와 문제 고유의 정확한 명령·옵션·필드 범위다.

## 2021–2026 집계

### 판단 기준

- 대상은 2021년 1회부터 2026년 1회까지, 총 **15회차**의 복원 문항이다. 2021년 2회, 2022~2025년 각 3회, 2026년 1회로 구성된다.
- **회차 수**는 한 회차에서 같은 주제 문항이 여러 개여도 1회만 센다. 따라서 표의 분모는 모두 15이다.
- 주제 묶음은 한 문항에서 겹칠 수 있다. 예를 들어 IPsec 문항은 네트워크와 암호통신에, Snort 기반 DoS 탐지 문항은 관제와 DoS/DDoS에 각각 직접 근거가 있을 때 함께 포함한다. 각 행의 횟수는 합산하지 않는다.
- 아래 우선순위는 복원 문항에 해당 묶음이 직접 등장한 **회차 빈도**만으로 정했다. 배점·합격 가능성·실제 시험 출제 확률을 추정하지 않는다.
- 대상 파일은 비공식 복원본이다. 이 집계는 각 파일에 기록된 문항·정답·해설 범위만 나타내며, 공식 시험지 원문·배점 또는 법령의 당시 효력을 확정하지 않는다.
- 현재 정리의 범위 표기는 `drafts/study/1장`~`5장`의 명시 내용에만 연결했다. 문제 고유의 제품·OS 버전·법령 시점·옵션값은 대주제 범위에 포함되어도 별도 검증·암기가 필요하다.

### 반복 출제 집계

| 우선 | 주제 묶음 | 출제 회차 | 문항에 직접 나타난 신호 | 현재 정리 연결 |
|---|---|---:|---|---|
| 최우선 | 위험관리·자산·위험평가·처리 | 15/15 | 자산·위협·취약점, 위험분석·평가, BIA/ALE, 위험회피·전가·감소·수용 | `5장` P1 |
| 최우선 | 웹·애플리케이션·인터넷 서비스 보안 | 15/15 | SQLi·XSS·CSRF·SSRF·파일 업로드, HTTP, Apache/IIS/Sendmail/DNS 설정, 시큐어 코딩 | `3장` P1; 제품·세부 설정은 P2/P3 병행 |
| 최우선 | 네트워크 프로토콜·장비·경계 보안 | 15/15 | TCP/IP, DNS·ARP, VLAN·스위치·라우팅, 방화벽·iptables, SNMP·NAC | `2장` P1; 무선 세부는 P2 |
| 높음 | 운영체제 계정·권한·로그·운영 설정 | 12/15 | PAM, passwd/shadow, 권한, Linux·Windows 로그, `/proc`, 계정·서비스 설정 | `1장` P1/P2 |
| 높음 | 개인정보·ISMS-P·안전성 확보조치 | 12/15 | 개인정보 처리·수집, 가명정보, PIA, 접속기록, ISMS/ISMS-P, CCTV·생체정보 | `5장` P1 |
| 높음 | 암호통신·IPsec/TLS·인증 | 12/15 | IPsec, TLS, 해시·PGP, Heartbleed, E2EE, 인증서 피닝 | `4장` P1; 피닝 등 세부는 P2 |
| 높음 | IDS/IPS·Snort·SIEM/DLP·관제 | 10/15 | IDS/IPS, 오탐·미탐, Snort rule, UEBA, DLP, SIEM·네트워크 모니터링 | `2장` P1 |
| 보완 | DoS/DDoS·패킷 기반 판별·완화 | 9/15 | Slow HTTP, SYN Flooding, Smurf, 반사·증폭, DNS/NTP 증폭, HTTP Flood | `2장` P1 |
| 보완 | 모바일·BYOD 보안 | 5/15 | Deep Link, BYOD, MDM·컨테이너·모바일 가상화, 인증서 피닝 | `2장`·`3장`·`4장` P2 |

### 회차별 교차검증 원장

약어는 `R` 위험관리, `W` 웹·서비스, `N` 네트워크, `O` 운영체제, `P` 개인정보, `C` 암호통신, `I` IDS/관제, `D` DoS/DDoS를 뜻한다. 이 표의 표시 수를 열별로 다시 세어 위의 15·12·10·9회 집계와 대조했다. 모바일·BYOD(`M`)는 해당 5회차만 별도로 표시한다.

| 회차 | 문항에 직접 나타난 주제 묶음 |
|---|---|
| 2021-1 | R, W, N, P, I, D |
| 2021-2 | R, W, N, O, C, D, M |
| 2022-1 | R, W, N, O, P, C, I |
| 2022-2 | R, W, N, P, C, I, D |
| 2022-4 | R, W, N, P, C, I, D |
| 2023-1 | R, W, N, O, P, I, D, M |
| 2023-2 | R, W, N, O, P, C, D |
| 2023-4 | R, W, N, O, P, C |
| 2024-1 | R, W, N, O, C, I |
| 2024-2 | R, W, N, O, P, C, I, D |
| 2024-4 | R, W, N, O, D |
| 2025-1 | R, W, N, O, P, C, D, M |
| 2025-2 | R, W, N, O, P, C, I, M |
| 2025-4 | R, W, N, O, P, C, I, M |
| 2026-1 | R, W, N, O, P, C, I |

### 회차 근거

| 주제 묶음 | 포함 회차 |
|---|---|
| 위험관리·자산·위험평가·처리 | 2021-1, 2021-2, 2022-1, 2022-2, 2022-4, 2023-1, 2023-2, 2023-4, 2024-1, 2024-2, 2024-4, 2025-1, 2025-2, 2025-4, 2026-1 |
| 웹·애플리케이션·인터넷 서비스 보안 | 2021-1, 2021-2, 2022-1, 2022-2, 2022-4, 2023-1, 2023-2, 2023-4, 2024-1, 2024-2, 2024-4, 2025-1, 2025-2, 2025-4, 2026-1 |
| 네트워크 프로토콜·장비·경계 보안 | 2021-1, 2021-2, 2022-1, 2022-2, 2022-4, 2023-1, 2023-2, 2023-4, 2024-1, 2024-2, 2024-4, 2025-1, 2025-2, 2025-4, 2026-1 |
| 운영체제 계정·권한·로그·운영 설정 | 2021-2, 2022-1, 2023-1, 2023-2, 2023-4, 2024-1, 2024-2, 2024-4, 2025-1, 2025-2, 2025-4, 2026-1 |
| 개인정보·ISMS-P·안전성 확보조치 | 2021-1, 2022-1, 2022-2, 2022-4, 2023-1, 2023-2, 2023-4, 2024-2, 2025-1, 2025-2, 2025-4, 2026-1 |
| 암호통신·IPsec/TLS·인증 | 2021-2, 2022-1, 2022-2, 2022-4, 2023-2, 2023-4, 2024-1, 2024-2, 2025-1, 2025-2, 2025-4, 2026-1 |
| IDS/IPS·Snort·SIEM/DLP·관제 | 2021-1, 2022-1, 2022-2, 2022-4, 2023-1, 2024-1, 2024-2, 2025-2, 2025-4, 2026-1 |
| DoS/DDoS·패킷 기반 판별·완화 | 2021-1, 2021-2, 2022-2, 2022-4, 2023-1, 2023-2, 2024-2, 2024-4, 2025-1 |
| 모바일·BYOD 보안 | 2021-2, 2023-1, 2025-1, 2025-2, 2025-4 |

### 보완 우선순위

1. **매 회차 출제된 세 묶음부터 답안 단위로 묶는다.** 위험관리에서는 자산·위협·취약점에서 평가와 처리까지, 웹·서비스에서는 취약점 원인·영향·대응과 서비스 설정을, 네트워크에서는 프로토콜 동작·공격·방어 장비를 각각 분리해 쓴다.
2. **12회차 묶음은 문제 조건에 맞는 정확한 표현을 보강한다.** 운영체제의 파일 경로·명령·로그 위치, 개인정보의 당시 법령·고시 항목, TLS/IPsec의 보호 범위와 인증 세부는 현재 대주제 정리와 별도로 해당 회차 문맥으로 확인한다.
3. **관제와 DoS/DDoS는 패킷·rule·로그를 함께 연습한다.** 탐지 방식의 정의만으로 끝내지 않고 Snort rule, 오탐·미탐, 공격 트래픽의 식별 근거와 완화 수단을 문항별 조건에 맞춰 답한다.
4. **모바일·BYOD는 P2 보완 항목으로 유지한다.** 5회차에서 Deep Link, BYOD/MDM·컨테이너, 인증서 피닝이 직접 등장하므로, 상위 8개 묶음을 마친 뒤 이 다섯 항목의 원인·대응을 독립적으로 정리한다.

### 결론

- 2021–2026의 15회차에서는 **위험관리·웹/서비스·네트워크**가 모두 15/15회차로 확인된다.
- 그 다음은 **운영체제·개인정보·암호통신**(각 12/15), **IDS/관제**(10/15), **DoS/DDoS**(9/15) 순이다.
- 이 수치는 복원 문항의 회차 빈도만 보인 것이며, 이 문서만으로 특정 회차의 득점·60점 통과·합격 여부를 판단하지 않는다.
