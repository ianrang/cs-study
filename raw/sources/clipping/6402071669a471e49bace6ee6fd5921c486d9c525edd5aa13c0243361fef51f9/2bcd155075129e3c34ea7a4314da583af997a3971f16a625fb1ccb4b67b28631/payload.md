---
title: "정보보안기사 실기 2장 — 네트워크 보안"
tier: llm-synthesis
page_type: method
domain: information-security
domain_confidence: high
shared_scope: domain
tags: []
status: active
date_created: 2026-07-11
date_updated: 2026-07-12
source_paths:
  - raw/assets/information-security-exam-references/kca-info-security-engineer-criteria-2023-2026.pdf
  - cs/information-security/02.network-security/
  - cs/information-security/study/02.network-security/
source_count: 3
provenance: extracted
summary: "정보보안기사 실기의 프로토콜·패킷·네트워크 공격·보안장비·설정·로그 분석을 우선순위와 답안 형태로 통합한 학습 문서."
evergreen: false
---

# 2 네트워크 보안

> 목표: 프로토콜·패킷·장비 설정을 보고 **정상 동작, 공격 원리, 판단 근거, 보완 방법**을 답안으로 쓴다. 이 문서는 KCA 실기 출제기준의 `프로토콜별 보안특성`, `보안장비 및 네트워크 장비별 보안특성`, `네트워크 및 보안장비 설정 점검과 보완`, `패킷 로그 분석` 범위를 시험용으로 정리한다.

> 이 장만 학습할 때는 `0 학습 지도 → 2.1~2.6 본문 → 2.7 P1 체크리스트 → 기출 적용` 순서로 본다. 2.8 P3는 시간이 남을 때 확장하고, 마지막에는 2.9의 회독 기준으로 스스로 답을 써 본다.

> 이 문서는 2장 개념 복습의 기준 문서로 사용한다. PDF를 다시 대조할 필요는 없지만, 새로운 자료를 읽는 것과 **기출 문제의 답을 직접 쓰는 훈련**은 다르다. 본문을 읽은 뒤에는 반드시 기출에서 근거 표시와 답안 작성을 수행한다.

## 0. 학습 우선순위와 출제 패턴

### 태그 규칙

- **[P1]**: 다음 주 기출 풀이 전 반드시 즉답·서술 가능한 핵심. 최근성·반복성·공식 기준이 모두 강하다.
- **[P2]**: P1을 마친 뒤 연결해서 준비할 변형·실무형 대비 항목.
- **[P3]**: 저빈도 또는 장비·버전 종속 세부. 정의와 보안 목적을 우선 기억한다.
- **[답안]**: 단답형, 서술형, 실무형에서 점수로 바꾸는 문장 구조다.

### 한눈에 보는 이해 흐름

```text
정상 동작 파악        공격자가 악용        통제로 차단·완화       로그로 검증          답안 작성
IP·ARP·TCP·VLAN  →  스캔·스푸핑·DoS  →  ACL·Firewall·IPS  →  패킷·장비·SIEM  →  원리·근거·영향·대응
```

- 2.1에서 “원래 어떻게 동작하는가”를 이해해야 2.2의 공격 원리가 보인다.
- 2.3은 경계에서 차단하고, 2.4는 놓친 공격을 탐지·분석하며, 2.5는 통신 자체를 암호화한다.
- 모든 문제는 `정상 동작 → 악용 지점 → 관찰 근거 → 대응 → 검증` 순서로 연결한다.

### 우선순위별 학습 완료 수준

| 우선순위 | 여기까지 할 수 있으면 완료 | 지금 제외해도 되는 것 |
|---|---|---|
| P1 | 정의·동작을 설명하고, 제시된 패킷/설정을 판독하며, 대응 2개 이상을 쓴다 | 없음. 다음 주 기출 전에 학습 |
| P2 | 용어를 식별하고 P1과의 차이·대표 위험·대응 1개를 말한다 | 세부 필드값, 제품별 구현 차이, 공격 연도 |
| P3 | 이름과 보안 목적을 알아본다 | 명령 전체 암기, 레거시 내부 동작, 세부 옵션 |

**시간이 부족하면 제외 가능한 범위**: 2.8 전체, TLS 1.3의 0-RTT·DTLS 세부, SNMPv3 내부 필드, IPv4 Options, Land·Ping of Death의 세부 동작은 마지막 회독으로 미룬다. 이 저빈도 항목들을 완전히 삭제하지 않은 이유는 단답형에서 다시 출제될 수 있기 때문이다.

### 근거 기반 우선순위

| 우선순위 | 학습 묶음 | 근거 | 시험에서의 변형 |
|---|---|---|---|
| P1 | TCP/IP·ARP·ICMP·서브넷·VLAN | 네트워크 보안은 전체 142/513(27.7%), 최근 23~31회 41/162(25.3%) | 필드·용어 빈칸 → 패킷 흐름 판단 → 공격과 대응 |
| P1 | DNS·SNMP·VLAN·라우터·방화벽 | 반복 개념군 54건, 최근 17건으로 장비·프로토콜 실무형과 직접 연결 | 설정 의미 → 취약점 → ACL·필터·보완 설정 |
| P1 | IDS/IPS·Snort·DLP·관제 | 반복 개념군 52건과 DLP 반복 단답, 서술/실무를 오감 | 분류·오탐/미탐 → 솔루션 식별·룰 해석 → 배치·대응 |
| P1 | 스캔·스니핑·스푸핑·DoS/DDoS | 반복 개념군 49건 | 패킷/로그 증거로 공격 식별 → 단계별 대응 |
| P1 | IPsec·VPN·TLS | 암호통신 반복 개념군 34건, 최근 IPsec·TLS 재출제 | AH/ESP/IKE·모드 비교 → 핸드셰이크·키 용도 |
| P2 | NAT·무선·점검 도구 | KCA 공식 세세항목에 직접 포함 | 유형·도구 식별 → 보안상 목적과 설정·결과 해석 |
| P2 | 보조 헤더 필드·레거시 공격 원리·프로토콜 내부 필드 | 공식 범위에는 포함되지만 최근 반복성은 상대적으로 낮음 | 필드·공격명 식별 → 대표 위험과 대응 |
| P3 | IPv6·TLS/DTLS 확장, 레거시 VPN, 벤더별 확인 명령 | 저빈도이거나 특정 구현과 버전에 의존 | 용어 식별과 핵심 보안 목적 수준으로 준비 |

> 수치는 복원된 1~31회 513문항의 **개념·유형 분류**에 기반한다. 공식 문항별 배점이나 다음 회차 출제를 보장하는 수치가 아니다.

### 반복 출제 패턴

1. **용어·헤더·포트 단답형**: TCP 플래그, ICMP Type, ARP/RARP, 포트, VLAN·NAT 유형을 정확히 쓴다.
2. **패킷·표·로그 판별형**: SYN/ACK/RST, 동일 MAC의 다수 ARP 항목, promiscuous mode, IDS 경보를 근거로 상태나 공격을 판단한다.
3. **설정 완성형**: ACL, `iptables`, Snort, 라우터, SNMP 설정의 빈칸과 방향을 채운다.
4. **원리-영향-대응 서술형**: ARP spoofing, Smurf, DNS/NTP 증폭, SYN Flooding 등을 원리와 대응으로 나눈다.
5. **비교형**: IDS/IPS, HIDS/NIDS, 오용/이상 탐지, IPsec 전송/터널, AH/ESP, 정적/동적 VLAN을 구분한다.

### 공식 범위 대응표

| KCA 세세 범위 | 이 문서의 대응 섹션 |
|---|---|
| OSI/TCP-IP, PDU·헤더 필드 | 2.1.1~2.1.6 |
| IP·ARP·RARP·ICMP·Routing 동작과 취약점 | 2.1.3~2.1.7, 2.2 |
| TCP·UDP·SSL/TLS·IPsec 동작과 취약점 | 2.1.5, 2.2.1, 2.5 |
| DoS/DDoS, 무선 프로토콜과 보안 | 2.2.3, 2.6 |
| 네트워크 구성도·IP·서브넷, DNS·SNMP·스캔, VLAN·Router·Firewall·IDS/IPS·VPN·NAT | 2.1.2, 2.1.6~2.1.10, 2.2.1, 2.3~2.5 |
| 장비 관리자 계정, 방화벽·IDS/IPS·NAT·무선·WAF·Anti-DDoS·Anti-APT 설정 점검 | 2.1.8, 2.3, 2.4, 2.6 |
| 네트워크·보안장비 로그 수집 및 패킷 분석·대응 | 2.4, 2.7 |

### 이 장과 3장의 경계

- 이 장은 **통신 동작·패킷·네트워크 장비·공격 트래픽·차단**에 초점을 둔다.
- DNS는 질의 흐름·전송 방식·공격 원리까지만, NTP·SNMP는 증폭 공격과 장비 관리 보안까지만 다룬다. 존 파일·서비스 데몬의 상세 설정은 3장에서 다룬다.
- TLS는 통신과 키 사용 흐름을 다루고, HTTPS·웹 취약점·웹 서버 설정은 3장에서 다룬다.

## 2.1 [P1] TCP/IP 기본과 패킷 판독

### 2.1.1 [P1] OSI 7계층·PDU·주소

| OSI 계층 | 핵심 기능·프로토콜 | PDU·식별자 | 대표 장비 |
|---|---|---|---|
| 7 응용 | HTTP, DNS, SMTP, FTP, SNMP | Data | Proxy, WAF |
| 6 표현 | 형식 변환, 암·복호화, 압축 | Data | - |
| 5 세션 | 세션 설정·유지·종료 | Data | - |
| 4 전송 | TCP, UDP, 포트 기반 종단 통신 | Segment/Datagram, Port | L4 Switch |
| 3 네트워크 | IP, ICMP, 라우팅 | Packet, IP | Router, L3 Switch |
| 2 데이터링크 | Ethernet, MAC, 프레임 전달 | Frame, MAC | Switch, Bridge, NIC |
| 1 물리 | 전기·광 신호와 비트 전송 | Bit | Hub, Repeater, Cable |

- TCP/IP 계층은 보통 응용-전송-인터넷-네트워크 접근의 4계층으로 본다.
- ARP는 IPv4 주소와 같은 링크의 MAC 주소를 연결한다. OSI 한 계층에 억지로 고정하기보다 **로컬 링크에서 IP→MAC 해석**이라는 기능을 기억한다.
- 캡슐화: 응용 데이터 → 전송 헤더 → IP 헤더 → Ethernet 헤더/트레일러. 수신 측은 역순으로 역캡슐화한다.

### 2.1.2 [P1] 포트·IPv4·서브넷

| 서비스 | 기본 포트 | 서비스 | 기본 포트 |
|---|---:|---|---:|
| FTP data/control | TCP 20/21 | SSH / Telnet | TCP 22/23 |
| SMTP | TCP 25 | DNS | UDP·TCP 53 |
| DHCP server/client | UDP 67/68 | HTTP / HTTPS | TCP 80/443 |
| POP3 / IMAP | TCP 110/143 | SNMP query/trap | UDP 161/162 |
| NTP | UDP 123 | SMB | TCP 445 |
| Syslog | UDP 514가 전통적 기본값 | RDP | TCP/UDP 3389 |

> 포트는 기본값일 뿐 변경 가능하다. 시험에서는 **서비스명-전송 프로토콜-기본 포트**를 묶고, 패킷에서는 실제 헤더를 확인한다.

#### IPv4 주소와 서브넷의 계산 순서

IPv4 주소는 점으로 구분한 4개의 옥텟, 즉 총 32비트다. `/n`은 왼쪽부터 네트워크로 고정한 비트 수이고, 나머지 `32-n`비트는 그 네트워크 안에서 호스트를 구분하는 비트다. 마스크에서 `1`은 네트워크 비트, `0`은 호스트 비트를 뜻한다.

| 항목 | 계산 | `200.100.50.25/26`에 적용 |
|---|---|---|
| 네트워크 비트 | prefix 길이 `/n` | 26비트 |
| 호스트 비트 | `32-n` | `32-26=6`비트 |
| 서브넷 전체 주소 수 | `2^(호스트 비트 수)` | `2^6=64`개 |
| 마스크 | 네트워크 비트는 1, 호스트 비트는 0 | `255.255.255.192` |
| 마스크의 2진수 | 옥텟마다 8비트로 표현 | `11111111.11111111.11111111.11000000` |

