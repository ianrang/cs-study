---
title: "정보보안기사 실기 9회 2017년 1회 실기 복원"
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
  - "https://information-security.tistory.com/274"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 9회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 9회 2017년 1회 실기 복원

## Scope
- Exam mapping: 2017년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 운영체제별로 경로는 다르지만 DNS 정보를 담고 있으며, Windows 7 이상에서는 관리자 외 수정이 제한되는 파일의 이름을 쓰시오. | hosts | source-derived from Information Security Tistory; answer block present |
| 2 | short | 스머프(Smurf) 공격 과정이다. 빈칸 (A), (B), (C)를 채우시오. | A : Echo Request B : Echo Reply C : Directed Broadcast | source-derived from Information Security Tistory; answer block present |
| 3 | short | 버퍼 오버플로우의 유형에 관한 설명이다. 빈칸 (A), (B)를 채우시오. | A : 스택 버퍼 오버플로우(Stack Buffer Overflow) B : 힙 버퍼 오버플로우(Heap Buffer Overflow) | source-derived from Information Security Tistory; answer block present |
| 4 | short | Trustwave사가 개발하여 Apache 웹 서버와 IIS에서 사용 가능한 공개용 웹 방화벽(WAF)의 명칭을 쓰시오. | ModSecurity | source-derived from Information Security Tistory; answer block present |
| 5 | essay | 다음은 단편화된 tcpdump 패킷 정보이다. 각 항목이 의미하는 바를 서술하시오. | A : Fragment ID (단편화 식별자) - 같은 원본 패킷에서 분리된 단편임을 나타내는 ID B : Size (단편의 크기) - 해당 단편의 데이터 크기(1480바이트) C : Offset (오프셋) - 원본 패킷에서 해당 단편이 시작되는 위치(2920바이트 지점) | source-derived from Information Security Tistory; answer block present |
| 6 | short | 정보통신망 이용촉진 및 정보보호 등에 관한 법률 제23조의2에 관한 설명이다. 빈칸 (a), (b)를 채우시오. | a : 본인확인기관 b : 대체수단 | source-derived from Information Security Tistory; answer block present |
| 7 | short | SSL/TLS 레코드 프로토콜이 메시지를 암호화하여 통신하는 처리 과정이다. 빈칸 (A), (B), (C), (D)를 순서대로 채우시오. | A : 단편화(Fragmentation) B : 압축(Compression) C : MAC(Message Authentication Code) 추가 D : 암호화(Encryption) | source-derived from Information Security Tistory; answer block present |
| 8 | essay | 정보시스템에 관한 전문 지식을 가진 전문가 집단이 다양한 위협과 취약성을 토론으로 분석하는 위험 분석 기법의 명칭을 쓰시오. | 델파이법(Delphi Method) | source-derived from Information Security Tistory; answer block present |
| 9 | short | 정보보호 시스템 공통평가기준(CC)에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 보호 프로파일(PP, Protection Profile) B : 보안 목표 명세서(ST, Security Target) C : 평가 보증 등급(EAL, Evaluation Assurance Level) | source-derived from Information Security Tistory; answer block present |
| 10 | short | 위험을 구성하는 4가지 기본 요소를 쓰시오. | 자산(Asset), 취약성(Vulnerability), 위협(Threat), 정보보호 대책(Countermeasure) | source-derived from Information Security Tistory; answer block present |
| 11 | short | 전자서명법에 따라 공인인증서의 효력이 소멸하는 4가지 사유를 쓰시오. | (1) 공인인증서의 유효기간이 경과한 경우 (2) 공인인증기관의 지정이 취소된 경우 (3) 공인인증서의 효력이 정지된 경우 (4) 공인인증서가 폐지된 경우 | source-derived from Information Security Tistory; answer block present |
| 12 | essay | 다음 xinetd.conf 설정값의 의미를 각각 서술하시오. | (가) 초당 연결 개수를 10개로 제한하고, 10개를 초과하면 5초간 해당 서비스의 신규 연결을 제한한다. (나) 동시에 서비스할 수 있는 서버 프로세스 수를 50개로 제한한다. (다) 동일한 출발지 호스트에서 동시에 접속 가능한 수를 10개로 제한한다. | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 다음 유닉스 ndd 명령어의 의미와 대응하는 공격을 각각 서술하시오. | (1) Directed Broadcast IP 패킷이 포워드되는 것을 차단하는 명령으로, 스머프(Smurf) 공격을 대응한다. (2) TCP 연결 요청 대기 큐(Backlog Queue)의 크기를 512로 설정하는 명령으로, TCP SYN Flooding 공격을 대응한다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | FTP Active Mode(능동 모드)에 관한 물음에 답하시오. | (1) 21번 포트는 제어 채널로 클라이언트가 서버에 초기 접속하고 명령을 전달한다. 20번 포트는 데이터 채널로 서버가 클라이언트의 지정 포트로 직접 접속하여 데이터를 전송한다. (2) Active Mode에서 데이터 채널 형성 시 서버(20/tcp)에서 클라이언트(1024 이상 tcp)로 접속해야 하는데, 클라이언트 측 방화벽이 해당 인바운드 연결을 차단하여 데이터 채널이 형성되지 않기 때문이다. (3) 클라이언트 방화벽에서 FTP 서버(20/tcp)의 인바운드 연결을 허용하거나, FTP 연결 방식을 수동 모드(Passive Mode)로 변경하여 클라이언트가 서버에 데이터 연결을 요청하도록 한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 헬스클럽 회원 가입 신청서에서 발생하는 개인정보보호법 위반 사항 2가지와 개선 방안을 서술하시오. | (1) 위반 사항 : 개인의 질병(건강 상태) 등 민감 정보를 수집한다. 개선 방안 : 민감 정보는 원칙적으로 수집을 금지하며, 처리가 불가피한 경우 다른 개인정보와 분리하여 정보주체의 별도 동의를 받아야 한다. (2) 위반 사항 : 법정 대리인의 동의 없이 만 14세 미만 아동의 개인정보를 수집한다. 개선 방안 : 만 14세 미만 아동의 개인정보를 수집할 때는 반드시 법정 대리인의 동의를 받아야 한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음은 TCP SYN Flooding 공격과 관련된 물음이다. 답하시오. | (1) TCP SYN Flooding 공격 (2) 서버의 TCP 연결 요청 대기 큐(Backlog Queue)가 가득 차서 정상적인 사용자의 연결 요청을 처리하지 못해 서비스 지연 또는 서비스 거부 상태가 발생한다. (3) (가) : --dport 80 (나) : --limit 10/s (다) : -j | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
