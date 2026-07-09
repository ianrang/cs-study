---
title: "정보보안기사 실기 기출 설정·실습 독립 환경 재현 가능성 딥리서치"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, hands-on-lab, verification, exam-reconstruction]
status: active
date_created: 2026-07-06
date_updated: 2026-07-06
source_paths:
  - "../index.md"
  - "../03-classification/subject-type-matrix.md"
  - "../04-mapping/item-reference-map.md"
  - "../06-verification/prompt-completeness-cross-verify-report.md"
  - "https://owasp.org/www-project-webgoat/"
  - "https://owasp.org/www-project-juice-shop/"
  - "https://www.zaproxy.org/docs/docker/"
  - "https://docs.snort.org/"
  - "https://docs.suricata.io/en/latest/"
  - "https://bind9.readthedocs.io/en/latest/reference.html"
  - "https://httpd.apache.org/docs/current/howto/htaccess.html"
  - "https://docs.securityonion.net/en/2.4/"
source_count: 12
provenance: inferred
summary: "정보보안기사 실기 복원 문항의 설정·명령·로그·패킷·웹 취약점 항목을 독립 실습 환경에서 재현 가능한지 검토하고, 안전한 랩 경계와 우선순위를 정리한다."
evergreen: false
---

# 정보보안기사 실기 기출 설정·실습 독립 환경 재현 가능성 딥리서치

## Verdict
가능하다. 다만 모든 기출 항목을 같은 방식으로 직접 재현하면 안 된다. 실습화 기준은 `독립 격리 환경`, `허가된 취약 애플리케이션`, `로컬/사설망 트래픽`, `파괴·증폭·무차별 공격 금지`, `공격 실행보다 설정·탐지·로그 해석 중심`이다.

현재 1~30회 복원 파일을 명령·설정·로그·패킷·웹 취약점 키워드로 스캔한 결과, 실습 후보 행은 301개로 잡힌다. 이 수치는 엄밀한 문항 수가 아니라 후보군이며, 관리·법규·위험평가 문항까지 키워드에 걸린 항목을 포함한다. 실제 실습 세트로 만들기 적합한 핵심 축은 웹 취약점, Linux/Windows 계정·로그, Apache/DNS/NTP/SNMP 등 서비스 설정, Snort/Suricata 룰·PCAP 분석, ARP/라우팅/VLAN 네트워크 동작이다.

## Safety Boundary
| boundary | rule |
|---|---|
| 네트워크 | 인터넷이나 제3자 시스템을 대상으로 스캔·공격·부하 발생을 하지 않는다. |
| DoS/증폭 | SYN Flooding, DNS Amplification, Smurf, Slow HTTP 계열은 실제 부하 재현보다 패킷 샘플·로그·룰 탐지로 학습한다. |
| 악성코드/웹셸 | 실제 지속성·리버스쉘·권한상승 페이로드를 만들지 않는다. toy sample, CTF 앱, 정적 분석, 탐지 룰 중심으로 제한한다. |
| 비밀번호/크래킹 | WPA·패스워드 크래킹은 직접 공격이 아니라 해시 형식, 방어 설정, toy wordlist/샘플 캡처 수준으로 제한한다. |
| 호스트 보호 | Docker는 포트를 `127.0.0.1`에 바인딩하고, VM은 NAT 또는 host-only 네트워크를 기본값으로 둔다. |
| 원본성 | 기출 복원 문항은 공식 원문이 아니라 복원 기준이므로, 실습은 개념 검증용으로 만들고 시험 원문 재현이라고 표현하지 않는다. |

## Feasibility Tiers
| tier | feasibility | examples from current dataset | recommended environment |
|---|---|---|---|
| A | 바로 실습 가능 | Linux 로그 파일, `last`, `lastb`, `lastcomm`, `lsof`, `find`, `chmod`, `chattr`, `lsattr`, `crontab`, `login.defs`, Apache `Options Indexes`, `.htaccess`, `robots.txt`, Cookie flags, `logrotate` | Docker container or throwaway Linux VM |
| A | 바로 실습 가능 | SQL Injection, XSS, 파일 업로드, SSRF, HTTP header injection/CRLF, proxy/ZAP 기반 요청 관찰 | OWASP WebGoat, OWASP Juice Shop, ZAP Docker, localhost binding |
| A | 바로 실습 가능 | Snort rule `msg`, `content`, `nocase`, `depth`, `threshold`; Suricata alert/EVE JSON; PCAP 기반 HTTP/DNS/TCP flag 분석 | local PCAP files + Snort/Suricata container or VM |
| B | 격리망에서 가능 | DNS zone transfer 제한, BIND `allow-transfer`, recursive/authoritative DNS, DNS cache/TTL | two containers or two VMs on an internal Docker network |
| B | 격리망에서 가능 | ARP spoofing 판단, static ARP 대응, promiscuous mode 탐지, routing table, VLAN 개념, Cisco-style command reading | Linux network namespace, GNS3/EVE-NG/Packet Tracer, host-only VM network |
| B | 리소스 필요 | IDS/관제 흐름, NIDS/HIDS, Zeek/Suricata metadata, PCAP pivot, alert triage | Security Onion eval/import VM; x86-64 and sufficient RAM required |
| C | 시뮬레이션 권장 | SYN Flooding, Smurf, DNS Amplification, Slowloris/Slow HTTP POST, NTP monlist DDoS | no live attack; use synthetic logs, tiny local PCAP, rule matching, config hardening |
| C | 시뮬레이션 권장 | ShellShock, reverse shell, web shell, exploit shellcode, PE malware behavior | static analysis, toy vulnerable container, YARA/log detection; no real persistence |
| D | 실습보다 케이스 스터디 | 법령, ISMS-P, 개인정보 안전성 확보조치, 위험평가, BCP/DR, 정책·절차 | checklist, tabletop exercise, answer rubric |

