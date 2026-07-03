---
title: "정보보안기사 실기 1회 2013년 1회 실기 복원"
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
  - "https://information-security.tistory.com/293"
source_count: 1
provenance: inferred
summary: "정보보안기사 실기 1회 복원 항목을 Tistory 원문 답안 블록 기준으로 정리한 페이지."
evergreen: false
---

# 정보보안기사 실기 1회 2013년 1회 실기 복원

## Scope
- Exam mapping: 2013년 1회 실기.
- Source status: Information Security Tistory direct reconstruction post; confidence: medium-high.
- This file stores paraphrased reconstruction notes and answer keys, not verbatim official exam text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.

## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 위협의 종류·영향·발생 가능성을 평가하는 과정, 그 결과로 비용 대비 통제 방안을 선택해 위협을 통제하는 과정, 선택한 통제의 목적·방안·적용 주체·시점·대상을 문서화한 계획의 빈칸 (A), (B), (C)를 채우시오. | A : 위험평가 B : 위험관리 C : 위험관리계획 | source-derived from Information Security Tistory; answer block present |
| 2 | short | NMS 서버가 장비 상태와 통계를 주기적으로 수집하는 방식, 장비가 특정 이벤트를 실시간 전달하는 방식, 장비 이벤트 정보를 서버로 전송하는 방식의 빈칸 (A), (B), (C)를 채우시오. | A : Polling B : Event Reporting C : syslog | source-derived from Information Security Tistory; answer block present |
| 3 | essay | 다음은 개인정보의 안전성 확보조치 기준에 따라 개인정보처리자가 수립·시행해야 하는 사항이다. 이와 같이 내부적으로 수립하고 시행해야 하는 계획의 명칭을 쓰시오. | 내부관리계획 | source-derived from Information Security Tistory; answer block present |
| 4 | short | 유닉스(UNIX) 솔라리스(Solaris) 운영체제의 사용 로그 파일에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : lastlog B : sulog C : loginlog | source-derived from Information Security Tistory; answer block present |
| 5 | short | 정보보호 정책을 구현하기 위해 개발하는 문서 유형에 관한 빈칸 (A), (B), (C)를 채우시오. (A)와 (B)는 시스템 보안을 위한 기술·방법을 구체화하고, (C)는 필요한 기술과 파라미터 설정을 일관성 있게 기술한 강제사항이다. | A : 표준 B : 지침 C : 절차 | source-derived from Information Security Tistory; answer block present |
| 6 | short | SIEM의 주요 기능에 관한 설명이다. 빈칸 (A), (B), (C), (D)를 채우시오. | A : 로그 수집 B : 로그 분류 C : 로그 변환 D : 로그 분석 | source-derived from Information Security Tistory; answer block present |
| 7 | short | IDS의 종류에 관한 설명이다. 빈칸 (A), (B)를 채우시오. | A : 호스트(Host) B : 네트워크(Network) | source-derived from Information Security Tistory; answer block present |
| 8 | short | 리눅스 시스템의 로그 파일에 관한 설명이다. 빈칸 (A), (B), (C)를 채우시오. | A : lastlog B : btmp C : xferlog | source-derived from Information Security Tistory; answer block present |
| 9 | short | 업무 목적으로 개인정보파일을 운용하며 개인정보를 처리하는 주체, 그 지휘·감독을 받아 개인정보를 처리하는 사람, 개인정보 처리를 위해 체계적으로 구성한 데이터베이스 시스템의 빈칸 (A), (B), (C)를 채우시오. | A : 개인정보처리자 B : 개인정보취급자 C : 개인정보처리시스템 | source-derived from Information Security Tistory; answer block present |
| 10 | short | 자산 관리 절차에 관한 설명이다. 빈칸 (A), (B)를 채우시오. | A : 자산목록 B : 자산분류(자산분석) | source-derived from Information Security Tistory; answer block present |
| 11 | essay | 다음 파일 및 디렉토리의 권한 설정에 관한 설명을 각각 서술하시오. | /usr/bin/passwd : 소유자(owner) 권한이 r-s로 setuid가 설정되어 있으며, 기타 사용자(other) 권한이 r-x로 실행 권한이 있다. 따라서 모든 사용자가 passwd 명령을 실행할 때 소유자인 root 권한으로 수행된다. /usr/bin/mail : 그룹(group) 권한이 r-s로 setgid가 설정되어 있다. 해당 파일 실행 시 mail 그룹 권한으로 수행된다. /tmp : 퍼미션이 rwt로 sticky bit가 설정되어 있다. 해당 디렉토리에 생성된 파일은 누구든지 읽기·쓰기는 가능하지만, 삭제는 파일 소유자와 root만 가능하다. | source-derived from Information Security Tistory; answer block present |
| 12 | essay | /etc/apache/conf 디렉토리 내에서 10일 이내에 내용이 변경된 파일을 검색하는 find 명령어를 한 줄로 작성하시오. | find /etc/apache/conf -type f -mtime -10 | source-derived from Information Security Tistory; answer block present |
| 13 | essay | 위험 대응 방안 중 위험 회피(Risk Avoidance)와 위험 전이(Risk Transfer)의 개념과 발생 조건을 자산, 위협, 취약점 관점에서 각각 서술하시오. | 위험 회피(Risk Avoidance) : 위험이 존재하는 프로세스나 사업을 수행하지 않고 포기하는 방안이다. 자산의 중요도가 높고 위협 발생 가능성이 높으나 취약점을 제거하기 어려울 때, 해당 업무나 시스템 자체를 폐기하거나 중단하는 방식으로 위험에 대응한다. 위험 전이(Risk Transfer) : 보험 가입이나 외주 등을 통해 잠재적 손실 비용을 제3자에게 이전하거나 할당하는 방안이다. 위협은 존재하나 자체적으로 통제하기 어렵거나 비용이 과다할 때, 위험의 재정적 책임을 외부로 전가하는 방식으로 대응한다. | source-derived from Information Security Tistory; answer block present |
| 14 | essay | 개인정보 안전성 확보조치 기준에 명시된 접근 권한의 관리 기준 3가지를 서술하시오. | (1) 개인정보처리자는 개인정보처리시스템에 대한 접근 권한을 업무 수행에 필요한 최소한의 범위로 업무 담당자에 따라 차등 부여하여야 한다. (2) 전보·퇴직 등 인사이동으로 개인정보취급자가 변경된 경우 지체 없이 개인정보처리시스템의 접근 권한을 변경 또는 말소하여야 한다. (3) 권한 부여·변경·말소에 대한 내역을 기록하고, 그 기록을 최소 3년간 보관하여야 한다. | source-derived from Information Security Tistory; answer block present |
| 15 | essay | 시스코(Cisco) 라우터에서 다음 조건에 맞는 패스워드 설정 명령어를 각각 완성하시오. | (1) service password-encryption (2) enable secret [패스워드] (3) enable password [패스워드] | source-derived from Information Security Tistory; answer block present |
| 16 | essay | 다음은 네트워크 관리자가 확인한 ARP 테이블이다. 물음에 답하시오. | (A) ARP Spoofing(ARP 스푸핑) 공격 (B) 관리자가 알고 있는 Gateway(175.113.81.1)의 실제 MAC 주소는 a1-b1-c1-d1-e1-f1이지만, ARP 테이블에는 90-9f-5e-00-2f-16으로 변조되어 있다. 동일한 MAC 주소가 175.113.81.65에도 등록되어 있어 ARP Spoofing 공격으로 판단된다. (C) 175.113.81.65 (MAC: 90-9f-5e-00-2f-16) (D) arp -s 175.113.81.1 a1-b1-c1-d1-e1-f1 (Gateway IP에 대한 ARP 캐시를 정적으로 설정하여 위조된 ARP 응답으로 덮어쓰이지 않도록 한다.) | source-derived from Information Security Tistory; answer block present |

## Verification Notes
- Cross-check basis: the round-specific Tistory post linked in `source_paths` was parsed by sequential question number and answer marker.
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Legal/regulatory answers should be checked against current statutes before memorization.
