---
title: "정보보안기사 실기 7회 2016년 1회 실기 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-03
source_paths:
  - "https://information-security.tistory.com/284"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 7회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 7회 2016년 1회 실기 복원

## Scope
- Exam mapping: 2016년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 윈도우 PE(Portable Executable) 파일의 섹션에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : .text B : .data C : .idata | source-derived from Information Security Tistory; answer block present |
| 2 | essay | 익스플로잇과 관련된 용어에 관한 물음에 답하시오. | A : 쉘코드(Shellcode) B : 0x90 C : jmp esp | source-derived from Information Security Tistory; answer block present |
| 3 | short | 윈도우 DNS 서버에서 DNS 설정 시 사용하는 두 가지 설정을 쓰시오. | A : Zone 설정 B : 리소스 레코드 설정 | source-derived from Information Security Tistory; answer block present |
| 4 | short | 다음은 Snort 룰에서 패킷 페이로드의 10번째 바이트부터 2바이트 범위(10~12바이트)에서 FFFF 바이트를 탐지하는 룰이다. 빈칸 (A), (B), (C)를 채우시오. | A : content B : offset C : depth | source-derived from Information Security Tistory; answer block present |
| 5 | short | 다음에서 설명하는 악성코드의 명칭을 각각 쓰시오. | A : 드롭퍼(Dropper) B : 인젝터(Injector) | source-derived from Information Security Tistory; answer block present |
| 6 | short | 와이어샤크(Wireshark)에서 DNS 응답(Response) 패킷만 출력하는 필터 표현식을 쓰시오. | dns.flags.response == 1 또는 dns.response_to | source-derived from Information Security Tistory; answer block present |
| 7 | short | 다음에서 설명하는 공격의 명칭을 쓰시오. | WebShell(웹쉘) | source-derived from Information Security Tistory; answer block present |
| 8 | short | 다음에서 설명하는 APT 대응 방법론의 명칭을 쓰시오. | 사이버 킬 체인(Cyber Kill Chain) | source-derived from Information Security Tistory; answer block present |
| 9 | short | 통제 시점에 따른 분류에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 예방 통제 B : 탐지 통제 C : 교정 통제(시정 통제) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 다음에서 설명하는 용어를 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 스머프(Smurf) 공격에 관한 물음에 답하시오. | (A) 공격자는 출발지 IP를 공격 대상 호스트의 IP로 위조한 ICMP Echo Request 패킷을 증폭 네트워크의 브로드캐스트 주소로 전송한다. 근처의 호스트들이 위조된 출발지 IP(공격 대상)로 다량의 ICMP Echo Reply를 전송하여 공격 대상에게 서비스 거부를 유발한다. (B) 라우터에서 외부 네트워크로부터 들어오는 IP Directed Broadcast 패킷을 차단한다. (no ip directed-broadcast) 호스트를 IP 브로드캐스트 주소로 전송된 ICMP Echo Request 패킷에 응답하지 않도록 설정한다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 위험 분석 관련 수치에 관한 물음에 답하시오. | (1) SLE(단일 손실 예상액) : 위협이 한 번 발생했을 때 예상되는 손실 금액이다. (2) SLE = AV(자산 가치) × EF(노출 계수) (3) ARO(Annual Rate of Occurrence, 연간 발생률) (4) ROI = ALE - X (보안 투자 비용 X는 ALE보다 작아야 투자 효과가 있다.) | source-derived from Information Security Tistory; answer block present |
| 13 | short | 정보통신망 이용촉진 및 정보보호 등에 관한 법률에 따라 개인정보 유출 사실을 알았을 때 이용자에게 지체 없이 알려야 하는 사항 5가지를 쓰시오. | (1) 유출된 개인정보 항목 (2) 유출이 발생한 시점 (3) 이용자가 취할 수 있는 조치 (4) 정보통신서비스 제공자 등의 대응 조치 (5) 신고 접수를 할 수 있는 담당 부서 및 연락처 | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음은 crontab 스케줄러 설정 내용이다. 각 항목의 동작을 분석하여 서술하시오. | (1) 매월 6일 0시 0분에 root 권한으로 /tmp/passwd1 파일을 /etc/passwd로 복사한다. 임의로 조작된 passwd1 파일이 원본 passwd 파일을 덮어쓰는 악의적인 계정 변조 행위이다. (2) 매월 12일 0시 0분에 root 권한으로 10.10.10.10 호스트의 80번 포트로 연결하면서 /bin/bash 쉘을 넘긴다. 공격자 서버로의 리버스 쉘(Reverse Shell) 연결로, 공격자가 피해 서버를 원격에서 제어할 수 있게 된다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음 HTTP Request 패킷을 분석하여 보안상 문제점을 서술하시오. | (1) Cache-Control에서 must-revalidate 설정으로 캐시 서버를 사용하지 않아 모든 요청이 서버로 직접 전달되어 서버 부하가 증가할 수 있다. (2) 요청 파라미터에 id와 password 등 민감한 정보가 평문으로 포함되어 있어 스니핑·도청에 의한 정보 유출 위험이 있다. (3) 쿠키 값이 HTTP 통신에서 노출되어 세션 하이재킹 등에 악용될 수 있다. (4) 443번 포트(HTTPS)에서 80번 포트(HTTP, 평문)로 전환하여 통신하고 있어 암호화되지 않은 구간이 발생한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음은 Bash 쉘 취약점과 관련된 내용이다. 물음에 답하시오. | (A) ShellShock(쉘 쇼크) (B) Bash 쉘이 제공하는 함수 선언 기능에서 취약점이 발견되었다. 환경 변수에 함수 정의 형태로 임의의 명령어를 삽입하면 Bash 실행 시 해당 명령어가 함께 실행되는 구조적 결함이 원인이다. (C) 공격자는 자신의 서버에 포트를 열어 대기하고, 피해자 서버에서 공격자 서버로 접속하도록 유도하여 리버스 쉘(Reverse Shell) 연결을 수립하는 행위이다. | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
