---
title: "정보보안기사 실기 24회 2023년 4회 실기 복원"
tier: llm-synthesis
page_type: dataset
domain: information-security
domain_confidence: high
shared_scope: domain
tags: [information-security, certification, exam-reconstruction]
status: active
date_created: 2026-07-03
date_updated: 2026-07-07
source_paths:
  - "https://it-utopia.tistory.com/entry/정보보안기사-2023년-24회-정보보안기사-실기-기출문제-복원"
  - "https://blog.naver.com/stereok2/223403908181"
  - "raw/sources/web/information-security-exam-references/pipc-privacy-impact-assessment-guide-2025-10.md"
  - "raw/assets/information-security-exam-references/pipc-privacy-impact-assessment-guide-2025-10.pdf"
source_count: 4
provenance: inferred
summary: "정보보안기사 실기 24회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction, Naver blog cross-check, PIPC/KISA 개인정보영향평가 수행 안내서 formula cross-check for item 1."
evergreen: false
---

# 정보보안기사 실기 24회 2023년 4회 실기 복원

## Scope
- Exam mapping: 2023년 4회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223403908181`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


## Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 개인정보보호위원회와 한국인터넷진흥원에서 발간한 "개인정보영향평가 수행 안내서"에 따르면 위험도 산정 공식을 다음과 같이 제시하고 있다. ( )에 들어갈 항목명을 기술하시오. [위험도 산정 공식] 위험도 = 자산가치(영향도) + ((A) * (B)) * (C) | (A) : 침해요인 발생 가능성, (B) : 법적 준거성, (C) : 2 | PIPC/KISA guide formula cross-checked: `자산 가치(영향도) + (침해요인 발생가능성 * 법적 준거성) * 2`; C is the constant multiplier 2, not 조직의 위험 수용 수준 |
| 2 | short | DB 암호화 기법에 대한 설명이다. ( )에 해당하는 기법의 명칭을 기술하시오. - (A) : 암복호화 모듈이 API 라이브러리 형태로 각 애플리케이션 서버에 설치되고, 응용프로그램에서 암복호화 모듈을 호출하는 방식 - (B) : 암복호화 모듈이 DB서버에 설치되고 DBMS에서 플러그인으로 연결된 암복호화 모듈을 호출하는 방식 - (C) : DBMS에 내장되어 있는 암호화 기능을 이용하여 암복호화 처리를 수행하는 방식 | (A) : API, (B) : Plug-in, (C) : TDE(Transparent Data Encryption) | source-derived; exact wording unverified |
| 3 | short | LAN 스위칭 기법에 대한 설명이다. ( )에 해당하는 기법의 명칭을 기술하시오. - (A) : 프레임의 헤더(목적지 주소)만을 보고 경로를 결정하는 방식 - (B) : 프레임의 앞 64바이트만을 읽어 에러를 처리하고, 목적지 포트로 포워딩 하는 방식 - (C) : 전체 프레임을 받은 다음 경로를 결정하는 방식 | (A) : Cut through, (B) : Modified Cut through(Fragment Free), (C) : Store and Forward | source-derived; exact wording unverified |
| 4 | short | EAP를 통해 인증을 수행하고 AES-CCMP 기반 암호화를 지원하는 무선랜 보안 표준은? | WPA2 | source-derived; exact wording unverified |
| 5 | short | VLAN(Virtual LAN)의 주소 할당 방법에 대한 설명이다. ( )에 해당하는 방식명을 기술하시오. - (A) : VLAN 할당을 관리자가 각 스위치에 직접 할당하는 방식 - (B) : MAC주소 등을 기반으로 VLAN 할당이 자동으로 이루어지는 방식 | (A) : 정적 VLAN(포트 주소 기반), (B) : 동적 VLAN(MAC 주소 기반) | source-derived; exact wording unverified |
| 6 | short | 검색로봇에게 웹사이트의 페이지를 수집할 수 있도록 허용/제한하는 국제 권고안으로 웹사이트의 루트 디렉터리에 위치해야 하며, 로봇 배제 표준을 따르는 일반 텍스트 파일(text/plain)로 작성해야 하는 파일명은 무엇인가? | robots.txt | source-derived; exact wording unverified |
| 7 | short | ISO 31000 위험평가 방법론에 따른 위험평가 절차에 대한 설명이다. ( )에 들어갈 위험평가 단계명을 기술하시오. - (A) : 운영 실패, 공급망 중단 또는 인재 격차와 같은 외부 및 내부 위험을 고려하여 잠재된 위험 식별 - (B) : 확인된 위험이 조직의 목표 및 운영에 미칠 가능성과 잠재적 영향을 분석 - (C) : 조직의 위험 감수성(Risk Appetite), 수용 능력, 위험과 보상 간의 균형을 고려하여 위험 허용 수준(DoA)을 결정하고, 위험의 중요성에 따라 위험 처리 필요성을 결정 | (A) : 위험식별, (B) : 위험분석, (C) : 위험평가 | source-derived; exact wording unverified |
| 8 | short | 다음과 같은 기능을 수행하는 정보보호 솔루션의 이름은 무엇인가? - PC에 설치된 에이전트, 네트워크 센서를 통하여 이동식 디스크, 이메일, 메신저, 웹사이트 파일 업로드 등 내부 문서 이동을 탐지 - HTTPS와 같은 암호화 통신에서도 중요 내부 문서 이동 탐지 가능 - 일부 솔루션에서는 파일 암호화, 파일 삭제와 같은 부가 기능 탑재 | DLP(Data Loss Prevention) | source-derived; exact wording unverified |
| 9 | short | 유닉스에서 현재 실행되고 있는 프로세스 정보가 기록되며, 숨겨진 프로세스를 찾기 위해 참조하는 경로는 / (A) 이다. | proc | source-derived; exact wording unverified |
| 10 | short | 다음 아파치 로그를 보고 물음에 답하시오. [아파치 로그] 200.3.1.4 - - [30/May/2023:01:20:01 +09:00] "(1) GET /bulletin/read.php?no=101&item=book (2) HTTP/1.1" 200 3549 (3) http://test.co.kr/main.php" "Mozilla/5.0 (compatible;MSIE 10.0;Windows NT 6.1;WOW64;Trident/6.0)" (1) no=101&item=book의 의미는? - /bulletin/read.php 파일을 GET 방식으로 호출할 때 2개의 파라미터(no, item)에 값을 각각 할당하여(no=101 and item=book) 매칭되는 결과를 요청 (2) http 상태코드는 무엇인가? - 200 (웹서버가 요청을 정상적으로 처리했음을 의미) (3) http://test.co.kr/main.php 의 의미는? | 현재 URL을 호출한 referer URL을 의미(test.co.kr/main.php에서 GET 방식으로 현재 URL(/bulletin/read.php)를 호출) | source typo normalized for Apache request line spacing/path spelling; answer unchanged |
| 11 | short | 개인정보 가명처리 기법 중 수치 데이터를 임의의 수인 자리수, 실제 수 기준으로 올림 또는 내림 처리하는 기법의 명칭은 무엇인가? | 랜덤 라운딩 | source-derived; exact wording unverified |
| 12 | short | 아파치 SW 재단에서 개발한 JAVA 기반의 오픈소스 프로그램으로 자바기반 프로그램을 개발할 때 로그를 쉽고 편하게 남기기 위한 목적으로 사용된다. 2021년 말 이 프로그램의 JNDI Lookup 메소드를 호출할 때 입력값에 대한 검증 없이, 임의의 코드가 실행되는 취약점이 발견되어 전세계를 떠들썩하게 만들었던 프로그램의 이름은 무엇인가? | Log4J | source-derived; exact wording unverified |
| 13 | essay | 다음의 두 가지 조치의 의미와 이 조치가 필요한 이유를 설명하시오. 1) chmod -s { 파일명 } 2) find / -user root -type f \(-perm -4000 -o -perm -2000 \) \|xargs ls -al (1) 두 가지 조치의 의미 - 특정 파일에 설정된 특수 비트(SetUID, SetGID)를 제거함 - / 경로 하위에 존재하는 root가 소유주인 파일 중 특수비트(SetUID, SetGID)가 설정된 파일을 검색함 (2) 두 가지 조치가 필요한 이유 | 특수비트가 설정된 파일을 실행하는 경우 파일의 소유주(SetUID 설정 시), 또는 소유그룹(SetGID 설정 시) 권한으로 실행 됨. 특히 root가 소유주 또는 소유그룹인 파일에 특수비트가 설정되면, 일반 사용자 계정으로 실행하더라도 root 권한으로 실행되어 악의적인 행위가 가능하기 때문 | source-derived; Naver cross-checked; official wording unverified |
| 14 | essay | rsh, rlogin, rexec 등은 인증 없이 관리자의 원격접속을 가능하게 하는 명령어들이므로 사용하지 않는 것이 안전하다. 불가피하게 사용하는 경우 `/etc/hosts.equiv`, `$HOME/.rhosts` 파일의 소유자, 권한, 파일 내 보안설정을 어떻게 해야 안전한지 설명하시오. | `/etc/hosts.equiv` 소유자는 root, `$HOME/.rhosts` 소유자는 해당 계정으로 설정한다. 두 파일 권한은 600 이하로 제한한다. 파일 내부의 `+` 설정은 제거하고 허용할 호스트와 계정만 명시한다. | source-derived; exact wording unverified |
| 15 | essay | IPTables와 관련해 1) INPUT, FORWARD, OUTPUT Chain을 설명하고, 2) `iptables -A INPUT -p tcp ! --syn -m state --state NEW -j LOG --log-prefix "[Faked NEW request]"` 룰의 의미를 설명하시오. | INPUT은 방화벽이 최종 목적지인 패킷, FORWARD는 방화벽을 경유하는 패킷, OUTPUT은 방화벽에서 출발하는 패킷에 적용되는 체인이다. 해당 룰은 신규 TCP 연결 패킷인데 SYN이 아닌 경우 `[Faked NEW request]` 접두어로 로그를 남긴다는 의미다. | source-derived; exact wording unverified |
| 16 | essay | SNMP 서비스 사용 시 적용되어야 하는 보안 설정 4가지를 설명하시오. | 커뮤니티 스트링을 기본값이 아닌 유추하기 어려운 값으로 변경한다. 암호화를 지원하는 SNMPv3를 사용한다. ACL로 SNMP 이용 가능 호스트를 제한한다. RW(Read-Write) 모드는 제거하고 가급적 RO(Read-Only) 모드를 사용한다. | source-derived; exact wording unverified |
| 17 | practical | A 기업에서는 다양한 유닉스 계열 서버를 운영하고 있다. Solaris, Linux, AIX, HP-UX 서버에서 패스워드 최소 길이를 8자리 이상으로 강화하기 위한 설정 파일과 설정값을 기술하시오. | Solaris: `/etc/default/passwd`의 `PASSLENGTH=8`; Linux: `/etc/login.defs`의 `PASS_MIN_LEN 8`; AIX: `/etc/security/user`의 `minlen=8`; HP-UX: `/etc/default/security`의 `MIN_PASSWORD_LENGTH=8` | source-derived; Naver cross-checked; official wording unverified |
| 18 | practical | xinetd 서비스에 대한 환경설정 파일에서 (1) ~ (4)에 적절한 값을 기술하시오. # cd /etc/xinetd.d/ # cat telnet service telnet { flag = REUSE # 서비스 포트가 사용중인 경우 해당포트 재사용 허용 socket_type = stream # TCP 프로토콜 선택 wait = no # 한번에 다중사용자에게 서비스 제공 user = root # root 권한으로 실행 server = /usr/sbin/in.telnetd # 실행할 데몬 파일 log_on_failure += USERID # 서버 접속 실패 시 USERID를 로그에 기록 disable = no # 서비스 사용 ( 1 ) = 10.0.0.0/8 # 10.0.0.0/8 대역은 서비스 미허용 ( 2 ) = 192.168.10.0/24 # 192.168.10.0/24 대역은 서비스 허용 ( 3 ) = 3 # 동시에 접속가능한 최대 세션 수 3개 access_time = ( 4 ) # 접속을 허용할 시간 (9시~18시) } | (1) no_access, (2) only_from, (3) instances, (4) 09:00-18:00 | source-derived; Naver cross-checked; CIDR typo normalized; official wording unverified |

## Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- 2026-07-07: Item 1 was checked against the PIPC/KISA 개인정보영향평가 수행 안내서 text. The source guide gives `위험도 = 자산 가치(영향도) + (침해요인 발생가능성 * 법적 준거성) * 2`; therefore `(C)` is the constant/multiplier `2`. It is not 조직의 위험 수용 수준; that concept appears in item 7's ISO 31000 위험평가 description. The reconstructed prompt says `항목명`, but the guide formula's third blank is a numeric multiplier rather than a named risk-management item.
- 2026-07-07: Items 2, 10, and 18 had reconstruction transcription defects from web-source wording (`방` truncation, Apache path spelling/spacing, and CIDR slash). These were normalized without changing the intended answers.
- Legal/regulatory answers should be checked against current statutes before memorization.
