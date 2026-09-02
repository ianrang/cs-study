---
title: "정보보안기사 실기 20회 2022년 2회 실기 복원"
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
  - "https://nhustler.tistory.com/38"
  - "https://nhustler.tistory.com/39"
  - "https://blog.naver.com/stereok2/222860841923"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 20회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 20회 2022년 2회 실기 복원

## Scope
- Exam mapping: 2022년 2회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Telnet으로 웹 서버에 접속한 후 응답 헤더에 `Allow: GET,HEAD,POST,OPTIONS,TRACE`가 표시되었다. 허용 HTTP Method를 확인하는 명령을 쓰시오. | OPTIONS | source-derived; Naver text extracted; official wording unverified |
| 2 | short | 위험분석 방법 빈칸을 채우시오. (A)는 전문가의 익명 설문과 피드백을 반복하여 위험과 취약성에 대한 합의를 도출하는 방법이다. (B)는 일정 조건하에서 발생 가능한 결과를 시나리오로 추정하는 방법이다. (C)는 비교 우위 순위결정표에 따라 위험 항목들의 서술적 순위를 결정하는 방법이다. | 델파이법, 시나리오법, 순위결정법 | source-derived; 2026-07-17 technical wording correction: Delphi method |
| 3 | short | 위험분석 접근법 빈칸을 채우시오. (A)는 모든 시스템에 보호의 기본 수준을 정하고 표준화된 체크리스트 기반 보호대책을 선택하는 방식이다. (B)는 정립된 모델에 기초하여 자산·위협·취약성 분석 단계를 수행하는 방식이다. (C)는 고위험 영역을 상세 위험분석하고 다른 영역은 베이스라인 접근법을 사용하는 방식이다. | 베이스라인 접근법, 상세 위험분석, 복합 접근법 | source-derived; Naver text extracted; official wording unverified |
| 4 | short | 접근통제 정책 빈칸을 채우시오. (A)는 사용자나 사용자 그룹에 근거한 사용자 중심 접근 제어 방식이다. (B)는 모든 객체가 정보의 비밀수준에 근거한 보안 레벨을 가지며 허가된 사용자만 접근 가능하도록 제어하는 방식이다. (C)는 사용자와 객체 상호관계를 역할 기반으로 접근 권한을 부여하는 방식이다. | DAC, MAC, RBAC | source-derived; Naver text extracted; official wording unverified |
| 5 | short | IDS 탐지 정책에서 (A)는 정상 행위를 이상행위로 판단하여 탐지하는 상황이고, (B)는 이상행위를 탐지하지 못하는 상황이다. 빈칸을 채우시오. | 오탐(False Positive), 미탐(False Negative) | source-derived; Naver text extracted; official wording unverified |
| 6 | short | IPSec에서 지원하는 보안 서비스. | 기밀성, 제한된 트래픽 흐름 기밀성, 데이터 근원지 인증, 접근제어, 비연결형 무결성, 재전송 공격 방지 중 3개 | source-derived; Naver cross-checked; official wording unverified |
| 7 | short | (A)는 사토시 나카모토가 개발한 가상화폐로, 거래 데이터를 기록하는 저장소로 (B)를 이용한다. Hash 연산으로 발생된 거래 작업을 증명한 대가로 (A)를 획득하는 행위를 (C)라 한다. | 비트코인, 블록체인, 채굴/마이닝 | source-derived; Naver text extracted; official wording unverified |
| 8 | short | Apache 설정 `<Directory /var/www> Options indexes FollowSymLinks; AllowOverride none; Require all granted </Directory>`에서 디렉터리 인덱싱 취약점 대응을 위해 삭제해야 하는 지시자를 쓰시오. | `Indexes` | source-derived; Naver text extracted; official wording unverified |
| 9 | short | 삭제하지 않은 CNAME이 피싱 사이트 등으로 악용되는 공격. | 서브도메인 하이재킹 또는 서브도메인 테이크오버 | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | ISMS-P 물리적 정보보호 대책 항목. | 보호구역 지정, 출입통제, 정보시스템 보호, 보호설비 운영, 보호구역 내 작업, 반출입 기기 통제, 업무환경 보안 중 3개 | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | 개인정보 최소수집 원칙에 의거하여 개인정보 수집이 가능한 경우 4가지를 쓰시오. | 정보주체 동의, 법령상 의무, 공공기관 소관업무, 계약 체결·이행, 급박한 생명·신체·재산 이익, 정당한 이익 등 | source-derived; Naver text extracted; legal wording needs current-law check |
| 12 | essay | 스위칭 허브의 기능 및 동작 원리를 서술하시오. 기능은 목적지 주소 기반 포트 전송, 고속 전송, 로드밸런싱, QoS 관점에서 설명하고, L2 동작 원리는 Learning, Forwarding, Filtering, Flooding, Aging 관점에서 설명한다. | 목적지 주소 기반 포트 전송 장치이며 learning, forwarding, filtering, flooding, aging 방식으로 MAC table을 운용 | source-derived; Naver text extracted; official wording unverified |
| 13 | essay | Snort 룰 `alert tcp any any -> any 21 {content:"anonymous"; nocase; msg:"Anonymous FTP attempt"; sid:1000012}`과 탐지 패킷 `55 53 45 52 20 41 6E 4F 6E 59 6D 4F 75 53 0D 0A USER AnOnYmOuS..`를 보고 어떤 공격이 수행되었는지 설명하시오. | Anonymous FTP 로그인 시도. 대소문자 혼합 입력은 탐지 우회 목적이며 `nocase`로 탐지 가능 | source-derived; Naver text extracted; official wording unverified |
| 14 | practical | Sendmail 스팸메일 릴레이 제한 설정과 관련하여 빈칸을 채우시오. `cat /etc/mail/(1) \| grep "R$*" \| grep "Relaying denied"` 결과는 `R$* $#error $@ 5.7.1 $ : "550 Relaying denied"`이다. `/etc/mail/access`에는 `localhost.localdomain RELAY`, `localhost RELAY`, `127.0.0.1 RELAY`, `spam.com (2)`가 있다. access DB 생성 명령은 `(3) hash /etc/mail/(4) < /etc/mail/access` 형식이다. | (1) `sendmail.cf`, (2) `REJECT`, (3) `makemap`, (4) `access.db`; 전체 명령 예시는 `makemap hash /etc/mail/access.db < /etc/mail/access`이다. | source-derived; 2026-07-17 technical correction: all reconstructed blanks are now answerable |
| 15 | practical | Smurf attack을 방지하기 위하여 신뢰할 수 있는 네트워크 범위 `192.168.1.0/24`에서 시작하는 UDP 패킷으로 directed broadcast를 제한하는 라우터 명령어를 쓰시오. `(config)# (A)`, `(config)# (B)`, `(config-if)# (C)`, `^z`, `Router#` | (A) `access-list 100 permit udp 192.168.1.0 0.0.0.255 any` (B) `interface FastEthernet 0/0` (C) `no ip directed-broadcast 100` | PDF compilation cross-check restored the negation in (C). The exact IOS syntax and ACL attachment are platform/version-dependent; Cisco documentation confirms `no ip directed-broadcast` disables directed-broadcast forwarding. This is a non-official blog compilation, not KCA wording. |
| 16 | practical | 위험 대응 기법에 대하여 답하시오. (1) 위험수용의 의미는? (2) 위험감소를 위한 보안대책 선정 시 특정 보안대책의 평가기준을 결정하는 정량적인 방법은? (3) 위험회피 시 위험이 있는 프로세스나 사업은 어떻게 대처하는가? (4) 위험전가를 위한 2가지 방법은? | (1) 위험수용은 승인된 잔여 위험을 감수하는 것이다. (2) 보안대책의 비용 대비 위험 감소 효과를 비교하는 비용-편익/ROI 분석을 사용한다. (3) 위험이 있는 프로세스·사업을 중단하거나 수행하지 않는다. (4) 보험 가입, 계약·외주를 통한 손실 책임 이전 등이 있다. | source-derived; 2026-07-17 technical correction: prior answer only listed headings |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
