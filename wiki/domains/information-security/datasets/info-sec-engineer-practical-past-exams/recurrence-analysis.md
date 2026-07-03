---
title: "정보보안기사 실기 재출제 및 변형출제 분석"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-analysis, recurrence]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "subject-type-classification-detail.md"
  - "subject-type-matrix.md"
  - "item-reference-map.md"
  - "frequency-analysis.md"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 1~30회 복원 문항에서 반복 개념과 최근 변형 출제 축을 추출한 분석."
evergreen: false
---

# 정보보안기사 실기 재출제 및 변형출제 분석

## Scope
- 반복 개념은 회차 파일의 prompt/answer 및 `subject-type-classification-detail.md`의 evidence를 키워드 기준으로 묶었다.
- 같은 개념이 다른 과목 분류에 걸치는 경우, 학습 관점의 개념군으로 통합했다.
- 공식 PDF 원문 미대조 상태이므로 동일 문구 반복이 아니라 동일 개념·동일 실무기술 반복이다.

## Recurring Concept Groups
| concept group | matched items | appeared rounds | recent items, 23~30회 | interpretation |
|---|---:|---:|---:|---|
| 위험관리/위험평가 | 79 | 30 | 25 | 전 회차에 걸쳐 반복되는 최상위 축. 위험분석 방법, 위험대응, 자산 중요도, BIA/ALE/SLE가 변형된다. |
| 접근통제/권한관리 | 74 | 28 | 31 | DAC/MAC/RBAC, 계정·권한·패스워드·PAM·IAM/EAM 등으로 넓게 반복된다. |
| 개인정보/ISMS-P/법규 | 56 | 27 | 13 | 개인정보 안전성 확보조치, ISMS-P, 정보통신망법/개인정보보호법 기반으로 반복된다. |
| HTTP/웹서버 설정 | 55 | 28 | 16 | Apache/IIS, 쿠키 속성, HTTP method/header, robots.txt, CRLF/response splitting 등으로 변형된다. |
| DNS/SNMP/VLAN/네트워크장비 | 54 | 26 | 17 | DNS, SNMP, VLAN, 스위치/라우터 설정이 단답과 실무형을 오간다. |
| IDS/IPS/Snort/관제 | 52 | 26 | 16 | IDS/IPS 개념, Snort 룰, SIEM/SOAR/HIDS/NIDS, 오탐/미탐으로 반복된다. |
| 리눅스/유닉스 로그·명령 | 52 | 26 | 21 | `/etc`, `/proc`, shadow/passwd, utmp/wtmp/btmp, 권한·xinetd·iptables 명령이 최근 강하다. |
| 네트워크 공격/스캔 | 49 | 23 | 9 | SYN/Smurf/DRDoS/ARP spoofing/scan/sniffing 계열이 반복된다. |
| 웹 취약점/시큐어코딩 | 36 | 22 | 15 | SQL Injection, XSS, SSRF, XXE, 파일 업로드, PreparedStatement 등으로 반복된다. |
| IPSec/VPN/암호통신 | 34 | 22 | 8 | IPSec AH/ESP/IKE, TLS/DTLS, PGP/E2EE, 인증서 고정으로 변형된다. |
| 업무연속성/재해복구 | 26 | 16 | 5 | BCP, DR site, RTO/RPO, 미러/핫/웜/콜드 사이트로 반복된다. |
| 악성코드/APT/포렌식 | 26 | 18 | 10 | APT/Kill Chain, malware, PE 분석, 포렌식, 제로데이·공급망 공격으로 최근성 높음. |
| 데이터베이스/데이터보호 | 19 | 14 | 7 | DB 보안, 감사, 암호화 저장, 마스킹, DLP 계열로 변형된다. |
| 무선/모바일 | 12 | 11 | 5 | WEP/WPA, CSMA/CA, deep link, MDM/BYOD 등으로 최근 확장된다. |

## Transformation Patterns
| pattern | examples | implication |
|---|---|---|
| 개념명 단답 → 구성요소 빈칸 | IPSec → AH/ESP/IKE, 위험관리 → 자산/위협/취약점, 접근통제 → DAC/MAC/RBAC | 핵심 약어와 구성요소를 같이 암기해야 한다. |
| 용어 식별 → 설정/명령 실무 | Linux 로그 파일 → `lastb`/`lastcomm`, Apache option → 제거 지시자, xinetd/iptables 설정 | 단순 정의보다 파일명·명령·설정 위치까지 연결해야 한다. |
| 공격명 식별 → 판단근거·대응 | SQL Injection, XSS, DRDoS, Slow HTTP, ARP spoofing, NTP monlist | 로그/패킷/코드에서 증거를 찾고 대응책을 쓰는 형태로 변형된다. |
| 법규/관리 기준 → 적용 상황 판단 | 개인정보 안전성 확보조치, ISMS-P, CISO, 영상정보처리기기, 위탁 공개사항 | 조문 암기보다 상황별 요구사항을 분리해야 한다. |
| 장비/프로토콜 특성 → 보안 설정 | VLAN, SNMP, DNS zone, IPsec, NetBIOS, NTP | 네트워크 지식과 보안 운영 설정을 함께 묻는다. |

## High-Recurrence Priorities
| priority | concept group | why |
|---:|---|---|
| 1 | 위험관리/위험평가 | 전 30회에 등장하고 최근 23~30회에서도 25건이 탐지된다. |
| 2 | 접근통제/권한관리 | 계정, 권한, 인증, 접근통제 모델이 시스템·관리·법규를 가로지른다. |
| 3 | 리눅스/유닉스 로그·명령 | 최근 23~30회에서 21건으로 최근성이 높다. |
| 4 | HTTP/웹서버 설정 + 웹 취약점 | HTTP 설정과 취약점이 단답·실무형 모두에서 반복된다. |
| 5 | DNS/SNMP/VLAN/네트워크장비 | 최근 23~30회에서 장비/프로토콜 실무 문항으로 반복된다. |

## Limits
- 키워드 기반 재출제 분석이므로 동의어 누락과 과포함 가능성이 있다.
- 공식 PDF 원문 대조 전까지는 "동일 공식 문구 반복"이 아니라 "동일 개념 반복"으로 해석해야 한다.