이 예에서는 마지막 옥텟의 마스크가 `192`다. 마지막 옥텟에서 주소 구간이 증가하는 **블록 간격**은 `256-192=64`이므로 `.0~.63`, `.64~.127`, `.128~.191`, `.192~.255`로 나뉜다. `.25`는 첫 번째 구간에 있으므로 이 주소가 속한 네트워크의 시작은 `.0`이다.

```text
마지막 옥텟의 IP:       25 = 00011001
마지막 옥텟의 마스크:  192 = 11000000
네트워크 부분을 남긴 값:     00000000 = 0
호스트 6비트를 모두 1로 한 값: 00111111 = 63
```

따라서 다음과 같이 결정한다.

| 주소 역할 | 호스트 비트 값 | 결과 |
|---|---|---|
| 네트워크 주소 | 모두 0 | `200.100.50.0` |
| 브로드캐스트 주소 | 모두 1 | `200.100.50.63` |
| 일반 호스트 주소 | 모두 0과 모두 1을 제외 | `200.100.50.1` ~ `200.100.50.62` |

일반식으로는 `네트워크 주소 = IP AND 마스크`, `브로드캐스트 주소 = 네트워크 주소 OR 마스크의 반전값`이다. 일반적인 IPv4 LAN에서는 네트워크 주소와 브로드캐스트 주소를 호스트에 할당하지 않으므로 사용 가능한 호스트 수는 `2^h-2`다. `/31`과 `/32`는 점대점 연결이나 단일 호스트 식별처럼 용도가 달라질 수 있으므로 이 규칙을 그대로 적용하지 않는다.

> 이 예에서는 블록 간격과 서브넷 전체 주소 수가 모두 64이지만, 두 용어는 구분한다. 블록 간격은 마스크가 처음으로 `255`가 아닌 옥텟에서의 증가폭이고, 서브넷 전체 주소 수는 32비트 전체에서 남은 호스트 비트 수로 계산한다.

#### 사설 IPv4 주소와 NAT

사설 IPv4 주소는 조직·가정 등 내부 네트워크에서 재사용할 수 있도록 예약한 주소 대역이다. 이 주소들은 공용 인터넷에서 목적지로 라우팅하지 않으므로, 서로 다른 내부망이 같은 사설 주소를 사용해도 인터넷에서 충돌하지 않는다. 외부 인터넷과 통신할 때는 경계 장비가 보통 NAT/PAT로 사설 주소와 포트를 공인 주소·포트로 변환한다.

| 사설 대역 | 실제 범위 | 빠른 판별 |
|---|---|---|
| `10.0.0.0/8` | `10.0.0.0` ~ `10.255.255.255` | 첫 옥텟이 `10` |
| `172.16.0.0/12` | `172.16.0.0` ~ `172.31.255.255` | 첫 옥텟이 `172`이고 둘째 옥텟이 `16~31` |
| `192.168.0.0/16` | `192.168.0.0` ~ `192.168.255.255` | 앞 두 옥텟이 `192.168` |

`172.16.0.0/12`의 마스크는 `255.240.0.0`이다. 둘째 옥텟의 블록 간격이 `256-240=16`이므로 `172.16`에서 시작해 다음 경계 직전인 `172.31`까지가 사설 대역이다. 따라서 `172.20.1.1`은 사설 주소지만 `172.15.1.1`과 `172.32.1.1`은 아니다. 같은 이유로 `192.168.1.1`은 사설 주소이나 `192.169.1.1`은 아니다.

사설 주소라는 사실만으로 통신이 안전해지는 것은 아니다. 사설 주소는 공용 인터넷에서 직접 라우팅되지 않을 뿐이며, 내부망 접근통제·방화벽 정책·NAT 규칙은 별도로 필요하다. `127.0.0.0/8`(loopback), `169.254.0.0/16`(link-local), `100.64.0.0/10`(CGNAT)은 사설 IPv4 세 대역과 목적이 다른 특수 주소 대역이다.

### 2.1.3 [P1] IPv4와 ICMP 헤더

| 필드 | 우선순위 | 기능 | 보안·판독 포인트 |
|---|---|---|---|
| Version / IHL | P2 | IP 버전 / IPv4 헤더 길이 | 비정상 길이·헤더 시작 위치 판독 |
| Total Length | P2 | 헤더를 포함한 전체 데이터그램 길이 | 단편·과대/비정상 길이 판독 |
| Identification | P1 | 같은 원본 데이터그램의 단편 식별 | 단편 재조립 연관성 |
| Flags | P1 | DF(단편화 금지), MF(뒤 단편 존재) | 비정상 단편·우회 탐지 |
| Fragment Offset | P1 | 원본에서 단편의 위치 | 중첩·비정상 offset은 Teardrop 계열 단서 |
| TTL | P1 | 라우터를 지날 때 감소, 0이면 폐기 | 루프 방지, traceroute 동작 |
| Protocol | P1 | 상위 프로토콜 식별 | ICMP 1, TCP 6, UDP 17 |
| Header Checksum | P2 | IPv4 헤더 오류 검출 | 홉마다 TTL 변경 후 재계산 |
| Source/Destination | P1 | 출발지·목적지 IP | spoofing·ACL 판정 |
| Options | P2 | 선택적 제어 정보, 가변 길이 | source route 등 불필요 옵션 점검 |

| ICMP Type | 의미 | 활용 |
|---:|---|---|
| 0 | Echo Reply | ping 응답 |
| 3 | Destination Unreachable | 도달 불가·UDP 스캔 판독 |
| 5 | Redirect | 더 나은 경로 통지, 불필요한 수신은 MITM 위험 |
| 8 | Echo Request | ping 요청 |
| 11 | Time Exceeded | traceroute의 홉 식별 |

- ICMP header의 공통 핵심은 Type, Code, Checksum이며, Echo Request/Reply에는 Identifier와 Sequence Number 등이 이어져 요청과 응답을 대응시킨다.
- Linux의 일반적인 `traceroute`는 UDP probe를, Windows `tracert`는 ICMP Echo Request를 사용하며 TTL을 점차 증가시킨다. 구현·옵션에 따라 ICMP/TCP 방식을 쓸 수 있다.
- ICMP Type 3의 Code 3은 Port Unreachable로, UDP probe가 닫힌 포트에 도달했음을 판단하는 대표 응답이다.
- TTL 초기값만으로 운영체제를 단정하지 않는다. 경유 홉과 설정에 따라 달라지며 보조 단서일 뿐이다.

### 2.1.4 [P1] ARP·RARP·GARP

- **ARP**: 같은 링크에서 목적지 IPv4 주소에 대응하는 MAC 주소를 구한다. Request는 브로드캐스트, Reply는 일반적으로 유니캐스트이며 결과를 ARP 캐시에 저장한다.
- 다른 서브넷 목적지라면 목적지 호스트가 아니라 **기본 게이트웨이의 MAC**을 ARP로 구한다.
- **RARP**: MAC 주소로 IPv4 주소를 얻던 레거시 프로토콜이다. 현재는 BOOTP/DHCP가 대체한다.
- **GARP(Gratuitous ARP)**: 자신의 IP에 대한 ARP를 자발적으로 알려 중복 IP 탐지, 캐시 갱신, 이중화 절체 등에 사용한다. 인증 기능이 없으므로 악용될 수 있다.
- **[P2] ARP 필드:** Hardware Type, Protocol Type, Hardware/Protocol Address Length, Opcode(Request 1·Reply 2), Sender MAC/IP(SHA/SPA), Target MAC/IP(THA/TPA)를 구분한다. Request의 THA는 아직 모르므로 `00:00:00:00:00:00`으로 채우며 Ethernet 목적지 MAC은 broadcast `ff:ff:ff:ff:ff:ff`다. Reply는 일반적으로 요청자에게 unicast한다.

**[답안]** ARP spoofing은 공격자가 위조 ARP Reply를 보내 피해자의 IP-MAC 매핑을 공격자 MAC으로 바꾸는 공격이다. 패킷이 공격자를 경유하여 도청·변조·세션 탈취 또는 통신 방해가 발생한다. 동일 MAC이 여러 주요 IP에 매핑되거나 게이트웨이 MAC이 갑자기 바뀐 기록이 판단 근거다. 정적 ARP는 소규모 핵심 장비에 제한 적용하고, 스위치의 DHCP Snooping과 Dynamic ARP Inspection, 포트 보안, 암호화 통신을 함께 사용한다.

```bash
# 현재 ARP cache 확인
arp -a

# 기출형 정적 ARP 등록: 운영체제별 옵션 차이는 문제 환경을 우선
arp -s <IP주소> <MAC주소>
```

정적 ARP 등록 뒤 `arp -a` 또는 운영체제의 이웃 테이블 명령으로 IP-MAC 매핑을 다시 확인한다. 정적 항목은 변경·장애 대응과 대규모 운영 부담이 있으므로 gateway 등 소수 핵심 대상에 제한하고 DAI·DHCP Snooping 같은 네트워크 통제와 병행한다.

### 2.1.5 [P1] TCP·UDP와 상태 판독

- TCP: 연결지향, 신뢰성·순서·흐름·혼잡 제어를 제공한다. UDP: 비연결, 헤더가 작고 전달·순서를 보장하지 않는다.
- TCP header 핵심: Source/Destination Port, Sequence Number, Acknowledgment Number, Data Offset, Flags, Window Size, Checksum, Urgent Pointer. Window는 **이 세그먼트의 송신 측이 앞으로 추가로 받을 수 있다고 상대에게 광고하는 수신 여유량**이며, Checksum은 header와 data의 오류를 검출한다.
- UDP header는 Source Port, Destination Port, Length, Checksum의 4개 필드로 단순하다. 연결 상태·순서번호·재전송 기능이 없으므로 필요한 신뢰성은 응용이 구현한다.
- TCP 주요 플래그:
  - `SYN`: 연결 시작·순서번호 동기화
  - `ACK`: Ack 번호가 유효함을 표시
  - `FIN`: 정상 연결 종료 요청
  - `RST`: 연결 즉시 재설정·거부
  - `PSH`: 수신 버퍼가 찰 때까지 기다리지 않고 응용에 전달 요청
  - `URG`: Urgent Pointer가 유효함을 표시
- 3-way handshake: `SYN(seq=x) → SYN/ACK(seq=y, ack=x+1) → ACK(ack=y+1)`.
- 일반적인 능동 종료: `FIN → ACK → FIN → ACK`. 양쪽이 독립적으로 송신을 닫으므로 네 단계가 된다.
- `seq`는 전송 바이트의 순서를, `ack`는 다음에 기대하는 순서번호를 나타낸다. SYN과 FIN은 각각 순서번호 1을 소비한다.

### 2.1.6 [P1] Ethernet·Switch·VLAN

- Ethernet frame은 `Destination MAC → Source MAC → EtherType/Length → Payload → FCS` 순으로 본다. EtherType은 상위 프로토콜을 식별하고, FCS는 전송 중 frame 오류를 검출한다. 물리 전송에는 앞쪽의 Preamble과 SFD도 사용된다.
- 스위치 전달 방식:
  - **Cut-through**: 목적지 MAC을 읽은 뒤 즉시 전달하여 지연이 작지만 오류 프레임도 전달할 수 있다.
  - **Fragment-free**: 충돌로 손상되기 쉬운 앞 64바이트를 확인한 후 전달한다.
  - **Store-and-forward**: 전체 프레임과 FCS를 확인한 뒤 전달하여 오류 검출이 가능하지만 지연이 늘어난다.
- VLAN은 하나의 물리 스위치망을 논리적 브로드캐스트 도메인으로 분리한다. 서로 다른 VLAN 간 통신에는 라우팅이 필요하다.
- 정적 VLAN은 스위치 포트에 수동 할당하고, 동적 VLAN은 MAC·인증·정책 등에 따라 할당한다. 구성 기준에 따라 Port/MAC/Protocol/Subnet 기반으로도 분류한다.
- VLAN hopping:
  - Switch spoofing: 공격 포트를 trunk로 협상한다. 사용하지 않는 포트 차단, access 모드 고정, DTP 비활성화로 대응한다.
  - Double tagging: 이중 802.1Q 태그와 native VLAN 처리를 악용한다. native VLAN을 사용자 VLAN과 분리하고 trunk 허용 VLAN을 최소화한다.
- MAC flooding은 CAM 테이블을 채워 비정상 flooding을 유도한다. Port Security로 허용 MAC 수·주소를 제한한다.
- Cisco 계열에서 VLAN 할당·상태를 확인하는 대표 명령은 `show vlan` 또는 `show vlan brief`다.

