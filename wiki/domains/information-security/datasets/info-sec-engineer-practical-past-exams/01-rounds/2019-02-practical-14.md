---
title: "정보보안기사 실기 14회 2019년 2회 실기 복원"
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
  - "https://blog.naver.com/stereok2/221751404526"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 14회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 14회 2019년 2회 실기 복원

## Scope
- Exam mapping: 2019년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 접근통제 정책 모델에 관한 설명이다. (A)는 모든 객체가 정보의 비밀 수준에 근거한 보안 레벨을 가지며 허가된 사용자만 접근 가능하도록 제어하는 모델이다. (B)는 사용자나 사용자 그룹에 근거한 사용자 중심 접근 제어 모델이다. (C)는 사용자와 객체의 상호 관계를 역할로 구분하여 접근 제어하는 모델이다. 빈칸을 채우시오. | MAC, DAC, RBAC | Naver text extracted; official wording unverified |
| 2 | short | ARP 프로토콜에서 목적지의 물리 주소를 얻기 위해 프레임에 실어 보내는 목적지 주소를 주소 형식에 맞게 쓰시오. | ff:ff:ff:ff:ff:ff | Naver text extracted; official wording unverified |
| 3 | short | IPSec 프로토콜에 대하여 답하시오. (1) 어느 계층에서 사용되는 프로토콜인가? (A) (2) 무결성을 보장하는 IPSec 세부 프로토콜은? (B) (3) 기밀성을 보장하는 IPSec 세부 프로토콜은? (C) | 네트워크 계층, AH, ESP | Naver text extracted; official wording unverified |
| 4 | short | MS 오피스와 애플리케이션 사이에서 데이터를 전달하는 데 사용되는 프로토콜로 외부로 데이터 등을 전달할 수 있으며, 엑셀에서 이 기능이 활성화될 경우 악용될 수 있는 프로토콜명을 쓰시오. | DDE(Dynamic Data Exchange) | Naver text extracted; official wording unverified |
| 5 | short | 사이버위기 경보 단계 `정상 -> (A) -> 주의 -> (B) -> (C)`에서 빈칸에 알맞은 단계별 명칭을 쓰시오. | 관심, 경계, 심각 | Naver text extracted; official wording unverified |
| 6 | short | 리눅스 시스템 로그 파일에 관한 설명이다. (A)는 현재 시스템에 로그인한 사용자의 상태가 출력되는 로그이다. (B)는 사용자의 로그인, 로그아웃, 시스템 재부팅 정보가 출력되는 로그이다. (C)는 5번 이상 로그인 실패 시 로그인 실패 정보가 기록되는 로그이다. 빈칸을 채우시오. | utmp, wtmp, btmp | Naver text extracted; official wording unverified |
| 7 | short | 정보보호제품 평가를 위한 국제 공통 기준의 명칭을 쓰시오. | CC(Common Criteria) 기반 평가·인증 | Naver text extracted; 2026-07-17 wording correction: CC is the evaluation criteria, not a standalone generic certificate name |
| 8 | short | `httpd.conf` 파일에서 디렉터리에 업로드 가능한 최대 파일 사이즈를 제한하는 지시자를 쓰시오. | LimitRequestBody | Naver text extracted; official wording unverified |
| 9 | short | 정보보호 관련 법률 명칭을 쓰시오. (A) 정보통신망에 관한 법률의 명칭 (B) 주요 정보통신 기반 시설에 관한 법률의 명칭 (C) 위치정보에 관한 법률의 명칭 | 정보통신망법, 정보통신기반보호법, 위치정보법 | Naver text extracted; legal wording needs current-law check |
| 10 | short | ISMS-P 인증 평가 항목에 관한 설명이다. `1.2.1 정보자산 식별`은 정보자산을 식별·분류하고 (A)를 산정한 후 목록을 최신으로 관리하도록 한다. `1.2.3 위험평가`는 대내외 환경분석을 통해 유형별 (B)를 수집하고, 연 1회 이상 위험평가 후 수용할 수 있는 위험은 (C)의 승인을 받아 관리하도록 한다. | 중요도, 위협 정보, 경영진 | Naver text extracted; official wording unverified |
| 11 | essay | 유닉스 계정 패스워드 임곗값 설정 옵션 `deny=5`, `unlock_time=120`, `no_magic_root`, `reset`의 의미를 설명하시오. | deny=5는 5회 실패 시 잠금, unlock_time=120은 120초 후 해제, no_magic_root는 root 예외, reset은 성공 시 실패 횟수 초기화 | Naver text extracted; official wording unverified |
| 12 | essay | `/etc/shadow` 파일에 대하여 답하시오. (1) `x:a$b$c:`에서 a, b, c의 의미는? (2) b가 레인보우테이블 공격에 대응할 수 있는 이유는? (3) `pwunconv` 명령의 기능은? | a는 해시 알고리즘, b는 salt, c는 해시값이다. salt로 레인보우테이블 공격을 완화하며, pwunconv는 shadow 비밀번호를 passwd로 되돌리고 shadow를 비활성화한다 | Naver text extracted; official wording unverified |
| 13 | essay | 강제적 접근제어 모델에 대하여 답하시오. (1) 정보의 불법적 파괴나 변조보다 기밀성 유지에 초점을 둔 모델명은? (2) no-read-up의 의미는? (3) no-write-down의 의미와 보안적 관점에서의 의의는? (4) Biba 모델의 write 정책은? | 기밀성 중심 모델은 BLP이며 no-read-up은 낮은 등급 주체의 높은 등급 객체 읽기 금지, no-write-down은 높은 등급 주체의 낮은 등급 객체 쓰기 금지, Biba write 정책은 no-write-up이다 | Naver text extracted; official wording unverified |
| 14 | essay | A 시스템에서 B 시스템으로 ACK 패킷을 2012~2018 포트까지 전송하여 2017 포트에서 RST 응답이 도착하였다. (1) 무슨 스캔인가? (2) 스캔의 목적은? (3) 본 스캔을 통하여 무엇을 알 수 있는가? | TCP ACK 스캔이며 방화벽 필터링 여부 확인이 목적이다. RST가 온 2017 포트는 필터링되지 않고, 무응답 포트는 필터링되는 것으로 판단한다 | Naver text extracted; official wording unverified |
| 15 | essay | Apache 설정 옵션의 의미를 설명하시오. (1) `Timeout 300` (2) `MaxKeepAliveRequests 100` (3) `DirectoryIndex index.htm, index.html, index.php` (4) `ErrorLog "경로"` | Timeout 300은 300초 무응답 시 연결 종료, MaxKeepAliveRequests 100은 KeepAlive 연결당 최대 요청 수, DirectoryIndex는 기본 인덱스 파일 순서, ErrorLog는 오류 로그 경로를 의미한다 | Naver text extracted; official wording unverified |
| 16 | essay | XSS 공격 탐지 Snort 룰 `alert tcp any any -> any 80 (msg:"XSS"; content:"GET"; offset:1; depth:3; content:"/login.php<script>XSS"; distance:1;)`에 대하여 답하시오. (1) `content:"GET"; offset:1; depth:3`의 의미는? (2) `content:"/login.php<script>XSS"; distance:1`의 의미는? (3) 바이너리로 전송된 패킷에서 `Login`의 L이 대문자라 위 룰로 탐지되지 않을 경우 수정 방법은? | offset은 검색 시작 위치, depth는 그 위치 기준 검색 범위이며, 패킷 첫 바이트에서 `GET`이 시작한다면 `offset:1; depth:3`은 그 문자열을 매치하지 못한다. 의도한 HTTP 메서드 조건은 적절한 HTTP 버퍼에서 `content:"GET"; offset:0; depth:3;`처럼 써야 한다. distance 1은 이전 매치 끝 이후 1바이트를 건너 다음 content 검색을 시작한다. 대소문자 무시는 `nocase`를 해당 content에 적용한다. 제공된 룰이 실제 원문과 동일한지는 복원 한계로 남긴다. | Naver text extracted; 2026-07-17 technical correction: offset/depth made the reconstructed rule internally inconsistent |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
