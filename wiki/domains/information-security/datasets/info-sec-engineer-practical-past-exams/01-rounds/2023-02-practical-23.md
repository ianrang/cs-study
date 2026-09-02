---
title: 정보보안기사 실기 23회 2023년 2회 실기 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-04'
source_paths:
- raw/sources/clipping/7d6bd11fb5a4c8e78b40a9de11cfe7b44d4d359eb3076e707df25669d22d4950/1de1fc24f2756c7a5b23fe0c8e2cc2f25383c0de2274f5426d913216550a42b0/manifest.json
summary: '정보보안기사 실기 23회 복원 항목을 동일 표 구조로 정리한 페이지. 출처 상태: direct web reconstruction,
  Naver blog cross-check.'
---

## Overview




# 정보보안기사 실기 23회 2023년 2회 실기 복원

### Scope
- Exam mapping: 2023년 2회 실기.
- Source status: direct web reconstruction cross-checked with Naver blog `stereok2/223202583456`; confidence: high for topic coverage, official wording still unverified.
- This file stores paraphrased reconstruction notes, not verbatim source text.
- Local 1~28회 thodi-lab/blog-source PDF compilation was unlocked and text-extracted on 2026-07-06; KCA official wording is still not claimed.


### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 윈도우 OS 환경에서 특정 서비스의 로그 파일 저장 경로를 참고하여, ( )에 들어갈 로그 파일 경로를 기술하시오. (IIS 로그) `C:\Windows\inetpub\logs\Logfiles\W3SVC1`, `C:\Windows\inetpub\logs\Logfiles\MSFTPSVC1`, `C:\Windows\System32\LogFiles\(A)` (DHCP) `C:\Windows\System32\(B)` | (A) : `HTTPERR`, (B) : `dhcp` | source-derived; 2026-07-17 technical correction: Windows default DHCP path is not under LogFiles |
| 2 | short | System V AMD64 ABI를 따르는 64비트 리눅스에서 아래 프로그램 코드를 실행하려고 한다. `printf` 호출 시 서식 문자열은 RDI에, 문자 인자 A, B, C는 순서대로 어느 레지스터에 전달되는지 기술하시오. `int main() { printf("%c, %c, %c\\n", 'A', 'B', 'C');}` | A : RSI, B : RDX, C : RCX. RDI는 첫 번째 인자인 서식 문자열 포인터다. | source-derived; 2026-07-17 technical correction: printf format argument offset |
| 3 | short | 리눅스 환경에서 컴파일 과정에 관한 설명이다. ( )에 들어갈 용어를 기술하시오. - 리눅스 환경에서 ( A ) 방식으로 컴파일하는 경우, 외부 라이브러리 함수를 사용할 수 있도록 주소를 프로그램에 연결시켜주는 테이블인 ( B ) 를 참조한다. - ( B ) 는 실제 해당 함수의 주소가 들어 있는 ( C ) 를 참조하여 함수 주소를 얻어 온다. | (A) : Dynamic Linking, (B) : PLT(Procedure Linkage Table), GOT(Global Offset Table) | source-derived; exact wording unverified |
| 4 | short | 정보보호 및 개인정보 관리체계 인증(ISMS-P)은 인증 기준이 3개 영역, 102개 항목으로 세분화되어 있다. 이 중 3개 영역을 기술하시오. | 관리체계 수립 및 운영, 보호대책 요구사항, 개인정보 처리 단계별 요구사항 | source-derived; exact wording unverified |
| 5 | short | 유닉스의 `/var/log/message` 샘플이 다음과 같이 기록되어 있다. 로그를 5개 항목으로 나눌 때 (A)~(C)의 의미를 쓰시오. `Mar 29 14:23:57 alex kernel:(A) [295087,236116] (B) Call Trace: (C)` 뒤에 `Mar 29 14:23:57 alex kernel: [295087,236131] do_idle+0x83/0xf0`, `Mar 29 14:23:57 alex systemd [1] apt-daily-upgrade.service: Consumed 50.187s CPU time`가 이어진다. | (A) 로그를 생성한 프로그램/태그(`kernel`), (B) kernel 메시지의 대괄호 시간 표기, (C) 상세 로그 메시지다. 일반 syslog 태그의 `[PID]` 형식과 달리 이 kernel 샘플의 대괄호 수치는 PID로 단정할 수 없다. 실제 로그 경로·표기 형식은 배포판과 rsyslog/journald 설정에 따라 다르다. | PDF compilation cross-check restored the exact sample labels. Linux kernel documentation identifies bracketed printk time as a timestamp format; this corrects the compilation answer’s unsupported PID interpretation. This is a non-official blog compilation, not KCA wording. |
| 6 | short | SQL Injection 취약점을 대응하는 방법에 대한 설명이다. ( )에 들어갈 용어를 설명하시오. (공격 대상 SQL 구문) string query = "select * from member a where gubun = '" + a.gubun "'" (대응 방법) 외부로부터 입력받은 값을 검증하지 않고, SQL문을 생성하는데 그대로 사용하는 경우 문제가 발생할 수 있다. 즉, gubun 값으로 a' or 'a' = 'a를 입력하는 경우 쿼리가 항상 참이 되므로 member 테이블의 모든 내용이 조회된다. 이에 대한 대응 방안으로 파라미터를 받는 ( ) 객체를 상수 스트링으로 정의하고, 파라미터를 setString과 같은 메소드로 설정하면 외부의 입력이 쿼리문의 구조를 바꾸는 것을 예방할 수 있다. | Prepared Statement | source-derived; exact wording unverified |
| 7 | short | 리눅스의 PAM(Pluggable Authentication Module) 모듈의 종류에 대한 설명이다. ( )에 들어갈 모듈명을 기술하시오. 1) ( A ) : 실질적인 인증 기능, 패스워드 확인을 담당하는 모듈 2) ( B ) : 사용자의 시스템 사용 권한을 확인하는 모듈 3) password : 패스워드를 설정하거나 확인하는 데 사용하는 모듈 4) ( C ) : 사용자가 인증 성공 시 세션을 맺어주는 모듈 | (A) : auth, (B) : account, (C) : session | source-derived; exact wording unverified |
| 8 | short | Salvatore Sanfilippo가 개발한 보안 테스트 툴로 ICMP, TCP, UDP 등과 같은 다양한 프로토콜을 지원한다. 다량의 공격용 패킷을 생성하여 DDoS 훈련 목적으로도 사용하는 이 툴의 이름은 무엇인가? | hping3 | source-derived; exact wording unverified |
| 9 | short | 보안 점검 도구에 대하여 ( )에 들어갈 명칭을 기술하시오. - Tripwire는 ( A ) 을 점검하는 도구이다. - ( B ) 는 미국 Tenable사가 개발하였고, 네트워크에 연결된 다양한 종류의 시스템에 대하여 자동화된 취약점 스캔을 지원하며 광범위한 취약점 DB를 가지고 있다. | (A) : 무결성, (B) : Nessus | source-derived; exact wording unverified |
| 10 | short | CVE-2014-0160으로 알려진 오픈 SSL 취약점이다. 오픈 SSL의 하트비트 체크 로직의 취약점을 악용하여 시스템 메모리에서 중요 데이터를 탈취할 수 있는 이 취약점의 이름은 무엇인가? | 하트블리드(HeartBleed) | source-derived; exact wording unverified |
| 11 | short | 위험관리 3단계에 대한 설명이다. ( )에 들어갈 단계명을 기술하시오. - ( A ) : 자산의 위협과 취약점을 분석하여 보안 위험의 종류와 규모를 결정하는 과정 - ( B ) : 식별된 자산, 위협 및 취약점을 기준으로 위험도를 산출하여 기존의 보호대책을 파악하고 위험의 대응 여부와 우선 순위를 결정하기 위한 평가 과정 - 대책 선정 : 허용가능 수준으로 위험을 줄이기 위해 적절하고 정당한 정보보호 대책을 선정하고 이행 계획을 수립하는 과정 | (A) : 위험분석, (B) : 위험평가 | source-derived; exact wording unverified |
| 12 | short | 위험관리를 위한 정보자산 분석 절차에 대한 설명이다. ( )에 들어갈 단계명을 기술하시오. - ( A ) : 보호받을 가치가 있는 자산을 식별하고, 이를 정보자산의 형태, 소유자, 관리자, 특성 등을 포함하여 자산 목록을 작성 - 자산 관리자 지정 : 식별된 정보자산에 대하여 책임자 및 관리자 지정 - ( B ) : 식별된 자산에 대해 침해 사고가 발생할 경우 그 영향을 기밀성, 무결성, 가용성 측면에서 파악하여 자산의 중요도를 선정 | (A) : 정보자산 식별, (B) : 정보자산 중요도 평가 (서술형) | source-derived; exact wording unverified |
| 13 | essay | PHP 게시판 업로드 코드가 파일명 확장자를 `explode(".")`로 분리해 `hwp`, `pdf`, `jpg`만 허용하고, 업로드 MIME type이 `image/gif`, `image/jpeg`, `image/JPG`, `text/plain`이면 성공 처리한다. 취약점명, Content-Type 변조·대소문자/이중확장자·Null byte 삽입 등 우회 기법, 업로드 파일이 실행 제한 설정에 걸리지 않아야 한다는 공격 성공 조건을 설명하시오. | 파일 업로드 취약점. 클라이언트 제공 Content-Type·확장자 검사만 신뢰하면 변조·대소문자·이중 확장자로 우회될 수 있다. Null byte 우회는 NUL 종료를 잘못 처리하는 **레거시** 구성요소에서만 가능한 예이므로 일반 정답으로 단정하지 않는다. 공격 성공에는 필터 우회뿐 아니라 업로드 파일이 웹에서 도달 가능하고 서버가 해당 형식을 실행 가능한 handler에 매핑한 조건이 필요하다. | OWASP File Upload Cheat Sheet cross-check. This preserves source-derived examples without generalizing a version-dependent Null byte bypass. |
| 14 | essay | TCP 헤더에 포함되어 있는 6비트의 Flag에 대한 설명이다. ( )에 적절한 설명을 기술하시오. - URG : 긴급하게 전송할 데이터가 있는 경우 사용하며, 순서에 상관없이 우선순위를 높여 처리됨 - PSH : 버퍼링된 데이터를 버퍼가 찰 때까지 기다리지 않고 수신 즉시 애플리케이션 계층으로 전달 - SYN : ( A ) - ACK : ( B ) - FIN : ( C ) | RST : ( D ) (A) : 최초 연결 수립을 요청하고, 순서 번호를 동기화할 때 사용됨 (B) : 상대로부터 패킷을 받았다는 것을 알려주며, 일반적으로 받은 시퀀스 번호에 +1 하여 응답을 보냄 (C) : 송신 장비가 연결 종료를 요청 시 사용 (D) : 연결 상의 문제가 발생한 비정상 세션을 강제로 끊을 때 사용 | source-derived; exact wording unverified |
| 15 | essay | 윈도우OS에서 사용하는 NetBIOS 바인딩이 보안상 취약한 이유와 보안 설정하는 방법을 설명하시오(보안 설정은 ncpa.cpl을 이용하여 설명). 1) 보안상 취약한 이유 : 인터넷에 직접 연결되어 있는 윈도우 시스템에 NetBIOS TCP/IP 바인딩이 활성화되어 있는 경우, 공격자가 원격에서 네트워크 공유자원을 사용할 우려가 존재하기 때문 2) 보안설정 방법 : 윈도우 OS에서 시작 > 실행 > ncpa.cpl > 로컬 영역 연결 > 속성 > TCP/IP > (일반) 탭에서 (고급) 클릭 > (WINS) 탭에서 TCP/IP에서 "NetBIOS 사용 안 함" 또는 "NetBIOS over TCP/IP 사용 안 함" 선택 | NetBIOS over TCP/IP 바인딩을 비활성화하여 원격 공유자원 노출 위험을 줄인다. | source-derived; Naver cross-checked; official wording unverified |
| 16 | essay | 1초에 1000번 이상 유입되는 HTTP 요청이 `GET /test.jsp`, `Host: webserver.com`, `User-Agent: Mozilla/5.0`, `Referer: http://www.abc.com/default.jsp (a)`, `Cache-Control: max-age=0 (b)` 헤더를 포함한다. `a`, `b`를 근거로 공격명을 쓰고 판단 사유를 설명하시오. | 고빈도 요청은 HTTP GET Flooding을 의심할 근거가 된다. `max-age=0`은 캐시된 응답을 재검증하도록 할 수 있어 원본 부하에 기여할 수 있으나, Referer가 다른 도메인이라는 사실은 공격·경유 요청의 증거가 아니다. 공격 확정에는 출발지 분포, 요청률, 서버 자원 고갈, 정상 트래픽 비교가 필요하다. | source-derived; 2026-07-17 technical correction: header evidence boundary |
| 17 | practical | 코로나 극복 후 새로운 서비스를 재개하려는 소상공인이 있다. 기존에 보유하고 있던 1만명 미만의 고객 정보를 프리미엄 서비스에 활용하는 경우 개인정보의 안전성 확보조치 기준에 따라 개인정보처리시스템 접근권한 관리, 접근통제를 위해 준수해야 할 사항을 기술하시오. | 접근권한 관리: 인사이동 시 접근권한을 지체 없이 변경·말소하고, 권한 부여·변경·말소 내역을 최소 3년 보관하며, 개인정보취급자별 사용자계정을 발급하고 공유를 금지한다. 접근통제: IP 등으로 인가받지 않은 접근을 제한하고, 접속 IP 등을 분석해 불법 개인정보 유출 시도를 탐지·대응한다. | source-derived; Naver cross-checked; official wording unverified |
| 18 | practical | Korea.co.kr 도메인의 존 파일을 설정하려고 한다. MASTER와 SLAVE DNS 서버의 named.conf 설정값을 각각 작성하시오(zone 파일은 ns.korea.co.kr.zone 이다.). - master name 서버 : ns1.korea.co.kr (192.168.1.53) - slave name 서버 : ns2.korea.co.kr (192.168.2.53) | Master 예: `zone "korea.co.kr" IN { type master; file "ns.korea.co.kr.zone"; allow-transfer { 192.168.2.53; }; };` Slave 예: `zone "korea.co.kr" IN { type slave; file "slave/ns.korea.co.kr.zone"; masters { 192.168.1.53; }; };`. `zone` 문자열은 설정하려는 `korea.co.kr`이고, 파일명 `ns.korea.co.kr.zone`은 이를 바꾸지 않는다. Slave가 zone을 받는 권한은 `allow-update`가 아니라 master의 `allow-transfer`로 제한한다. | source-derived; 2026-07-17 technical correction: BIND zone name and transfer/update distinction |

### Verification Notes
- Exact official KCA/KISA practical question wording is not available in this workspace.
- Rows are normalized from accessible web reconstructions and cross-checked against the Naver blog reconstruction listed in `source_paths`; they were cross-checked against the unlocked thodi-lab/blog-source PDFs where in 1~28 scope; KCA official wording is still not claimed.
- Legal/regulatory answers should be checked against current statutes before memorization.

## Schema / Composition

## Usage

## Limitations / Biases

## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|


## Relations

| type | target | notes |
|---|---|---|


## Sources

- `raw/sources/clipping/7d6bd11fb5a4c8e78b40a9de11cfe7b44d4d359eb3076e707df25669d22d4950/1de1fc24f2756c7a5b23fe0c8e2cc2f25383c0de2274f5426d913216550a42b0/manifest.json`