### 2.1.7 [P1] Routing 기본과 보안

라우팅은 **목적지 IP가 어느 네트워크에 있는지 판단하고, 그곳으로 보낼 다음 경로를 고르는 과정**이다. 스위치는 같은 LAN 안에서 MAC 주소를 보고 프레임을 전달하지만, 다른 IP 네트워크로 가려면 라우터(기본 게이트웨이)가 필요하다.

#### 1. 먼저 같은 네트워크인지 판단한다

호스트는 자신의 IP와 마스크로 목적지 IP가 같은 서브넷인지 먼저 판단한다.

```text
내 PC:       192.168.10.20/24
목적지:      192.168.10.80  → 같은 서브넷
목적지:      10.20.30.40    → 다른 서브넷
기본 게이트웨이: 192.168.10.1
```

- 목적지가 같은 서브넷이면 목적지 호스트의 MAC 주소를 ARP로 알아내 스위치를 통해 직접 보낸다.
- 목적지가 다른 서브넷이면 목적지 서버의 MAC 주소를 알아내지 않는다. **기본 게이트웨이의 MAC 주소**를 ARP로 알아내 그 라우터에 보낸다.
- 이때 Ethernet 프레임의 목적지 MAC은 게이트웨이 MAC이지만, IP 패킷의 목적지 IP는 최종 서버 IP인 `10.20.30.40`으로 유지된다. 라우터는 프레임을 벗기고 이 목적지 IP를 보고 다음 경로를 고른다.

#### 2. 라우터는 라우팅 테이블에서 목적지에 맞는 행을 찾는다

라우팅 테이블의 각 행은 “이 목적지 대역으로 가려면 어디로 내보낼 것인가”라는 규칙이다. 보통 `목적지 network/prefix → next-hop gateway 또는 직접 연결 → 출력 interface → metric` 순서로 읽는다.

| 목적지 prefix | next hop | 의미 |
|---|---|---|
| `10.0.0.0/8` | Router A | `10.x.x.x` 대역은 Router A로 전달 |
| `10.20.0.0/16` | Router B | `10.20.x.x` 대역은 Router B로 전달 |
| `10.20.30.0/24` | Router C | `10.20.30.x` 대역은 Router C로 전달 |
| `0.0.0.0/0` | Internet gateway | 어느 규칙에도 맞지 않을 때 전달 |

`10.20.30.40`은 위 표의 앞 세 행에 모두 들어간다. 이때 가장 구체적인 `/24`를 선택하므로 Router C로 보낸다. 이를 **Longest Prefix Match(LPM)** 라고 한다. prefix가 길수록 네트워크 범위가 더 좁고 구체적이다.

```text
10.0.0.0/8       : 10.*.*.*
10.20.0.0/16     : 10.20.*.*
10.20.30.0/24    : 10.20.30.*  ← 10.20.30.40에 가장 구체적
```

- **Host route**: 한 IP 주소만 가리키는 `/32` 경로다.
- **Network route**: 특정 네트워크 대역을 가리키는 `/8`, `/16`, `/24` 등의 경로다.
- **Default route**: `0.0.0.0/0`이며, 더 구체적인 경로가 없을 때 사용하는 마지막 경로다. 기본 경로도 없으면 라우터는 패킷을 폐기하고, 상황에 따라 ICMP Destination Unreachable을 돌려줄 수 있다.
- **직접 연결(connected) 경로**는 라우터 자신의 인터페이스에 연결된 네트워크다. 이 경우 다음 라우터가 아니라 같은 링크의 최종 호스트 MAC 주소를 ARP로 알아내 보낸다.

#### 3. 같은 prefix의 경로가 여러 개면 출처와 비용을 비교한다

LPM으로 가장 긴 prefix를 먼저 고른 뒤, **동일한 목적지 prefix**를 가진 경로가 둘 이상일 때 경로 출처의 신뢰도와 metric을 비교한다.

- 경로 출처의 신뢰도는 연결 경로·정적 경로·동적 라우팅 프로토콜 중 어느 정보를 우선할지 정하는 기준이다. Cisco에서는 Administrative Distance(AD)라는 용어를 사용한다.
- metric은 같은 종류의 경로 중 어느 쪽이 더 좋은지를 나타내는 비용이다. hop 수, 대역폭, 지연, 관리자가 정한 cost 등이 될 수 있다.
- 장비와 운영체제마다 표시 이름·기본값은 다를 수 있지만, 판독 순서는 **가장 긴 prefix → 동일 prefix 간 경로 출처 → metric**으로 이해한다.

#### 4. 라우팅 경로는 직접 연결·정적 설정·동적 교환으로 만들어진다

| 경로의 출처 | 만드는 방법 | 핵심 특징 |
|---|---|---|
| Connected | 인터페이스에 IP와 마스크를 설정 | 해당 네트워크로 가는 경로가 자동으로 생김 |
| Static | 관리자가 next hop 또는 출력 interface를 직접 설정 | 단순하고 예측 가능하지만, 장애·변경 때 수동 관리가 필요 |
| Dynamic | 라우터끼리 라우팅 정보를 교환 | 경로 변화에 대응하지만 프로토콜 설정·검증이 필요 |

동적 라우팅 프로토콜은 “어떤 목적지 네트워크가 어디에 있고, 어느 길이 나은가”를 라우터끼리 알리는 방식이다.

- **RIP**: 거리 벡터 방식이다. 이웃에게 목적지까지의 거리 정보를 알리고, hop count를 기준으로 경로를 고른다. 최대 15 hop까지만 도달 가능으로 본다.
- **OSPF**: 링크 상태 방식이다. 라우터들이 네트워크 연결 상태를 공유하고, 각 라우터가 전체 구조를 바탕으로 SPF(최단 경로 우선) 계산을 수행한다. 경로 비용에는 cost를 사용한다.
- **EIGRP**: DUAL 알고리즘으로 loop-free 경로 계산을 지원하는 고급 거리 벡터 계열 프로토콜이다. Cisco 계열 환경에서 주로 접한다.

#### 5. 라우팅 보안: 거짓 경로를 믿지 않게 한다

라우터가 잘못되거나 공격자가 위조한 경로 광고를 믿으면, 정상 트래픽이 공격자 쪽으로 우회되어 도청·변조될 수 있고, 존재하지 않는 경로로 보내져 서비스가 끊기는 **블랙홀**이 될 수 있다.

| 통제 | 막으려는 문제 |
|---|---|
| 라우팅 프로토콜 인증 | 인증되지 않은 장비의 경로 광고 수용 방지 |
| 신뢰 인터페이스 제한·`passive-interface` | 사용자망 등 라우터가 아닌 구간에서 인접 관계·라우팅 갱신이 생기는 것 방지 |
| 경로 필터링 | 받아들이거나 광고할 prefix를 필요한 대역으로 제한 |
| 관리망 분리·관리 접근통제 | 라우터 설정·라우팅 정책의 무단 변경 방지 |
| 로그·라우팅 테이블 모니터링 | 예기치 않은 next hop, 경로 변경, flap을 탐지 |

IP source routing은 송신자가 패킷에 경유 경로를 지정하는 오래된 IP 옵션이다. 불필요한 환경에서는 Cisco 계열의 `no ip source-route`처럼 이를 비활성화해, 송신자가 임의의 우회 경로를 지시하는 기능을 허용하지 않는다. 이는 라우팅 프로토콜의 위조 광고 방어와는 별개의 통제다.

> 라우팅을 읽을 때는 `목적지 IP가 같은 서브넷인가 → 아니면 기본 게이트웨이로 보낸다 → 라우터가 LPM으로 경로를 고른다 → 같은 prefix면 출처와 metric을 비교한다` 순서만 먼저 확실히 잡는다.

### 2.1.8 [P2] NAT

- Static NAT: 내부-공인 주소를 1:1로 고정 매핑한다.
- Dynamic NAT: 공인 주소 pool에서 동적으로 1:1 매핑한다.
- PAT(NAPT): 여러 내부 주소를 하나 또는 소수의 공인 주소와 포트로 구분한다.
- 내부 호스트가 외부로 연결할 때 장비가 사설 source 주소·포트를 공인 주소·포트로 변환해 변환표에 저장하고, 응답은 그 표를 역으로 조회해 내부 호스트에 전달한다. 외부에서 시작하는 연결은 정적 NAT·port forwarding 같은 명시적 매핑과 방화벽 허용이 필요하다.
- 점검 시 변환 대상·방향·주소 pool, 정적/동적 규칙, timeout, 불필요한 port forwarding, 방화벽 정책과 로그의 일치 여부를 확인한다.
- NAT는 주소 변환 기술이지 그 자체가 완전한 보안 통제가 아니다. 외부 노출을 줄이는 효과가 있어도 방화벽 정책·접근통제·로그가 별도로 필요하다.

### 2.1.9 [P1] 네트워크 구성도 판독

1. Internet·외부기관·DMZ·내부 업무망·DB망·관리망·무선/게스트망의 **신뢰 경계**를 표시한다.
2. 각 구간의 subnet, gateway, 공개/사설 IP, NAT 지점과 서버·DB·단말·네트워크/보안장비 자산을 대응시킨다.
3. 외부→DMZ→내부, 내부→외부, 관리망→장비의 실제 통신 경로와 허용 port를 따라간다.
4. Firewall/IPS는 inline 차단 경로, IDS는 TAP/SPAN 수집 지점, WAF는 공개 웹 앞, Anti-DDoS는 대용량 공격을 처리할 경계·우회 경로에 있는지 본다.
5. DB의 직접 인터넷 노출, DMZ와 내부망의 무제한 통신, 관리 인터페이스의 업무망 노출, 단일 장비 장애점, 우회 경로, 자산목록의 누락·중복을 찾는다.
6. 구성도·자산목록·실제 `route/ARP/MAC/NAT/Firewall` 정보를 대조하고 발견 사항과 보완 후 경로를 기록한다.

**[답안]** DMZ는 외부 공개 서버를 내부망과 분리하여 침해 시 내부 확산을 제한하는 완충 구간이다. 공개 서비스에 필요한 트래픽만 외부→DMZ로 허용하고, DMZ→내부는 업무상 필요한 목적지·포트만 별도 허용한다.

### 2.1.10 [P1] DNS 최소 정상 동작

1. 단말의 stub resolver가 local recursive/cache DNS에 재귀 질의를 보낸다.
2. cache에 답이 없으면 recursive DNS가 `Root → TLD → Authoritative DNS`의 referral을 따라 최종 응답을 얻고 단말에 돌려준다. Root와 TLD가 모든 호스트의 최종 IP를 직접 저장하는 것은 아니다.
3. 재귀 질의는 요청자가 최종 답을 요구하는 방식이고, 반복 질의는 DNS 서버가 다음에 물을 서버 정보를 referral로 돌려주는 방식이다.
4. 일반 질의는 주로 UDP 53을 사용한다. Zone transfer는 TCP 53을 사용하고, 응답의 TC bit가 설정되거나 큰 응답·DNSSEC 등 구현 조건에 따라 TCP로 전환할 수 있다.
5. TTL은 resolver가 응답을 cache할 수 있는 시간을 제어한다. 정상 흐름을 알아야 위조 응답·cache poisoning·비인가 zone transfer를 판단할 수 있다.

## 2.2 [P1] 스캔·스니핑·스푸핑·서비스 거부 공격

### 2.2.1 [P1] 포트 스캔 판독

| 방식 | 열린 포트 | 닫힌 포트 | 핵심 특징 |
|---|---|---|---|
| TCP Connect | 연결 성립 | RST/ACK 또는 연결 거부 | 전체 handshake, 로그가 비교적 잘 남음 |
| SYN(Half-open) | SYN/ACK 후 RST | RST/ACK | 연결을 완성하지 않아 빠름 |
| FIN / NULL / XMAS | 무응답(open\|filtered) | RST/ACK | 비정상 플래그, OS·방화벽에 따라 결과 차이 |
| UDP | UDP 응답이면 open | ICMP Port Unreachable이면 closed | 무응답은 open\|filtered 가능 |

- XMAS는 보통 FIN·PSH·URG를 켜고, NULL은 플래그를 켜지 않는다.
- ACK scan은 포트의 open/closed보다 방화벽의 stateful 필터와 filtered 여부를 추정하는 데 사용한다.
- Decoy scan은 여러 위장 출발지와 실제 출발지를 섞어 스캐너 식별을 어렵게 한다.
- 스캔 결과는 패킷 손실·방화벽·운영체제 구현에 따라 달라지므로 한 응답만으로 단정하지 않는다.

