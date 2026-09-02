---
title: 정보보안기사 실기 28회 2025년 1회 복원
page_type: dataset
tags:
- information-security
- certification
- exam-reconstruction
date_created: '2026-07-03'
date_updated: '2026-07-06'
source_paths:
- raw/sources/clipping/a0d2e8c6d316242a9b9abd35b6fb37a7aea8c29cc828024465495199a5b9648a/9f085cff41ff1e39b01198df625362e8633cf91457fc7cb1848050b22fe0dc2b/manifest.json
summary: 2025년 1회 정보보안기사 실기 28회 복원 문항을 단답형·서술형·실무형 동일 구조로 정리한 검증본. Naver category
  post was added as a cross-check source.
---

## Overview










# 정보보안기사 실기 28회 2025년 1회 복원

### Scope
- Source classification: Naver category post and Jaesung category pages contained explicit practical exam restoration posts for this round.
- This file is a paraphrased reconstruction, not a verbatim copy of the blog post.
- Count: 18 items = 12 short-answer, 4 essay, 2 practical.

### Reconstruction
| no | type | reconstructed prompt | answer | verification |
|---:|---|---|---|---|
| 1 | short | 반사 서버를 경유하여 대량의 ICMP echo reply 패킷을 전송해 서비스 거부를 유발하는 공격을 (A)라고 한다. 반사 서버로 악용되지 않기 위해 차단해야 하는 (B) 패킷과 (C) 패킷을 쓰시오. | Smurf, Directed Broadcast, ICMP echo request | PDF compilation cross-check restored prompt condition |
| 2 | short | 공격자가 서버가 신뢰하는 특정 서버나 네트워크 리소스에 대해 임의 요청을 보내도록 서버를 속이는 웹 보안 취약점이다. 서버가 외부 입력을 기반으로 HTTP 요청을 생성하는 기능을 가질 때 주로 발생하는 이 취약점명을 쓰시오. | SSRF | PDF compilation cross-check restored prompt condition |
| 3 | short | VLAN 빈칸을 채우시오. 수동으로 VLAN 주소를 할당하는 방식 (A), 자동으로 VLAN 주소를 할당하는 방식 (B), Cisco 스위치에서 VLAN을 확인하는 명령어 (C)를 쓰시오. | 정적 VLAN, 동적 VLAN, show vlan | PDF compilation cross-check restored prompt condition |
| 4 | short | 웹 브라우저에서 JavaScript `document.cookie` 등을 통해 쿠키에 접근하는 행위를 차단하려면 쿠키에 어떤 보안 속성을 설정해야 하는지 쓰시오. | HttpOnly | PDF compilation cross-check restored prompt condition |
| 5 | short | HTTP 요청 메시지 입력값이 HTTP 응답 헤더에 포함되어 응답이 여러 개로 분리되는 HTTP 응답 분할(Response Splitting) 공격에서, 추가 HTTP 응답 생성·쿠키 탈취·XSS 등에 악용되는 개행 문자 2개를 쓰시오. | CR, LF | PDF compilation cross-check restored prompt condition |
| 6 | short | APT 공격 대응을 위해 록히드 마틴사가 제시한 방법으로, 공격 단계를 7단계로 분리하고 그중 하나만 사전에 제거해도 실제 공격까지 이어질 수 없다는 점에 착안한 방어 전략을 쓰시오. | 사이버 킬 체인 | PDF compilation cross-check restored prompt condition |
| 7 | short | 시스템이 공격자가 설치한 루트킷 등으로 장악되면 `ps` 같은 기본 명령어를 신뢰할 수 없을 수 있다. 이때 `ps` 대신 실행 중인 프로세스들이 오픈한 파일 목록을 확인하는 명령어를 쓰시오. | lsof | PDF compilation cross-check restored prompt condition |
| 8 | short | 리눅스에서 로그인 실패 로그는 `btmp` 파일에 남는다. `btmp` 로그 내용을 확인하는 명령어를 쓰시오. | lastb | PDF compilation cross-check restored prompt condition |
| 9 | short | 정보자산 중요도 평가 기준은 일반적으로 기밀성, 무결성, (A)를 고려한다. 또한 정보자산 (B)을 통해 유사 특성의 자산을 하나의 그룹으로 묶어 위험분석 및 보호대책 수립을 효율적이고 일관되게 적용할 수 있다. | 가용성, 그룹핑 | PDF compilation cross-check restored prompt condition |
| 10 | short | 조직의 정보자산을 위협으로부터 보호하고 손실을 최소화하기 위해 위험관리 방법 및 절차, 수행 인력, 기간, 대상, 방법, 예산 등을 구체화하여 수립하는 계획 문서를 쓰시오. | 위험관리계획 | PDF compilation cross-check restored prompt condition |
| 11 | short | ISMS-P 인증에서 요구하는 물리적 보안 대책 중 3가지를 설명하시오. | 보호구역 지정, 출입통제, 정보시스템 보호, 보호설비 운영, 보호구역 내 작업 통제, 반출입 기기 통제, 업무환경 보안 중 3개 | PDF compilation cross-check restored prompt condition |
| 12 | short | 모바일 기기에서 링크에 접속하면 설치된 앱이 실행되고 특정 화면으로 이동되는 기능이다. 악용 시 특정 웹페이지를 악성 링크로 접속하도록 조작해 개인정보 조회나 의도하지 않은 계좌이체를 유도할 수 있는 이 기능명을 쓰시오. | Deep link | PDF compilation cross-check restored prompt condition |
| 13 | essay | 쉘의 정의와 기능 두 가지를 설명하시오. | 운영체제와 사용자 사이의 명령 인터페이스이며, 명령 해석·커널 전달·환경 설정·스크립트 자동화 등을 수행한다. | PDF compilation cross-check restored prompt condition |
| 14 | essay | Windows OS에서 사용하는 NetBIOS 바인딩이 보안상 취약한 이유와 `ncpa.cpl`을 이용한 보안 설정 방법을 설명하시오. | 인터넷 연결 Windows에서 NetBIOS over TCP/IP가 활성화되면 원격 공유자원 접근 위험이 있다. ncpa.cpl에서 네트워크 어댑터 속성 > TCP/IP 고급 > WINS 탭에서 NetBIOS over TCP/IP 사용 안 함을 선택한다 | PDF compilation cross-check restored prompt condition |
| 15 | essay | IPSec의 정의와 보안 모드 두 가지를 설명하시오. | 네트워크/IP 계층에서 IP 패킷 단위 인증(AH), 암호화(ESP), 키관리(IKE)를 수행하는 프로토콜이다. 터널모드는 새 IP 헤더를 추가해 패킷 전체를 보호하고, 전송모드는 원 IP 헤더 외 데이터 부분을 보호한다 | PDF compilation cross-check restored prompt condition |
| 16 | essay | 정보자산 중요도 산정의 개념과 필수 기준 3가지를 설명하시오. | 자산이 조직에 주는 가치와 손실 영향을 평가해 보호 우선순위를 정하는 절차다. 해당 자산의 기밀성, 무결성, 가용성 등급을 평가해 중요도를 산정한다 | PDF compilation cross-check restored prompt condition |
| 17 | practical | Oracle 감사 로그 설정 결과 `audit_file_dest string /u01/app/oracle/admin/ORCL/adump`, `audit_sys_operations boolean FALSE`, `audit_syslog_level string LOCAL0.INFO`, `audit_trail string NONE`을 보고 답하시오. 1) 설정 의미를 설명하시오. 2) 감사 로그를 `SYS.AUD$` 테이블에 저장하려면 어떤 값을 수정해야 하는가? 3) 감사 로그를 DB 내부보다 외부에 남기는 것이 좋은 이유를 보안 측면에서 설명하시오. | audit_file_dest는 OS 감사 로그 저장 경로, audit_sys_operations=FALSE는 SYS 계정 감사 미수행, audit_syslog_level은 syslog 전송 등급, audit_trail=NONE은 감사 로그 미저장을 의미한다. SYS.AUD$에 저장하려면 audit_trail을 DB로 변경한다. 외부 저장은 DB 장악 시 로그 위변조를 줄이고 SIEM 연계와 신뢰 가능한 증거 확보에 유리하다 | PDF compilation cross-check restored prompt condition |
| 18 | practical | 리눅스 OS 접속 화면 (A)는 Telnet으로 `192.168.10.20` 접속 시 `Ubuntu 20.04.6 LTS`, 커널 정보, `server01 login: root`, root 로그인 성공이 표시된다. (B)는 FTP로 `192.168.10.30` 접속 시 `220 Welcome to vsFTPd 3.0.3`, `Name (...:root): root`, `230 Login successful`이 표시된다. 1) A와 B에서 확인된 취약점은 무엇인가? 2) A 대응 방안은? 3) B 대응 방안은? | Telnet/FTP 평문 서비스, OS·커널·데몬 버전 배너 노출, root 직접 로그인 허용이 취약점이다. Telnet은 SSH로, FTP는 SFTP/FTPS로 대체하고 root 직접 로그인을 차단하며, issue.net·vsftpd 배너 설정 등으로 상세 버전 노출을 제거한다 | PDF compilation cross-check restored prompt condition |

### Verification Notes
- Completeness: primary source exposes 18 numbered items and one attached PDF for the same round.
- Confidence: high for item count and answer topics; medium for exact original wording because KCA does not publish official practical question text.
- Known normalization: item 11 was normalized to ISMS-P physical security control terminology. Items 14~16 follow the Naver post order: NetBIOS, IPsec, asset importance.

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

- `raw/sources/clipping/a0d2e8c6d316242a9b9abd35b6fb37a7aea8c29cc828024465495199a5b9648a/9f085cff41ff1e39b01198df625362e8633cf91457fc7cb1848050b22fe0dc2b/manifest.json`
