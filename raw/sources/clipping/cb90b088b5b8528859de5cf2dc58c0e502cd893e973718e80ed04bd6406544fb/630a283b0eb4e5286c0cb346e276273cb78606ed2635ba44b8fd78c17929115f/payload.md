---
title: "정보보안기사 실기 21회 2022년 4회 실기 복원"
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
  - "https://nhustler.tistory.com/36"
  - "https://nhustler.tistory.com/37"
  - "https://blog.naver.com/stereok2/222985383781"
source_count: 3
provenance: inferred
summary: "정보보안기사 실기 21회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 21회 2022년 4회 실기 복원

## Scope
- Exam mapping: 2022년 4회 실기.
- Source status: Naver blog reconstruction cross-check; confidence: high for topic coverage, medium for exact wording.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | Sendmail에서 스팸메일 릴레이 제한 설정 후 access DB를 생성하려고 한다. `# (A) (B) /etc/mail/access.db < /etc/mail/access`의 빈칸을 채우시오. | (A) `makemap`, (B) `hash` | source-derived; Naver cross-checked; leading slash in reconstructed source was ambiguous |
| 2 | short | 라우터에서 SNMP 프로토콜을 비활성화하려고 한다. `Router# configure terminal`, `Router(config)# (A) (B)`의 빈칸을 채우시오. | (A) `no`, (B) `snmp-server` | source-derived; Naver cross-checked; official wording unverified |
| 3 | short | 위험분석과 관련해 1) 수용 가능한 수준의 위험을 지칭하는 용어를 쓰고, 2) 위험이 낮으면 원칙적으로 비용 절감을 위해 그대로 두는 것이 맞는지 O/X로 답하시오. | 1) 위험수용기준/허용 가능한 위험 수준(복원 원천의 `DoA` 약어 확장은 확인되지 않음) 2) X. 낮은 위험도 조직의 위험수용기준·법적 의무·통제 비용을 검토해 승인 절차로 결정한다. | source-derived; 2026-07-17 reconstruction-limit correction: DoA expansion was unsupported |
| 4 | short | 업무연속성계획(BCP) 5단계 중 2~4단계의 명칭을 쓰시오. | BIA(사업영향평가), 복구전략 개발, 복구계획 수립 | source-derived; Naver cross-checked; official wording unverified |
| 5 | short | 특정 대상을 겨냥해 다양한 공격기법, 특히 알려지지 않은 취약점을 이용하여 장기간 지속적으로 공격하는 기법을 쓰시오. | APT(Advanced Persistent Threat, 지능형 지속 위협) | source-derived; Naver cross-checked; official wording unverified |
| 6 | short | 불완전한 암호화 저장 취약점이 있는 웹 애플리케이션은 데이터와 자격증명을 보호하는 암호화 기능을 충분히 사용하지 않아 신원 도용·신용카드 사기 등의 위험이 있다. 다음 점검 방법의 빈칸을 채우시오. (1) DB에 저장된 중요정보가 (A)로 열람 가능한지 확인한다. (2) (B) 또는 암호화된 쿠키값이 명백하게 랜덤으로 생성되는지 확인한다. (3) 적절한 (C)이 제대로 적용됐는지 검증한다. | (A) SQL Query, (B) 세션 ID, (C) 암호화 알고리즘 | PDF compilation cross-check restored the full stem and all blanks. This is a non-official blog compilation, not KCA wording. |
| 7 | short | TCP/IP 인터넷 계층에서 동작하는 VPN 보안 프로토콜과 그 세부 프로토콜 중 무결성·메시지 인증을 제공하는 항목, 암호화를 통한 기밀성을 제공하는 항목의 빈칸 (A), (B), (C)를 채우시오. | (A) IPSec, (B) AH(Authentication Header), (C) ESP(Encapsulating Security Payload) | source-derived; N-hustler problem text cross-checked; exact official wording unverified |
| 8 | short | 위험분석 방법의 빈칸을 채우시오. (A)는 전문가의 익명 설문과 피드백을 반복하여 위험·취약성에 대한 합의를 도출한다. (B)는 일정 조건에서 발생 가능한 결과를 시나리오로 추정한다. (C)는 자산·위협·보안체계 등을 정성적 언어값으로 표현해 기대손실을 평가한다. | (A) 델파이법, (B) 시나리오법, (C) 퍼지행렬법 | source-derived; 2026-07-17 technical wording correction: Delphi method |
| 9 | short | 익스플로잇 코드의 빈칸을 채우시오. (A)는 어셈블리어/기계어로 구성된 익스플로잇 코드 본체, (B)는 NOP에 해당하는 x86 Hex Code, (C)는 ESP가 가리키는 주소로 실행 흐름을 옮기는 어셈블리 명령이다. | (A) Shell Code, (B) `0x90`, (C) `JMP ESP` 계열. `RET`은 스택에서 값을 pop하여 EIP로 옮기므로 같은 의미의 일반 정답으로 병기하지 않는다. | source-derived; 2026-07-17 technical correction: control transfer semantics |
| 10 | short | Apache 업로드 가능 파일 크기 제한 명령/지시자. | `LimitRequestBody` | source-derived; Naver cross-checked; official wording unverified |
| 11 | essay | IDS 침입탐지 방식에 대해 1) 오용 탐지의 정의, 2) 이상 탐지의 정의, 3) 오용 탐지의 장점, 4) 오용 탐지의 단점을 설명하시오. | 오용 탐지는 알려진 공격 패턴/시그니처 기반 탐지, 이상 탐지는 정상 행위 프로파일과의 차이 기반 탐지. 오용 탐지는 오탐이 낮지만 신규 공격 탐지가 어렵고 패턴 업데이트가 필요하다. | source-derived; Naver cross-checked; official wording unverified |
| 12 | essay | 재해복구시스템 유형 중 미러사이트에 대해 1) 정의, 2) 장단점 각 2개, 3) RTO가 가장 오래 걸리는 방식과 이유를 설명하시오. | 미러사이트는 주센터와 동일 수준 시스템을 백업센터에 구축해 액티브-액티브로 실시간 서비스하는 방식. 장점은 즉시 복구와 최신 데이터 보장, 단점은 높은 구축·운영 비용과 데이터 업데이트 과부하 가능성. RTO가 가장 긴 방식은 콜드사이트이며, 재해 시 자원 조달과 복구 시간이 필요하다. | source-derived; Naver cross-checked; official wording unverified |
| 13 | essay | 개인정보 기술적·관리적 보호조치 기준에 포함된 개인정보취급자 비밀번호 작성규칙 3가지를 기술하시오. | 복잡도/길이 기준 준수, 유추하기 어려운 비밀번호 사용, 유효기간 설정 및 주기적 변경 등 | source-derived; Naver cross-checked; current policy wording may vary |
| 14 | practical | 동일한 출발지 IP에서 2초 동안 80번 포트로 30개 이상 SYN 요청이 들어오는 경우 차단하는 iptables 룰을 작성하고, 룰 옵션을 5개로 구분해 설명하시오. | `recent --update`는 먼저 동일 목록에 IP를 넣는 `--set` 규칙이 있어야 동작한다. 예: 새 SYN을 `--name SYN_DROP --set`으로 기록한 뒤, 다음 규칙에서 `--update --seconds 2 --hitcount 30 --name SYN_DROP -j DROP`을 적용한다. 단일 `--update` 행만으로는 최초 요청을 추적할 수 없다. | source-derived; 2026-07-17 technical correction: recent module state initialization |
| 15 | practical | ALE와 관련해 1) SLE 정의, 2) SLE 계산식, 3) ALE 계산에 필요한 정보, 4) 연간 손실이 완전 제거되는데 투입된 비용이 X일 때 ROI(%) 계산식을 답하시오. | 1) 단일 사건 손실액 2) `SLE = AV * EF` 3) ARO 4) `(ALE - X) / X * 100` | source-derived; Naver cross-checked; official wording unverified |
| 16 | practical | Master DNS `ns1.korea.co.kr(192.168.1.1)`와 Slave DNS `ns2.korea.co.kr(192.168.1.2)`의 zone 설정 빈칸을 채우시오. Master `/etc/named.conf`: `type (A); allow-transfer { (B) }`; zone file: `ns1 IN A (C)`, `ns2 IN A (D)`; Slave `/etc/named.conf`: `type (E); masters { (F) }`. | (A) `master`, (B) `192.168.1.2;`, (C) `192.168.1.1`, (D) `192.168.1.2`, (E) `slave`, (F) `192.168.1.1;`. Slave의 zone transfer 허용은 `allow-update`가 아니라 `allow-transfer` 문맥이다. | source-derived; 2026-07-17 technical correction: BIND transfer/update distinction |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.