### 2.2.2 [P1] 스니핑·스푸핑·세션 하이재킹

- Promiscuous mode는 NIC가 자신의 MAC 목적지가 아닌 프레임도 상위 계층으로 전달하도록 하는 수신 모드다. 패킷 분석·관제에 정상 사용되지만 비인가 장비에서 발견되면 스니핑 단서다.
- 스니핑 탐지: 인터페이스 모드·프로세스 점검, 비정상 DNS/ARP 반응, 허니토큰·decoy 트래픽, 스위치 포트 미러링/IDS 로그를 함께 본다.
- 고전적 ping 탐지는 의심 호스트에 **정상적으로는 NIC가 버릴 비정상 목적지 MAC의 ICMP Echo**를 보내 응답 여부를 보는 방식이다. 드라이버·OS에 따라 실패할 수 있어 단독 증거로 쓰지 않는다.
- IP spoofing은 출발지 IP를 위조한다. 반사·증폭과 신뢰관계 악용에 사용된다. 외부 인터페이스 ingress ACL, egress filtering, uRPF, 인증·암호화를 적용한다.
- DNS spoofing/cache poisoning은 정상 DNS보다 빠른 위조 응답이나 캐시 오염으로 잘못된 IP를 제공한다. 소스 포트·트랜잭션 ID 무작위화, DNSSEC 검증, 신뢰 DNS 제한, 캐시·로그 점검으로 대응한다.
- TCP session hijacking은 세션 식별 정보나 sequence를 탈취·예측하여 기존 연결에 개입한다. TLS/SSH, 강한 세션 인증, 비정상 sequence/RST·중복 ACK 모니터링으로 대응한다.

### 2.2.3 [P1] DoS·DDoS·DRDoS

#### 시험용 빠른 식별표

| 공격 | 공격 흐름 | 대표 판단 근거 | 결과 | 핵심 대응 |
|---|---|---|---|---|
| SYN Flooding `[P1]` | 다량의 SYN을 보내고 최종 ACK를 보내지 않아 서버에 half-open 연결을 누적 | SYN 급증, SYN/ACK 대비 최종 ACK 부족, `SYN_RECV`·backlog 사용량 증가, 정상 신규 연결 실패 | 연결 대기 큐와 연결 상태 자원이 고갈되어 서비스 지연·거부 | SYN cache/cookie·SYN proxy, 임계치·rate limit, source validation, backlog·timeout 보정, Anti-DDoS |
| Smurf `[P1]` | 피해자 IP로 출발지를 위조한 ICMP Echo Request를 증폭망의 directed broadcast 주소로 보내 다수 호스트의 Echo Reply를 피해자에게 반사 | broadcast 목적지의 Echo Request와 여러 호스트에서 한 피해자로 집중되는 Echo Reply | 반사·증폭된 ICMP 트래픽으로 피해자 회선·처리 자원 고갈 | `no ip directed-broadcast`, broadcast Echo 무응답, ingress/egress filtering·uRPF, ICMP rate limit |
| DNS/NTP 증폭 DRDoS `[P1]` | 피해자 IP로 출발지를 위조한 작은 UDP 질의를 여러 공개 DNS/NTP 서버에 보내 더 큰 응답을 피해자에게 반사 | 요청 기록 없이 다수 서버의 UDP 53/123 응답이 집중, 응답 크기·양이 요청보다 큼 | 공격원 은닉과 트래픽 증폭으로 피해자 회선·서비스 고갈 | source validation, 공개 재귀 DNS 제한·DNS RRL, NTP 접근제어·지원 버전 갱신, rate limit·스크러빙 |
| Slow HTTP Header DoS(Slowloris) `[P1]` | HTTP request header를 끝내지 않고 작은 header 조각을 천천히 보내 다수 연결을 유지 | 불완전 header, 종료되지 않은 request, 주기적인 소량 header 전송, 장시간 connection | 서버가 header 완료를 기다리면서 connection·worker를 점유하여 정상 신규 접속 거부 | header·idle timeout, header 최소 전송률, source별·전체 동시 연결 제한, reverse proxy/WAF |
| Slow HTTP POST DoS(RUDY) `[P1]` | 큰 `Content-Length`를 선언한 뒤 request body를 매우 천천히 보내 다수 연결을 유지 | `POST`, 큰 `Content-Length`, 1 byte 단위·낮은 body 전송률, 장시간 미완성 body | 서버가 body 수신을 기다리면서 connection·worker·memory를 점유하여 정상 요청 처리 지연·거부 | body/read·idle timeout, body 최소 전송률·최대 크기, 동시 연결 제한, reverse proxy/WAF |
| Slow HTTP Read DoS `[P2]` | 작은 TCP receive window 또는 Zero Window를 광고하여 서버의 response 수신을 의도적으로 지연 | 작은/Zero Window, 장시간 server-side 송신 대기, 낮은 client 수신률 | 서버의 response buffer·connection을 장시간 점유 | write timeout, 송신 대기·동시 연결 제한, reverse proxy, 비정상 window·세션 모니터링 |
| Teardrop `[P2]` | 같은 IP datagram의 fragment offset을 중첩·불일치하게 조작하여 취약한 재조립 구현을 오동작시킴 | 같은 Identification의 단편에서 겹치거나 모순되는 offset·길이, 재조립 오류 뒤 시스템 정지·재부팅 | 취약한 IP stack의 오류·crash로 서비스 거부 | OS·네트워크 장비 패치, 방화벽/IPS의 단편 재조립·정규화, 비정상 중첩 단편 차단·로그 |
| Land `[P2]` | 출발지와 목적지 IP를 피해자 주소로 같게 만들고, 전형적으로 TCP SYN의 출발지·목적지 port도 같게 위조 | `src IP = dst IP = 피해자`, 전형적으로 `src port = dst port`인 비정상 패킷 | 취약한 구현이 자기 자신에게 응답·처리를 반복하여 자원 고갈·정지 | 패치, 외부에서 들어오는 내부 출발지 차단, 동일 source/destination tuple 등 비정상 패킷 필터 |
| Ping of Death `[P2]` | IP 단편을 재조립했을 때 IPv4 최대 datagram 크기 65,535 bytes를 넘도록 조작하며 흔히 ICMP Echo를 운반 | fragment offset·길이 합산 시 최대 IP 길이 초과, 비정상 단편 재조립과 직후 crash·reboot | 취약한 IP stack의 buffer 처리 오류로 시스템 정지·재부팅 | 패치, 방화벽/IPS의 재조립 검사·정규화, 초과 크기·비정상 단편 차단 |

#### 실기 서술형 공통 답안 구조

공격별 답안은 다음 순서로 쓰면 패킷·로그 판독형과 원리·대응 서술형을 같은 구조로 처리할 수 있다.

1. **공격명·정의**: 어떤 DoS 계열이며 무엇을 악용하는지 쓴다.
2. **공격 흐름**: 공격자가 보내는 값 → 중간 시스템 또는 피해자의 처리 → 자원 고갈 순서로 쓴다.
3. **판단 근거**: 문제에 제시된 packet flag, IP·port, 상태, fragment, 로그 값을 직접 인용한다.
4. **영향**: 어떤 queue·connection·bandwidth·worker·IP stack 자원이 고갈되며 어떤 장애가 발생하는지 쓴다.
5. **대응**: 원인 제거 → source·protocol 검증 → 서버 보호 → 경계·상위망 완화 → 로그 확인 순으로 2개 이상 쓴다.

```text
[공통 템플릿]
이 공격은 (악용 대상)을 이용하는 (공격명)이다. 공격자는 (입력·위조값)을 보내고,
(중간 장비/피해자)가 (처리)를 하게 하여 (자원)을 고갈시킨다.
(패킷·로그·상태값)이 관찰되므로 해당 공격으로 판단하며, 그 결과 (서비스 영향)이 발생한다.
대응으로 (원인 제거), (필터·검증), (서버/경계 완화)를 적용하고 로그와 정상 서비스 복구를 확인한다.
```

#### 공격별 모범 답안

##### SYN Flooding

- **정의·원리**: TCP 3-way handshake에서 공격자가 SYN을 대량 전송한 뒤 최종 ACK를 보내지 않아 서버의 연결을 `SYN-RECEIVED` half-open 상태로 유지시키는 DoS 공격이다. 출발지 IP 위조가 자주 사용되지만 SYN Flooding의 필수 조건은 아니며, 실제 bot이 유효한 주소로 대량 연결을 시도할 수도 있다.
- **판단 근거**: 단순히 SYN이 많다는 사실만 보지 않고 SYN/ACK 대비 최종 ACK 비율 저하, `SYN_RECV` 증가, listen backlog 사용량·overflow, 정상 신규 접속 실패를 함께 확인한다.
- **영향**: 연결 대기 큐와 TCP 상태 자원이 고갈되어 정상 사용자의 새 연결이 지연되거나 거부된다.
- **대응**: SYN cache/cookie 또는 SYN proxy로 검증 전 상태 할당을 줄이고, 비정상 SYN rate·동시 half-open 임계치를 제한한다. source validation과 Anti-DDoS·상위망 차단을 병행하며 backlog 확대·SYN-RECEIVED timeout 축소는 운영 부작용을 검토한 보조책으로 사용한다.

**[답안]** TCP SYN Flooding은 다량의 SYN 전송 후 최종 ACK를 완료하지 않아 서버의 half-open 연결과 backlog를 고갈시키는 공격이다. SYN 급증, SYN/ACK 대비 ACK 부족, `SYN_RECV`·backlog 증가와 정상 접속 실패가 판단 근거다. SYN cache/cookie·SYN proxy, 임계치/rate limit, source validation, Anti-DDoS를 적용하고 backlog·timeout은 정상 접속 영향을 검토해 보정한다.

##### Smurf

- **정의·원리**: 공격자가 출발지 IP를 피해자 IP로 위조한 ICMP Echo Request를 다른 네트워크의 directed broadcast 주소로 보내고, 그 네트워크의 여러 호스트가 Echo Reply를 피해자에게 보내게 하는 ICMP 반사·증폭 DoS 공격이다.
- **판단 근거**: broadcast 주소로 향하는 ICMP Echo Request, 위조된 피해자 source IP, 여러 호스트에서 한 피해자로 집중되는 Echo Reply가 핵심 증거다.
- **영향**: 반사 호스트 수만큼 응답이 증폭되어 피해자의 회선과 ICMP 처리 자원이 고갈된다.
- **대응**: 라우터에서 directed broadcast 전달을 차단하고(`no ip directed-broadcast`), 호스트가 broadcast·multicast Echo Request에 응답하지 않게 한다. ingress/egress filtering·uRPF로 source spoofing을 줄이고 ICMP rate limit과 Anti-DDoS를 적용한다.

**[답안]** Smurf는 피해자 IP로 출발지를 위조한 ICMP Echo Request를 증폭망의 directed broadcast 주소로 보내 다수 호스트의 Echo Reply가 피해자에게 집중되게 하는 반사·증폭 공격이다. broadcast 목적지 Echo Request와 다수 source의 Echo Reply 집중으로 판단한다. 라우터의 directed broadcast를 차단하고 호스트의 broadcast Echo 응답을 비활성화하며 source validation과 ICMP rate limit을 적용한다.

##### DNS/NTP 증폭 DRDoS

- **정의·원리**: 공격자가 피해자 IP로 source를 위조한 작은 UDP 질의를 다수의 공개 DNS resolver·authoritative server 또는 취약한 NTP 서버에 보내고, 요청보다 큰 응답이 피해자에게 돌아가도록 하는 분산 반사·증폭 DoS 공격이다.
- **판단 근거**: 피해자가 질의하지 않았는데 여러 외부 서버의 UDP 53/123 응답이 집중되고, 응답 크기·대역폭이 요청보다 크며, 동일 유형 응답이 짧은 시간에 급증하는지를 본다. DNS에서는 반드시 `ANY` 질의만 사용되는 것은 아니므로 큰 응답을 만드는 query·EDNS·DNSSEC 조건을 패킷에서 확인한다.
- **영향**: 반사 서버로 공격 출처가 가려지고 증폭된 트래픽이 피해자 회선·방화벽·서비스를 고갈시킨다.
- **대응**: 네트워크는 BCP38 성격의 ingress/egress filtering·uRPF로 spoofed source를 차단한다. DNS는 불필요한 공개 recursion을 제한하고 DNS Response Rate Limiting을 적용한다. NTP는 지원 버전으로 갱신하고 접근제어·rate limit을 적용하며, 레거시 `monlist` 환경은 monitoring facility를 비활성화한다. 피해 측은 상위 ISP·Anti-DDoS 스크러빙과 ACL·rate limit을 연계한다.

