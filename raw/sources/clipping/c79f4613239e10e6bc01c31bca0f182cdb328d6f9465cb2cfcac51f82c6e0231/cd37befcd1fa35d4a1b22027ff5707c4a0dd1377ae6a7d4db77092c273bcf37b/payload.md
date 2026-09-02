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
| 11 | essay | `[IP 헤더][TCP 헤더][데이터]` 패킷을 ESP 터널모드로 전송하는 경우 답하시오. (1) 추가되는 필드를 도식화하시오. (2) 암호화되는 필드의 범위를 설명하시오. (3) 인증되는 필드의 범위를 설명하시오. | New IP header와 ESP header/trailer/authentication data가 추가된다. 원래 IP 패킷 전체와 ESP trailer는 암호화되며, 무결성·출처 인증 서비스를 선택한 ESP SA에서는 ESP header·암호화된 payload·trailer가 인증 범위가 된다. Authentication Data 필드 자체는 그 계산 범위에 포함되지 않는다. | Naver text extracted; 2026-07-17 technical correction: ESP authentication is SA-dependent and excludes its own auth data |
| 12 | essay | 백도어가 설치된 것을 다음으로 확인했으나 해당 파일 경로에는 파일이 존재하지 않았다. `ls -al /proc/5900` 결과는 `exe -> 백도어경로(delete)`이다. (1) 백도어 파일 경로에서 해당 프로세스가 보이지 않는 이유는? (2) 삭제된 백도어 프로세스를 `/tmp/backdoor`로 복원하는 명령어는? (3) `ps`가 변조되어 사용 불가할 때 공격자가 사용한 명령어를 확인하는 방법은? | (1) 실행 후 파일을 삭제했을 수 있다. (2) `cp /proc/5900/exe /tmp/backdoor`. (3) `history` 또는 `cat /proc/5900/cmdline`로 명령과 인자를 확인한다. 단, 해당 PID가 살아 있고 `/proc/5900/exe`를 읽을 권한이 있다는 조건이 필요하다. | PDF compilation cross-check restored the complete prompt and answer choices; this is a non-official blog compilation, not KCA wording. |
| 13 | essay | 정보통신망법 적용을 받는 신생회사가 비밀번호 작성 규칙을 수립하려고 한다. 개인정보의 기술적·관리적 보호조치 기준에 따른 비밀번호 작성 규칙 3가지를 설명하시오. | 복잡도·길이, 추측 어려운 비밀번호, 유효기간/주기적 변경 등 | Naver text extracted; current-law wording needs check |
| 14 | practical | 백업 스크립트는 `tar -cvzf /data/backup/etc_$dat.tgz /etc/*`, `tar -cvzf /data/backup/home_$dat.tgz /home/*`를 수행하고, 결과 파일 권한은 `rw-r--r-- root root /data/backup/etc_YYYYMMDD.tgz`, `rw-r--r-- root root /data/backup/home_YYYYMMDD.tgz`이다. (1) 권한 문제를 설명하시오. (2) `umask` 변경 후 백업 파일을 생성하고 원래대로 만드는 스크립트를 작성하시오. (3) operator 사용자만 `/usr/local/bin/backup`을 사용하도록 만드는 명령어와 의미를 쓰시오. | 백업 파일은 world-readable이므로 민감 내용 노출 위험이 있다. 생성 전 기존 umask를 저장한 뒤 `umask 077`으로 파일을 소유자만 읽고 쓰게 생성하고 원래 값으로 복원한다. `umask 266`은 일반적인 0666 파일 생성 모드에서 0400이 될 수 있어 0600을 의도한 설정으로 적절하지 않다. 실행 파일은 `chown operator /usr/local/bin/backup`과 `chmod 700 /usr/local/bin/backup`으로 operator만 실행하도록 제한할 수 있다. | Naver text extracted; 2026-07-17 technical correction: umask calculation |
| 15 | practical | HTTP Request 패킷 캡처 화면에서 `POST / HTTP/1.1`, `content-length: 1000000`이 보이고, 다른 화면에서 `TCP segment data (1 byte)`로 1바이트씩 분할 전송되는 상황이다. (1) 어떤 공격인가? (2) 판단 근거를 구체적으로 설명하시오. (3) 서버 측 대응 방안 2가지를 설명하시오. | Slow HTTP POST DoS(RUDY). 큰 body 길이와 저속 전송으로 연결을 장시간 점유하며 connection/read timeout, 동시연결 제한, 방화벽 임계치로 대응 | Naver text extracted; official wording unverified |
| 16 | practical | A시 어르신 교통카드 신청서 안내문에서 개인정보보호법 위반 사항 4가지를 찾으시오. (1) 수집·이용(필수): 주민등록번호 포함, 목적 본인확인, 기간 영구보관, 동의 거부 권리·불이익 고지는 있음. (2) 제3자 제공: 제공기관 유관기관, 주민등록번호 포함, 목적·기간은 교통카드 만료 시까지. (3) 위탁: 위탁기관 OO신용카드, 위탁업무 교통카드 발급업무. (4) 위 세 항목에 대한 동의 확인을 요청한다. | PDF 편집본의 제시 답안은 (a) 주민등록번호 수집·제3자 제공의 법정 근거 부재, (b) 영구 보관, (c) 제3자 제공 동의 거부권 및 거부에 따른 불이익 고지 누락, (d) 제3자 제공 기관 명칭 불명확이다. 법령 문구·적용 기준은 시험 당시 법령 대조가 필요하며 현행 기준으로 치환하지 않는다. | PDF compilation cross-check restored the complete form and answer points. This is a non-official blog compilation, not KCA wording; legal correctness remains time-bounded. |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
