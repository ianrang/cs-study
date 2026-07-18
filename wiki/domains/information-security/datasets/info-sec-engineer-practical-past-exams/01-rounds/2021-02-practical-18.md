---
title: "정보보안기사 실기 18회 2021년 2회 실기 복원"
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
  - "https://blog.naver.com/stereok2/222587717690"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 18회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver direct analysis/reconstruction blog with answers."
evergreen: false
---

# 정보보안기사 실기 18회 2021년 2회 실기 복원

## Scope
- Exam mapping: 2021년 2회 실기.
- Source status: Naver direct analysis/reconstruction blog with answers; confidence: medium-high for topic and answer coverage, medium for exact official wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | EAP를 통해 인증을 수행하고 AES-CCMP 기반 암호화를 지원하는 무선랜 보안 표준은? | WPA2 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 2 | short | VirusTotal에서 제작하였고, 악성코드의 특성과 행위에 포함된 패턴을 이용하여 악성코드를 분류하는 툴 이름은? | YARA | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 3 | short | SW 개발 보안 취약점명 또는 공격기법을 쓰시오. (A)는 DB와 연결된 애플리케이션 입력값을 조작하여 의도하지 않은 결과를 반환하게 하는 공격이다. (B)는 게시판, 웹, 메일 등에 삽입된 악성 스크립트가 쿠키 및 개인정보를 특정 사이트로 전송시키는 공격이다. (C)는 검증되지 않은 사용자 입력값이 운영체제 명령어 일부로 전달되어 의도하지 않은 시스템 명령어가 실행되는 공격이다. | SQL Injection, XSS, OS Command Injection | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 4 | short | Microsoft Office와 애플리케이션 사이 데이터를 전달하는 프로토콜로, Excel에서 활성화될 경우 악용될 수 있는 프로토콜명을 쓰시오. | DDE(Dynamic Data Exchange) | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 5 | short | 위험관리 용어 빈칸을 채우시오. (A)는 (B)로부터 보호해야 할 대상이다. (B)는 (A)에 손실을 발생시키는 원인이나 행위이다. (C)는 (B)에 의해 손실이 발생하게 되는 (A)에 내재된 약점이다. | 자산, 위협, 취약점 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 6 | short | 정보의 무결성, 서비스 연속성, 정보자산 보호를 위한 것으로 기업 거버넌스의 부분집합이며, 전략적 방향 제시, 목적 달성, 적절한 위험관리, 조직 자산의 책임 있는 사용, 보안 프로그램의 성공과 실패 모니터링을 보장하는 것은 무엇인가? | 정보보안 거버넌스 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 7 | short | DDoS, APT 등 공격 수행 시 C&C 서버와 접속하기 위한 도메인명을 지속적으로 변경하여 보안장비의 탐지를 우회하기 위한 기법은? | DGA(Domain Generation Algorithm) | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 8 | short | 위험분석 절차 `1) (A), 2) (B), 3) 기존 보안대책 평가, 4) 취약성 평가, 5) 위험평가`에서 빈칸을 채우시오. | 자산식별, 자산 가치 및 의존도 평가 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 9 | short | HTTP 요청 헤더를 끝내지 않고 일부 헤더를 천천히 지속 전송해 웹서버 연결을 점유하고 서비스 가용성을 떨어뜨리는 공격은? | Slowloris | Naver text extracted; 2026-07-17 wording correction: incomplete slow headers, not generic CRLF manipulation |
| 10 | short | 모바일 앱의 특정 화면으로 바로 이동할 수 있도록 지원하는 기능으로, 입력 검증·인가가 없는 경우 공격자가 악용하면 앱 내 민감한 개인정보가 노출될 수 있는 기능 이름은? | 모바일 딥링크 | Naver text extracted; 2026-07-17 wording correction: deep links are not inherently vulnerable |
| 11 | essay | SQL Injection을 예방하기 위한 Prepared Statement에 대하여 답하시오. (1) Prepared Statement의 개념 (2) Prepared Statement가 SQL Injection 공격을 막을 수 있는 이유 | SQL과 파라미터를 분리해 미리 컴파일하고 값을 바인딩하므로 입력값이 SQL 구문으로 해석되지 않아 SQL Injection을 방어한다 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 12 | essay | DRDoS에 대하여 답하시오. (1) DRDoS의 공격 원리 (2) 기존 DoS와의 차이점 (3) Unicast RPF | 공격자가 피해자 IP로 출발지를 위조해 반사 서버에 요청을 보내고 응답이 피해자에게 집중된다. Unicast RPF는 수신 인터페이스로 향하는 역방향 경로를 확인해 위조 출발지 패킷을 차단할 수 있다. 다만 비대칭 라우팅 환경에서는 strict mode가 정상 트래픽을 차단할 수 있으므로 토폴로지에 맞춰 적용한다. | Naver text extracted; 2026-07-17 technical correction: uRPF deployment condition |
| 13 | essay | 패킷 필터링 방화벽과 관련하여 답하시오. (1) 존재하지 않는 외부 IP를 이용한 Spoofing 공격에 대응하기 위한 패킷 필터링 방화벽 기술의 이름과 원리 (2) 공격자가 패킷을 소형 단편화하여 Tiny Fragment 공격을 수행하는 이유 (3) Tiny Fragment 공격 대응 방법 (4) Stateful 패킷 필터링과 일반 패킷 필터링 방화벽의 차이점 | Ingress filtering으로 외부에서 내부 출발지 IP를 가진 패킷을 차단하고, tiny fragment는 TCP 헤더 일부를 뒤쪽 조각으로 밀어 필터 우회를 노린다. 조각 재조립 검사와 stateful inspection으로 대응한다 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 14 | essay | 이메일 로그에 `version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256`, `Received-SPF: pass`, `spf=pass`, `dkim=pass header.i=@gmail.com`이 보인다. (1) RSA의 용도는? (2) 이메일 로그에서 확인할 수 있는 스팸메일 대응 기법명과 동작 원리를 설명하시오. | `ECDHE-RSA`에서 ECDHE는 임시 키 합의를, RSA는 서버 인증서의 서명·인증에 사용된다. SPF는 SMTP envelope sender 도메인의 DNS 정책과 접속 IP를 검증하고, DKIM은 DNS 공개키로 도메인 서명을 검증한다. DMARC는 SPF/DKIM의 도메인 정렬 결과와 게시 정책을 이용한다. | Naver text extracted; 2026-07-17 technical correction: cipher-suite RSA role and mail-auth scope |
| 15 | essay | 리눅스 보안 설정에 대하여 답하시오. (1) 계정 임곗값 설정 파일명 (A)와 `auth required /lib/security/pam_tally.so (B)=5 unlock_time=120 no_magic_root reset`의 (B)를 쓰시오. (2) `iptables -A INPUT -p tcp -s 172.30.1.55 --dport 21 -j (C)`에서 차단 옵션은? (3) `/etc/shadow` 소유자를 root로 변경하고 소유자에게만 읽기 권한을 부여하는 명령은? (4) Apache 설정 `LimitRequestBody 5000000`의 의미는? | PAM 설정에서 deny로 잠금 임계값을 설정하고, iptables DROP으로 차단하며, /etc/shadow는 root 소유와 400 권한으로 보호한다. LimitRequestBody는 요청 본문 크기를 제한한다 | Naver text extracted; source says reconstructed wording may not be 100% exact |
| 16 | essay | DNS 로그 `DNS standard query 0x2872 ANY cpsc.gov ...`를 보고 답하시오. (1) 어떤 공격인가? (2) 판단 이유는? (3) 공격 원리는? (4) 공격자들이 이 기법을 사용하는 이유 두 가지는? | ANY 질의는 큰 응답을 노린 DNS 증폭 공격에 악용될 수 있는 징후지만, 이 한 질의만으로 DRDoS를 확정할 수는 없다. 출발지 IP 위조, 다수 재귀 리졸버에 대한 반복 질의, 피해자에게 향한 큰 응답·트래픽량을 함께 확인해야 한다. 조건이 충족되면 응답 증폭과 반사를 이용한 DRDoS가 된다. | Naver text extracted; 2026-07-17 technical correction: DNS ANY log alone is insufficient attribution |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