**[답안]** DNS/NTP 증폭 DRDoS는 피해자 IP로 출발지를 위조한 작은 UDP 요청을 다수 반사 서버에 보내 큰 응답이 피해자에게 집중되게 하는 공격이다. 요청 기록 없이 여러 UDP 53/123 서버의 큰 응답이 집중되는 것이 판단 근거다. source validation, 공개 recursion·불필요 NTP 기능 제한, DNS RRL·rate limit, 지원 버전 갱신과 상위망 스크러빙을 적용한다.

##### Slow HTTP Header DoS(Slowloris)

- **정의·원리**: HTTP request header를 완성하지 않고 작은 header 조각을 제한시간 안에 조금씩 계속 보내 웹 서버가 request 완료를 기다리면서 연결을 유지하게 하는 application-layer DoS 공격이다.
- **판단 근거**: 다수 connection에서 header 종료를 나타내는 빈 줄까지 도달하지 않은 불완전 request가 장시간 유지되고, 작은 header 조각이 주기적으로 전송되며 정상 신규 연결이 실패한다. 기출 복원의 `CRLF 필드 조작` 표현은 이어지는 **조작된 HTTP header의 지속 전송·장시간 연결 유지** 조건과 함께 Slowloris로 판별한다. CRLF로 임의 header나 별도 response를 삽입하는 CRLF Injection/HTTP Response Splitting과는 구분한다.
- **영향**: 서버의 최대 connection, worker·thread, socket·memory가 장시간 점유되어 정상 사용자의 새 접속이 지연되거나 거부된다.
- **대응**: header 완료 timeout과 idle timeout, header 최소 전송률을 설정하고 source별·전체 동시 연결 수를 제한한다. reverse proxy/WAF에서 불완전·저속 header 세션을 차단하고 웹 서버의 worker·connection 사용량을 모니터링한다.

**[답안]** Slow HTTP Header DoS(Slowloris)는 HTTP request header를 완성하지 않고 작은 header 조각을 천천히 지속 전송하여 서버 connection을 장시간 점유하는 공격이다. 불완전 header, 주기적인 소량 전송, 장시간 connection과 정상 접속 실패가 판단 근거다. header·idle timeout, 최소 header 전송률, 동시 연결 제한과 reverse proxy/WAF를 적용한다.

##### Slow HTTP POST DoS(RUDY)

- **정의·원리**: HTTP POST request에 큰 `Content-Length`를 선언한 뒤 message body를 1 byte 단위처럼 매우 느리게 전송하여 웹 서버가 body 수신 완료를 기다리면서 연결을 유지하게 하는 application-layer DoS 공격이다.
- **판단 근거**: `POST` method, 비정상적으로 큰 `Content-Length`, TCP segment의 1 byte 단위 또는 매우 낮은 body 전송률, 장시간 미완성 body와 정상 요청 실패를 함께 확인한다. header가 아니라 **message body 수신 단계**가 지연된다는 점이 Header형과의 핵심 차이다.
- **영향**: body를 수신 중인 connection과 worker·thread·request buffer가 장시간 점유되어 정상 요청의 접수·처리가 지연되거나 거부된다.
- **대응**: body/read timeout과 idle timeout, body 최소 전송률과 최대 request body 크기를 설정하고 source별·전체 동시 연결 수를 제한한다. reverse proxy/WAF에서 비정상 `Content-Length`와 저속 body 세션을 차단하고 connection·worker·memory 사용량을 모니터링한다.

**[답안]** Slow HTTP POST DoS(RUDY)는 큰 `Content-Length`를 선언한 뒤 HTTP message body를 매우 천천히 전송하여 서버 connection과 request 처리 자원을 장시간 점유하는 공격이다. `POST`, 큰 `Content-Length`, 1 byte 단위 저속 전송과 미완성 body가 판단 근거다. body/read·idle timeout, 최소 body 전송률·최대 크기, 동시 연결 제한과 reverse proxy/WAF를 적용한다.

##### Slow HTTP Read DoS(P2 보조 유형)

- **정의·원리**: client가 작은 TCP receive window 또는 Zero Window를 광고하여 서버 response를 매우 느리게 수신하고, 서버의 송신 대기 상태와 connection을 오래 유지하는 공격이다.
- **판단 근거**: request header·body의 저속 전송이 아니라 서버에서 client 방향 response에 작은/Zero Window가 반복되고 server-side 송신 대기와 장시간 connection이 증가한다.
- **영향**: 서버의 response buffer, socket, connection과 worker가 장시간 점유되어 정상 응답 처리가 지연된다.
- **대응**: response write timeout과 송신 대기·동시 connection 제한을 설정하고 reverse proxy에서 비정상 저속 reader를 종료한다. TCP window·connection duration·server send queue를 함께 모니터링한다.

**[답안]** Slow HTTP Read DoS는 작은 TCP receive window 또는 Zero Window로 서버 response 수신을 지연하여 송신 buffer와 connection을 장시간 점유하는 공격이다. 작은/Zero Window와 server-side 송신 대기가 판단 근거이며, write timeout·동시 연결 제한과 reverse proxy를 적용한다.

##### Teardrop

- **정의·원리**: 공격자가 같은 IP datagram에 속하는 fragment의 offset과 길이를 중첩·불일치하게 만들어 취약한 IP 재조립 구현에서 오류를 유발하는 단편화 기반 DoS 공격이다.
- **판단 근거**: 같은 source·destination·protocol·Identification을 가진 단편 사이에 겹치는 범위나 모순된 offset·길이가 있고, 재조립 오류 직후 시스템 정지·재부팅이 발생하는지 확인한다.
- **영향**: 취약한 운영체제의 IP stack이 단편을 잘못 재조립하면서 crash·hang이 발생해 서비스가 거부된다.
- **대응**: 운영체제와 네트워크 장비를 패치하고 방화벽/IPS에서 단편 재조립·정규화를 수행하여 중첩·불일치 단편을 차단·기록한다. 정상 단편 통신이 존재할 수 있으므로 모든 fragment를 일괄 차단하는 것은 업무 영향을 검토해야 한다.

**[답안]** Teardrop은 중첩되거나 모순된 fragment offset을 전송해 취약한 IP 재조립 로직의 오류를 유발하는 공격이다. 같은 Identification의 단편 범위가 겹치고 재조립 오류·crash가 발생하는 것이 근거다. OS·장비 패치와 방화벽/IPS의 단편 재조립·정규화, 비정상 중첩 단편 차단을 적용한다.

##### Land

- **정의·원리**: 출발지와 목적지 IP를 피해자 자신의 주소로 동일하게 위조하고, 전형적으로 TCP SYN의 출발지·목적지 port도 같게 설정해 취약한 시스템이 자기 자신과 연결을 처리하게 만드는 DoS 공격이다.
- **판단 근거**: 외부에서 들어온 패킷인데 `source IP = destination IP = 피해자 IP`이고, 전형적인 예에서 source port와 destination port까지 같은 비정상 tuple인지 확인한다.
- **영향**: 취약한 TCP/IP 구현이 자기 자신에게 응답하거나 연결 상태를 반복 처리하여 CPU·연결 자원을 고갈시키고 시스템이 느려지거나 정지한다.
- **대응**: 취약한 OS·네트워크 장비를 패치하고, 경계에서 외부 interface로 들어오는 내부 source 주소를 차단한다. source와 destination IP·port가 비정상적으로 같은 패킷을 ACL·방화벽/IPS로 필터링하고 로그를 확인한다.

**[답안]** Land 공격은 source와 destination IP를 피해자 주소로 같게 위조하고 전형적으로 TCP port도 동일하게 만들어 피해자가 자기 자신과 통신을 처리하게 하는 DoS 공격이다. 외부 유입 패킷에서 source·destination IP와 port가 동일한 것이 판단 근거다. 패치, ingress filtering, 동일 source/destination tuple 필터링을 적용한다.

##### Ping of Death

- **정의·원리**: 여러 IP fragment를 각각 정상 범위처럼 보내지만 재조립 결과가 IPv4 최대 datagram 크기인 65,535 bytes를 초과하도록 조작해 취약한 IP stack의 길이·buffer 처리를 오동작시키는 DoS 공격이다. 흔히 ICMP Echo를 사용하지만 핵심은 **재조립 후 초과 크기**다.
- **판단 근거**: fragment offset과 payload length를 계산했을 때 재조립 끝 위치가 최대 IP 길이를 넘고, 비정상 ICMP/IP 단편 수신 뒤 crash·reboot가 발생하는지 확인한다. 일반적인 큰 ping이나 정상 MTU 단편화만으로 단정하지 않는다.
- **영향**: 취약한 운영체제에서 buffer overflow·memory corruption·crash가 발생하여 서비스가 중단된다.
- **대응**: 운영체제·네트워크 장비를 패치하고, 방화벽/IPS가 단편을 재조립·정규화한 뒤 초과 크기와 비정상 offset·길이를 차단하도록 한다. ICMP rate limit은 트래픽 완화에 도움이 되지만 재조립 취약점 제거를 대신하지 않는다.

**[답안]** Ping of Death는 IP 단편 재조립 결과가 최대 datagram 크기 65,535 bytes를 넘도록 조작해 취약한 IP stack의 buffer 오류와 crash를 유발하는 공격이다. fragment offset·length 합산 결과의 최대 길이 초과와 직후 장애가 판단 근거다. 패치와 방화벽/IPS의 재조립 검사·정규화, 초과 크기·비정상 단편 차단을 적용한다.

- **DDoS**는 다수 공격원이 한 피해자를 공격한다. **DRDoS**는 출발지를 피해자로 위조해 여러 정상 반사 서버가 피해자에게 증폭 응답을 보내게 한다.
- Slowloris는 HTTP header를 끝내지 않고 천천히 보내며, Slow POST는 message body를 천천히 보내고, Slow Read는 매우 작은 수신 window 또는 Zero Window를 광고해 서버의 응답·연결 자원을 오래 점유한다.
- NTP는 불필요한 외부 질의를 제한하고, 레거시 `monlist`가 제거된 지원 버전으로 갱신하며, 접근제어와 rate limit을 적용한다. 구형 `ntpd`를 즉시 업그레이드할 수 없는 기출 환경에서는 `/etc/ntp.conf`의 `disable monitor`로 monitoring facility를 비활성화하여 `monlist` 악용을 완화한다. 이는 지원 버전 업그레이드를 대신하는 영구 대책이 아니며, 특정 지시자의 지원 여부는 문제의 구현·버전을 우선한다.
- 대응은 한 줄로 끝내지 않는다: `출발지 위조 차단 → 반사 서버 오픈 서비스 제거 → 경계 rate limit/ACL → Anti-DDoS 우회·스크러빙 → 로그 보존·공조` 순으로 쓴다.

**[답안]** “공격명”만 쓰지 말고 `공격자가 무엇을 위조/고갈하는지 → 패킷·로그의 판단 근거 → 서버·네트워크 각 계층의 대응`을 분리하면 서술형 부분점수를 확보하기 쉽다.

## 2.3 [P1] 방화벽·라우터·관리 서비스 보안설정

### 2.3.1 [P1] 방화벽 정책 판독

- 패킷 필터링(Packet Filtering): IP·포트·프로토콜 등 헤더 기준. 빠르지만 응용 내용 판단이 제한된다.
- 상태 기반 검사(Stateful Inspection): 연결 상태를 추적하여 정상 세션에 속하는 패킷인지 판단한다.
- 응용/프록시 방화벽(Application/Proxy Firewall): 응용 프로토콜을 중계·검사한다. 세밀하지만 처리 부하와 구성이 증가한다.
- 기본 원칙: **Default Deny, 최소 허용, 구체적 규칙 우선, 양방향·상태 고려, 변경 승인과 로그 검토**.
- 룰 검토 순서: `방향 → 출발지 → 목적지 → 프로토콜/포트 → 상태 → action → logging → 앞선 shadow rule`.
- `any-any permit`, 불필요한 관리 포트 공개, 사용 종료 규칙, 중복·상충·shadowed rule, 과도한 객체 범위를 점검한다.

### 2.3.2 [P1] Linux iptables

