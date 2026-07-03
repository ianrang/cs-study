---
title: "정보보안기사 실기 15회 2020년 1회 실기 복원"
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
  - "https://itwiki.kr/w/정보보안기사_15회"
  - "https://blog.naver.com/stereok2/222051462751"
source_count: 2
provenance: inferred
summary: "정보보안기사 실기 15회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 15회 2020년 1회 실기 복원

## Scope
- Exam mapping: 2020년 1회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.
- Note: ITWiki practical section has several blank items; Naver reconstruction was used to fill missing prompts and answer summaries.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 웹 취약점 설명과 점검 스크립트 빈칸. | XSS, alert | source-derived; Naver cross-checked; official wording unverified |
| 2 | short | 웹 로봇 Agent의 크롤링을 제한하는 파일명. | `robots.txt` | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | 출발지/목적지 IP 동일, ICMP broadcast, SYN 다량 전송 DoS 공격기법. | Land Attack, Smurf Attack, TCP SYN Flooding | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | UDP 1900 포트와 IoT 시스템을 악용하는 reflection 공격. | SSDP DRDoS | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | Snort 장점을 수용한 오픈소스 IDS/IPS와 원형 엔진. | Suricata, Snort | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | 개인정보 안전성 확보조치 기준의 접속기록 보관·점검 빈칸. | 고유식별정보, 민감정보, 내부관리계획 | source-derived; Naver cross-checked; current-law wording needs check |
| 7 | short | TLS 연결을 SSL 3.0으로 낮춰 암호문을 해독하는 공격. | POODLE 공격 | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | ISMS-P 인증 체계의 정책·인증서 발급·심의 주체. | 방송통신위원회, KISA, 인증위원회 | source-derived; Naver cross-checked; current governance wording needs check |
| 9 | short | 자산 및 시스템 위험을 평가하고 수용 가능한 수준으로 완화하는 과정. | 위험관리 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | VPN 프로토콜 설명 빈칸. | L2F, PPTP, IPSec | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | ESP 터널모드에서 추가 필드, 암호화 범위, 인증 범위. | New IP header와 ESP header/trailer/auth가 추가되며 원 IP packet과 ESP trailer가 암호화되고 ESP header부터 trailer까지 인증된다. | source-derived; Naver cross-checked; official wording unverified |
| 12 | essay | 삭제된 백도어 프로세스의 이유, 복원 명령, 실행 명령 확인 방법. | 실행 후 파일을 삭제했기 때문이며 `/proc/<pid>/exe`를 복사해 복원하고 history 또는 `/proc/<pid>/cmdline`으로 실행 명령을 확인 | source-derived; Naver cross-checked; exact pid/path wording unverified |
| 13 | essay | 개인정보 기술적·관리적 보호조치 기준의 비밀번호 작성 규칙. | 복잡도·길이, 추측 어려운 비밀번호, 유효기간/주기적 변경 등 | source-derived; Naver cross-checked; current-law wording needs check |
| 14 | practical | 백업 파일 권한 문제와 umask, operator 전용 실행 설정. | 백업 파일 world-readable 문제를 지적하고 `umask 266` 적용 후 원복, `chown operator`와 `chmod 700`으로 스크립트 실행 주체 제한 | source-derived; Naver cross-checked; exact shell wording unverified |
| 15 | practical | 큰 Content-Length와 1바이트 분할 전송 패킷의 공격명, 판단근거, 서버 대응. | Slow HTTP POST DoS(RUDY). 큰 body 길이와 저속 전송으로 연결을 장시간 점유하며 connection/read timeout, 동시연결 제한, 방화벽 임계치로 대응 | source-derived; Naver cross-checked; official wording unverified |
| 16 | practical | 교통카드 신청서 안내문의 개인정보보호법 위반 항목. | 주민등록번호 수집·제공 근거, 영구보관, 제3자 제공 동의거부 고지 누락, 제공 기관명 불명확 등을 지적 | source-derived; Naver cross-checked; current-law wording needs check |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
