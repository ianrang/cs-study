---
title: 정보보안기사 실기 9회 2017년 1회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-18'
source_paths:
- raw/sources/clipping/f2a6224b03411c630150eea487dc7306ab28866f83e47d0737532d1052788786/cd4f74a4769f3740eedd9855046e8879345e12fefb8eddecf0ca521aa1f4a485/manifest.json
summary: 정보보안기사 실기 9회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지.
---

## Overview




# 정보보안기사 실기 9회 2017년 1회 실기 복원

### Scope
- Exam mapping: 2017년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 운영체제별로 경로는 다르지만 DNS 정보를 담고 있으며, Windows 7 이상에서는 관리자 외 수정이 제한되는 파일의 이름을 쓰시오. | hosts | source-derived from Information Security Tistory; answer block present |
| 2 | short | Smurf 공격 과정의 빈칸을 채우시오. 공격자가 희생자 IP로 위조하여 ICMP (A)를 브로드캐스트 주소로 전송한다. 브로드캐스트 범위 내 호스트들이 희생자 IP로 ICMP (B)를 전송한다. 이를 방어하기 위해 라우터에서 (C) 패킷이 포워드되지 않도록 설정한다. | A : Echo Request B : Echo Reply C : Directed Broadcast | source-derived from Information Security Tistory; prompt process restored |
| 3 | short | 버퍼 오버플로우 유형의 빈칸을 채우시오. (A): 스택 영역 버퍼 크기를 초과하는 데이터나 실행 가능한 코드를 넣어 변수나 복귀 주소를 변경해 임의 코드를 실행한다. (B): 힙 영역에서 동적 할당된 버퍼를 초과하는 데이터를 입력해 발생한다. | A : 스택 버퍼 오버플로우(Stack Buffer Overflow) B : 힙 버퍼 오버플로우(Heap Buffer Overflow) | source-derived from Information Security Tistory; prompt descriptions restored |
| 4 | short | Trustwave사가 개발하여 Apache 웹 서버와 IIS에서 사용 가능한 공개용 웹 방화벽(WAF)의 명칭을 쓰시오. | ModSecurity | source-derived from Information Security Tistory; answer block present |
| 5 | essay | 단편화된 tcpdump 패킷 정보 `frag 95 : 1480 @ 2920+`를 보고 다음 각 값의 의미를 서술하시오.<br>(A) `95`<br>(B) `1480`<br>(C) `2920` | (A) Fragment ID(단편화 식별자): 같은 원본 패킷에서 분리된 단편임을 나타내는 ID<br>(B) Size(단편의 크기): 해당 단편의 데이터 크기(1480바이트)<br>(C) Offset(오프셋): 원본 패킷에서 해당 단편이 시작되는 위치(2920바이트 지점) | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: each tcpdump value is explicitly mapped to its answer; exact official wording unavailable |
| 6 | short | 정보통신망법 제23조의2 설명의 빈칸을 채우시오. 제1항제1호: 제23조의3에 따라 (a)으로 지정받은 경우. 제2항: 주민등록번호를 수집·이용할 수 있는 경우에도 주민등록번호를 사용하지 않고 본인을 확인하는 방법인 (b)를 제공해야 한다. | a : 본인확인기관 b : 대체수단 | source-derived from Information Security Tistory; legal text restored |
| 7 | short | TLS 1.2 이하의 레코드 프로토콜 처리 순서 `상위 계층 메시지 -> (A) -> (B) -> (C) 추가 -> (D) -> 헤더 추가 -> 하위 계층 전달`의 빈칸을 채우시오. | A : 단편화(Fragmentation) B : 압축(Compression) C : MAC(Message Authentication Code) 추가 D : 암호화(Encryption). TLS 1.3은 압축을 협상하지 않고 레코드 보호 구조도 달라 이 순서를 일반 TLS 규칙으로 사용하지 않는다. | source-derived from Information Security Tistory; 2026-07-17 version boundary correction |
| 8 | essay | 정보시스템에 관한 전문 지식을 가진 전문가가 익명 설문과 피드백을 여러 차례 반복하여 다양한 위협과 취약성에 대한 합의를 도출하는 위험 분석 기법의 명칭을 쓰시오. | 델파이법(Delphi Method) | source-derived from Information Security Tistory; 2026-07-17 technical wording correction: Delphi is iterative and anonymous, not direct group discussion |
| 9 | short | 정보보호 시스템 공통평가기준(CC)의 빈칸을 채우시오. (A): 특정 소비자 요구에 부합하는 구현 독립적인 보안 요구사항 집합. (B): 식별된 평가대상의 평가 근거로 사용되는 보안 요구사항과 구현 명세의 집합. (C): 공통평가기준에서 미리 정의된 보증 수준을 가지는 보증 컴포넌트 패키지. | A : 보호 프로파일(PP, Protection Profile) B : 보안 목표 명세서(ST, Security Target) C : 평가 보증 등급(EAL, Evaluation Assurance Level) | source-derived from Information Security Tistory; prompt descriptions restored |
| 10 | short | 위험을 구성하는 4가지 기본 요소를 쓰시오. | 자산(Asset), 취약성(Vulnerability), 위협(Threat), 정보보호 대책(Countermeasure) | source-derived from Information Security Tistory; answer block present |
| 11 | short | 전자서명법에 따라 공인인증서의 효력이 소멸하는 4가지 사유를 쓰시오. | (1) 공인인증서의 유효기간이 경과한 경우 (2) 공인인증기관의 지정이 취소된 경우 (3) 공인인증서의 효력이 정지된 경우 (4) 공인인증서가 폐지된 경우 | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 다음 xinetd.conf 설정값의 의미를 각각 서술하시오.<br>{{code:config}}(가) cps = 10 5\n(나) instances = 50\n(다) per_source = 10{{/code}} | (가) 초당 연결 개수를 10개로 제한하고, 10개를 초과하면 5초간 해당 서비스의 신규 연결을 제한한다. (나) 동시에 서비스할 수 있는 서버 프로세스 수를 50개로 제한한다. (다) 동일한 출발지 호스트에서 동시에 접속 가능한 수를 10개로 제한한다. | source-derived from Information Security Tistory; context restored from source text |
| 13 | essay | 다음 유닉스 명령의 의미와 대응하는 공격을 각각 서술하시오.<br>{{code:shell}}(A) ndd -set /dev/ip ip_forward_directed_broadcasts 0\n(B) ndd -set /dev/tcp tcp_conn_req_max_q0 512{{/code}} | (A) Directed Broadcast IP 패킷이 포워드되는 것을 차단하는 명령으로, 스머프(Smurf) 공격을 대응한다.<br>(B) TCP 연결 요청 대기 큐(Backlog Queue)의 크기를 512로 설정하는 명령으로, TCP SYN Flooding 공격을 대응한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction: each command is explicitly mapped to its security purpose; exact official wording unavailable |
| 14 | essay | FTP Active Mode에 답하시오. (1) 서버 20번, 21번 포트의 역할, (2) 클라이언트에서 서버 파일 목록이 보이지 않는 이유, (3) 파일 목록이 보이지 않는 문제를 클라이언트 단에서 해결하는 방법을 서술하시오. | (1) 21번 포트는 제어 채널로 클라이언트가 서버에 초기 접속하고 명령을 전달한다. 20번 포트는 데이터 채널로 서버가 클라이언트의 지정 포트로 직접 접속하여 데이터를 전송한다. (2) Active Mode에서 데이터 채널 형성 시 서버(20/tcp)에서 클라이언트(1024 이상 tcp)로 접속해야 하는데, 클라이언트 측 방화벽이 해당 인바운드 연결을 차단하여 데이터 채널이 형성되지 않기 때문이다. (3) 클라이언트 방화벽에서 FTP 서버(20/tcp)의 인바운드 연결을 허용하거나, FTP 연결 방식을 수동 모드(Passive Mode)로 변경하여 클라이언트가 서버에 데이터 연결을 요청하도록 한다. | source-derived from Information Security Tistory; question prompts restored |
| 15 | essay | 헬스클럽 회원 가입 신청서에서 발생하는 개인정보보호법 위반 사항 2가지와 개선 방안을 서술하시오. | (1) 위반 사항 : 개인의 질병(건강 상태) 등 민감 정보를 수집한다. 개선 방안 : 민감 정보는 원칙적으로 수집을 금지하며, 처리가 불가피한 경우 다른 개인정보와 분리하여 정보주체의 별도 동의를 받아야 한다. (2) 위반 사항 : 법정 대리인의 동의 없이 만 14세 미만 아동의 개인정보를 수집한다. 개선 방안 : 만 14세 미만 아동의 개인정보를 수집할 때는 반드시 법정 대리인의 동의를 받아야 한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다수의 출발지 IP가 단일 목적지 IP의 80번 포트로 SYN 패킷을 대량 전송하는 캡처가 확인되었다. 다음을 답하시오.<br>(A) 의심되는 공격명<br>(B) 서버에서 발생할 수 있는 상황<br>(C) 다음 명령의 빈칸 `(가)`, `(나)`, `(다)`<br>{{code:shell}}iptables -A INPUT -p tcp (가) -m limit (나) (다) DROP{{/code}} | (A) TCP SYN Flooding 공격을 의심한다.<br>(B) SYN backlog 고갈 시 정상 연결이 지연·거부될 수 있다.<br>(C) 예시 완성값은 `(가) --syn --dport 80`, `(나) --limit 10/s`, `(다) -j`이다. 다만 이 한 줄은 **limit에 매치한 패킷을 DROP**하므로 초과 패킷만 차단하는 완전한 rate limit이 아니다. 허용률을 먼저 ACCEPT하고 다음 규칙에서 DROP하거나 `hashlimit`/SYN proxy 등 정책을 함께 구성해야 한다. | source-derived from Information Security Tistory; 2026-07-18 prompt-format correction preserves the 2026-07-17 warning: the example completion alone is not a complete excess-rate blocking policy; exact official wording unavailable |

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

- `raw/sources/clipping/f2a6224b03411c630150eea487dc7306ab28866f83e47d0737532d1052788786/cd4f74a4769f3740eedd9855046e8879345e12fefb8eddecf0ca521aa1f4a485/manifest.json`