- filter table의 기본 chain:
  - `INPUT`: 로컬 시스템이 최종 목적지
  - `OUTPUT`: 로컬 시스템이 출발지
  - `FORWARD`: 시스템을 경유
- 주요 옵션: `-A` 추가, `-I` 삽입, `-D` 삭제, `-L` 조회, `-p` 프로토콜, `-s/-d` 출발지/목적지, `--sport/--dport` 포트, `-i/-o` 입·출력 인터페이스, `-j` target.

```bash
# 현재 규칙을 번호·카운터와 함께 확인
iptables -L -n -v --line-numbers

# 로컬에서 외부로 나가는 ICMP Echo Request(Type 8) 차단
iptables -A OUTPUT -p icmp --icmp-type 8 -j DROP

# 외부에서 서버의 SSH로 신규 접속하는 관리 IP만 허용하는 예
iptables -A INPUT -p tcp -s 192.0.2.10 --dport 22 \
  -m conntrack --ctstate NEW -j ACCEPT
```

- `DROP`은 응답 없이 폐기하고, `REJECT`는 오류 응답을 돌려준다. 은닉성·클라이언트 지연·운영 요구를 고려해 선택한다.
- 규칙은 위에서 아래로 평가한다. `ACCEPT`, `DROP`, `REJECT` 같은 종결 verdict가 나오면 처리를 끝내지만 `LOG`처럼 기록 후 다음 규칙으로 계속 가는 target도 있으므로 “처음 일치하면 항상 종료”라고 외우지 않는다.
- `--syn`은 일반적으로 SYN만 설정되고 ACK·RST·FIN이 설정되지 않은 연결 시작 패킷과 연결한다. `NEW`인데 `! --syn`인 비정상 TCP를 LOG/DROP하는 유형에서는 `!`의 부정 조건과 **LOG 뒤 실제 차단 규칙**을 함께 확인한다.
- 예시 한 줄만 복사하지 말고 기존 정책·loopback·ESTABLISHED/RELATED·관리 접속 보존 여부를 먼저 확인한다.
- 현대 Linux에서는 nftables가 iptables를 대체하거나 backend로 사용될 수 있다. 시험에 iptables가 제시되면 그 문법으로 답한다.

### 2.3.3 [P1] ACL·Ingress/Egress·uRPF

- Standard ACL: 주로 출발지 IPv4 기준. 전통적 번호 범위는 1~99이며 확장 범위도 존재한다.
- Extended ACL: 출발지·목적지·프로토콜·포트까지 지정한다. 전통적 번호 범위는 100~199이며 확장 범위도 존재한다.
- Cisco wildcard mask는 subnet mask의 bit를 반전한다. `0`은 해당 bit가 반드시 일치, `1`은 무시한다. 예: `/24 → 0.0.0.255`, 특정 host → `0.0.0.0` 또는 `host`, 전체 주소 → `255.255.255.255` 또는 `any`.
- Cisco 계열 numbered ACL의 대표 형태:

```text
access-list 10 permit host 192.0.2.10
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 deny any

access-list 101 deny tcp any host 198.51.100.20 eq 23
access-list 101 permit ip any any
```

- ACL 끝에는 암묵적 `deny any`가 있으므로 허용 규칙 누락과 적용 방향을 확인한다.
- Ingress filtering은 들어오는 패킷의 위조·비정상 출발지를, Egress filtering은 내부에서 나가는 위조·비인가 출발지를 차단한다.
- uRPF는 출발지로 돌아가는 경로의 타당성을 확인한다. Strict mode는 수신 인터페이스와 최적 역경로까지 일치시키므로 비대칭 라우팅에서 정상 트래픽을 막을 수 있고, Loose mode는 출발지로의 경로 존재 여부를 중심으로 본다.

```text
interface GigabitEthernet0/0
 ip verify unicast source reachable-via rx
```

> 위 명령은 Cisco IOS 계열의 대표 예다. 장비·버전에 따라 구문과 지원 모드가 다르므로 시험 지문에 제시된 플랫폼을 우선한다.

### 2.3.4 [P1] 라우터 관리면·트래픽 보안

- 관리면: 기본/공유 계정 제거, 개인별 계정, 강한 secret, AAA, SSH, 관리 IP ACL, 세션 타임아웃, NTP·원격 로그, 설정 백업을 적용한다.
- `enable secret`은 `enable password`보다 우선되고 저장 보호가 강하다. 실제 해시 형식은 IOS·설정에 따라 달라진다. 시험에서는 **평문·Type 7보다 secret을 우선한다**는 목적을 쓰고, 세부 Type 번호 전체는 암기하지 않는다.
- `service password-encryption`의 전통적 Type 7은 가역적 난독화 수준이므로 강한 비밀 저장을 대신하지 못한다.

```text
username netadmin privilege 15 secret <강한-비밀>
ip domain-name example.local
crypto key generate rsa
ip ssh version 2

access-list 10 permit host 192.0.2.10
line vty 0 4
 login local
 transport input ssh
 access-class 10 in
 exec-timeout 5 0
```

- 대표적인 데이터면 보완:

```text
interface GigabitEthernet0/0
 no ip redirects
 no ip directed-broadcast
 no ip unreachables

no ip source-route

interface Null0
 no ip unreachables
ip route 203.0.113.55 255.255.255.255 Null0
```

- `no ip redirects`: 불필요한 ICMP Redirect 송신 방지.
- `no ip directed-broadcast`: Smurf에 악용되는 directed broadcast 전달 방지.
- `no ip unreachables`: 필요 시 정보 노출·반사 응답을 줄이지만 PMTUD와 장애 분석에 영향을 줄 수 있으므로 무조건 적용이 아니라 요구사항을 검토한다.
- Null route/blackhole은 공격 목적지 트래픽을 폐기하지만 정상 서비스도 함께 끊을 수 있다.
- 외부 인터페이스에서 사설·예약 출발지 등 **그 방향에서 올 수 없는 주소**를 차단한다. 내부 인터페이스에 같은 규칙을 잘못 적용하지 않는다.

### 2.3.5 [P1] SNMP 관리 보안

- SNMP는 Manager가 Agent의 MIB 객체를 조회·설정하고, Agent는 Trap/Inform으로 이벤트를 알리는 구조다.
- SNMPv1/v2c는 community string 기반이며 암호화가 없어 평문 노출·추측 위험이 있다.
- SNMPv3는 사용자 기반 보안 모델에서 인증과 프라이버시(암호화)를 제공할 수 있다. 시험에서는 `authPriv`를 가장 강한 보안 수준으로 연결한다.
- **[P2] 확장:** SNMPv3 보안 수준은 `noAuthNoPriv`, `authNoPriv`, `authPriv`로 구분한다. EngineID는 SNMP 엔진을 식별하고, engineBoots·engineTime은 메시지의 시간 적합성을 확인하여 replay를 줄인다. Authentication Parameters는 메시지 출처 인증·무결성, Privacy Parameters는 암호화 처리에 필요한 값을 전달한다.
- 보완: 불필요하면 서비스 제거, 기본 community 변경·RW 금지, 가능하면 SNMPv3 authPriv, 관리 호스트 ACL, 관리망 분리, 최소 OID/View, Trap·로그 점검, 지원 버전·패치 유지.

```text
# 레거시 기본 community 제거의 대표 예
no snmp-server community public
no snmp-server community private
```

> `no snmp-server` 하나를 모든 Cisco 장비의 보편적 제거 명령으로 암기하지 않는다. 실행 중인 설정을 확인하고 해당 community/user/host 구성을 제거한다.

### 2.3.6 [P1] NetBIOS over TCP/IP 노출 점검

- NetBIOS 이름·데이터그램·세션 서비스는 대표적으로 UDP 137, UDP 138, TCP 139를 사용하며, 직접 호스팅 SMB는 TCP 445를 사용한다.
- 인터넷 연결 인터페이스에서 NetBIOS/SMB가 노출되면 컴퓨터·공유 이름 열거, 공유 자원 비인가 접근, 자격증명 공격과 악성코드 확산 위험이 커진다.
- Windows 설정형 답안: `ncpa.cpl → 해당 어댑터 속성 → Internet Protocol Version 4(TCP/IPv4) 속성 → 고급 → WINS → NetBIOS over TCP/IP 사용 안 함`을 선택한다. 업무상 필요가 없으면 137~139/445를 경계 방화벽에서 차단하고 불필요 공유·SMB 버전·권한도 함께 점검한다.

## 2.4 [P1] IDS·IPS·Snort·보안관제

### 2.4.1 [P1] IDS/IPS와 배치

| 구분 | IDS | IPS |
|---|---|---|
| 목적 | 침입 탐지·경보·기록 | 탐지 후 실시간 차단까지 수행 |
| 일반 배치 | TAP/SPAN으로 복제 패킷을 보는 out-of-band | 트래픽 경로의 inline |
| 주요 위험 | 패킷 유실·탐지 누락 | 오탐 시 정상 트래픽 차단, 장애 영향 |

- HIDS는 호스트의 로그·파일·프로세스·시스템 호출 등을, NIDS는 네트워크 패킷·세션을 분석한다.
- 오용(Signature/Misuse) 탐지는 알려진 패턴에 강하고 설명하기 쉬우나 신규·변형 공격에 약하고 룰 갱신이 필요하다.
- 이상(Anomaly) 탐지는 정상 기준에서 벗어난 행위를 찾아 미지 공격 가능성이 있으나 학습·튜닝이 필요하고 오탐이 늘 수 있다.
- False Positive(오탐): 정상인데 공격으로 판단. False Negative(미탐): 공격인데 정상으로 판단.
- IDS가 할 수 있는 대표 행위: 경보, 로그 저장, 세션 reset/연동 차단, 방화벽·SIEM·SOAR 등 다른 통제에 이벤트 전달. 실제 능력은 제품과 구성에 따른다.

### 2.4.2 [P1] Snort 룰 해석

```text
alert tcp $EXTERNAL_NET any -> $HOME_NET 80 \
 (msg:"WEB suspicious request"; flow:to_server,established; \
  content:"attack="; nocase; sid:1000001; rev:1;)
```

- Header: `action protocol source_ip source_port direction destination_ip destination_port`.
- 대표 action: `alert`, `log`, `pass`, `drop`(inline 지원·구성 시).
- Option:
  - `msg`: 경보 메시지
  - `flow`: 세션 방향·상태
  - `content`: 탐지할 문자열·바이트 패턴
  - `nocase`: 영문 대소문자 무시
  - `offset/depth`: payload 시작 기준 검색 위치·범위
  - `distance/within`: 이전 content 이후의 상대 위치·범위
  - `flags`: TCP 플래그 조건
  - `sid/rev`: 룰 식별자·개정 번호
- `->`는 단방향, `<>`는 양방향이다. IP·Port·방향·상태·content 범위를 너무 넓히면 오탐과 성능 부하가 늘고, 너무 좁히면 우회·미탐이 늘어난다.
- 전통적 threshold type의 구분:
  - `limit`: 지정 시간 동안 처음 `count`개까지만 경보한다.
  - `threshold`: 지정 시간 동안 매 `count`번째 이벤트마다 경보한다.
  - `both`: `count`번째에 한 번 경보한 뒤 해당 시간 동안 추가 경보를 억제한다.
- threshold/event_filter 계열은 출발지 또는 목적지 기준으로 경보 빈도를 제어하지만 공격 패킷 자체를 반드시 차단하는 것은 아니다. Snort 세대별 권장 구문이 다르므로 시험 지문의 버전·문법을 따른다.

### 2.4.3 [P1] 로그·패킷 기반 관제 흐름

1. 시간 동기화와 수집 상태를 확인한다.
2. Firewall·IDS/IPS·Router·Switch·AP·서버 로그를 공통 시간축으로 정렬한다.
3. 출발지/목적지 IP·Port·Protocol·action·signature·bytes/packets·session ID를 연결한다.
4. 단일 경보가 아니라 선행 스캔 → 침투 시도 → 성공 여부 → 내부 확산·외부 통신을 확인한다.
5. 차단 전 정상 업무·오탐 가능성을 검토하고, 필요한 경우 세션·IP·계정·도메인을 격리한다.
6. 원본 로그와 패킷을 보존하고, 룰·정책 보완 및 재발 여부를 검증한다.