## External Source Findings
| source | useful finding | lab impact |
|---|---|---|
| OWASP WebGoat | Deliberately insecure app for teaching web application security; official page explicitly emphasizes safe/legal environments and warns to disconnect or bind to localhost. | Web 취약점 실습의 1순위. SQLi/XSS/인증/세션/파일 관련 문제를 합법적으로 재현 가능. |
| OWASP Juice Shop | Modern intentionally insecure app for trainings, awareness demos, CTFs, and security tools; supports Node.js, Docker, Vagrant and challenge scoreboard. | 최근 웹/REST/API/프론트엔드 취약점 실습에 적합. |
| ZAP Docker | Docker images support automated ZAP usage, baseline scan, full scan, API scan, and browser UI via Webswing. | WebGoat/Juice Shop 실습 후 passive/active scan 차이, HTTP 요청·응답 관찰에 적합. |
| Snort 3 docs | Rule writing guide covers rule headers, actions, protocols, payload options, `content`, `nocase`, `offset`, `depth`, HTTP buffers, threshold/detection filters. | 기출 Snort 룰 해석 문항을 rule syntax + PCAP alert 실습으로 전환 가능. |
| Suricata docs | User guide covers quickstart, signatures, EVE JSON, rules, HTTP/DNS/SNMP/NTP/SMTP keywords, PCAP file reading, IPS/firewall mode. | Snort와 비교하면서 EVE JSON 로그 분석, PCAP offline detection 실습 가능. |
| BIND 9 ARM | `allow-transfer` defines which hosts may transfer zone information; if not specified, outgoing transfers are disabled by default. | DNS zone transfer 문항은 primary/secondary 컨테이너 2개로 안전하게 검증 가능. |
| Apache HTTP Server docs | `.htaccess` is per-directory config; `AllowOverride None` ignores `.htaccess`; main config is preferred for performance/security. | `.htaccess`, `Options Indexes`, `FilesMatch`, `AddType` 문항을 컨테이너에서 재현 가능. |
| Security Onion docs | Provides network/host visibility, Suricata NIDS alerts, Zeek/Suricata metadata, full packet capture, Elastic Agent, SOC workflow. Hardware docs list eval/import/standalone resource requirements. | 전체 관제 실습은 가능하지만 무겁다. 먼저 Import 또는 Eval로 PCAP/EVTX 분석부터 시작하는 것이 현실적이다. |

## Recommended Lab Architecture
| lab | objective | minimum components | representative exam topics |
|---|---|---|---|
| Lab 1 Web App Security | 웹 취약점 공격 원리와 방어 설정을 허가된 앱에서 재현 | WebGoat or Juice Shop, ZAP, browser, optional Burp | SQLi, XSS, SSRF, file upload, CRLF, Cookie flags, Cache-Control, HTTP OPTIONS |
| Lab 2 Linux Hardening | OS 계정·권한·로그·예약작업을 손으로 확인 | Ubuntu/Debian container or VM, non-production accounts | `/etc/passwd`, `/etc/shadow`, setuid/setgid/sticky, `login.defs`, `last`, `lastb`, `lastcomm`, `crontab`, `lsof` |
| Lab 3 Web/DNS Service Config | 서비스 설정 취약점과 대응을 직접 바꿔 확인 | Apache container, BIND primary/secondary containers | `.htaccess`, `Options Indexes`, `robots.txt`, zone transfer, DNS cache/TTL |
| Lab 4 IDS/PCAP | 탐지 룰과 패킷/로그 해석을 반복 | Snort or Suricata, sample PCAPs, optional Zeek | Snort content/depth/threshold, Suricata EVE, TCP flags, DNS/HTTP logs |
| Lab 5 Network Mini Lab | ARP/라우팅/VLAN/스니핑 개념을 내부망에서 관찰 | Linux network namespaces or 2~3 VMs; optional GNS3/Packet Tracer | ARP cache, static ARP, routing table, promiscuous mode, VLAN command reading |
| Lab 6 Monitoring Stack | 관제 워크플로를 경험 | Security Onion Import/Eval VM | NIDS/HIDS, alert triage, metadata, PCAP pivot, case documentation |

