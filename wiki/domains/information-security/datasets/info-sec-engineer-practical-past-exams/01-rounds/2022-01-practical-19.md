---
title: "정보보안기사 실기 19회 2022년 1회 실기 복원"
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
  - "https://nhustler.tistory.com/40"
  - "https://nhustler.tistory.com/41"
  - "https://blog.naver.com/stereok2/222723288429"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 19회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 19회 2022년 1회 실기 복원

## Scope
- Exam mapping: 2022년 1회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 위험을 구성하는 요소의 빈칸을 채우시오. (A): 조직이 보호해야 할 대상으로 정보, 하드웨어, 소프트웨어, 시설, 관련 인력, 기업 이미지 같은 무형자산을 포함한다. (B): (A)에 손실을 초래할 수 있는 원치 않는 사건의 잠재적 원인 또는 행위자다. (C): (B)에 의해 손실이 발생하게 되는 (A)에 내재된 약점이다. | 자산, 위협, 취약점 | source-derived; PDF compilation cross-check restored prompt condition |
| 2 | short | 네트워크 진입 시 단말과 사용자를 인증하고, 단말에 대한 지속적인 보안 취약점 점검과 통제를 통해 내부 시스템을 보호하는 솔루션을 쓰시오. | NAC(Network Access Control) | source-derived; PDF compilation cross-check restored prompt condition |
| 3 | short | 여러 프로세스가 공유자원에 동시에 접근할 때 접근 순서에 따라 비정상 결과가 발생하는 상황을 악용하는 공격기법을 쓰시오. | Race Condition 공격 | source-derived; PDF compilation cross-check restored prompt condition |
| 4 | short | Victim의 MAC 주소를 위조하여 해당 IP로 전달되는 데이터를 중간에서 가로채는 공격 기법을 쓰시오. | ARP Spoofing | source-derived; PDF compilation cross-check restored prompt condition |
| 5 | short | IDS는 네트워크 패킷만 보고 공격을 탐지하는 (A) IDS와, 서버에 직접 설치되어 관리자 권한 탈취 등으로 발생하는 공격을 탐지하는 (B) IDS로 구분된다. 빈칸을 채우시오. | 네트워크 기반 IDS, 호스트 기반 IDS | source-derived; PDF compilation cross-check restored prompt condition |
| 6 | short | BCP 수립 시 장애·재해로 업무 프로세스가 중단되는 경우 예상 재무 손실, 외부 규제 요건 등을 고려해 업무 중요도를 평가하고 RTO와 RPO를 결정하는 절차를 쓰시오. | BIA(Business Impact Analysis, 업무영향도 분석) | source-derived; PDF compilation cross-check restored prompt condition |
| 7 | short | Apache 로그의 빈칸을 채우시오. 정상적인 접속 로그가 기록되는 (A) 로그, 접속 에러가 기록되는 (B) 로그가 있으며, 로그 파일 경로를 확인할 수 있는 파일은 (C)이다. | access log, error log, httpd.conf | source-derived; PDF compilation cross-check restored prompt condition |
| 8 | short | 필 짐머만이 개발했으며 PEM보다 보안성은 떨어지나 구현 프로그램이 공개되어 현재 많이 사용되는 이메일 보안 기술을 쓰시오. | PGP(Pretty Good Privacy) | source-derived; PDF compilation cross-check restored prompt condition |
| 9 | short | 위험평가 수행 시 자산을 식별하고, 식별된 자산의 가치를 CIA(기밀성·무결성·가용성) 측면에서 평가하여 산정하는 값을 쓰시오. | 자산 중요도 | source-derived; PDF compilation cross-check restored prompt condition |
| 10 | short | 공격자가 사용자와 서버 간 이미 활성화된 세션을 가로채 사용자의 신원으로 서버와 통신을 시도하는 공격 기법을 쓰시오. | 세션 하이재킹 | source-derived; PDF compilation cross-check restored prompt condition |
| 11 | essay | 특수비트와 관련하여 다음 각 항목에 설정된 접근권한의 의미를 설명하시오. (1) `-r-sr-xr-x root sys /etc/chk/passwd` (2) `-r-xr-sr-x root mail /etc/chk/mail` (3) `drwxrwxrwt sys sys /tmp` | setuid는 소유자 권한 실행, setgid는 그룹 권한 실행, sticky bit는 공용 디렉터리에서 소유자/root 외 삭제 제한 | source-derived; Naver text extracted; official wording unverified |
| 12 | essay | 공공기관에서 개인정보처리방침 수립 시 포함해야 할 사항을 4가지 이상 쓰고, 수립된 개인정보처리방침을 알리는 방법을 3가지 이상 쓰시오. | 처리 목적·보유기간·제3자 제공·파기·위탁·정보주체 권리·책임자 연락처 등과 홈페이지/사업장 게시/관보·신문/간행물/계약서 고지 | source-derived; Naver text extracted; legal wording needs current-law check |
| 13 | essay | 로그 `device eth0 entered Promiscuous mode`에 대하여 답하시오. (1) Promiscuous mode의 의미는? (2) 해당 모드로 진입 시 수행 가능한 공격은? (3) 공격에 대응할 수 있는 방법을 1가지 이상 설명하시오. | NIC가 목적지가 아닌 패킷도 수신하는 모드이며 스니핑이 가능하다. 암호화 통신, promisc 해제, 스위치 운용 등으로 대응 | source-derived; Naver text extracted; official wording unverified |
| 14 | practical | 정보 자산 구성도와 자산목록을 보고 자산 식별 문제점 1개와 보안 취약 문제점 1개를 설명하시오. 구성도: 인터넷과 내부망 사이 방화벽으로 DMZ를 구성하고 web/mail 서버를 배치, web 서버 앞단에 웹방화벽 배치, 내부망은 방화벽으로 업무망·VDI망·서버망 Farm 분리, 서버망에는 dns/db/was/개발 서버가 위치. 자산목록: db서버 OS AIX 6.4 호스트명 krserver1 관리책임자 홍과장, was서버 OS AIX 8.0 호스트명 krserver1 관리책임자 김부장, dns서버 OS AIX 6.4 호스트명 dns_srv 관리책임자 홍대리, web서버 OS Windows 2003 호스트명 web1 관리책임자 김부장, mail서버 OS CentOS 7 호스트명 krmail01 관리책임자 김사원. | 개발 서버 누락 같은 자산 식별 누락과 중복 호스트명/노후 OS 등 보안 취약점을 지적 | source-derived; Naver text extracted; official wording unverified |
| 15 | practical | 파일 업로드 취약점 대응을 위한 `.htaccess` 설정의 의미를 설명하시오. (1) `<FilesMatch \.(ph\|lib\|sh\|)> Order Allow DENY; Deny From ALL; </FilesMatch>` (2) `AddType text/html .php .php1 .php2 .php3 .php4 .phtml` | 실행 차단, 특정 확장자 제한, MIME/Handler 제거 등 업로드 파일 실행 방지 설정 | source-derived; Naver text extracted; official wording unverified |
| 16 | practical | 위험평가서 양식과 관련하여 답하시오. 위험평가서 양식 열은 자산명, 자산 중요도(C/I/A), 우려사항, 가능성, 위험도(C/I/A)이다. 행1은 ERP데이터, 중요도 H/H/M, 우려사항 "DB의 접근 통제 위반이나 위반 시도를 적시에 발견하여 처리할 수 없다", 가능성 H, 위험도 H/H/M이다. 행2는 워드문서, 중요도 L/L/L, 우려사항 "적절한 보안 규정이 부족하여 자산이 제대로 보호되지 않을 수 있음", 가능성 M, 위험도 L/L/L이다. (1) 자산 중요도 평가의 목적은? (2) 우려사항이란 무엇인가? (3) 가능성이란 무엇인가? (4) ERP데이터·ERP서버·워드문서 자산 평가 테이블을 보고 위험분석기법을 적용하여 위험분석을 수행하시오. | CIA 기반 중요도 산정으로 통제 우선순위를 정하고 우려사항·발생가능성을 반영해 위험도와 대응 우선순위를 결정 | source-derived; Naver text extracted; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