- SIEM은 여러 원천의 로그를 수집·정규화·상관분석하고 경보·대시보드를 제공한다.
- SOAR은 경보 분류·조회·차단 같은 대응 절차를 playbook으로 연계·자동화한다.
- 보안관제 구성요소형 답안: Agent는 로그 수집·전송, 수집 서버는 저장·정규화·처리, 통합관제 시스템은 상관분석·시각화·대응 지원을 담당한다.

### 2.4.4 [P1/P2] 보안 솔루션 역할 구분

| 솔루션 | 주 관찰·통제 대상 | 한계·구분 포인트 |
|---|---|---|
| Firewall | IP·Port·Protocol·상태·정책 | 허용된 응용 트래픽 내부 공격은 제한적 |
| IDS/IPS | 패킷·세션·시그니처·행위 | IDS는 탐지 중심, IPS는 inline 차단 중심 |
| WAF | HTTP 요청·응답과 웹 공격 패턴 | 일반 네트워크 방화벽을 대체하지 않음 |
| NAC | 단말 인증·상태에 따른 접속 허용·격리 | 네트워크 진입 통제 중심 |
| DLP `[P1 식별]` | 저장·사용·전송 중 중요정보와 반출 경로 | 데이터 식별·정책·endpoint/traffic 가시성이 필요 |
| Anti-DDoS | 비정상 대용량·프로토콜 공격 트래픽 | 탐지 임계치와 우회/스크러빙 연계 필요 |
| Anti-APT/Sandbox | 의심 파일·행위의 격리 실행·분석 | 암호화·우회·지연 실행에 대한 다계층 보완 필요 |

> 제품명보다 **어디에 배치하고, 무엇을 보고, 탐지 후 무엇을 하는지**를 써야 한다.

- WAF: 보호 URL·메서드·파라미터, 탐지/차단 모드, 시그니처·예외, TLS 처리, 우회 접근 경로, 로그 연동을 점검한다.
- DLP(Data Loss Prevention): 중요 문서·개인정보가 저장된 위치와 endpoint에서의 사용, 이동식 매체·메일·메신저·웹 업로드 등 전송 경로를 식별하여 탐지·차단·기록한다. Endpoint DLP는 단말 agent로 파일 사용·복사·암호화 전후 행위를 보고, Network DLP는 센서가 관찰 가능한 트래픽을 검사하며, Discovery DLP는 저장소의 중요정보를 검색·분류한다. HTTPS 내부까지 항상 볼 수 있는 것은 아니므로 endpoint agent 또는 조직이 승인한 복호화 지점이 필요하고, 업무 예외는 승인·기간·대상·로그를 남겨 최소화한다.
- Anti-DDoS: 서비스별 정상 트래픽 기준선·임계치, 프로토콜별 rate limit, 탐지 후 차단/우회·스크러빙 경로, 용량과 장애 시 동작, 경보·원본 로그를 점검한다.
- Anti-APT/Sandbox: 분석 대상 파일·URL·메일 경로, 엔진·시그니처 업데이트, 격리·차단 연동, 암호화 파일·지연 실행의 사각지대, 오탐 예외와 분석 로그를 점검한다.

### 2.4.5 [P2] 대표 점검·분석 도구

| 도구 | 시험에서 구분할 목적 |
|---|---|
| Nessus | 네트워크에 연결된 시스템·서비스의 알려진 취약점을 스캔 |
| Nmap | 호스트 생존 여부, 포트, 서비스·버전 등을 탐색 |
| hping | ICMP·TCP·UDP 패킷을 생성·분석하여 방화벽·네트워크를 점검 |
| Wireshark / tcpdump | 패킷을 캡처하고 프로토콜·세션을 분석 |
| Suricata | 오픈소스 IDS/IPS·네트워크 보안 모니터링 엔진 |
| Honeypot | 공격자를 유인하여 공격 행위와 기법을 관찰하는 기만 자원 |

> P2에서는 설치·전체 옵션이 아니라 `도구명 → 점검 대상 → 결과로 알 수 있는 것`만 연결한다. 승인되지 않은 시스템을 스캔하거나 패킷을 생성해서는 안 된다.

## 2.5 [P1] VPN·IPsec·TLS

### 2.5.1 [P1] VPN과 IPsec 구성

- VPN은 공중망에 인증·암호화된 논리 터널을 구성한다. Site-to-Site는 지점 간, Remote Access는 사용자 단말과 조직망 간 연결에 주로 사용한다.
- PPTP·L2F·L2TP 같은 레거시 터널링 프로토콜은 2.8.3에서 이름과 한계만 확인한다. P1에서는 IPsec 구성요소와 모드 비교를 우선한다.

| 구성요소 | 역할 | 시험 포인트 |
|---|---|---|
| AH | 출발지 인증·무결성·재전송 방지, 기밀성 없음 | IP 헤더의 변경되지 않는 부분도 보호, NAT와 충돌 가능 |
| ESP | 기밀성, 선택/구성에 따른 인증·무결성, 재전송 방지 | 실제 VPN에서 널리 사용 |
| IKE | 피어 인증, 알고리즘·키·SA 협상 | UDP 500, NAT-T는 보통 UDP 4500 |
| SA | 선택된 알고리즘·키·수명 등 보안 매개변수의 단방향 논리 연결 | 양방향 통신에는 SA가 각각 필요 |

- AH와 ESP의 Sequence Number 및 수신 측 anti-replay window는 재전송 공격 탐지에 사용된다.
- SA는 대표적으로 SPI, 목적지 IP, 보안 프로토콜(AH/ESP)로 식별한다.

**[답안]** IPsec은 피어의 **출처 인증**, 전송 데이터의 **무결성**, ESP를 통한 **기밀성**, Sequence Number와 anti-replay window를 통한 **재전송 공격 방지**를 제공한다. AH는 기밀성을 제공하지 않고, 실제 제공 기능은 선택한 AH/ESP와 알고리즘·SA 설정에 따라 달라진다.

### 2.5.2 [P1] IPsec 전송·터널 모드

- 전송 모드: 원래 IP 헤더는 유지하고 상위 payload를 주로 보호한다. 일반적으로 host-to-host에 적합하다.
- 터널 모드: 원래 IP 패킷 전체를 내부 패킷으로 감싸고 새 외부 IP 헤더를 붙인다. 일반적으로 gateway-to-gateway 또는 remote access VPN에 적합하다.

```text
AH  transport: [IP Header][AH][Payload]
AH  tunnel:    [New IP Header][AH][Original IP Header][Payload]
ESP transport: [IP Header][ESP Header][Payload][ESP Trailer][Auth/Tag]
ESP tunnel:    [New IP Header][ESP Header][Original IP Packet][ESP Trailer][Auth/Tag]
```

> ESP의 정확한 무결성 필드·AEAD tag 표현은 알고리즘과 문서 버전에 따라 다르다. 시험에서는 **전송은 원 IP 헤더 노출, 터널은 원 패킷 전체 캡슐화**를 먼저 명확히 쓴다.

### 2.5.3 [P1] TLS 핸드셰이크와 키 역할

- ClientHello/ServerHello: 지원·선택 버전, cipher suite, 난수·키 교환 매개변수를 협상한다.
- Certificate: 서버의 공개키와 신원 결합을 인증기관 서명으로 검증한다.
- (EC)DHE: 임시 키 교환으로 공동 비밀을 만들고 세션키를 파생한다. 인증서 개인키는 서버 서명·인증에 사용된다.
- Finished: 앞선 handshake 메시지와 파생 키의 일치·무결성을 확인한다.
- 이후 Application Data는 효율적인 대칭키로 암호화·무결성 보호한다.
- TLS 1.2의 레거시 RSA key exchange는 premaster secret을 서버 RSA 공개키로 암호화했지만, 현대 구성은 순방향 비밀성을 제공하는 (EC)DHE를 우선한다.

**[답안]** 비대칭키는 서버 인증과 안전한 키 합의에 사용하고, 합의로 파생한 대칭 세션키는 실제 대용량 데이터를 빠르게 암호화·무결성 보호하는 데 사용한다.

### 2.5.4 [P2] TLS 점검 포인트

- SSLv2/v3와 취약한 TLS 버전·cipher suite 비활성화, 신뢰 가능한 인증서·호스트명·유효기간·체인 검증, 안전한 재협상·키 교환, 라이브러리 패치를 점검한다.
- TLS Record 계층은 상위 데이터를 record로 나누고, 협상된 알고리즘에 따라 암호화와 무결성/인증 tag를 적용한다. 압축은 과거 규격 요소였지만 CRIME 같은 정보 노출 위험 때문에 현대 TLS에서는 사용하지 않는다.
- 공격명 연표를 모두 외우기보다 `취약 버전/구성 제거 → 라이브러리 패치 → 인증서·키 교체 가능성 검토 → 로그 점검`의 대응 흐름을 우선한다.

## 2.6 [P2] 무선 네트워크 보안

### 2.6.1 [P2] 무선 동작과 인증·암호화

- 802.11은 충돌을 직접 탐지하기 어려워 CSMA/CA를 사용한다. 채널 감지 후 임의 backoff를 거치고, 선택적으로 RTS/CTS와 NAV로 매체 예약을 알린다.
- RTS의 Duration은 이어질 CTS·DATA·ACK에 필요한 예약 시간을 알리고, CTS 수신 범위의 단말도 남은 Duration으로 NAV를 설정한다. 따라서 숨은 단말이 송신 중인 매체를 방해하는 문제를 줄인다.
- WEP: RC4와 짧은 IV 재사용 등 구조적 취약점이 있어 사용하지 않는다.
- WPA: WEP 개선을 위해 TKIP를 사용한 과도기 방식으로 현재는 사용하지 않는다.
- WPA2: 802.11i 기반, AES-CCMP를 대표적으로 사용한다.
- WPA3-Personal: WPA2-Personal의 PSK 기반 인증·키 파생 대신 SAE(password-authenticated key exchange)를 사용하여 수동 도청 자료를 이용한 오프라인 사전 대입 저항성을 높인다. 지원 환경에서는 강한 암호군과 보호 관리 프레임을 함께 적용한다.
- Personal은 공유 비밀, Enterprise는 802.1X/EAP와 인증 서버를 이용한 사용자별 인증을 중심으로 구분한다.

### 2.6.2 [P2] 무선 장비 점검과 공격 대응

- 기본 SSID·관리자 비밀번호 변경, 관리 인터페이스 외부 노출 차단, 최신 firmware, WPA2-AES 이상, 강한 자격증명, WPS 비활성화, 관리망·사용자망·게스트망 분리를 점검한다.
- Rogue AP/Evil Twin은 승인되지 않았거나 정상 AP를 사칭한 장비다. WIDS/WIPS, 무선 자산 목록, 인증서 검증, 802.1X, 현장 탐지·제거 절차로 대응한다.
- Deauthentication 공격은 관리 프레임을 위조해 연결을 끊는다. 802.11w/PMF를 적용하고 반복 해제 프레임을 탐지한다.
- MAC filtering과 SSID 숨김은 쉽게 우회되므로 핵심 인증·암호화 통제를 대신하지 못한다.

## 2.7 [P1] 실전 답안·점검 체크리스트

### 2.7.1 [P1] 패킷·연결 상태 확인 명령

```bash
# Linux 주소·라우팅·ARP(NDP) 이웃 확인
ip addr
ip route
ip neigh

# 수신 대기 포트와 프로세스 확인
ss -lntup

# 인터페이스·숫자 주소로 패킷 확인
tcpdump -nn -i eth0

# 특정 호스트의 DNS 트래픽 예
tcpdump -nn -i eth0 'host 192.0.2.10 and port 53'

# Windows 연결·ARP·경로 확인
netstat -ano
arp -a
route print
```

- 패킷 필터는 `프로토콜 → 출발지/목적지 → 포트 → TCP flags → 시간·반복량` 순으로 좁힌다.
- `netstat/ss`의 LISTEN은 서비스 대기를 뜻할 뿐 정상·악성을 단정하지 않는다. PID·실행 파일·소유자·설정·변경 이력을 이어서 확인한다.
- `tcpdump`·Wireshark·Nmap·hping 같은 도구는 승인된 점검 환경에서만 사용한다. 시험에서는 도구의 **목적과 결과 해석**을 쓴다.

### 2.7.2 [P1] 설정형 문제 풀이 순서

