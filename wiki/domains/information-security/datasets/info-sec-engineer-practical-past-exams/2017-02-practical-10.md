---
title: "정보보안기사 실기 10회 2017년 2회 실기 복원"
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
  - "https://information-security.tistory.com/273"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 10회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 10회 2017년 2회 실기 복원

## Scope
- Exam mapping: 2017년 2회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | TCP 포트가 닫혀 있을 때만 RST+ACK 응답이 오는 스텔스 스캔 3가지를 쓰시오. | NULL Scan, FIN Scan, Xmas Scan | source-derived from Information Security Tistory; answer block present |
| 2 | short | FTP 동작 방식에 관한 설명이다. 빈칸 (A), (B), (C), (D)를 채우시오. | A : Active(능동) B : 21 C : 20 D : 1024 | source-derived from Information Security Tistory; answer block present |
| 3 | short | 오픈소스 도구인 PacketFence와 같이 네트워크 접속 단말의 보안 상태를 점검하고 비인가 단말의 네트워크 접근을 통제하는 보안 솔루션의 명칭을 쓰시오. | NAC(Network Access Control) | source-derived from Information Security Tistory; answer block present |
| 4 | short | VLAN의 목적에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 보안 B : 크기(브로드캐스트 도메인 크기) C : 성능 | source-derived from Information Security Tistory; answer block present |
| 5 | short | 위험 처리 방법 중 보험이나 외주를 통해 잠재적 손실 비용을 제3자에게 이전하는 방법의 명칭을 쓰시오. | 위험 전가(Risk Transfer) | source-derived from Information Security Tistory; answer block present |
| 6 | short | 정보통신기반보호법 제8조에 따른 주요정보통신기반시설 지정 시 고려 사항이다. 빈칸 (A), (B), (C)를 채우시오. | A : 의존도 B : 상호연계성 C : 용이성 | source-derived from Information Security Tistory; answer block present |
| 7 | short | 재해복구 사이트 유형에 관한 설명이다. (A)는 중요도가 높은 정보기술 자원만 부분적으로 사이트에 보유하며 백업 장치나 테이프 등을 구비한다. (B)는 주 센터와 동일한 수준의 정보기술 자원을 사이트에 보유하면서 데이터를 최신 상태로 유지한다. (C)는 컴퓨터실 같은 장소만 확보하고 정보 자원은 확보하지 않은 상태로, 재해 발생 시 정보 자원을 새로 반입한다. 빈칸 (A), (B), (C)를 채우시오. | A : 웜 사이트(Warm Site) B : 핫 사이트(Hot Site) C : 콜드 사이트(Cold Site) | source-derived from Information Security Tistory; user-provided source image cross-checked |
| 8 | essay | 개인정보 안전성 확보조치 기준에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 개인정보처리시스템 B : 비밀번호 C : 내부망 | source-derived from Information Security Tistory; answer block present |
| 9 | short | 정보통신망 이용촉진 및 정보보호 등에 관한 법률 제25조에 따라 개인정보의 처리 위탁 시 공개해야 하는 사항 2가지를 쓰시오. | (1) 개인정보 처리 위탁을 받는 자 (2) 개인정보 처리 위탁을 하는 업무의 내용 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 위험 관리에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : 취약성(Vulnerability) B : 감소(위험 감소) C : 보유(위험 수용) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 버퍼 오버플로우 방어 기법에 관한 물음에 답하시오. | (1) 메모리상에서 프로그램의 복귀 주소(Return Address)와 변수/버퍼 사이에 특정 값(Canary)을 저장해두는 기법이다. (2) 버퍼 오버플로우가 발생하면 특정 값(Canary)이 변조되므로 함수 반환 시 해당 값을 확인하여 변조가 감지되면 프로그램 실행을 중단하고 공격을 차단한다. (3) 메모리 공격을 방어하기 위해 스택·힙·라이브러리 등 메모리 영역의 주소를 실행할 때마다 무작위로 배치하는 기법이다. (4) 실행 시마다 메모리 주소가 변경되므로 공격자가 특정 메모리 주소(복귀 주소, 쉘코드 주소 등)를 예측하기 어렵게 만들어 버퍼 오버플로우를 통한 특정 주소 호출을 방지한다. | source-derived from Information Security Tistory; answer block present |
| 12 | short | 정보통신서비스 제공자가 연 1회 이용자에게 통보해야 하는 개인정보 관련 사항 3가지를 쓰시오. | (1) 개인정보의 수집·이용 목적 및 수집한 개인정보의 항목 (2) 개인정보를 제공받는 자와 그 제공 목적 및 제공한 개인정보의 항목 (3) 개인정보 처리 위탁을 받은 자 및 그 처리 위탁을 하는 업무의 내용 | source-derived from Information Security Tistory; answer block present |
| 13 | essay | iptables의 -j 옵션 중 DROP과 REJECT에 관한 물음에 답하시오. | (1) DROP : 매치된 패킷을 차단하고 아무런 응답 메시지도 전송하지 않는다. (2) REJECT : 매치된 패킷을 차단하고 출발지에 RST 패킷 또는 ICMP 오류 메시지를 응답으로 전송한다. (3) 보안 관점에서 DROP이 적절하다. REJECT는 ICMP 응답 메시지를 통해 포트 상태 등 시스템 정보가 공격자에게 노출될 수 있으므로, 아무런 응답을 보내지 않는 DROP을 사용하여 공격자에게 정보를 제공하지 않는 것이 보안상 유리하다. | source-derived from Information Security Tistory; answer block present |
| 14 | short | 다음은 TCP 연결 설정 및 해제 과정이다. 빈칸을 채우시오. | A : SYN (000010) B : 344 C : SYN+ACK (010010) D : 677 E : ACK (010000) F : ACK (010000) G : FIN+ACK (010001) | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 다음은 하나의 출발지에서 브로드캐스트로 ICMP Echo Request를 전송하는 패킷 캡처이다. 물음에 답하시오. | (1) 스머프(Smurf) 공격 (2) 공격자는 출발지 IP를 희생자 IP로 위조한 ICMP Echo Request 패킷을 브로드캐스트 주소로 전송한다. 네트워크 내 모든 호스트가 ICMP Echo Reply를 희생자에게 일제히 전송하여 대량의 트래픽이 집중되고 서비스 거부 상태가 발생한다. (3) 라우터에서 외부 네트워크로부터 자신의 네트워크로 들어오는 Directed Broadcast 패킷을 차단한다. (no ip directed-broadcast) 호스트에서 브로드캐스트 주소로 전송된 ICMP Echo Request에 응답하지 않도록 설정한다. | source-derived from Information Security Tistory; answer block present |
| 16 | essay | CentOS에서 네트워크 인터페이스가 Promiscuous Mode로 동작하고 있음이 확인되었다. 물음에 답하시오. | (1) 스니핑(Sniffing) 공격이다. Promiscuous Mode는 자신을 목적지로 하는 패킷뿐만 아니라 네트워크의 모든 패킷을 수신하므로, 공격자가 스니핑 프로그램을 설치하여 네트워크 트래픽을 도청하기 위해 설정한 것으로 판단된다. (2) ifconfig eth0 -promisc (3) /var/log/messages | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