## Prioritized Build Order
1. Lab 2 Linux Hardening: 가장 빠르고 시험 반복도가 높다. 호스트 `/etc`를 직접 바꾸지 말고 컨테이너/VM 내부에서만 실습한다.
2. Lab 1 Web App Security: OWASP 공식 취약 앱으로 SQLi/XSS/파일업로드/쿠키/HTTP 헤더 문항을 안전하게 묶을 수 있다.
3. Lab 4 IDS/PCAP: Snort/Suricata 룰 문항과 로그 분석 문항을 점수화하기 좋다.
4. Lab 3 Web/DNS Service Config: Apache/BIND 설정은 실무형 문제로 전환하기 쉽다.
5. Lab 5 Network Mini Lab: 네트워크 namespace 또는 VM 네트워크 이해가 필요하므로 2차 단계로 둔다.
6. Lab 6 Monitoring Stack: 리소스가 크므로 Security Onion 전체 설치보다 PCAP import/eval부터 검토한다.

## Code Path Contract
| 항목 | 내용 | 근거 |
|---|---|---|
| Request boundary | 정보보안기사 실기 복원 문항의 설정·실습을 독립 환경에서 직접 학습 가능한지 검토한다. 실제 공격 실행 도구 제작이나 외부 대상 공격 절차는 범위 밖이다. | 사용자 요청, current dataset |
| Symptom path | N/A — 버그/장애가 아니라 학습 환경 가능성 검토이다. | N/A |
| Requirement Proposition Matrix | 실습 문항은 격리성, 재현성, 채점 가능성, 법적 안전성을 만족해야 한다. | Safety Boundary, Feasibility Tiers |
| Execution path | 회차별 `*-practical-*.md` 테이블에서 명령·설정·로그·패킷 키워드를 스캔해 후보군을 만들고, 공식 도구 문서로 실습 가능성을 대조했다. | local scan, External Source Findings |
| Connected Surface Inventory | `subject-type-matrix.md` reference-only; `item-reference-map.md` reference-only; future lab guide editable as new dataset document. | same-directory dataset |
| Last-leaf candidate | 후속 구현 시 `hands-on-lab-roadmap.md` 또는 `labs/` 하위에 Docker Compose 기반 실습 세트를 별도 생성한다. | this review |
| Shared surfaces | 회차별 복원 파일, 인덱스, 참고문서 매핑, 예측문제 파일. | dataset directory |
| Allowlist draft | 새 실습 문서, 새 `labs/` 디렉터리, README, docker-compose examples. | future work only |
| Denylist draft | 기존 회차 복원 원문, authored notes, 실제 공격 페이로드, 인터넷 대상 스캔/부하 스크립트. | project AGENTS + safety boundary |
| Validation surface | Docker/VM 실행 검증, localhost binding 확인, no-public-target check, sample PCAP/rule expected alert check. | lab architecture |
| Unknowns | 사용자 장비 사양, Docker/VM 설치 여부, Apple Silicon 여부, Security Onion 실행 가능 RAM, 선호 도구(Burp/ZAP/GNS3/Packet Tracer). | not yet inspected |

## Open Questions For Implementation
| question | why it matters |
|---|---|
| 장비가 Apple Silicon인지 x86-64인지 | Security Onion은 x86-64만 지원하므로 Mac ARM이면 별도 x86 서버/클라우드 또는 Suricata/Zeek 경량 대체가 필요하다. |
| Docker Desktop/Colima/Podman 중 무엇을 쓸지 | 네트워크 namespace, 포트 바인딩, privileged capture 권한 설계가 달라진다. |
| 실습 목표가 시험 대비인지 실무 역량인지 | 시험 대비라면 짧은 재현+암기 체크리스트, 실무 역량이면 관제/로그/리포팅까지 포함한다. |
| 공격 실습 허용 수준 | 실제 공격 부하 재현은 제외하고, 취약 앱·toy sample·offline PCAP 중심으로 고정하는 것이 안전하다. |

## Next Artifact Proposal
다음 산출물은 `hands-on-lab-roadmap.md`가 적절하다. 각 Lab별로 `기출 문항 매핑`, `목표`, `구성`, `실습 절차`, `기대 관찰값`, `채점 질문`, `정리 명령`, `금지 행동`을 표준 템플릿으로 만든다.
