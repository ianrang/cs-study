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
date_updated: 2026-07-06
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
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.
- Note: ITWiki practical section has several blank items; Naver reconstruction was used to fill missing prompts and answer summaries.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 웹 취약점 설명과 점검 스크립트 빈칸이다. (A)는 게시판, 웹 메일 등에 삽입된 악의적인 스크립트에 의해 페이지가 깨지거나 다른 사용자의 사용을 방해하거나 쿠키 및 기타 개인정보를 특정 사이트로 전송시키는 공격이다. 점검 스크립트는 `<script> (B)(document.cookie) </script>`이다. | XSS, alert | Naver text extracted; official wording unverified |
| 2 | short | 웹 로봇 Agent의 크롤링을 제한하는 파일명. | `robots.txt` | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | 출발지/목적지 IP 동일, ICMP broadcast, SYN 다량 전송 DoS 공격기법. | Land Attack, Smurf Attack, TCP SYN Flooding | source-derived; Naver cross-checked; official wording unverified |
| 4 | short | UDP 1900 포트와 IoT 시스템을 악용하는 reflection 공격. | SSDP DRDoS | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | (A)는 오픈소스 IDS/IPS로 기존의 (B)의 장점을 수용하고, 대용량 트래픽을 실시간으로 처리하는 데 특화된 소프트웨어이다. 빈칸을 채우시오. | Suricata, Snort | Naver text extracted; official wording unverified |
| 6 | short | 개인정보의 안전성 확보조치 기준 제8조 접속기록의 보관 및 점검에 관한 빈칸을 채우시오. 개인정보처리자는 접속기록을 1년 이상 보관·관리해야 하며, 5만명 이상의 정보주체에 관한 개인정보를 처리하거나 (A) 또는 (B)를 처리하는 개인정보처리시스템은 2년 이상 보관·관리해야 한다. 개인정보 다운로드가 발견된 경우에는 (C)으로 정하는 바에 따라 사유를 확인해야 한다. | 고유식별정보, 민감정보, 내부관리계획 | Naver text extracted; current-law wording needs check |
| 7 | short | TLS 연결을 SSL 3.0으로 낮춰 암호문을 해독하는 공격. | POODLE 공격 | source-derived; Naver cross-checked; official wording unverified |
| 8 | short | ISMS-P 인증 체계에서 빈칸을 채우시오. (A)는 과학기술정보통신부, 행정안전부와 함께 정책협의회를 구성하여 법·제도 개선, 정책 결정, 인증기관 및 심사기관 지정 업무를 수행한다. (B)는 인증서 발급, 인증심사원 양성 및 자격관리 업무를 수행한다. (C)는 인증심사 결과에 대한 심의·의결을 수행한다. | 방송통신위원회, KISA, 인증위원회 | Naver text extracted; current governance wording needs check |
| 9 | short | 자산 및 시스템 위험을 평가하고 수용 가능한 수준으로 완화하는 과정. | 위험관리 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | VPN 관련 프로토콜명 빈칸을 채우시오. (A)는 Cisco가 개발한 터널링 프로토콜로 데이터 링크층에서 캡슐화 가능하다. (B)는 MS, 3Com 등 여러 회사가 공동 개발한 프로토콜이다. (C)는 OSI 3계층에서 보안성을 제공하는 표준 프로토콜이다. | L2F, PPTP, IPSec | Naver text extracted; official wording unverified |
| 11 | essay | `[IP 헤더][TCP 헤더][데이터]` 패킷을 ESP 터널모드로 전송하는 경우 답하시오. (1) 추가되는 필드를 도식화하시오. (2) 암호화되는 필드의 범위를 설명하시오. (3) 인증되는 필드의 범위를 설명하시오. | New IP header와 ESP header/trailer/auth가 추가되며 원 IP packet과 ESP trailer가 암호화되고 ESP header부터 trailer까지 인증된다. | Naver text extracted; official wording unverified |
| 12 | essay | 백도어 설치를 `/proc/5900`에서 확인했으나 해당 파일 경로에는 파일이 존재하지 않고, `exe -> 백도어경로(delete)`로 표시된다. (1) 백도어 파일 경로 접속 시 해당 프로세스가 보이지 않는 이유는? (2) 삭제된 백도어 프로세스를 `/tmp/backdoor`로 복원하는 명령어는? (3) `ps`가 변조되어 사용 불가할 때 공격자가 사용한 명령어를 확인하는 방법은? | 실행 후 파일을 삭제했기 때문이며 `cp /proc/5900/exe /tmp/backdoor`로 복원하고 history 또는 `cat /proc/5900/cmdline`으로 실행 명령을 확인 | Naver text extracted; exact official wording unverified |
| 13 | essay | 정보통신망법 적용을 받는 신생회사가 비밀번호 작성 규칙을 수립하려고 한다. 개인정보의 기술적·관리적 보호조치 기준에 따른 비밀번호 작성 규칙 3가지를 설명하시오. | 복잡도·길이, 추측 어려운 비밀번호, 유효기간/주기적 변경 등 | Naver text extracted; current-law wording needs check |
| 14 | practical | 백업 스크립트는 `tar -cvzf /data/backup/etc_$dat.tgz /etc/*`, `tar -cvzf /data/backup/home_$dat.tgz /home/*`를 수행하고, 결과 파일 권한은 `rw-r--r-- root root /data/backup/etc_YYYYMMDD.tgz`, `rw-r--r-- root root /data/backup/home_YYYYMMDD.tgz`이다. (1) 권한 문제를 설명하시오. (2) `umask` 변경 후 백업 파일을 생성하고 원래대로 만드는 스크립트를 작성하시오. (3) operator 사용자만 `/usr/local/bin/backup`을 사용하도록 만드는 명령어와 의미를 쓰시오. | 백업 파일 world-readable 문제를 지적하고 `umask 266` 적용 후 원복, `chown operator`와 `chmod 700`으로 스크립트 실행 주체 제한 | Naver text extracted; exact shell wording unverified |
| 15 | practical | HTTP Request 패킷 캡처 화면에서 `POST / HTTP/1.1`, `content-length: 1000000`이 보이고, 다른 화면에서 `TCP segment data (1 byte)`로 1바이트씩 분할 전송되는 상황이다. (1) 어떤 공격인가? (2) 판단 근거를 구체적으로 설명하시오. (3) 서버 측 대응 방안 2가지를 설명하시오. | Slow HTTP POST DoS(RUDY). 큰 body 길이와 저속 전송으로 연결을 장시간 점유하며 connection/read timeout, 동시연결 제한, 방화벽 임계치로 대응 | Naver text extracted; official wording unverified |
| 16 | practical | OOO 시 어르신 교통카드 신청서 안내문에서 개인정보보호법 위반 사항 4가지를 찾으시오. 필수 수집·이용 항목에는 주민등록번호 포함, 목적은 본인확인, 기간은 영구보관이며 동의 거부 권리 및 불이익은 명시되어 있다. 제3자 제공은 유관기관에 주민등록번호 포함 정보를 교통카드 만료 시까지 제공하며, 위탁기관은 OO신용카드이고 위탁업무는 교통카드 발급업무이다. | 주민등록번호 수집·제공 근거, 영구보관, 제3자 제공 동의거부 고지 누락, 제공 기관명 불명확 등을 지적 | Naver text extracted; current-law wording needs check |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