1. 장비·OS·버전과 설정 위치를 확인한다.
2. 트래픽 방향과 보호 대상 자산을 표시한다.
3. 제시된 룰의 source/destination/protocol/port/state/action을 해석한다.
4. 취약 설정이 만드는 위험을 한 문장으로 쓴다.
5. 최소 허용 원칙으로 보완 룰·설정을 쓴다.
6. 적용 순서, 암묵적 deny, 기존 관리 세션 단절 가능성을 확인한다.
7. 로그·카운터·테스트 패킷으로 조치 결과를 검증한다.
8. 변경자·일시·사유·이전/변경 값·검증 결과·복구 절차를 기록한다.

### 2.7.3 [P1] 공격 분석형 답안 틀

> `관찰 증거`에서 `공격/취약점`을 판단한다. 공격자는 `악용한 필드·프로토콜 동작`을 이용해 `보안 영향`을 일으킨다. 서버/호스트에서는 `패치·서비스·timeout·인증 통제`, 네트워크에서는 `ACL·rate limit·출발지 검증·보안장비`, 관제에서는 `로그 보존·상관분석·재발 탐지`를 적용한다.

- ARP 표: 게이트웨이와 여러 IP가 같은 의심 MAC → ARP spoofing 가능성 → 실제 장비 MAC·스위치 MAC table·DHCP binding 교차 확인 → DAI/port security/암호화.
- SYN 패킷 급증: SYN 대비 완료 ACK 비율과 half-open 상태 증가 → SYN Flooding 판단 → SYN cookie/rate limit/Anti-DDoS.
- UDP 소량 요청 뒤 대용량 응답: 출발지 위조와 다수 반사 서버 → DRDoS → BCP38 성격의 ingress/egress filtering, 오픈 서비스 제한, rate limit.
- IDS 경보 급증: 룰·방향·content·원본 패킷 확인 → 진짜 공격/오탐 판정 → 범위 조정과 차단·튜닝을 분리.

### 2.7.4 [P1/P2] 즉답 체크리스트

- [ ] 주요 서비스의 전송 프로토콜·기본 포트를 연결하고 `/26` 수준의 서브넷을 계산할 수 있다.
- [ ] IPv4 단편화 필드와 ICMP Type 0·3·8·11의 의미를 설명할 수 있다.
- [ ] ARP Request/Reply와 다른 서브넷 통신 시 gateway MAC을 설명할 수 있다.
- [ ] `arp -s <IP> <MAC>`으로 핵심 대상의 정적 ARP를 등록하고 `arp -a`로 검증하는 절차와 한계를 쓴다.
- [ ] TCP 6개 플래그와 3-way handshake의 seq/ack를 쓸 수 있다.
- [ ] RIP·OSPF·EIGRP의 방식·핵심 특징을 구분하고 `show vlan`의 목적을 말할 수 있다.
- [ ] 라우팅 테이블에서 Longest Prefix Match, next-hop/interface, default route를 판독할 수 있다.
- [ ] DNS의 stub/recursive/cache/Root/TLD/Authoritative 흐름과 UDP·TCP 53 사용 조건을 설명할 수 있다.
- [ ] SYN·FIN/NULL/XMAS·UDP scan의 open/closed 응답을 구분한다.
- [ ] ARP spoofing, IP/DNS spoofing, session hijacking의 판단 근거와 대응을 쓴다.
- [ ] SYN Flooding, Smurf, DNS/NTP 증폭, Slow HTTP Header·POST의 서로 다른 판단 근거와 대응을 쓴다.
- [ ] 레거시 `ntpd`의 `disable monitor` 적용 조건과 업그레이드·접근제어·rate limit을 함께 쓴다.
- [ ] VLAN 분리·정적/동적 방식, hopping·MAC flooding 대응을 설명한다.
- [ ] 구성도에서 신뢰 구간·통신 경로·보안장비 배치·위험한 우회 경로를 찾을 수 있다.
- [ ] Firewall 룰의 방향·순서·암묵적 deny와 INPUT/OUTPUT/FORWARD를 구분한다.
- [ ] `iptables -A OUTPUT -p icmp --icmp-type 8 -j DROP`을 방향·프로토콜·ICMP Echo Request·동작으로 해석하고 작성한다.
- [ ] Ingress/Egress filtering, uRPF, blackhole의 목적과 부작용을 설명한다.
- [ ] SNMPv1/v2c와 v3 authPriv, 최소 4가지 보완책을 쓴다.
- [ ] NetBIOS/SMB 노출 위험, 사용 포트, Windows 비활성화 경로를 쓸 수 있다.
- [ ] IDS/IPS, HIDS/NIDS, 오용/이상, 오탐/미탐을 비교한다.
- [ ] `[P1 식별]` 이동식 매체·메일·메신저·웹 업로드의 내부 문서 반출을 agent·network sensor로 탐지·차단하는 솔루션이 DLP임을 식별한다.
- [ ] `[P2 확장]` DLP의 Endpoint·Network·Discovery 방식과 HTTPS 가시성·예외관리 한계를 설명한다.
- [ ] Snort header 7요소와 `content`, `flow`, `sid`, `rev`를 해석한다.
- [ ] AH/ESP/IKE/SA와 IPsec 전송/터널 모드를 비교한다.
- [ ] TLS에서 인증서·비대칭키·(EC)DHE·대칭 세션키의 역할을 구분한다.

## 2.8 [P3] 세부 참고·저빈도 암기

### 2.8.1 [P3] IPv6 핵심

- IPv6는 128비트이며 16진수 8개 그룹으로 표현한다. 선행 0과 연속 0 그룹을 축약할 수 있으며 `::`는 한 주소에서 한 번만 사용한다.
- broadcast가 없고 multicast·anycast를 사용한다. ARP 대신 ICMPv6 기반 NDP가 이웃·라우터 탐색을 담당한다.
- NDP/Router Advertisement spoofing, 불필요한 IPv6 tunnel, extension header 우회가 보안 포인트다. RA Guard, DHCPv6 Guard, IPv6 ACL, 불필요 터널 차단, ICMPv6를 무조건 전부 막지 않는 정책이 필요하다.

### 2.8.2 [P3] 라우터·스위치 확인 명령

```text
show running-config
show access-lists
show ip interface brief
show ip route
show vlan brief
show interfaces trunk
show mac address-table
show logging
```

- Cisco 모드: User EXEC `>`, Privileged EXEC `#`, Global Configuration `(config)#`, Interface/Line 등 세부 Configuration `(config-if)#`, `(config-line)#`.
- 명령 출력에서 먼저 인터페이스 상태, 적용 방향, ACL hit count, trunk/native/allowed VLAN, 관리 프로토콜, 로그 목적지를 확인한다.

### 2.8.3 [P3] 레거시 VPN 용어

| 용어 | 최소 암기 내용 |
|---|---|
| PPTP | PPP를 터널링한 레거시 VPN, 현대 보안 용도로 부적절 |
| L2F | Cisco가 제안한 레거시 2계층 터널링 프로토콜 |
| L2TP | L2 터널 제공, 자체 암호화가 없어 IPsec과 결합 |

### 2.8.4 [P3] 추가 공격·보호 기법

- ICMP Redirect spoofing: 위조 Redirect로 경로를 바꾼다. 호스트의 불필요 Redirect 수용 차단과 라우터 설정·로그를 점검한다.
- DHCP starvation/rogue DHCP: 주소 pool 고갈 또는 위조 서버가 잘못된 gateway/DNS를 배포한다. DHCP Snooping, 신뢰 포트 지정, port security·rate limit을 적용한다.
- STP BPDU spoofing: 공격자가 root bridge가 되어 트래픽 경로를 바꿀 수 있다. Root Guard, BPDU Guard, PortFast 적용 범위를 점검한다.
- DNS zone transfer: 비인가 AXFR로 내부 호스트 정보를 수집한다. 허용된 secondary DNS만 ACL로 제한하고 전송 인증·로그를 적용한다. 상세 `named.conf`는 3장에서 다룬다.
- Fraggle은 Smurf와 유사하게 UDP 서비스를 반사에 악용한다. 불필요 UDP echo/chargen 비활성화와 directed broadcast·출발지 위조 차단을 적용한다.
- WPA/WPA2-Personal의 4-way handshake에는 PSK 자체가 전송되지 않는다. 그러나 약한 passphrase를 사용하면 캡처한 nonce·MAC·MIC와 SSID를 이용해 후보 키를 파생하고 MIC를 대조하는 오프라인 사전 대입이 가능하므로 길고 무작위한 비밀번호 또는 802.1X 기반 Enterprise 인증을 사용한다.

### 2.8.5 [P3] TLS·DTLS 확장

- TLS 1.3의 일반 full handshake는 1-RTT에 응용 데이터 전송을 시작할 수 있고, 재개 시 0-RTT early data를 쓸 수 있다. 0-RTT에는 replay 위험이 있으므로 중복 실행에 민감한 요청에는 허용하지 않는다.
- DTLS는 UDP 위에서 TLS와 유사한 보안을 제공하며 메시지 손실·재정렬·재전송을 고려한다. cookie 교환은 큰 상태를 만들기 전에 발신자 도달 가능성을 확인해 DoS 위험을 줄인다.
- Heartbleed는 OpenSSL heartbeat 길이 검증 결함에 의한 메모리 노출, POODLE은 SSL 3.0 CBC padding oracle, DROWN은 SSLv2 지원을 악용한 cross-protocol 공격이다.

## 2.9 이 장만 보는 최종 회독 순서

### 1회독: 구조 이해

`패킷의 정상 동작(2.1) → 정상 동작의 악용(2.2) → 경계 차단(2.3) → 탐지·관제(2.4) → 암호통신(2.5) → 무선(2.6)` 흐름으로 읽는다.

### 2회독: 백지 회상

아래 질문에 자료 없이 2~4문장으로 답한다.

1. ARP spoofing의 원리·증거·대응은 무엇인가?
2. 정적 ARP 등록·검증 명령과 적용 범위의 한계는 무엇인가?
3. SYN scan에서 열린 포트와 닫힌 포트는 각각 무엇을 응답하는가?
4. DDoS와 DRDoS의 차이는 무엇인가?
5. Smurf와 DNS/NTP 증폭은 출발지 위조를 어떻게 이용하며, 레거시 `ntpd`는 어떻게 보완하는가?
6. VLAN hopping 두 방식과 각각의 대응은 무엇인가?
7. `iptables`의 INPUT·OUTPUT·FORWARD는 어떻게 다르며, outbound ICMP Echo Request 차단 룰은 어떻게 쓰는가?
8. 방화벽 룰을 어떤 순서로 해석하는가?
9. IDS/IPS, HIDS/NIDS, 오용/이상 탐지는 어떻게 다른가?
10. False Positive와 False Negative 중 실제 공격을 놓친 것은 무엇인가?
11. Snort 룰의 header와 option을 어떻게 읽는가?
12. `[P1]` 내부 문서 반출 경로와 agent·network sensor 단서로 DLP를 어떻게 식별하는가? `[P2]` Firewall·WAF·NAC·DLP의 관찰·통제 대상은 어떻게 다른가?
13. SNMPv3 authPriv를 쓰는 이유와 보완책 네 가지는 무엇인가?
14. AH·ESP·IKE·SA의 역할은 무엇인가?
15. IPsec 전송 모드와 터널 모드는 무엇을 보호하는가?
16. TLS 인증서 공개키·임시 키 교환·대칭 세션키의 역할은 무엇인가?
17. 라우팅 테이블에서 Longest Prefix Match와 default route는 어떻게 적용되는가?
18. DNS 질의는 stub resolver에서 Authoritative DNS까지 어떻게 진행되는가?
19. 패킷 한 줄을 보고 공격을 단정하면 안 되는 이유는 무엇인가?

### 3회독: 기출 답안화

- 단답형은 정확한 영문 약어·필드·명령 옵션까지 쓴다.
- 서술형은 `정의/원리 → 판단 근거 → 영향 → 대응` 순으로 3~5개 채점 키워드를 분리한다.
- 설정형은 `방향·대상·조건·동작`을 먼저 표시하고 명령을 쓴 뒤, 룰 순서와 검증 방법을 덧붙인다.
- 틀린 문제는 공격명만 적지 말고 **놓친 패킷 필드·설정 조건·대응 계층**을 이 문서의 해당 P1 항목에 연결한다.

### 완료 조건

- P1 체크리스트를 보지 않고 말하거나 쓸 수 있다.
- ARP·TCP·ICMP·방화벽·Snort·IPsec 문제에서 제시된 값을 근거로 답한다.
- 공격별로 호스트 대응 1개, 네트워크 대응 1개, 관제·검증 1개 이상을 쓴다.
- P3는 P1 답안이 안정된 뒤 남는 시간에 회독한다.
