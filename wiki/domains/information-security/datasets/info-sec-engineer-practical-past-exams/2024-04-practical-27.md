---
title: "정보보안기사 실기 27회 2024년 4회 실기 복원"
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
  - "https://it-utopia.tistory.com/entry/정보보안기사-2024년-제27회-정보보안기사-실기-기출문제-복원"
  - "https://blog.naver.com/stereok2/223762794914"
source_count: 2
provenance: inferred
summary: "정보보안기사 실기 27회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction, Naver blog cross-check."
evergreen: false
---

# 정보보안기사 실기 27회 2024년 4회 실기 복원

## Scope
- Exam mapping: 2024년 4회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223762794914`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local PDFs supplied for 1~28회 are password-protected in this environment, so PDF-level validation is pending.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 접근통제 정책에 대하여 다음 물음에 답하시오. - (A) : 사용자나 사용자 그룹에 근거한 사용자 중심의 접근 제어 수행 - (B) : 모든 객체는 정보의 비밀수준에 근거하여 보안 레벨이 주어지고 허가된 사용자만 접근 가능토록 제어 - (C) : 사용자와 객체 상호관계를 역할에 따라 접근 제어 수행 | (A) : DAC, (B) : MAC, (C) : RBAC | source-derived; Naver cross-checked; official wording unverified |
| 2 | short | MAC 주소(물리 주소)를 기반으로 IP 주소(논리 주소)를 할당받기 위해 사용되며, 디스크 없는 장치나 네트워크 부팅을 지원하는 장비에서 사용하는 TCP/IP 프로토콜은 무엇인가? | RARP(Reverse Address Resolution Protocol) | source-derived; exact wording unverified |
| 3 | short | VLAN 구성 방식에 대하여 다음 ( )에 들어갈 명칭을 기술하시오. - (A) 기반 VLAN : 스위치 포트를 각 VLAN에 할당. 같은 VLAN에 속한 호스트 간에만 통신 가능. 가장 일반적인 방식 - (B) 기반 VLAN : 호스트의 MAC 주소를 VLAN에 등록. 모든 MAC을 등록하고 관리하는 어려움. - (C) 기반 VLAN : 네트워크 주소별로 VLAN 구성. - (D) 기반 VLAN : 같은 통신 프로토콜을 가진 호스트 간에는 통신가능토록 VLAN 설정 | (A) : 포트, (B) : MAC, (C) : 네트워크 주소, (D) : 프로토콜 | source-derived; exact wording unverified |
| 4 | short | 전자금융거래법 제21조2 제4항에 기술된 다음 각호의 업무를 수행하는 사람을 무엇이라고 하나? 1) 전자금융거래의 안정성 확보 및 이용자 보호를 위한 전략 및 계획의 수립 2) 정보기술부문의 보호 3) 정보기술부문의 보안에 필요한 인력관리 및 예산편성 4) 전자금융거래의 사고 예방 및 조치 | CISO(Chief Information Security Officer) | source-derived; exact wording unverified |
| 5 | short | 리눅스 시스템 로그 파일에 대하여 다음 빈칸에 적절한 파일을 기술하시오. - (A) : 현재 시스템에 로그인한 사용자의 상태가 출력되는 로그 - (B) : 사용자의 로그인, 로그아웃, 시스템 재부팅 정보가 누적되어 출력되는 로그 - (C) : 마지막으로 성공한 로그인 정보가 출력되는 로그 | (A) : utmp, (B) : wtmp, (C) : lastlog | source-derived; exact wording unverified |
| 6 | short | 다음 스캔 방법 중 포트가 닫혀있을 때만 응답이 오는 스캔 방식을 고르시오. SYN scan / FIN scan / XMAS scan / Null scan / Decoy scan | FIN scan, XMAS scan, Null scan | source-derived; exact wording unverified |
| 7 | short | SW 개발 보안과 관련하여 ( )에 들어갈 취약점명(공격기법)을 기술하시오. - (A) : DB와 연결되어 있는 애플리케이션의 입력값을 조작하여 의도하지 않은 결과를 반환하도록 하는 공격 기법 - (B) : 게시판, 웹, 메일 등에 삽입된 악의적인 스크립트에 의해 쿠키 및 기타 개인정보를 특정 사이트로 전송시키는 공격 기법 - (C) : 적절한 검증 절차를 수행하지 않은 사용자 입력값이 운영체제 명령어의 일부로 전달되어 의도하지 않은 시스템 명령어가 실행되도록 하는 공격 기법 | (A) : SQL Injection, XSS, 운영체제 명령어 삽입 | source-derived; exact wording unverified |
| 8 | short | 다음은 특정 명령어를 수행한 결과이다. ( )에 들어갈 명령어를 기술하시오. root@kali:~#Telnet webserver.com 80 Trying 192.168.1.2 ... Connect to webserver.com Escape character is '^]' ( ) * HTTP/1.0 HTTP/1.1 200 OK Date: Sat 6 Aug 2022 09:01:01 KST Server: Microsoft-IIS/5.0 Allow: GET, HEAD, POST, OPTIONS, TRACE Content-Length: 0 Connection: close Content-Type: text/plain; charset-euc-kr Connection closed by foreign host | OPTIONS | source-derived; exact wording unverified |
| 9 | short | 소프트웨어 패치의 종류와 관련하여 ( )에 들어갈 용어를 기술하시오. - (A) : 즉시 교정되어야만 하는 주요한 취약점을 패치하기 위해 배포되는 프로그램으로 서비스팩이 발표된 이후 패치가 추가될 필요가 있을 때 별도로 발표됨 - (B) : 문제를 예방 또는 해결하거나 컴퓨터 작동 방식을 향상시키거나, 컴퓨터 경험을 향상시킬 수 있도록 추가되는 소프트웨어 | (A) : 핫픽스(Hot Fix), (B) : 업데이트(Update) | source-derived; Naver cross-checked; official wording unverified |
| 10 | short | 매니저와 에이전트 구조로 되어 있고, 네트워크 장비의 상태를 모니터링하고 관리하기 위해 사용되는 TCP/IP 기반 네트워크 프로토콜을 무엇이라고 하나? | SNMP(Simple Network Management Protocol) | source-derived; exact wording unverified |
| 11 | short | 어떠한 대책을 도입하더라도 위험을 완전히 제거할 수 없으므로 일정 수준 이하의 위험은 받아들이고 사업을 진행하는 위험대응 방식을 무엇이라고 하나? | 위험수용 | source-derived; exact wording unverified |
| 12 | short | 네트워크 논리 그룹을 구분하여 보안을 강화하고, 브로드캐스트 도메인의 범위를 줄여 네트워크 성능 향상을 지원하는 LAN 기술을 무엇이라고 하나? | VLAN(Virtual LAN) | source-derived; exact wording unverified |
| 13 | essay | 위험분석 접근법 중 복합접근법의 개념, 장점, 단점을 설명하시오. | 개념: 고위험 영역은 상세 위험분석을 수행하고 다른 영역은 베이스라인 접근법을 사용하는 방식. 장점: 분석 정확성과 속도의 균형을 유지해 효율적인 보안 정책 적용이 가능하고, 환경에 맞춰 상세분석과 베이스라인 비중을 조정할 수 있다. 단점: 두 접근법을 조합하므로 명확한 기준이 필요하고 관리정책이 복잡해질 수 있으며, 자산 중요도 판단 오류 시 비용 과다 또는 중요 시스템 보안 부족이 발생할 수 있다. | source-derived; Naver cross-checked; official wording unverified |
| 14 | essay | 정보보호조치에 관한 지침은 정보통신망법 제45조 2항에 따라 정보통신서비스 제공자가 정보통신서비스를 제공하는데 사용되는 정보통신망의 안정성 및 정보의 신뢰성을 확보하기 위한 보호조치의 구체적인 내용 중 다음 항목에서 규정하고 있는 내용을 기술하시오. 1) 1.2.1. 정보보호 방침의 수립·이행 2) 1.2.2. 정보보호 실행 계획의 수립 및 이행 - 정보보호 목표, 범위, 책임 등을 포함한 정보보호 방침(policy) 수립 - 정보통신서비스와 관련된 모든 법, 규제, 계약, 정책, 기술상의 요구사항을 문서화하고 시행 2) 1.2.2. 정보보호 실행계획의 수립·이행 - 정보보호 방침을 토대로 예산, 일정 등을 포함한 당해 연도의 정보보호 실행계획을 수립 | 최고경영층이 실행계획을 승인하고 정보보호 최고책임자가 추진 상황을 매 반기마다 점검 | source-derived; exact wording unverified |
| 15 | essay | 유닉스 시스템에 저장된 파일에 다음과 같은 권한이 설정되었다. 권한의 상세한 의미를 설명하시오. [설정된 권한] -rwxr-x--x | 해당 파일의 소유자는 읽고 쓰고 실행이 모두 가능함. 해당 파일의 그룹에 속한 사용자들은 읽고 실행은 가능하나 파일 쓰기(Write)는 불가함. 기타 다른 사용자들은 실행만 가능하며 파일을 읽고, 쓰기(Write)는 불가함. | source-derived; exact wording unverified |
| 16 | essay | 재해복구시스템 유형에는 미러사이트, 핫사이트, 웜사이트, 콜드사이트가 있다. 다음 물음에 답하시오. 1) 미러사이트의 정의 - 주센터와 동일한 수준의 시스템을 백업센터에 구축하고, 액티브-액티브 상태로 실시간 동시 서비스를 제공하는 방식 2) 미러사이트의 장단점 각 2개씩 설명 - 장점) 신속한 업무재개 가능(RTO: 즉시), 데이터의 최신성 보장(RPO: 0) - 단점) 초기 투자 및 유지보수 비용이 높음, 데이터 업데이트가 많은 경우 과부하 초래 3) RTO가 가장 오래 걸리는 방식은 무엇이며, 이유는 무엇인가? | COLD 사이트, 데이터만 원격지에 보관하고 서비스를 위한 정보자원은 최소한으로 확보되어 있어, 재해 시 필요한 자원을 조달하여 복구하는데 오랜 시간이 소요됨 | source-derived; exact wording unverified |
| 17 | practical | 다음 자바 프로그램은 SQL Injection에 취약한 소스와 취약점을 해소한 소스코드이다. ( )에 들어갈 코드를 작성하시오. [취약한 소스코드] 1: // 외부로부터 입력받은 값을 검증 없이 사용할 경우 안전하지 않다. 2: String gubun = request.getParameter("gubun"); 3: ........ 4: String sql = "SELECT * FROM board WHERE b_gubun = '"+gubun+"'"; 5: Connection con = db.getConnection(); 6: Statement stmt = con.createStatement(); 7: // 외부로부터 입력받은 값이 검증 또는 처리 없이 쿼리로 수행되어 안전하지 않다. 8: ResultSet rs = stmt.executeQuery(sql); [취약점을 해소한 소스코드] 1: String gubun = request.getParameter("gubun"); 2: ........ 3: //1. 사용자에 의해... | (A) : ?, (B) : preparedStatement, (C) : setString, (D) : executeQuery() | source-derived; exact wording unverified |
| 18 | practical | NTP 서비스 취약점을 이용한 DDoS 공격 대응방안 4가지를 서술하시오. 1) 서버측면 대응 방안 2가지 1-1) NTP 서버 버전 업그레이드 : monlist 기능이 제거된 버전(4.2.8 이상)으로 업그레이드 하기 1-2) NTP 서버 버전 업그레이드 불가 시 monlist 기능 비활성화 : /etc/ntp.conf 파일에 "disable monitor" 설정 2) 네트워크 측면 대응 방안 2가지 | 서버 측면: NTP 서버를 4.2.8 이상으로 업그레이드하거나 `disable monitor`로 monlist 기능을 비활성화한다. 네트워크 측면: 신뢰할 수 있는 관리망·클라이언트만 NTP 접근을 허용하도록 ACL/방화벽을 적용하고, 외부에서 내부 NTP 서버로 들어오는 UDP/123 트래픽 또는 비정상 대량 NTP 응답 트래픽을 차단·속도 제한한다. | source-derived; Naver cross-checked; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they must still be rechecked against the password-protected PDFs when the password is available.
- Legal/regulatory answers should be checked against current statutes before memorization.
