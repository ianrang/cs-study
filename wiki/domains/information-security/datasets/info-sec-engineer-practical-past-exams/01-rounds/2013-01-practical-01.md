---
title: 정보보안기사 실기 1회 2013년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/a3014b0c678106452b252ab42c88f8b210d0d985929578ca18a2e65c1da42389/f987d81b5198bdf5e914e7004200da1b5f606d38af6971325564e37fcba2f772/manifest.json
summary: 정보보안기사 실기 1회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 1회 2013년 1회 실기 복원

### Scope
- Exam mapping: 2013년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 다음 위험관리 용어의 빈칸 (A), (B), (C)를 채우시오.<br>(A) 위협의 종류·영향·발생 가능성을 평가하는 과정<br>(B) 위험평가 결과를 바탕으로 비용 대비 통제 방안을 선택·적용하여 위험을 통제하는 과정<br>(C) 선택한 통제의 목적·방안·적용 주체·시점·대상을 문서화한 계획 | (A) 위험평가<br>(B) 위험관리<br>(C) 위험관리계획 | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three answer slots are explicitly mapped; exact official wording unavailable |
| 2 | short | NMS의 정보 수집·전달 방식에 관한 빈칸 (A), (B), (C)를 채우시오.<br>(A) NMS 서버가 장비 상태·통계를 주기적으로 요청·수집하는 방식<br>(B) 장비가 특정 이벤트 발생 사실을 NMS에 비동기로 전달하는 방식<br>(C) 장비의 이벤트·운영 로그를 중앙 로그 서버로 전송·저장하는 방식 | (A) Polling<br>(B) Event Reporting<br>(C) syslog | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three answer slots are explicitly mapped; exact official wording unavailable |
| 3 | essay | 개인정보처리자가 내부적으로 수립·시행해야 하는 계획의 명칭을 쓰시오. 제시 항목은 개인정보 보호책임자 지정, 개인정보 보호책임자와 개인정보취급자의 역할·책임, 개인정보 안전성 확보에 필요한 조치, 개인정보취급자 교육, 그 밖의 개인정보 보호 필요사항이다. | 내부관리계획 | source-derived from Information Security Tistory; prompt list restored |
| 4 | short | 유닉스(UNIX) 솔라리스(Solaris) 사용 로그 파일의 빈칸을 채우시오. (A): 각 사용자의 가장 최근 로그인 시간을 기록하는 파일. (B): `su` 명령 사용 기록을 저장하는 파일. (C): 실패한 로그인 시도를 기록하는 파일. | A : lastlog B : sulog C : loginlog | source-derived from Information Security Tistory; prompt list restored |
| 5 | short | 정보보호 정책을 구현하기 위해 개발하는 문서 유형에 관한 빈칸 (A), (B), (C)를 채우시오. (A)와 (B)는 시스템 보안을 위한 기술·방법을 구체화하고, (C)는 필요한 기술과 파라미터 설정을 일관성 있게 기술한 강제사항이다. | A : 표준 B : 지침 C : 절차 | source-derived from Information Security Tistory; 용어는 정책-표준-지침-절차 문서 체계의 복원 문맥으로 한정 |
| 6 | short | SIEM 주요 기능의 빈칸을 채우시오. (A): 관제 대상 시스템 에이전트가 SNMP·syslog 등으로 로그를 수집·전송하는 과정. (B): 이벤트 발생 누적 횟수 등 유사 정보를 기준으로 그룹화해 하나의 정보로 취합하는 과정. (C): 다양한 로그 표현 형식을 표준 포맷으로 변환하는 과정. (D): 표준화된 로그의 타임스탬프, IP 주소, 이벤트 구성 규칙을 기준으로 여러 로그 간 관계를 분석하는 과정. | A : 로그 수집 B : 로그 분류 C : 로그 변환 D : 로그 분석 | source-derived from Information Security Tistory; 2026-07-16 technical wording correction: collection is not storage |
| 7 | short | IDS 종류의 빈칸을 채우시오. (A) 기반 IDS: 시스템 내부에 설치되어 내부 사용자 활동과 침입 시도를 감시한다. (B) 기반 IDS: 네트워크 패킷 캡처링을 기반으로 통신망 패킷을 분석해 침입을 탐지한다. | A : 호스트(Host) B : 네트워크(Network) | source-derived from Information Security Tistory; prompt list restored |
| 8 | short | 리눅스 시스템 로그 파일의 빈칸을 채우시오. (A): 각 사용자의 최근 로그인 시간과 접근 소스 호스트 정보를 기록하는 파일. (B): 로그인 실패 시도 기록을 저장하는 바이너리 파일. (C): FTP 로그인 사용자 로그와 파일 업로드·다운로드 내역을 기록하는 파일. | A : lastlog B : btmp C : xferlog | source-derived from Information Security Tistory; prompt list restored |
| 9 | short | 업무 목적으로 개인정보파일을 운용하며 개인정보를 처리하는 주체, 그 지휘·감독을 받아 개인정보를 처리하는 사람, 개인정보 처리를 위해 체계적으로 구성한 데이터베이스 시스템의 빈칸 (A), (B), (C)를 채우시오. | A : 개인정보처리자 B : 개인정보취급자 C : 개인정보처리시스템 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 자산 관리 절차의 빈칸을 채우시오. 자산 중요도 평가를 위해 먼저 (A)를 만들고, 누락 없이 자세히 나열한 뒤 자산을 평가·관리하기 쉽게 재분류하기 위해 사용 용도, 피해 규모, 사용 환경 등을 포함한 (B)를 실시한다. | A : 자산목록 B : 자산분류(자산분석) | source-derived from Information Security Tistory; prompt restored |
| 11 | essay | 다음 파일·디렉터리 권한 설정의 의미를 각각 서술하시오.<br>(1) `-r-sr-xr-x root sys /usr/bin/passwd`<br>(2) `-r-xr-sr-x root mail /usr/bin/mail`<br>(3) `drwxrwxrwt sys sys /tmp` | (1) `/usr/bin/passwd` : 소유자(owner) 권한이 r-s로 setuid가 설정되어 있으며, 기타 사용자(other) 권한이 r-x로 실행 권한이 있다. 따라서 모든 사용자가 passwd 명령을 실행할 때 소유자인 root 권한으로 수행된다.<br>(2) `/usr/bin/mail` : 그룹(group) 권한이 r-s로 setgid가 설정되어 있다. 해당 파일 실행 시 mail 그룹 권한으로 수행된다.<br>(3) `/tmp` : 퍼미션이 rwt로 sticky bit가 설정되어 있다. 일반 사용자는 파일 또는 디렉터리 소유자가 아닌 다른 사용자의 파일을 삭제·이름 변경할 수 없다. | source-derived from Information Security Tistory; 2026-07-16 technical correction cross-checked: sticky-directory deletion is allowed to the file owner or directory owner, with privileged users separately exempt |
| 12 | essay | /etc/apache/conf 디렉토리 내에서 10일 이내에 내용이 변경된 파일을 검색하는 find 명령어를 한 줄로 작성하시오. | find /etc/apache/conf -type f -mtime -10 | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 위험 대응 방안에 답하시오.<br>(1) 위험 회피(Risk Avoidance)의 개념과 적용 상황을 자산·위협·취약점 관점에서 서술하시오.<br>(2) 위험 전이(Risk Transfer)의 개념과 적용 상황을 자산·위협·취약점 관점에서 서술하시오. | (1) 위험 회피(Risk Avoidance) : 위험이 존재하는 프로세스나 사업을 수행하지 않고 포기하는 방안이다. 자산의 중요도가 높고 위협 발생 가능성이 높으나 취약점을 제거하기 어려울 때, 해당 업무나 시스템 자체를 폐기하거나 중단하는 방식으로 위험에 대응한다.<br>(2) 위험 전이(Risk Transfer) : 보험 가입이나 외주 등을 통해 잠재적 손실 비용을 제3자에게 이전하거나 할당하는 방안이다. 위협은 존재하나 자체적으로 통제하기 어렵거나 비용이 과다할 때, 위험의 재정적 책임을 외부로 전가하는 방식으로 대응한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: answer parts are explicitly mapped; exact official wording unavailable |
| 14 | essay | 개인정보 안전성 확보조치 기준에 명시된 접근 권한 관리 기준 3가지를 각각 (1), (2), (3)으로 나누어 서술하시오.<br>(1) 업무 담당자별 접근 권한 부여 기준<br>(2) 인사이동 시 권한 조치<br>(3) 권한 이력의 기록·보관 기준 | (1) 개인정보처리자는 개인정보처리시스템에 대한 접근 권한을 업무 수행에 필요한 최소한의 범위로 업무 담당자에 따라 차등 부여하여야 한다.<br>(2) 전보·퇴직 등 인사이동으로 개인정보취급자가 변경된 경우 지체 없이 개인정보처리시스템의 접근 권한을 변경 또는 말소하여야 한다.<br>(3) 권한 부여·변경·말소에 대한 내역을 기록하고, 그 기록을 최소 3년간 보관하여야 한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: three requested answer slots are explicit; legal answer remains source-derived |
| 15 | essay | Cisco 라우터 패스워드 설정 명령어를 각각 완성하시오. (1) 패스워드 암호화 서비스를 활성화하는 전역 설정: `Router(config)# ____`. (2) 패스워드를 암호화하여 저장하는 설정: `Router(config)# ____`. (3) 패스워드를 평문으로 저장하는 설정: `Router(config)# ____`. | (1) service password-encryption (2) enable secret [패스워드] (3) enable password [패스워드] | source-derived from Information Security Tistory; command blanks restored |
| 16 | essay | ARP 테이블을 보고 답하시오. 관리자가 알고 있는 게이트웨이는 `175.113.81.1`이고 실제 MAC은 `a1-b1-c1-d1-e1-f1`이다. ARP 테이블에는 `175.113.81.65 -> 90-9f-5e-00-2f-16`, `175.113.81.1 -> 90-9f-5e-00-2f-16`, `175.113.81.55 -> f4-e1-5e-7f-f0-8f`, `175.113.81.88 -> f4-e1-5e-7f-80-16`이 표시된다. (A) 공격명, (B) 판단 이유, (C) 공격 의심 IP와 MAC, (D) 차단 명령어를 쓰시오. | (A) ARP Spoofing(ARP 스푸핑) 공격 (B) 관리자가 알고 있는 Gateway(175.113.81.1)의 실제 MAC 주소는 a1-b1-c1-d1-e1-f1이지만, ARP 테이블에는 90-9f-5e-00-2f-16으로 변조되어 있다. 동일한 MAC 주소가 175.113.81.65에도 등록되어 있어 ARP Spoofing 공격으로 판단된다. (C) 175.113.81.65 (MAC: 90-9f-5e-00-2f-16) (D) arp -s 175.113.81.1 a1-b1-c1-d1-e1-f1 (Gateway IP에 대한 ARP 캐시를 정적으로 설정하여 위조된 ARP 응답으로 덮어쓰이지 않도록 한다.) | source-derived from Information Security Tistory; ARP table restored |

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

- `raw/sources/clipping/a3014b0c678106452b252ab42c88f8b210d0d985929578ca18a2e65c1da42389/f987d81b5198bdf5e914e7004200da1b5f606d38af6971325564e37fcba2f772/manifest.json`
