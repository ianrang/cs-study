---
title: "정보보안기사 실기 2026년 2회 학습 우선순위 및 예측 가능성 검증"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, study-strategy, prediction, verification]
status: active
date_created: 2026-07-07
date_updated: 2026-07-07
source_paths:
  - "../05-analysis/frequency-analysis.md"
  - "../05-analysis/pattern-analysis.md"
  - "../05-analysis/recurrence-analysis.md"
  - "../03-classification/subject-type-matrix.md"
  - "../03-classification/subject-type-classification-detail.md"
  - "../06-verification/prompt-completeness-cross-verify-report.md"
  - "study-strategy-2026-02.md"
  - "../08-prediction/predicted-practical-questions-2026-02.md"
source_count: 8
provenance: inferred
summary: "1~31회 513문항 기준으로 학습 우선순위와 다음 회차 예측 가능성을 분리해 검증한 리포트. 정밀 예측은 확률적 후보군 압축까지만 가능하고, 실제 문항 단정은 불가능하다고 판정한다."
evergreen: false
---

# 정보보안기사 실기 2026년 2회 학습 우선순위 및 예측 가능성 검증

## Verdict
- 학습 우선순위 분석은 유의미하다. 1~31회 513문항의 과목·유형 분포와 23~31회 최근성 신호가 일관되게 나온다.
- 정밀 예측은 확률 분포와 후보군 압축 수준에서는 가능하다. 특정 실제 문항, 순번, 문구를 높은 신뢰도로 단정하는 예측은 불가능하다.
- 기존 `study-strategy-2026-02.md`와 `predicted-practical-questions-2026-02.md`는 아직 1~30회/23~30회 기준 문구가 남아 있으므로, 31회 반영 전에는 최종 전략 문서로 사용하면 안 된다.

## Evidence Base
| evidence | current value | interpretation |
|---|---:|---|
| 전체 분석 단위 | 513문항 | 1~31회 과목·유형 분석 가능 |
| 최근 분석 단위 | 162문항 | 23~31회 최근성 분석 가능 |
| 단답형 | 318문항, 62.0% | 단답 즉답 훈련이 기본축 |
| 서술형/실무형 | 195문항, 38.0% | 설정·로그·코드·법규 적용 답안 훈련 필요 |
| 31회 원천 한계 | 사용자 제공 HTML 표 | 공식 문구 예측에는 사용 불가, 최근성 신호에는 제한적으로 사용 |
| 32회 원천 | verified reconstruction source absent | 32회는 기출 데이터셋에 넣지 않음 |

## Subject Priority, 1~31회
| priority | subject | all count/share | recent 23~31 count/share | learning decision |
|---:|---|---:|---:|---|
| 1 | 정보보안 관리 및 법규 | 156 / 30.4% | 44 / 27.2% | 최우선. 위험관리, 개인정보, ISMS-P, CISO, 생체인식 보호 원칙을 서술형까지 준비 |
| 2 | 네트워크 보안 | 142 / 27.7% | 41 / 25.3% | 최우선. DNS, SNMP, VLAN, IPSec, ARP/ICMP, 방화벽 룰을 설정형으로 준비 |
| 3 | 어플리케이션 보안 | 96 / 18.7% | 33 / 20.4% | 최근 상승. XSS, CSRF, SQLi, 파일 업로드, SSRF, 퍼징, 웹 서버 설정을 강화 |
| 4 | 시스템 보안 | 73 / 14.2% | 34 / 21.0% | 최근 상승. Linux/Unix 파일·권한·로그·명령, Windows 로그 경로를 강화 |
| 5 | 정보보안 일반 | 46 / 9.0% | 10 / 6.2% | 압축 학습. 암호, 해시, 접근통제, DR 기본 개념 위주 |

## Study Allocation
| area | allocation | reason |
|---|---:|---|
| 관리/법규·위험관리 | 25% | 전체 최다, 최근도 1위. 법령/관리 문항은 단답과 서술형 모두 출제 |
| 네트워크·프로토콜·장비 | 22% | 전체 2위, 최근 2위. 설정·공격·프로토콜 해석으로 변형 |
| 어플리케이션·웹 취약점 | 21% | 31회 반영 후 최근 비중 상승. XSS/CSRF/Fiddler/퍼징까지 확장 |
| 시스템·OS 로그/명령 | 20% | 전체보다 최근 비중이 높음. `/etc`, 로그, 권한, xinetd, iptables 중심 |
| 정보보안 일반 | 7% | 낮은 빈도지만 암호·해시·접근통제 기반 개념은 놓치면 안 됨 |
| 답안 작성/오답 회수 | 5% | 실기는 키워드만 알고 문장화하지 못하면 감점 |

## High-Value Concept Groups
| tier | concept group | basis | required output |
|---|---|---|---|
| A | 위험관리/위험평가 | 1~30회 recurrence 79건, 31회 위험관리 단계 추가 | 위험분석/평가/대응, 자산·위협·취약점, SLE/ALE/ARO, 기준선/상세/복합 |
| A | 접근통제/권한관리 | recurrence 74건, 시스템·관리 양쪽에 걸침 | DAC/MAC/RBAC, PAM, 계정·패스워드, 최소권한, IAM/EAM |
| A | Linux/Unix 로그·명령 | 최근 23~30회 21건, 31회 `/etc/passwd` 추가 | passwd/shadow, utmp/wtmp/btmp, lastb/lastcomm/lsof, SUID/SGID, xinetd/iptables |
| A | 웹 취약점/웹 서버 설정 | 31회 XSS/CSRF/Fiddler/URL Rewrite 추가 | SQLi, XSS, CSRF, SSRF, 파일 업로드, CRLF, Apache/IIS 설정 |
| B | DNS/SNMP/VLAN/네트워크장비 | recurrence 54건, 31회 DNS spoofing/iptables 추가 | DNS spoofing/zone transfer, SNMPv3/ACL/RO, VLAN, uRPF, ACL |
| B | IDS/IPS/Snort/관제 | recurrence 52건, 31회 SIEM 추가 | Snort 룰, HIDS/NIDS, FP/FN, SIEM/SOAR, 로그 상관분석 |
| B | 개인정보/ISMS-P/법규 | recurrence 56건, 31회 IDC/CISO/생체인식 추가 | 안전성 확보조치, CISO, 집적정보통신시설, 생체정보 원칙, ISMS-P |
| C | IPSec/TLS/암호통신 | recurrence 34건, 31회 TLS handshake 추가 | AH/ESP/IKE, TLS 세션키, 비대칭/대칭키 용도, 해시 |
| C | DB/데이터보호 | recurrence 19건 | API/Plug-in/TDE, 감사, 마스킹, DLP, GRANT/REVOKE |
| C | 업무연속성/재해복구·무선/모바일 | lower frequency | DR site, RTO/RPO, WPA2, MDM/BYOD, deep link |

## Prediction Model
다음 회차가 18문항이라고 가정하고, 최근 23~31회 162문항에 단순 Dirichlet(1) 보정을 적용했다. 이는 공식 출제모형이 아니라 현재 복원 데이터 내부의 확률적 기준선이다.

| subject | recent count/share | posterior mean | expected in 18 items | approx 80% range | prediction use |
|---|---:|---:|---:|---:|---|
| 정보보안 관리 및 법규 | 44 / 27.2% | 26.9% | 4.9 | 2.4~7.3 | 거의 반드시 대비 |
| 네트워크 보안 | 41 / 25.3% | 25.1% | 4.5 | 2.2~6.9 | 거의 반드시 대비 |
| 시스템 보안 | 34 / 21.0% | 21.0% | 3.8 | 1.6~6.0 | 고확률 대비 |
| 어플리케이션 보안 | 33 / 20.4% | 20.4% | 3.7 | 1.5~5.9 | 고확률 대비 |
| 정보보안 일반 | 10 / 6.2% | 6.6% | 1.2 | 0~2.5 | 0~2문항 대비 |

## What Can Be Predicted
| prediction target | feasibility | reason |
|---|---|---|
| 과목별 기대 문항 수 | 가능 | 최근 162문항 분포가 있고 회차당 18문항 구조가 안정적 |
| 고빈도 개념군 | 가능 | 반복 개념군과 최근성 신호가 중첩됨 |
| 답안 형태 | 가능 | 단답 62%, 서술/실무 38% 구조가 안정적 |
| 실제 문제 문구 | 불가능 | KCA 공식 원문 미확보, 복원 원천 기반 |
| 특정 순번 예측 | 불가능 | 순번과 과목의 안정적 규칙이 없음 |
| 특정 문항 적중 보장 | 불가능 | 출제자는 비랜덤·비공개 기준으로 문제를 구성하며 과거 데이터 표본이 작음 |

## High-Probability Prediction Set
아래는 "출제될 가능성이 큰 학습 후보군"이지 실제 문항 보장이 아니다.

| rank | predicted axis | expected form |
|---:|---|---|
| 1 | 위험관리/위험평가 | 위험분석 단계, 위험대응, 자산·위협·취약점, 개인정보 영향평가 공식 |
| 2 | Linux/Unix 계정·로그·권한 | `/etc/passwd`, `/etc/shadow`, 로그 파일, SUID/SGID, xinetd/iptables 설정 |
| 3 | 웹 취약점 | XSS/CSRF/SQLi/SSRF/파일 업로드의 원리·판단근거·대응 |
| 4 | DNS/SNMP/VLAN/방화벽 | DNS spoofing/zone transfer, SNMP 보안, VLAN 방식, iptables/ACL |
| 5 | 개인정보/ISMS-P/법규 | CISO, IDC 사업자, 개인정보 안전조치, 생체정보 보호 원칙 |
| 6 | IDS/IPS/Snort/SIEM | Snort 룰 해석, HIDS/NIDS, SIEM 기능, 로그 상관분석 |
| 7 | TLS/IPSec/암호 | TLS handshake, AH/ESP/IKE, 해시, 인증서·세션키 |
| 8 | 서비스 설정 | Apache/IIS URL Rewrite, HTTP 헤더, SMTP relay, NTP, DB 감사 |

## Final Judgment
- 학습 우선순위는 통계적으로도 실무적으로도 뽑을 수 있다.
- 정밀 예측은 "다음 회차에 관리/법규 3~6문항, 네트워크 3~6문항, 시스템 2~5문항, 어플리케이션 2~5문항, 일반 0~2문항이 나올 가능성이 높다" 수준까지 가능하다.
- "어떤 실제 문항이 나온다"는 단정형 예측은 현재 데이터로는 불가능하며, 그렇게 말하면 과적합이다.
